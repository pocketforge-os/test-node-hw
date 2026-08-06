#!/usr/bin/env python3
"""Tests for deterministic print-pack release bundles and publication."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
import zipfile
from dataclasses import replace
from pathlib import Path
from unittest import mock

import publish_print_pack as publisher
import release_print_pack as releases


COMMIT = "a" * 40
PROFILE_ID = "trimui-smart-pro-family"
DEVICE_SLUGS = ("trimui-smart-pro", "trimui-smart-pro-s")


def write_json(path: Path, value: object) -> None:
    path.write_bytes(releases._json_bytes(value))


def minimal_pack(path: Path, slug: str) -> dict[str, object]:
    path.mkdir(parents=True)
    document: dict[str, object] = {
        "schema": releases.packs.PACK_SCHEMA,
        "device": {
            "slug": slug,
            "display_name": slug.replace("-", " ").title(),
        },
        "mode": "full",
        "profile": {
            "id": PROFILE_ID,
            "path": (
                "mechanical/dut-cradle-v1/profiles/"
                "trimui-smart-pro-family.json"
            ),
            "sha256": "b" * 64,
        },
        "qualification": {
            "status": "physically_qualified",
            "manifest_status": "physically_accepted",
            "manifest": {
                "path": (
                    "mechanical/dut-cradle-v1/qualification/"
                    "trimui-smart-pro-family-v1.json"
                ),
                "sha256": "c" * 64,
                "schema": "pocketforge-qualified-geometry-v1",
            },
        },
        "fixture": {
            "interface_sha256": "d" * 64,
            "lock": {"sha256": "e" * 64},
        },
        "layout": {"id": "chassis-core-v1", "sha256": "f" * 64},
        "source": {
            "repository": releases.packs.REPOSITORY_URL,
            "commit": COMMIT,
            "dirty": False,
        },
        "toolchain": {
            "lock_sha256": "1" * 64,
            "openscad_reported_version": "OpenSCAD version 2021.01",
        },
        "production_eligible": True,
        "nonproduction_reasons": [],
        "overrides": [],
        "artifacts": [],
    }
    write_json(path / "manifest.json", document)
    (path / "SHA256SUMS").write_bytes(b"")
    return document


def no_pack_verify(root: Path, pack: Path) -> None:
    del root, pack


class ReleaseArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = releases.packs.REPO_ROOT
        cls.profile = releases.resolve_profile(cls.root, PROFILE_ID)
        cls.identity = releases.release_identity(cls.profile)

    def test_qualification_manifest_defines_stable_release_identity(self) -> None:
        self.assertEqual(
            "print-pack-trimui-smart-pro-family-v2",
            self.identity.tag,
        )
        self.assertEqual(2, self.identity.version)
        self.assertEqual(
            "trimui-smart-pro-family-v2.json",
            self.identity.qualification_path.name,
        )
        self.assertTrue(self.identity.uses_release_qualification)
        legacy = releases.release_identity(self.profile, 1)
        self.assertEqual("print-pack-trimui-smart-pro-family-v1", legacy.tag)
        self.assertEqual(
            "trimui-smart-pro-family-v1.json",
            legacy.qualification_path.name,
        )
        self.assertFalse(legacy.uses_release_qualification)
        future_holder = replace(
            legacy,
            version=2,
            tag="print-pack-trimui-smart-pro-family-v2",
        )
        self.assertEqual(
            releases.RELEASE_SCHEMA_V1,
            releases._release_schema(future_holder),
        )

    def test_release_uses_bound_layouts_despite_candidate_registry(self) -> None:
        registered = {
            slug: releases.packs.resolve_device_layout(self.root, slug)
            for slug in DEVICE_SLUGS
        }
        bound = releases._release_layouts(
            self.root, self.profile, self.identity
        )
        self.assertEqual(
            {
                "trimui-smart-pro": "chassis-dualbar-smart-pro-v2",
                "trimui-smart-pro-s": "chassis-dualbar-v3",
            },
            {slug: layout.layout_id for slug, layout in registered.items()},
        )
        self.assertEqual(
            {
                "trimui-smart-pro": "chassis-core-v2",
                "trimui-smart-pro-s": "chassis-dualbar-v1",
            },
            {slug: layout.layout_id for slug, layout in bound.items()},
        )
        self.assertTrue(
            all(
                layout.qualification["status"] == "physically_qualified"
                for layout in bound.values()
            )
        )

    def test_future_holder_v2_schema_v1_rejects_mixed_layouts_early(
        self,
    ) -> None:
        legacy = releases.release_identity(self.profile, 1)
        future_holder = replace(
            legacy,
            version=2,
            tag="print-pack-trimui-smart-pro-family-v2",
        )
        qualified = releases._release_layouts(
            self.root, self.profile, self.identity
        )

        def layout_for(root: Path, slug: str):
            del root
            return qualified[slug]

        with tempfile.TemporaryDirectory(prefix="pf-release-test-") as temp:
            with mock.patch.object(
                releases.packs,
                "source_state",
                return_value=releases.packs.SourceState(COMMIT, False),
            ), mock.patch.object(
                releases, "release_identity", return_value=future_holder
            ), mock.patch.object(
                releases.packs,
                "resolve_device_layout",
                side_effect=layout_for,
            ):
                with self.assertRaisesRegex(
                    releases.ReleaseError,
                    "release schema v1 cannot encode mixed per-device chassis "
                    "layouts",
                ):
                    releases.build_release_bundle(
                        self.root,
                        profile_id=PROFILE_ID,
                        output=Path(temp) / future_holder.tag,
                        openscad="unused-openscad",
                        replace=False,
                    )

    def test_canonical_archives_are_byte_identical_and_verifiable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-release-test-") as temp:
            root = Path(temp)
            first_pack = root / "first-pack"
            second_pack = root / "second-pack"
            minimal_pack(first_pack, DEVICE_SLUGS[0])
            minimal_pack(second_pack, DEVICE_SLUGS[0])
            first = root / "first.zip"
            second = root / "second.zip"
            archive_root = f"device-pack-{DEVICE_SLUGS[0]}"
            releases._write_archive(first_pack, first, archive_root)
            releases._write_archive(second_pack, second, archive_root)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            manifest = releases._verify_archive(
                self.root,
                first,
                device_slug=DEVICE_SLUGS[0],
                pack_verifier=no_pack_verify,
            )
            self.assertTrue(manifest["production_eligible"])

    def test_archive_rejects_traversal_and_noncanonical_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-release-test-") as temp:
            root = Path(temp)
            traversal = root / "traversal.zip"
            with zipfile.ZipFile(traversal, "w") as output:
                info = zipfile.ZipInfo("../escape", releases.ZIP_TIMESTAMP)
                info.create_system = 3
                info.external_attr = releases.ZIP_FILE_MODE << 16
                output.writestr(info, b"escape")
            with self.assertRaisesRegex(releases.ReleaseError, "safe relative"):
                releases._verify_archive(
                    self.root,
                    traversal,
                    device_slug=DEVICE_SLUGS[0],
                    pack_verifier=no_pack_verify,
                )

            pack = root / "pack"
            minimal_pack(pack, DEVICE_SLUGS[0])
            noncanonical = root / "noncanonical.zip"
            member_root = f"device-pack-{DEVICE_SLUGS[0]}"
            with zipfile.ZipFile(noncanonical, "w") as output:
                for path in sorted(pack.iterdir()):
                    info = zipfile.ZipInfo(
                        f"{member_root}/{path.name}",
                        (2026, 1, 1, 0, 0, 0),
                    )
                    info.create_system = 3
                    info.external_attr = releases.ZIP_FILE_MODE << 16
                    output.writestr(info, path.read_bytes())
            with self.assertRaisesRegex(
                releases.ReleaseError, "metadata is noncanonical"
            ):
                releases._verify_archive(
                    self.root,
                    noncanonical,
                    device_slug=DEVICE_SLUGS[0],
                    pack_verifier=no_pack_verify,
                )

    def test_archive_rejects_nonproduction_and_wrong_device(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-release-test-") as temp:
            root = Path(temp)
            pack = root / "pack"
            document = minimal_pack(pack, DEVICE_SLUGS[0])
            document["production_eligible"] = False
            write_json(pack / "manifest.json", document)
            archive = root / "pack.zip"
            releases._write_archive(
                pack, archive, f"device-pack-{DEVICE_SLUGS[0]}"
            )
            with self.assertRaisesRegex(
                releases.ReleaseError, "not an unmodified production"
            ):
                releases._verify_archive(
                    self.root,
                    archive,
                    device_slug=DEVICE_SLUGS[0],
                    pack_verifier=no_pack_verify,
                )

            document["production_eligible"] = True
            document["device"]["slug"] = DEVICE_SLUGS[1]
            write_json(pack / "manifest.json", document)
            releases._write_archive(
                pack, archive, f"device-pack-{DEVICE_SLUGS[0]}"
            )
            with self.assertRaisesRegex(
                releases.ReleaseError, "wrong device identity"
            ):
                releases._verify_archive(
                    self.root,
                    archive,
                    device_slug=DEVICE_SLUGS[0],
                    pack_verifier=no_pack_verify,
                )

    def _bundle(self, root: Path) -> Path:
        bundle = root / self.identity.tag
        bundle.mkdir()
        archive_records = []
        source_pack = None
        archive_names = []
        release_layouts = releases._release_layouts(
            self.root, self.profile, self.identity
        )
        for slug in DEVICE_SLUGS:
            pack = root / f"pack-{slug}"
            manifest = minimal_pack(pack, slug)
            # The release profile hash must represent the real committed input.
            manifest["profile"]["sha256"] = releases._sha256(self.profile.path)
            layout = release_layouts[slug]
            manifest["layout"] = {
                "id": layout.layout_id,
                "path": releases._relative(self.root, layout.path),
                "sha256": releases._sha256(layout.path),
                "qualification": copy.deepcopy(layout.qualification),
            }
            write_json(pack / "manifest.json", manifest)
            name = releases.archive_name(slug)
            archive = bundle / name
            releases._write_archive(pack, archive, f"device-pack-{slug}")
            archive_records.append(
                releases._archive_record(
                    archive, slug, manifest, include_layout=True
                )
            )
            archive_names.append(name)
            source_pack = source_pack or manifest
        assert source_pack is not None
        document = releases._release_document(
            self.root,
            self.identity,
            self.profile,
            source_pack,
            archive_records,
        )
        write_json(bundle / releases.RELEASE_MANIFEST_NAME, document)
        releases._write_release_checksums(bundle, archive_names)
        return bundle

    def test_complete_bundle_verifies_and_checksum_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-release-test-") as temp:
            bundle = self._bundle(Path(temp))
            with mock.patch.object(
                releases.packs,
                "source_state",
                return_value=releases.packs.SourceState(COMMIT, False),
            ):
                document = releases.verify_release_bundle(
                    self.root,
                    bundle,
                    pack_verifier=no_pack_verify,
                )
            self.assertEqual(self.identity.tag, document["tag"])

            (bundle / releases.RELEASE_CHECKSUM_NAME).write_text(
                f"{'0' * 64}  {releases.RELEASE_MANIFEST_NAME}\n",
                encoding="utf-8",
            )
            with mock.patch.object(
                releases.packs,
                "source_state",
                return_value=releases.packs.SourceState(COMMIT, False),
            ), self.assertRaisesRegex(
                releases.ReleaseError, "SHA256SUMS"
            ):
                releases.verify_release_bundle(
                    self.root,
                    bundle,
                    pack_verifier=no_pack_verify,
                )


class FakeGitHub:
    repository = publisher.DEFAULT_REPOSITORY

    def __init__(self) -> None:
        self.enabled = True
        self.release: dict[str, object] | None = None
        self.remote_assets: list[dict[str, object]] = []
        self.payloads: dict[str, bytes] = {}
        self.orphan_tag = False
        self.upload_count = 0
        self.publish_count = 0
        self.setting_checks = 0
        self.variables: dict[str, str] = {}

    def immutable_setting(self) -> dict[str, object]:
        self.setting_checks += 1
        return {"enabled": self.enabled}

    def set_actions_variable(self, name: str, value: str) -> None:
        self.variables[name] = value

    def release_by_tag(self, tag: str) -> dict[str, object] | None:
        if self.release is None or self.release["tag_name"] != tag:
            return None
        return copy.deepcopy(self.release)

    def tag_ref(self, tag: str) -> dict[str, object] | None:
        del tag
        return {"ref": "refs/tags/orphan"} if self.orphan_tag else None

    def create_draft(
        self,
        *,
        tag: str,
        commit: str,
        title: str,
        body: str,
    ) -> dict[str, object]:
        self.release = {
            "id": 7,
            "tag_name": tag,
            "target_commitish": commit,
            "name": title,
            "body": body,
            "draft": True,
            "prerelease": False,
            "immutable": False,
        }
        return copy.deepcopy(self.release)

    def release_assets(self, release_id: int) -> list[dict[str, object]]:
        self.assert_release_id(release_id)
        return copy.deepcopy(self.remote_assets)

    def upload_asset(
        self, release_id: int, asset: publisher.Asset
    ) -> dict[str, object]:
        self.assert_release_id(release_id)
        self.upload_count += 1
        url = f"https://github.com/fake/releases/download/tag/{asset.name}"
        self.payloads[url] = asset.path.read_bytes()
        remote = {
            "id": 100 + self.upload_count,
            "name": asset.name,
            "size": asset.size_bytes,
            "digest": f"sha256:{asset.sha256}",
            "browser_download_url": url,
        }
        self.remote_assets.append(remote)
        return copy.deepcopy(remote)

    def publish_release(self, release_id: int) -> dict[str, object]:
        self.assert_release_id(release_id)
        assert self.release is not None
        self.publish_count += 1
        self.release["draft"] = False
        self.release["immutable"] = True
        return copy.deepcopy(self.release)

    def resolved_commit(self, ref: str) -> str:
        if ref == "main":
            return COMMIT
        assert self.release is not None
        self.assertEqual(ref, self.release["tag_name"])
        return str(self.release["target_commitish"])

    def download_public_asset(self, url: str) -> bytes:
        return self.payloads[url]

    def assert_release_id(self, release_id: int) -> None:
        if release_id != 7:
            raise AssertionError(f"unexpected release ID: {release_id}")

    def assertEqual(self, first: object, second: object) -> None:
        if first != second:
            raise AssertionError(f"{first!r} != {second!r}")


class PublisherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = releases.packs.REPO_ROOT
        cls.profile = releases.resolve_profile(cls.root, PROFILE_ID)
        cls.identity = releases.release_identity(cls.profile)

    def _bundle(self, root: Path) -> tuple[Path, dict[str, object]]:
        bundle = root / "bundle"
        bundle.mkdir()
        devices = []
        for slug in DEVICE_SLUGS:
            name = releases.archive_name(slug)
            payload = f"archive:{slug}\n".encode()
            (bundle / name).write_bytes(payload)
            devices.append(
                {
                    "device_slug": slug,
                    "archive": {
                        "name": name,
                        "sha256": hashlib.sha256(payload).hexdigest(),
                        "size_bytes": len(payload),
                    },
                }
            )
        manifest: dict[str, object] = {
            "schema": releases.RELEASE_SCHEMA,
            "tag": self.identity.tag,
            "title": releases.release_title(self.identity),
            "profile": {"id": PROFILE_ID},
            "qualification": {"status": "physically_qualified"},
            "source": {
                "repository": releases.packs.REPOSITORY_URL,
                "commit": COMMIT,
                "dirty": False,
            },
            "devices": devices,
        }
        write_json(bundle / releases.RELEASE_MANIFEST_NAME, manifest)
        (bundle / releases.RELEASE_CHECKSUM_NAME).write_bytes(b"checksums\n")
        return bundle, manifest

    def test_publish_is_draft_first_verified_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-publisher-test-") as temp:
            bundle, manifest = self._bundle(Path(temp))
            client = FakeGitHub()
            verifier = lambda root, path: manifest
            tag = publisher.publish_bundle(
                self.root,
                bundle,
                client,
                bundle_verifier=verifier,
                sleeper=lambda seconds: None,
            )
            self.assertEqual(self.identity.tag, tag)
            self.assertEqual(4, client.upload_count)
            self.assertEqual(1, client.publish_count)
            self.assertTrue(client.release["immutable"])

            # GitHub designates the repository's only published full release
            # as latest even when both mutations requested make_latest=false.
            # That moving repository pointer is not part of release identity.
            client.release["isLatest"] = True
            publisher.publish_bundle(
                self.root,
                bundle,
                client,
                bundle_verifier=verifier,
                sleeper=lambda seconds: None,
            )
            self.assertEqual(4, client.upload_count)
            self.assertEqual(1, client.publish_count)

    def test_release_mutations_never_request_the_latest_designation(
        self,
    ) -> None:
        client = publisher.GitHubClient(
            publisher.DEFAULT_REPOSITORY, "test-token"
        )
        calls: list[
            tuple[str, str, dict[str, object] | None]
        ] = []

        def fake_api(
            method: str,
            path: str,
            document: dict[str, object] | None = None,
        ) -> dict[str, object]:
            calls.append((method, path, copy.deepcopy(document)))
            return {"id": 7}

        with mock.patch.object(client, "_api", side_effect=fake_api):
            client.create_draft(
                tag=self.identity.tag,
                commit=COMMIT,
                title=releases.release_title(self.identity),
                body=releases.release_body(self.identity, COMMIT),
            )
            client.publish_release(7)

        self.assertEqual(2, len(calls))
        draft_document = calls[0][2]
        publish_document = calls[1][2]
        self.assertIsNotNone(draft_document)
        self.assertIsNotNone(publish_document)
        assert draft_document is not None
        assert publish_document is not None
        self.assertEqual("false", draft_document["make_latest"])
        self.assertEqual("false", publish_document["make_latest"])
        self.assertTrue(draft_document["draft"])
        self.assertFalse(publish_document["draft"])

    def test_short_lived_admin_proof_is_exact_and_skips_admin_api(self) -> None:
        now = publisher.dt.datetime(
            2026, 7, 27, 0, 0, tzinfo=publisher.dt.timezone.utc
        )
        proof = publisher.create_immutability_proof(
            repository=publisher.DEFAULT_REPOSITORY,
            tag=self.identity.tag,
            commit=COMMIT,
            now=now,
        )
        document = publisher.validate_immutability_proof(
            proof,
            repository=publisher.DEFAULT_REPOSITORY,
            tag=self.identity.tag,
            commit=COMMIT,
            now=now + publisher.dt.timedelta(minutes=1),
        )
        self.assertTrue(document["enabled"])
        with self.assertRaisesRegex(
            publisher.PublishError, "commit does not match"
        ):
            publisher.validate_immutability_proof(
                proof,
                repository=publisher.DEFAULT_REPOSITORY,
                tag=self.identity.tag,
                commit="b" * 40,
                now=now,
            )
        with self.assertRaisesRegex(publisher.PublishError, "expired"):
            publisher.validate_immutability_proof(
                proof,
                repository=publisher.DEFAULT_REPOSITORY,
                tag=self.identity.tag,
                commit=COMMIT,
                now=now + publisher.dt.timedelta(hours=1),
            )

        with tempfile.TemporaryDirectory(prefix="pf-publisher-test-") as temp:
            bundle, manifest = self._bundle(Path(temp))
            client = FakeGitHub()
            client.enabled = False
            publisher.publish_bundle(
                self.root,
                bundle,
                client,
                bundle_verifier=lambda root, path: manifest,
                sleeper=lambda seconds: None,
                immutability_proof=proof,
                now=now,
            )
            self.assertEqual(0, client.setting_checks)
            self.assertEqual(1, client.publish_count)

    def test_authorization_checks_live_setting_and_remote_main(self) -> None:
        now = publisher.dt.datetime(
            2026, 7, 27, 0, 0, tzinfo=publisher.dt.timezone.utc
        )
        client = FakeGitHub()
        with mock.patch.object(
            releases.packs,
            "source_state",
            return_value=releases.packs.SourceState(COMMIT, False),
        ):
            document = publisher.authorize_workflow(
                self.root,
                PROFILE_ID,
                client,
                now=now,
            )
        self.assertEqual(1, client.setting_checks)
        proof = client.variables[publisher.IMMUTABILITY_PROOF_VARIABLE]
        self.assertEqual(
            document,
            publisher.validate_immutability_proof(
                proof,
                repository=publisher.DEFAULT_REPOSITORY,
                tag=self.identity.tag,
                commit=COMMIT,
                now=now,
            ),
        )

    def test_disabled_immutability_fails_before_remote_mutation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-publisher-test-") as temp:
            bundle, manifest = self._bundle(Path(temp))
            client = FakeGitHub()
            client.enabled = False
            with self.assertRaisesRegex(
                publisher.PublishError, "must be enabled"
            ):
                publisher.publish_bundle(
                    self.root,
                    bundle,
                    client,
                    bundle_verifier=lambda root, path: manifest,
                    sleeper=lambda seconds: None,
                )
            self.assertIsNone(client.release)
            self.assertEqual(0, client.upload_count)

    def test_orphan_tag_and_conflicting_draft_asset_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pf-publisher-test-") as temp:
            bundle, manifest = self._bundle(Path(temp))
            client = FakeGitHub()
            client.orphan_tag = True
            with self.assertRaisesRegex(
                publisher.PublishError, "already exists"
            ):
                publisher.publish_bundle(
                    self.root,
                    bundle,
                    client,
                    bundle_verifier=lambda root, path: manifest,
                    sleeper=lambda seconds: None,
                )

            client = FakeGitHub()
            client.create_draft(
                tag=self.identity.tag,
                commit=COMMIT,
                title=releases.release_title(self.identity),
                body=releases.release_body(self.identity, COMMIT),
            )
            client.remote_assets = [
                {
                    "name": releases.RELEASE_MANIFEST_NAME,
                    "size": 1,
                    "digest": f"sha256:{'0' * 64}",
                }
            ]
            with self.assertRaisesRegex(
                publisher.PublishError, "size conflicts"
            ):
                publisher.publish_bundle(
                    self.root,
                    bundle,
                    client,
                    bundle_verifier=lambda root, path: manifest,
                    sleeper=lambda seconds: None,
                )
            self.assertEqual(0, client.publish_count)


class ReleaseWorkflowTests(unittest.TestCase):
    def test_lint_release_gate_is_independent_of_unrelated_candidates(
        self,
    ) -> None:
        path = (
            releases.packs.REPO_ROOT
            / ".github"
            / "workflows"
            / "openscad-lint.yml"
        )
        text = path.read_text(encoding="utf-8")
        release_job = text.split("\n  release_bundle:\n", 1)[1].split(
            "\n  # Preserve the existing required status-check name", 1
        )[0]

        self.assertNotIn("layout_candidate_count", release_job)
        self.assertIn(
            "Prove two real dual-device builds are byte-identical",
            release_job,
        )
        self.assertEqual(
            2, release_job.count("release_print_pack.py build")
        )
        self.assertIn("release_print_pack.py verify", release_job)
        self.assertIn("Upload ephemeral release evidence", release_job)

    def test_publication_workflow_is_trusted_main_only_and_fail_closed(
        self,
    ) -> None:
        path = (
            releases.packs.REPO_ROOT
            / ".github"
            / "workflows"
            / "publish-print-pack.yml"
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("pull_request:", text)
        self.assertIn("permissions:", text)
        self.assertIn("  attestations: read", text)
        self.assertIn("  contents: write", text)
        self.assertIn("github.ref == 'refs/heads/main'", text)
        self.assertIn(
            'test "$(git rev-parse origin/main)" = "${HEAD_SHA}"', text
        )
        self.assertIn("cancel-in-progress: false", text)
        self.assertIn("openscad=2021.01-6build4", text)
        self.assertIn("vars.PF_PRINT_PACK_IMMUTABILITY_PROOF", text)
        self.assertNotIn("actions/upload-artifact", text)
        preflight = text.index("publish_print_pack.py preflight")
        build = text.index("release_print_pack.py build")
        publish = text.index("publish_print_pack.py publish")
        self.assertLess(preflight, build)
        self.assertLess(build, publish)


if __name__ == "__main__":
    unittest.main(verbosity=2)
