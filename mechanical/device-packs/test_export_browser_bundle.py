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

    def test_candidate_and_dirty_policy_are_preserved(self) -> None:
        clean_by_slug = {
            device["slug"]: device for device in self.catalog["devices"]
        }
        self.assertTrue(
            clean_by_slug["trimui-smart-pro"]["modes"]["full"][
                "production_eligible"
            ]
        )
        pro_s_full = clean_by_slug["trimui-smart-pro-s"]["modes"]["full"]
        self.assertFalse(pro_s_full["production_eligible"])
        self.assertEqual(
            ["layout_unqualified"], pro_s_full["nonproduction_reasons"]
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
