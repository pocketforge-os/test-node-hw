#!/usr/bin/env python3
"""Check or deliberately re-record physically qualified STL geometry."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Mapping

from mesh_fingerprint import (
    COORDINATE_QUANTUM_MM,
    FINGERPRINT_ALGORITHM,
    StlError,
    describe_mesh,
)

MANIFEST_SCHEMA = "pocketforge-qualified-geometry-v1"
TOOLCHAIN_SCHEMA = "pocketforge-cad-toolchain-v1"


class QualificationError(ValueError):
    """The qualification contract or generated geometry is invalid."""


def _load_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise QualificationError(f"{path} must contain a JSON object")
    return value


def _project_path(root: Path, relative: object, field: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise QualificationError(f"{field} must be a non-empty relative path")
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise QualificationError(f"{field} escapes project root: {relative}") from exc
    return path


def _validate_manifest_contract(
    root: Path, manifest: Mapping[str, object]
) -> tuple[Path, Mapping[str, object]]:
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise QualificationError(
            f"unsupported manifest schema: {manifest.get('schema')!r}"
        )
    fingerprint = manifest.get("fingerprint_contract")
    if not isinstance(fingerprint, dict):
        raise QualificationError("fingerprint_contract must be an object")
    if fingerprint.get("algorithm") != FINGERPRINT_ALGORITHM:
        raise QualificationError(
            f"fingerprint algorithm mismatch: {fingerprint.get('algorithm')!r}"
        )
    if fingerprint.get("coordinate_quantum_mm") != str(COORDINATE_QUANTUM_MM):
        raise QualificationError(
            "fingerprint coordinate quantum mismatch: "
            f"{fingerprint.get('coordinate_quantum_mm')!r}"
        )

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise QualificationError("artifacts must be a non-empty object")
    qualification = manifest.get("qualification")
    if not isinstance(qualification, dict):
        raise QualificationError("qualification must be an object")
    if qualification.get("status") not in {
        "draft",
        "unqualified",
        "physically_accepted",
    }:
        raise QualificationError(
            f"unsupported qualification status: {qualification.get('status')!r}"
        )
    toolchain_path = _project_path(
        root, manifest.get("toolchain_lock"), "toolchain_lock"
    )
    return toolchain_path, artifacts


def _require_physical_acceptance(manifest: Mapping[str, object]) -> None:
    qualification = manifest["qualification"]
    assert isinstance(qualification, dict)
    if qualification.get("status") != "physically_accepted":
        raise QualificationError(
            "ordinary qualification checks require status=physically_accepted"
        )
    acceptance_ref = qualification.get("acceptance_ref")
    if not isinstance(acceptance_ref, str) or not acceptance_ref.strip():
        raise QualificationError("physically accepted geometry needs acceptance_ref")
    accepted_on = qualification.get("accepted_on")
    if not isinstance(accepted_on, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", accepted_on
    ):
        raise QualificationError(
            "physically accepted geometry needs accepted_on=YYYY-MM-DD"
        )
    for field in ("accepted_source_revision", "characterized_source_revision"):
        revision = qualification.get(field)
        if not isinstance(revision, str) or not re.fullmatch(
            r"[0-9a-f]{40}", revision
        ):
            raise QualificationError(f"{field} must be a full lowercase Git SHA")


def check_toolchain(lock_path: Path, openscad: str) -> None:
    lock = _load_json(lock_path)
    if lock.get("schema") != TOOLCHAIN_SCHEMA:
        raise QualificationError(
            f"unsupported toolchain schema: {lock.get('schema')!r}"
        )
    expected = lock.get("openscad_reported_version")
    if not isinstance(expected, str) or not expected:
        raise QualificationError("openscad_reported_version must be a string")
    fingerprint = lock.get("fingerprint")
    if not isinstance(fingerprint, dict) or fingerprint != {
        "algorithm": FINGERPRINT_ALGORITHM,
        "coordinate_quantum_mm": str(COORDINATE_QUANTUM_MM),
    }:
        raise QualificationError("toolchain fingerprint contract is stale")

    try:
        result = subprocess.run(
            [openscad, "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise QualificationError(f"cannot run {openscad!r}: {exc}") from exc
    reported = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    if result.returncode != 0:
        raise QualificationError(
            f"{openscad!r} --version failed with {result.returncode}: {reported}"
        )
    expected_line = f"OpenSCAD version {expected}"
    if expected_line not in reported.splitlines():
        raise QualificationError(
            f"OpenSCAD mismatch: expected {expected_line!r}, got {reported!r}"
        )
    print(
        f"qualified_toolchain=pass openscad={expected} "
        f"lock={lock_path.as_posix()}"
    )


def _artifact_expected(
    artifact_name: str, artifact: object
) -> tuple[str, Mapping[str, object]]:
    if not isinstance(artifact, dict):
        raise QualificationError(f"artifact {artifact_name!r} must be an object")
    path = artifact.get("path")
    if not isinstance(path, str) or not path:
        raise QualificationError(f"artifact {artifact_name!r} has invalid path")
    expected = artifact.get("expected")
    if not isinstance(expected, dict):
        raise QualificationError(
            f"artifact {artifact_name!r} expected metrics must be an object"
        )
    return path, expected


def compare_artifact(
    artifact_name: str,
    path: Path,
    expected: Mapping[str, object],
) -> list[str]:
    try:
        actual = describe_mesh(path)
    except (OSError, StlError) as exc:
        return [f"mesh_error expected=valid actual={exc}"]

    mismatches: list[str] = []
    topology = actual["topology"]
    assert isinstance(topology, dict)
    if topology["boundary_edges"] != 0 or topology["nonmanifold_edges"] != 0:
        mismatches.append(
            "topology_not_closed "
            f"boundary_edges={topology['boundary_edges']} "
            f"nonmanifold_edges={topology['nonmanifold_edges']}"
        )
    expected_keys = {
        "fingerprint",
        "triangle_count",
        "bounds_mm",
        "surface_area_mm2",
        "volume_mm3",
        "topology",
    }
    missing = sorted(expected_keys - set(expected))
    unexpected = sorted(set(expected) - expected_keys)
    if missing:
        mismatches.append(f"manifest_missing_fields={missing}")
    if unexpected:
        mismatches.append(f"manifest_unexpected_fields={unexpected}")

    for field in sorted(expected_keys & set(expected)):
        if expected[field] != actual[field]:
            mismatches.append(
                f"field={field} expected={json.dumps(expected[field], sort_keys=True)} "
                f"actual={json.dumps(actual[field], sort_keys=True)}"
            )
    return mismatches


def check_manifest(
    root: Path,
    manifest_path: Path,
    *,
    openscad: str,
    verify_toolchain: bool = True,
) -> None:
    manifest = _load_json(manifest_path)
    toolchain_path, artifacts = _validate_manifest_contract(root, manifest)
    _require_physical_acceptance(manifest)
    if verify_toolchain:
        check_toolchain(toolchain_path, openscad)

    failures: list[str] = []
    for artifact_name, artifact in artifacts.items():
        path_text, expected = _artifact_expected(artifact_name, artifact)
        path = _project_path(root, path_text, f"artifacts.{artifact_name}.path")
        mismatches = compare_artifact(artifact_name, path, expected)
        if mismatches:
            failures.extend(
                f"qualified_geometry_mismatch artifact={artifact_name} {mismatch}"
                for mismatch in mismatches
            )
        else:
            digest = expected["fingerprint"]
            assert isinstance(digest, dict)
            print(
                f"qualified_geometry=pass artifact={artifact_name} "
                f"sha256={digest['sha256']}"
            )
    if failures:
        raise QualificationError("\n".join(failures))


def compare_one(
    root: Path,
    manifest_path: Path,
    artifact_name: str,
    stl_path: Path,
) -> None:
    manifest = _load_json(manifest_path)
    _, artifacts = _validate_manifest_contract(root, manifest)
    _require_physical_acceptance(manifest)
    if artifact_name not in artifacts:
        raise QualificationError(f"unknown qualified artifact: {artifact_name}")
    _, expected = _artifact_expected(artifact_name, artifacts[artifact_name])
    mismatches = compare_artifact(artifact_name, stl_path.resolve(), expected)
    if mismatches:
        raise QualificationError(
            "\n".join(
                f"qualified_geometry_mismatch artifact={artifact_name} {mismatch}"
                for mismatch in mismatches
            )
        )
    print(f"qualified_geometry=pass artifact={artifact_name} path={stl_path}")


def candidate_manifest(
    root: Path,
    manifest_path: Path,
    *,
    acceptance_ref: str,
    accepted_source_revision: str,
    characterized_source_revision: str,
    accepted_on: str,
    confirmed: bool,
) -> dict[str, object]:
    if not confirmed:
        raise QualificationError(
            "recording geometry requires --confirm-physical-acceptance"
        )
    for field_name, value in (
        ("acceptance_ref", acceptance_ref),
        ("accepted_source_revision", accepted_source_revision),
        ("characterized_source_revision", characterized_source_revision),
        ("accepted_on", accepted_on),
    ):
        if not value.strip():
            raise QualificationError(f"{field_name} must be non-empty")
    for field_name, revision in (
        ("accepted_source_revision", accepted_source_revision),
        ("characterized_source_revision", characterized_source_revision),
    ):
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise QualificationError(
                f"{field_name} must be a full lowercase Git SHA"
            )
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", accepted_on):
        raise QualificationError("accepted_on must use YYYY-MM-DD")

    manifest = _load_json(manifest_path)
    _, artifacts = _validate_manifest_contract(root, manifest)
    candidate = deepcopy(manifest)
    qualification = candidate.get("qualification")
    if not isinstance(qualification, dict):
        raise QualificationError("qualification must be an object")
    qualification.update(
        {
            "status": "physically_accepted",
            "acceptance_ref": acceptance_ref,
            "accepted_source_revision": accepted_source_revision,
            "characterized_source_revision": characterized_source_revision,
            "accepted_on": accepted_on,
        }
    )

    candidate_artifacts = candidate["artifacts"]
    assert isinstance(candidate_artifacts, dict)
    for artifact_name, artifact in artifacts.items():
        path_text, _ = _artifact_expected(artifact_name, artifact)
        path = _project_path(root, path_text, f"artifacts.{artifact_name}.path")
        candidate_artifact = candidate_artifacts[artifact_name]
        assert isinstance(candidate_artifact, dict)
        candidate_artifact["expected"] = describe_mesh(path)
    return candidate


def _resolve(root: Path, path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--manifest", type=Path, required=True)
    check_parser.add_argument("--openscad", default="openscad")

    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("--manifest", type=Path, required=True)
    compare_parser.add_argument("--artifact", required=True)
    compare_parser.add_argument("--stl", type=Path, required=True)

    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--manifest", type=Path, required=True)
    record_parser.add_argument("--acceptance-ref", required=True)
    record_parser.add_argument("--accepted-source-revision", required=True)
    record_parser.add_argument("--characterized-source-revision", required=True)
    record_parser.add_argument("--accepted-on", required=True)
    record_parser.add_argument(
        "--confirm-physical-acceptance", action="store_true"
    )
    record_parser.add_argument(
        "--write",
        action="store_true",
        help="replace the manifest; otherwise print a review candidate",
    )

    args = parser.parse_args()
    root = args.root.resolve()

    try:
        if args.command == "check":
            check_manifest(
                root,
                _resolve(root, args.manifest),
                openscad=args.openscad,
            )
        elif args.command == "compare":
            compare_one(
                root,
                _resolve(root, args.manifest),
                args.artifact,
                _resolve(root, args.stl),
            )
        else:
            manifest_path = _resolve(root, args.manifest)
            candidate = candidate_manifest(
                root,
                manifest_path,
                acceptance_ref=args.acceptance_ref,
                accepted_source_revision=args.accepted_source_revision,
                characterized_source_revision=args.characterized_source_revision,
                accepted_on=args.accepted_on,
                confirmed=args.confirm_physical_acceptance,
            )
            rendered = json.dumps(candidate, indent=2, sort_keys=True) + "\n"
            if args.write:
                manifest_path.write_text(rendered, encoding="utf-8")
                print(f"qualified_geometry_recorded={manifest_path}")
            else:
                print(rendered, end="")
    except (OSError, QualificationError, StlError) as exc:
        raise SystemExit(f"qualification_error: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
