#!/usr/bin/env python3
"""Validate the holder-design skill and its read-only repository handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


RESULT_SCHEMA = "pocketforge-holder-skill-validation-v1"
SKILL_RELATIVE = Path(".agents/skills/design-dut-holder")
CRADLE_RELATIVE = Path("mechanical/dut-cradle-v1")

REQUIRED_ENTRYPOINTS = (
    CRADLE_RELATIVE / "scripts/fixture_dependency_intake.py",
    CRADLE_RELATIVE / "scripts/holder_profiles.py",
    CRADLE_RELATIVE / "scripts/qualification_ci.py",
    Path("mechanical/device-packs/build_device_pack.py"),
    Path("mechanical/device-packs/release_print_pack.py"),
)

REQUIRED_TEXT = {
    "routing:no-drift": "No fixture-interface drift",
    "routing:existing": "Existing mechanism, new device",
    "routing:changed-fit": "Changed fit for a qualified profile",
    "routing:novel": "Genuinely novel retention",
    "state:intake": "awaiting_holder_design",
    "state:physical": "awaiting_physical_acceptance",
    "state:accepted": "physically_accepted",
    "state:qualified": "physically_qualified",
    "mechanism:existing": "perimeter_j_hook_v1",
    "mechanism:escape": "custom_openscad",
    "boundary:model": "$model-handheld-device",
    "boundary:integration": "integration profile",
    "boundary:generated": "Do not commit routine STL",
    "command:intake": "fixture_dependency_intake.py",
    "command:profiles": "holder_profiles.py",
    "command:qualification": "qualification_ci.py",
    "command:packs": "build_device_pack.py",
    "command:release": "release_print_pack.py",
}


class WorkflowError(ValueError):
    """The skill contract or repository handoff is incomplete or unsafe."""


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        + b"\n"
    )


def load_json(path: Path) -> Any:
    def reject_duplicates(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise WorkflowError(f"{path}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicates,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"cannot read strict JSON {path}: {exc}") from exc


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise WorkflowError(f"{path}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise WorkflowError(f"{path}: unterminated YAML frontmatter") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if not separator or not key or not value.strip():
            raise WorkflowError(f"{path}: invalid frontmatter line {line!r}")
        if key in values:
            raise WorkflowError(f"{path}: duplicate frontmatter key {key!r}")
        values[key] = value.strip()
    if set(values) != {"name", "description"}:
        raise WorkflowError(
            f"{path}: frontmatter keys must be name and description"
        )
    if values["name"] != "design-dut-holder":
        raise WorkflowError(f"{path}: unexpected skill name")
    if len(values["description"]) < 120:
        raise WorkflowError(f"{path}: trigger description is incomplete")
    return values


def validate_openai_yaml(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    expected = (
        '  display_name: "Design DUT Holder"',
        '  short_description: "Design and qualify reproducible DUT holders"',
        '  default_prompt: "Use $design-dut-holder ',
    )
    for fragment in expected:
        if fragment not in text:
            raise WorkflowError(f"{path}: missing {fragment!r}")
    short_match = re.search(
        r'^  short_description: "([^"]+)"$', text, re.MULTILINE
    )
    if short_match is None or not 25 <= len(short_match.group(1)) <= 64:
        raise WorkflowError(f"{path}: short_description must be 25-64 chars")


def validate_contract(repo_root: Path) -> dict[str, Any]:
    skill = repo_root / SKILL_RELATIVE
    expected_files = (
        skill / "SKILL.md",
        skill / "agents/openai.yaml",
        skill / "references/workflow-contract.md",
        skill / "references/mechanism-design.md",
        skill / "scripts/validate_holder_workflow.py",
        skill / "scripts/test_validate_holder_workflow.py",
    )
    missing = [path for path in expected_files if not path.is_file()]
    if missing:
        raise WorkflowError(
            "missing skill resource(s): "
            + ", ".join(str(path.relative_to(repo_root)) for path in missing)
        )
    parse_frontmatter(skill / "SKILL.md")
    validate_openai_yaml(skill / "agents/openai.yaml")

    documents = (
        skill / "SKILL.md",
        skill / "references/workflow-contract.md",
        skill / "references/mechanism-design.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in documents)
    if "TODO" in combined:
        raise WorkflowError("skill contains an unresolved TODO")
    for label, required in REQUIRED_TEXT.items():
        if required not in combined:
            raise WorkflowError(
                f"skill contract is missing {label}: {required!r}"
            )
    for entrypoint in REQUIRED_ENTRYPOINTS:
        if not (repo_root / entrypoint).is_file():
            raise WorkflowError(f"missing repository entrypoint: {entrypoint}")
    readmes = sorted(skill.rglob("README*"))
    if readmes:
        raise WorkflowError("skill must not contain auxiliary README files")
    return {
        "documents": len(documents),
        "entrypoints": len(REQUIRED_ENTRYPOINTS),
        "required_claims": len(REQUIRED_TEXT),
    }


def resolve_profile(repo_root: Path, value: str) -> tuple[Path, str]:
    cradle = (repo_root / CRADLE_RELATIVE).resolve()
    raw = Path(value)
    if raw.is_absolute():
        candidate = raw.resolve()
    elif raw.parts[:2] == ("mechanical", "dut-cradle-v1"):
        candidate = (repo_root / raw).resolve()
    else:
        candidate = (cradle / raw).resolve()
    profile_root = (cradle / "profiles").resolve()
    if candidate.parent != profile_root or candidate.suffix != ".json":
        raise WorkflowError(
            "profile must be one JSON file directly under "
            "mechanical/dut-cradle-v1/profiles"
        )
    if not candidate.is_file():
        raise WorkflowError(f"profile does not exist: {candidate}")
    relative = candidate.relative_to(cradle).as_posix()
    return candidate, relative


def source_digest(repo_root: Path) -> str:
    cradle = repo_root / CRADLE_RELATIVE
    roots = (
        cradle / "profiles",
        cradle / "qualification",
        cradle / "lib",
    )
    paths: list[Path] = []
    for root in roots:
        paths.extend(path for path in root.rglob("*") if path.is_file())
    paths.extend(cradle.glob("*.scad"))
    digest = hashlib.sha256()
    for path in sorted(set(paths)):
        if "build" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(repo_root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def run(repo_root: Path, arguments: list[str]) -> str:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, *arguments],
        cwd=repo_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise WorkflowError(
            f"command failed ({' '.join(arguments)}): {detail}"
        )
    return result.stdout.strip()


def parse_matrix(raw: str, label: str) -> list[dict[str, Any]]:
    try:
        document = json.loads(raw)
        include = document["include"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise WorkflowError(f"{label} did not emit a matrix") from exc
    if not isinstance(include, list):
        raise WorkflowError(f"{label}.include must be an array")
    return include


def validate_repository(
    repo_root: Path,
    profile_value: str,
    platform_root: Path | None,
) -> dict[str, Any]:
    contract = validate_contract(repo_root)
    profile_path, profile_relative = resolve_profile(
        repo_root, profile_value
    )
    profile = load_json(profile_path)
    before = source_digest(repo_root)
    cradle_script = CRADLE_RELATIVE / "scripts"

    run(
        repo_root,
        [
            str(cradle_script / "holder_profiles.py"),
            "validate",
            "--profile",
            profile_relative,
        ],
    )
    run(
        repo_root,
        [
            str(cradle_script / "fixture_dependency_intake.py"),
            "validate-candidates",
        ],
    )
    candidates = parse_matrix(
        run(
            repo_root,
            [
                str(cradle_script / "fixture_dependency_intake.py"),
                "matrix",
            ],
        ),
        "fixture candidates",
    )
    qualified_profiles = parse_matrix(
        run(
            repo_root,
            [
                str(cradle_script / "qualification_ci.py"),
                "matrix",
                "--kind",
                "qualified-profiles",
            ],
        ),
        "qualified profiles",
    )
    qualified_devices = parse_matrix(
        run(
            repo_root,
            [
                str(cradle_script / "qualification_ci.py"),
                "matrix",
                "--kind",
                "qualified-devices",
            ],
        ),
        "qualified devices",
    )
    run(
        repo_root,
        [
            str(cradle_script / "holder_profiles.py"),
            "print-command",
            "--profile",
            profile_relative,
            "--artifact",
            "fit_coupon",
            "--output",
            "/tmp/pocketforge-holder-skill-fit-coupon.stl",
        ],
    )

    platform_verified = False
    if platform_root is not None:
        platform = platform_root.resolve()
        if not (platform / ".git").exists():
            raise WorkflowError(f"platform root is not a checkout: {platform}")
        run(
            repo_root,
            [
                str(cradle_script / "holder_profiles.py"),
                "verify-source",
                "--profile",
                profile_relative,
                "--platform-root",
                str(platform),
            ],
        )
        platform_verified = True

    release_identity = None
    qualification = profile.get("qualification")
    if (
        isinstance(qualification, dict)
        and qualification.get("status") == "physically_qualified"
    ):
        release_identity = run(
            repo_root,
            [
                "mechanical/device-packs/release_print_pack.py",
                "identity",
                "--profile-id",
                str(profile["profile_id"]),
            ],
        )

    after = source_digest(repo_root)
    if before != after:
        raise WorkflowError(
            "repository validation mutated fit-bearing source state"
        )
    device_slugs = profile.get("device_slugs")
    if not isinstance(device_slugs, list):
        raise WorkflowError("validated profile has no device_slugs array")
    return {
        "schema": RESULT_SCHEMA,
        "status": "pass",
        "contract": contract,
        "profile": {
            "path": profile_relative,
            "profile_id": profile["profile_id"],
            "device_slugs": device_slugs,
            "qualification_status": qualification.get("status")
            if isinstance(qualification, dict)
            else None,
        },
        "candidate_count": len(candidates),
        "qualified_profile_count": len(qualified_profiles),
        "qualified_device_count": len(qualified_devices),
        "compiled_artifact": "fit_coupon",
        "platform_verified": platform_verified,
        "release_identity": release_identity,
        "source_mutation": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("contract")
    repository = subparsers.add_parser("repository")
    repository.add_argument(
        "--profile",
        default="profiles/trimui-smart-pro-family.json",
    )
    repository.add_argument("--platform-root", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = (args.repo_root or repo_root_from_script()).resolve()
    try:
        if args.command == "contract":
            result = {
                "schema": RESULT_SCHEMA,
                "status": "pass",
                "contract": validate_contract(repo_root),
            }
        else:
            result = validate_repository(
                repo_root,
                args.profile,
                args.platform_root,
            )
        sys.stdout.buffer.write(canonical_bytes(result))
        return 0
    except (KeyError, OSError, UnicodeError, WorkflowError) as exc:
        print(f"holder_skill_error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
