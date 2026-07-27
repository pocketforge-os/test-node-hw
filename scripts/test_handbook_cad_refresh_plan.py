#!/usr/bin/env python3
"""Regression tests for artifact-qualified handbook CAD refresh planning."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import handbook_cad_refresh_plan as planner


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github/workflows/handbook-cad-refresh.yml"
SOURCE_SHA = "a" * 40
NEWER_SHA = "b" * 40


def workflow_run_payload(
    *,
    conclusion: str = "success",
    branch: str = "main",
    event: str = "push",
    sha: str = SOURCE_SHA,
) -> dict:
    return {
        "action": "completed",
        "repository": {"full_name": planner.SOURCE_REPOSITORY},
        "workflow_run": {
            "name": planner.WORKFLOW_NAME,
            "path": planner.WORKFLOW_PATH,
            "event": event,
            "conclusion": conclusion,
            "head_branch": branch,
            "head_sha": sha,
            "head_repository": {
                "full_name": planner.SOURCE_REPOSITORY,
            },
        },
    }


def plan(payload: dict, **overrides: str) -> dict:
    arguments = {
        "event_name": "workflow_run",
        "payload": payload,
        "repository": planner.SOURCE_REPOSITORY,
        "ref": planner.MAIN_REF,
        "sha": NEWER_SHA,
    }
    arguments.update(overrides)
    return planner.plan_event(**arguments)


class HandbookCadRefreshPlanTests(unittest.TestCase):
    def test_successful_exact_main_push_is_the_only_automatic_candidate(
        self,
    ) -> None:
        result = plan(workflow_run_payload())
        self.assertTrue(result["authorized"])
        self.assertEqual("successful_main_artifact_push", result["reason"])
        self.assertEqual(SOURCE_SHA, result["source"]["revision"])
        self.assertEqual(result, planner.validate_plan(result))

    def test_failure_cancellation_and_skip_are_rejected(self) -> None:
        for conclusion in (
            "failure",
            "cancelled",
            "skipped",
            "timed_out",
            "neutral",
            None,
        ):
            with self.subTest(conclusion=conclusion):
                result = plan(
                    workflow_run_payload(conclusion=conclusion)
                )
                self.assertFalse(result["authorized"])
                self.assertEqual("unsuccessful_run", result["reason"])
                self.assertIsNone(result["source"])

    def test_branch_pull_request_and_wrong_workflow_are_rejected(self) -> None:
        branch = plan(workflow_run_payload(branch="feature/cad"))
        self.assertEqual("non_main_branch", branch["reason"])

        pull_request = plan(workflow_run_payload(event="pull_request"))
        self.assertEqual("non_push_run", pull_request["reason"])

        wrong_name_payload = workflow_run_payload()
        wrong_name_payload["workflow_run"]["name"] = "OpenSCAD lint"
        self.assertEqual(
            "wrong_workflow",
            plan(wrong_name_payload)["reason"],
        )

        wrong_path_payload = workflow_run_payload()
        wrong_path_payload["workflow_run"]["path"] = ".github/workflows/fake.yml"
        self.assertEqual(
            "wrong_workflow_path",
            plan(wrong_path_payload)["reason"],
        )

    def test_repository_action_sha_and_payload_guards(self) -> None:
        wrong_outer = workflow_run_payload()
        wrong_outer["repository"]["full_name"] = "other/repository"
        self.assertEqual("wrong_repository", plan(wrong_outer)["reason"])

        wrong_head = workflow_run_payload()
        wrong_head["workflow_run"]["head_repository"]["full_name"] = (
            "other/repository"
        )
        self.assertEqual(
            "wrong_head_repository",
            plan(wrong_head)["reason"],
        )

        requested = workflow_run_payload()
        requested["action"] = "requested"
        self.assertEqual(
            "action_not_completed",
            plan(requested)["reason"],
        )

        bad_sha = workflow_run_payload(sha="short")
        self.assertEqual("invalid_head_sha", plan(bad_sha)["reason"])

        missing = workflow_run_payload()
        del missing["workflow_run"]
        self.assertEqual("malformed_payload", plan(missing)["reason"])

        wrong_context = plan(
            workflow_run_payload(),
            repository="other/repository",
        )
        self.assertEqual("wrong_repository", wrong_context["reason"])

    def test_manual_recovery_must_be_exact_main(self) -> None:
        accepted = plan(
            {},
            event_name="workflow_dispatch",
            ref=planner.MAIN_REF,
            sha=SOURCE_SHA,
        )
        self.assertTrue(accepted["authorized"])
        self.assertEqual("manual_exact_main_candidate", accepted["reason"])

        branch = plan(
            {},
            event_name="workflow_dispatch",
            ref="refs/heads/feature",
            sha=SOURCE_SHA,
        )
        self.assertEqual("manual_not_main", branch["reason"])

        bad_sha = plan(
            {},
            event_name="workflow_dispatch",
            ref=planner.MAIN_REF,
            sha="not-a-commit",
        )
        self.assertEqual("invalid_manual_sha", bad_sha["reason"])

    def test_current_main_authorization_closes_late_completion_race(self) -> None:
        accepted = plan(workflow_run_payload())
        current = planner.authorize_current(accepted, SOURCE_SHA)
        self.assertTrue(current["authorized"])
        self.assertEqual("exact_current_main", current["reason"])

        stale = planner.authorize_current(accepted, NEWER_SHA)
        self.assertFalse(stale["authorized"])
        self.assertEqual("stale_source", stale["reason"])
        self.assertEqual(SOURCE_SHA, stale["source"]["revision"])
        self.assertEqual(NEWER_SHA, stale["current_main_revision"])

        failed = plan(workflow_run_payload(conclusion="failure"))
        rejected = planner.authorize_current(failed, SOURCE_SHA)
        self.assertFalse(rejected["authorized"])
        self.assertEqual("event_rejected", rejected["reason"])
        self.assertIsNone(rejected["source"])

    def test_failed_mechanical_run_and_older_success_cannot_advance(
        self,
    ) -> None:
        failed = plan(
            workflow_run_payload(
                conclusion="failure",
                sha=NEWER_SHA,
            )
        )
        failed_current = planner.authorize_current(failed, NEWER_SHA)
        self.assertFalse(failed_current["authorized"])
        self.assertEqual("event_rejected", failed_current["reason"])

        older_success = plan(workflow_run_payload(sha=SOURCE_SHA))
        late = planner.authorize_current(older_success, NEWER_SHA)
        self.assertFalse(late["authorized"])
        self.assertEqual("stale_source", late["reason"])

    def test_cli_malformed_payload_is_a_canonical_rejection(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pf-handbook-refresh-plan-"
        ) as temporary:
            root = Path(temporary)
            event = root / "event.json"
            output = root / "plan.json"
            event.write_text('{"workflow_run":', encoding="utf-8")
            status = planner.main(
                [
                    "plan",
                    "--event-name",
                    "workflow_run",
                    "--event-path",
                    str(event),
                    "--repository",
                    planner.SOURCE_REPOSITORY,
                    "--ref",
                    planner.MAIN_REF,
                    "--sha",
                    SOURCE_SHA,
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, status)
            document = planner.load_json(output)
            self.assertFalse(document["authorized"])
            self.assertEqual("malformed_payload", document["reason"])
            self.assertEqual(
                planner.canonical_bytes(document),
                output.read_bytes(),
            )

    def test_plan_validation_rejects_tampering(self) -> None:
        accepted = plan(workflow_run_payload())
        unknown = copy.deepcopy(accepted)
        unknown["surprise"] = True
        with self.assertRaisesRegex(planner.RefreshPlanError, "unknown field"):
            planner.validate_plan(unknown)

        rejected_with_source = plan(
            workflow_run_payload(conclusion="failure")
        )
        rejected_with_source["source"] = {
            "repository": planner.SOURCE_REPOSITORY,
            "revision": SOURCE_SHA,
        }
        with self.assertRaisesRegex(planner.RefreshPlanError, "must be null"):
            planner.validate_plan(rejected_with_source)

    def test_workflow_credentials_and_mutation_are_authorization_gated(
        self,
    ) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        trigger = text.split("permissions:", 1)[0]
        self.assertIn("workflow_run:", trigger)
        self.assertIn('workflows: ["OpenSCAD artifacts"]', trigger)
        self.assertIn("types: [completed]", trigger)
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("authorize-current", text)
        self.assertIn("steps.current.outputs.authorized == 'true'", text)
        self.assertGreaterEqual(
            text.count("steps.current.outputs.authorized == 'true'"),
            4,
        )
        self.assertIn("pf-secret get", text)
        self.assertIn("--force-with-lease", text)
        self.assertIn("cad/test-node-hw", text)
        self.assertNotIn("gh pr merge", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
