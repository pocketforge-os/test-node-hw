#!/usr/bin/env python3
"""Regression tests for declarative PocketForge DUT holder profiles."""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import holder_profiles as profiles


ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = ROOT / "profiles/trimui-smart-pro-family.json"
LOCK_PATH = (
    ROOT
    / "profiles/fixture-locks/trimui-smart-pro-family-v1.json"
)
QUALIFICATION_PATH = (
    ROOT / "qualification/trimui-smart-pro-family-v1.json"
)
TOOLCHAIN_PATH = ROOT / "qualification/cad-toolchain.json"
SCAD_SOURCES = (
    "trimui-smart-pro-family-cradle.scad",
    "trimui-smart-pro-cradle.scad",
    "trimui-smart-pro-s-cradle.scad",
)


def raw_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def refresh_lock_hash(lock: dict, profile: dict) -> str:
    digest = profiles.fixture_interface_hash(lock)
    lock["interface"]["sha256"] = digest
    for contract in lock["source"]["contracts"]:
        contract["resolved_interface_sha256"] = digest
    profile["fixture"]["interface_sha256"] = digest
    profile["qualification"]["fixture_interface_sha256"] = digest
    return digest


def write_profile_root(root: Path, profile: dict, lock: dict) -> Path:
    write_json(root / "profiles/trimui-smart-pro-family.json", profile)
    write_json(
        root / "profiles/fixture-locks/trimui-smart-pro-family-v1.json",
        lock,
    )
    (root / "qualification").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        QUALIFICATION_PATH,
        root / "qualification/trimui-smart-pro-family-v1.json",
    )
    shutil.copy2(
        TOOLCHAIN_PATH,
        root / "qualification/cad-toolchain.json",
    )
    for source in SCAD_SOURCES:
        (root / source).write_text("// profile test source\n", encoding="utf-8")
    return root / "profiles/trimui-smart-pro-family.json"


class HolderProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = raw_json(PROFILE_PATH)
        self.lock = raw_json(LOCK_PATH)
        self.resolved = profiles.validate_profile(ROOT, PROFILE_PATH)

    def validate_temp(self, profile: dict, lock: dict):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        path = write_profile_root(root, profile, lock)
        return profiles.validate_profile(root, path)

    def test_repository_profile_is_read_only_and_matches_known_lock(self) -> None:
        paths = [PROFILE_PATH, LOCK_PATH, QUALIFICATION_PATH]
        before = {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }
        resolved = profiles.validate_profile(ROOT, PROFILE_PATH)
        after = {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }
        self.assertEqual(before, after)
        self.assertEqual(
            "637aa67b32e284af2d5ad1b1655e630392e06fa80af1996f498f8d3cdecb20d5",
            resolved.lock_state["hash"],
        )
        self.assertEqual(
            set(self.profile["device_slugs"]),
            set(resolved.lock_state["contracts"]),
        )

    def test_compiler_maps_locked_contacts_to_accepted_carrier_poses(self) -> None:
        poses = {
            row[0]: row[1:]
            for row in self.resolved.openscad_parameters["clamp_poses"]
        }
        self.assertEqual(
            [
                [profiles.Decimal("58.825"), profiles.Decimal("60.115")],
                90,
                profiles.Decimal("0.25"),
            ],
            poses["bottom_left"],
        )
        self.assertEqual(
            [
                [profiles.Decimal("188.175"), profiles.Decimal("60.115")],
                90,
                profiles.Decimal("0.25"),
            ],
            poses["bottom_right"],
        )
        self.assertEqual(
            [
                [profiles.Decimal("29.325"), profiles.Decimal("100")],
                0,
                profiles.Decimal("0.6"),
            ],
            poses["left_datum"],
        )
        self.assertEqual(
            [
                [profiles.Decimal("217.675"), profiles.Decimal("100")],
                180,
                profiles.Decimal("0.6"),
            ],
            poses["right_datum"],
        )
        self.assertEqual(
            [
                [profiles.Decimal("72.030"), profiles.Decimal("139.885")],
                -90,
                profiles.Decimal("0.45"),
            ],
            poses["top_left"],
        )
        self.assertEqual(
            [
                [profiles.Decimal("175.675"), profiles.Decimal("139.885")],
                -90,
                profiles.Decimal("0.45"),
            ],
            poses["top_right"],
        )
        self.assertEqual(
            [profiles.Decimal("34"), profiles.Decimal("50")],
            self.resolved.openscad_parameters["top_right_safe"],
        )

    def test_hash_rejects_changed_lock_and_normalizes_representation(self) -> None:
        changed = copy.deepcopy(self.lock)
        changed["interface"]["fixture_interface"]["contact_regions"].reverse()
        changed["interface"]["fixture_interface"]["contact_regions"][0][
            "contact_modes"
        ].reverse()
        self.assertEqual(
            profiles.fixture_interface_hash(self.lock),
            profiles.fixture_interface_hash(changed),
        )

        changed["interface"]["fixture_interface"]["contact_regions"][0]["shape"][
            "max_mm"
        ] += 0.001
        with self.assertRaisesRegex(profiles.ProfileError, "stale lock hash"):
            profiles.validate_fixture_lock(ROOT, LOCK_PATH, changed)

    def test_unknown_missing_and_wrong_types_are_rejected(self) -> None:
        unknown = copy.deepcopy(self.profile)
        unknown["surprise"] = True
        with self.assertRaisesRegex(profiles.ProfileError, "unknown field"):
            self.validate_temp(unknown, self.lock)

        missing = copy.deepcopy(self.profile)
        del missing["fixture"]
        with self.assertRaisesRegex(profiles.ProfileError, "missing required field"):
            self.validate_temp(missing, self.lock)

        wrong_type = copy.deepcopy(self.profile)
        wrong_type["implementation"]["retention"]["hook"]["throat_mm"] = "11.3"
        with self.assertRaisesRegex(profiles.ProfileError, "finite number"):
            self.validate_temp(wrong_type, self.lock)

    def test_contact_outside_locked_range_and_bad_binding_are_rejected(self) -> None:
        outside = copy.deepcopy(self.profile)
        outside["implementation"]["contacts"][0]["selected_coordinate_mm"] = 23.999
        with self.assertRaisesRegex(profiles.ProfileError, "outside locked interval"):
            self.validate_temp(outside, self.lock)

        bad_binding = copy.deepcopy(self.profile)
        bad_binding["fixture"]["bindings"]["local_depth"] = "invented_depth"
        with self.assertRaisesRegex(profiles.ProfileError, "unknown locked depths"):
            self.validate_temp(bad_binding, self.lock)

    def test_mechanism_contact_roles_cannot_move_to_another_surface(self) -> None:
        profile = copy.deepcopy(self.profile)
        lock = copy.deepcopy(self.lock)
        top_left = next(
            contact
            for contact in lock["interface"]["fixture_interface"][
                "contact_regions"
            ]
            if contact["id"] == "top_left"
        )
        top_left["shape"]["surface"] = "bottom_edge"
        top_left["normal"] = [0, 1, 0]
        refresh_lock_hash(lock, profile)
        with self.assertRaisesRegex(
            profiles.ProfileError,
            "requires surface 'top_edge'",
        ):
            self.validate_temp(profile, lock)

    def test_contact_must_use_the_bound_local_depth(self) -> None:
        profile = copy.deepcopy(self.profile)
        lock = copy.deepcopy(self.lock)
        alternate = copy.deepcopy(
            lock["interface"]["fixture_interface"]["local_depths"][0]
        )
        alternate["id"] = "alternate_perimeter_depth"
        lock["interface"]["fixture_interface"]["local_depths"].append(alternate)
        lock["interface"]["fixture_interface"]["contact_regions"][0][
            "local_depth_ref"
        ] = alternate["id"]
        refresh_lock_hash(lock, profile)
        with self.assertRaisesRegex(
            profiles.ProfileError,
            "does not use the bound local depth",
        ):
            self.validate_temp(profile, lock)

    def test_fixture_lock_supports_a_device_without_aliases(self) -> None:
        profile = copy.deepcopy(self.profile)
        lock = copy.deepcopy(self.lock)
        profile["device_slugs"] = ["trimui-smart-pro"]
        qualification = profile["qualification"]
        qualification["status"] = "unqualified"
        qualification["acceptance_ref"] = None
        qualification["accepted_on"] = None
        qualification["accepted_geometry_revision"] = None
        qualification["geometry_manifest"] = None
        qualification["artifact_names"] = []
        lock["source"]["contracts"] = [
            contract
            for contract in lock["source"]["contracts"]
            if contract["kind"] == "fixture_interface"
        ]
        resolved = self.validate_temp(profile, lock)
        self.assertEqual(
            {"trimui-smart-pro"},
            set(resolved.lock_state["contracts"]),
        )

    def test_insufficient_locked_rear_clearance_fails_qualified_fit_linkage(self) -> None:
        profile = copy.deepcopy(self.profile)
        lock = copy.deepcopy(self.lock)
        lock["interface"]["fixture_interface"]["clearance_requirements"][0][
            "minimum_mm"
        ] = 10
        refresh_lock_hash(lock, profile)
        with self.assertRaisesRegex(
            profiles.ProfileError,
            "device_rear_gap does not match",
        ):
            self.validate_temp(profile, lock)

    def test_malformed_consumed_fixture_values_are_rejected_before_render(
        self,
    ) -> None:
        profile = copy.deepcopy(self.profile)
        lock = copy.deepcopy(self.lock)
        lock["interface"]["fixture_interface"]["local_depths"][0][
            "nominal_mm"
        ] = "10.7"
        refresh_lock_hash(lock, profile)
        with self.assertRaisesRegex(profiles.ProfileError, "finite number"):
            self.validate_temp(profile, lock)

        profile = copy.deepcopy(self.profile)
        lock = copy.deepcopy(self.lock)
        lock["interface"]["fixture_interface"]["access_regions"][0]["shape"][
            "surface"
        ] = "front"
        refresh_lock_hash(lock, profile)
        with self.assertRaisesRegex(
            profiles.ProfileError,
            "must be a rear XY surface rectangle",
        ):
            self.validate_temp(profile, lock)

    def test_qualification_manifest_must_name_the_profile_devices(self) -> None:
        profile = copy.deepcopy(self.profile)
        manifest = raw_json(QUALIFICATION_PATH)
        manifest["qualification"]["device_ids"] = ["another-device"]
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        path = write_profile_root(root, profile, self.lock)
        write_json(
            root / "qualification/trimui-smart-pro-family-v1.json",
            manifest,
        )
        with self.assertRaisesRegex(
            profiles.ProfileError,
            "device slugs do not match",
        ):
            profiles.validate_profile(root, path)

    def test_paths_cannot_escape_cradle_root(self) -> None:
        profile = copy.deepcopy(self.profile)
        profile["implementation"]["source"] = "../outside.scad"
        with self.assertRaisesRegex(profiles.ProfileError, "escapes cradle root"):
            self.validate_temp(profile, self.lock)

    def test_custom_openscad_escape_hatch_must_remain_unqualified(self) -> None:
        custom = copy.deepcopy(self.profile)
        custom["implementation"] = {
            "kind": "custom_openscad",
            "source": "trimui-smart-pro-family-cradle.scad",
            "rationale": "New shell mechanism not expressible by an existing family.",
            "reusable_family_followup": "bead:tsp-example",
        }
        with self.assertRaisesRegex(
            profiles.ProfileError,
            "unqualified escape hatch",
        ):
            self.validate_temp(custom, self.lock)

        qualification = custom["qualification"]
        qualification["status"] = "unqualified"
        qualification["acceptance_ref"] = None
        qualification["accepted_on"] = None
        qualification["accepted_geometry_revision"] = None
        qualification["geometry_manifest"] = None
        qualification["artifact_names"] = []
        resolved = self.validate_temp(custom, self.lock)
        self.assertEqual("custom_openscad", resolved.document["implementation"]["kind"])
        self.assertEqual({}, resolved.openscad_parameters)

    def test_openscad_serialization_and_command_are_deterministic(self) -> None:
        self.assertEqual("true", profiles.openscad_literal(True))
        self.assertEqual("-0.25", profiles.openscad_literal(-0.25))
        self.assertEqual(
            '[[1, 2], "safe"]',
            profiles.openscad_literal([[1, 2], "safe"]),
        )
        with self.assertRaisesRegex(profiles.ProfileError, "only finite numbers"):
            profiles.openscad_literal({"unsafe": "object"})

        output = Path("/tmp/profile-test-output.stl")
        first = profiles.artifact_command(
            self.resolved,
            "j_hook",
            output,
            openscad="openscad",
        )
        second = profiles.artifact_command(
            self.resolved,
            "j_hook",
            output,
            openscad="openscad",
        )
        self.assertEqual(first, second)
        self.assertIsInstance(first, list)
        definitions = [
            first[index + 1]
            for index, token in enumerate(first[:-1])
            if token == "-D"
        ]
        self.assertEqual(definitions, sorted(definitions))
        self.assertIn("hook_throat=11.3", definitions)

    def test_source_pin_verification_checks_raw_bytes_and_alias_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            platform_root = Path(tmp)
            subprocess.run(
                ["git", "init", "-q", str(platform_root)],
                check=True,
            )
            interface = self.lock["interface"]
            full = {
                "schema_version": interface["schema_version"],
                "kind": "fixture_interface",
                "device": {"slug": "trimui-smart-pro"},
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
            full_path = (
                platform_root
                / "device-models/trimui-smart-pro/fixture-contract.json"
            )
            alias_path = (
                platform_root
                / "device-models/trimui-smart-pro-s/fixture-contract.json"
            )
            write_json(full_path, full)
            write_json(alias_path, alias)
            subprocess.run(["git", "-C", str(platform_root), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(platform_root),
                    "-c",
                    "user.name=Fixture Test",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "fixture source",
                ],
                check=True,
            )
            revision = subprocess.check_output(
                ["git", "-C", str(platform_root), "rev-parse", "HEAD"],
                text=True,
            ).strip()

            lock = copy.deepcopy(self.lock)
            lock["source"]["revision"] = revision
            source_paths = {
                "trimui-smart-pro": full_path,
                "trimui-smart-pro-s": alias_path,
            }
            for contract in lock["source"]["contracts"]:
                contract["raw_sha256"] = hashlib.sha256(
                    source_paths[contract["device_slug"]].read_bytes()
                ).hexdigest()
            state = profiles.validate_fixture_lock(ROOT, LOCK_PATH, lock)
            resolved = dataclasses.replace(
                self.resolved,
                lock=lock,
                lock_state=state,
            )
            profiles.verify_source_pin(resolved, platform_root)

            alias["expected_fixture_interface_sha256"] = "f" * 64
            write_json(alias_path, alias)
            subprocess.run(["git", "-C", str(platform_root), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(platform_root),
                    "-c",
                    "user.name=Fixture Test",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "bad alias",
                ],
                check=True,
            )
            revision = subprocess.check_output(
                ["git", "-C", str(platform_root), "rev-parse", "HEAD"],
                text=True,
            ).strip()
            lock["source"]["revision"] = revision
            for contract in lock["source"]["contracts"]:
                contract["raw_sha256"] = hashlib.sha256(
                    source_paths[contract["device_slug"]].read_bytes()
                ).hexdigest()
            state = profiles.validate_fixture_lock(ROOT, LOCK_PATH, lock)
            resolved = dataclasses.replace(
                self.resolved,
                lock=lock,
                lock_state=state,
            )
            with self.assertRaisesRegex(
                profiles.ProfileError,
                "does not resolve the locked interface",
            ):
                profiles.verify_source_pin(resolved, platform_root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
