#!/usr/bin/env python3
"""Export and verify the source-only browser device-pack generation bundle.

The browser bundle is a deterministic projection of the same holder profiles,
device-to-layout registry, and build plans used by ``build_device_pack.py``.
It contains no rendered mesh.  A consumer receives a catalog of exact
OpenSCAD definitions plus the hashed source closure required to render them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import build_device_pack
import holder_profiles


CATALOG_SCHEMA = "pocketforge-browser-device-pack-catalog-v1"
BUNDLE_SCHEMA = "pocketforge-browser-device-pack-bundle-v1"
DEFAULT_OUTPUT = Path("mechanical/device-packs/build/browser")
CATALOG_NAME = "catalog.json"
CHECKSUM_NAME = "SHA256SUMS"
SOURCES_DIRECTORY = PurePosixPath("sources")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class BrowserBundleError(ValueError):
    """The browser generation bundle or its source contract is invalid."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise BrowserBundleError(f"path escapes repository: {path}") from exc


def _safe_relative(value: str, field: str) -> PurePosixPath:
    if "\\" in value:
        raise BrowserBundleError(f"{field} must use POSIX separators")
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or "." in path.parts
        or ".." in path.parts
    ):
        raise BrowserBundleError(f"{field} must be a safe relative path")
    return path


def _discover_device_profiles(
    root: Path,
) -> dict[str, holder_profiles.ResolvedProfile]:
    cradle_root = root / "mechanical" / "dut-cradle-v1"
    profiles: dict[str, holder_profiles.ResolvedProfile] = {}
    for profile_path in holder_profiles.discover_profiles(cradle_root):
        profile = holder_profiles.validate_profile(cradle_root, profile_path)
        for slug in profile.variants:
            if slug in profiles:
                raise BrowserBundleError(
                    f"device {slug!r} belongs to more than one holder profile"
                )
            profiles[slug] = profile
    if not profiles:
        raise BrowserBundleError("no holder device variants were discovered")
    return profiles


def _source_record(root: Path, path: Path) -> dict[str, Any]:
    relative = _relative(root, path)
    return {
        "path": relative,
        "bundle_path": (SOURCES_DIRECTORY / relative).as_posix(),
        "sha256": _sha256(path),
        "size_bytes": path.stat().st_size,
    }


def _input_record(root: Path, path: Path) -> dict[str, Any]:
    return {
        "path": _relative(root, path),
        "sha256": _sha256(path),
        "size_bytes": path.stat().st_size,
    }


def _artifact_record(
    root: Path, item: build_device_pack.PlanItem
) -> dict[str, Any]:
    definitions = build_device_pack._definitions(item.parameters)
    return {
        "id": item.artifact_id,
        "output": item.output.as_posix(),
        "role": item.role,
        "scope": item.scope,
        "source": _relative(root, item.source),
        "definitions": [
            {"name": name, "literal": literal}
            for name, literal in definitions.items()
        ],
        "print": build_device_pack._json_safe(item.print_contract),
        "expected_normalized_sha256": item.expected_normalized_sha256,
    }


def _mode_record(
    root: Path,
    profile: holder_profiles.ResolvedProfile,
    layout: build_device_pack.ResolvedLayout,
    device_slug: str,
    mode: str,
    state: build_device_pack.SourceState,
) -> tuple[dict[str, Any], tuple[build_device_pack.PlanItem, ...]]:
    plan = build_device_pack.build_plan(
        root, profile, layout, device_slug, mode
    )
    production_eligible, overrides, reasons = build_device_pack._policy(
        profile,
        layout,
        mode,
        state,
        allow_dirty=state.dirty,
        allow_unqualified=True,
    )
    return (
        {
            "production_eligible": production_eligible,
            "nonproduction_reasons": reasons,
            "required_overrides": overrides,
            "artifacts": [_artifact_record(root, item) for item in plan],
        },
        plan,
    )


def build_catalog(
    root: Path,
    *,
    state: build_device_pack.SourceState | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    """Build the deterministic catalog and return its copied SCAD closure."""
    root = root.resolve()
    current_state = (
        state if state is not None else build_device_pack.source_state(root)
    )
    registry_path = root / build_device_pack.DEFAULT_LAYOUT_REGISTRY
    registry = build_device_pack.load_layout_registry(root, registry_path)
    profiles = _discover_device_profiles(root)

    missing_profiles = sorted(set(registry) - set(profiles))
    if missing_profiles:
        raise BrowserBundleError(
            "registered devices have no holder profile: "
            + ", ".join(missing_profiles)
        )

    devices: list[dict[str, Any]] = []
    source_starts: set[Path] = set()
    input_paths: set[Path] = {
        Path(__file__).resolve(),
        Path(build_device_pack.__file__).resolve(),
        Path(holder_profiles.__file__).resolve(),
        registry_path.resolve(),
    }
    for slug in sorted(registry):
        profile = profiles[slug]
        layout = build_device_pack.resolve_device_layout(root, slug)
        modes: dict[str, Any] = {}
        for mode in build_device_pack.MODES:
            mode_record, plan = _mode_record(
                root, profile, layout, slug, mode, current_state
            )
            modes[mode] = mode_record
            source_starts.update(item.source.resolve() for item in plan)
            input_paths.update(
                build_device_pack._input_paths(root, profile, layout, plan)
            )

        variant = profile.variants[slug]
        devices.append(
            {
                "slug": slug,
                "display_name": variant["display_name"],
                "profile": {
                    "id": profile.document["profile_id"],
                    "qualification": build_device_pack._json_safe(
                        profile.document["qualification"]
                    ),
                },
                "layout": {
                    "id": layout.layout_id,
                    "qualification": build_device_pack._json_safe(
                        layout.qualification
                    ),
                },
                "modes": modes,
            }
        )

    sources = tuple(
        sorted(
            build_device_pack._scad_closure(root, source_starts),
            key=lambda path: _relative(root, path),
        )
    )
    if not sources:
        raise BrowserBundleError("browser bundle source closure is empty")
    if any(path.suffix.lower() == ".stl" for path in sources):
        raise BrowserBundleError("browser source closure contains an STL")

    catalog = {
        "schema": CATALOG_SCHEMA,
        "bundle_schema": BUNDLE_SCHEMA,
        "source": {
            "repository": build_device_pack.REPOSITORY_URL,
            "commit": current_state.commit,
            "dirty": current_state.dirty,
        },
        "modes": list(build_device_pack.MODES),
        "fingerprint_contract": {
            "algorithm": build_device_pack.FINGERPRINT_ALGORITHM,
            "coordinate_quantum_mm": str(
                build_device_pack.COORDINATE_QUANTUM_MM
            ),
        },
        "inputs": [
            _input_record(root, path)
            for path in sorted(
                input_paths, key=lambda path: _relative(root, path)
            )
        ],
        "sources": [_source_record(root, path) for path in sources],
        "devices": devices,
    }
    validate_catalog(catalog)
    return catalog, sources


def validate_catalog(catalog: Mapping[str, Any]) -> None:
    """Validate the strict public shape consumed by the handbook."""
    if catalog.get("schema") != CATALOG_SCHEMA:
        raise BrowserBundleError("browser catalog schema changed")
    if catalog.get("bundle_schema") != BUNDLE_SCHEMA:
        raise BrowserBundleError("browser bundle schema changed")
    source = catalog.get("source")
    if not isinstance(source, dict):
        raise BrowserBundleError("browser catalog source must be an object")
    if source.get("repository") != build_device_pack.REPOSITORY_URL:
        raise BrowserBundleError("browser catalog repository changed")
    if not isinstance(source.get("commit"), str) or not re.fullmatch(
        r"[0-9a-f]{40}", source["commit"]
    ):
        raise BrowserBundleError("browser catalog commit is invalid")
    if not isinstance(source.get("dirty"), bool):
        raise BrowserBundleError("browser catalog dirty flag is invalid")
    if catalog.get("modes") != list(build_device_pack.MODES):
        raise BrowserBundleError("browser catalog mode contract changed")

    sources = catalog.get("sources")
    if not isinstance(sources, list) or not sources:
        raise BrowserBundleError("browser catalog sources must be non-empty")
    source_paths: set[str] = set()
    for index, record in enumerate(sources):
        field = f"sources[{index}]"
        if not isinstance(record, dict):
            raise BrowserBundleError(f"{field} must be an object")
        path = _safe_relative(record.get("path", ""), f"{field}.path")
        bundle_path = _safe_relative(
            record.get("bundle_path", ""), f"{field}.bundle_path"
        )
        if bundle_path != SOURCES_DIRECTORY / path:
            raise BrowserBundleError(f"{field}.bundle_path changed")
        if path.suffix.lower() == ".stl":
            raise BrowserBundleError(f"{field} names a rendered STL")
        if path.as_posix() in source_paths:
            raise BrowserBundleError(f"{field}.path is duplicated")
        source_paths.add(path.as_posix())
        if not isinstance(record.get("sha256"), str) or not SHA256_RE.fullmatch(
            record["sha256"]
        ):
            raise BrowserBundleError(f"{field}.sha256 is invalid")
        if (
            not isinstance(record.get("size_bytes"), int)
            or record["size_bytes"] <= 0
        ):
            raise BrowserBundleError(f"{field}.size_bytes is invalid")

    devices = catalog.get("devices")
    if not isinstance(devices, list) or not devices:
        raise BrowserBundleError("browser catalog devices must be non-empty")
    slugs: set[str] = set()
    for device_index, device in enumerate(devices):
        field = f"devices[{device_index}]"
        if not isinstance(device, dict):
            raise BrowserBundleError(f"{field} must be an object")
        slug = device.get("slug")
        if (
            not isinstance(slug, str)
            or not build_device_pack.DEVICE_SLUG_RE.fullmatch(slug)
        ):
            raise BrowserBundleError(f"{field}.slug is invalid")
        if slug in slugs:
            raise BrowserBundleError(f"{field}.slug is duplicated")
        slugs.add(slug)
        if not isinstance(device.get("display_name"), str) or not device[
            "display_name"
        ]:
            raise BrowserBundleError(f"{field}.display_name is invalid")
        modes = device.get("modes")
        if not isinstance(modes, dict) or set(modes) != set(
            build_device_pack.MODES
        ):
            raise BrowserBundleError(f"{field}.modes changed")
        for mode in build_device_pack.MODES:
            mode_record = modes[mode]
            mode_field = f"{field}.modes.{mode}"
            if not isinstance(mode_record, dict):
                raise BrowserBundleError(f"{mode_field} must be an object")
            artifacts = mode_record.get("artifacts")
            expected_count = {"coupon": 1, "retrofit": 6, "full": 12}[mode]
            if not isinstance(artifacts, list) or len(artifacts) != expected_count:
                raise BrowserBundleError(
                    f"{mode_field}.artifacts must contain {expected_count} rows"
                )
            artifact_ids: set[str] = set()
            outputs: set[str] = set()
            for artifact_index, artifact in enumerate(artifacts):
                artifact_field = (
                    f"{mode_field}.artifacts[{artifact_index}]"
                )
                if not isinstance(artifact, dict):
                    raise BrowserBundleError(
                        f"{artifact_field} must be an object"
                    )
                artifact_id = artifact.get("id")
                if (
                    not isinstance(artifact_id, str)
                    or not build_device_pack.ID_RE.fullmatch(artifact_id)
                    or artifact_id in artifact_ids
                ):
                    raise BrowserBundleError(
                        f"{artifact_field}.id is invalid or duplicated"
                    )
                artifact_ids.add(artifact_id)
                output = _safe_relative(
                    artifact.get("output", ""),
                    f"{artifact_field}.output",
                )
                if output.suffix.lower() != ".stl" or output.as_posix() in outputs:
                    raise BrowserBundleError(
                        f"{artifact_field}.output is invalid or duplicated"
                    )
                outputs.add(output.as_posix())
                source_path = _safe_relative(
                    artifact.get("source", ""),
                    f"{artifact_field}.source",
                ).as_posix()
                if source_path not in source_paths:
                    raise BrowserBundleError(
                        f"{artifact_field}.source is outside the source closure"
                    )
                definitions = artifact.get("definitions")
                if not isinstance(definitions, list) or not definitions:
                    raise BrowserBundleError(
                        f"{artifact_field}.definitions must be non-empty"
                    )
                names = [
                    row.get("name")
                    for row in definitions
                    if isinstance(row, dict)
                ]
                if len(names) != len(definitions) or names != sorted(names):
                    raise BrowserBundleError(
                        f"{artifact_field}.definitions must be ordered"
                    )
                if len(names) != len(set(names)) or "PART" not in names:
                    raise BrowserBundleError(
                        f"{artifact_field}.definitions are incomplete"
                    )
                for row in definitions:
                    if not isinstance(row.get("literal"), str):
                        raise BrowserBundleError(
                            f"{artifact_field}.definitions literal is invalid"
                        )
                fingerprint = artifact.get("expected_normalized_sha256")
                if fingerprint is not None and (
                    not isinstance(fingerprint, str)
                    or not SHA256_RE.fullmatch(fingerprint)
                ):
                    raise BrowserBundleError(
                        f"{artifact_field}.expected_normalized_sha256 is invalid"
                    )


def _bundle_files(bundle: Path) -> list[Path]:
    files: list[Path] = []
    for path in bundle.rglob("*"):
        if path.is_symlink():
            raise BrowserBundleError(f"bundle contains a symlink: {path}")
        if path.is_file() and path.name != CHECKSUM_NAME:
            files.append(path)
    return sorted(files, key=lambda path: path.relative_to(bundle).as_posix())


def _checksum_bytes(bundle: Path) -> bytes:
    return "".join(
        f"{_sha256(path)}  {path.relative_to(bundle).as_posix()}\n"
        for path in _bundle_files(bundle)
    ).encode("utf-8")


def _recognized_bundle(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        raise BrowserBundleError(f"refusing to replace non-bundle output: {path}")
    catalog_path = path / CATALOG_NAME
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BrowserBundleError(
            f"refusing to replace unrecognized browser bundle: {path}"
        ) from exc
    if not isinstance(catalog, dict):
        raise BrowserBundleError("browser catalog must be an object")
    validate_catalog(catalog)
    verify_bundle(path, expected_catalog=catalog)


def write_bundle(
    root: Path,
    output: Path,
    *,
    replace: bool = False,
    state: build_device_pack.SourceState | None = None,
) -> Path:
    """Atomically write a complete source-only browser bundle."""
    root = root.resolve()
    output = Path(os.path.abspath(output.expanduser()))
    if output == root:
        raise BrowserBundleError("browser bundle output may not be repository root")
    if output.exists() or output.is_symlink():
        if not replace:
            raise BrowserBundleError(
                f"output already exists: {output}; pass --replace"
            )
        _recognized_bundle(output)

    catalog, sources = build_catalog(root, state=state)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.stage-", dir=output.parent)
    )
    backup: Path | None = None
    try:
        (stage / CATALOG_NAME).write_bytes(_json_bytes(catalog))
        for source in sources:
            relative = Path(*PurePosixPath(_relative(root, source)).parts)
            destination = stage / Path(*SOURCES_DIRECTORY.parts) / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        (stage / CHECKSUM_NAME).write_bytes(_checksum_bytes(stage))
        verify_bundle(stage, expected_catalog=catalog)
        if output.exists() or output.is_symlink():
            backup = output.parent / f".{output.name}.backup"
            if backup.exists() or backup.is_symlink():
                raise BrowserBundleError(f"stale browser bundle backup: {backup}")
            os.replace(output, backup)
        os.replace(stage, output)
        if backup is not None:
            shutil.rmtree(backup)
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        if backup is not None and backup.exists() and not output.exists():
            os.replace(backup, output)
        raise
    print(
        "browser_bundle_build=pass "
        f"devices={len(catalog['devices'])} "
        f"sources={len(catalog['sources'])} output={output}"
    )
    return output


def verify_bundle(
    bundle: Path,
    *,
    root: Path | None = None,
    expected_catalog: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """Verify bundle membership, hashes, and optionally the current source."""
    bundle = bundle.resolve()
    if not bundle.is_dir():
        raise BrowserBundleError(f"browser bundle does not exist: {bundle}")
    try:
        catalog = json.loads(
            (bundle / CATALOG_NAME).read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise BrowserBundleError("cannot read browser catalog") from exc
    if not isinstance(catalog, dict):
        raise BrowserBundleError("browser catalog must be an object")
    validate_catalog(catalog)
    if expected_catalog is not None and catalog != expected_catalog:
        raise BrowserBundleError("browser catalog differs from expected source")

    expected_members = {
        CATALOG_NAME,
        CHECKSUM_NAME,
        *(
            record["bundle_path"]
            for record in catalog["sources"]
        ),
    }
    actual_members = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file()
    }
    if actual_members != expected_members:
        missing = sorted(expected_members - actual_members)
        extra = sorted(actual_members - expected_members)
        raise BrowserBundleError(
            f"browser bundle membership changed: missing={missing} extra={extra}"
        )
    if any(path.lower().endswith(".stl") for path in actual_members):
        raise BrowserBundleError("browser bundle contains a rendered STL")

    for record in catalog["sources"]:
        path = bundle / Path(*PurePosixPath(record["bundle_path"]).parts)
        if path.stat().st_size != record["size_bytes"]:
            raise BrowserBundleError(f"browser source size changed: {path}")
        if _sha256(path) != record["sha256"]:
            raise BrowserBundleError(f"browser source hash changed: {path}")
    checksum_path = bundle / CHECKSUM_NAME
    if checksum_path.read_bytes() != _checksum_bytes(bundle):
        raise BrowserBundleError("browser bundle SHA256SUMS changed")

    if root is not None:
        state = build_device_pack.source_state(root.resolve())
        rebuilt, _ = build_catalog(root, state=state)
        if catalog != rebuilt:
            raise BrowserBundleError(
                "browser bundle is stale for the current source checkout"
            )
    print(
        "browser_bundle_verify=pass "
        f"devices={len(catalog['devices'])} "
        f"sources={len(catalog['sources'])} bundle={bundle}"
    )
    return catalog


def _resolve_output(root: Path, output: Path) -> Path:
    return output if output.is_absolute() else root / output


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=build_device_pack.REPO_ROOT
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    build_parser.add_argument("--replace", action="store_true")
    build_parser.add_argument("--allow-dirty", action="store_true")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--bundle", type=Path, default=DEFAULT_OUTPUT)

    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "build":
            state = build_device_pack.source_state(root)
            if state.dirty and not args.allow_dirty:
                raise BrowserBundleError(
                    "source tree is dirty; commit it or pass --allow-dirty "
                    "for a visibly non-production development bundle"
                )
            write_bundle(
                root,
                _resolve_output(root, args.output),
                replace=args.replace,
                state=state,
            )
        else:
            verify_bundle(
                _resolve_output(root, args.bundle),
                root=root,
            )
    except (
        BrowserBundleError,
        build_device_pack.PackError,
        holder_profiles.ProfileError,
        OSError,
    ) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
