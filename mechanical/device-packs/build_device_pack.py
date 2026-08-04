#!/usr/bin/env python3
"""Build and verify deterministic PocketForge device print packs.

Committed JSON profiles and OpenSCAD sources are the source of truth. STL
files, manifests, and checksums are generated outputs and are never rewritten
into those sources by this program.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
CRADLE_ROOT = REPO_ROOT / "mechanical" / "dut-cradle-v1"
CRADLE_SCRIPTS = CRADLE_ROOT / "scripts"
CHASSIS_SCRIPTS = (
    REPO_ROOT / "mechanical" / "dut-chassis-2020-v1" / "scripts"
)
sys.path.insert(0, str(CRADLE_SCRIPTS))
sys.path.insert(0, str(CHASSIS_SCRIPTS))

import holder_profiles  # noqa: E402
import check_stl_topology  # noqa: E402
from mesh_fingerprint import (  # noqa: E402
    CANONICAL_ASCII_STL_SCHEMA,
    COORDINATE_QUANTUM_MM,
    FINGERPRINT_ALGORITHM,
    StlError,
    canonicalize_stl,
    describe_mesh,
    read_stl_points,
)


PACK_SCHEMA = "pocketforge-device-print-pack-v2"
LAYOUT_SCHEMA = "pocketforge-device-pack-layout-v1"
LAYOUT_REGISTRY_SCHEMA = "pocketforge-device-layout-registry-v1"
REPOSITORY_URL = "https://github.com/pocketforge-os/test-node-hw"
MODES = ("coupon", "retrofit", "full")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
DEVICE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCAD_INCLUDE_RE = re.compile(r"^\s*(?:include|use)\s*<([^>]+)>", re.MULTILINE)
STL_SERIALIZATION = CANONICAL_ASCII_STL_SCHEMA
DEFAULT_LAYOUT_REGISTRY = Path(
    "mechanical/device-packs/device-layouts.json"
)


class PackError(ValueError):
    """The requested pack or one of its source contracts is invalid."""


@dataclass(frozen=True)
class LayoutArtifact:
    artifact_id: str
    output: PurePosixPath
    role: str
    scope: str
    modes: tuple[str, ...]
    source: Path
    part: str
    parameters: Mapping[str, Any]
    parameter_bindings: Mapping[str, str]
    print_contract: Mapping[str, Any]
    expected_normalized_sha256: str | None


@dataclass(frozen=True)
class ResolvedLayout:
    path: Path
    layout_id: str
    supersedes_layout_id: str | None
    toolchain_lock: Path
    input_paths: tuple[Path, ...]
    artifacts: tuple[LayoutArtifact, ...]
    qualification: Mapping[str, Any]


@dataclass(frozen=True)
class PlanItem:
    artifact_id: str
    output: PurePosixPath
    role: str
    scope: str
    source: Path
    part: str
    parameters: Mapping[str, Any]
    print_contract: Mapping[str, Any]
    expected_normalized_sha256: str | None


@dataclass(frozen=True)
class SourceState:
    commit: str
    dirty: bool


def _reject_constant(token: str) -> None:
    raise PackError(f"JSON contains non-finite number {token}")


def _reject_duplicate_keys(
    pairs: Sequence[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PackError(f"JSON contains duplicate key {key!r}")
        result[key] = value
    return result


def _load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_float=Decimal,
            parse_int=Decimal,
            parse_constant=_reject_constant,
            object_pairs_hook=_reject_duplicate_keys,
        )
    except OSError as exc:
        raise PackError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PackError(
            f"{path}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc


def _object(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise PackError(f"{field} must be an object")
    return value


def _array(value: Any, field: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise PackError(f"{field} must be an array")
    return value


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise PackError(f"{field} must be a non-empty string")
    return value


def _strict_keys(
    value: Mapping[str, Any],
    field: str,
    required: Iterable[str],
    optional: Iterable[str] = (),
) -> None:
    required_set = set(required)
    allowed = required_set | set(optional)
    missing = sorted(required_set - value.keys())
    extra = sorted(value.keys() - allowed)
    if missing:
        raise PackError(f"{field} missing fields: {', '.join(missing)}")
    if extra:
        raise PackError(f"{field} has unknown fields: {', '.join(extra)}")


def _repo_path(root: Path, value: Any, field: str) -> Path:
    text = _string(value, field)
    if "\\" in text:
        raise PackError(f"{field} must use POSIX separators")
    relative = PurePosixPath(text)
    if relative.is_absolute() or ".." in relative.parts:
        raise PackError(f"{field} must stay within the repository")
    path = (root / Path(*relative.parts)).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise PackError(f"{field} escapes the repository: {text}") from exc
    if not path.is_file():
        raise PackError(f"{field} is not an existing file: {text}")
    return path


def _output_path(value: Any, field: str) -> PurePosixPath:
    text = _string(value, field)
    if "\\" in text:
        raise PackError(f"{field} must use POSIX separators")
    path = PurePosixPath(text)
    if (
        path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or path.suffix.lower() != ".stl"
    ):
        raise PackError(f"{field} must be a safe relative .stl path")
    return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise PackError(f"path is outside repository: {path}") from exc


def _validate_parameters(value: Any, field: str) -> Mapping[str, Any]:
    parameters = _object(value, field)
    for name, parameter in parameters.items():
        if not isinstance(name, str) or not re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_]*", name
        ):
            raise PackError(f"{field} has invalid OpenSCAD variable {name!r}")
        try:
            holder_profiles.openscad_literal(parameter)
        except holder_profiles.ProfileError as exc:
            raise PackError(f"{field}.{name}: {exc}") from exc
    return parameters


def _validate_print_contract(value: Any, field: str) -> Mapping[str, Any]:
    contract = _object(value, field)
    _strict_keys(
        contract,
        field,
        {"material", "scale_percent", "supports", "auto_orient", "notes"},
    )
    _string(contract["material"], f"{field}.material")
    if contract["scale_percent"] != 100:
        raise PackError(f"{field}.scale_percent must be 100")
    for name in ("supports", "auto_orient"):
        if not isinstance(contract[name], bool) or contract[name]:
            raise PackError(f"{field}.{name} must be false")
    for index, note in enumerate(_array(contract["notes"], f"{field}.notes")):
        _string(note, f"{field}.notes[{index}]")
    return contract


def _validate_layout_qualification(
    value: Any, field: str
) -> Mapping[str, Any]:
    qualification = _object(value, field)
    _strict_keys(
        qualification,
        field,
        {
            "status",
            "acceptance_ref",
            "accepted_on",
            "device_slugs",
            "scope",
        },
    )
    status = _string(qualification["status"], f"{field}.status")
    if status not in {"candidate", "physically_qualified"}:
        raise PackError(f"{field}.status is unsupported: {status!r}")
    _string(qualification["acceptance_ref"], f"{field}.acceptance_ref")
    accepted_on = qualification["accepted_on"]
    if status == "physically_qualified":
        if not isinstance(accepted_on, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", accepted_on
        ):
            raise PackError(
                f"{field}.accepted_on must be YYYY-MM-DD when qualified"
            )
        try:
            date.fromisoformat(accepted_on)
        except ValueError as exc:
            raise PackError(
                f"{field}.accepted_on is not a real calendar date"
            ) from exc
    elif accepted_on is not None:
        raise PackError(f"{field}.accepted_on must be null while candidate")

    device_slugs = _array(
        qualification["device_slugs"], f"{field}.device_slugs"
    )
    if not device_slugs or len(set(device_slugs)) != len(device_slugs):
        raise PackError(f"{field}.device_slugs must be non-empty and unique")
    for index, slug in enumerate(device_slugs):
        if not isinstance(slug, str) or not DEVICE_SLUG_RE.fullmatch(slug):
            raise PackError(
                f"{field}.device_slugs[{index}] is not a valid device slug"
            )

    scope = _array(qualification["scope"], f"{field}.scope")
    if not scope:
        raise PackError(f"{field}.scope must be non-empty")
    for index, statement in enumerate(scope):
        _string(statement, f"{field}.scope[{index}]")
    return qualification


def load_layout(root: Path, path: Path) -> ResolvedLayout:
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise PackError("layout must be inside the repository") from exc
    document = _object(_load_json(path), str(path))
    _strict_keys(
        document,
        str(path),
        {
            "schema",
            "layout_id",
            "toolchain_lock",
            "input_paths",
            "qualification",
            "artifacts",
        },
        {"supersedes_layout_id"},
    )
    if document["schema"] != LAYOUT_SCHEMA:
        raise PackError(f"{path}.schema must be {LAYOUT_SCHEMA!r}")
    layout_id = _string(document["layout_id"], f"{path}.layout_id")
    if not ID_RE.fullmatch(layout_id.replace("-", "_")):
        raise PackError(f"{path}.layout_id has invalid format")
    supersedes_layout_id = document.get("supersedes_layout_id")
    if supersedes_layout_id is not None:
        supersedes_layout_id = _string(
            supersedes_layout_id, f"{path}.supersedes_layout_id"
        )
        if not ID_RE.fullmatch(supersedes_layout_id.replace("-", "_")):
            raise PackError(f"{path}.supersedes_layout_id has invalid format")
        if supersedes_layout_id == layout_id:
            raise PackError(
                f"{path}.supersedes_layout_id must name an older layout"
            )
    toolchain_lock = _repo_path(
        root, document["toolchain_lock"], f"{path}.toolchain_lock"
    )
    input_paths = tuple(
        _repo_path(root, value, f"{path}.input_paths[{index}]")
        for index, value in enumerate(
            _array(document["input_paths"], f"{path}.input_paths")
        )
    )

    artifacts: list[LayoutArtifact] = []
    seen_ids: set[str] = set()
    seen_outputs: set[PurePosixPath] = set()
    for index, raw in enumerate(_array(document["artifacts"], f"{path}.artifacts")):
        field = f"{path}.artifacts[{index}]"
        artifact = _object(raw, field)
        _strict_keys(
            artifact,
            field,
            {
                "id",
                "output",
                "role",
                "scope",
                "modes",
                "source",
                "part",
                "parameters",
                "parameter_bindings",
                "print",
            },
            {"expected_normalized_sha256"},
        )
        artifact_id = _string(artifact["id"], f"{field}.id")
        if not ID_RE.fullmatch(artifact_id):
            raise PackError(f"{field}.id has invalid format")
        if artifact_id in seen_ids:
            raise PackError(f"{field}.id duplicates {artifact_id!r}")
        seen_ids.add(artifact_id)
        output = _output_path(artifact["output"], f"{field}.output")
        if output in seen_outputs:
            raise PackError(f"{field}.output duplicates {output.as_posix()!r}")
        seen_outputs.add(output)
        role = _string(artifact["role"], f"{field}.role")
        scope = _string(artifact["scope"], f"{field}.scope")
        if scope not in {"calibration", "common", "device"}:
            raise PackError(f"{field}.scope is unsupported: {scope!r}")
        modes = tuple(
            _string(value, f"{field}.modes[{mode_index}]")
            for mode_index, value in enumerate(
                _array(artifact["modes"], f"{field}.modes")
            )
        )
        if not modes or len(set(modes)) != len(modes):
            raise PackError(f"{field}.modes must be non-empty and unique")
        if any(mode not in MODES for mode in modes):
            raise PackError(f"{field}.modes contains an unsupported mode")
        source = _repo_path(root, artifact["source"], f"{field}.source")
        if source.suffix != ".scad":
            raise PackError(f"{field}.source must be an OpenSCAD file")
        part = _string(artifact["part"], f"{field}.part")
        if not ID_RE.fullmatch(part):
            raise PackError(f"{field}.part has invalid format")
        parameters = _validate_parameters(
            artifact["parameters"], f"{field}.parameters"
        )
        bindings = _object(
            artifact["parameter_bindings"], f"{field}.parameter_bindings"
        )
        for name, binding in bindings.items():
            if not isinstance(name, str) or not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*", name
            ):
                raise PackError(
                    f"{field}.parameter_bindings has invalid variable {name!r}"
                )
            if binding != "device.display_name":
                raise PackError(
                    f"{field}.parameter_bindings.{name} has unsupported "
                    f"binding {binding!r}"
                )
        overlap = sorted(set(parameters) & set(bindings))
        if overlap:
            raise PackError(
                f"{field} binds and sets the same parameter(s): {', '.join(overlap)}"
            )
        expected = artifact.get("expected_normalized_sha256")
        if expected is not None and (
            not isinstance(expected, str) or not SHA256_RE.fullmatch(expected)
        ):
            raise PackError(
                f"{field}.expected_normalized_sha256 must be lowercase SHA-256"
            )
        artifacts.append(
            LayoutArtifact(
                artifact_id=artifact_id,
                output=output,
                role=role,
                scope=scope,
                modes=modes,
                source=source,
                part=part,
                parameters=parameters,
                parameter_bindings=bindings,
                print_contract=_validate_print_contract(
                    artifact["print"], f"{field}.print"
                ),
                expected_normalized_sha256=expected,
            )
        )
    if not artifacts:
        raise PackError(f"{path}.artifacts must not be empty")
    qualification = _validate_layout_qualification(
        document["qualification"], f"{path}.qualification"
    )
    return ResolvedLayout(
        path=path,
        layout_id=layout_id,
        supersedes_layout_id=supersedes_layout_id,
        toolchain_lock=toolchain_lock,
        input_paths=input_paths,
        artifacts=tuple(artifacts),
        qualification=qualification,
    )


def load_layout_registry(root: Path, path: Path) -> Mapping[str, Path]:
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise PackError("layout registry must be inside the repository") from exc
    document = _object(_load_json(path), str(path))
    _strict_keys(document, str(path), {"schema", "devices"})
    if document["schema"] != LAYOUT_REGISTRY_SCHEMA:
        raise PackError(
            f"{path}.schema must be {LAYOUT_REGISTRY_SCHEMA!r}"
        )
    devices = _object(document["devices"], f"{path}.devices")
    if not devices:
        raise PackError(f"{path}.devices must not be empty")
    resolved: dict[str, Path] = {}
    for slug, raw in devices.items():
        if not isinstance(slug, str) or not DEVICE_SLUG_RE.fullmatch(slug):
            raise PackError(f"{path}.devices has invalid slug {slug!r}")
        field = f"{path}.devices.{slug}"
        record = _object(raw, field)
        _strict_keys(record, field, {"layout"})
        resolved[slug] = _repo_path(
            root, record["layout"], f"{field}.layout"
        )
    return resolved


def guard_qualified_layouts(
    root: Path,
    base_root: Path,
    *,
    registry_path: Path = DEFAULT_LAYOUT_REGISTRY,
) -> tuple[int, int, int]:
    """Protect qualified layouts and require staged candidate promotion.

    A physically qualified layout is immutable by version: any geometry,
    parameter, print-contract, or even formatting change must be introduced
    under a new candidate layout ID. A device may move from that frozen record
    only to a layout that explicitly names it with supersedes_layout_id and
    includes the device in its qualification scope. Candidate-to-qualified
    promotion may change only the qualification record, ensuring the physically
    inspected candidate and the promoted source contract are identical.

    Layouts that predate the qualification field are admitted once as a
    bootstrap.  After that bootstrap lands, the ordinary immutable rule
    protects them on every later pull request.
    """

    root = root.resolve()
    base_root = base_root.resolve()
    if not base_root.is_dir():
        raise PackError(
            f"qualified-layout base root is not a directory: {base_root}"
        )
    registry = (
        registry_path.resolve()
        if registry_path.is_absolute()
        else (root / registry_path).resolve()
    )
    mappings = load_layout_registry(root, registry)
    layouts_relative = Path("mechanical/device-packs/layouts")
    base_layouts = base_root / layouts_relative
    if not base_layouts.is_dir():
        raise PackError(
            "qualified-layout base is missing mechanical/device-packs/layouts"
        )

    locked = 0
    for base_path in sorted(base_layouts.glob("*.json")):
        base_document = _object(_load_json(base_path), str(base_path))
        qualification = base_document.get("qualification")
        if (
            not isinstance(qualification, dict)
            or qualification.get("status") != "physically_qualified"
        ):
            continue
        layout_id = _string(
            base_document.get("layout_id"), f"{base_path}.layout_id"
        )
        relative = base_path.relative_to(base_root)
        head_path = root / relative
        if not head_path.is_file():
            raise PackError(
                f"qualified layout {layout_id!r} was removed; qualified "
                "layout versions are immutable"
            )
        if base_path.read_bytes() != head_path.read_bytes():
            raise PackError(
                f"qualified layout {layout_id!r} changed; create a new "
                "candidate layout ID instead of editing a physically "
                "qualified version"
            )
        device_slugs = _array(
            qualification.get("device_slugs"),
            f"{base_path}.qualification.device_slugs",
        )
        for index, slug_value in enumerate(device_slugs):
            slug = _string(
                slug_value,
                f"{base_path}.qualification.device_slugs[{index}]",
            )
            registered = mappings.get(slug)
            if registered != head_path.resolve():
                successor = (
                    load_layout(root, registered)
                    if registered is not None
                    else None
                )
                if (
                    successor is not None
                    and successor.supersedes_layout_id == layout_id
                    and slug in successor.qualification["device_slugs"]
                ):
                    continue
                registered_text = (
                    "<unmapped>"
                    if registered is None
                    else _relative(root, registered)
                )
                raise PackError(
                    f"qualified device {slug!r} was remapped from "
                    f"{relative.as_posix()!r} to {registered_text!r}; "
                    "the proven device/layout mapping is immutable"
                )
        locked += 1

    promotions = 0
    bootstraps = 0
    for head_path in sorted(set(mappings.values())):
        head_layout = load_layout(root, head_path)
        if head_layout.qualification["status"] != "physically_qualified":
            continue
        relative = head_path.relative_to(root)
        base_path = base_root / relative
        if not base_path.is_file():
            raise PackError(
                f"new layout {head_layout.layout_id!r} cannot begin as "
                "physically qualified; land it as a candidate first"
            )
        base_document = _object(_load_json(base_path), str(base_path))
        base_qualification = base_document.get("qualification")
        if (
            isinstance(base_qualification, dict)
            and base_qualification.get("status") == "physically_qualified"
        ):
            continue
        if (
            isinstance(base_qualification, dict)
            and base_qualification.get("status") == "candidate"
        ):
            head_document = _object(_load_json(head_path), str(head_path))
            base_contract = {
                key: value
                for key, value in base_document.items()
                if key != "qualification"
            }
            head_contract = {
                key: value
                for key, value in head_document.items()
                if key != "qualification"
            }
            if base_contract != head_contract:
                raise PackError(
                    f"layout {head_layout.layout_id!r} changed its source "
                    "contract while being promoted; land candidate geometry "
                    "first, physically accept that exact revision, then "
                    "change only qualification"
                )
            promotions += 1
            continue
        if base_qualification is None:
            bootstraps += 1
            continue
        raise PackError(
            f"layout {head_layout.layout_id!r} has unsupported qualification "
            "transition to physically_qualified"
        )

    print(
        "qualified_layout_guard=pass "
        f"locked={locked} promotions={promotions} bootstraps={bootstraps}"
    )
    return locked, promotions, bootstraps


def resolve_device_layout(
    root: Path,
    device_slug: str,
    *,
    registry_path: Path = DEFAULT_LAYOUT_REGISTRY,
    requested_layout: Path | None = None,
) -> ResolvedLayout:
    root = root.resolve()
    if not DEVICE_SLUG_RE.fullmatch(device_slug):
        raise PackError(f"invalid device slug: {device_slug!r}")
    registry = (
        registry_path.resolve()
        if registry_path.is_absolute()
        else (root / registry_path).resolve()
    )
    mappings = load_layout_registry(root, registry)
    registered = mappings.get(device_slug)
    if registered is None:
        choices = ", ".join(sorted(mappings))
        raise PackError(
            f"device {device_slug!r} has no registered chassis layout; "
            f"choose one of: {choices}"
        )
    if requested_layout is not None:
        requested = (
            requested_layout.resolve()
            if requested_layout.is_absolute()
            else (root / requested_layout).resolve()
        )
        if requested != registered:
            raise PackError(
                f"requested layout {_relative(root, requested)!r} does not "
                f"match registered layout {_relative(root, registered)!r} "
                f"for {device_slug}"
            )
    layout = load_layout(root, registered)
    if registry not in layout.input_paths:
        raise PackError(
            f"layout {_relative(root, registered)!r} must list registry "
            f"{_relative(root, registry)!r} in input_paths"
        )
    if device_slug not in layout.qualification["device_slugs"]:
        raise PackError(
            f"layout {layout.layout_id!r} qualification does not cover "
            f"device {device_slug!r}"
        )
    return layout


def device_layout_matrix(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
    *,
    registry_path: Path = DEFAULT_LAYOUT_REGISTRY,
    kind: str,
) -> dict[str, list[dict[str, str]]]:
    if kind not in {
        "production-devices",
        "candidate-layout-devices",
    }:
        raise PackError(f"unsupported device layout matrix kind: {kind!r}")
    holder_status = profile.document["qualification"]["status"]
    include: list[dict[str, str]] = []
    for slug in sorted(profile.variants):
        layout = resolve_device_layout(
            root, slug, registry_path=registry_path
        )
        layout_status = layout.qualification["status"]
        production_ready = (
            holder_status == "physically_qualified"
            and layout_status == "physically_qualified"
        )
        selected = (
            production_ready
            if kind == "production-devices"
            else layout_status != "physically_qualified"
        )
        if selected:
            include.append(
                {
                    "device_slug": slug,
                    "layout_id": layout.layout_id,
                    "layout_status": layout_status,
                    "holder_status": holder_status,
                }
            )
    return {"include": include}


def discover_device_profiles(
    root: Path,
) -> dict[str, holder_profiles.ResolvedProfile]:
    cradle_root = root.resolve() / "mechanical" / "dut-cradle-v1"
    devices: dict[str, holder_profiles.ResolvedProfile] = {}
    for profile_path in holder_profiles.discover_profiles(cradle_root):
        profile = holder_profiles.validate_profile(cradle_root, profile_path)
        for slug in profile.variants:
            if slug in devices:
                raise PackError(
                    f"device {slug!r} belongs to more than one holder profile"
                )
            devices[slug] = profile
    if not devices:
        raise PackError("no holder device variants were discovered")
    return devices


def all_device_layout_matrix(
    root: Path,
    *,
    registry_path: Path = DEFAULT_LAYOUT_REGISTRY,
    kind: str,
) -> dict[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    profiles = discover_device_profiles(root)
    for slug in sorted(profiles):
        profile = profiles[slug]
        one = device_layout_matrix(
            root,
            profile,
            registry_path=registry_path,
            kind=kind,
        )
        rows.extend(row for row in one["include"] if row["device_slug"] == slug)
    rows.sort(key=lambda row: row["device_slug"])
    return {"include": rows}


def _qualification_expected(
    profile: holder_profiles.ResolvedProfile, artifact_name: str
) -> str | None:
    if profile.qualification_manifest is None:
        return None
    artifact = profile.qualification_manifest["artifacts"].get(artifact_name)
    if not isinstance(artifact, dict):
        raise PackError(
            f"qualification manifest is missing artifact {artifact_name!r}"
        )
    expected = artifact.get("expected")
    if not isinstance(expected, dict):
        raise PackError(
            f"qualification artifact {artifact_name!r} has no expected metrics"
        )
    fingerprint = expected.get("fingerprint")
    if not isinstance(fingerprint, dict):
        raise PackError(
            f"qualification artifact {artifact_name!r} has no fingerprint"
        )
    value = fingerprint.get("sha256")
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise PackError(
            f"qualification artifact {artifact_name!r} has invalid SHA-256"
        )
    return value


def _profile_item(
    profile: holder_profiles.ResolvedProfile,
    *,
    artifact_id: str,
    output: str,
    role: str,
    recipe: Mapping[str, Any],
    expected_artifact: str | None = None,
    print_notes: Sequence[str] = (),
) -> PlanItem:
    source = (profile.root / recipe["source"]).resolve()
    parameters = holder_profiles.recipe_parameters(profile, recipe)
    return PlanItem(
        artifact_id=artifact_id,
        output=PurePosixPath(output),
        role=role,
        scope="device",
        source=source,
        part=recipe["part"],
        parameters=parameters,
        print_contract={
            "material": "PETG",
            "scale_percent": 100,
            "supports": False,
            "auto_orient": False,
            "notes": list(print_notes),
        },
        expected_normalized_sha256=(
            _qualification_expected(profile, expected_artifact)
            if expected_artifact is not None
            else None
        ),
    )


def build_plan(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    device_slug: str,
    mode: str,
) -> tuple[PlanItem, ...]:
    if mode not in MODES:
        raise PackError(f"unsupported pack mode: {mode!r}")
    implementation_kind = profile.document["implementation"]["kind"]
    if implementation_kind not in {"declarative", "custom_openscad"}:
        raise PackError(
            f"unsupported holder implementation kind: {implementation_kind!r}"
        )
    required_profile_artifacts = {"fit_coupon"}
    if mode in {"retrofit", "full"}:
        required_profile_artifacts.add("j_hook_set")
    missing_profile_artifacts = sorted(
        required_profile_artifacts - set(profile.artifacts)
    )
    if missing_profile_artifacts:
        raise PackError(
            "holder profile is missing required pack artifact(s): "
            + ", ".join(missing_profile_artifacts)
        )
    variant = profile.variants.get(device_slug)
    if not isinstance(variant, dict):
        choices = ", ".join(sorted(profile.variants))
        raise PackError(
            f"device {device_slug!r} is not mapped by profile "
            f"{profile.document['profile_id']!r}; choose one of: {choices}"
        )
    if device_slug not in layout.qualification["device_slugs"]:
        raise PackError(
            f"layout {layout.layout_id!r} qualification does not cover "
            f"device {device_slug!r}"
        )

    items = [
        _profile_item(
            profile,
            artifact_id="holder_fit_coupon",
            output="coupon/holder-fit-coupon.stl",
            role="Fit coupon for the selected holder mechanism",
            recipe=profile.artifacts["fit_coupon"],
            expected_artifact="fit_coupon",
            print_notes=(
                "Use the same material and process intended for the carrier "
                "and hooks.",
            ),
        )
    ]
    if mode in {"retrofit", "full"}:
        items.extend(
            [
                _profile_item(
                    profile,
                    artifact_id="device_carrier",
                    output="device/carrier.stl",
                    role="Device-labeled DUT carrier",
                    recipe=variant["production_carrier"],
                    print_notes=(
                        "Print flat with labels upward; change to the label "
                        "color at 3.2 mm.",
                    ),
                ),
                _profile_item(
                    profile,
                    artifact_id="device_j_hook_set",
                    output="device/j-hook-set.stl",
                    role="Complete retention set for the selected carrier",
                    recipe=profile.artifacts["j_hook_set"],
                    expected_artifact="j_hook_set",
                    print_notes=(
                        "The retention parts are already exported on their "
                        "strong printing side; use the profile's documented "
                        "quantities.",
                    ),
                ),
            ]
        )

    display_name = variant["display_name"]
    for artifact in layout.artifacts:
        if mode not in artifact.modes:
            continue
        parameters = dict(artifact.parameters)
        for name, binding in artifact.parameter_bindings.items():
            if binding == "device.display_name":
                parameters[name] = display_name
        parameters["PART"] = artifact.part
        items.append(
            PlanItem(
                artifact_id=artifact.artifact_id,
                output=artifact.output,
                role=artifact.role,
                scope=artifact.scope,
                source=artifact.source,
                part=artifact.part,
                parameters=parameters,
                print_contract=artifact.print_contract,
                expected_normalized_sha256=artifact.expected_normalized_sha256,
            )
        )

    ordered = tuple(sorted(items, key=lambda item: item.output.as_posix()))
    outputs = [item.output for item in ordered]
    ids = [item.artifact_id for item in ordered]
    if len(outputs) != len(set(outputs)) or len(ids) != len(set(ids)):
        raise PackError("profile and layout produce duplicate artifact IDs or paths")
    profile_count = 3 if mode in {"retrofit", "full"} else 1
    layout_count = sum(mode in artifact.modes for artifact in layout.artifacts)
    expected_count = profile_count + layout_count
    if len(ordered) != expected_count:
        raise PackError(
            f"{mode} layout must contain exactly {expected_count} "
            f"artifacts, found {len(ordered)}"
        )
    for item in ordered:
        try:
            item.source.resolve().relative_to(root.resolve())
        except ValueError as exc:
            raise PackError(
                f"artifact source escapes repository: {item.source}"
            ) from exc
    return ordered


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        diagnostic = "\n".join(
            part.strip() for part in (result.stdout, result.stderr) if part.strip()
        )
        raise PackError(f"git {' '.join(args)} failed: {diagnostic}")
    return result.stdout.strip()


def source_state(root: Path) -> SourceState:
    top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    if top != root.resolve():
        raise PackError(f"repository root mismatch: expected {root}, got {top}")
    commit = _git(root, "rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise PackError(f"git returned an invalid commit: {commit!r}")
    dirty = bool(
        _git(
            root,
            "status",
            "--porcelain=v1",
            "--untracked-files=normal",
            "--",
            ".",
        )
    )
    return SourceState(commit=commit, dirty=dirty)


def _policy(
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    mode: str,
    state: SourceState,
    *,
    allow_dirty: bool,
    allow_unqualified: bool,
) -> tuple[bool, list[str], list[str]]:
    holder_qualified = (
        profile.document["qualification"]["status"] == "physically_qualified"
    )
    layout_qualified = (
        layout.qualification["status"] == "physically_qualified"
    )
    if state.dirty and not allow_dirty:
        raise PackError(
            "source tree is dirty; commit the source or pass --allow-dirty "
            "for a non-production pack"
        )
    holder_blocks = not holder_qualified and mode != "coupon"
    layout_blocks = not layout_qualified and mode == "full"
    if (holder_blocks or layout_blocks) and not allow_unqualified:
        requirements = []
        if holder_blocks:
            requirements.append("holder geometry")
        if layout_blocks:
            requirements.append("chassis layout")
        raise PackError(
            f"{mode} packs require physically qualified "
            f"{' and '.join(requirements)}; "
            "pass --allow-unqualified only for a non-production prototype"
        )

    overrides: set[str] = set()
    reasons: list[str] = []
    if state.dirty:
        overrides.add("allow_dirty")
        reasons.append("dirty_source")
    if not holder_qualified:
        if mode != "coupon":
            overrides.add("allow_unqualified")
        reasons.append("holder_unqualified")
    if not layout_qualified and mode == "full":
        overrides.add("allow_unqualified")
        reasons.append("layout_unqualified")
    if mode == "coupon":
        reasons.append("coupon_only")
    production_eligible = not reasons
    return production_eligible, sorted(overrides), sorted(reasons)


def _scad_closure(root: Path, initial: Iterable[Path]) -> set[Path]:
    pending = list(initial)
    seen: set[Path] = set()
    while pending:
        path = pending.pop().resolve()
        if path in seen:
            continue
        try:
            path.relative_to(root.resolve())
        except ValueError as exc:
            raise PackError(f"OpenSCAD input escapes repository: {path}") from exc
        if not path.is_file():
            raise PackError(f"OpenSCAD input is missing: {_relative(root, path)}")
        seen.add(path)
        if path.suffix != ".scad":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise PackError(f"cannot read OpenSCAD input {path}: {exc}") from exc
        for include in SCAD_INCLUDE_RE.findall(text):
            candidate = (path.parent / include).resolve()
            if not candidate.is_file():
                candidate = (root / include).resolve()
            if not candidate.is_file():
                raise PackError(
                    f"{_relative(root, path)} includes missing source {include!r}"
                )
            pending.append(candidate)
    return seen


def _input_paths(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    plan: Sequence[PlanItem],
) -> list[Path]:
    paths: set[Path] = {
        Path(__file__).resolve(),
        layout.path.resolve(),
        layout.toolchain_lock.resolve(),
        profile.path.resolve(),
        profile.root / "scripts" / "holder_profiles.py",
        profile.root / "scripts" / "mesh_fingerprint.py",
        profile.root / "scripts" / "qualified_geometry.py",
        CHASSIS_SCRIPTS / "check_stl_topology.py",
        profile.root / profile.document["fixture"]["lock"],
        *layout.input_paths,
    }
    scad_paths = {item.source.resolve() for item in plan}
    implementation = profile.document["implementation"]
    scad_paths.add((profile.root / implementation["source"]).resolve())
    for recipe in profile.artifacts.values():
        scad_paths.add((profile.root / recipe["source"]).resolve())
    for variant in profile.variants.values():
        scad_paths.add(
            (
                profile.root / variant["production_carrier"]["source"]
            ).resolve()
        )
    paths.update(_scad_closure(root, scad_paths))

    if profile.qualification_manifest is not None:
        qualification_path = (
            profile.root / profile.document["qualification"]["geometry_manifest"]
        ).resolve()
        paths.add(qualification_path)
        manifest = profile.qualification_manifest
        paths.add((profile.root / manifest["toolchain_lock"]).resolve())
        for index, item in enumerate(manifest.get("source_inputs", [])):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise PackError(
                    f"qualification source_inputs[{index}] has invalid path"
                )
            paths.add((profile.root / item["path"]).resolve())

    for path in paths:
        try:
            path.resolve().relative_to(root.resolve())
        except ValueError as exc:
            raise PackError(f"pack input escapes repository: {path}") from exc
        if not path.is_file():
            raise PackError(f"pack input is missing: {_relative(root, path)}")
    return sorted((path.resolve() for path in paths), key=lambda p: _relative(root, p))


def _input_manifest(root: Path, paths: Sequence[Path]) -> list[dict[str, str]]:
    return [
        {"path": _relative(root, path), "sha256": _sha256(path)}
        for path in paths
    ]


def _definitions(parameters: Mapping[str, Any]) -> dict[str, str]:
    return {
        name: holder_profiles.openscad_literal(parameters[name])
        for name in sorted(parameters)
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    if isinstance(value, dict):
        return {key: _json_safe(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(child) for child in value]
    return value


def _command(item: PlanItem, output: Path, openscad: str) -> list[str]:
    command = [
        openscad,
        "--hardwarnings",
        "--check-parameters=true",
        "--check-parameter-ranges=true",
        "-o",
        str(output.resolve()),
    ]
    for name, literal in _definitions(item.parameters).items():
        command.extend(["-D", f"{name}={literal}"])
    command.append(str(item.source.resolve()))
    return command


def _decimal_text(value: Decimal) -> str:
    """Compatibility helper used by serialization regression fixtures."""
    if value == 0:
        return "0"
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered


def _canonicalize_stl(path: Path) -> None:
    """Replace an STL with a deterministic, geometry-preserving ASCII form."""
    try:
        canonicalize_stl(path)
    except (OSError, StlError) as exc:
        raise PackError(f"cannot canonicalize STL {path.name}: {exc}") from exc


def _render(item: PlanItem, output: Path, openscad: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            _command(item, output, openscad),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise PackError(f"cannot run {openscad!r}: {exc}") from exc
    diagnostic = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    errors = [
        line for line in diagnostic.splitlines() if line.startswith("ERROR:")
    ]
    if result.returncode != 0 or errors:
        raise PackError(
            f"OpenSCAD failed for {item.artifact_id} "
            f"rc={result.returncode}: {diagnostic}"
        )
    if not output.is_file() or output.stat().st_size == 0:
        raise PackError(
            f"OpenSCAD produced no non-empty output for {item.artifact_id}"
        )


def _artifact_record(
    root: Path, item: PlanItem, path: Path
) -> dict[str, Any]:
    try:
        normalized = describe_mesh(path)
    except (OSError, StlError) as exc:
        raise PackError(f"{item.artifact_id} is not a valid STL: {exc}") from exc
    try:
        topology_validation = check_stl_topology.inspect_topology(path)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise PackError(
            f"{item.artifact_id} topology check failed: {exc}"
        ) from exc
    if (
        topology_validation["invalid_edges"]
        or topology_validation["degenerate_facets"]
    ):
        raise PackError(
            f"{item.artifact_id} is not closed and manifold: "
            f"invalid_edges={topology_validation['invalid_edges']} "
            f"degenerate_facets={topology_validation['degenerate_facets']}"
        )
    actual_fingerprint = normalized["fingerprint"]["sha256"]
    if (
        item.expected_normalized_sha256 is not None
        and actual_fingerprint != item.expected_normalized_sha256
    ):
        raise PackError(
            f"{item.artifact_id} normalized geometry drift: expected "
            f"{item.expected_normalized_sha256}, got {actual_fingerprint}"
        )
    return {
        "id": item.artifact_id,
        "path": item.output.as_posix(),
        "role": item.role,
        "scope": item.scope,
        "generation": {
            "source": _relative(root, item.source),
            "part": item.part,
            "definitions": _definitions(item.parameters),
            "expected_normalized_sha256": item.expected_normalized_sha256,
        },
        "print": _json_safe(item.print_contract),
        "raw": {
            "sha256": _sha256(path),
            "size_bytes": path.stat().st_size,
        },
        "normalized": normalized,
        "manifold_validation": {
            "algorithm": "rounded-stl-edge-incidence-v1",
            "decimal_places_mm": 6,
            **topology_validation,
        },
    }


def _toolchain_record(root: Path, layout: ResolvedLayout) -> dict[str, str]:
    lock = _object(_load_json(layout.toolchain_lock), str(layout.toolchain_lock))
    version = _string(
        lock.get("openscad_reported_version"),
        f"{layout.toolchain_lock}.openscad_reported_version",
    )
    return {
        "lock": _relative(root, layout.toolchain_lock),
        "lock_sha256": _sha256(layout.toolchain_lock),
        "openscad_reported_version": version,
    }


def _qualification_record(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
) -> dict[str, Any]:
    qualification = profile.document["qualification"]
    manifest_record: dict[str, Any] | None = None
    accepted_source_revision: str | None = None
    characterized_source_revision: str | None = None
    manifest_status: str | None = None
    if profile.qualification_manifest is not None:
        manifest_path = (
            profile.root / qualification["geometry_manifest"]
        ).resolve()
        manifest_qualification = _object(
            profile.qualification_manifest["qualification"],
            "qualification manifest.qualification",
        )
        manifest_record = {
            "path": _relative(root, manifest_path),
            "sha256": _sha256(manifest_path),
            "schema": profile.qualification_manifest["schema"],
        }
        accepted_source_revision = manifest_qualification[
            "accepted_source_revision"
        ]
        characterized_source_revision = manifest_qualification[
            "characterized_source_revision"
        ]
        manifest_status = manifest_qualification["status"]
    return {
        "status": qualification["status"],
        "manifest_status": manifest_status,
        "manifest": manifest_record,
        "acceptance_ref": qualification["acceptance_ref"],
        "accepted_on": qualification["accepted_on"],
        "accepted_geometry_revision": qualification[
            "accepted_geometry_revision"
        ],
        "accepted_source_revision": accepted_source_revision,
        "characterized_source_revision": characterized_source_revision,
        "fixture_interface_sha256": qualification[
            "fixture_interface_sha256"
        ],
    }


def _fixture_record(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
) -> dict[str, Any]:
    lock_path = (profile.root / profile.document["fixture"]["lock"]).resolve()
    source = _object(profile.lock["source"], "fixture lock.source")
    return {
        "lock": {
            "path": _relative(root, lock_path),
            "sha256": _sha256(lock_path),
            "schema": profile.lock["schema"],
        },
        "interface_sha256": profile.document["fixture"]["interface_sha256"],
        "platform_source": _json_safe(source),
    }


def _manifest_header(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    device_slug: str,
    mode: str,
    state: SourceState,
    *,
    production_eligible: bool,
    overrides: Sequence[str],
    reasons: Sequence[str],
    inputs: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    variant = profile.variants[device_slug]
    return {
        "schema": PACK_SCHEMA,
        "device": {
            "slug": device_slug,
            "display_name": variant["display_name"],
        },
        "mode": mode,
        "profile": {
            "id": profile.document["profile_id"],
            "path": _relative(root, profile.path),
            "sha256": _sha256(profile.path),
        },
        "layout": {
            "id": layout.layout_id,
            "path": _relative(root, layout.path),
            "sha256": _sha256(layout.path),
            "qualification": _json_safe(layout.qualification),
        },
        "qualification": _qualification_record(root, profile),
        "fixture": _fixture_record(root, profile),
        "production_eligible": production_eligible,
        "nonproduction_reasons": list(reasons),
        "overrides": list(overrides),
        "source": {
            "repository": REPOSITORY_URL,
            "commit": state.commit,
            "dirty": state.dirty,
        },
        "toolchain": _toolchain_record(root, layout),
        "fingerprint_contract": {
            "algorithm": FINGERPRINT_ALGORITHM,
            "coordinate_quantum_mm": str(COORDINATE_QUANTUM_MM),
        },
        "stl_serialization": {
            "algorithm": STL_SERIALIZATION,
            "facet_order": "lexicographic",
            "facet_start_vertex": "lexicographic cyclic rotation",
            "facet_winding": "preserved",
            "coordinates": "exact renderer values",
            "facet_normals": "advisory zero",
        },
        "inputs": list(inputs),
    }


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _write_metadata(stage: Path, manifest: Mapping[str, Any]) -> None:
    (stage / "manifest.json").write_bytes(_json_bytes(manifest))
    lines = [
        f"{artifact['raw']['sha256']}  {artifact['path']}\n"
        for artifact in sorted(
            manifest["artifacts"], key=lambda row: row["path"]
        )
    ]
    (stage / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")


def _safe_output(root: Path, output: Path) -> Path:
    root = root.resolve()
    expanded = output.expanduser()
    absolute = Path(os.path.abspath(expanded))
    if absolute.is_symlink():
        raise PackError(f"output may not be a symlink: {absolute}")
    try:
        lexical_relative = absolute.relative_to(root)
    except ValueError:
        lexical_relative = None
    if lexical_relative is not None:
        cursor = root
        for part in lexical_relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise PackError(
                    f"in-repository output traverses a symlink: {cursor}"
                )
    output = absolute.resolve()
    if output == root:
        raise PackError("output may not be the repository root")
    try:
        relative = output.relative_to(root)
    except ValueError:
        return output
    allowed = PurePosixPath("mechanical/device-packs/build")
    relative_posix = PurePosixPath(relative.as_posix())
    if relative_posix != allowed and allowed not in relative_posix.parents:
        raise PackError(
            "in-repository output must be below mechanical/device-packs/build"
        )
    if relative_posix == allowed:
        raise PackError("output must be a device/mode directory, not build root")
    return output


def _recognized_existing_pack(output: Path) -> None:
    if output.is_symlink() or not output.is_dir():
        raise PackError(f"refusing to replace non-pack output: {output}")
    manifest = _read_pack_manifest(output)
    artifact_paths: set[str] = set()
    for index, raw in enumerate(
        _array(manifest["artifacts"], "manifest.artifacts")
    ):
        artifact = _object(raw, f"manifest.artifacts[{index}]")
        path = _output_path(
            artifact.get("path"), f"manifest.artifacts[{index}].path"
        )
        if path.as_posix() in artifact_paths:
            raise PackError("refusing to replace pack with duplicate paths")
        artifact_paths.add(path.as_posix())
    allowed_files = {"manifest.json", "SHA256SUMS", *artifact_paths}
    allowed_dirs = {
        parent.as_posix()
        for path in (PurePosixPath(value) for value in artifact_paths)
        for parent in path.parents
        if parent.as_posix() != "."
    }
    actual_files: set[str] = set()
    actual_dirs: set[str] = set()
    for path in output.rglob("*"):
        if path.is_symlink():
            raise PackError(f"refusing to replace pack containing symlink: {path}")
        relative = path.relative_to(output).as_posix()
        if path.is_file():
            actual_files.add(relative)
        elif path.is_dir():
            actual_dirs.add(relative)
    if actual_files != allowed_files or actual_dirs != allowed_dirs:
        raise PackError(
            "refusing to replace pack with unrecognized directory membership"
        )


def _preflight_output(output: Path, replace: bool) -> None:
    if not output.exists() and not output.is_symlink():
        return
    if not replace:
        raise PackError(
            f"output already exists: {output}; pass --replace to replace "
            "a recognized generated pack"
        )
    _recognized_existing_pack(output)


def _publish_stage(stage: Path, output: Path, replace: bool) -> None:
    backup: Path | None = None
    if output.exists() or output.is_symlink():
        if not replace:
            raise PackError(
                f"output already exists: {output}; pass --replace to replace "
                "a recognized generated pack"
            )
        _recognized_existing_pack(output)
        backup = output.parent / (
            f".{output.name}.backup-{secrets.token_hex(8)}"
        )
        os.replace(output, backup)
    try:
        os.replace(stage, output)
    except BaseException:
        if backup is not None and not output.exists():
            os.replace(backup, output)
        raise
    if backup is not None:
        shutil.rmtree(backup)


ContractChecker = Callable[
    [holder_profiles.ResolvedProfile, ResolvedLayout, str], None
]
Renderer = Callable[[PlanItem, Path, str], None]


def _check_contract(
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    openscad: str,
) -> None:
    if profile.document["qualification"]["status"] == "physically_qualified":
        assert profile.qualification_manifest is not None
        qualification_lock = (
            profile.root / profile.qualification_manifest["toolchain_lock"]
        ).resolve()
        if layout.toolchain_lock != qualification_lock:
            raise PackError(
                "layout and holder qualification use different CAD "
                "toolchain locks"
            )
        holder_profiles.check_qualified(profile, openscad=openscad)
    else:
        holder_profiles.check_toolchain(layout.toolchain_lock, openscad)


def build_pack(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    *,
    device_slug: str,
    mode: str,
    output: Path,
    openscad: str,
    replace: bool,
    allow_dirty: bool,
    allow_unqualified: bool,
    state: SourceState | None = None,
    renderer: Renderer = _render,
    contract_checker: ContractChecker = _check_contract,
) -> Path:
    root = root.resolve()
    output = _safe_output(root, output)
    _preflight_output(output, replace)
    current_state = state if state is not None else source_state(root)
    production_eligible, overrides, reasons = _policy(
        profile,
        layout,
        mode,
        current_state,
        allow_dirty=allow_dirty,
        allow_unqualified=allow_unqualified,
    )
    plan = build_plan(root, profile, layout, device_slug, mode)
    contract_checker(profile, layout, openscad)

    inputs = _input_manifest(
        root, _input_paths(root, profile, layout, plan)
    )
    header = _manifest_header(
        root,
        profile,
        layout,
        device_slug,
        mode,
        current_state,
        production_eligible=production_eligible,
        overrides=overrides,
        reasons=reasons,
        inputs=inputs,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.stage-", dir=output.parent)
    )
    try:
        records: list[dict[str, Any]] = []
        for item in plan:
            artifact_path = stage / Path(*item.output.parts)
            renderer(item, artifact_path, openscad)
            _canonicalize_stl(artifact_path)
            records.append(_artifact_record(root, item, artifact_path))
        manifest = dict(header)
        manifest["artifacts"] = records
        _write_metadata(stage, manifest)
        _verify_materialized_pack(
            root,
            stage,
            profile,
            layout,
            plan,
            expected_header=header,
        )
        _publish_stage(stage, output, replace)
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        raise
    print(
        f"device_pack_build=pass device={device_slug} mode={mode} "
        f"artifacts={len(plan)} production_eligible="
        f"{str(production_eligible).lower()} output={output}"
    )
    return output


def _read_pack_manifest(pack: Path) -> Mapping[str, Any]:
    manifest_path = pack / "manifest.json"
    manifest = _object(_load_json(manifest_path), str(manifest_path))
    _strict_keys(
        manifest,
        str(manifest_path),
        {
            "schema",
            "device",
            "mode",
            "profile",
            "layout",
            "qualification",
            "fixture",
            "production_eligible",
            "nonproduction_reasons",
            "overrides",
            "source",
            "toolchain",
            "fingerprint_contract",
            "stl_serialization",
            "inputs",
            "artifacts",
        },
    )
    if manifest["schema"] != PACK_SCHEMA:
        raise PackError(f"unsupported pack schema: {manifest['schema']!r}")
    return manifest


def _verify_materialized_pack(
    root: Path,
    pack: Path,
    profile: holder_profiles.ResolvedProfile,
    layout: ResolvedLayout,
    plan: Sequence[PlanItem],
    *,
    expected_header: Mapping[str, Any],
) -> None:
    manifest = _read_pack_manifest(pack)
    for key, expected in expected_header.items():
        if manifest.get(key) != expected:
            raise PackError(f"manifest metadata mismatch for {key}")

    raw_artifacts = _array(manifest["artifacts"], "manifest.artifacts")
    if len(raw_artifacts) != len(plan):
        raise PackError(
            f"manifest artifact count mismatch: expected {len(plan)}, "
            f"got {len(raw_artifacts)}"
        )
    expected_records: list[dict[str, Any]] = []
    for item in plan:
        path = pack / Path(*item.output.parts)
        try:
            path.resolve().relative_to(pack.resolve())
        except ValueError as exc:
            raise PackError(
                f"artifact path escapes pack: {item.output.as_posix()}"
            ) from exc
        if not path.is_file():
            raise PackError(f"pack artifact is missing: {item.output.as_posix()}")
        expected_records.append(_artifact_record(root, item, path))
    if raw_artifacts != expected_records:
        raise PackError("manifest artifact metadata does not match generated files")

    expected_sums = "".join(
        f"{record['raw']['sha256']}  {record['path']}\n"
        for record in sorted(expected_records, key=lambda row: row["path"])
    )
    try:
        actual_sums = (pack / "SHA256SUMS").read_text(encoding="utf-8")
    except OSError as exc:
        raise PackError(f"cannot read pack SHA256SUMS: {exc}") from exc
    if actual_sums != expected_sums:
        raise PackError("SHA256SUMS does not match pack artifacts")

    allowed_files = {
        "manifest.json",
        "SHA256SUMS",
        *(item.output.as_posix() for item in plan),
    }
    actual_files = {
        path.relative_to(pack).as_posix()
        for path in pack.rglob("*")
        if path.is_file()
    }
    if actual_files != allowed_files:
        extra = sorted(actual_files - allowed_files)
        missing = sorted(allowed_files - actual_files)
        raise PackError(
            f"pack membership mismatch: extra={extra} missing={missing}"
        )


def verify_pack(root: Path, pack: Path) -> None:
    root = root.resolve()
    pack = pack.expanduser().resolve()
    if not pack.is_dir() or pack.is_symlink():
        raise PackError(f"pack is not a directory: {pack}")
    manifest = _read_pack_manifest(pack)
    profile_record = _object(manifest["profile"], "manifest.profile")
    layout_record = _object(manifest["layout"], "manifest.layout")
    device_record = _object(manifest["device"], "manifest.device")
    profile_path = _repo_path(
        root, profile_record.get("path"), "manifest.profile.path"
    )
    layout_path = _repo_path(
        root, layout_record.get("path"), "manifest.layout.path"
    )
    device_slug = _string(device_record.get("slug"), "manifest.device.slug")
    profile = holder_profiles.validate_profile(CRADLE_ROOT, profile_path)
    layout = resolve_device_layout(
        root, device_slug, requested_layout=layout_path
    )
    mode = _string(manifest["mode"], "manifest.mode")
    plan = build_plan(root, profile, layout, device_slug, mode)

    source_record = _object(manifest["source"], "manifest.source")
    state = source_state(root)
    if source_record.get("dirty") is not state.dirty:
        raise PackError(
            "manifest source.dirty does not match the current source tree"
        )
    production_eligible, overrides, reasons = _policy(
        profile,
        layout,
        mode,
        state,
        allow_dirty=state.dirty,
        allow_unqualified=True,
    )
    inputs = _input_manifest(
        root, _input_paths(root, profile, layout, plan)
    )
    expected_header = _manifest_header(
        root,
        profile,
        layout,
        device_slug,
        mode,
        state,
        production_eligible=production_eligible,
        overrides=overrides,
        reasons=reasons,
        inputs=inputs,
    )
    _verify_materialized_pack(
        root,
        pack,
        profile,
        layout,
        plan,
        expected_header=expected_header,
    )
    print(
        f"device_pack_verify=pass device={device_slug} mode={mode} "
        f"artifacts={len(plan)} production_eligible="
        f"{str(production_eligible).lower()} pack={pack}"
    )


def _resolve_cli_path(root: Path, path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def _load_cli_contracts(
    root: Path,
    profile_path: Path | None,
    device_slug: str,
    registry_path: Path,
    layout_path: Path | None,
) -> tuple[holder_profiles.ResolvedProfile, ResolvedLayout]:
    if profile_path is None:
        profiles = discover_device_profiles(root)
        profile = profiles.get(device_slug)
        if profile is None:
            choices = ", ".join(sorted(profiles))
            raise PackError(
                f"device {device_slug!r} has no holder profile; "
                f"choose one of: {choices}"
            )
    else:
        profile = holder_profiles.validate_profile(
            root / "mechanical" / "dut-cradle-v1",
            _resolve_cli_path(root, profile_path),
        )
    layout = resolve_device_layout(
        root,
        device_slug,
        registry_path=registry_path,
        requested_layout=layout_path,
    )
    return profile, layout


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--device", required=True)
    build_parser.add_argument("--mode", choices=MODES, required=True)
    build_parser.add_argument(
        "--profile",
        type=Path,
        help="Explicit holder profile; otherwise resolve it from --device",
    )
    build_parser.add_argument(
        "--layout",
        type=Path,
        help=(
            "Optional assertion of the registered layout path; mismatched "
            "device/layout combinations are rejected"
        ),
    )
    build_parser.add_argument(
        "--layout-registry",
        type=Path,
        default=DEFAULT_LAYOUT_REGISTRY,
    )
    build_parser.add_argument("--output", type=Path)
    build_parser.add_argument("--openscad", default="openscad")
    build_parser.add_argument("--replace", action="store_true")
    build_parser.add_argument("--allow-dirty", action="store_true")
    build_parser.add_argument("--allow-unqualified", action="store_true")

    matrix_parser = subparsers.add_parser("matrix")
    matrix_parser.add_argument(
        "--kind",
        choices=("production-devices", "candidate-layout-devices"),
        required=True,
    )
    matrix_parser.add_argument(
        "--profile",
        type=Path,
        help="Optional single-profile matrix; default discovers all profiles",
    )
    matrix_parser.add_argument(
        "--layout-registry",
        type=Path,
        default=DEFAULT_LAYOUT_REGISTRY,
    )

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--pack", type=Path, required=True)

    guard_parser = subparsers.add_parser("guard-qualified-layouts")
    guard_parser.add_argument("--base-root", type=Path, required=True)
    guard_parser.add_argument(
        "--layout-registry",
        type=Path,
        default=DEFAULT_LAYOUT_REGISTRY,
    )

    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "build":
            profile, layout = _load_cli_contracts(
                root,
                args.profile,
                args.device,
                args.layout_registry,
                args.layout,
            )
            output = args.output
            if output is None:
                output = (
                    root
                    / "mechanical"
                    / "device-packs"
                    / "build"
                    / args.device
                    / args.mode
                )
            elif not output.is_absolute():
                output = root / output
            build_pack(
                root,
                profile,
                layout,
                device_slug=args.device,
                mode=args.mode,
                output=output,
                openscad=args.openscad,
                replace=args.replace,
                allow_dirty=args.allow_dirty,
                allow_unqualified=args.allow_unqualified,
            )
        elif args.command == "matrix":
            if args.profile is None:
                matrix = all_device_layout_matrix(
                    root,
                    registry_path=args.layout_registry,
                    kind=args.kind,
                )
            else:
                profile = holder_profiles.validate_profile(
                    root / "mechanical" / "dut-cradle-v1",
                    _resolve_cli_path(root, args.profile),
                )
                matrix = device_layout_matrix(
                    root,
                    profile,
                    registry_path=args.layout_registry,
                    kind=args.kind,
                )
            print(
                json.dumps(
                    matrix,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
        elif args.command == "verify":
            pack = args.pack if args.pack.is_absolute() else root / args.pack
            verify_pack(root, pack)
        elif args.command == "guard-qualified-layouts":
            guard_qualified_layouts(
                root,
                args.base_root,
                registry_path=args.layout_registry,
            )
        else:  # pragma: no cover - argparse enforces the command set.
            raise PackError(f"unsupported command: {args.command}")
    except (
        PackError,
        holder_profiles.ProfileError,
        subprocess.SubprocessError,
    ) as exc:
        print(f"device_pack_error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
