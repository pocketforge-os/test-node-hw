#!/usr/bin/env python3
"""Regression tests for draft-only platform fixture dependency intake."""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

import fixture_dependency_intake as intake
import holder_profiles
import qualification_ci


ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = (
    ROOT
    / "profiles/fixture-locks/trimui-smart-pro-family-v1.json"
)
WORKFLOW_PATH = (
    ROOT.parent.parent
    / ".github/workflows/fixture-dependency-intake.yml"
)
LINT_WORKFLOW_PATH = (
    ROOT.parent.parent
    / ".github/workflows/openscad-lint.yml"
)


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FixtureDependencyIntakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(
            prefix="pf-fixture-intake-test-"
        )
        self.addCleanup(self.temp.cleanup)
        self.temp_root = Path(self.temp.name)
        self.root = self.temp_root / "dut-cradle-v1"
        shutil.copytree(ROOT, self.root)
        self.lock = holder_profiles.load_json(LOCK_PATH)
        self.accepted_hashes = self.accepted_file_hashes()

    def accepted_file_hashes(self) -> dict[str, str]:
        paths = (
            "profiles/trimui-smart-pro-family.json",
            "profiles/fixture-locks/trimui-smart-pro-family-v1.json",
            "qualification/trimui-smart-pro-family-v1.json",
        )
        return {relative: sha256(self.root / relative) for relative in paths}

    def snapshot_document(
        self,
        *,
        interface: dict | None = None,
        revision: str | None = None,
        raw_suffix: str = "",
    ) -> dict:
        interface = copy.deepcopy(interface or self.lock["interface"])
        contracts = copy.deepcopy(self.lock["source"]["contracts"])
        for index, contract in enumerate(contracts):
            contract["resolved_interface_sha256"] = interface["sha256"]
            if raw_suffix:
                contract["raw_sha256"] = hashlib.sha256(
                    f"{raw_suffix}-{index}".encode()
                ).hexdigest()
        return {
            "schema": intake.SNAPSHOT_SCHEMA,
            "canonicalization": intake.CANONICALIZATION,
            "source": {
                "repository": intake.SOURCE_REPOSITORY,
                "revision": revision or self.lock["source"]["revision"],
            },
            "contract_schema": {
                "path": intake.CONTRACT_SCHEMA_PATH,
                "raw_sha256": "1" * 64,
            },
            "contracts": contracts,
            "interfaces": [interface],
        }

    def changed_interface(self, delta: Decimal = Decimal("0.01")) -> dict:
        interface = copy.deepcopy(self.lock["interface"])
        interface["interface_revision"] = 2
        interface["fixture_interface"]["contact_regions"][0]["shape"][
            "max_mm"
        ] += delta
        interface["sha256"] = intake._interface_hash(interface)
        return interface

    def write_snapshot(self, document: dict, name: str = "snapshot.json") -> Path:
        path = self.temp_root / name
        path.write_bytes(intake._canonical_bytes(document))
        return path

    def load_changed_snapshot(self) -> intake.Snapshot:
        document = self.snapshot_document(
            interface=self.changed_interface(),
            revision="b" * 40,
            raw_suffix="fit-v2",
        )
        return intake.load_snapshot(self.write_snapshot(document))

    def test_current_and_raw_only_upstream_changes_are_exact_noops(self) -> None:
        current = intake.load_snapshot(
            self.write_snapshot(self.snapshot_document(), "current.json")
        )
        plan, updates = intake.plan_updates(self.root, current)
        self.assertEqual("no_change", plan["status"])
        self.assertEqual([], plan["write_paths"])
        self.assertEqual([], updates)

        raw_only = self.snapshot_document(
            revision="a" * 40,
            raw_suffix="evidence-only",
        )
        raw_plan, raw_updates = intake.plan_updates(
            self.root,
            intake.load_snapshot(self.write_snapshot(raw_only, "raw.json")),
        )
        self.assertEqual("no_change", raw_plan["status"])
        self.assertEqual([], raw_updates)
        self.assertEqual(self.accepted_hashes, self.accepted_file_hashes())
        self.assertFalse((self.root / intake.RECEIPT_DIRECTORY).exists())

    def test_unqualified_profile_stays_in_the_manual_lane(self) -> None:
        current = intake.load_snapshot(
            self.write_snapshot(self.snapshot_document(), "current.json")
        )
        plan, updates = intake.plan_updates(self.root, current)
        profiles = {
            profile["profile_id"]: profile for profile in plan["profiles"]
        }

        self.assertEqual([], updates)
        self.assertEqual(
            "unqualified_manual", profiles["trimui-brick"]["status"]
        )
        self.assertIsNone(
            profiles["trimui-brick"]["resolved_interface_sha256"]
        )
        self.assertEqual([], plan["write_paths"])
        self.assertFalse((self.root / intake.RECEIPT_DIRECTORY).exists())

    def test_fit_change_stages_only_new_candidate_and_is_idempotent(self) -> None:
        snapshot = self.load_changed_snapshot()
        plan, updates = intake.plan_updates(self.root, snapshot)
        self.assertEqual("candidate_updates", plan["status"])
        self.assertEqual(1, len(updates))
        self.assertEqual(2, len(plan["write_paths"]))

        staged = intake.stage_updates(self.root, snapshot)
        self.assertEqual(plan, staged)
        candidates = intake.discover_candidates(self.root)
        self.assertEqual(1, len(candidates))
        candidate = next(iter(candidates.values()))
        self.assertEqual(
            intake.AWAITING_HOLDER_DESIGN,
            candidate.receipt["state"],
        )
        self.assertEqual(
            self.changed_interface()["sha256"],
            candidate.lock["interface"]["sha256"],
        )
        first_hashes = {
            candidate.lock_relative: sha256(self.root / candidate.lock_relative),
            candidate.receipt_relative: sha256(
                self.root / candidate.receipt_relative
            ),
        }

        repeated = intake.stage_updates(self.root, snapshot)
        self.assertEqual([], repeated["write_paths"])
        self.assertEqual(
            first_hashes,
            {
                relative: sha256(self.root / relative)
                for relative in first_hashes
            },
        )
        self.assertEqual(self.accepted_hashes, self.accepted_file_hashes())

    def test_alias_divergence_missing_devices_and_unsafe_paths_fail(self) -> None:
        changed = self.snapshot_document(
            interface=self.changed_interface(),
            revision="b" * 40,
        )
        second = copy.deepcopy(changed["interfaces"][0])
        second["interface_revision"] = 3
        second["fixture_interface"]["contact_regions"][0]["shape"][
            "max_mm"
        ] += Decimal("0.01")
        second["sha256"] = intake._interface_hash(second)
        changed["interfaces"] = sorted(
            [changed["interfaces"][0], second],
            key=lambda item: item["sha256"],
        )
        changed["contracts"][1]["resolved_interface_sha256"] = second["sha256"]
        divergent = intake.load_snapshot(
            self.write_snapshot(changed, "divergent.json")
        )
        with self.assertRaisesRegex(intake.IntakeError, "mixed interfaces"):
            intake.plan_updates(self.root, divergent)

        missing = self.snapshot_document()
        missing["contracts"].pop()
        missing_snapshot = intake.load_snapshot(
            self.write_snapshot(missing, "missing.json")
        )
        with self.assertRaisesRegex(intake.IntakeError, "missing subscribed"):
            intake.plan_updates(self.root, missing_snapshot)

        unsafe = self.snapshot_document()
        unsafe["contracts"][0]["path"] = "../fixture-contract.json"
        with self.assertRaisesRegex(intake.IntakeError, "must be"):
            intake.load_snapshot(self.write_snapshot(unsafe, "unsafe.json"))

    def test_newer_upstream_interface_gets_a_distinct_refresh_identity(
        self,
    ) -> None:
        first_snapshot = self.load_changed_snapshot()
        _, first_updates = intake.plan_updates(self.root, first_snapshot)

        newer_root = self.temp_root / "newer-cradle"
        shutil.copytree(ROOT, newer_root)
        newer_interface = self.changed_interface(Decimal("0.02"))
        newer_interface["interface_revision"] = 3
        newer_interface["sha256"] = intake._interface_hash(newer_interface)
        newer_document = self.snapshot_document(
            interface=newer_interface,
            revision="c" * 40,
            raw_suffix="fit-v3",
        )
        newer_snapshot = intake.load_snapshot(
            self.write_snapshot(newer_document, "newer.json")
        )
        _, newer_updates = intake.plan_updates(newer_root, newer_snapshot)

        self.assertNotEqual(
            first_updates[0].receipt_id,
            newer_updates[0].receipt_id,
        )
        self.assertNotEqual(
            first_updates[0].lock_relative,
            newer_updates[0].lock_relative,
        )
        intake.stage_updates(newer_root, newer_snapshot)
        self.assertEqual(1, len(intake.discover_candidates(newer_root)))

    def test_snapshot_rejects_duplicate_noncanonical_and_unknown_data(self) -> None:
        duplicate = self.temp_root / "duplicate.json"
        duplicate.write_text(
            '{"schema":"one","schema":"two"}\n',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(intake.IntakeError, "duplicate"):
            intake.load_snapshot(duplicate)

        pretty = self.temp_root / "pretty.json"
        plain = json.loads(
            intake._canonical_bytes(self.snapshot_document()).decode()
        )
        pretty.write_text(json.dumps(plain, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(intake.IntakeError, "not canonical"):
            intake.load_snapshot(pretty)

        unknown = self.snapshot_document()
        unknown["surprise"] = True
        with self.assertRaisesRegex(intake.IntakeError, "unknown field"):
            intake.load_snapshot(self.write_snapshot(unknown, "unknown.json"))

    def test_collision_and_unreferenced_candidate_fail_closed(self) -> None:
        snapshot = self.load_changed_snapshot()
        _, updates = intake.plan_updates(self.root, snapshot)
        update = updates[0]
        collision = self.root / update.lock_relative
        collision.parent.mkdir(parents=True)
        collision.write_bytes(b"different candidate bytes")
        with self.assertRaises(intake.IntakeError):
            intake.stage_updates(self.root, snapshot)
        self.assertFalse((self.root / update.receipt_relative).exists())
        self.assertEqual(self.accepted_hashes, self.accepted_file_hashes())

        collision.write_bytes(update.lock_bytes)
        with self.assertRaisesRegex(intake.IntakeError, "unreferenced"):
            intake.discover_candidates(self.root)

    def test_atomic_create_does_not_replace_or_leave_a_temporary_file(self) -> None:
        directory = self.temp_root / "atomic"
        directory.mkdir()
        output = directory / "candidate.json"
        output.write_bytes(b"known-good")
        with self.assertRaisesRegex(intake.IntakeError, "replace"):
            intake._atomic_write_new(output, b"new")
        self.assertEqual(b"known-good", output.read_bytes())

        output.unlink()
        with mock.patch.object(
            intake.os,
            "link",
            side_effect=OSError("injected link failure"),
        ):
            with self.assertRaisesRegex(OSError, "injected link"):
                intake._atomic_write_new(output, b"candidate")
        self.assertFalse(output.exists())
        self.assertEqual([], list(directory.glob(".candidate.json.*")))

    def test_multiple_profiles_are_planned_independently(self) -> None:
        snapshot_document = self.snapshot_document(
            interface=self.changed_interface(),
            revision="b" * 40,
        )
        other_contract = copy.deepcopy(snapshot_document["contracts"][0])
        other_contract["device_slug"] = "other-device"
        other_contract["path"] = (
            "device-models/other-device/fixture-contract.json"
        )
        snapshot_document["contracts"].append(other_contract)
        snapshot_document["contracts"].sort(
            key=lambda item: item["device_slug"]
        )
        snapshot = intake.load_snapshot(
            self.write_snapshot(snapshot_document, "multiple.json")
        )
        registry = qualification_ci.discover_registry(self.root)
        first = registry["trimui-smart-pro-family"]
        second = dataclasses.replace(
            first,
            profile_id="other-family",
            relative_path="profiles/other-family.json",
            device_slugs=("other-device",),
        )
        with mock.patch.object(
            intake.qualification_ci,
            "discover_registry",
            return_value={
                first.profile_id: first,
                second.profile_id: second,
            },
        ):
            plan, updates = intake.plan_updates(self.root, snapshot)
        self.assertEqual("candidate_updates", plan["status"])
        self.assertEqual(
            ["other-family", "trimui-smart-pro-family"],
            [update.profile_id for update in updates],
        )
        self.assertEqual(4, len(plan["write_paths"]))

    def platform_repository(
        self,
        interface: dict,
    ) -> tuple[Path, dict]:
        platform = self.temp_root / "platform"
        full_path = (
            platform
            / "device-models/trimui-smart-pro/fixture-contract.json"
        )
        alias_path = (
            platform
            / "device-models/trimui-smart-pro-s/fixture-contract.json"
        )
        schema_path = platform / intake.CONTRACT_SCHEMA_PATH
        full_path.parent.mkdir(parents=True)
        alias_path.parent.mkdir(parents=True)
        schema_path.parent.mkdir(parents=True)
        full = {
            "kind": "fixture_interface",
            "device": {"slug": "trimui-smart-pro"},
            "schema_version": interface["schema_version"],
            "interface_revision": interface["interface_revision"],
            "fixture_interface_sha256": interface["sha256"],
            "coordinate_system": interface["coordinate_system"],
            "fixture_interface": interface["fixture_interface"],
        }
        alias = {
            "kind": "shared_chassis_alias",
            "device": {"slug": "trimui-smart-pro-s"},
            "expected_fixture_interface_sha256": interface["sha256"],
        }
        full_path.write_bytes(intake._canonical_bytes(full))
        alias_path.write_bytes(intake._canonical_bytes(alias))
        schema_path.write_bytes(b"{\"title\":\"test schema\"}\n")
        git(platform, "init", "--initial-branch=main")
        git(platform, "config", "user.name", "Fixture Intake Test")
        git(platform, "config", "user.email", "fixture@example.invalid")
        git(platform, "add", ".")
        git(platform, "commit", "-m", "fixture v2")
        revision = git(platform, "rev-parse", "HEAD")
        document = self.snapshot_document(
            interface=interface,
            revision=revision,
        )
        document["contract_schema"]["raw_sha256"] = sha256(schema_path)
        for contract in document["contracts"]:
            source = platform / contract["path"]
            contract["raw_sha256"] = sha256(source)
        return platform, document

    def test_candidate_verifies_against_exact_platform_source(self) -> None:
        platform, document = self.platform_repository(
            self.changed_interface()
        )
        snapshot = intake.load_snapshot(
            self.write_snapshot(document, "source.json")
        )
        intake.stage_updates(self.root, snapshot)
        candidate = next(iter(intake.discover_candidates(self.root).values()))
        verified = intake.verify_candidate_source(
            self.root,
            self.root / candidate.receipt_relative,
            platform,
        )
        self.assertEqual(candidate.receipt_id, verified.receipt_id)

        stale = self.temp_root / "stale-platform"
        stale.mkdir()
        git(stale, "init", "--initial-branch=main")
        git(stale, "config", "user.name", "Fixture Intake Test")
        git(stale, "config", "user.email", "fixture@example.invalid")
        (stale / "README").write_text("unrelated\n", encoding="utf-8")
        git(stale, "add", ".")
        git(stale, "commit", "-m", "unrelated")
        with self.assertRaisesRegex(intake.IntakeError, "does not contain"):
            intake.verify_candidate_source(
                self.root,
                self.root / candidate.receipt_relative,
                stale,
            )

    def test_intake_workflow_is_trusted_draft_only_and_race_safe(self) -> None:
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        trigger = text.split("permissions:", 1)[0]
        self.assertIn("schedule:", trigger)
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("pull_request:", trigger)
        self.assertIn("contents: read", text)
        self.assertIn("id-token: write", text)
        self.assertIn("pf-secret get", text)
        self.assertIn("--force-with-lease", text)
        self.assertIn("--draft", text)
        self.assertIn("upstream platform main advanced", text)
        self.assertIn("source test-node-hw main advanced", text)
        self.assertIn("unexpected file on remote automation branch", text)
        self.assertIn("became non-draft before push", text)
        self.assertNotIn("gh pr merge", text)

    def test_zero_candidate_matrix_is_an_explicit_successful_noop(self) -> None:
        text = LINT_WORKFLOW_PATH.read_text(encoding="utf-8")
        output = (
            "fixture_candidate_count: "
            "${{ steps.plan.outputs.fixture_candidate_count }}"
        )
        guard = (
            "if: ${{ needs.qualification_plan.outputs."
            "fixture_candidate_count != '0' }}"
        )
        self.assertIn(output, text)
        self.assertIn("jq -r '.include | length'", text)
        self.assertIn(
            'echo "fixture_candidate_count=${fixture_candidate_count}"',
            text,
        )
        job = text.split("\n  fixture_candidate:\n", 1)[1].split(
            "\n  qualification:\n",
            1,
        )[0]
        self.assertIn(guard, job)
        self.assertLess(job.index(guard), job.index("strategy:"))
        self.assertIn(
            '"${FIXTURE_CANDIDATE_RESULT}" == "skipped"',
            text,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
