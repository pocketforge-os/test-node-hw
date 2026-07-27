#!/usr/bin/env python3
"""Build and verify immutable-release bundles for qualified device print packs.

A release is keyed by one versioned physical-qualification manifest.  It
contains one canonical ZIP for every device variant covered by that holder
profile, plus release-level provenance and checksums.  The generated bundle is
an ignored artifact; committed source and qualification records remain the
source of truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping, Sequence

import build_device_pack as packs


RELEASE_SCHEMA = "pocketforge-print-pack-release-v1"
RELEASE_MANIFEST_NAME = "release-manifest.json"
RELEASE_CHECKSUM_NAME = "SHA256SUMS"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = stat.S_IFREG | 0o644
MAX_ARCHIVE_FILES = 64
MAX_ARCHIVE_FILE_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_BYTES = 1024 * 1024 * 1024
PROFILE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ReleaseError(ValueError):
    """A release identity, bundle, archive, or publication input is invalid."""


@dataclass(frozen=True)
class ReleaseIdentity:
    profile_id: str
    version: int
    tag: str
    qualification_path: Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _reject_constant(token: str) -> None:
    raise ReleaseError(f"JSON contains non-finite number {token}")


def _reject_duplicate_keys(
    pairs: Sequence[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReleaseError(f"JSON contains duplicate key {key!r}")
        result[key] = value
    return result


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ReleaseError(f"path is outside repository: {path}") from exc


def _safe_relative_file(value: Any, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ReleaseError(f"{field} must be a non-empty POSIX path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or "." in path.parts
        or ".." in path.parts
        or any(not part for part in path.parts)
    ):
        raise ReleaseError(f"{field} must be a safe relative file path")
    return path


def _safe_asset_name(value: Any, field: str) -> str:
    path = _safe_relative_file(value, field)
    if len(path.parts) != 1:
        raise ReleaseError(f"{field} must be a file name, not a path")
    return path.name


def _load_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_constant,
            object_pairs_hook=_reject_duplicate_keys,
        )
    except OSError as exc:
        raise ReleaseError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseError(
            f"{path}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"{path} must contain a JSON object")
    return value


def _strict_keys(
    value: Mapping[str, Any],
    field: str,
    required: set[str],
) -> None:
    missing = sorted(required - value.keys())
    extra = sorted(value.keys() - required)
    if missing:
        raise ReleaseError(f"{field} missing fields: {', '.join(missing)}")
    if extra:
        raise ReleaseError(f"{field} has unknown fields: {', '.join(extra)}")


def resolve_profile(
    root: Path, profile_id: str
) -> packs.holder_profiles.ResolvedProfile:
    if not PROFILE_ID_RE.fullmatch(profile_id):
        raise ReleaseError(f"invalid profile ID: {profile_id!r}")
    cradle_root = root.resolve() / "mechanical" / "dut-cradle-v1"
    paths = [
        path
        for path in packs.holder_profiles.discover_profiles(cradle_root)
        if path.stem == profile_id
    ]
    if len(paths) != 1:
        raise ReleaseError(
            f"expected exactly one holder profile {profile_id!r}, found "
            f"{len(paths)}"
        )
    profile = packs.holder_profiles.validate_profile(
        cradle_root, paths[0]
    )
    try:
        profile.path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ReleaseError("holder profile is outside the repository") from exc
    return profile


def release_identity(
    profile: packs.holder_profiles.ResolvedProfile,
) -> ReleaseIdentity:
    profile_id = profile.document["profile_id"]
    qualification = profile.document["qualification"]
    if (
        qualification["status"] != "physically_qualified"
        or profile.qualification_manifest is None
    ):
        raise ReleaseError(
            f"profile {profile_id!r} is not physically qualified"
        )
    path = (profile.root / qualification["geometry_manifest"]).resolve()
    match = re.fullmatch(
        rf"{re.escape(profile_id)}-v([1-9][0-9]*)\.json", path.name
    )
    if path.parent != (profile.root / "qualification").resolve() or not match:
        raise ReleaseError(
            "qualification manifest must be named "
            f"qualification/{profile_id}-vN.json"
        )
    version = int(match.group(1))
    return ReleaseIdentity(
        profile_id=profile_id,
        version=version,
        tag=f"print-pack-{profile_id}-v{version}",
        qualification_path=path,
    )


def archive_name(device_slug: str) -> str:
    if not PROFILE_ID_RE.fullmatch(device_slug):
        raise ReleaseError(f"invalid device slug: {device_slug!r}")
    return f"device-pack-{device_slug}.zip"


def release_title(identity: ReleaseIdentity) -> str:
    return (
        f"PocketForge qualified print pack: {identity.profile_id} "
        f"v{identity.version}"
    )


def release_body(
    identity: ReleaseIdentity, source_commit: str
) -> str:
    return (
        "Immutable PocketForge production print packs generated from "
        f"`{source_commit}` and physical qualification "
        f"`{identity.qualification_path.name}`.\n\n"
        "Verify `SHA256SUMS` before printing. The release manifest records "
        "the complete holder, fixture, platform, toolchain, and source "
        "provenance. This release is intentionally not the repository's "
        "moving latest release."
    )


def _zip_member(root_name: str, relative: PurePosixPath) -> str:
    if not PROFILE_ID_RE.fullmatch(root_name):
        raise ReleaseError(f"invalid archive root: {root_name!r}")
    return (PurePosixPath(root_name) / relative).as_posix()


def _write_archive(pack: Path, archive: Path, root_name: str) -> None:
    if not pack.is_dir() or pack.is_symlink():
        raise ReleaseError(f"pack is not a directory: {pack}")
    files = sorted(
        (path for path in pack.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(pack).as_posix(),
    )
    if not files:
        raise ReleaseError(f"pack contains no files: {pack}")
    for path in pack.rglob("*"):
        if path.is_symlink():
            raise ReleaseError(f"pack contains a symlink: {path}")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        archive,
        mode="w",
        compression=zipfile.ZIP_STORED,
        allowZip64=True,
    ) as output:
        output.comment = b""
        for path in files:
            relative = PurePosixPath(path.relative_to(pack).as_posix())
            member = _zip_member(root_name, relative)
            info = zipfile.ZipInfo(member, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = ZIP_FILE_MODE << 16
            info.extra = b""
            info.comment = b""
            output.writestr(info, path.read_bytes())


def _expected_pack_files(manifest: Mapping[str, Any]) -> set[str]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ReleaseError("inner pack manifest.artifacts must be an array")
    paths = {"manifest.json", "SHA256SUMS"}
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ReleaseError(
                f"inner pack manifest.artifacts[{index}] must be an object"
            )
        path = _safe_relative_file(
            artifact.get("path"),
            f"inner pack manifest.artifacts[{index}].path",
        ).as_posix()
        if path in paths:
            raise ReleaseError(f"duplicate inner pack path: {path}")
        paths.add(path)
    return paths


PackVerifier = Callable[[Path, Path], None]


def _verify_archive(
    root: Path,
    archive: Path,
    *,
    device_slug: str,
    pack_verifier: PackVerifier = packs.verify_pack,
) -> Mapping[str, Any]:
    expected_root = f"device-pack-{device_slug}"
    if archive.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ReleaseError(f"archive exceeds size limit: {archive.name}")
    with tempfile.TemporaryDirectory(prefix="pf-release-archive-") as temp:
        extraction = Path(temp)
        try:
            source = zipfile.ZipFile(archive, mode="r")
        except (OSError, zipfile.BadZipFile) as exc:
            raise ReleaseError(f"invalid ZIP {archive.name}: {exc}") from exc
        with source:
            if source.comment:
                raise ReleaseError(f"{archive.name} has a ZIP comment")
            infos = source.infolist()
            if not infos or len(infos) > MAX_ARCHIVE_FILES:
                raise ReleaseError(
                    f"{archive.name} has an invalid member count"
                )
            names = [info.filename for info in infos]
            if names != sorted(names):
                raise ReleaseError(
                    f"{archive.name} members are not canonically ordered"
                )
            if len(names) != len(set(names)):
                raise ReleaseError(f"{archive.name} has duplicate members")
            total_size = 0
            relative_names: set[str] = set()
            for index, info in enumerate(infos):
                member = _safe_relative_file(
                    info.filename, f"{archive.name}.members[{index}]"
                )
                if len(member.parts) < 2 or member.parts[0] != expected_root:
                    raise ReleaseError(
                        f"{archive.name} member is outside {expected_root}/: "
                        f"{info.filename}"
                    )
                if info.is_dir():
                    raise ReleaseError(
                        f"{archive.name} must not contain directory entries"
                    )
                if (
                    info.date_time != ZIP_TIMESTAMP
                    or info.compress_type != zipfile.ZIP_STORED
                    or info.create_system != 3
                    or info.external_attr != ZIP_FILE_MODE << 16
                    or info.extra
                    or info.comment
                    or info.flag_bits & 0x1
                ):
                    raise ReleaseError(
                        f"{archive.name} member metadata is noncanonical: "
                        f"{info.filename}"
                    )
                if (
                    info.file_size > MAX_ARCHIVE_FILE_BYTES
                    or info.compress_size != info.file_size
                ):
                    raise ReleaseError(
                        f"{archive.name} member has invalid size/compression: "
                        f"{info.filename}"
                    )
                total_size += info.file_size
                if total_size > MAX_ARCHIVE_BYTES:
                    raise ReleaseError(
                        f"{archive.name} expanded content exceeds size limit"
                    )
                relative = PurePosixPath(*member.parts[1:])
                relative_names.add(relative.as_posix())
                destination = extraction / Path(*member.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read(info))
            bad_member = source.testzip()
            if bad_member is not None:
                raise ReleaseError(
                    f"{archive.name} failed CRC verification: {bad_member}"
                )

        pack = extraction / expected_root
        manifest = _load_json(pack / "manifest.json")
        if (pack / "manifest.json").read_bytes() != _json_bytes(manifest):
            raise ReleaseError(
                f"{archive.name} inner manifest JSON is noncanonical"
            )
        expected_files = _expected_pack_files(manifest)
        if relative_names != expected_files:
            raise ReleaseError(
                f"{archive.name} membership mismatch: "
                f"extra={sorted(relative_names - expected_files)} "
                f"missing={sorted(expected_files - relative_names)}"
            )
        if manifest.get("schema") != packs.PACK_SCHEMA:
            raise ReleaseError(
                f"{archive.name} has unsupported inner pack schema"
            )
        device = manifest.get("device")
        if not isinstance(device, dict) or device.get("slug") != device_slug:
            raise ReleaseError(f"{archive.name} has the wrong device identity")
        if (
            manifest.get("mode") != "full"
            or manifest.get("production_eligible") is not True
            or manifest.get("nonproduction_reasons") != []
            or manifest.get("overrides") != []
        ):
            raise ReleaseError(
                f"{archive.name} is not an unmodified production full pack"
            )
        source_record = manifest.get("source")
        if (
            not isinstance(source_record, dict)
            or source_record.get("dirty") is not False
            or not isinstance(source_record.get("commit"), str)
            or not GIT_SHA_RE.fullmatch(source_record["commit"])
        ):
            raise ReleaseError(f"{archive.name} has invalid source provenance")
        pack_verifier(root, pack)

        rebuilt = extraction / "canonical.zip"
        _write_archive(pack, rebuilt, expected_root)
        if archive.read_bytes() != rebuilt.read_bytes():
            raise ReleaseError(
                f"{archive.name} is not the canonical deterministic ZIP"
            )
        return manifest


def _archive_record(
    archive: Path,
    device_slug: str,
    pack_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    with zipfile.ZipFile(archive, mode="r") as source:
        manifest_bytes = source.read(
            f"device-pack-{device_slug}/manifest.json"
        )
    return {
        "device_slug": device_slug,
        "display_name": pack_manifest["device"]["display_name"],
        "archive": {
            "name": archive.name,
            "sha256": _sha256(archive),
            "size_bytes": archive.stat().st_size,
        },
        "pack": {
            "schema": pack_manifest["schema"],
            "mode": pack_manifest["mode"],
            "manifest_path": f"device-pack-{device_slug}/manifest.json",
            "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "artifact_count": len(pack_manifest["artifacts"]),
        },
    }


def _release_document(
    root: Path,
    identity: ReleaseIdentity,
    profile: packs.holder_profiles.ResolvedProfile,
    source_pack: Mapping[str, Any],
    devices: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "schema": RELEASE_SCHEMA,
        "tag": identity.tag,
        "title": release_title(identity),
        "profile": {
            "id": identity.profile_id,
            "path": _relative(root, profile.path),
            "sha256": _sha256(profile.path),
        },
        "qualification": source_pack["qualification"],
        "fixture": source_pack["fixture"],
        "layout": source_pack["layout"],
        "source": source_pack["source"],
        "toolchain": source_pack["toolchain"],
        "generator": {
            "path": _relative(root, Path(__file__)),
            "sha256": _sha256(Path(__file__)),
            "archive_algorithm": "canonical-zip-stored-v1",
        },
        "devices": list(devices),
    }


def _write_release_checksums(stage: Path, archive_names: Sequence[str]) -> None:
    names = [*sorted(archive_names), RELEASE_MANIFEST_NAME]
    lines = [f"{_sha256(stage / name)}  {name}\n" for name in names]
    (stage / RELEASE_CHECKSUM_NAME).write_text(
        "".join(lines), encoding="utf-8"
    )


def _safe_output(root: Path, output: Path) -> Path:
    root = root.resolve()
    absolute = Path(os.path.abspath(output.expanduser()))
    if absolute.is_symlink():
        raise ReleaseError(f"output may not be a symlink: {absolute}")
    try:
        lexical = absolute.relative_to(root)
    except ValueError:
        lexical = None
    if lexical is not None:
        cursor = root
        for part in lexical.parts:
            cursor /= part
            if cursor.is_symlink():
                raise ReleaseError(
                    f"in-repository output traverses a symlink: {cursor}"
                )
    resolved = absolute.resolve()
    if resolved == root:
        raise ReleaseError("output may not be the repository root")
    try:
        relative = PurePosixPath(resolved.relative_to(root).as_posix())
    except ValueError:
        return resolved
    allowed = PurePosixPath("mechanical/device-packs/build/releases")
    if allowed not in relative.parents or relative == allowed:
        raise ReleaseError(
            "in-repository release output must be one directory below "
            "mechanical/device-packs/build/releases"
        )
    if relative.parent != allowed:
        raise ReleaseError(
            "in-repository release output must be exactly one tag directory"
        )
    return resolved


def _read_release_manifest(bundle: Path) -> Mapping[str, Any]:
    document = _load_json(bundle / RELEASE_MANIFEST_NAME)
    _strict_keys(
        document,
        RELEASE_MANIFEST_NAME,
        {
            "schema",
            "tag",
            "title",
            "profile",
            "qualification",
            "fixture",
            "layout",
            "source",
            "toolchain",
            "generator",
            "devices",
        },
    )
    if document["schema"] != RELEASE_SCHEMA:
        raise ReleaseError(
            f"unsupported release schema: {document['schema']!r}"
        )
    return document


def _recognized_bundle(output: Path) -> None:
    if not output.is_dir() or output.is_symlink():
        raise ReleaseError(f"refusing to replace non-bundle output: {output}")
    document = _read_release_manifest(output)
    devices = document.get("devices")
    if not isinstance(devices, list):
        raise ReleaseError("release manifest.devices must be an array")
    archive_names = {
        _safe_asset_name(
            device.get("archive", {}).get("name")
            if isinstance(device, dict)
            and isinstance(device.get("archive"), dict)
            else None,
            "release manifest device archive",
        )
        for device in devices
    }
    expected = {
        RELEASE_MANIFEST_NAME,
        RELEASE_CHECKSUM_NAME,
        *archive_names,
    }
    actual = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    if any(path.is_symlink() or path.is_dir() for path in output.rglob("*")):
        raise ReleaseError(
            "refusing to replace bundle containing symlinks/directories"
        )
    if actual != expected:
        raise ReleaseError(
            "refusing to replace bundle with unrecognized membership"
        )


def _publish_stage(stage: Path, output: Path, replace: bool) -> None:
    backup: Path | None = None
    if output.exists() or output.is_symlink():
        if not replace:
            raise ReleaseError(
                f"output already exists: {output}; pass --replace to replace "
                "a recognized generated release bundle"
            )
        _recognized_bundle(output)
        backup = output.parent / (
            f".{output.name}.backup-{secrets.token_hex(8)}"
        )
        os.replace(output, backup)
    try:
        os.replace(stage, output)
    except BaseException:
        if backup is not None and not output.exists():
            os.replace(backup, output)
        raise
    if backup is not None:
        shutil.rmtree(backup)


def verify_release_bundle(
    root: Path,
    bundle: Path,
    *,
    pack_verifier: PackVerifier = packs.verify_pack,
) -> Mapping[str, Any]:
    root = root.resolve()
    bundle = bundle.expanduser().resolve()
    if not bundle.is_dir() or bundle.is_symlink():
        raise ReleaseError(f"release bundle is not a directory: {bundle}")
    if any(path.is_symlink() for path in bundle.rglob("*")):
        raise ReleaseError("release bundle must not contain symlinks")
    document = _read_release_manifest(bundle)
    if (bundle / RELEASE_MANIFEST_NAME).read_bytes() != _json_bytes(document):
        raise ReleaseError("release manifest JSON is noncanonical")
    profile_record = document.get("profile")
    if not isinstance(profile_record, dict):
        raise ReleaseError("release manifest.profile must be an object")
    profile_id = profile_record.get("id")
    if not isinstance(profile_id, str):
        raise ReleaseError("release manifest.profile.id is invalid")
    profile = resolve_profile(root, profile_id)
    identity = release_identity(profile)
    if document.get("tag") != identity.tag:
        raise ReleaseError("release tag does not match qualification identity")

    devices = document.get("devices")
    if not isinstance(devices, list) or not devices:
        raise ReleaseError("release manifest.devices must be non-empty")
    slugs: list[str] = []
    archive_records: list[dict[str, Any]] = []
    source_pack: Mapping[str, Any] | None = None
    archive_names: list[str] = []
    for index, record in enumerate(devices):
        if not isinstance(record, dict):
            raise ReleaseError(
                f"release manifest.devices[{index}] must be an object"
            )
        slug = record.get("device_slug")
        if not isinstance(slug, str) or not PROFILE_ID_RE.fullmatch(slug):
            raise ReleaseError(
                f"release manifest.devices[{index}].device_slug is invalid"
            )
        name = archive_name(slug)
        archive_record = record.get("archive")
        if not isinstance(archive_record, dict) or archive_record.get(
            "name"
        ) != name:
            raise ReleaseError(f"release archive name mismatch for {slug}")
        archive = bundle / name
        if not archive.is_file() or archive.is_symlink():
            raise ReleaseError(f"release archive is missing: {name}")
        manifest = _verify_archive(
            root,
            archive,
            device_slug=slug,
            pack_verifier=pack_verifier,
        )
        if source_pack is None:
            source_pack = manifest
        for field in (
            "profile",
            "qualification",
            "fixture",
            "layout",
            "source",
            "toolchain",
        ):
            if manifest.get(field) != source_pack.get(field):
                raise ReleaseError(
                    f"device packs have mixed {field} provenance"
                )
        computed = _archive_record(archive, slug, manifest)
        if record != computed:
            raise ReleaseError(f"release archive metadata mismatch for {slug}")
        slugs.append(slug)
        archive_names.append(name)
        archive_records.append(computed)

    expected_slugs = sorted(profile.variants)
    if slugs != expected_slugs or len(slugs) != len(set(slugs)):
        raise ReleaseError(
            f"release devices must be exactly {expected_slugs}, got {slugs}"
        )
    assert source_pack is not None
    if source_pack.get("profile") != document.get("profile"):
        raise ReleaseError(
            "inner packs do not identify the release holder profile"
        )
    expected_document = _release_document(
        root, identity, profile, source_pack, archive_records
    )
    if document != expected_document:
        raise ReleaseError(
            "release manifest does not match current qualified source"
        )

    expected_files = {
        RELEASE_MANIFEST_NAME,
        RELEASE_CHECKSUM_NAME,
        *archive_names,
    }
    actual_files = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file()
    }
    actual_dirs = [
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_dir()
    ]
    if actual_files != expected_files or actual_dirs:
        raise ReleaseError(
            f"release membership mismatch: "
            f"extra={sorted(actual_files - expected_files)} "
            f"missing={sorted(expected_files - actual_files)} "
            f"directories={actual_dirs}"
        )
    expected_sums = "".join(
        f"{_sha256(bundle / name)}  {name}\n"
        for name in [*sorted(archive_names), RELEASE_MANIFEST_NAME]
    )
    try:
        actual_sums = (bundle / RELEASE_CHECKSUM_NAME).read_text(
            encoding="utf-8"
        )
    except OSError as exc:
        raise ReleaseError(f"cannot read release SHA256SUMS: {exc}") from exc
    if actual_sums != expected_sums:
        raise ReleaseError("release SHA256SUMS does not match release assets")

    state = packs.source_state(root)
    if state.dirty or document["source"] != {
        "repository": packs.REPOSITORY_URL,
        "commit": state.commit,
        "dirty": False,
    }:
        raise ReleaseError(
            "release bundle does not identify the current clean source commit"
        )
    print(
        f"print_pack_release_verify=pass tag={identity.tag} "
        f"devices={len(slugs)} bundle={bundle}"
    )
    return document


def build_release_bundle(
    root: Path,
    *,
    profile_id: str,
    output: Path | None,
    openscad: str,
    replace: bool,
) -> Path:
    root = root.resolve()
    state = packs.source_state(root)
    if state.dirty:
        raise ReleaseError(
            "release bundles require a clean committed source tree"
        )
    profile = resolve_profile(root, profile_id)
    identity = release_identity(profile)
    layout = packs.load_layout(
        root,
        root
        / "mechanical"
        / "device-packs"
        / "layouts"
        / "chassis-core-v1.json",
    )
    if output is None:
        output = (
            root
            / "mechanical"
            / "device-packs"
            / "build"
            / "releases"
            / identity.tag
        )
    elif not output.is_absolute():
        output = root / output
    output = _safe_output(root, output)
    if output.exists() or output.is_symlink():
        if not replace:
            raise ReleaseError(
                f"output already exists: {output}; pass --replace to replace "
                "a recognized generated release bundle"
            )
        _recognized_bundle(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(prefix=f".{identity.tag}.stage-", dir=output.parent)
    )
    try:
        work = stage / ".packs"
        work.mkdir()
        archive_records: list[dict[str, Any]] = []
        source_pack: Mapping[str, Any] | None = None
        archive_names: list[str] = []
        for slug in sorted(profile.variants):
            pack = work / slug
            packs.build_pack(
                root,
                profile,
                layout,
                device_slug=slug,
                mode="full",
                output=pack,
                openscad=openscad,
                replace=False,
                allow_dirty=False,
                allow_unqualified=False,
                state=state,
            )
            packs.verify_pack(root, pack)
            manifest = _load_json(pack / "manifest.json")
            name = archive_name(slug)
            archive = stage / name
            _write_archive(pack, archive, f"device-pack-{slug}")
            verified_manifest = _verify_archive(
                root, archive, device_slug=slug
            )
            if manifest != verified_manifest:
                raise ReleaseError(
                    f"archive changed the inner pack manifest for {slug}"
                )
            if source_pack is None:
                source_pack = manifest
            archive_records.append(_archive_record(archive, slug, manifest))
            archive_names.append(name)
        assert source_pack is not None
        shutil.rmtree(work)
        release_manifest = _release_document(
            root, identity, profile, source_pack, archive_records
        )
        (stage / RELEASE_MANIFEST_NAME).write_bytes(
            _json_bytes(release_manifest)
        )
        _write_release_checksums(stage, archive_names)
        verify_release_bundle(root, stage)
        _publish_stage(stage, output, replace)
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        raise
    print(
        f"print_pack_release_build=pass tag={identity.tag} "
        f"devices={len(profile.variants)} output={output}"
    )
    return output


def _resolve_cli_path(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=packs.REPO_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    identity_parser = subparsers.add_parser("identity")
    identity_parser.add_argument("--profile-id", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--profile-id", required=True)
    build_parser.add_argument("--output", type=Path)
    build_parser.add_argument("--openscad", default="openscad")
    build_parser.add_argument("--replace", action="store_true")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--bundle", type=Path, required=True)

    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "identity":
            identity = release_identity(
                resolve_profile(root, args.profile_id)
            )
            print(identity.tag)
        elif args.command == "build":
            build_release_bundle(
                root,
                profile_id=args.profile_id,
                output=args.output,
                openscad=args.openscad,
                replace=args.replace,
            )
        elif args.command == "verify":
            verify_release_bundle(
                root, _resolve_cli_path(root, args.bundle)
            )
        else:  # pragma: no cover
            raise ReleaseError(f"unsupported command: {args.command}")
    except (
        ReleaseError,
        packs.PackError,
        packs.holder_profiles.ProfileError,
        OSError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"print_pack_release_error: {exc}", file=packs.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
