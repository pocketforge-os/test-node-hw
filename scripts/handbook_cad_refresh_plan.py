#!/usr/bin/env python3
"""Authorize handbook CAD refreshes from exact successful artifact builds."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence


PLAN_SCHEMA = "pocketforge-handbook-cad-refresh-plan-v1"
AUTHORIZATION_SCHEMA = "pocketforge-handbook-cad-refresh-authorization-v1"
SOURCE_REPOSITORY = "pocketforge-os/test-node-hw"
WORKFLOW_NAME = "OpenSCAD artifacts"
WORKFLOW_PATH = ".github/workflows/openscad-artifacts.yml"
MAIN_REF = "refs/heads/main"
MAIN_BRANCH = "main"
GIT_REV_RE = re.compile(r"^[0-9a-f]{40}$")


class RefreshPlanError(ValueError):
    """A malformed planner input or output."""


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise RefreshPlanError(f"{path}: must be an object")
    return value


def _keys(
    value: Mapping[str, Any],
    path: str,
    expected: set[str],
) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise RefreshPlanError(
            f"{path}: missing required field(s): {', '.join(missing)}"
        )
    if extra:
        raise RefreshPlanError(
            f"{path}: unknown field(s): {', '.join(extra)}"
        )


def _reject_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RefreshPlanError(f"JSON contains duplicate object key {key!r}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise RefreshPlanError(f"JSON contains non-finite number {token}")


def load_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_constant,
            object_pairs_hook=_reject_duplicate_keys,
        )
    except OSError as exc:
        raise RefreshPlanError(f"{path}: cannot read: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RefreshPlanError(
            f"{path}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc
    return _object(value, str(path))


def canonical_bytes(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise RefreshPlanError(f"cannot canonicalize plan: {exc}") from exc
    return (encoded + "\n").encode("utf-8")


def _repository_name(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    name = value.get("full_name")
    return name if isinstance(name, str) and name else None


def _rejected(
    event_name: str,
    reason: str,
    detail: str,
) -> dict[str, Any]:
    return {
        "schema": PLAN_SCHEMA,
        "authorized": False,
        "reason": reason,
        "detail": detail,
        "trigger": {"event_name": event_name},
        "source": None,
    }


def _accepted(
    event_name: str,
    reason: str,
    revision: str,
) -> dict[str, Any]:
    return {
        "schema": PLAN_SCHEMA,
        "authorized": True,
        "reason": reason,
        "detail": "exact source candidate selected",
        "trigger": {"event_name": event_name},
        "source": {
            "repository": SOURCE_REPOSITORY,
            "revision": revision,
        },
    }


def plan_event(
    *,
    event_name: str,
    payload: Mapping[str, Any],
    repository: str,
    ref: str,
    sha: str,
) -> dict[str, Any]:
    """Interpret one GitHub event without contacting GitHub or mutating state."""

    if repository != SOURCE_REPOSITORY:
        return _rejected(
            event_name,
            "wrong_repository",
            f"expected {SOURCE_REPOSITORY}, got {repository!r}",
        )
    if event_name == "workflow_dispatch":
        if ref != MAIN_REF:
            return _rejected(
                event_name,
                "manual_not_main",
                f"manual recovery requires {MAIN_REF}, got {ref!r}",
            )
        if not GIT_REV_RE.fullmatch(sha):
            return _rejected(
                event_name,
                "invalid_manual_sha",
                "manual recovery source is not an exact 40-hex commit",
            )
        return _accepted(event_name, "manual_exact_main_candidate", sha)

    if event_name != "workflow_run":
        return _rejected(
            event_name,
            "unsupported_event",
            "only workflow_run or workflow_dispatch is supported",
        )
    if payload.get("action") != "completed":
        return _rejected(
            event_name,
            "action_not_completed",
            "workflow_run action must be completed",
        )
    if _repository_name(payload.get("repository")) != SOURCE_REPOSITORY:
        return _rejected(
            event_name,
            "wrong_repository",
            "event repository does not match test-node-hw",
        )
    run_value = payload.get("workflow_run")
    if not isinstance(run_value, dict):
        return _rejected(
            event_name,
            "malformed_payload",
            "workflow_run object is missing",
        )
    run = run_value
    if run.get("name") != WORKFLOW_NAME:
        return _rejected(
            event_name,
            "wrong_workflow",
            f"expected workflow {WORKFLOW_NAME!r}",
        )
    if run.get("path") != WORKFLOW_PATH:
        return _rejected(
            event_name,
            "wrong_workflow_path",
            f"expected workflow path {WORKFLOW_PATH!r}",
        )
    if run.get("event") != "push":
        return _rejected(
            event_name,
            "non_push_run",
            "only artifact runs triggered by push may authorize refresh",
        )
    if run.get("conclusion") != "success":
        return _rejected(
            event_name,
            "unsuccessful_run",
            f"artifact conclusion was {run.get('conclusion')!r}",
        )
    if run.get("head_branch") != MAIN_BRANCH:
        return _rejected(
            event_name,
            "non_main_branch",
            f"artifact branch was {run.get('head_branch')!r}",
        )
    if _repository_name(run.get("head_repository")) != SOURCE_REPOSITORY:
        return _rejected(
            event_name,
            "wrong_head_repository",
            "artifact source repository does not match test-node-hw",
        )
    revision = run.get("head_sha")
    if not isinstance(revision, str) or not GIT_REV_RE.fullmatch(revision):
        return _rejected(
            event_name,
            "invalid_head_sha",
            "artifact source is not an exact 40-hex commit",
        )
    return _accepted(
        event_name,
        "successful_main_artifact_push",
        revision,
    )


def validate_plan(value: Any) -> Mapping[str, Any]:
    plan = _object(value, "plan")
    _keys(
        plan,
        "plan",
        {"schema", "authorized", "reason", "detail", "trigger", "source"},
    )
    if plan["schema"] != PLAN_SCHEMA:
        raise RefreshPlanError(f"plan.schema: must be {PLAN_SCHEMA!r}")
    if not isinstance(plan["authorized"], bool):
        raise RefreshPlanError("plan.authorized: must be a boolean")
    for key in ("reason", "detail"):
        if not isinstance(plan[key], str) or not plan[key]:
            raise RefreshPlanError(f"plan.{key}: must be a non-empty string")
    trigger = _object(plan["trigger"], "plan.trigger")
    _keys(trigger, "plan.trigger", {"event_name"})
    if not isinstance(trigger["event_name"], str) or not trigger["event_name"]:
        raise RefreshPlanError(
            "plan.trigger.event_name: must be a non-empty string"
        )
    if plan["authorized"]:
        source = _object(plan["source"], "plan.source")
        _keys(source, "plan.source", {"repository", "revision"})
        if source["repository"] != SOURCE_REPOSITORY:
            raise RefreshPlanError(
                f"plan.source.repository: must be {SOURCE_REPOSITORY!r}"
            )
        revision = source["revision"]
        if not isinstance(revision, str) or not GIT_REV_RE.fullmatch(revision):
            raise RefreshPlanError(
                "plan.source.revision: must be an exact 40-hex commit"
            )
    elif plan["source"] is not None:
        raise RefreshPlanError("plan.source: must be null when rejected")
    return plan


def authorize_current(
    plan_value: Any,
    current_main_revision: str,
) -> dict[str, Any]:
    plan = validate_plan(plan_value)
    if not GIT_REV_RE.fullmatch(current_main_revision):
        raise RefreshPlanError(
            "current main revision must be an exact 40-hex commit"
        )
    source = plan["source"]
    if not plan["authorized"]:
        return {
            "schema": AUTHORIZATION_SCHEMA,
            "authorized": False,
            "reason": "event_rejected",
            "source": None,
            "current_main_revision": current_main_revision,
        }
    assert isinstance(source, dict)
    if source["revision"] != current_main_revision:
        return {
            "schema": AUTHORIZATION_SCHEMA,
            "authorized": False,
            "reason": "stale_source",
            "source": source,
            "current_main_revision": current_main_revision,
        }
    return {
        "schema": AUTHORIZATION_SCHEMA,
        "authorized": True,
        "reason": "exact_current_main",
        "source": source,
        "current_main_revision": current_main_revision,
    }


def _write_external(
    output: Path | None,
    payload: bytes,
) -> None:
    if output is None:
        sys.stdout.buffer.write(payload)
        return
    repository_root = Path(__file__).resolve().parent.parent
    output = output.expanduser().resolve()
    try:
        output.relative_to(repository_root)
    except ValueError:
        pass
    else:
        raise RefreshPlanError(
            "generated planner output must remain outside the repository"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=output.parent,
            prefix=f".{output.name}.",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--event-name", required=True)
    plan_parser.add_argument("--event-path", type=Path, required=True)
    plan_parser.add_argument("--repository", required=True)
    plan_parser.add_argument("--ref", required=True)
    plan_parser.add_argument("--sha", required=True)
    plan_parser.add_argument("--output", type=Path)

    authorize_parser = subparsers.add_parser("authorize-current")
    authorize_parser.add_argument("--plan", type=Path, required=True)
    authorize_parser.add_argument("--current-main", required=True)
    authorize_parser.add_argument("--output", type=Path)

    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            try:
                payload = load_json(args.event_path)
            except RefreshPlanError as exc:
                payload = {}
                plan = _rejected(
                    args.event_name,
                    "malformed_payload",
                    str(exc),
                )
            else:
                plan = plan_event(
                    event_name=args.event_name,
                    payload=payload,
                    repository=args.repository,
                    ref=args.ref,
                    sha=args.sha,
                )
            validate_plan(plan)
            _write_external(args.output, canonical_bytes(plan))
            if args.output is not None:
                print(
                    "handbook_cad_refresh_plan="
                    f"{'authorized' if plan['authorized'] else 'rejected'} "
                    f"reason={plan['reason']} output={args.output}"
                )
        elif args.command == "authorize-current":
            plan = load_json(args.plan)
            authorization = authorize_current(plan, args.current_main)
            _write_external(
                args.output,
                canonical_bytes(authorization),
            )
            if args.output is not None:
                print(
                    "handbook_cad_refresh_current="
                    f"{'authorized' if authorization['authorized'] else 'rejected'} "
                    f"reason={authorization['reason']} output={args.output}"
                )
        else:  # pragma: no cover
            raise RefreshPlanError(f"unsupported command: {args.command}")
    except (OSError, RefreshPlanError) as exc:
        print(f"handbook_cad_refresh_error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
