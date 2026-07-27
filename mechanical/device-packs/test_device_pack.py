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
        for artifact in self.layout.artifacts:
            with self.subTest(artifact=artifact.artifact_id):
                if artifact.parameter_bindings:
                    self.assertEqual("device_nameplate", artifact.artifact_id)
                    self.assertIsNone(artifact.expected_normalized_sha256)
                else:
                    self.assertRegex(
                        artifact.expected_normalized_sha256 or "",
                        r"^[0-9a-f]{64}$",
                    )

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
            self.layout,
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
        self.assertEqual("TrimUI Smart Pro", pro_nameplate.parameters["DEVICE_LABEL"])
        self.assertEqual(
            "TrimUI Smart Pro S", pro_s_nameplate.parameters["DEVICE_LABEL"]
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

    def test_custom_holder_escape_hatch_cannot_emit_a_pack(self) -> None:
        document = copy.deepcopy(self.profile.document)
        document["implementation"]["kind"] = "custom_openscad"
        custom = replace(self.profile, document=document)
        with self.assertRaisesRegex(
            packs.PackError,
            "require a declarative reusable holder mechanism",
        ):
            packs.build_plan(
                self.root,
                custom,
                self.layout,
                "trimui-smart-pro",
                "coupon",
            )

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

    def test_policy_requires_explicit_nonproduction_overrides(self) -> None:
        clean = packs.SourceState("a" * 40, False)
        dirty = packs.SourceState("a" * 40, True)
        eligible, overrides, reasons = packs._policy(
            self.profile,
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
                "full",
                dirty,
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            self.profile,
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
                "retrofit",
                clean,
                allow_dirty=False,
                allow_unqualified=False,
            )
        eligible, overrides, reasons = packs._policy(
            unqualified,
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
            "coupon",
            clean,
            allow_dirty=False,
            allow_unqualified=False,
        )
        self.assertFalse(eligible)
        self.assertEqual([], overrides)
        self.assertEqual(["coupon_only", "holder_unqualified"], reasons)

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

            document["device"]["display_name"] = "TrimUI Smart Pro"
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
        self.assertIn('DEVICE_LABEL="TrimUI Smart Pro"', command)
        definitions = [
            command[index + 1]
            for index, value in enumerate(command[:-1])
            if value == "-D"
        ]
        self.assertEqual(sorted(definitions), definitions)


if __name__ == "__main__":
    unittest.main(verbosity=2)
