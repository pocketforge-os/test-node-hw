#!/usr/bin/env python3
"""Plan, stage, and verify upstream fixture-interface candidates.

The active holder profile, accepted fixture lock, geometry, and qualification
are immutable inputs here.  A changed platform interface creates only a new
candidate lock and an ``awaiting_holder_design`` receipt.  Promotion into an
active profile remains a separate holder-design and physical-acceptance change.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Sequence

import holder_profiles
import qualification_ci


SNAPSHOT_SCHEMA = "pocketforge-fixture-dependency-snapshot-v1"
PLAN_SCHEMA = "pocketforge-fixture-update-plan-v1"
CANDIDATE_LOCK_SCHEMA = "pocketforge-fixture-candidate-lock-v1"
RECEIPT_SCHEMA = "pocketforge-fixture-update-receipt-v1"
CANONICALIZATION = "pocketforge-fixture-interface-json-v1"
SOURCE_REPOSITORY = "https://github.com/pocketforge-os/platform.git"
CONTRACT_SCHEMA_PATH = "schemas/device-fixture-contract.schema.json"
AWAITING_HOLDER_DESIGN = "awaiting_holder_design"

CANDIDATE_LOCK_DIRECTORY = Path("profiles/fixture-locks/candidates")
RECEIPT_DIRECTORY = Path("qualification/fixture-updates")

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_REV_RE = re.compile(r"^[0-9a-f]{40}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RECEIPT_ID_RE = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*-r[1-9][0-9]*-[0-9a-f]{64}$"
)


class IntakeError(ValueError):
    """A fixture dependency is malformed, stale, or unsafe to stage."""


@dataclass(frozen=True)
class Snapshot:
    document: Mapping[str, Any]
    sha256: str
    contracts: Mapping[str, Mapping[str, Any]]
    interfaces: Mapping[str, Mapping[str, Any]]


@dataclass(frozen=True)
class PlannedUpdate:
    profile_id: str
    receipt_id: str
    lock_relative: str
    lock_document: Mapping[str, Any]
    lock_bytes: bytes
    receipt_relative: str
    receipt_document: Mapping[str, Any]
    receipt_bytes: bytes


@dataclass(frozen=True)
class Candidate:
    profile_id: str
    receipt_id: str
    receipt_relative: str
    receipt: Mapping[str, Any]
    lock_relative: str
    lock: Mapping[str, Any]
    platform_revision: str


def _fail(path: str, message: str) -> None:
    raise IntakeError(f"{path}: {message}")


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    return value


def _array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(path, "must be an array")
    return value


def _keys(
    value: Mapping[str, Any],
    path: str,
    expected: set[str],
) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        _fail(path, f"missing required field(s): {', '.join(missing)}")
    if extra:
        _fail(path, f"unknown field(s): {', '.join(extra)}")


def _string(
    value: Any,
    path: str,
    *,
    pattern: re.Pattern[str] | None = None,
) -> str:
    if not isinstance(value, str) or not value:
        _fail(path, "must be a non-empty string")
    if pattern is not None and not pattern.fullmatch(value):
        _fail(path, f"has invalid format: {value!r}")
    return value


def _positive_integer(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        _fail(path, "must be a positive integer")
    if isinstance(value, Decimal) and not value.is_finite():
        _fail(path, "must be a positive integer")
    integer = int(value)
    if value != integer or integer < 1:
        _fail(path, "must be a positive integer")
    return integer


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    normalized = holder_profiles._normalize_semantic_lists(value)
    return (holder_profiles._canonical_json(normalized) + "\n").encode("utf-8")


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise IntakeError(f"path is outside cradle root: {path}") from exc


def _owned_path(root: Path, relative: str, directory: Path) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise IntakeError(f"unsafe repository path: {relative!r}")
    if candidate.parent != directory or candidate.suffix != ".json":
        raise IntakeError(
            f"path is outside the owned {directory.as_posix()} directory: "
            f"{relative!r}"
        )
    resolved = (root / candidate).resolve()
    _relative(root, resolved)
    return resolved


def _interface_hash(interface: Mapping[str, Any]) -> str:
    return holder_profiles.fixture_interface_hash(
        {
            "canonicalization": CANONICALIZATION,
            "interface": interface,
        }
    )


def _validate_contract_record(
    value: Any,
    path: str,
) -> tuple[str, Mapping[str, Any]]:
    contract = _object(value, path)
    _keys(
        contract,
        path,
        {
            "device_slug",
            "kind",
            "path",
            "raw_sha256",
            "resolved_interface_sha256",
        },
    )
    slug = _string(
        contract["device_slug"],
        f"{path}.device_slug",
        pattern=SLUG_RE,
    )
    kind = _string(contract["kind"], f"{path}.kind")
    if kind not in {"fixture_interface", "shared_chassis_alias"}:
        _fail(f"{path}.kind", f"unsupported contract kind {kind!r}")
    expected_path = f"device-models/{slug}/fixture-contract.json"
    if contract["path"] != expected_path:
        _fail(f"{path}.path", f"must be {expected_path!r}")
    _string(
        contract["raw_sha256"],
        f"{path}.raw_sha256",
        pattern=SHA256_RE,
    )
    _string(
        contract["resolved_interface_sha256"],
        f"{path}.resolved_interface_sha256",
        pattern=SHA256_RE,
    )
    return slug, contract


def _validate_interface_record(
    value: Any,
    path: str,
) -> tuple[str, Mapping[str, Any]]:
    interface = _object(value, path)
    _keys(
        interface,
        path,
        {
            "sha256",
            "schema_version",
            "interface_revision",
            "coordinate_system",
            "fixture_interface",
        },
    )
    digest = _string(
        interface["sha256"],
        f"{path}.sha256",
        pattern=SHA256_RE,
    )
    if _positive_integer(
        interface["schema_version"],
        f"{path}.schema_version",
    ) != 1:
        _fail(f"{path}.schema_version", "unsupported version")
    _positive_integer(
        interface["interface_revision"],
        f"{path}.interface_revision",
    )
    _object(interface["coordinate_system"], f"{path}.coordinate_system")
    _object(interface["fixture_interface"], f"{path}.fixture_interface")
    actual = _interface_hash(interface)
    if actual != digest:
        _fail(
            f"{path}.sha256",
            f"stale interface hash: recorded {digest}, computed {actual}",
        )
    return digest, interface


def load_snapshot(path: Path) -> Snapshot:
    try:
        raw = path.read_bytes()
        document = _object(holder_profiles.load_json(path), str(path))
    except (OSError, holder_profiles.ProfileError) as exc:
        raise IntakeError(str(exc)) from exc
    if raw != _canonical_bytes(document):
        _fail(str(path), "snapshot bytes are not canonical")
    _keys(
        document,
        str(path),
        {
            "schema",
            "canonicalization",
            "source",
            "contract_schema",
            "contracts",
            "interfaces",
        },
    )
    if document["schema"] != SNAPSHOT_SCHEMA:
        _fail(f"{path}.schema", f"must be {SNAPSHOT_SCHEMA!r}")
    if document["canonicalization"] != CANONICALIZATION:
        _fail(
            f"{path}.canonicalization",
            f"must be {CANONICALIZATION!r}",
        )

    source = _object(document["source"], f"{path}.source")
    _keys(source, f"{path}.source", {"repository", "revision"})
    if source["repository"] != SOURCE_REPOSITORY:
        _fail(
            f"{path}.source.repository",
            f"must be {SOURCE_REPOSITORY!r}",
        )
    _string(
        source["revision"],
        f"{path}.source.revision",
        pattern=GIT_REV_RE,
    )

    schema = _object(document["contract_schema"], f"{path}.contract_schema")
    _keys(schema, f"{path}.contract_schema", {"path", "raw_sha256"})
    if schema["path"] != CONTRACT_SCHEMA_PATH:
        _fail(
            f"{path}.contract_schema.path",
            f"must be {CONTRACT_SCHEMA_PATH!r}",
        )
    _string(
        schema["raw_sha256"],
        f"{path}.contract_schema.raw_sha256",
        pattern=SHA256_RE,
    )

    interfaces: dict[str, Mapping[str, Any]] = {}
    interface_order: list[str] = []
    for index, item in enumerate(_array(document["interfaces"], f"{path}.interfaces")):
        digest, interface = _validate_interface_record(
            item,
            f"{path}.interfaces[{index}]",
        )
        if digest in interfaces:
            _fail(f"{path}.interfaces[{index}].sha256", "duplicate interface")
        interfaces[digest] = interface
        interface_order.append(digest)
    if not interfaces:
        _fail(f"{path}.interfaces", "must not be empty")
    if interface_order != sorted(interface_order):
        _fail(f"{path}.interfaces", "must be sorted by sha256")

    contracts: dict[str, Mapping[str, Any]] = {}
    contract_order: list[str] = []
    for index, item in enumerate(_array(document["contracts"], f"{path}.contracts")):
        slug, contract = _validate_contract_record(
            item,
            f"{path}.contracts[{index}]",
        )
        if slug in contracts:
            _fail(f"{path}.contracts[{index}].device_slug", "duplicate device")
        resolved = contract["resolved_interface_sha256"]
        if resolved not in interfaces:
            _fail(
                f"{path}.contracts[{index}].resolved_interface_sha256",
                "references an unknown interface",
            )
        contracts[slug] = contract
        contract_order.append(slug)
    if not contracts:
        _fail(f"{path}.contracts", "must not be empty")
    if contract_order != sorted(contract_order):
        _fail(f"{path}.contracts", "must be sorted by device_slug")

    return Snapshot(
        document=document,
        sha256=_sha256(raw),
        contracts=contracts,
        interfaces=interfaces,
    )


def _candidate_identity(
    profile_id: str,
    interface: Mapping[str, Any],
) -> tuple[str, str, str]:
    revision = _positive_integer(
        interface["interface_revision"],
        "candidate.interface_revision",
    )
    digest = _string(
        interface["sha256"],
        "candidate.sha256",
        pattern=SHA256_RE,
    )
    receipt_id = f"{profile_id}-r{revision}-{digest}"
    if not RECEIPT_ID_RE.fullmatch(receipt_id):
        raise IntakeError(f"invalid generated receipt id: {receipt_id}")
    lock_relative = (
        CANDIDATE_LOCK_DIRECTORY / f"{receipt_id}.json"
    ).as_posix()
    receipt_relative = (RECEIPT_DIRECTORY / f"{receipt_id}.json").as_posix()
    return receipt_id, lock_relative, receipt_relative


def _candidate_documents(
    record: qualification_ci.ProfileRecord,
    snapshot: Snapshot,
    contracts: Sequence[Mapping[str, Any]],
    interface: Mapping[str, Any],
) -> PlannedUpdate:
    receipt_id, lock_relative, receipt_relative = _candidate_identity(
        record.profile_id,
        interface,
    )
    source = snapshot.document["source"]
    lock = {
        "schema": CANDIDATE_LOCK_SCHEMA,
        "canonicalization": CANONICALIZATION,
        "source": {
            "repository": source["repository"],
            "revision": source["revision"],
            "contracts": list(contracts),
        },
        "interface": interface,
    }
    lock_bytes = _canonical_bytes(lock)
    lock_sha256 = _sha256(lock_bytes)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "receipt_id": receipt_id,
        "state": AWAITING_HOLDER_DESIGN,
        "profile": {
            "profile_id": record.profile_id,
            "profile_path": record.relative_path,
            "device_slugs": list(record.device_slugs),
        },
        "accepted": {
            "fixture_lock": record.fixture_lock_path,
            "fixture_lock_sha256": record.fixture_lock_sha256,
            "fixture_interface_revision": record.resolved.lock_state["revision"],
            "fixture_interface_sha256": record.fixture_sha256,
        },
        "platform": {
            "repository": source["repository"],
            "revision": source["revision"],
            "snapshot_sha256": snapshot.sha256,
            "contracts": list(contracts),
        },
        "candidate": {
            "interface_revision": interface["interface_revision"],
            "fixture_interface_sha256": interface["sha256"],
            "fixture_lock": lock_relative,
            "fixture_lock_sha256": lock_sha256,
        },
    }
    receipt_bytes = _canonical_bytes(receipt)
    return PlannedUpdate(
        profile_id=record.profile_id,
        receipt_id=receipt_id,
        lock_relative=lock_relative,
        lock_document=lock,
        lock_bytes=lock_bytes,
        receipt_relative=receipt_relative,
        receipt_document=receipt,
        receipt_bytes=receipt_bytes,
    )


def _classify_output(root: Path, relative: str, expected: bytes) -> bool:
    path = (root / relative).resolve()
    _relative(root, path)
    if not path.exists():
        return True
    if not path.is_file():
        raise IntakeError(f"candidate output is not a file: {relative}")
    if path.read_bytes() != expected:
        raise IntakeError(
            f"candidate output collision at {relative}; existing bytes differ"
        )
    return False


def plan_updates(
    root: Path,
    snapshot: Snapshot,
) -> tuple[Mapping[str, Any], list[PlannedUpdate]]:
    root = root.resolve()
    try:
        registry = qualification_ci.discover_registry(root)
    except qualification_ci.QualificationCiError as exc:
        raise IntakeError(str(exc)) from exc
    existing = discover_candidates(root, registry)
    existing_by_profile = {
        candidate.profile_id: candidate for candidate in existing.values()
    }

    results: list[dict[str, Any]] = []
    updates: list[PlannedUpdate] = []
    write_paths: list[str] = []
    for profile_id in sorted(registry):
        record = registry[profile_id]
        if record.status != qualification_ci.QUALIFIED:
            # An unqualified/custom holder is already in the manual design
            # lane. It has no accepted geometry to preserve and therefore
            # must not create or block the immutable qualified-refresh queue.
            # Its committed fixture lock remains the prototype source pin.
            contracts = [
                snapshot.contracts[slug]
                for slug in record.device_slugs
                if slug in snapshot.contracts
            ]
            results.append(
                {
                    "profile_id": profile_id,
                    "profile_path": record.relative_path,
                    "device_slugs": list(record.device_slugs),
                    "accepted_interface_sha256": record.fixture_sha256,
                    "resolved_interface_sha256": (
                        contracts[0]["resolved_interface_sha256"]
                        if len(contracts) == len(record.device_slugs)
                        and len(
                            {
                                contract["resolved_interface_sha256"]
                                for contract in contracts
                            }
                        )
                        == 1
                        else None
                    ),
                    "status": "unqualified_manual",
                }
            )
            continue
        selected: list[Mapping[str, Any]] = []
        missing: list[str] = []
        for slug in record.device_slugs:
            contract = snapshot.contracts.get(slug)
            if contract is None:
                missing.append(slug)
            else:
                selected.append(contract)
        if missing:
            raise IntakeError(
                f"profile {profile_id!r}: snapshot is missing subscribed "
                f"device(s): {', '.join(missing)}"
            )
        selected.sort(key=lambda item: item["device_slug"])
        resolved_hashes = {
            str(contract["resolved_interface_sha256"])
            for contract in selected
        }
        if len(resolved_hashes) != 1:
            raise IntakeError(
                f"profile {profile_id!r}: subscribed devices resolve mixed "
                f"interfaces: {', '.join(sorted(resolved_hashes))}"
            )
        resolved_hash = next(iter(resolved_hashes))
        result: dict[str, Any] = {
            "profile_id": profile_id,
            "profile_path": record.relative_path,
            "device_slugs": list(record.device_slugs),
            "accepted_interface_sha256": record.fixture_sha256,
            "resolved_interface_sha256": resolved_hash,
        }
        if resolved_hash == record.fixture_sha256:
            result["status"] = "no_change"
            results.append(result)
            continue
        interface = snapshot.interfaces[resolved_hash]
        candidate_revision = _positive_integer(
            interface["interface_revision"],
            f"profile {profile_id}.candidate.interface_revision",
        )
        accepted_revision = int(record.resolved.lock_state["revision"])
        if candidate_revision <= accepted_revision:
            raise IntakeError(
                f"profile {profile_id!r}: changed interface revision "
                f"{candidate_revision} must exceed accepted revision "
                f"{accepted_revision}"
            )
        update = _candidate_documents(
            record,
            snapshot,
            selected,
            interface,
        )
        prior = existing_by_profile.get(profile_id)
        if prior is not None and prior.receipt_id != update.receipt_id:
            raise IntakeError(
                f"profile {profile_id!r}: unresolved candidate "
                f"{prior.receipt_id!r} conflicts with {update.receipt_id!r}"
            )
        for relative, payload in (
            (update.lock_relative, update.lock_bytes),
            (update.receipt_relative, update.receipt_bytes),
        ):
            if _classify_output(root, relative, payload):
                write_paths.append(relative)
        result.update(
            {
                "status": "candidate_update",
                "candidate": {
                    "receipt_id": update.receipt_id,
                    "interface_revision": interface["interface_revision"],
                    "fixture_interface_sha256": resolved_hash,
                    "fixture_lock": update.lock_relative,
                    "fixture_lock_sha256": _sha256(update.lock_bytes),
                    "receipt": update.receipt_relative,
                    "receipt_sha256": _sha256(update.receipt_bytes),
                },
            }
        )
        results.append(result)
        updates.append(update)

    write_paths.sort()
    plan = {
        "schema": PLAN_SCHEMA,
        "status": "candidate_updates" if updates else "no_change",
        "snapshot": {
            "repository": snapshot.document["source"]["repository"],
            "revision": snapshot.document["source"]["revision"],
            "sha256": snapshot.sha256,
        },
        "profiles": results,
        "write_paths": write_paths,
    }
    return plan, updates


def _atomic_write_new(path: Path, payload: bytes) -> bool:
    if path.exists():
        if path.is_file() and path.read_bytes() == payload:
            return False
        raise IntakeError(f"refusing to replace existing candidate path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.link(temporary, path)
        return True
    except FileExistsError as exc:
        if path.is_file() and path.read_bytes() == payload:
            return False
        raise IntakeError(f"candidate path appeared concurrently: {path}") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def stage_updates(
    root: Path,
    snapshot: Snapshot,
) -> Mapping[str, Any]:
    plan, updates = plan_updates(root, snapshot)
    expected_paths = set(plan["write_paths"])
    for update in updates:
        for relative, payload, directory in (
            (
                update.lock_relative,
                update.lock_bytes,
                CANDIDATE_LOCK_DIRECTORY,
            ),
            (
                update.receipt_relative,
                update.receipt_bytes,
                RECEIPT_DIRECTORY,
            ),
        ):
            path = _owned_path(root, relative, directory)
            wrote = _atomic_write_new(path, payload)
            if wrote and relative not in expected_paths:
                raise IntakeError(f"unexpected staged path: {relative}")
    discover_candidates(root)
    return plan


def _validate_candidate_lock(
    path: Path,
) -> Mapping[str, Any]:
    try:
        raw = path.read_bytes()
        lock = _object(holder_profiles.load_json(path), str(path))
    except (OSError, holder_profiles.ProfileError) as exc:
        raise IntakeError(str(exc)) from exc
    if raw != _canonical_bytes(lock):
        _fail(str(path), "candidate lock bytes are not canonical")
    _keys(
        lock,
        str(path),
        {"schema", "canonicalization", "source", "interface"},
    )
    if lock["schema"] != CANDIDATE_LOCK_SCHEMA:
        _fail(f"{path}.schema", f"must be {CANDIDATE_LOCK_SCHEMA!r}")
    if lock["canonicalization"] != CANONICALIZATION:
        _fail(
            f"{path}.canonicalization",
            f"must be {CANONICALIZATION!r}",
        )
    source = _object(lock["source"], f"{path}.source")
    _keys(source, f"{path}.source", {"repository", "revision", "contracts"})
    if source["repository"] != SOURCE_REPOSITORY:
        _fail(f"{path}.source.repository", f"must be {SOURCE_REPOSITORY!r}")
    _string(
        source["revision"],
        f"{path}.source.revision",
        pattern=GIT_REV_RE,
    )
    contracts: list[Mapping[str, Any]] = []
    slugs: list[str] = []
    for index, item in enumerate(_array(source["contracts"], f"{path}.source.contracts")):
        slug, contract = _validate_contract_record(
            item,
            f"{path}.source.contracts[{index}]",
        )
        slugs.append(slug)
        contracts.append(contract)
    if not contracts:
        _fail(f"{path}.source.contracts", "must not be empty")
    if slugs != sorted(set(slugs)):
        _fail(
            f"{path}.source.contracts",
            "device slugs must be unique and sorted",
        )
    digest, interface = _validate_interface_record(
        lock["interface"],
        f"{path}.interface",
    )
    for index, contract in enumerate(contracts):
        if contract["resolved_interface_sha256"] != digest:
            _fail(
                f"{path}.source.contracts[{index}]",
                "resolved interface does not match candidate payload",
            )
    return {
        "document": lock,
        "source": source,
        "contracts": contracts,
        "interface": interface,
        "sha256": _sha256(raw),
    }


def _validate_receipt(
    root: Path,
    path: Path,
    lock_states: Mapping[str, Mapping[str, Any]],
    registry: Mapping[str, qualification_ci.ProfileRecord],
) -> Candidate:
    try:
        raw = path.read_bytes()
        receipt = _object(holder_profiles.load_json(path), str(path))
    except (OSError, holder_profiles.ProfileError) as exc:
        raise IntakeError(str(exc)) from exc
    if raw != _canonical_bytes(receipt):
        _fail(str(path), "receipt bytes are not canonical")
    _keys(
        receipt,
        str(path),
        {
            "schema",
            "receipt_id",
            "state",
            "profile",
            "accepted",
            "platform",
            "candidate",
        },
    )
    if receipt["schema"] != RECEIPT_SCHEMA:
        _fail(f"{path}.schema", f"must be {RECEIPT_SCHEMA!r}")
    receipt_id = _string(
        receipt["receipt_id"],
        f"{path}.receipt_id",
        pattern=RECEIPT_ID_RE,
    )
    if path.stem != receipt_id:
        _fail(f"{path}.receipt_id", f"must match filename stem {path.stem!r}")
    if receipt["state"] != AWAITING_HOLDER_DESIGN:
        _fail(
            f"{path}.state",
            f"must be {AWAITING_HOLDER_DESIGN!r}",
        )

    profile = _object(receipt["profile"], f"{path}.profile")
    _keys(
        profile,
        f"{path}.profile",
        {"profile_id", "profile_path", "device_slugs"},
    )
    profile_id = _string(
        profile["profile_id"],
        f"{path}.profile.profile_id",
        pattern=SLUG_RE,
    )
    record = registry.get(profile_id)
    if record is None:
        _fail(f"{path}.profile.profile_id", "references an unknown profile")
    slugs = [
        _string(item, f"{path}.profile.device_slugs", pattern=SLUG_RE)
        for item in _array(
            profile["device_slugs"],
            f"{path}.profile.device_slugs",
        )
    ]
    if slugs != list(record.device_slugs):
        _fail(
            f"{path}.profile.device_slugs",
            "does not exactly match the subscribed holder devices",
        )
    if profile["profile_path"] != record.relative_path:
        _fail(
            f"{path}.profile.profile_path",
            "does not match the current holder profile path",
        )

    accepted = _object(receipt["accepted"], f"{path}.accepted")
    _keys(
        accepted,
        f"{path}.accepted",
        {
            "fixture_lock",
            "fixture_lock_sha256",
            "fixture_interface_revision",
            "fixture_interface_sha256",
        },
    )
    expected_accepted = {
        "fixture_lock": record.fixture_lock_path,
        "fixture_lock_sha256": record.fixture_lock_sha256,
        "fixture_interface_revision": record.resolved.lock_state["revision"],
        "fixture_interface_sha256": record.fixture_sha256,
    }
    if accepted != expected_accepted:
        _fail(
            f"{path}.accepted",
            "does not exactly identify the active accepted fixture lock",
        )

    platform = _object(receipt["platform"], f"{path}.platform")
    _keys(
        platform,
        f"{path}.platform",
        {
            "repository",
            "revision",
            "snapshot_sha256",
            "contracts",
        },
    )
    if platform["repository"] != SOURCE_REPOSITORY:
        _fail(f"{path}.platform.repository", f"must be {SOURCE_REPOSITORY!r}")
    _string(
        platform["revision"],
        f"{path}.platform.revision",
        pattern=GIT_REV_RE,
    )
    _string(
        platform["snapshot_sha256"],
        f"{path}.platform.snapshot_sha256",
        pattern=SHA256_RE,
    )

    candidate = _object(receipt["candidate"], f"{path}.candidate")
    _keys(
        candidate,
        f"{path}.candidate",
        {
            "interface_revision",
            "fixture_interface_sha256",
            "fixture_lock",
            "fixture_lock_sha256",
        },
    )
    revision = _positive_integer(
        candidate["interface_revision"],
        f"{path}.candidate.interface_revision",
    )
    digest = _string(
        candidate["fixture_interface_sha256"],
        f"{path}.candidate.fixture_interface_sha256",
        pattern=SHA256_RE,
    )
    lock_relative = _string(
        candidate["fixture_lock"],
        f"{path}.candidate.fixture_lock",
    )
    _owned_path(root, lock_relative, CANDIDATE_LOCK_DIRECTORY)
    lock_state = lock_states.get(lock_relative)
    if lock_state is None:
        _fail(f"{path}.candidate.fixture_lock", "candidate lock is missing")
    _string(
        candidate["fixture_lock_sha256"],
        f"{path}.candidate.fixture_lock_sha256",
        pattern=SHA256_RE,
    )
    if candidate["fixture_lock_sha256"] != lock_state["sha256"]:
        _fail(
            f"{path}.candidate.fixture_lock_sha256",
            "does not match candidate lock bytes",
        )
    lock = lock_state["document"]
    if platform["repository"] != lock["source"]["repository"]:
        _fail(f"{path}.platform.repository", "differs from candidate lock")
    if platform["revision"] != lock["source"]["revision"]:
        _fail(f"{path}.platform.revision", "differs from candidate lock")
    if _canonical_bytes(platform["contracts"]) != _canonical_bytes(
        lock["source"]["contracts"]
    ):
        _fail(f"{path}.platform.contracts", "differs from candidate lock")
    if revision != lock["interface"]["interface_revision"]:
        _fail(f"{path}.candidate.interface_revision", "differs from lock")
    if digest != lock["interface"]["sha256"]:
        _fail(
            f"{path}.candidate.fixture_interface_sha256",
            "differs from lock",
        )
    if digest == record.fixture_sha256:
        _fail(
            f"{path}.candidate.fixture_interface_sha256",
            "must differ from the accepted interface",
        )
    if revision <= int(record.resolved.lock_state["revision"]):
        _fail(
            f"{path}.candidate.interface_revision",
            "must exceed the accepted interface revision",
        )
    if [
        contract["device_slug"] for contract in lock_state["contracts"]
    ] != list(record.device_slugs):
        _fail(
            f"{path}.platform.contracts",
            "does not exactly cover the subscribed holder devices",
        )
    expected_id, expected_lock, expected_receipt = _candidate_identity(
        profile_id,
        lock["interface"],
    )
    if receipt_id != expected_id:
        _fail(f"{path}.receipt_id", "does not match candidate identity")
    if lock_relative != expected_lock:
        _fail(
            f"{path}.candidate.fixture_lock",
            f"must be {expected_lock!r}",
        )
    relative = _relative(root, path)
    if relative != expected_receipt:
        _fail(str(path), f"receipt path must be {expected_receipt!r}")
    return Candidate(
        profile_id=profile_id,
        receipt_id=receipt_id,
        receipt_relative=relative,
        receipt=receipt,
        lock_relative=lock_relative,
        lock=lock,
        platform_revision=str(platform["revision"]),
    )


def discover_candidates(
    root: Path,
    registry: Mapping[str, qualification_ci.ProfileRecord] | None = None,
) -> dict[str, Candidate]:
    root = root.resolve()
    if registry is None:
        try:
            registry = qualification_ci.discover_registry(root)
        except qualification_ci.QualificationCiError as exc:
            raise IntakeError(str(exc)) from exc
    lock_directory = root / CANDIDATE_LOCK_DIRECTORY
    lock_states: dict[str, Mapping[str, Any]] = {}
    if lock_directory.exists():
        for path in sorted(lock_directory.glob("*.json")):
            relative = _relative(root, path)
            lock_states[relative] = _validate_candidate_lock(path)
    receipt_directory = root / RECEIPT_DIRECTORY
    candidates: dict[str, Candidate] = {}
    locks_referenced: set[str] = set()
    profiles_seen: dict[str, str] = {}
    if receipt_directory.exists():
        for path in sorted(receipt_directory.glob("*.json")):
            candidate = _validate_receipt(
                root,
                path,
                lock_states,
                registry,
            )
            if candidate.receipt_id in candidates:
                raise IntakeError(
                    f"duplicate candidate receipt id: {candidate.receipt_id}"
                )
            prior = profiles_seen.get(candidate.profile_id)
            if prior is not None:
                raise IntakeError(
                    f"profile {candidate.profile_id!r} has multiple unresolved "
                    f"candidate receipts: {prior}, {candidate.receipt_id}"
                )
            profiles_seen[candidate.profile_id] = candidate.receipt_id
            candidates[candidate.receipt_id] = candidate
            locks_referenced.add(candidate.lock_relative)
    unreferenced = sorted(set(lock_states) - locks_referenced)
    if unreferenced:
        raise IntakeError(
            "unreferenced candidate lock(s): " + ", ".join(unreferenced)
        )
    return dict(sorted(candidates.items()))


def verify_candidate_source(
    root: Path,
    receipt_path: Path,
    platform_root: Path,
) -> Candidate:
    candidates = discover_candidates(root)
    relative = _relative(
        root,
        receipt_path if receipt_path.is_absolute() else root / receipt_path,
    )
    matches = [
        candidate
        for candidate in candidates.values()
        if candidate.receipt_relative == relative
    ]
    if len(matches) != 1:
        raise IntakeError(f"candidate receipt is not discovered: {relative}")
    candidate = matches[0]
    platform_root = platform_root.resolve()
    revision = candidate.platform_revision
    try:
        inside = subprocess.run(
            ["git", "-C", str(platform_root), "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            text=True,
        )
        commit = subprocess.run(
            [
                "git",
                "-C",
                str(platform_root),
                "rev-parse",
                f"{revision}^{{commit}}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise IntakeError(f"cannot run git: {exc}") from exc
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise IntakeError(f"platform root is not a Git checkout: {platform_root}")
    if commit.returncode != 0 or commit.stdout.strip() != revision:
        raise IntakeError(
            f"platform checkout does not contain candidate revision {revision}"
        )

    interface = candidate.lock["interface"]
    full_seen = False
    for contract in candidate.lock["source"]["contracts"]:
        slug = str(contract["device_slug"])
        source_path = str(contract["path"])
        result = subprocess.run(
            [
                "git",
                "-C",
                str(platform_root),
                "show",
                f"{revision}:{source_path}",
            ],
            check=False,
            capture_output=True,
        )
        if result.returncode != 0:
            raise IntakeError(
                f"cannot read platform {revision}:{source_path}: "
                f"{result.stderr.decode(errors='replace').strip()}"
            )
        raw_hash = _sha256(result.stdout)
        if raw_hash != contract["raw_sha256"]:
            raise IntakeError(
                f"raw source mismatch for {slug}: expected "
                f"{contract['raw_sha256']}, got {raw_hash}"
            )
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as handle:
            source_temp = Path(handle.name)
            handle.write(result.stdout)
        try:
            source_document = _object(
                holder_profiles.load_json(source_temp),
                f"platform:{source_path}",
            )
        except holder_profiles.ProfileError as exc:
            raise IntakeError(str(exc)) from exc
        finally:
            source_temp.unlink(missing_ok=True)
        if source_document.get("kind") != contract["kind"]:
            raise IntakeError(f"contract kind mismatch for {slug}")
        device = _object(
            source_document.get("device"),
            f"platform:{source_path}.device",
        )
        if device.get("slug") != slug:
            raise IntakeError(f"device slug mismatch for {slug}")
        if contract["kind"] == "fixture_interface":
            full_seen = True
            comparisons = {
                "schema_version": interface["schema_version"],
                "interface_revision": interface["interface_revision"],
                "fixture_interface_sha256": interface["sha256"],
                "coordinate_system": interface["coordinate_system"],
                "fixture_interface": interface["fixture_interface"],
            }
            for key, expected in comparisons.items():
                if _canonical_bytes(source_document.get(key)) != _canonical_bytes(
                    expected
                ):
                    raise IntakeError(
                        f"candidate {key} differs from platform source for {slug}"
                    )
        elif (
            source_document.get("expected_fixture_interface_sha256")
            != interface["sha256"]
        ):
            raise IntakeError(
                f"alias {slug} does not resolve the candidate interface"
            )
        print(
            f"fixture_candidate_source=pass device={slug} "
            f"raw_sha256={raw_hash}"
        )
    if not full_seen:
        raise IntakeError("candidate lock contains no full source contract")
    return candidate


def _write_external(
    root: Path,
    output: Path | None,
    payload: bytes,
) -> None:
    if output is None:
        sys.stdout.buffer.write(payload)
        return
    output = output.expanduser().resolve()
    try:
        output.relative_to(root.resolve())
    except ValueError:
        pass
    else:
        raise IntakeError("generated plan output must remain outside the repository")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=output.parent,
            prefix=f".{output.name}.",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: Sequence[str] | None = None) -> int:
    default_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--snapshot", type=Path, required=True)
    plan_parser.add_argument("--output", type=Path)

    stage_parser = subparsers.add_parser("stage")
    stage_parser.add_argument("--snapshot", type=Path, required=True)

    subparsers.add_parser("validate-candidates")
    subparsers.add_parser("matrix")

    verify_parser = subparsers.add_parser("verify-source")
    verify_parser.add_argument("--receipt", type=Path, required=True)
    verify_parser.add_argument("--platform-root", type=Path, required=True)

    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "plan":
            snapshot = load_snapshot(args.snapshot)
            plan, _ = plan_updates(root, snapshot)
            _write_external(root, args.output, _canonical_bytes(plan))
            if args.output is not None:
                print(
                    f"fixture_intake_plan={plan['status']} "
                    f"snapshot_revision={plan['snapshot']['revision']} "
                    f"writes={len(plan['write_paths'])} output={args.output}"
                )
        elif args.command == "stage":
            snapshot = load_snapshot(args.snapshot)
            plan = stage_updates(root, snapshot)
            print(
                f"fixture_intake_stage={plan['status']} "
                f"snapshot_revision={plan['snapshot']['revision']} "
                f"writes={len(plan['write_paths'])}"
            )
        elif args.command == "validate-candidates":
            candidates = discover_candidates(root)
            print(f"fixture_candidates=pass count={len(candidates)}")
        elif args.command == "matrix":
            candidates = discover_candidates(root)
            matrix = {
                "include": [
                    {
                        "profile_id": candidate.profile_id,
                        "receipt_path": candidate.receipt_relative,
                        "candidate_lock_path": candidate.lock_relative,
                        "platform_revision": candidate.platform_revision,
                    }
                    for candidate in candidates.values()
                ]
            }
            sys.stdout.buffer.write(_canonical_bytes(matrix))
        elif args.command == "verify-source":
            candidate = verify_candidate_source(
                root,
                args.receipt,
                args.platform_root,
            )
            print(
                "fixture_candidate_verify=pass "
                f"profile={candidate.profile_id} "
                f"revision={candidate.platform_revision}"
            )
        else:  # pragma: no cover
            raise IntakeError(f"unsupported command: {args.command}")
    except (
        IntakeError,
        OSError,
        holder_profiles.ProfileError,
        qualification_ci.QualificationCiError,
    ) as exc:
        print(f"fixture_intake_error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
