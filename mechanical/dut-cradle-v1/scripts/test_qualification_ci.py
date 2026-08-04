#!/usr/bin/env python3
"""Regression tests for dynamic holder qualification CI."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import qualification_ci as qualification
from mesh_fingerprint import describe_mesh


ROOT = Path(__file__).resolve().parent.parent
PROFILE = "profiles/trimui-smart-pro-family.json"
LOCK = "profiles/fixture-locks/trimui-smart-pro-family-v1.json"
MANIFEST = "qualification/trimui-smart-pro-family-v1.json"


TETRAHEDRON = """\
solid tetrahedron
  facet normal 0 0 0
    outer loop
      vertex 0 0 0
      vertex 1 0 0
      vertex 0 1 0
    endloop
  endfacet
  facet normal 0 0 0
    outer loop
      vertex 0 0 0
      vertex 0 0 1
      vertex 1 0 0
    endloop
  endfacet
  facet normal 0 0 0
    outer loop
      vertex 0 0 0
      vertex 0 1 0
      vertex 0 0 1
    endloop
  endfacet
  facet normal 0 0 0
    outer loop
      vertex 1 0 0
      vertex 0 0 1
      vertex 0 1 0
    endloop
  endfacet
endsolid tetrahedron
"""


SCALED_TETRAHEDRON = TETRAHEDRON.replace("vertex 1 0 0", "vertex 2 0 0")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def downgrade(profile: dict) -> None:
    record = profile["qualification"]
    record.update(
        {
            "status": "unqualified",
            "acceptance_ref": None,
            "accepted_on": None,
            "accepted_geometry_revision": None,
            "geometry_manifest": None,
            "artifact_names": [],
        }
    )


class QualificationCiTests(unittest.TestCase):
    def clone_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name) / "dut-cradle-v1"
        shutil.copytree(
            ROOT,
            target,
            ignore=shutil.ignore_patterns("build", "__pycache__", "*.pyc"),
        )
        return target

    def accepted_base(self, root: Path) -> dict:
        record = qualification.discover_registry(root)[
            "trimui-smart-pro-family"
        ]
        return {
            "profile_path": record.relative_path,
            "geometry_manifest": record.manifest_path,
            "manifest_sha256": record.manifest_sha256,
            "acceptance_ref": record.qualification["acceptance_ref"],
            "fixture_interface_sha256": record.fixture_sha256,
            "fixture_lock": record.fixture_lock_path,
            "fixture_lock_sha256": record.fixture_lock_sha256,
            "toolchain_lock": record.toolchain_lock_path,
            "toolchain_lock_sha256": record.toolchain_lock_sha256,
        }

    def waiting_change(
        self,
        root: Path,
        *,
        base: dict | None,
        change_id: str = "trimui-retention-update",
        scopes: list[str] | None = None,
    ) -> Path:
        fixture_hash = read_json(root / LOCK)["interface"]["sha256"]
        toolchain_path = root / "qualification/cad-toolchain.json"
        path = root / "qualification/changes" / f"{change_id}.json"
        write_json(
            path,
            {
                "schema": qualification.CHANGE_SCHEMA,
                "change_id": change_id,
                "profile_id": "trimui-smart-pro-family",
                "base": base,
                "intent": {
                    "tracking_ref": "tsp-test",
                    "reason": "Exercise an intentional retention change.",
                    "scopes": scopes or ["j_hook"],
                },
                "transition": {
                    "state": qualification.AWAITING,
                    "candidate_fixture_interface_sha256": fixture_hash,
                    "candidate_fixture_lock": LOCK,
                    "candidate_fixture_lock_sha256": sha256(root / LOCK),
                    "candidate_toolchain_lock": (
                        "qualification/cad-toolchain.json"
                    ),
                    "candidate_toolchain_sha256": sha256(toolchain_path),
                    "physical_acceptance": None,
                },
            },
        )
        return path

    def add_second_qualified_profile(
        self,
        root: Path,
        *,
        device_slug: str = "second-device",
    ) -> None:
        profile = read_json(root / PROFILE)
        lock = read_json(root / LOCK)
        manifest = read_json(root / MANIFEST)

        profile["profile_id"] = "second-family"
        profile["device_slugs"] = [device_slug]
        profile["device_variants"] = [
            {
                "device_slug": device_slug,
                "display_name": "Second Device",
                "production_carrier": {
                    "source": "trimui-smart-pro-cradle.scad",
                    "part": "plate",
                    "parameters": {
                        "DEVICE_LABEL": "Second Device",
                        "SHOW_DEVICE": False,
                        "SHOW_HOOKS": False,
                        "SHOW_LABELS": True,
                    },
                },
            }
        ]
        profile["fixture"]["lock"] = (
            "profiles/fixture-locks/second-family-v1.json"
        )
        profile["qualification"]["acceptance_ref"] = "tsp-second"
        profile["qualification"]["geometry_manifest"] = (
            "qualification/second-family-v1.json"
        )

        contract = copy.deepcopy(lock["source"]["contracts"][0])
        contract["device_slug"] = device_slug
        contract["path"] = (
            f"device-models/{device_slug}/fixture-contract.json"
        )
        lock["source"]["contracts"] = [contract]

        manifest["qualification"]["acceptance_ref"] = "tsp-second"
        manifest["qualification"]["device_ids"] = [device_slug]

        write_json(
            root / "profiles/second-family.json",
            profile,
        )
        write_json(
            root / "profiles/fixture-locks/second-family-v1.json",
            lock,
        )
        write_json(
            root / "qualification/second-family-v1.json",
            manifest,
        )

    def install_fake_metrics(self, root: Path) -> None:
        mesh = root / "fake-tetrahedron.stl"
        mesh.write_text(TETRAHEDRON, encoding="ascii")
        metrics = describe_mesh(mesh)
        mesh.unlink()
        manifest = read_json(root / MANIFEST)
        for artifact in manifest["artifacts"].values():
            artifact["expected"] = copy.deepcopy(metrics)
        write_json(root / MANIFEST, manifest)

    def fake_renderer(self, changed_artifact: str | None = None):
        def render(
            _resolved,
            artifact_name: str,
            output: Path,
            *,
            openscad: str,
        ) -> None:
            self.assertEqual("fake-openscad", openscad)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                (
                    SCALED_TETRAHEDRON
                    if artifact_name == changed_artifact
                    else TETRAHEDRON
                ),
                encoding="ascii",
            )

        return render

    def test_current_registry_and_plan_are_dynamic_and_sorted(self) -> None:
        root = self.clone_root()
        self.add_second_qualified_profile(root)

        profile_matrix = qualification.registry_matrix(
            root,
            "qualified-profiles",
        )
        self.assertEqual(
            ["second-family", "trimui-smart-pro-family"],
            [
                item["profile_id"]
                for item in profile_matrix["include"]
            ],
        )
        device_matrix = qualification.registry_matrix(
            root,
            "qualified-devices",
        )
        self.assertEqual(
            [
                "second-device",
                "trimui-smart-pro",
                "trimui-smart-pro-s",
            ],
            [item["device_slug"] for item in device_matrix["include"]],
        )

        plan = qualification.build_plan(root, root)
        self.assertEqual(
            ["second-family", "trimui-smart-pro-family"],
            [
                item["profile_id"]
                for item in plan["matrix"]["include"]
            ],
        )
        self.assertTrue(
            all(
                item["mode"] == "protect"
                for item in plan["matrix"]["include"]
            )
        )

    def test_duplicate_device_ownership_is_rejected(self) -> None:
        root = self.clone_root()
        self.add_second_qualified_profile(
            root,
            device_slug="trimui-smart-pro",
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "owned by both",
        ):
            qualification.discover_registry(root)

    def test_silent_downgrade_and_golden_rewrite_are_rejected(self) -> None:
        base = self.clone_root()
        head = self.clone_root()

        profile = read_json(head / PROFILE)
        downgrade(profile)
        write_json(head / PROFILE, profile)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "exactly one.*awaiting",
        ):
            qualification.build_plan(head, base)

        head = self.clone_root()
        manifest = read_json(head / MANIFEST)
        manifest["artifacts"]["j_hook"]["expected"]["fingerprint"][
            "sha256"
        ] = "0" * 64
        write_json(head / MANIFEST, manifest)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "accepted manifest is immutable",
        ):
            qualification.build_plan(head, base)

        head = self.clone_root()
        fixture_lock = head / LOCK
        fixture_lock.write_text(
            fixture_lock.read_text(encoding="utf-8") + " \n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "accepted fixture lock is immutable",
        ):
            qualification.build_plan(head, base)

        head = self.clone_root()
        toolchain = head / "qualification/cad-toolchain.json"
        toolchain.write_text(
            toolchain.read_text(encoding="utf-8") + " \n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "accepted toolchain lock is immutable",
        ):
            qualification.build_plan(head, base)

    def test_base_qualified_removal_and_direct_new_qualification_are_rejected(
        self,
    ) -> None:
        base = self.clone_root()
        head = self.clone_root()
        self.add_second_qualified_profile(base)
        self.add_second_qualified_profile(head)
        (head / "profiles/second-family.json").unlink()
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "base-qualified profile cannot be removed",
        ):
            qualification.build_plan(head, base)

        base = self.clone_root()
        head = self.clone_root()
        self.add_second_qualified_profile(head)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "must land unqualified",
        ):
            qualification.build_plan(head, base)

    def test_malformed_and_stale_change_records_fail_closed(self) -> None:
        base = self.clone_root()
        head = self.clone_root()
        accepted = self.accepted_base(base)
        profile = read_json(head / PROFILE)
        downgrade(profile)
        write_json(head / PROFILE, profile)
        change_path = self.waiting_change(
            head,
            base=accepted,
            scopes=["j_hook", "carrier_body"],
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "must be sorted",
        ):
            qualification.build_plan(head, base)

        change = read_json(change_path)
        change["intent"]["scopes"] = ["carrier_body", "j_hook"]
        change["transition"]["candidate_fixture_interface_sha256"] = "0" * 64
        write_json(change_path, change)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "candidate fixture hash does not match",
        ):
            qualification.build_plan(head, base)

        change["transition"]["candidate_fixture_interface_sha256"] = (
            read_json(head / LOCK)["interface"]["sha256"]
        )
        change["transition"]["candidate_fixture_lock_sha256"] = "0" * 64
        write_json(change_path, change)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "candidate fixture-lock hash mismatch",
        ):
            qualification.build_plan(head, base)

        change["transition"]["candidate_fixture_lock_sha256"] = sha256(
            head / LOCK
        )
        change["transition"]["candidate_toolchain_sha256"] = "0" * 64
        write_json(change_path, change)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "candidate toolchain hash mismatch",
        ):
            qualification.build_plan(head, base)

        head = self.clone_root()
        accepted = self.accepted_base(head)
        change_path = self.waiting_change(head, base=accepted)
        change = read_json(change_path)
        change["transition"].update(
            {
                "state": qualification.ACCEPTED,
                "physical_acceptance": {
                    "acceptance_ref": accepted["acceptance_ref"],
                    "accepted_on": "2026-07-21",
                    "geometry_manifest": accepted["geometry_manifest"],
                    "manifest_sha256": accepted["manifest_sha256"],
                },
            }
        )
        write_json(change_path, change)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "must advance an awaiting record",
        ):
            qualification.build_plan(head, base)

    def test_retained_change_history_cannot_be_removed(self) -> None:
        accepted_root = self.clone_root()
        accepted = self.accepted_base(accepted_root)

        base = self.clone_root()
        profile = read_json(base / PROFILE)
        downgrade(profile)
        write_json(base / PROFILE, profile)
        waiting_path = self.waiting_change(base, base=accepted)

        head = self.clone_root()
        shutil.rmtree(head)
        shutil.copytree(base, head)
        (head / "qualification/changes" / waiting_path.name).unlink()
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "retained change history cannot be removed",
        ):
            qualification.build_plan(head, base)

        completed = read_json(waiting_path)
        completed["transition"].update(
            {
                "state": qualification.ACCEPTED,
                "physical_acceptance": {
                    "acceptance_ref": accepted["acceptance_ref"],
                    "accepted_on": "2026-07-21",
                    "geometry_manifest": accepted["geometry_manifest"],
                    "manifest_sha256": accepted["manifest_sha256"],
                },
            }
        )
        write_json(waiting_path, completed)
        head = self.clone_root()
        shutil.rmtree(head)
        shutil.copytree(base, head)
        (head / "qualification/changes" / waiting_path.name).unlink()
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "retained change history cannot be removed",
        ):
            qualification.build_plan(head, base)

    def test_declared_invalidation_is_planned_and_preserves_old_manifest(
        self,
    ) -> None:
        base = self.clone_root()
        head = self.clone_root()
        accepted = self.accepted_base(base)
        profile = read_json(head / PROFILE)
        downgrade(profile)
        write_json(head / PROFILE, profile)
        self.waiting_change(head, base=accepted)

        plan = qualification.build_plan(head, base)
        self.assertEqual("invalidate", plan["matrix"]["include"][0]["mode"])

        (head / MANIFEST).write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "prior accepted manifest changed",
        ):
            qualification.build_plan(head, base)

        head = self.clone_root()
        profile = read_json(head / PROFILE)
        downgrade(profile)
        write_json(head / PROFILE, profile)
        self.waiting_change(head, base=accepted)
        fixture_lock = head / LOCK
        fixture_lock.write_text(
            fixture_lock.read_text(encoding="utf-8") + " \n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "prior accepted fixture lock changed",
        ):
            qualification.build_plan(head, base)

    def test_requalification_requires_later_pr_and_new_manifest(self) -> None:
        base = self.clone_root()
        self.install_fake_metrics(base)
        accepted = self.accepted_base(base)
        profile = read_json(base / PROFILE)
        downgrade(profile)
        write_json(base / PROFILE, profile)
        change_path = self.waiting_change(base, base=accepted)

        head = self.clone_root()
        shutil.rmtree(head)
        shutil.copytree(base, head)

        new_manifest_path = head / "qualification/trimui-smart-pro-family-v2.json"
        new_manifest = read_json(head / MANIFEST)
        new_manifest["qualification"].update(
            {
                "acceptance_ref": "tsp-owner-fit-v2",
                "accepted_on": "2026-07-26",
                "accepted_source_revision": "b" * 40,
                "characterized_source_revision": "b" * 40,
            }
        )
        write_json(new_manifest_path, new_manifest)

        profile = read_json(head / PROFILE)
        profile["qualification"].update(
            {
                "status": qualification.QUALIFIED,
                "acceptance_ref": "tsp-owner-fit-v2",
                "accepted_on": "2026-07-26",
                "accepted_geometry_revision": "b" * 40,
                "geometry_manifest": (
                    "qualification/trimui-smart-pro-family-v2.json"
                ),
                "artifact_names": [
                    "carrier_body",
                    "fit_coupon",
                    "j_hook",
                    "j_hook_set",
                ],
            }
        )
        write_json(head / PROFILE, profile)

        change = read_json(
            head / "qualification/changes" / change_path.name
        )
        change["transition"].update(
            {
                "state": qualification.ACCEPTED,
                "physical_acceptance": {
                    "acceptance_ref": "tsp-owner-fit-v2",
                    "accepted_on": "2026-07-26",
                    "geometry_manifest": (
                        "qualification/trimui-smart-pro-family-v2.json"
                    ),
                    "manifest_sha256": sha256(new_manifest_path),
                },
            }
        )
        write_json(
            head / "qualification/changes" / change_path.name,
            change,
        )

        plan = qualification.build_plan(head, base)
        self.assertEqual("requalify", plan["matrix"]["include"][0]["mode"])

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        report = qualification.check_job(
            head,
            base,
            "trimui-smart-pro-family",
            Path(temporary.name) / "requalification",
            openscad="fake-openscad",
            renderer=self.fake_renderer(),
            verify_toolchain=False,
        )
        self.assertEqual(
            [],
            report["summary"]["physical_acceptance_drift_artifacts"],
        )

        def drift_after_acceptance(
            resolved,
            artifact_name: str,
            output: Path,
            *,
            openscad: str,
        ) -> None:
            self.assertEqual("fake-openscad", openscad)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                (
                    SCALED_TETRAHEDRON
                    if (
                        resolved.root == head.resolve()
                        and artifact_name == "j_hook"
                    )
                    else TETRAHEDRON
                ),
                encoding="ascii",
            )

        drift_output = Path(temporary.name) / "requalification-drift"
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "drifted after physical acceptance",
        ):
            qualification.check_job(
                head,
                base,
                "trimui-smart-pro-family",
                drift_output,
                openscad="fake-openscad",
                renderer=drift_after_acceptance,
                verify_toolchain=False,
            )
        drift_report = read_json(drift_output / "geometry-diff.json")
        self.assertEqual(
            ["j_hook"],
            drift_report["summary"][
                "physical_acceptance_drift_artifacts"
            ],
        )

        new_manifest["qualification"]["acceptance_ref"] = accepted[
            "acceptance_ref"
        ]
        write_json(new_manifest_path, new_manifest)
        profile = read_json(head / PROFILE)
        profile["qualification"]["acceptance_ref"] = accepted["acceptance_ref"]
        write_json(head / PROFILE, profile)
        change = read_json(
            head / "qualification/changes" / change_path.name
        )
        change["transition"]["physical_acceptance"].update(
            {
                "acceptance_ref": accepted["acceptance_ref"],
                "manifest_sha256": sha256(new_manifest_path),
            }
        )
        write_json(
            head / "qualification/changes" / change_path.name,
            change,
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "fresh physical acceptance reference",
        ):
            qualification.build_plan(head, base)

    def test_awaiting_candidate_can_be_refined_before_acceptance(self) -> None:
        accepted_root = self.clone_root()
        base = self.clone_root()
        accepted = self.accepted_base(accepted_root)
        profile = read_json(base / PROFILE)
        downgrade(profile)
        write_json(base / PROFILE, profile)
        change_path = self.waiting_change(base, base=accepted)

        head = self.clone_root()
        shutil.rmtree(head)
        shutil.copytree(base, head)
        accepted_toolchain = head / "qualification/cad-toolchain.json"
        toolchain = head / "qualification/cad-toolchain-candidate-v2.json"
        toolchain.write_text(
            accepted_toolchain.read_text(encoding="utf-8") + " \n",
            encoding="utf-8",
        )
        change = read_json(
            head / "qualification/changes" / change_path.name
        )
        change["transition"].update(
            {
                "candidate_toolchain_lock": (
                    "qualification/cad-toolchain-candidate-v2.json"
                ),
                "candidate_toolchain_sha256": sha256(toolchain),
            }
        )
        write_json(
            head / "qualification/changes" / change_path.name,
            change,
        )

        plan = qualification.build_plan(head, base)
        self.assertEqual("candidate", plan["matrix"]["include"][0]["mode"])

        accepted_toolchain.write_text(
            accepted_toolchain.read_text(encoding="utf-8") + " \n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "prior accepted toolchain lock changed",
        ):
            qualification.build_plan(head, base)

    def test_fake_renderer_proves_exact_and_drift_reports_are_deterministic(
        self,
    ) -> None:
        base = self.clone_root()
        head = self.clone_root()
        self.install_fake_metrics(base)
        self.install_fake_metrics(head)

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        first = Path(temporary.name) / "first"
        second = Path(temporary.name) / "second"
        report = qualification.check_job(
            head,
            base,
            "trimui-smart-pro-family",
            first,
            openscad="fake-openscad",
            renderer=self.fake_renderer(),
            verify_toolchain=False,
        )
        self.assertEqual([], report["summary"]["changed_artifacts"])
        self.assertEqual(
            [
                "carrier_body",
                "fit_coupon",
                "j_hook",
                "j_hook_set",
            ],
            report["summary"]["unchanged_artifacts"],
        )
        qualification.check_job(
            head,
            base,
            "trimui-smart-pro-family",
            second,
            openscad="fake-openscad",
            renderer=self.fake_renderer(),
            verify_toolchain=False,
        )
        self.assertEqual(
            (first / "geometry-diff.json").read_bytes(),
            (second / "geometry-diff.json").read_bytes(),
        )
        report_text = (first / "geometry-diff.json").read_text(
            encoding="utf-8"
        )
        self.assertNotIn(str(head), report_text)
        self.assertNotIn(str(base), report_text)

        drift = Path(temporary.name) / "drift"
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "qualified geometry drifted",
        ):
            qualification.check_job(
                head,
                base,
                "trimui-smart-pro-family",
                drift,
                openscad="fake-openscad",
                renderer=self.fake_renderer("j_hook"),
                verify_toolchain=False,
            )
        drift_report = read_json(drift / "geometry-diff.json")
        self.assertEqual(
            ["j_hook"],
            drift_report["summary"]["changed_artifacts"],
        )
        self.assertTrue(
            drift_report["artifacts"]["j_hook"]["delta"][
                "fingerprint_changed"
            ]
        )

    def test_declared_interface_invalidation_allows_an_exact_mesh_candidate(
        self,
    ) -> None:
        base = self.clone_root()
        head = self.clone_root()
        self.install_fake_metrics(base)
        self.install_fake_metrics(head)
        accepted = self.accepted_base(base)
        profile = read_json(head / PROFILE)
        downgrade(profile)
        write_json(head / PROFILE, profile)
        self.waiting_change(
            head,
            base=accepted,
            scopes=["fixture_interface"],
        )

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        report = qualification.check_job(
            head,
            base,
            "trimui-smart-pro-family",
            Path(temporary.name) / "interface-candidate",
            openscad="fake-openscad",
            renderer=self.fake_renderer(),
            verify_toolchain=False,
        )
        self.assertEqual("invalidate", report["mode"])
        self.assertEqual([], report["summary"]["changed_artifacts"])

    def test_intentional_candidate_reports_added_and_removed_artifacts(
        self,
    ) -> None:
        base = self.clone_root()
        head = self.clone_root()
        self.install_fake_metrics(base)
        self.install_fake_metrics(head)
        accepted = self.accepted_base(base)
        profile = read_json(head / PROFILE)
        profile["artifacts"]["new_clamp"] = profile["artifacts"].pop(
            "j_hook_set"
        )
        downgrade(profile)
        write_json(head / PROFILE, profile)
        self.waiting_change(
            head,
            base=accepted,
            scopes=["mechanism"],
        )

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        report = qualification.check_job(
            head,
            base,
            "trimui-smart-pro-family",
            Path(temporary.name) / "mechanism-candidate",
            openscad="fake-openscad",
            renderer=self.fake_renderer(),
            verify_toolchain=False,
        )
        self.assertEqual(
            ["new_clamp"],
            report["summary"]["added_artifacts"],
        )
        self.assertEqual(
            ["j_hook_set"],
            report["summary"]["removed_artifacts"],
        )
        self.assertEqual(
            ["j_hook_set", "new_clamp"],
            report["summary"]["changed_artifacts"],
        )
        self.assertFalse(
            report["artifacts"]["j_hook_set"]["candidate_present"]
        )
        self.assertFalse(
            report["artifacts"]["new_clamp"]["baseline_present"]
        )

    def test_generated_output_cannot_overwrite_source_or_existing_evidence(
        self,
    ) -> None:
        base = self.clone_root()
        head = self.clone_root()
        self.install_fake_metrics(base)
        self.install_fake_metrics(head)
        source_path = head / PROFILE
        source_bytes = source_path.read_bytes()
        self.assertEqual(
            1,
            qualification.main(
                [
                    "--root",
                    str(head),
                    "plan",
                    "--base-root",
                    str(base),
                    "--output",
                    str(source_path),
                ]
            ),
        )
        self.assertEqual(source_bytes, source_path.read_bytes())

        repository_root = head.parent
        (repository_root / ".git").mkdir()
        repository_source = repository_root / "README.md"
        repository_source.write_text("source\n", encoding="utf-8")
        self.assertEqual(
            1,
            qualification.main(
                [
                    "--root",
                    str(head),
                    "plan",
                    "--base-root",
                    str(base),
                    "--output",
                    str(repository_source),
                ]
            ),
        )
        self.assertEqual(
            "source\n",
            repository_source.read_text(encoding="utf-8"),
        )

        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "must stay under build",
        ):
            qualification.check_job(
                head,
                base,
                "trimui-smart-pro-family",
                head / "profiles/generated-review",
                openscad="fake-openscad",
                renderer=self.fake_renderer(),
                verify_toolchain=False,
            )

        existing = head / "build/existing-review"
        existing.mkdir(parents=True)
        with self.assertRaisesRegex(
            qualification.QualificationCiError,
            "refusing to overwrite",
        ):
            qualification.check_job(
                head,
                base,
                "trimui-smart-pro-family",
                existing,
                openscad="fake-openscad",
                renderer=self.fake_renderer(),
                verify_toolchain=False,
            )


if __name__ == "__main__":
    unittest.main()
