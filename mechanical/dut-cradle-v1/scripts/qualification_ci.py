#!/usr/bin/env python3
"""Plan and verify qualification transitions for every DUT holder profile.

Physically accepted meshes are immutable baselines.  A no-intent change must
reproduce those meshes exactly.  An intentional fit/interface change is a
two-PR transition:

1. downgrade the profile to ``unqualified`` and add an awaiting change record;
2. after physical acceptance, add a new manifest and complete that same record.

Generated candidate meshes and reports are review artifacts, never source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import holder_profiles
from mesh_fingerprint import (
    CANONICAL_ASCII_STL_SCHEMA,
    StlError,
    canonicalize_stl,
    describe_mesh,
)
from qualified_geometry import check_toolchain


PLAN_SCHEMA = "pocketforge-holder-qualification-plan-v1"
REPORT_SCHEMA = "pocketforge-holder-geometry-diff-v1"
CHANGE_SCHEMA = "pocketforge-holder-geometry-change-v1"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

QUALIFIED = "physically_qualified"
AWAITING = "awaiting_physical_acceptance"
ACCEPTED = "physically_accepted"

ALLOWED_SCOPES = {
    "carrier_body",
    "fit_coupon",
    "fixture_interface",
    "j_hook",
    "j_hook_set",
    "mechanism",
    "print_process",
    "toolchain",
}


class QualificationCiError(ValueError):
    """The profile registry or qualification transition is unsafe."""


@dataclass(frozen=True)
class ProfileRecord:
    profile_id: str
    relative_path: str
    device_slugs: tuple[str, ...]
    status: str
    fixture_sha256: str
    fixture_lock_path: str
    fixture_lock_sha256: str
    qualification: Mapping[str, Any]
    manifest_path: str | None
    manifest_sha256: str | None
    toolchain_lock_path: str | None
    toolchain_lock_sha256: str | None
    resolved: holder_profiles.ResolvedProfile


@dataclass(frozen=True)
class ChangeRecord:
    relative_path: str
    change_id: str
    profile_id: str
    base: Mapping[str, Any] | None
    intent: Mapping[str, Any]
    transition: Mapping[str, Any]
    document: Mapping[str, Any]

    @property
    def state(self) -> str:
        return str(self.transition["state"])


Renderer = Callable[..., None]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _strict_json(path: Path) -> Mapping[str, Any]:
    def reject_constant(token: str) -> None:
        raise QualificationCiError(
            f"{path}: JSON contains non-finite number {token}"
        )

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_constant,
        )
    except OSError as exc:
        raise QualificationCiError(f"{path}: cannot read: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise QualificationCiError(
            f"{path}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise QualificationCiError(f"{path}: must contain a JSON object")
    return value


def _exact_keys(
    value: Mapping[str, Any],
    required: set[str],
    path: str,
) -> None:
    missing = sorted(required - value.keys())
    extra = sorted(value.keys() - required)
    if missing:
        raise QualificationCiError(
            f"{path}: missing required field(s): {', '.join(missing)}"
        )
    if extra:
        raise QualificationCiError(
            f"{path}: unknown field(s): {', '.join(extra)}"
        )


def _string(
    value: Any,
    path: str,
    *,
    pattern: re.Pattern[str] | None = None,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QualificationCiError(f"{path}: must be a non-empty string")
    if pattern is not None and not pattern.fullmatch(value):
        raise QualificationCiError(f"{path}: invalid format: {value!r}")
    return value


def _nullable_path(root: Path, value: Any, path: str) -> tuple[str, Path]:
    relative = _string(value, path)
    candidate = Path(relative)
    if candidate.is_absolute():
        raise QualificationCiError(f"{path}: must be relative")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise QualificationCiError(f"{path}: escapes the cradle root") from exc
    return candidate.as_posix(), resolved


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise QualificationCiError(
            f"path is outside cradle root: {path}"
        ) from exc


def _json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_safe(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(child) for child in value]
    return value


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            _json_safe(value),
            indent=2,
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def discover_registry(root: Path) -> dict[str, ProfileRecord]:
    """Validate and return every source-owned profile, keyed by profile ID."""
    root = root.resolve()
    paths = holder_profiles.discover_profiles(root)
    if not paths:
        raise QualificationCiError(f"no holder profiles discovered under {root}")

    records: dict[str, ProfileRecord] = {}
    devices: dict[str, str] = {}
    for profile_path in paths:
        try:
            resolved = holder_profiles.validate_profile(root, profile_path)
        except (OSError, holder_profiles.ProfileError) as exc:
            raise QualificationCiError(str(exc)) from exc
        profile_id = str(resolved.document["profile_id"])
        if profile_id in records:
            raise QualificationCiError(f"duplicate profile id: {profile_id}")
        slugs = tuple(sorted(str(item) for item in resolved.document["device_slugs"]))
        for slug in slugs:
            prior = devices.get(slug)
            if prior is not None:
                raise QualificationCiError(
                    f"device {slug!r} is owned by both {prior!r} and "
                    f"{profile_id!r}"
                )
            devices[slug] = profile_id

        qualification = resolved.document["qualification"]
        status = str(qualification["status"])
        fixture_lock_path, fixture_lock = _nullable_path(
            root,
            resolved.document["fixture"]["lock"],
            f"{profile_path}.fixture.lock",
        )
        if not fixture_lock.is_file():
            raise QualificationCiError(
                f"{profile_path}: fixture lock is missing: {fixture_lock_path}"
            )
        manifest_path: str | None = None
        manifest_hash: str | None = None
        toolchain_lock_path: str | None = None
        toolchain_lock_hash: str | None = None
        if status == QUALIFIED:
            manifest_path, manifest = _nullable_path(
                root,
                qualification["geometry_manifest"],
                f"{profile_path}.qualification.geometry_manifest",
            )
            if not manifest.is_file():
                raise QualificationCiError(
                    f"{profile_path}: qualification manifest is missing: "
                    f"{manifest_path}"
                )
            manifest_hash = _sha256(manifest)
            toolchain_lock_path, toolchain_lock_hash = _manifest_toolchain(
                root,
                manifest_path,
                manifest_hash,
            )

        records[profile_id] = ProfileRecord(
            profile_id=profile_id,
            relative_path=_relative(root, profile_path),
            device_slugs=slugs,
            status=status,
            fixture_sha256=str(resolved.lock_state["hash"]),
            fixture_lock_path=fixture_lock_path,
            fixture_lock_sha256=_sha256(fixture_lock),
            qualification=qualification,
            manifest_path=manifest_path,
            manifest_sha256=manifest_hash,
            toolchain_lock_path=toolchain_lock_path,
            toolchain_lock_sha256=toolchain_lock_hash,
            resolved=resolved,
        )
    return dict(sorted(records.items()))


def _validate_base(
    root: Path,
    value: Any,
    path: str,
) -> Mapping[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise QualificationCiError(f"{path}: must be an object or null")
    required = {
        "profile_path",
        "geometry_manifest",
        "manifest_sha256",
        "acceptance_ref",
        "fixture_interface_sha256",
        "fixture_lock",
        "fixture_lock_sha256",
        "toolchain_lock",
        "toolchain_lock_sha256",
    }
    _exact_keys(value, required, path)
    _nullable_path(root, value["profile_path"], f"{path}.profile_path")
    _nullable_path(root, value["geometry_manifest"], f"{path}.geometry_manifest")
    _string(value["manifest_sha256"], f"{path}.manifest_sha256", pattern=SHA256_RE)
    _string(value["acceptance_ref"], f"{path}.acceptance_ref")
    _string(
        value["fixture_interface_sha256"],
        f"{path}.fixture_interface_sha256",
        pattern=SHA256_RE,
    )
    _nullable_path(root, value["fixture_lock"], f"{path}.fixture_lock")
    _string(
        value["fixture_lock_sha256"],
        f"{path}.fixture_lock_sha256",
        pattern=SHA256_RE,
    )
    _nullable_path(root, value["toolchain_lock"], f"{path}.toolchain_lock")
    _string(
        value["toolchain_lock_sha256"],
        f"{path}.toolchain_lock_sha256",
        pattern=SHA256_RE,
    )
    return value


def _validate_intent(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise QualificationCiError(f"{path}: must be an object")
    _exact_keys(value, {"tracking_ref", "reason", "scopes"}, path)
    _string(value["tracking_ref"], f"{path}.tracking_ref")
    _string(value["reason"], f"{path}.reason")
    scopes = value["scopes"]
    if not isinstance(scopes, list) or not scopes:
        raise QualificationCiError(f"{path}.scopes: must be a non-empty array")
    if any(not isinstance(item, str) for item in scopes):
        raise QualificationCiError(f"{path}.scopes: every value must be a string")
    if scopes != sorted(set(scopes)):
        raise QualificationCiError(
            f"{path}.scopes: must be sorted and contain no duplicates"
        )
    unknown = sorted(set(scopes) - ALLOWED_SCOPES)
    if unknown:
        raise QualificationCiError(
            f"{path}.scopes: unsupported scope(s): {', '.join(unknown)}"
        )
    return value


def _validate_acceptance(
    root: Path,
    value: Any,
    path: str,
) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise QualificationCiError(f"{path}: must be an object")
    required = {
        "acceptance_ref",
        "accepted_on",
        "geometry_manifest",
        "manifest_sha256",
    }
    _exact_keys(value, required, path)
    _string(value["acceptance_ref"], f"{path}.acceptance_ref")
    _string(value["accepted_on"], f"{path}.accepted_on", pattern=DATE_RE)
    _nullable_path(root, value["geometry_manifest"], f"{path}.geometry_manifest")
    _string(value["manifest_sha256"], f"{path}.manifest_sha256", pattern=SHA256_RE)
    return value


def _validate_transition(
    root: Path,
    value: Any,
    path: str,
) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise QualificationCiError(f"{path}: must be an object")
    required = {
        "state",
        "candidate_fixture_interface_sha256",
        "candidate_fixture_lock",
        "candidate_fixture_lock_sha256",
        "candidate_toolchain_lock",
        "candidate_toolchain_sha256",
        "physical_acceptance",
    }
    _exact_keys(value, required, path)
    state = _string(value["state"], f"{path}.state")
    if state not in {AWAITING, ACCEPTED}:
        raise QualificationCiError(
            f"{path}.state: must be {AWAITING!r} or {ACCEPTED!r}"
        )
    _string(
        value["candidate_fixture_interface_sha256"],
        f"{path}.candidate_fixture_interface_sha256",
        pattern=SHA256_RE,
    )
    _nullable_path(
        root,
        value["candidate_fixture_lock"],
        f"{path}.candidate_fixture_lock",
    )
    _string(
        value["candidate_fixture_lock_sha256"],
        f"{path}.candidate_fixture_lock_sha256",
        pattern=SHA256_RE,
    )
    _nullable_path(
        root,
        value["candidate_toolchain_lock"],
        f"{path}.candidate_toolchain_lock",
    )
    _string(
        value["candidate_toolchain_sha256"],
        f"{path}.candidate_toolchain_sha256",
        pattern=SHA256_RE,
    )
    acceptance = value["physical_acceptance"]
    if state == AWAITING and acceptance is not None:
        raise QualificationCiError(
            f"{path}.physical_acceptance: must be null while awaiting"
        )
    if state == ACCEPTED:
        _validate_acceptance(root, acceptance, f"{path}.physical_acceptance")
    return value


def discover_changes(root: Path) -> dict[str, ChangeRecord]:
    root = root.resolve()
    directory = root / "qualification" / "changes"
    if not directory.exists():
        return {}
    records: dict[str, ChangeRecord] = {}
    for path in sorted(directory.glob("*.json")):
        document = _strict_json(path)
        required = {"schema", "change_id", "profile_id", "base", "intent", "transition"}
        _exact_keys(document, required, str(path))
        if document["schema"] != CHANGE_SCHEMA:
            raise QualificationCiError(
                f"{path}.schema: must be {CHANGE_SCHEMA!r}"
            )
        change_id = _string(
            document["change_id"],
            f"{path}.change_id",
            pattern=ID_RE,
        )
        if path.stem != change_id:
            raise QualificationCiError(
                f"{path}.change_id: must match filename stem {path.stem!r}"
            )
        profile_id = _string(
            document["profile_id"],
            f"{path}.profile_id",
            pattern=ID_RE,
        )
        base = _validate_base(root, document["base"], f"{path}.base")
        intent = _validate_intent(document["intent"], f"{path}.intent")
        transition = _validate_transition(
            root,
            document["transition"],
            f"{path}.transition",
        )
        relative = _relative(root, path)
        if change_id in records:
            raise QualificationCiError(f"duplicate change id: {change_id}")
        records[change_id] = ChangeRecord(
            relative_path=relative,
            change_id=change_id,
            profile_id=profile_id,
            base=base,
            intent=intent,
            transition=transition,
            document=document,
        )
    return dict(sorted(records.items()))


def registry_matrix(root: Path, kind: str) -> dict[str, list[dict[str, Any]]]:
    registry = discover_registry(root)
    # Main/push matrix generation also validates all retained change history;
    # it must not silently ignore malformed provenance just because no PR base
    # comparison is available in that workflow.
    discover_changes(root)
    include: list[dict[str, Any]] = []
    if kind == "qualified-profiles":
        for record in registry.values():
            if record.status == QUALIFIED:
                include.append(
                    {
                        "profile_id": record.profile_id,
                        "profile_path": record.relative_path,
                    }
                )
    elif kind == "qualified-devices":
        for record in registry.values():
            if record.status == QUALIFIED:
                for slug in record.device_slugs:
                    include.append(
                        {
                            "device_slug": slug,
                            "profile_id": record.profile_id,
                            "profile_path": record.relative_path,
                        }
                    )
    else:
        raise QualificationCiError(f"unsupported matrix kind: {kind}")
    return {"include": include}


def _changes_for_profile(
    records: Mapping[str, ChangeRecord],
    profile_id: str,
    state: str | None = None,
) -> list[ChangeRecord]:
    return [
        record
        for record in records.values()
        if record.profile_id == profile_id
        and (state is None or record.state == state)
    ]


def _one_change(
    records: Mapping[str, ChangeRecord],
    profile_id: str,
    state: str,
    context: str,
) -> ChangeRecord:
    matches = _changes_for_profile(records, profile_id, state)
    if len(matches) != 1:
        raise QualificationCiError(
            f"{context}: profile {profile_id!r} needs exactly one {state!r} "
            f"change record, found {len(matches)}"
        )
    return matches[0]


def _assert_old_manifest_preserved(
    head_root: Path,
    base: Mapping[str, Any],
    context: str,
) -> None:
    relative, path = _nullable_path(
        head_root,
        base["geometry_manifest"],
        f"{context}.base.geometry_manifest",
    )
    if not path.is_file():
        raise QualificationCiError(
            f"{context}: prior accepted manifest was removed: {relative}"
        )
    actual = _sha256(path)
    if actual != base["manifest_sha256"]:
        raise QualificationCiError(
            f"{context}: prior accepted manifest changed: expected "
            f"{base['manifest_sha256']}, got {actual}"
        )


def _assert_old_fixture_lock_preserved(
    head_root: Path,
    base: Mapping[str, Any],
    context: str,
) -> None:
    relative, path = _nullable_path(
        head_root,
        base["fixture_lock"],
        f"{context}.base.fixture_lock",
    )
    if not path.is_file():
        raise QualificationCiError(
            f"{context}: prior accepted fixture lock was removed: {relative}"
        )
    actual = _sha256(path)
    if actual != base["fixture_lock_sha256"]:
        raise QualificationCiError(
            f"{context}: prior accepted fixture lock changed: expected "
            f"{base['fixture_lock_sha256']}, got {actual}"
        )


def _assert_old_baseline_preserved(
    head_root: Path,
    base: Mapping[str, Any],
    context: str,
) -> None:
    _assert_old_manifest_preserved(head_root, base, context)
    _assert_old_fixture_lock_preserved(head_root, base, context)
    relative, path = _nullable_path(
        head_root,
        base["toolchain_lock"],
        f"{context}.base.toolchain_lock",
    )
    if not path.is_file():
        raise QualificationCiError(
            f"{context}: prior accepted toolchain lock was removed: {relative}"
        )
    actual = _sha256(path)
    if actual != base["toolchain_lock_sha256"]:
        raise QualificationCiError(
            f"{context}: prior accepted toolchain lock changed: expected "
            f"{base['toolchain_lock_sha256']}, got {actual}"
        )


def _assert_candidate_toolchain(
    declaration: ChangeRecord,
    head_root: Path,
) -> None:
    relative, path = _nullable_path(
        head_root,
        declaration.transition["candidate_toolchain_lock"],
        f"{declaration.relative_path}.transition.candidate_toolchain_lock",
    )
    if not path.is_file():
        raise QualificationCiError(
            f"{declaration.relative_path}: candidate toolchain lock is "
            f"missing: {relative}"
        )
    actual = _sha256(path)
    expected = declaration.transition["candidate_toolchain_sha256"]
    if actual != expected:
        raise QualificationCiError(
            f"{declaration.relative_path}: candidate toolchain hash mismatch: "
            f"expected {expected}, got {actual}"
        )


def _assert_candidate_fixture(
    declaration: ChangeRecord,
    head_record: ProfileRecord,
    head_root: Path,
) -> None:
    if declaration.transition[
        "candidate_fixture_interface_sha256"
    ] != head_record.fixture_sha256:
        raise QualificationCiError(
            f"{declaration.relative_path}: candidate fixture hash does not "
            "match the head profile"
        )
    if declaration.transition[
        "candidate_fixture_lock"
    ] != head_record.fixture_lock_path:
        raise QualificationCiError(
            f"{declaration.relative_path}: candidate fixture-lock path does "
            "not match the head profile"
        )
    relative, path = _nullable_path(
        head_root,
        declaration.transition["candidate_fixture_lock"],
        f"{declaration.relative_path}.transition.candidate_fixture_lock",
    )
    if not path.is_file():
        raise QualificationCiError(
            f"{declaration.relative_path}: candidate fixture lock is missing: "
            f"{relative}"
        )
    actual = _sha256(path)
    expected = declaration.transition["candidate_fixture_lock_sha256"]
    if actual != expected or expected != head_record.fixture_lock_sha256:
        raise QualificationCiError(
            f"{declaration.relative_path}: candidate fixture-lock hash "
            f"mismatch: expected {expected}, got {actual}"
        )


def _assert_declaration_matches_base(
    declaration: ChangeRecord,
    base_record: ProfileRecord | None,
    head_root: Path,
) -> None:
    context = declaration.relative_path
    if base_record is None:
        if declaration.base is not None:
            raise QualificationCiError(
                f"{context}: a new unqualified profile must use base=null"
            )
        return
    if declaration.base is None:
        raise QualificationCiError(
            f"{context}: an accepted-profile invalidation needs a base object"
        )
    expected = {
        "profile_path": base_record.relative_path,
        "geometry_manifest": base_record.manifest_path,
        "manifest_sha256": base_record.manifest_sha256,
        "acceptance_ref": base_record.qualification["acceptance_ref"],
        "fixture_interface_sha256": base_record.fixture_sha256,
        "fixture_lock": base_record.fixture_lock_path,
        "fixture_lock_sha256": base_record.fixture_lock_sha256,
        "toolchain_lock": base_record.toolchain_lock_path,
        "toolchain_lock_sha256": base_record.toolchain_lock_sha256,
    }
    if declaration.base != expected:
        raise QualificationCiError(
            f"{context}: base does not exactly identify the accepted profile: "
            f"expected {json.dumps(expected, sort_keys=True)}"
        )
    _assert_old_baseline_preserved(head_root, declaration.base, context)


def _qualification_identity(record: ProfileRecord) -> dict[str, Any]:
    return {
        "acceptance_ref": record.qualification["acceptance_ref"],
        "accepted_on": record.qualification["accepted_on"],
        "accepted_geometry_revision": record.qualification[
            "accepted_geometry_revision"
        ],
        "fixture_interface_sha256": record.qualification[
            "fixture_interface_sha256"
        ],
        "geometry_manifest": record.qualification["geometry_manifest"],
        "artifact_names": list(record.qualification["artifact_names"]),
    }


def _manifest_document(
    root: Path,
    relative: str,
    expected_sha256: str | None = None,
) -> Mapping[str, Any]:
    _, path = _nullable_path(root, relative, "geometry_manifest")
    if not path.is_file():
        raise QualificationCiError(f"geometry manifest is missing: {relative}")
    actual = _sha256(path)
    if expected_sha256 is not None and actual != expected_sha256:
        raise QualificationCiError(
            f"geometry manifest hash mismatch for {relative}: expected "
            f"{expected_sha256}, got {actual}"
        )
    return _strict_json(path)


def _manifest_toolchain(
    root: Path,
    relative: str,
    expected_sha256: str | None = None,
) -> tuple[str, str]:
    manifest = _manifest_document(root, relative, expected_sha256)
    toolchain_relative, toolchain = _nullable_path(
        root,
        manifest.get("toolchain_lock"),
        f"{relative}.toolchain_lock",
    )
    if not toolchain.is_file():
        raise QualificationCiError(
            f"{relative}: toolchain lock is missing: {toolchain_relative}"
        )
    return toolchain_relative, _sha256(toolchain)


def _assert_qualified_immutable(
    base: ProfileRecord,
    head: ProfileRecord,
    base_root: Path,
    head_root: Path,
) -> None:
    if _qualification_identity(base) != _qualification_identity(head):
        raise QualificationCiError(
            f"profile {head.profile_id!r}: qualified provenance changed in "
            "place; invalidate first and requalify in a later PR"
        )
    if (
        base.fixture_lock_path != head.fixture_lock_path
        or base.fixture_lock_sha256 != head.fixture_lock_sha256
    ):
        raise QualificationCiError(
            f"profile {head.profile_id!r}: accepted fixture lock is immutable; "
            "invalidate before selecting a new fixture contract"
        )
    if base.manifest_path is None or base.manifest_sha256 is None:
        raise QualificationCiError(
            f"profile {base.profile_id!r}: base qualification has no manifest"
        )
    _, manifest = _nullable_path(
        head_root,
        base.manifest_path,
        f"profile {head.profile_id}.geometry_manifest",
    )
    if not manifest.is_file() or _sha256(manifest) != base.manifest_sha256:
        raise QualificationCiError(
            f"profile {head.profile_id!r}: accepted manifest is immutable"
        )
    base_toolchain = _manifest_toolchain(
        base_root,
        base.manifest_path,
        base.manifest_sha256,
    )
    head_toolchain = _manifest_toolchain(
        head_root,
        base.manifest_path,
        base.manifest_sha256,
    )
    if head_toolchain != base_toolchain:
        raise QualificationCiError(
            f"profile {head.profile_id!r}: accepted toolchain lock is immutable; "
            "invalidate before selecting a new toolchain"
        )


def _transition_core(record: ChangeRecord) -> dict[str, Any]:
    return {
        "schema": record.document["schema"],
        "change_id": record.change_id,
        "profile_id": record.profile_id,
        "base": record.base,
        "intent": record.intent,
        "candidate_fixture_interface_sha256": record.transition[
            "candidate_fixture_interface_sha256"
        ],
        "candidate_fixture_lock": record.transition[
            "candidate_fixture_lock"
        ],
        "candidate_fixture_lock_sha256": record.transition[
            "candidate_fixture_lock_sha256"
        ],
        "candidate_toolchain_lock": record.transition[
            "candidate_toolchain_lock"
        ],
        "candidate_toolchain_sha256": record.transition[
            "candidate_toolchain_sha256"
        ],
    }


def _lineage_core(record: ChangeRecord) -> dict[str, Any]:
    """Fields that remain fixed while an unqualified candidate is refined."""
    return {
        "schema": record.document["schema"],
        "change_id": record.change_id,
        "profile_id": record.profile_id,
        "base": record.base,
        "intent": record.intent,
    }


def _assert_requalification(
    base_root: Path,
    head_root: Path,
    base_profile: ProfileRecord,
    head_profile: ProfileRecord,
    base_changes: Mapping[str, ChangeRecord],
    head_changes: Mapping[str, ChangeRecord],
) -> ChangeRecord:
    waiting = _one_change(
        base_changes,
        head_profile.profile_id,
        AWAITING,
        "requalification",
    )
    accepted = head_changes.get(waiting.change_id)
    if accepted is None or accepted.state != ACCEPTED:
        raise QualificationCiError(
            f"profile {head_profile.profile_id!r}: the base awaiting change "
            f"{waiting.change_id!r} must be completed"
        )
    if _transition_core(waiting) != _transition_core(accepted):
        raise QualificationCiError(
            f"{accepted.relative_path}: base/intent/candidate identity changed "
            "during physical acceptance"
        )
    _assert_candidate_fixture(waiting, base_profile, base_root)
    _assert_candidate_toolchain(waiting, base_root)
    _assert_candidate_fixture(accepted, head_profile, head_root)
    _assert_candidate_toolchain(accepted, head_root)
    acceptance = accepted.transition["physical_acceptance"]
    assert isinstance(acceptance, dict)
    if (
        waiting.base is not None
        and acceptance["acceptance_ref"] == waiting.base["acceptance_ref"]
    ):
        raise QualificationCiError(
            f"{accepted.relative_path}: requalification needs a fresh "
            "physical acceptance reference"
        )
    if acceptance["acceptance_ref"] != head_profile.qualification["acceptance_ref"]:
        raise QualificationCiError(
            f"{accepted.relative_path}: acceptance_ref does not match profile"
        )
    if acceptance["accepted_on"] != head_profile.qualification["accepted_on"]:
        raise QualificationCiError(
            f"{accepted.relative_path}: accepted_on does not match profile"
        )
    if acceptance["geometry_manifest"] != head_profile.manifest_path:
        raise QualificationCiError(
            f"{accepted.relative_path}: new manifest does not match profile"
        )
    if acceptance["manifest_sha256"] != head_profile.manifest_sha256:
        raise QualificationCiError(
            f"{accepted.relative_path}: new manifest hash does not match"
        )
    if waiting.base is not None:
        _assert_old_baseline_preserved(
            head_root,
            waiting.base,
            accepted.relative_path,
        )
        if head_profile.manifest_path == waiting.base["geometry_manifest"]:
            raise QualificationCiError(
                f"{accepted.relative_path}: requalification must add a new "
                "immutable manifest"
            )
    if head_profile.manifest_path is None:
        raise QualificationCiError(
            f"profile {head_profile.profile_id!r}: missing new manifest"
        )
    manifest_toolchain = _manifest_toolchain(
        head_root,
        head_profile.manifest_path,
        head_profile.manifest_sha256,
    )
    declared_toolchain = (
        str(accepted.transition["candidate_toolchain_lock"]),
        str(accepted.transition["candidate_toolchain_sha256"]),
    )
    if manifest_toolchain != declared_toolchain:
        raise QualificationCiError(
            f"{accepted.relative_path}: accepted manifest toolchain does not "
            "match the reviewed candidate toolchain"
        )
    prior_path = base_root / head_profile.manifest_path
    if prior_path.exists():
        raise QualificationCiError(
            f"profile {head_profile.profile_id!r}: new qualification manifest "
            "already existed at the PR base"
        )
    if head_profile.qualification["accepted_geometry_revision"] == (
        base_profile.qualification.get("accepted_geometry_revision")
    ):
        raise QualificationCiError(
            f"profile {head_profile.profile_id!r}: requalification needs a new "
            "accepted_geometry_revision"
        )
    return accepted


def build_plan(head_root: Path, base_root: Path) -> dict[str, Any]:
    head_root = head_root.resolve()
    base_root = base_root.resolve()
    head = discover_registry(head_root)
    base = discover_registry(base_root)
    head_changes = discover_changes(head_root)
    base_changes = discover_changes(base_root)

    jobs: list[dict[str, Any]] = []
    used_head_changes: set[str] = set()
    accounted_qualified: set[str] = set()

    # Change records are the durable audit trail. An awaiting record may only
    # advance its candidate state or become accepted; an accepted record is
    # immutable forever. In particular, deletion must not evade the checks
    # below, which otherwise iterate only records still present at head.
    for change_id, base_change in base_changes.items():
        head_change = head_changes.get(change_id)
        if head_change is None:
            raise QualificationCiError(
                f"{base_change.relative_path}: retained change history cannot "
                "be removed"
            )
        if base_change.state == ACCEPTED:
            if head_change.document != base_change.document:
                raise QualificationCiError(
                    f"{head_change.relative_path}: completed change history is "
                    "immutable"
                )
        elif _lineage_core(head_change) != _lineage_core(base_change):
            raise QualificationCiError(
                f"{head_change.relative_path}: an awaiting change must "
                "preserve its base and intent"
            )

    for profile_id in sorted(set(base) | set(head)):
        base_record = base.get(profile_id)
        head_record = head.get(profile_id)

        if base_record is not None and base_record.status == QUALIFIED:
            if head_record is None:
                raise QualificationCiError(
                    f"profile {profile_id!r}: a base-qualified profile cannot "
                    "be removed"
                )
            if head_record.status == QUALIFIED:
                _assert_qualified_immutable(
                    base_record,
                    head_record,
                    base_root,
                    head_root,
                )
                jobs.append(
                    _job_row(head_record, base_record, "protect", None)
                )
                accounted_qualified.add(profile_id)
            else:
                declaration = _one_change(
                    head_changes,
                    profile_id,
                    AWAITING,
                    "qualification invalidation",
                )
                if declaration.change_id in base_changes:
                    raise QualificationCiError(
                        f"{declaration.relative_path}: invalidation declaration "
                        "must be introduced with the downgrade"
                    )
                _assert_declaration_matches_base(
                    declaration,
                    base_record,
                    head_root,
                )
                _assert_candidate_fixture(declaration, head_record, head_root)
                _assert_candidate_toolchain(declaration, head_root)
                jobs.append(
                    _job_row(
                        head_record,
                        base_record,
                        "invalidate",
                        declaration,
                    )
                )
                used_head_changes.add(declaration.change_id)
            continue

        if head_record is None:
            continue
        if head_record.status == QUALIFIED:
            if base_record is None:
                raise QualificationCiError(
                    f"profile {profile_id!r}: a new profile must land "
                    "unqualified before physical qualification"
                )
            declaration = _assert_requalification(
                base_root,
                head_root,
                base_record,
                head_record,
                base_changes,
                head_changes,
            )
            jobs.append(
                _job_row(
                    head_record,
                    base_record,
                    "requalify",
                    declaration,
                )
            )
            used_head_changes.add(declaration.change_id)
            accounted_qualified.add(profile_id)
            continue

        waiting = _changes_for_profile(head_changes, profile_id, AWAITING)
        if len(waiting) > 1:
            raise QualificationCiError(
                f"profile {profile_id!r}: multiple awaiting change records"
            )
        if waiting:
            declaration = waiting[0]
            if declaration.base is not None:
                _assert_old_baseline_preserved(
                    head_root,
                    declaration.base,
                    declaration.relative_path,
                )
                base_declaration = base_changes.get(declaration.change_id)
                if (
                    base_declaration is None
                    or _lineage_core(base_declaration)
                    != _lineage_core(declaration)
                    or base_declaration.state != AWAITING
                ):
                    raise QualificationCiError(
                        f"{declaration.relative_path}: an existing invalidated "
                        "candidate must preserve its base and intent"
                    )
            else:
                # An existing draft may begin a candidate lifecycle with no
                # accepted baseline, so base=null is correct here.
                _assert_declaration_matches_base(
                    declaration,
                    None,
                    head_root,
                )
            _assert_candidate_fixture(declaration, head_record, head_root)
            _assert_candidate_toolchain(declaration, head_root)
            jobs.append(
                _job_row(
                    head_record,
                    base_record,
                    "candidate",
                    declaration,
                )
            )
            used_head_changes.add(declaration.change_id)

    for record in head_changes.values():
        if record.state == AWAITING and record.change_id not in used_head_changes:
            raise QualificationCiError(
                f"{record.relative_path}: awaiting change is not attached to an "
                "unqualified profile transition"
            )
        if record.state == ACCEPTED and record.change_id not in used_head_changes:
            prior = base_changes.get(record.change_id)
            if prior is None:
                raise QualificationCiError(
                    f"{record.relative_path}: a completed change must advance "
                    "an awaiting record from the PR base"
                )
            if prior.document != record.document:
                raise QualificationCiError(
                    f"{record.relative_path}: completed change history is "
                    "immutable outside its requalification transition"
                )

    head_qualified = {
        profile_id
        for profile_id, record in head.items()
        if record.status == QUALIFIED
    }
    if accounted_qualified != head_qualified:
        missing = sorted(head_qualified - accounted_qualified)
        raise QualificationCiError(
            "qualified profile(s) escaped the CI plan: " + ", ".join(missing)
        )

    return {
        "schema": PLAN_SCHEMA,
        "base": {
            "qualified_profiles": sorted(
                profile_id
                for profile_id, record in base.items()
                if record.status == QUALIFIED
            )
        },
        "head": {
            "qualified_profiles": sorted(head_qualified),
            "qualified_devices": [
                slug
                for record in head.values()
                if record.status == QUALIFIED
                for slug in record.device_slugs
            ],
        },
        "matrix": {"include": jobs},
    }


def _job_row(
    head: ProfileRecord,
    base: ProfileRecord | None,
    mode: str,
    declaration: ChangeRecord | None,
) -> dict[str, Any]:
    return {
        "base_profile_path": (
            base.relative_path if base is not None else ""
        ),
        "change_path": (
            declaration.relative_path if declaration is not None else ""
        ),
        "head_status": head.status,
        "mode": mode,
        "profile_id": head.profile_id,
        "profile_path": head.relative_path,
    }


def _decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered


def _number(value: Any) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise QualificationCiError(f"invalid metric number: {value!r}") from exc
    if not result.is_finite():
        raise QualificationCiError(f"non-finite metric number: {value!r}")
    return result


def _delta_text(candidate: Any, baseline: Any) -> str:
    return _decimal_text(_number(candidate) - _number(baseline))


def metric_delta(
    baseline: Mapping[str, Any] | None,
    candidate: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    if baseline is None:
        return None
    bounds_delta = {
        field: [
            _delta_text(candidate["bounds_mm"][field][index], value)
            for index, value in enumerate(baseline["bounds_mm"][field])
        ]
        for field in ("min", "max", "size")
    }
    topology_delta = {
        field: int(candidate["topology"][field]) - int(value)
        for field, value in sorted(baseline["topology"].items())
    }
    return {
        "bounds_mm": bounds_delta,
        "fingerprint_changed": (
            candidate["fingerprint"] != baseline["fingerprint"]
        ),
        "surface_area_mm2": _delta_text(
            candidate["surface_area_mm2"],
            baseline["surface_area_mm2"],
        ),
        "topology": topology_delta,
        "triangle_count": (
            int(candidate["triangle_count"])
            - int(baseline["triangle_count"])
        ),
        "volume_mm3": _delta_text(
            candidate["volume_mm3"],
            baseline["volume_mm3"],
        ),
    }


def _manifest_artifacts(
    root: Path,
    relative: str,
    expected_sha256: str | None = None,
) -> Mapping[str, Any]:
    document = _manifest_document(root, relative, expected_sha256)
    artifacts = document.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise QualificationCiError(
            f"{relative}: artifacts must be a non-empty object"
        )
    return artifacts


def _baseline_for_job(
    job: Mapping[str, Any],
    base_root: Path,
    head_root: Path,
    base_registry: Mapping[str, ProfileRecord],
    head_changes: Mapping[str, ChangeRecord],
) -> Mapping[str, Any] | None:
    profile_id = str(job["profile_id"])
    if job["mode"] in {"protect", "invalidate"}:
        base = base_registry[profile_id]
        assert base.manifest_path is not None
        return _manifest_artifacts(
            base_root,
            base.manifest_path,
            base.manifest_sha256,
        )
    if job["mode"] in {"candidate", "requalify"}:
        change_path = str(job["change_path"])
        declaration = next(
            record
            for record in head_changes.values()
            if record.relative_path == change_path
        )
        if declaration.base is None:
            return None
        return _manifest_artifacts(
            head_root,
            str(declaration.base["geometry_manifest"]),
            str(declaration.base["manifest_sha256"]),
        )
    raise QualificationCiError(f"unknown job mode: {job['mode']}")


def _target_for_requalification(
    job: Mapping[str, Any],
    head_registry: Mapping[str, ProfileRecord],
    head_root: Path,
) -> Mapping[str, Any] | None:
    if job["mode"] != "requalify":
        return None
    record = head_registry[str(job["profile_id"])]
    assert record.manifest_path is not None
    return _manifest_artifacts(
        head_root,
        record.manifest_path,
        record.manifest_sha256,
    )


def _candidate_toolchain_for_job(
    job: Mapping[str, Any],
    head_root: Path,
    base_root: Path,
    head_registry: Mapping[str, ProfileRecord],
    base_registry: Mapping[str, ProfileRecord],
    head_changes: Mapping[str, ChangeRecord],
) -> tuple[str, str]:
    profile_id = str(job["profile_id"])
    if job["mode"] == "protect":
        base = base_registry[profile_id]
        assert base.manifest_path is not None
        return _manifest_toolchain(
            base_root,
            base.manifest_path,
            base.manifest_sha256,
        )
    if job["mode"] in {"invalidate", "candidate"}:
        declaration = next(
            record
            for record in head_changes.values()
            if record.relative_path == job["change_path"]
        )
        return (
            str(declaration.transition["candidate_toolchain_lock"]),
            str(declaration.transition["candidate_toolchain_sha256"]),
        )
    if job["mode"] == "requalify":
        head = head_registry[profile_id]
        assert head.manifest_path is not None
        return _manifest_toolchain(
            head_root,
            head.manifest_path,
            head.manifest_sha256,
        )
    raise QualificationCiError(f"unknown job mode: {job['mode']}")


def _base_toolchain_for_job(
    job: Mapping[str, Any],
    head_root: Path,
    base_root: Path,
    base_registry: Mapping[str, ProfileRecord],
    head_changes: Mapping[str, ChangeRecord],
) -> tuple[str, str] | None:
    profile_id = str(job["profile_id"])
    if job["mode"] in {"protect", "invalidate"}:
        base = base_registry[profile_id]
        assert base.manifest_path is not None
        return _manifest_toolchain(
            base_root,
            base.manifest_path,
            base.manifest_sha256,
        )
    declaration = next(
        (
            record
            for record in head_changes.values()
            if record.relative_path == job["change_path"]
        ),
        None,
    )
    if declaration is None or declaration.base is None:
        return None
    return (
        str(declaration.base["toolchain_lock"]),
        str(declaration.base["toolchain_lock_sha256"]),
    )


def _prepare_output(root: Path, output: Path) -> Path:
    resolved = output.resolve()
    root = root.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        relative = None
    if relative is not None and (
        not relative.parts or relative.parts[0] != "build"
    ):
        raise QualificationCiError(
            "qualification output inside the cradle must stay under build/: "
            f"{relative.as_posix()}"
        )
    if relative is None:
        repository_root = next(
            (
                ancestor
                for ancestor in (root, *root.parents)
                if (ancestor / ".git").exists()
            ),
            None,
        )
        if repository_root is not None:
            try:
                repository_relative = resolved.relative_to(repository_root)
            except ValueError:
                repository_relative = None
            if repository_relative is not None:
                raise QualificationCiError(
                    "qualification output cannot target repository source: "
                    f"{repository_relative.as_posix()}"
                )
    if resolved.exists():
        raise QualificationCiError(
            f"refusing to overwrite existing qualification output: {resolved}"
        )
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def check_job(
    head_root: Path,
    base_root: Path,
    profile_id: str,
    output: Path,
    *,
    openscad: str = "openscad",
    renderer: Renderer = holder_profiles.render_artifact,
    verify_toolchain: bool = True,
) -> Mapping[str, Any]:
    """Render one planned profile, write its report, and enforce its mode."""
    head_root = head_root.resolve()
    base_root = base_root.resolve()
    output = _prepare_output(head_root, output)
    plan = build_plan(head_root, base_root)
    matches = [
        row
        for row in plan["matrix"]["include"]
        if row["profile_id"] == profile_id
    ]
    if len(matches) != 1:
        raise QualificationCiError(
            f"profile {profile_id!r} appears {len(matches)} times in CI plan"
        )
    job = matches[0]
    head_registry = discover_registry(head_root)
    base_registry = discover_registry(base_root)
    head_changes = discover_changes(head_root)
    record = head_registry[profile_id]
    candidate_toolchain = _candidate_toolchain_for_job(
        job,
        head_root,
        base_root,
        head_registry,
        base_registry,
        head_changes,
    )
    base_toolchain = _base_toolchain_for_job(
        job,
        head_root,
        base_root,
        base_registry,
        head_changes,
    )
    if job["mode"] in {"protect", "invalidate"}:
        base_fixture_record = base_registry[profile_id]
        base_fixture_lock: Mapping[str, str] | None = {
            "path": base_fixture_record.fixture_lock_path,
            "sha256": base_fixture_record.fixture_lock_sha256,
        }
    else:
        declaration = next(
            (
                item
                for item in head_changes.values()
                if item.relative_path == job["change_path"]
            ),
            None,
        )
        base_fixture_lock = (
            {
                "path": str(declaration.base["fixture_lock"]),
                "sha256": str(declaration.base["fixture_lock_sha256"]),
            }
            if declaration is not None and declaration.base is not None
            else None
        )
    if verify_toolchain:
        _, toolchain_path = _nullable_path(
            head_root,
            candidate_toolchain[0],
            "candidate_toolchain_lock",
        )
        actual_toolchain_hash = _sha256(toolchain_path)
        if actual_toolchain_hash != candidate_toolchain[1]:
            raise QualificationCiError(
                "candidate toolchain changed after planning: expected "
                f"{candidate_toolchain[1]}, got {actual_toolchain_hash}"
            )
        check_toolchain(toolchain_path, openscad)
        if job["mode"] == "requalify":
            _, base_candidate_toolchain = _nullable_path(
                base_root,
                candidate_toolchain[0],
                "base_candidate_toolchain_lock",
            )
            actual_base_toolchain_hash = _sha256(base_candidate_toolchain)
            if actual_base_toolchain_hash != candidate_toolchain[1]:
                raise QualificationCiError(
                    "physical-acceptance-base toolchain changed: expected "
                    f"{candidate_toolchain[1]}, got "
                    f"{actual_base_toolchain_hash}"
                )
            check_toolchain(base_candidate_toolchain, openscad)
    baseline_artifacts = _baseline_for_job(
        job,
        base_root,
        head_root,
        base_registry,
        head_changes,
    )
    target_artifacts = _target_for_requalification(
        job,
        head_registry,
        head_root,
    )

    artifact_reports: dict[str, Any] = {}
    errors: list[str] = []
    added: list[str] = []
    changed: list[str] = []
    physical_acceptance_drift: list[str] = []
    removed: list[str] = []
    unchanged: list[str] = []

    acceptance_base_names: set[str] = set()
    acceptance_base_metrics: dict[str, Mapping[str, Any] | None] = {}
    acceptance_base_records: dict[str, Mapping[str, Any] | None] = {}
    if job["mode"] == "requalify":
        acceptance_base = base_registry[profile_id]
        acceptance_base_names = set(acceptance_base.resolved.artifacts)
        acceptance_directory = output / "physical-acceptance-base-candidates"
        acceptance_directory.mkdir(parents=True, exist_ok=True)
        for artifact_name in sorted(acceptance_base_names):
            path = acceptance_directory / f"{artifact_name}.stl"
            metrics: Mapping[str, Any] | None = None
            try:
                renderer(
                    acceptance_base.resolved,
                    artifact_name,
                    path,
                    openscad=openscad,
                )
                canonicalize_stl(path)
                metrics = describe_mesh(path)
                topology = metrics["topology"]
                if (
                    topology["boundary_edges"] != 0
                    or topology["nonmanifold_edges"] != 0
                ):
                    errors.append(
                        f"{artifact_name}: physical-acceptance-base candidate "
                        "is not closed/manifold"
                    )
            except (
                OSError,
                StlError,
                holder_profiles.ProfileError,
                QualificationCiError,
            ) as exc:
                errors.append(
                    f"{artifact_name}: cannot render physical-acceptance-base "
                    f"candidate: {exc}"
                )
            acceptance_base_metrics[artifact_name] = metrics
            acceptance_base_records[artifact_name] = (
                {
                    **metrics,
                    "path": (
                        "physical-acceptance-base-candidates/"
                        f"{artifact_name}.stl"
                    ),
                    "raw_sha256": _sha256(path),
                    "serialization": CANONICAL_ASCII_STL_SCHEMA,
                    "size_bytes": path.stat().st_size,
                }
                if metrics is not None
                else None
            )

    candidates = output / "candidates"
    candidates.mkdir(parents=True, exist_ok=True)
    candidate_names = set(record.resolved.artifacts)
    baseline_names = set(baseline_artifacts or {})
    target_names = set(target_artifacts or {})
    for artifact_name in sorted(
        candidate_names
        | baseline_names
        | target_names
        | acceptance_base_names
    ):
        path = candidates / f"{artifact_name}.stl"
        candidate_present = artifact_name in candidate_names
        candidate: Mapping[str, Any] | None = None
        render_error: str | None = None
        if candidate_present:
            try:
                renderer(
                    record.resolved,
                    artifact_name,
                    path,
                    openscad=openscad,
                )
                canonicalize_stl(path)
                candidate = describe_mesh(path)
            except (
                OSError,
                StlError,
                holder_profiles.ProfileError,
                QualificationCiError,
            ) as exc:
                render_error = str(exc)
                errors.append(f"{artifact_name}: {exc}")

        baseline_expected = None
        baseline_present = (
            baseline_artifacts is not None
            and artifact_name in baseline_artifacts
        )
        if baseline_present:
            baseline_entry = baseline_artifacts[artifact_name]
            if not isinstance(baseline_entry, dict) or not isinstance(
                baseline_entry.get("expected"), dict
            ):
                errors.append(
                    f"{artifact_name}: missing from baseline qualification"
                )
            else:
                baseline_expected = baseline_entry["expected"]

        target_expected = None
        target_present = (
            target_artifacts is not None
            and artifact_name in target_artifacts
        )
        if target_present:
            target_entry = target_artifacts[artifact_name]
            if not isinstance(target_entry, dict) or not isinstance(
                target_entry.get("expected"), dict
            ):
                errors.append(
                    f"{artifact_name}: missing from requalification manifest"
                )
            else:
                target_expected = target_entry["expected"]

        matches_baseline = (
            None
            if baseline_artifacts is None
            else (
                candidate_present == baseline_present
                and (
                    not candidate_present
                    or (
                        candidate is not None
                        and candidate == baseline_expected
                    )
                )
            )
        )
        matches_target = (
            None
            if target_artifacts is None
            else (
                candidate_present == target_present
                and (
                    not candidate_present
                    or (
                        candidate is not None
                        and candidate == target_expected
                    )
                )
            )
        )
        acceptance_base_present = artifact_name in acceptance_base_names
        acceptance_base_candidate = acceptance_base_metrics.get(artifact_name)
        matches_acceptance_base = (
            None
            if job["mode"] != "requalify"
            else (
                candidate_present == acceptance_base_present
                and (
                    not candidate_present
                    or (
                        candidate is not None
                        and candidate == acceptance_base_candidate
                    )
                )
            )
        )
        if matches_acceptance_base is False:
            physical_acceptance_drift.append(artifact_name)
        if baseline_artifacts is None:
            if candidate_present:
                added.append(artifact_name)
                changed.append(artifact_name)
        elif matches_baseline is True:
            unchanged.append(artifact_name)
        else:
            changed.append(artifact_name)
            if candidate_present and not baseline_present:
                added.append(artifact_name)
            elif baseline_present and not candidate_present:
                removed.append(artifact_name)

        if candidate is not None:
            topology = candidate["topology"]
            if (
                topology["boundary_edges"] != 0
                or topology["nonmanifold_edges"] != 0
            ):
                errors.append(
                    f"{artifact_name}: candidate is not closed/manifold "
                    f"(boundary_edges={topology['boundary_edges']}, "
                    f"nonmanifold_edges={topology['nonmanifold_edges']})"
                )

        artifact_reports[artifact_name] = {
            "baseline_present": baseline_present,
            "baseline": baseline_expected,
            "candidate_present": candidate_present,
            "candidate": (
                {
                    **candidate,
                    "path": f"candidates/{artifact_name}.stl",
                    "raw_sha256": _sha256(path),
                    "serialization": CANONICAL_ASCII_STL_SCHEMA,
                    "size_bytes": path.stat().st_size,
                }
                if candidate is not None
                else None
            ),
            "delta": (
                metric_delta(baseline_expected, candidate)
                if candidate is not None
                else None
            ),
            "matches_baseline": matches_baseline,
            "matches_physical_acceptance_base": matches_acceptance_base,
            "matches_qualification_target": matches_target,
            "physical_acceptance_base": acceptance_base_records.get(
                artifact_name
            ),
            "physical_acceptance_base_present": acceptance_base_present,
            "physical_acceptance_delta": (
                metric_delta(acceptance_base_candidate, candidate)
                if (
                    acceptance_base_candidate is not None
                    and candidate is not None
                )
                else None
            ),
            "qualification_target": target_expected,
            "qualification_target_present": target_present,
            "render_error": render_error,
        }

    report = {
        "schema": REPORT_SCHEMA,
        "profile_id": profile_id,
        "mode": job["mode"],
        "qualification_transition": {
            "base_status": (
                base_registry[profile_id].status
                if profile_id in base_registry
                else None
            ),
            "head_status": record.status,
            "change_path": job["change_path"] or None,
            "base_fixture_interface_sha256": (
                base_registry[profile_id].fixture_sha256
                if profile_id in base_registry
                else None
            ),
            "candidate_fixture_interface_sha256": record.fixture_sha256,
            "base_fixture_lock": base_fixture_lock,
            "candidate_fixture_lock": {
                "path": record.fixture_lock_path,
                "sha256": record.fixture_lock_sha256,
            },
            "base_toolchain": (
                {
                    "path": base_toolchain[0],
                    "sha256": base_toolchain[1],
                }
                if base_toolchain is not None
                else None
            ),
            "candidate_toolchain": {
                "path": candidate_toolchain[0],
                "sha256": candidate_toolchain[1],
            },
        },
        "artifacts": artifact_reports,
        "summary": {
            "added_artifacts": added,
            "changed_artifacts": changed,
            "physical_acceptance_drift_artifacts": (
                physical_acceptance_drift
            ),
            "removed_artifacts": removed,
            "unchanged_artifacts": unchanged,
            "errors": errors,
        },
    }
    _write_json(output / "geometry-diff.json", report)

    if job["mode"] == "protect":
        drift = [
            name
            for name, row in artifact_reports.items()
            if row["matches_baseline"] is not True
        ]
        if drift:
            errors.append(
                "qualified geometry drifted without invalidation: "
                + ", ".join(drift)
            )
    elif job["mode"] == "requalify":
        if physical_acceptance_drift:
            errors.append(
                "candidate drifted after physical acceptance: "
                + ", ".join(physical_acceptance_drift)
            )
        mismatch = [
            name
            for name, row in artifact_reports.items()
            if row["matches_qualification_target"] is not True
        ]
        if mismatch:
            errors.append(
                "candidate does not match new qualification manifest: "
                + ", ".join(mismatch)
            )

    if errors:
        # Rewrite after adding mode-level errors so the uploaded report is the
        # complete deterministic failure explanation.
        report["summary"]["errors"] = errors
        _write_json(output / "geometry-diff.json", report)
        raise QualificationCiError("\n".join(errors))
    return report


def check_mutation_guard(
    head_root: Path,
    base_root: Path,
    profile_id: str,
    output: Path,
    *,
    openscad: str = "openscad",
) -> Mapping[str, Any]:
    """Prove that a printable 0.1 mm hook mutation is detected and reported."""
    registry = discover_registry(head_root)
    record = registry.get(profile_id)
    if record is None or record.status != QUALIFIED:
        raise QualificationCiError(
            f"profile {profile_id!r} must be physically qualified for the "
            "mutation guard"
        )
    current = record.resolved.openscad_parameters.get("hook_throat")
    if not isinstance(current, Decimal):
        current = _number(current)

    def mutated_renderer(
        resolved: holder_profiles.ResolvedProfile,
        artifact_name: str,
        path: Path,
        *,
        openscad: str,
    ) -> None:
        overrides = (
            {"hook_throat": current + Decimal("0.1")}
            if artifact_name == "j_hook"
            else None
        )
        holder_profiles.render_artifact(
            resolved,
            artifact_name,
            path,
            openscad=openscad,
            parameter_overrides=overrides,
        )

    try:
        check_job(
            head_root,
            base_root,
            profile_id,
            output,
            openscad=openscad,
            renderer=mutated_renderer,
        )
    except QualificationCiError:
        report_path = output.resolve() / "geometry-diff.json"
        if not report_path.is_file():
            raise
        report = _strict_json(report_path)
        summary = report.get("summary")
        artifacts = report.get("artifacts")
        if not isinstance(summary, dict) or not isinstance(artifacts, dict):
            raise QualificationCiError(
                "mutation guard produced a malformed geometry diff"
            )
        hook = artifacts.get("j_hook")
        if not isinstance(hook, dict):
            raise QualificationCiError(
                "0.1 mm hook mutation produced no j_hook report"
            )
        if report.get("mode") == "requalify":
            target_mismatches = sorted(
                name
                for name, row in artifacts.items()
                if (
                    isinstance(row, dict)
                    and row.get("matches_qualification_target") is not True
                )
            )
            isolated = target_mismatches == ["j_hook"]
            target = hook.get("qualification_target")
            candidate = hook.get("candidate")
            fingerprint_changed = (
                isinstance(target, dict)
                and isinstance(candidate, dict)
                and target.get("fingerprint") != candidate.get("fingerprint")
            )
        else:
            isolated = summary.get("changed_artifacts") == ["j_hook"]
            delta = hook.get("delta")
            fingerprint_changed = (
                isinstance(delta, dict)
                and delta.get("fingerprint_changed") is True
            )
        if not isolated:
            raise QualificationCiError(
                "0.1 mm hook mutation did not isolate j_hook drift"
            )
        if not fingerprint_changed:
            raise QualificationCiError(
                "0.1 mm hook mutation did not change the normalized fingerprint"
            )
        return report
    raise QualificationCiError(
        "0.1 mm hook mutation unexpectedly passed qualified geometry"
    )


def main(argv: Sequence[str] | None = None) -> int:
    default_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    subparsers = parser.add_subparsers(dest="command", required=True)

    matrix_parser = subparsers.add_parser("matrix")
    matrix_parser.add_argument(
        "--kind",
        choices=("qualified-profiles", "qualified-devices"),
        required=True,
    )

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--base-root", type=Path, required=True)
    plan_parser.add_argument("--output", type=Path, required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--base-root", type=Path, required=True)
    check_parser.add_argument("--profile-id", required=True)
    check_parser.add_argument("--output", type=Path, required=True)
    check_parser.add_argument("--openscad", default="openscad")

    mutation_parser = subparsers.add_parser("check-mutation")
    mutation_parser.add_argument("--base-root", type=Path, required=True)
    mutation_parser.add_argument("--profile-id", required=True)
    mutation_parser.add_argument("--output", type=Path, required=True)
    mutation_parser.add_argument("--openscad", default="openscad")

    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "matrix":
            print(
                json.dumps(
                    registry_matrix(root, args.kind),
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
        elif args.command == "plan":
            plan = build_plan(root, args.base_root)
            output = _prepare_output(root, args.output)
            _write_json(output, plan)
            print(
                f"qualification_plan=pass jobs="
                f"{len(plan['matrix']['include'])} output={output}"
            )
        elif args.command == "check":
            report = check_job(
                root,
                args.base_root,
                args.profile_id,
                args.output,
                openscad=args.openscad,
            )
            print(
                f"qualification_ci=pass profile={args.profile_id} "
                f"mode={report['mode']} output={args.output}"
            )
        else:
            report = check_mutation_guard(
                root,
                args.base_root,
                args.profile_id,
                args.output,
                openscad=args.openscad,
            )
            print(
                f"qualification_mutation_guard=pass profile={args.profile_id} "
                f"changed={','.join(report['summary']['changed_artifacts'])} "
                f"output={args.output}"
            )
        return 0
    except (
        OSError,
        QualificationCiError,
        holder_profiles.ProfileError,
    ) as exc:
        print(f"qualification_ci_error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
