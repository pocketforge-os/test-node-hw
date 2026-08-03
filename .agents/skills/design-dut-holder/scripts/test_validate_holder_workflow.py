#!/usr/bin/env python3
"""Regression tests for the repo-owned DUT holder design skill."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import validate_holder_workflow as workflow


REPO_ROOT = Path(__file__).resolve().parents[4]


class HolderSkillValidationTests(unittest.TestCase):
    def test_contract_and_trimui_preflight_are_read_only(self) -> None:
        before = workflow.source_digest(REPO_ROOT)
        result = workflow.validate_repository(
            REPO_ROOT,
            "profiles/trimui-smart-pro-family.json",
            None,
        )
        self.assertEqual(workflow.RESULT_SCHEMA, result["schema"])
        self.assertEqual("pass", result["status"])
        self.assertEqual(
            "trimui-smart-pro-family",
            result["profile"]["profile_id"],
        )
        self.assertEqual(
            ["trimui-smart-pro", "trimui-smart-pro-s"],
            result["profile"]["device_slugs"],
        )
        self.assertEqual(0, result["candidate_count"])
        self.assertEqual(1, result["qualified_profile_count"])
        self.assertEqual(2, result["qualified_device_count"])
        self.assertEqual(
            "print-pack-trimui-smart-pro-family-v2",
            result["release_identity"],
        )
        self.assertFalse(result["source_mutation"])
        self.assertEqual(before, workflow.source_digest(REPO_ROOT))

    def test_contract_rejects_a_missing_decision_state(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pf-holder-skill-contract-"
        ) as temporary:
            root = Path(temporary)
            skill_source = (
                REPO_ROOT / ".agents/skills/design-dut-holder"
            )
            skill_target = (
                root / ".agents/skills/design-dut-holder"
            )
            shutil.copytree(skill_source, skill_target)
            for relative in workflow.REQUIRED_ENTRYPOINTS:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            contract = skill_target / "references/workflow-contract.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "awaiting_holder_design",
                    "removed-holder-state",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                workflow.WorkflowError,
                "state:intake",
            ):
                workflow.validate_contract(root)

    def test_profile_path_cannot_escape_the_profile_registry(self) -> None:
        with self.assertRaisesRegex(
            workflow.WorkflowError,
            "directly under",
        ):
            workflow.resolve_profile(
                REPO_ROOT,
                "../qualification/cad-toolchain.json",
            )

    def test_contract_cli_is_canonical_json(self) -> None:
        script = Path(workflow.__file__).resolve()
        result = subprocess.run(
            [sys.executable, str(script), "contract"],
            check=True,
            capture_output=True,
        )
        document = json.loads(result.stdout)
        self.assertEqual(
            workflow.canonical_bytes(document),
            result.stdout,
        )

    def test_ci_validates_and_propagates_skill_changes(self) -> None:
        lint = (
            REPO_ROOT / ".github/workflows/openscad-lint.yml"
        ).read_text(encoding="utf-8")
        artifacts = (
            REPO_ROOT / ".github/workflows/openscad-artifacts.yml"
        ).read_text(encoding="utf-8")
        path_filter = (
            '- ".agents/skills/design-dut-holder/**"'
        )
        self.assertIn(path_filter, lint)
        self.assertIn(path_filter, artifacts)
        self.assertIn(
            "Test the DUT holder design skill contract",
            lint,
        )
        self.assertIn(
            "validate_holder_workflow.py",
            lint,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
