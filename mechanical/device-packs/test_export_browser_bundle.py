#!/usr/bin/env python3
"""Regression tests for the source-only browser generation bundle."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import build_device_pack
import export_browser_bundle
import holder_profiles


ROOT = Path(__file__).resolve().parents[2]
CLEAN_STATE = build_device_pack.SourceState(
    commit="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)
DIRTY_STATE = build_device_pack.SourceState(
    commit="0123456789abcdef0123456789abcdef01234567",
    dirty=True,
)


class BrowserBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, cls.sources = export_browser_bundle.build_catalog(
            ROOT, state=CLEAN_STATE
        )

    def test_catalog_covers_registry_through_authoritative_build_plans(
        self,
    ) -> None:
        registry = build_device_pack.load_layout_registry(
            ROOT, ROOT / build_device_pack.DEFAULT_LAYOUT_REGISTRY
        )
        devices = {device["slug"]: device for device in self.catalog["devices"]}
        self.assertEqual(set(registry), set(devices))
        self.assertEqual(
            list(build_device_pack.MODES), self.catalog["modes"]
        )

        cradle_root = ROOT / "mechanical" / "dut-cradle-v1"
        profiles = [
            holder_profiles.validate_profile(cradle_root, path)
            for path in holder_profiles.discover_profiles(cradle_root)
        ]
        profile_by_device = {
            slug: profile
            for profile in profiles
            for slug in profile.variants
        }
        for slug, device in devices.items():
            profile = profile_by_device[slug]
            layout = build_device_pack.resolve_device_layout(ROOT, slug)
            self.assertEqual(layout.layout_id, device["layout"]["id"])
            for mode in build_device_pack.MODES:
                expected = build_device_pack.build_plan(
                    ROOT, profile, layout, slug, mode
                )
                actual = device["modes"][mode]["artifacts"]
                self.assertEqual(
                    [item.artifact_id for item in expected],
                    [item["id"] for item in actual],
                )
                self.assertEqual(
                    [item.output.as_posix() for item in expected],
                    [item["output"] for item in actual],
                )
                for plan_item, artifact in zip(
                    expected, actual, strict=True
                ):
                    self.assertEqual(
                        build_device_pack._definitions(
                            plan_item.parameters
                        ),
                        {
                            row["name"]: row["literal"]
                            for row in artifact["definitions"]
                        },
                    )

    def test_catalog_bytes_are_deterministic(self) -> None:
        repeated, repeated_sources = export_browser_bundle.build_catalog(
            ROOT, state=CLEAN_STATE
        )
        self.assertEqual(self.catalog, repeated)
        self.assertEqual(self.sources, repeated_sources)
        self.assertEqual(
            export_browser_bundle._json_bytes(self.catalog),
            export_browser_bundle._json_bytes(repeated),
        )

    def test_bundle_contains_only_catalog_checksums_and_hashed_scad(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "browser"
            export_browser_bundle.write_bundle(
                ROOT, output, state=CLEAN_STATE
            )
            verified = export_browser_bundle.verify_bundle(
                output, expected_catalog=self.catalog
            )
            self.assertEqual(self.catalog, verified)
            members = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file()
            }
            self.assertIn("catalog.json", members)
            self.assertIn("SHA256SUMS", members)
            self.assertTrue(
                all(
                    path in {"catalog.json", "SHA256SUMS"}
                    or (
                        path.startswith("sources/")
                        and path.endswith(".scad")
                    )
                    for path in members
                )
            )
            self.assertFalse(any(path.endswith(".stl") for path in members))

    def test_fixture_sources_and_full_only_artifacts_are_complete(
        self,
    ) -> None:
        expected_fixture_sources = {
            "mechanical/dut-fixture-v1/alientek-dp100.scad",
            "mechanical/dut-fixture-v1/bpi-m2-zero-v1.scad",
            "mechanical/dut-fixture-v1/ceksezx-mtsd001.scad",
            "mechanical/dut-fixture-v1/dut-fixture.scad",
            "mechanical/dut-fixture-v1/eightwood-ewua0205.scad",
            "mechanical/dut-fixture-v1/elegoo-4-channel-relay.scad",
            "mechanical/dut-fixture-v1/esp32-s3-supermini-hw747-v0.0.2.scad",
            "mechanical/dut-fixture-v1/hiletgo-xl6009.scad",
            "mechanical/dut-fixture-v1/logitech-c270.scad",
            "mechanical/dut-fixture-v1/smays-microb-hub-8152.scad",
            "mechanical/dut-fixture-v1/vienon-usb-001.scad",
        }
        actual_fixture_sources = {
            item["path"]
            for item in self.catalog["sources"]
            if item["path"].startswith("mechanical/dut-fixture-v1/")
        }
        self.assertEqual(expected_fixture_sources, actual_fixture_sources)

        expected_artifacts = {
            "fixture_dut_plate": {
                "output": "fixture/dut-fixture-plate.stl",
                "definitions": {
                    "PART": '\"plate\"',
                    "SHOW_COMPONENTS": "false",
                },
            },
            "fixture_dut_fit_coupon": {
                "output": "fixture/dut-fixture-fit-coupon.stl",
                "definitions": {
                    "PART": '\"fit_coupon\"',
                    "SHOW_COMPONENTS": "false",
                },
            },
        }
        for device in self.catalog["devices"]:
            with self.subTest(device=device["slug"]):
                modes = device["modes"]
                self.assertEqual(
                    {"coupon": 1, "retrofit": 7, "full": 15},
                    {
                        mode: len(record["artifacts"])
                        for mode, record in modes.items()
                    },
                )
                for mode in ("coupon", "retrofit"):
                    self.assertTrue(
                        set(expected_artifacts).isdisjoint(
                            artifact["id"]
                            for artifact in modes[mode]["artifacts"]
                        )
                    )

                full = {
                    artifact["id"]: artifact
                    for artifact in modes["full"]["artifacts"]
                }
                bracket = full["chassis_usb_c_interrupter_bracket"]
                self.assertEqual(
                    "chassis/dual-usb-c-interrupter-rail-bracket.stl",
                    bracket["output"],
                )
                self.assertEqual(
                    "7c98e46e5ae0435803df79b7d8a0902632c83192047d51635823237d3b584f8a",
                    bracket["expected_normalized_sha256"],
                )
                self.assertIn(
                    "mechanical/dut-chassis-2020-v1/lib/usb-c-interrupter-bracket.scad",
                    {source["path"] for source in self.catalog["sources"]},
                )
                self.assertTrue(set(expected_artifacts) <= set(full))
                for artifact_id, contract in expected_artifacts.items():
                    artifact = full[artifact_id]
                    self.assertEqual(contract["output"], artifact["output"])
                    self.assertEqual(
                        "mechanical/dut-fixture-v1/dut-fixture.scad",
                        artifact["source"],
                    )
                    self.assertEqual(
                        contract["definitions"],
                        {
                            row["name"]: row["literal"]
                            for row in artifact["definitions"]
                        },
                    )
                    self.assertEqual("PETG", artifact["print"]["material"])
                    self.assertIsNone(
                        artifact["expected_normalized_sha256"]
                    )
                self.assertTrue(
                    all(
                        not definition["literal"]
                        .strip('\"')
                        .startswith("presentation")
                        and definition["literal"].strip('\"')
                        not in {"plate_lower", "plate_upper", "joiner"}
                        for artifact in full.values()
                        for definition in artifact["definitions"]
                        if definition["name"] == "PART"
                    )
                )

    def test_source_tampering_fails_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "browser"
            export_browser_bundle.write_bundle(
                ROOT, output, state=CLEAN_STATE
            )
            source = next((output / "sources").rglob("*.scad"))
            source.write_bytes(source.read_bytes() + b"\n// tampered\n")
            with self.assertRaisesRegex(
                export_browser_bundle.BrowserBundleError,
                "source (size|hash) changed",
            ):
                export_browser_bundle.verify_bundle(output)

    def test_catalog_rejects_source_path_escape_and_duplicate_device(
        self,
    ) -> None:
        escaped = copy.deepcopy(self.catalog)
        escaped["sources"][0]["path"] = "../outside.scad"
        with self.assertRaisesRegex(
            export_browser_bundle.BrowserBundleError,
            "safe relative path",
        ):
            export_browser_bundle.validate_catalog(escaped)

        duplicated = copy.deepcopy(self.catalog)
        duplicated["devices"].append(
            copy.deepcopy(duplicated["devices"][0])
        )
        with self.assertRaisesRegex(
            export_browser_bundle.BrowserBundleError,
            "slug is duplicated",
        ):
            export_browser_bundle.validate_catalog(duplicated)

    def test_qualified_and_dirty_policy_are_preserved(self) -> None:
        clean_by_slug = {
            device["slug"]: device for device in self.catalog["devices"]
        }
        pro_full = clean_by_slug["trimui-smart-pro"]["modes"]["full"]
        self.assertFalse(pro_full["production_eligible"])
        self.assertEqual(
            ["layout_unqualified"], pro_full["nonproduction_reasons"]
        )
        self.assertEqual(
            ["allow_unqualified"], pro_full["required_overrides"]
        )
        pro_s_full = clean_by_slug["trimui-smart-pro-s"]["modes"]["full"]
        self.assertFalse(pro_s_full["production_eligible"])
        self.assertEqual(
            ["layout_unqualified"], pro_s_full["nonproduction_reasons"]
        )
        self.assertEqual(
            ["allow_unqualified"], pro_s_full["required_overrides"]
        )

        brick = clean_by_slug["trimui-brick"]
        brick_full = brick["modes"]["full"]
        self.assertFalse(brick_full["production_eligible"])
        self.assertEqual(
            ["holder_unqualified", "layout_unqualified"],
            brick_full["nonproduction_reasons"],
        )
        self.assertEqual(
            ["allow_unqualified"], brick_full["required_overrides"]
        )
        self.assertEqual(
            ["coupon_only", "holder_unqualified"],
            brick["modes"]["coupon"]["nonproduction_reasons"],
        )

        dirty, _ = export_browser_bundle.build_catalog(
            ROOT, state=DIRTY_STATE
        )
        for device in dirty["devices"]:
            for mode in device["modes"].values():
                self.assertFalse(mode["production_eligible"])
                self.assertIn(
                    "dirty_source", mode["nonproduction_reasons"]
                )

    def test_serialized_catalog_round_trips_strict_validation(self) -> None:
        restored = json.loads(
            export_browser_bundle._json_bytes(self.catalog)
        )
        export_browser_bundle.validate_catalog(restored)
        self.assertEqual(self.catalog, restored)


if __name__ == "__main__":
    unittest.main()
