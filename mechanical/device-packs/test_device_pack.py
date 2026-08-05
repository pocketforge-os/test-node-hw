#!/usr/bin/env python3
"""Unit tests for deterministic device print-pack generation."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

import build_device_pack as packs


TETRAHEDRON = """solid tetrahedron
facet normal 0 0 -1
  outer loop
    vertex 0 0 0
    vertex 0 1 0
    vertex 1 0 0
  endloop
endfacet
facet normal 0 -1 0
  outer loop
    vertex 0 0 0
    vertex 1 0 0
    vertex 0 0 1
  endloop
endfacet
facet normal -1 0 0
  outer loop
    vertex 0 0 0
    vertex 0 0 1
    vertex 0 1 0
  endloop
endfacet
facet normal 1 1 1
  outer loop
    vertex 1 0 0
    vertex 0 1 0
    vertex 0 0 1
  endloop
endfacet
endsolid tetrahedron
"""


def fake_renderer(
    item: packs.PlanItem, output: Path, openscad: str
) -> None:
    del item, openscad
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(TETRAHEDRON, encoding="ascii")


def no_contract_check(
    profile: packs.holder_profiles.ResolvedProfile,
    layout: packs.ResolvedLayout,
    openscad: str,
) -> None:
    del profile, layout, openscad


def write_layout_guard_tree(
    root: Path,
    *,
    status: str,
    role: str = "Deterministic test artifact",
) -> Path:
    layout_path = (
        root
        / "mechanical"
        / "device-packs"
        / "layouts"
        / "demo-v1.json"
    )
    registry_path = (
        root / "mechanical" / "device-packs" / "device-layouts.json"
    )
    source_path = root / "mechanical" / "demo.scad"
    toolchain_path = root / "mechanical" / "toolchain.json"
    layout_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("cube([1, 1, 1]);\n", encoding="utf-8")
    toolchain_path.write_text("{}\n", encoding="utf-8")
    registry_path.write_text(
        json.dumps(
            {
                "schema": packs.LAYOUT_REGISTRY_SCHEMA,
                "devices": {
                    "device-demo": {
                        "layout": (
                            "mechanical/device-packs/layouts/demo-v1.json"
                        )
                    }
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    layout_path.write_text(
        json.dumps(
            {
                "schema": packs.LAYOUT_SCHEMA,
                "layout_id": "demo-v1",
                "toolchain_lock": "mechanical/toolchain.json",
                "input_paths": [
                    "mechanical/device-packs/device-layouts.json"
                ],
                "qualification": {
                    "status": status,
                    "acceptance_ref": "test-acceptance",
                    "accepted_on": (
                        "2026-07-27"
                        if status == "physically_qualified"
                        else None
                    ),
                    "device_slugs": ["device-demo"],
                    "scope": ["Test-only layout guard contract."],
                },
                "artifacts": [
                    {
                        "id": "demo_artifact",
                        "output": "chassis/demo.stl",
                        "role": role,
                        "scope": "common",
                        "modes": ["full"],
                        "source": "mechanical/demo.scad",
                        "part": "demo",
                        "parameters": {},
                        "parameter_bindings": {},
                        "expected_normalized_sha256": "a" * 64,
                        "print": {
                            "material": "ABS",
                            "scale_percent": 100,
                            "supports": False,
                            "auto_orient": False,
                            "notes": [],
                        },
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return layout_path


class DevicePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = packs.REPO_ROOT
        cls.profile_path = (
            packs.CRADLE_ROOT
            / "profiles"
            / "trimui-smart-pro-family.json"
        )
        cls.layout_path = (
            cls.root
            / "mechanical"
            / "device-packs"
            / "layouts"
            / "chassis-core-v1.json"
        )
        cls.profile = packs.holder_profiles.validate_profile(
            packs.CRADLE_ROOT, cls.profile_path
        )
        cls.layout = packs.load_layout(cls.root, cls.layout_path)
        cls.current_layout_path = (
            cls.root
            / "mechanical"
            / "device-packs"
            / "layouts"
            / "chassis-core-v3.json"
        )
        cls.current_layout = packs.load_layout(
            cls.root, cls.current_layout_path
        )
        cls.dualbar_layout_path = (
            cls.root
            / "mechanical"
            / "device-packs"
            / "layouts"
            / "chassis-dualbar-v2.json"
        )
        cls.dualbar_layout = packs.load_layout(
            cls.root, cls.dualbar_layout_path
        )
        cls.brick_profile_path = (
            packs.CRADLE_ROOT / "profiles" / "trimui-brick.json"
        )
        cls.brick_profile = packs.holder_profiles.validate_profile(
            packs.CRADLE_ROOT, cls.brick_profile_path
        )
        cls.brick_layout_path = (
            cls.root
            / "mechanical"
            / "device-packs"
            / "layouts"
            / "chassis-dualbar-brick-v2.json"
        )
        cls.brick_layout = packs.load_layout(
            cls.root, cls.brick_layout_path
        )

    def test_modes_have_exact_membership(self) -> None:
        expected = {
            "coupon": {"holder_fit_coupon"},
            "retrofit": {
                "holder_fit_coupon",
                "device_carrier",
                "device_j_hook_set",
                "device_carrier_links",
                "device_nameplate",
                "device_wire_anchors",
            },
            "full": {
                "holder_fit_coupon",
                "device_carrier",
                "device_j_hook_set",
                "device_carrier_links",
                "device_nameplate",
                "device_wire_anchors",
                "chassis_process_calibration",
                "chassis_core_01_ironed_interfaces",
                "chassis_core_02_splice_collars",
                "chassis_core_03_movable_mounts",
                "chassis_core_04_frame_hardware",
                "chassis_core_05_placard_holder",
            },
        }
        for mode, artifact_ids in expected.items():
            with self.subTest(mode=mode):
                plan = packs.build_plan(
                    self.root,
                    self.profile,
                    self.layout,
                    "trimui-smart-pro",
                    mode,
                )
                self.assertEqual(artifact_ids, {item.artifact_id for item in plan})
                for item in plan:
                    expected_material = (
                        "PETG"
                        if item.artifact_id
                        in {
                            "holder_fit_coupon",
                            "device_carrier",
                            "device_j_hook_set",
                        }
                        else "ABS"
                    )
                    self.assertEqual(
                        expected_material,
                        item.print_contract["material"],
                    )

    def test_static_layout_geometry_is_regression_locked(self) -> None:
        for layout in (
            self.layout,
            self.current_layout,
            self.dualbar_layout,
        ):
            for artifact in layout.artifacts:
                with self.subTest(
                    layout=layout.layout_id,
                    artifact=artifact.artifact_id,
                ):
                    if artifact.parameter_bindings:
                        self.assertEqual(
                            "device_nameplate", artifact.artifact_id
                        )
                        self.assertIsNone(
                            artifact.expected_normalized_sha256
                        )
                    else:
                        self.assertRegex(
                            artifact.expected_normalized_sha256 or "",
                            r"^[0-9a-f]{64}$",
                        )

    def test_device_registry_selects_layout_and_rejects_mismatch(self) -> None:
        pro = packs.resolve_device_layout(
            self.root, "trimui-smart-pro"
        )
        pro_s = packs.resolve_device_layout(
            self.root, "trimui-smart-pro-s"
        )
        self.assertEqual("chassis-core-v3", pro.layout_id)
        self.assertEqual("chassis-core-v2", pro.supersedes_layout_id)
        self.assertEqual("candidate", pro.qualification["status"])
        self.assertEqual("chassis-dualbar-v2", pro_s.layout_id)
        self.assertEqual("chassis-dualbar-v1", pro_s.supersedes_layout_id)
        self.assertEqual("candidate", pro_s.qualification["status"])
        for layout in (pro, pro_s):
            carrier_links = next(
                artifact
                for artifact in layout.artifacts
                if artifact.artifact_id == "device_carrier_links"
            )
            self.assertEqual(
                "stack_clear_v2",
                carrier_links.parameters["CARRIER_LINK_REVISION"],
            )
        with self.assertRaisesRegex(
            packs.PackError, "does not match registered layout"
        ):
            packs.resolve_device_layout(
                self.root,
                "trimui-smart-pro-s",
                requested_layout=self.layout_path,
            )

    def test_layout_matrix_separates_production_and_candidate_devices(
        self,
    ) -> None:
        production = packs.device_layout_matrix(
            self.root,
            self.profile,
            kind="production-devices",
        )
        candidate = packs.device_layout_matrix(
            self.root,
            self.profile,
            kind="candidate-layout-devices",
        )
        self.assertEqual([], production["include"])
        self.assertEqual(
            [
                {
                    "device_slug": "trimui-smart-pro",
                    "layout_id": "chassis-core-v3",
                    "layout_status": "candidate",
                    "holder_status": "physically_qualified",
                },
                {
                    "device_slug": "trimui-smart-pro-s",
                    "layout_id": "chassis-dualbar-v2",
                    "layout_status": "candidate",
                    "holder_status": "physically_qualified",
                },
            ],
            candidate["include"],
        )

    def test_side_clear_successors_emit_a_dedicated_retrofit_bed(
        self,
    ) -> None:
        for device_slug, profile, layout in (
            ("trimui-smart-pro", self.profile, self.current_layout),
            ("trimui-smart-pro-s", self.profile, self.dualbar_layout),
            ("trimui-brick", self.brick_profile, self.brick_layout),
        ):
            with self.subTest(device=device_slug):
                retrofit = packs.build_plan(
                    self.root, profile, layout, device_slug, "retrofit"
                )
                joint = next(
                    item
                    for item in retrofit
                    if item.artifact_id
                    == "chassis_side_clear_joint_plate_set"
                )
                self.assertEqual("gantry_joint_plate_set", joint.part)
                self.assertEqual(
                    "side_clear_v2",
                    joint.parameters["GANTRY_JOINT_REVISION"],
                )
                self.assertEqual(
                    "ba6209606b3927a56d865571c41a5f8c45ac6d350d8680780499983b5c575cc2",
                    joint.expected_normalized_sha256,
                )

    def test_dualbar_full_mode_replaces_only_legacy_core_01_to_03(
        self,
    ) -> None:
        plan = packs.build_plan(
            self.root,
            self.profile,
            self.dualbar_layout,
            "trimui-smart-pro-s",
            "full",
        )
        ids = {item.artifact_id for item in plan}
        self.assertEqual(12, len(plan))
        self.assertTrue(
            {
                "chassis_dualbar_01_ironed_interfaces",
                "chassis_dualbar_02_fixture_links",
                "chassis_side_clear_joint_plate_set",
            }
            <= ids
        )
        self.assertFalse(
            {
                "chassis_core_01_ironed_interfaces",
                "chassis_core_02_splice_collars",
                "chassis_core_03_movable_mounts",
            }
            & ids
        )
        self.assertTrue(
            {
                "chassis_core_04_frame_hardware",
                "chassis_core_05_placard_holder",
                "device_carrier_links",
                "device_wire_anchors",
            }
            <= ids
        )
        for item in plan:
            if item.source.name == "pocketforge-node-chassis.scad":
                self.assertEqual(
                    "dualbar_v1", item.parameters["CHASSIS_VARIANT"]
                )

    def test_brick_candidate_reuses_dualbar_core_with_new_optical_links(
        self,
    ) -> None:
        self.assertEqual(
            "unqualified",
            self.brick_profile.document["qualification"]["status"],
        )
        self.assertEqual("candidate", self.brick_layout.qualification["status"])
        self.assertEqual(
            "chassis-dualbar-brick-v1",
            self.brick_layout.supersedes_layout_id,
        )
        candidate = packs.all_device_layout_matrix(
            self.root, kind="candidate-layout-devices"
        )
        self.assertEqual(
            [
                {
                    "device_slug": "trimui-brick",
                    "layout_id": "chassis-dualbar-brick-v2",
                    "layout_status": "candidate",
                    "holder_status": "unqualified",
                },
                {
                    "device_slug": "trimui-smart-pro",
                    "layout_id": "chassis-core-v3",
                    "layout_status": "candidate",
                    "holder_status": "physically_qualified",
                },
                {
                    "device_slug": "trimui-smart-pro-s",
                    "layout_id": "chassis-dualbar-v2",
                    "layout_status": "candidate",
                    "holder_status": "physically_qualified",
                },
            ],
            candidate["include"],
        )
        plan = packs.build_plan(
            self.root,
            self.brick_profile,
            self.brick_layout,
            "trimui-brick",
            "full",
        )
        self.assertEqual(12, len(plan))
        retention = next(
            item for item in plan if item.artifact_id == "device_j_hook_set"
        )
        self.assertEqual("trimui-brick-cradle.scad", retention.source.name)
        self.assertEqual("hook_set", retention.part)
        links = next(
            item for item in plan if item.artifact_id == "device_carrier_links"
        )
        self.assertEqual(
            [packs.Decimal(180), packs.Decimal(205), packs.Decimal("3.2")],
            links.parameters["cradle_plate_size"],
        )
        self.assertEqual(
            [packs.Decimal(90), packs.Decimal("131.375")],
            links.parameters["cradle_screen_datum"],
        )
        self.assertEqual(
            [packs.Decimal(18), packs.Decimal(7)],
            links.parameters["cradle_slot_inset"],
        )
        self.assertEqual(
            "184fc37b03916a70f16b47753f83ec8404602dea4de0481620f36b5b2cd2e1d6",
            links.expected_normalized_sha256,
        )

        qualified_common = {
            item.artifact_id: item
            for item in self.dualbar_layout.artifacts
            if item.artifact_id != "device_carrier_links"
        }
        candidate_common = {
            item.artifact_id: item
            for item in self.brick_layout.artifacts
            if item.artifact_id != "device_carrier_links"
        }
        self.assertEqual(qualified_common, candidate_common)

    def test_device_slug_selects_exact_wrapper_and_label(self) -> None:
        pro = packs.build_plan(
            self.root,
            self.profile,
            self.layout,
            "trimui-smart-pro",
            "retrofit",
        )
        pro_s = packs.build_plan(
            self.root,
            self.profile,
            self.dualbar_layout,
            "trimui-smart-pro-s",
            "retrofit",
        )
        pro_carrier = next(item for item in pro if item.artifact_id == "device_carrier")
        pro_s_carrier = next(
            item for item in pro_s if item.artifact_id == "device_carrier"
        )
        self.assertEqual("trimui-smart-pro-cradle.scad", pro_carrier.source.name)
        self.assertEqual(
            "trimui-smart-pro-s-cradle.scad", pro_s_carrier.source.name
        )
        pro_nameplate = next(
            item for item in pro if item.artifact_id == "device_nameplate"
        )
        pro_s_nameplate = next(
            item for item in pro_s if item.artifact_id == "device_nameplate"
        )
        self.assertEqual(
            "TrimUI Smart Pro / TG5040",
            pro_nameplate.parameters["DEVICE_LABEL"],
        )
        self.assertEqual(
            "TrimUI Smart Pro S / TG5050",
            pro_s_nameplate.parameters["DEVICE_LABEL"],
        )

    def test_unknown_device_is_fail_closed(self) -> None:
        with self.assertRaisesRegex(packs.PackError, "is not mapped by profile"):
            packs.build_plan(
                self.root,
                self.profile,
                self.layout,
                "wrong-device",
                "coupon",
            )

    def test_custom_holder_escape_hatch_emits_only_a_prototype_pack(self) -> None:
        document = copy.deepcopy(self.profile.document)
        document["implementation"]["kind"] = "custom_openscad"
        document["qualification"]["status"] = "unqualified"
        custom = replace(self.profile, document=document)
        plan = packs.build_plan(
            self.root,
            custom,
            self.layout,
            "trimui-smart-pro",
            "retrofit",
        )
        self.assertIn(
            "device_j_hook_set", {item.artifact_id for item in plan}
        )
        with self.assertRaisesRegex(packs.PackError, "allow-unqualified"):
            packs._policy(
                custom,
                self.layout,
                "retrofit",
                packs.SourceState(commit="a" * 40, dirty=False),
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            custom,
            self.layout,
            "retrofit",
            packs.SourceState(commit="a" * 40, dirty=False),
            allow_dirty=False,
            allow_unqualified=True,
        )
        self.assertFalse(eligible)
        self.assertEqual(["allow_unqualified"], overrides)
        self.assertEqual(["holder_unqualified"], reasons)

    def _write_layout(self, document: dict[str, object]) -> Path:
        temp_root = Path(
            tempfile.mkdtemp(
                prefix=".layout-test-",
                dir=self.root / "mechanical" / "device-packs",
            )
        )
        self.addCleanup(lambda: packs.shutil.rmtree(temp_root))
        path = temp_root / "layout.json"
        path.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return path

    def test_layout_rejects_unknown_fields_and_path_escape(self) -> None:
        original = json.loads(self.layout_path.read_text(encoding="utf-8"))
        unknown = copy.deepcopy(original)
        unknown["surprise"] = True
        with self.assertRaisesRegex(packs.PackError, "unknown fields"):
            packs.load_layout(self.root, self._write_layout(unknown))

        escaped = copy.deepcopy(original)
        escaped["artifacts"][0]["output"] = "../escape.stl"
        with self.assertRaisesRegex(packs.PackError, "safe relative"):
            packs.load_layout(self.root, self._write_layout(escaped))

    def test_layout_qualification_is_strict_and_calendar_valid(self) -> None:
        original = json.loads(self.layout_path.read_text(encoding="utf-8"))

        impossible_date = copy.deepcopy(original)
        impossible_date["qualification"]["accepted_on"] = "2026-02-30"
        with self.assertRaisesRegex(packs.PackError, "real calendar date"):
            packs.load_layout(
                self.root, self._write_layout(impossible_date)
            )

        premature_acceptance = copy.deepcopy(original)
        premature_acceptance["qualification"]["status"] = "candidate"
        with self.assertRaisesRegex(
            packs.PackError, "must be null while candidate"
        ):
            packs.load_layout(
                self.root, self._write_layout(premature_acceptance)
            )

        duplicate_scope = copy.deepcopy(original)
        duplicate_scope["qualification"]["device_slugs"].append(
            "trimui-smart-pro"
        )
        with self.assertRaisesRegex(packs.PackError, "non-empty and unique"):
            packs.load_layout(
                self.root, self._write_layout(duplicate_scope)
            )

    def test_qualified_layout_guard_locks_and_stages_promotions(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pf-layout-head-"
        ) as head_temp, tempfile.TemporaryDirectory(
            prefix="pf-layout-base-"
        ) as base_temp:
            head = Path(head_temp)
            base = Path(base_temp)
            write_layout_guard_tree(head, status="physically_qualified")
            write_layout_guard_tree(base, status="physically_qualified")
            self.assertEqual(
                (1, 0, 0),
                packs.guard_qualified_layouts(head, base),
            )

            write_layout_guard_tree(
                head,
                status="physically_qualified",
                role="Changed after physical acceptance",
            )
            with self.assertRaisesRegex(
                packs.PackError, "qualified layout .* changed"
            ):
                packs.guard_qualified_layouts(head, base)

        with tempfile.TemporaryDirectory(
            prefix="pf-layout-head-"
        ) as head_temp, tempfile.TemporaryDirectory(
            prefix="pf-layout-base-"
        ) as base_temp:
            head = Path(head_temp)
            base = Path(base_temp)
            write_layout_guard_tree(head, status="physically_qualified")
            write_layout_guard_tree(base, status="candidate")
            self.assertEqual(
                (0, 1, 0),
                packs.guard_qualified_layouts(head, base),
            )

            write_layout_guard_tree(
                head,
                status="physically_qualified",
                role="Changed during promotion",
            )
            with self.assertRaisesRegex(
                packs.PackError, "changed its source contract"
            ):
                packs.guard_qualified_layouts(head, base)

        with tempfile.TemporaryDirectory(
            prefix="pf-layout-head-"
        ) as head_temp, tempfile.TemporaryDirectory(
            prefix="pf-layout-base-"
        ) as base_temp:
            head = Path(head_temp)
            base = Path(base_temp)
            write_layout_guard_tree(head, status="physically_qualified")
            (
                base
                / "mechanical"
                / "device-packs"
                / "layouts"
            ).mkdir(parents=True)
            with self.assertRaisesRegex(
                packs.PackError, "cannot begin as physically qualified"
            ):
                packs.guard_qualified_layouts(head, base)

    def test_qualified_layout_guard_allows_declared_candidate_successor(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pf-layout-head-"
        ) as head_temp, tempfile.TemporaryDirectory(
            prefix="pf-layout-base-"
        ) as base_temp:
            head = Path(head_temp)
            base = Path(base_temp)
            head_v1 = write_layout_guard_tree(
                head, status="physically_qualified"
            )
            write_layout_guard_tree(base, status="physically_qualified")

            successor = json.loads(head_v1.read_text(encoding="utf-8"))
            successor["layout_id"] = "demo-v2"
            successor["supersedes_layout_id"] = "demo-v1"
            successor["qualification"]["status"] = "candidate"
            successor["qualification"]["accepted_on"] = None
            successor_path = head_v1.with_name("demo-v2.json")
            successor_path.write_text(
                json.dumps(successor, indent=2) + "\n",
                encoding="utf-8",
            )
            registry_path = (
                head
                / "mechanical"
                / "device-packs"
                / "device-layouts.json"
            )
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["devices"]["device-demo"]["layout"] = (
                "mechanical/device-packs/layouts/demo-v2.json"
            )
            registry_path.write_text(
                json.dumps(registry, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                (1, 0, 0),
                packs.guard_qualified_layouts(head, base),
            )

            chained = copy.deepcopy(successor)
            chained["layout_id"] = "demo-v3"
            chained["supersedes_layout_id"] = "demo-v2"
            chained_path = head_v1.with_name("demo-v3.json")
            chained_path.write_text(
                json.dumps(chained, indent=2) + "\n",
                encoding="utf-8",
            )
            registry["devices"]["device-demo"]["layout"] = (
                "mechanical/device-packs/layouts/demo-v3.json"
            )
            registry_path.write_text(
                json.dumps(registry, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                (1, 0, 0),
                packs.guard_qualified_layouts(head, base),
            )

            chained.pop("supersedes_layout_id")
            chained_path.write_text(
                json.dumps(chained, indent=2) + "\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                packs.PackError, "proven device/layout mapping is immutable"
            ):
                packs.guard_qualified_layouts(head, base)

    def test_policy_requires_explicit_nonproduction_overrides(self) -> None:
        clean = packs.SourceState("a" * 40, False)
        dirty = packs.SourceState("a" * 40, True)
        eligible, overrides, reasons = packs._policy(
            self.profile,
            self.layout,
            "full",
            clean,
            allow_dirty=False,
            allow_unqualified=False,
        )
        self.assertTrue(eligible)
        self.assertEqual([], overrides)
        self.assertEqual([], reasons)

        with self.assertRaisesRegex(packs.PackError, "source tree is dirty"):
            packs._policy(
                self.profile,
                self.layout,
                "full",
                dirty,
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            self.profile,
            self.layout,
            "full",
            dirty,
            allow_dirty=True,
            allow_unqualified=False,
        )
        self.assertFalse(eligible)
        self.assertEqual(["allow_dirty"], overrides)
        self.assertEqual(["dirty_source"], reasons)

        document = copy.deepcopy(self.profile.document)
        document["qualification"]["status"] = "unqualified"
        unqualified = replace(
            self.profile,
            document=document,
            qualification_manifest=None,
        )
        with self.assertRaisesRegex(packs.PackError, "require physically qualified"):
            packs._policy(
                unqualified,
                self.layout,
                "retrofit",
                clean,
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            unqualified,
            self.layout,
            "retrofit",
            clean,
            allow_dirty=False,
            allow_unqualified=True,
        )
        self.assertFalse(eligible)
        self.assertEqual(["allow_unqualified"], overrides)
        self.assertEqual(["holder_unqualified"], reasons)

        eligible, overrides, reasons = packs._policy(
            unqualified,
            self.layout,
            "coupon",
            clean,
            allow_dirty=False,
            allow_unqualified=False,
        )
        self.assertFalse(eligible)
        self.assertEqual([], overrides)
        self.assertEqual(["coupon_only", "holder_unqualified"], reasons)

        candidate_qualification = copy.deepcopy(
            self.dualbar_layout.qualification
        )
        candidate_qualification["status"] = "candidate"
        candidate_qualification["accepted_on"] = None
        candidate_layout = replace(
            self.dualbar_layout,
            qualification=candidate_qualification,
        )
        with self.assertRaisesRegex(
            packs.PackError, "chassis layout"
        ):
            packs._policy(
                self.profile,
                candidate_layout,
                "full",
                clean,
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            self.profile,
            candidate_layout,
            "full",
            clean,
            allow_dirty=False,
            allow_unqualified=True,
        )
        self.assertFalse(eligible)
        self.assertEqual(["allow_unqualified"], overrides)
        self.assertEqual(["layout_unqualified"], reasons)

        with self.assertRaisesRegex(
            packs.PackError, "chassis layout"
        ):
            packs._policy(
                self.profile,
                candidate_layout,
                "retrofit",
                clean,
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            self.profile,
            candidate_layout,
            "retrofit",
            clean,
            allow_dirty=False,
            allow_unqualified=True,
        )
        self.assertFalse(eligible)
        self.assertEqual(["allow_unqualified"], overrides)
        self.assertEqual(["layout_unqualified"], reasons)

        eligible, overrides, reasons = packs._policy(
            self.profile,
            self.layout,
            "retrofit",
            clean,
            allow_dirty=False,
            allow_unqualified=False,
        )
        self.assertTrue(eligible)
        self.assertEqual([], overrides)
        self.assertEqual([], reasons)

    def _build_fake_pack(
        self, output: Path, *, replace_output: bool = False
    ) -> tuple[Path, packs.PlanItem]:
        real_item = packs.build_plan(
            self.root,
            self.profile,
            self.layout,
            "trimui-smart-pro",
            "coupon",
        )[0]
        test_item = replace(real_item, expected_normalized_sha256=None)
        with mock.patch.object(packs, "build_plan", return_value=(test_item,)):
            result = packs.build_pack(
                self.root,
                self.profile,
                self.layout,
                device_slug="trimui-smart-pro",
                mode="coupon",
                output=output,
                openscad="unused-openscad",
                replace=replace_output,
                allow_dirty=False,
                allow_unqualified=False,
                state=packs.SourceState("a" * 40, False),
                renderer=fake_renderer,
                contract_checker=no_contract_check,
            )
        return result, test_item

    def test_build_is_deterministic_atomic_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-pack-test-") as temp:
            root = Path(temp)
            first, _ = self._build_fake_pack(root / "first")
            second, _ = self._build_fake_pack(root / "second")
            self.assertEqual(
                (first / "manifest.json").read_bytes(),
                (second / "manifest.json").read_bytes(),
            )
            self.assertEqual(
                (first / "SHA256SUMS").read_bytes(),
                (second / "SHA256SUMS").read_bytes(),
            )
            before = (first / "manifest.json").read_bytes()
            with self.assertRaisesRegex(packs.PackError, "already exists"):
                self._build_fake_pack(first)
            self.assertEqual(before, (first / "manifest.json").read_bytes())
            self._build_fake_pack(first, replace_output=True)
            self.assertEqual(before, (first / "manifest.json").read_bytes())
            self.assertFalse(
                any(path.name.startswith(".first.stage-") for path in root.iterdir())
            )

            (first / "owner-note.txt").write_text("keep me", encoding="utf-8")
            with self.assertRaisesRegex(
                packs.PackError, "unrecognized directory membership"
            ):
                self._build_fake_pack(first, replace_output=True)
            self.assertEqual(
                "keep me",
                (first / "owner-note.txt").read_text(encoding="utf-8"),
            )

    def test_manifest_has_relative_hashed_inputs_and_no_machine_metadata(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-pack-test-") as temp:
            pack, _ = self._build_fake_pack(Path(temp) / "pack")
            document = json.loads((pack / "manifest.json").read_text())
            serialized = json.dumps(document, sort_keys=True)
            self.assertNotIn(str(self.root), serialized)
            self.assertNotIn(str(Path(temp)), serialized)
            self.assertNotIn("timestamp", serialized.lower())
            self.assertNotIn("generated_at", serialized.lower())
            self.assertTrue(document["inputs"])
            for source_input in document["inputs"]:
                self.assertFalse(Path(source_input["path"]).is_absolute())
                self.assertRegex(source_input["sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(packs.PACK_SCHEMA, document["schema"])
            qualification = document["qualification"]
            self.assertEqual(
                "mechanical/dut-cradle-v1/qualification/"
                "trimui-smart-pro-family-v1.json",
                qualification["manifest"]["path"],
            )
            self.assertRegex(
                qualification["manifest"]["sha256"], r"^[0-9a-f]{64}$"
            )
            self.assertEqual(
                qualification["accepted_geometry_revision"],
                qualification["accepted_source_revision"],
            )
            fixture = document["fixture"]
            self.assertEqual(
                "mechanical/dut-cradle-v1/profiles/fixture-locks/"
                "trimui-smart-pro-family-v1.json",
                fixture["lock"]["path"],
            )
            self.assertEqual(
                qualification["fixture_interface_sha256"],
                fixture["interface_sha256"],
            )
            self.assertRegex(
                fixture["platform_source"]["revision"], r"^[0-9a-f]{40}$"
            )
            layout = document["layout"]
            self.assertEqual(
                "physically_qualified",
                layout["qualification"]["status"],
            )
            self.assertEqual(
                ["trimui-smart-pro"],
                layout["qualification"]["device_slugs"],
            )

    def test_manifest_and_checksum_tampering_are_detected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-pack-test-") as temp:
            pack, item = self._build_fake_pack(Path(temp) / "pack")
            manifest = packs._read_pack_manifest(pack)
            header = {
                key: value for key, value in manifest.items() if key != "artifacts"
            }
            document = json.loads((pack / "manifest.json").read_text())
            document["device"]["display_name"] = "Tampered"
            (pack / "manifest.json").write_text(
                json.dumps(document, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                packs.PackError, "manifest metadata mismatch"
            ):
                packs._verify_materialized_pack(
                    self.root,
                    pack,
                    self.profile,
                    self.layout,
                    (item,),
                    expected_header=header,
                )

            document["device"]["display_name"] = "TrimUI Smart Pro / TG5040"
            (pack / "manifest.json").write_text(
                json.dumps(document, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            artifact_path = pack / item.output
            original_artifact = artifact_path.read_bytes()
            artifact_path.write_bytes(original_artifact + b"\n")
            with self.assertRaisesRegex(
                packs.PackError, "artifact metadata"
            ):
                packs._verify_materialized_pack(
                    self.root,
                    pack,
                    self.profile,
                    self.layout,
                    (item,),
                    expected_header=header,
                )
            artifact_path.write_bytes(original_artifact)

            (pack / "SHA256SUMS").write_text("0" * 64 + "  wrong.stl\n")
            with self.assertRaisesRegex(packs.PackError, "SHA256SUMS"):
                packs._verify_materialized_pack(
                    self.root,
                    pack,
                    self.profile,
                    self.layout,
                    (item,),
                    expected_header=header,
                )

    def test_normalized_geometry_lock_detects_drift(self) -> None:
        item = packs.build_plan(
            self.root,
            self.profile,
            self.layout,
            "trimui-smart-pro",
            "coupon",
        )[0]
        locked = replace(item, expected_normalized_sha256="0" * 64)
        with tempfile.TemporaryDirectory(prefix="pf-pack-test-") as temp:
            path = Path(temp) / "coupon.stl"
            fake_renderer(locked, path, "unused")
            with self.assertRaisesRegex(packs.PackError, "geometry drift"):
                packs._artifact_record(self.root, locked, path)

    def test_stl_serialization_normalizes_facet_order_and_start_vertex(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-pack-test-") as temp:
            first = Path(temp) / "first.stl"
            reordered = Path(temp) / "reordered.stl"
            first.write_text(TETRAHEDRON, encoding="ascii")
            points = packs.read_stl_points(first)
            facets = [
                tuple(points[offset : offset + 3])
                for offset in range(0, len(points), 3)
            ]
            lines = ["solid reordered\n"]
            for triangle in reversed(facets):
                rotated = (triangle[1], triangle[2], triangle[0])
                lines.extend(
                    [
                        "facet normal 9 8 7\n",
                        "outer loop\n",
                        *(
                            "vertex "
                            + " ".join(
                                packs._decimal_text(value) for value in point
                            )
                            + "\n"
                            for point in rotated
                        ),
                        "endloop\n",
                        "endfacet\n",
                    ]
                )
            lines.append("endsolid reordered\n")
            reordered.write_text("".join(lines), encoding="ascii")

            first_geometry = packs.describe_mesh(first)
            reordered_geometry = packs.describe_mesh(reordered)
            self.assertEqual(first_geometry, reordered_geometry)
            packs._canonicalize_stl(first)
            packs._canonicalize_stl(reordered)
            self.assertEqual(first.read_bytes(), reordered.read_bytes())
            self.assertEqual(first_geometry, packs.describe_mesh(first))

    def test_open_mesh_is_rejected_by_manifold_gate(self) -> None:
        item = replace(
            packs.build_plan(
                self.root,
                self.profile,
                self.layout,
                "trimui-smart-pro",
                "coupon",
            )[0],
            expected_normalized_sha256=None,
        )
        open_mesh = TETRAHEDRON.replace(
            """facet normal 1 1 1
  outer loop
    vertex 1 0 0
    vertex 0 1 0
    vertex 0 0 1
  endloop
endfacet
""",
            "",
        )
        with tempfile.TemporaryDirectory(prefix="pf-pack-test-") as temp:
            path = Path(temp) / "open.stl"
            path.write_text(open_mesh, encoding="ascii")
            with self.assertRaisesRegex(packs.PackError, "not closed"):
                packs._artifact_record(self.root, item, path)

    def test_output_guard_only_allows_generated_tree_inside_repo(self) -> None:
        allowed = (
            self.root
            / "mechanical"
            / "device-packs"
            / "build"
            / "trimui-smart-pro"
            / "coupon"
        )
        self.assertEqual(allowed, packs._safe_output(self.root, allowed))
        with self.assertRaisesRegex(packs.PackError, "below mechanical"):
            packs._safe_output(
                self.root,
                self.root / "mechanical" / "dut-cradle-v1" / "output",
            )

    def test_renderer_command_is_argv_with_stable_definitions(self) -> None:
        item = next(
            item
            for item in packs.build_plan(
                self.root,
                self.profile,
                self.layout,
                "trimui-smart-pro",
                "retrofit",
            )
            if item.artifact_id == "device_nameplate"
        )
        command = packs._command(item, Path("/tmp/nameplate.stl"), "openscad")
        self.assertIsInstance(command, list)
        self.assertIn('DEVICE_LABEL="TrimUI Smart Pro / TG5040"', command)
        definitions = [
            command[index + 1]
            for index, value in enumerate(command[:-1])
            if value == "-D"
        ]
        self.assertEqual(sorted(definitions), definitions)


if __name__ == "__main__":
    unittest.main(verbosity=2)
