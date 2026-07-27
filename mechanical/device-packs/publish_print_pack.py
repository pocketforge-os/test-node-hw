#!/usr/bin/env python3
"""Publish a verified print-pack bundle as a fail-closed immutable release."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import release_print_pack as releases


API_VERSION = "2026-03-10"
DEFAULT_REPOSITORY = "pocketforge-os/test-node-hw"
REPOSITORY_RE = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MAX_ERROR_BODY = 4096
ASSET_DIGEST_POLLS = 12
IMMUTABLE_POLLS = 12
POLL_SECONDS = 5.0
IMMUTABILITY_PROOF_SCHEMA = "pocketforge-immutable-release-proof-v1"
IMMUTABILITY_PROOF_VARIABLE = "PF_PRINT_PACK_IMMUTABILITY_PROOF"
IMMUTABILITY_PROOF_TTL = dt.timedelta(hours=1)
IMMUTABILITY_PROOF_CLOCK_SKEW = dt.timedelta(minutes=2)


class PublishError(RuntimeError):
    """Remote release state conflicts with the verified local bundle."""


class ApiError(PublishError):
    """A GitHub API request failed."""

    def __init__(self, status: int, message: str):
        super().__init__(f"GitHub API status={status}: {message}")
        self.status = status


@dataclass(frozen=True)
class Asset:
    name: str
    path: Path
    sha256: str
    size_bytes: int


class GitHubClient:
    """Small REST client whose mutation surface is limited to releases."""

    def __init__(
        self,
        repository: str,
        token: str,
        *,
        api_url: str = "https://api.github.com",
        uploads_url: str = "https://uploads.github.com",
    ):
        if not REPOSITORY_RE.fullmatch(repository):
            raise PublishError(f"invalid GitHub repository: {repository!r}")
        if not token:
            raise PublishError("GH_TOKEN is required")
        self.repository = repository
        self.token = token
        self.api_url = api_url.rstrip("/")
        self.uploads_url = uploads_url.rstrip("/")

    def _request(
        self,
        method: str,
        url: str,
        *,
        body: bytes | None = None,
        content_type: str = "application/vnd.github+json",
    ) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "pocketforge-print-pack-publisher",
        }
        if body is not None:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(
            url, data=body, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read(MAX_ERROR_BODY).decode("utf-8", errors="replace")
            raise ApiError(exc.code, detail.strip() or exc.reason) from exc
        except urllib.error.URLError as exc:
            raise PublishError(f"GitHub request failed: {exc.reason}") from exc
        if not payload:
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise PublishError("GitHub returned invalid JSON") from exc

    def _api(
        self,
        method: str,
        path: str,
        document: Mapping[str, Any] | None = None,
    ) -> Any:
        body = (
            None
            if document is None
            else json.dumps(
                document, separators=(",", ":"), sort_keys=True
            ).encode("utf-8")
        )
        return self._request(method, f"{self.api_url}{path}", body=body)

    def immutable_setting(self) -> Mapping[str, Any]:
        value = self._api(
            "GET",
            f"/repos/{self.repository}/immutable-releases",
        )
        if not isinstance(value, dict):
            raise PublishError("immutable-release setting response is invalid")
        return value

    def set_actions_variable(self, name: str, value: str) -> None:
        if not re.fullmatch(r"^[A-Z][A-Z0-9_]{0,99}$", name):
            raise PublishError(f"invalid Actions variable name: {name!r}")
        path = f"/repos/{self.repository}/actions/variables/{name}"
        try:
            self._api("GET", path)
        except ApiError as exc:
            if exc.status != 404:
                raise
            self._api(
                "POST",
                f"/repos/{self.repository}/actions/variables",
                {"name": name, "value": value},
            )
        else:
            self._api("PATCH", path, {"name": name, "value": value})

    def release_by_tag(self, tag: str) -> Mapping[str, Any] | None:
        try:
            value = self._api(
                "GET",
                f"/repos/{self.repository}/releases/tags/"
                f"{urllib.parse.quote(tag, safe='')}",
            )
        except ApiError as exc:
            if exc.status == 404:
                return None
            raise
        if not isinstance(value, dict):
            raise PublishError("release response is invalid")
        return value

    def tag_ref(self, tag: str) -> Mapping[str, Any] | None:
        try:
            value = self._api(
                "GET",
                f"/repos/{self.repository}/git/ref/tags/"
                f"{urllib.parse.quote(tag, safe='')}",
            )
        except ApiError as exc:
            if exc.status == 404:
                return None
            raise
        if not isinstance(value, dict):
            raise PublishError("tag response is invalid")
        return value

    def create_draft(
        self,
        *,
        tag: str,
        commit: str,
        title: str,
        body: str,
    ) -> Mapping[str, Any]:
        value = self._api(
            "POST",
            f"/repos/{self.repository}/releases",
            {
                "tag_name": tag,
                "target_commitish": commit,
                "name": title,
                "body": body,
                "draft": True,
                "prerelease": False,
                "make_latest": "false",
            },
        )
        if not isinstance(value, dict):
            raise PublishError("create-release response is invalid")
        return value

    def release_assets(self, release_id: int) -> list[Mapping[str, Any]]:
        value = self._api(
            "GET",
            f"/repos/{self.repository}/releases/{release_id}/assets"
            "?per_page=100",
        )
        if not isinstance(value, list) or any(
            not isinstance(item, dict) for item in value
        ):
            raise PublishError("release-assets response is invalid")
        return value

    def upload_asset(
        self, release_id: int, asset: Asset
    ) -> Mapping[str, Any]:
        url = (
            f"{self.uploads_url}/repos/{self.repository}/releases/"
            f"{release_id}/assets?name="
            f"{urllib.parse.quote(asset.name, safe='')}"
        )
        value = self._request(
            "POST",
            url,
            body=asset.path.read_bytes(),
            content_type="application/octet-stream",
        )
        if not isinstance(value, dict):
            raise PublishError("upload-asset response is invalid")
        return value

    def publish_release(self, release_id: int) -> Mapping[str, Any]:
        value = self._api(
            "PATCH",
            f"/repos/{self.repository}/releases/{release_id}",
            {"draft": False, "make_latest": "false"},
        )
        if not isinstance(value, dict):
            raise PublishError("publish-release response is invalid")
        return value

    def resolved_commit(self, ref: str) -> str:
        value = self._api(
            "GET",
            f"/repos/{self.repository}/commits/"
            f"{urllib.parse.quote(ref, safe='')}",
        )
        if not isinstance(value, dict) or not isinstance(value.get("sha"), str):
            raise PublishError("resolved-commit response is invalid")
        return value["sha"]

    def latest_release(self) -> Mapping[str, Any] | None:
        try:
            value = self._api(
                "GET", f"/repos/{self.repository}/releases/latest"
            )
        except ApiError as exc:
            if exc.status == 404:
                return None
            raise
        if not isinstance(value, dict):
            raise PublishError("latest-release response is invalid")
        return value

    def download_public_asset(self, url: str) -> bytes:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "github.com":
            raise PublishError(f"unsafe release download URL: {url!r}")
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "pocketforge-print-pack-publisher"},
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read(releases.MAX_ARCHIVE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            raise ApiError(exc.code, f"asset download failed: {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise PublishError(
                f"asset download failed: {exc.reason}"
            ) from exc


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _timestamp(value: dt.datetime) -> str:
    if value.tzinfo is None:
        raise PublishError("immutability proof time must be timezone-aware")
    return (
        value.astimezone(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _parse_timestamp(value: Any, field: str) -> dt.datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise PublishError(f"immutability proof {field} is invalid")
    try:
        parsed = dt.datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as exc:
        raise PublishError(
            f"immutability proof {field} is invalid"
        ) from exc
    if parsed.microsecond:
        raise PublishError(
            f"immutability proof {field} must use whole seconds"
        )
    return parsed


def create_immutability_proof(
    *,
    repository: str,
    tag: str,
    commit: str,
    now: dt.datetime | None = None,
) -> str:
    checked_at = (
        now.astimezone(dt.timezone.utc)
        if now is not None
        else dt.datetime.now(dt.timezone.utc)
    ).replace(microsecond=0)
    document = {
        "schema": IMMUTABILITY_PROOF_SCHEMA,
        "repository": repository,
        "tag": tag,
        "commit": commit,
        "enabled": True,
        "checked_at": _timestamp(checked_at),
        "expires_at": _timestamp(checked_at + IMMUTABILITY_PROOF_TTL),
    }
    payload = json.dumps(
        document, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")


def validate_immutability_proof(
    proof: str,
    *,
    repository: str,
    tag: str,
    commit: str,
    now: dt.datetime | None = None,
) -> Mapping[str, Any]:
    if not isinstance(proof, str) or not proof or len(proof) > 4096:
        raise PublishError("immutability proof is missing or oversized")
    if not re.fullmatch(r"^[A-Za-z0-9_-]+$", proof):
        raise PublishError("immutability proof is not canonical base64url")
    padding = "=" * (-len(proof) % 4)
    try:
        payload = base64.b64decode(
            proof + padding, altchars=b"-_", validate=True
        )
        document = json.loads(payload)
    except (ValueError, json.JSONDecodeError) as exc:
        raise PublishError("immutability proof is malformed") from exc
    if not isinstance(document, dict):
        raise PublishError("immutability proof must contain an object")
    expected_fields = {
        "schema",
        "repository",
        "tag",
        "commit",
        "enabled",
        "checked_at",
        "expires_at",
    }
    if set(document) != expected_fields:
        raise PublishError("immutability proof fields are invalid")
    canonical = base64.urlsafe_b64encode(
        json.dumps(
            document, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    ).rstrip(b"=").decode("ascii")
    if canonical != proof:
        raise PublishError("immutability proof encoding is noncanonical")
    expected = {
        "schema": IMMUTABILITY_PROOF_SCHEMA,
        "repository": repository,
        "tag": tag,
        "commit": commit,
        "enabled": True,
    }
    for field, value in expected.items():
        if document.get(field) != value:
            raise PublishError(
                f"immutability proof {field} does not match publication"
            )
    checked_at = _parse_timestamp(document["checked_at"], "checked_at")
    expires_at = _parse_timestamp(document["expires_at"], "expires_at")
    current = (
        now.astimezone(dt.timezone.utc)
        if now is not None
        else dt.datetime.now(dt.timezone.utc)
    ).replace(microsecond=0)
    if checked_at > current + IMMUTABILITY_PROOF_CLOCK_SKEW:
        raise PublishError("immutability proof was checked in the future")
    if expires_at - checked_at != IMMUTABILITY_PROOF_TTL:
        raise PublishError("immutability proof has an invalid lifetime")
    if current >= expires_at:
        raise PublishError("immutability proof has expired")
    return document


def authorize_workflow(
    root: Path,
    profile_id: str,
    client: GitHubClient,
    *,
    now: dt.datetime | None = None,
) -> Mapping[str, Any]:
    root = root.resolve()
    state = releases.packs.source_state(root)
    if state.dirty:
        raise PublishError(
            "workflow authorization requires a clean source checkout"
        )
    profile = releases.resolve_profile(root, profile_id)
    identity = releases.release_identity(profile)
    remote_main = client.resolved_commit("main")
    if remote_main != state.commit:
        raise PublishError(
            f"local commit {state.commit} is not current remote main "
            f"{remote_main}"
        )
    setting = client.immutable_setting()
    if setting.get("enabled") is not True:
        raise PublishError(
            "repository immutable releases must be enabled before authorization"
        )
    proof = create_immutability_proof(
        repository=client.repository,
        tag=identity.tag,
        commit=state.commit,
        now=now,
    )
    client.set_actions_variable(IMMUTABILITY_PROOF_VARIABLE, proof)
    document = validate_immutability_proof(
        proof,
        repository=client.repository,
        tag=identity.tag,
        commit=state.commit,
        now=now,
    )
    print(
        "print_pack_publish_authorize=pass "
        f"repository={client.repository} tag={identity.tag} "
        f"commit={state.commit} expires_at={document['expires_at']}"
    )
    return document


def expected_assets(
    bundle: Path, manifest: Mapping[str, Any]
) -> dict[str, Asset]:
    devices = manifest.get("devices")
    if not isinstance(devices, list) or not devices:
        raise PublishError("release manifest.devices must be non-empty")
    names = [
        releases.RELEASE_MANIFEST_NAME,
        releases.RELEASE_CHECKSUM_NAME,
    ]
    for index, device in enumerate(devices):
        if not isinstance(device, dict) or not isinstance(
            device.get("archive"), dict
        ):
            raise PublishError(
                f"release manifest.devices[{index}] is invalid"
            )
        names.append(
            releases._safe_asset_name(
                device["archive"].get("name"),
                f"release manifest.devices[{index}].archive.name",
            )
        )
    if len(names) != len(set(names)):
        raise PublishError("release asset names are not unique")
    assets: dict[str, Asset] = {}
    for name in sorted(names):
        path = bundle / name
        if not path.is_file() or path.is_symlink():
            raise PublishError(f"release asset is missing: {name}")
        assets[name] = Asset(
            name=name,
            path=path,
            sha256=_sha256(path),
            size_bytes=path.stat().st_size,
        )
    return assets


def _release_id(value: Mapping[str, Any]) -> int:
    release_id = value.get("id")
    if isinstance(release_id, bool) or not isinstance(release_id, int):
        raise PublishError("release has no valid numeric ID")
    return release_id


def _validate_release_identity(
    release: Mapping[str, Any],
    *,
    tag: str,
    commit: str,
    title: str,
    body: str,
) -> None:
    expected = {
        "tag_name": tag,
        "target_commitish": commit,
        "name": title,
        "body": body,
        "prerelease": False,
    }
    for field, value in expected.items():
        if release.get(field) != value:
            raise PublishError(
                f"existing release {field} conflicts with local bundle"
            )


def _asset_digest(remote: Mapping[str, Any]) -> str | None:
    digest = remote.get("digest")
    if digest is None:
        return None
    if (
        not isinstance(digest, str)
        or not digest.startswith("sha256:")
        or not SHA256_RE.fullmatch(digest.removeprefix("sha256:"))
    ):
        raise PublishError(f"remote asset has invalid digest: {digest!r}")
    return digest.removeprefix("sha256:")


def _validate_remote_assets(
    remote: Sequence[Mapping[str, Any]],
    expected: Mapping[str, Asset],
    *,
    allow_missing: bool,
) -> set[str]:
    by_name: dict[str, Mapping[str, Any]] = {}
    for item in remote:
        name = item.get("name")
        if not isinstance(name, str) or name in by_name:
            raise PublishError("remote release has invalid/duplicate asset names")
        by_name[name] = item
    extra = sorted(by_name.keys() - expected.keys())
    if extra:
        raise PublishError(
            f"remote release has unexpected assets: {', '.join(extra)}"
        )
    missing = set(expected) - by_name.keys()
    if missing and not allow_missing:
        raise PublishError(
            f"remote release is missing assets: {', '.join(sorted(missing))}"
        )
    for name, remote_asset in by_name.items():
        local = expected[name]
        if remote_asset.get("size") != local.size_bytes:
            raise PublishError(f"remote asset size conflicts for {name}")
        digest = _asset_digest(remote_asset)
        if digest is not None and digest != local.sha256:
            raise PublishError(f"remote asset digest conflicts for {name}")
    return missing


Sleeper = Callable[[float], None]


def _wait_for_asset_digests(
    client: GitHubClient,
    release_id: int,
    expected: Mapping[str, Asset],
    *,
    sleeper: Sleeper,
) -> list[Mapping[str, Any]]:
    remote: list[Mapping[str, Any]] = []
    for attempt in range(ASSET_DIGEST_POLLS):
        remote = client.release_assets(release_id)
        _validate_remote_assets(remote, expected, allow_missing=False)
        if all(_asset_digest(item) is not None for item in remote):
            return remote
        if attempt + 1 < ASSET_DIGEST_POLLS:
            sleeper(POLL_SECONDS)
    raise PublishError("GitHub did not report every asset SHA-256 in time")


def _verify_downloads(
    client: GitHubClient,
    remote: Sequence[Mapping[str, Any]],
    expected: Mapping[str, Asset],
) -> None:
    for item in remote:
        name = item["name"]
        url = item.get("browser_download_url")
        if not isinstance(url, str):
            raise PublishError(f"remote asset has no download URL: {name}")
        payload = client.download_public_asset(url)
        local = expected[name]
        if (
            len(payload) != local.size_bytes
            or hashlib.sha256(payload).hexdigest() != local.sha256
        ):
            raise PublishError(f"downloaded asset bytes conflict for {name}")


def _verify_published_state(
    client: GitHubClient,
    release: Mapping[str, Any],
    *,
    tag: str,
    commit: str,
    expected: Mapping[str, Asset],
) -> None:
    if release.get("draft") is not False:
        raise PublishError("release is still a draft")
    if release.get("immutable") is not True:
        raise PublishError("published release is not immutable")
    remote = client.release_assets(_release_id(release))
    _validate_remote_assets(remote, expected, allow_missing=False)
    if any(_asset_digest(item) is None for item in remote):
        raise PublishError("published release has an asset without a digest")
    resolved = client.resolved_commit(tag)
    if resolved != commit:
        raise PublishError(
            f"release tag resolves to {resolved}, expected {commit}"
        )
    latest = client.latest_release()
    if latest is not None and latest.get("tag_name") == tag:
        raise PublishError("qualified print-pack release was marked latest")
    _verify_downloads(client, remote, expected)


BundleVerifier = Callable[[Path, Path], Mapping[str, Any]]


def publish_bundle(
    root: Path,
    bundle: Path,
    client: GitHubClient,
    *,
    bundle_verifier: BundleVerifier = releases.verify_release_bundle,
    sleeper: Sleeper = time.sleep,
    immutability_proof: str | None = None,
    now: dt.datetime | None = None,
) -> str:
    root = root.resolve()
    bundle = bundle.expanduser().resolve()
    manifest = bundle_verifier(root, bundle)
    tag = manifest.get("tag")
    title = manifest.get("title")
    source = manifest.get("source")
    if (
        not isinstance(tag, str)
        or not isinstance(title, str)
        or not isinstance(source, dict)
        or not isinstance(source.get("commit"), str)
        or not GIT_SHA_RE.fullmatch(source["commit"])
        or source.get("dirty") is not False
    ):
        raise PublishError("release manifest publication identity is invalid")
    commit = source["commit"]
    expected_repository = (
        f"https://github.com/{client.repository}"
    )
    if source.get("repository") != expected_repository:
        raise PublishError(
            "release source repository does not match publication target"
        )
    profile = manifest.get("profile")
    qualification = manifest.get("qualification")
    if (
        not isinstance(profile, dict)
        or not isinstance(profile.get("id"), str)
        or not isinstance(qualification, dict)
    ):
        raise PublishError("release qualification identity is invalid")
    identity = releases.release_identity(
        releases.resolve_profile(root, profile.get("id"))
    )
    if tag != identity.tag:
        raise PublishError("release tag does not match qualified profile")
    body = releases.release_body(identity, commit)
    assets = expected_assets(bundle, manifest)

    if immutability_proof is None:
        setting = client.immutable_setting()
        if setting.get("enabled") is not True:
            raise PublishError(
                "repository immutable releases must be enabled before "
                "publication"
            )
    else:
        validate_immutability_proof(
            immutability_proof,
            repository=client.repository,
            tag=tag,
            commit=commit,
            now=now,
        )

    release = client.release_by_tag(tag)
    if release is None:
        if client.tag_ref(tag) is not None:
            raise PublishError(
                f"tag {tag} already exists without a matching release"
            )
        try:
            release = client.create_draft(
                tag=tag,
                commit=commit,
                title=title,
                body=body,
            )
        except ApiError as exc:
            if exc.status != 422:
                raise
            # A concurrent exact publisher may have won the create race.
            release = client.release_by_tag(tag)
            if release is None:
                raise

    _validate_release_identity(
        release,
        tag=tag,
        commit=commit,
        title=title,
        body=body,
    )
    if release.get("draft") is False:
        _verify_published_state(
            client,
            release,
            tag=tag,
            commit=commit,
            expected=assets,
        )
        print(f"print_pack_publish=pass tag={tag} state=already_published")
        return tag
    if release.get("draft") is not True:
        raise PublishError("existing release has an invalid draft state")

    release_id = _release_id(release)
    remote = client.release_assets(release_id)
    missing = _validate_remote_assets(remote, assets, allow_missing=True)
    for name in sorted(missing):
        client.upload_asset(release_id, assets[name])
    _wait_for_asset_digests(
        client, release_id, assets, sleeper=sleeper
    )

    published = client.publish_release(release_id)
    for attempt in range(IMMUTABLE_POLLS):
        current = client.release_by_tag(tag)
        if current is None:
            raise PublishError("published release disappeared")
        published = current
        if (
            published.get("draft") is False
            and published.get("immutable") is True
        ):
            break
        if attempt + 1 < IMMUTABLE_POLLS:
            sleeper(POLL_SECONDS)
    _validate_release_identity(
        published,
        tag=tag,
        commit=commit,
        title=title,
        body=body,
    )
    _verify_published_state(
        client,
        published,
        tag=tag,
        commit=commit,
        expected=assets,
    )
    print(f"print_pack_publish=pass tag={tag} state=published_immutable")
    return tag


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=releases.packs.REPO_ROOT)
    parser.add_argument(
        "--repository",
        default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    authorize = subparsers.add_parser("authorize")
    authorize.add_argument("--profile-id", required=True)
    authorize.add_argument("--token-env", default="PF_RELEASE_ADMIN_TOKEN")

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--profile-id", required=True)
    preflight.add_argument(
        "--immutability-proof",
        default=os.environ.get(IMMUTABILITY_PROOF_VARIABLE, ""),
    )
    preflight.add_argument("--token-env", default="GH_TOKEN")

    publish = subparsers.add_parser("publish")
    publish.add_argument("--bundle", type=Path, required=True)
    publish.add_argument(
        "--immutability-proof",
        default=os.environ.get(IMMUTABILITY_PROOF_VARIABLE, ""),
    )
    publish.add_argument("--token-env", default="GH_TOKEN")

    args = parser.parse_args(argv)
    try:
        token = os.environ.get(args.token_env, "")
        client = GitHubClient(args.repository, token)
        if args.command == "authorize":
            authorize_workflow(
                args.root, args.profile_id, client
            )
        elif args.command == "preflight":
            if args.immutability_proof:
                state = releases.packs.source_state(args.root)
                identity = releases.release_identity(
                    releases.resolve_profile(args.root, args.profile_id)
                )
                validate_immutability_proof(
                    args.immutability_proof,
                    repository=args.repository,
                    tag=identity.tag,
                    commit=state.commit,
                )
            else:
                setting = client.immutable_setting()
                if setting.get("enabled") is not True:
                    raise PublishError(
                        "repository immutable releases are not enabled"
                    )
            print(
                "print_pack_publish_preflight=pass "
                f"repository={args.repository} immutable=true"
            )
        elif args.command == "publish":
            bundle = (
                args.bundle
                if args.bundle.is_absolute()
                else args.root / args.bundle
            )
            publish_bundle(
                args.root,
                bundle,
                client,
                immutability_proof=args.immutability_proof or None,
            )
        else:  # pragma: no cover
            raise PublishError(f"unsupported command: {args.command}")
    except (
        PublishError,
        releases.ReleaseError,
        releases.packs.PackError,
        releases.packs.holder_profiles.ProfileError,
        OSError,
    ) as exc:
        print(f"print_pack_publish_error: {exc}", file=releases.packs.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
