#!/usr/bin/env python3
"""Validate and render source-owned PocketForge DUT holder profiles.

The committed profile and fixture lock are the inputs.  OpenSCAD meshes are
generated outputs.  No normal command rewrites a profile, lock, qualification
record, or CAD source.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from qualified_geometry import (
    QualificationError,
    check_toolchain,
    compare_artifact,
)


PROFILE_SCHEMA = "pocketforge-holder-profile-v1"
LOCK_SCHEMA = "pocketforge-fixture-lock-v1"
CANONICALIZATION = "pocketforge-fixture-interface-json-v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_REV_RE = re.compile(r"^[0-9a-f]{40}$")
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UNORDERED_STRING_LIST_KEYS = {"contact_modes", "protects", "region_refs"}
SURFACE_POSE = {
    "bottom_edge": ("x", 90),
    "top_edge": ("x", -90),
    "left_edge": ("y", 0),
    "right_edge": ("y", 180),
}
PERIMETER_CONTACT_SURFACES = {
    "bottom_left": "bottom_edge",
    "bottom_right": "bottom_edge",
    "left_datum": "left_edge",
    "right_datum": "right_edge",
    "top_left": "top_edge",
    "top_right": "top_edge",
}
QUALIFIED_ARTIFACTS = {
    "carrier_body",
    "fit_coupon",
    "j_hook",
    "j_hook_set",
}


class ProfileError(ValueError):
    """A holder profile, fixture lock, or generated artifact is invalid."""


def _fail(path: str, message: str) -> None:
    raise ProfileError(f"{path}: {message}")


def _reject_constant(token: str) -> None:
    raise ProfileError(f"JSON contains non-finite number {token}")


def _reject_duplicate_keys(
    pairs: Sequence[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProfileError(f"JSON contains duplicate object key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_float=Decimal,
            parse_int=Decimal,
            parse_constant=_reject_constant,
            object_pairs_hook=_reject_duplicate_keys,
        )
    except OSError as exc:
        raise ProfileError(f"{path}: cannot read: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ProfileError(
            f"{path}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    return value


def _array(value: Any, path: str) -> Sequence[Any]:
    if not isinstance(value, list):
        _fail(path, "must be an array")
    return value


def _keys(
    value: Mapping[str, Any],
    path: str,
    required: Iterable[str],
    optional: Iterable[str] = (),
) -> None:
    required_set = set(required)
    allowed = required_set | set(optional)
    missing = sorted(required_set - value.keys())
    extra = sorted(value.keys() - allowed)
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


def _number(
    value: Any,
    path: str,
    *,
    minimum: Decimal | None = None,
    exclusive_minimum: Decimal | None = None,
) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        _fail(path, "must be a finite number")
    result = value if isinstance(value, Decimal) else Decimal(str(value))
    if not result.is_finite():
        _fail(path, "must be a finite number")
    if minimum is not None and result < minimum:
        _fail(path, f"must be >= {minimum}")
    if exclusive_minimum is not None and result <= exclusive_minimum:
        _fail(path, f"must be > {exclusive_minimum}")
    return result


def _integer(value: Any, path: str, *, minimum: int = 0) -> int:
    result = _number(value, path)
    if result != result.to_integral_value():
        _fail(path, "must be an integer")
    integer = int(result)
    if integer < minimum:
        _fail(path, f"must be >= {minimum}")
    return integer


def _boolean(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        _fail(path, "must be a boolean")
    return value


def _vector(
    value: Any,
    path: str,
    length: int,
    *,
    minimum: Decimal | None = None,
) -> tuple[Decimal, ...]:
    items = _array(value, path)
    if len(items) != length:
        _fail(path, f"must contain exactly {length} numbers")
    return tuple(
        _number(item, f"{path}[{index}]", minimum=minimum)
        for index, item in enumerate(items)
    )


def _string_list(
    value: Any,
    path: str,
    *,
    minimum: int = 0,
    pattern: re.Pattern[str] | None = None,
) -> list[str]:
    items = _array(value, path)
    if len(items) < minimum:
        _fail(path, f"must contain at least {minimum} item(s)")
    result = [
        _string(item, f"{path}[{index}]", pattern=pattern)
        for index, item in enumerate(items)
    ]
    if len(result) != len(set(result)):
        _fail(path, "must not contain duplicates")
    return result


def _project_path(root: Path, relative: Any, field: str) -> Path:
    text = _string(relative, field)
    candidate = Path(text)
    if candidate.is_absolute():
        _fail(field, "must be relative to the cradle root")
    path = (root / candidate).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        _fail(field, f"path escapes cradle root: {text}")
    return path


def _canonical_number(value: int | float | Decimal) -> str:
    number = value if isinstance(value, Decimal) else Decimal(str(value))
    if not number.is_finite():
        raise ProfileError("cannot canonicalize non-finite number")
    if number == 0:
        return "0"
    rendered = format(number, "f")
    return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered


def _normalize_semantic_lists(value: Any, parent_key: str | None = None) -> Any:
    if isinstance(value, dict):
        return {
            key: _normalize_semantic_lists(child, key)
            for key, child in value.items()
        }
    if isinstance(value, list):
        normalized = [
            _normalize_semantic_lists(child, parent_key) for child in value
        ]
        if normalized and all(
            isinstance(child, dict) and isinstance(child.get("id"), str)
            for child in normalized
        ):
            return sorted(normalized, key=lambda child: child["id"])
        if parent_key in UNORDERED_STRING_LIST_KEYS and all(
            isinstance(child, str) for child in normalized
        ):
            return sorted(normalized)
        return normalized
    return value


def _canonical_json(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
        return _canonical_number(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(_canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{_canonical_json(key)}:{_canonical_json(value[key])}"
            for key in sorted(value)
        ) + "}"
    raise ProfileError(
        f"cannot canonicalize value of type {type(value).__name__}"
    )


def fixture_interface_hash(lock: Mapping[str, Any]) -> str:
    interface = _object(lock.get("interface"), "lock.interface")
    payload = {
        "canonicalization": lock.get("canonicalization"),
        "schema_version": interface.get("schema_version"),
        "coordinate_system": interface.get("coordinate_system"),
        "fixture_interface": interface.get("fixture_interface"),
    }
    encoded = _canonical_json(_normalize_semantic_lists(payload)).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _id_map(value: Any, path: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(_array(value, path)):
        item_path = f"{path}[{index}]"
        obj = _object(item, item_path)
        item_id = _string(obj.get("id"), f"{item_path}.id", pattern=ID_RE)
        if item_id in result:
            _fail(f"{item_path}.id", f"duplicate id {item_id!r}")
        result[item_id] = obj
    return result


def validate_fixture_lock(
    root: Path,
    lock_path: Path,
    lock: Mapping[str, Any],
) -> dict[str, Any]:
    _keys(
        lock,
        str(lock_path),
        {"schema", "canonicalization", "source", "interface"},
    )
    if lock["schema"] != LOCK_SCHEMA:
        _fail(f"{lock_path}.schema", f"must be {LOCK_SCHEMA!r}")
    if lock["canonicalization"] != CANONICALIZATION:
        _fail(
            f"{lock_path}.canonicalization",
            f"must be {CANONICALIZATION!r}",
        )

    source = _object(lock["source"], f"{lock_path}.source")
    _keys(source, f"{lock_path}.source", {"repository", "revision", "contracts"})
    repository = _string(source["repository"], f"{lock_path}.source.repository")
    if repository != "https://github.com/pocketforge-os/platform.git":
        _fail(
            f"{lock_path}.source.repository",
            "must pin the canonical PocketForge platform repository",
        )
    _string(
        source["revision"],
        f"{lock_path}.source.revision",
        pattern=GIT_REV_RE,
    )
    contracts: dict[str, Mapping[str, Any]] = {}
    contract_paths: set[str] = set()
    full_count = 0
    for index, item in enumerate(
        _array(source["contracts"], f"{lock_path}.source.contracts")
    ):
        item_path = f"{lock_path}.source.contracts[{index}]"
        contract = _object(item, item_path)
        _keys(
            contract,
            item_path,
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
            f"{item_path}.device_slug",
            pattern=SLUG_RE,
        )
        if slug in contracts:
            _fail(f"{item_path}.device_slug", f"duplicate device {slug!r}")
        kind = _string(contract["kind"], f"{item_path}.kind")
        if kind not in {"fixture_interface", "shared_chassis_alias"}:
            _fail(f"{item_path}.kind", f"unsupported contract kind {kind!r}")
        full_count += kind == "fixture_interface"
        path_text = _string(contract["path"], f"{item_path}.path")
        if (
            Path(path_text).is_absolute()
            or ".." in Path(path_text).parts
            or not path_text.endswith("/fixture-contract.json")
        ):
            _fail(f"{item_path}.path", "must be a safe platform contract path")
        if path_text in contract_paths:
            _fail(f"{item_path}.path", f"duplicate source path {path_text!r}")
        contract_paths.add(path_text)
        _string(
            contract["raw_sha256"],
            f"{item_path}.raw_sha256",
            pattern=SHA256_RE,
        )
        _string(
            contract["resolved_interface_sha256"],
            f"{item_path}.resolved_interface_sha256",
            pattern=SHA256_RE,
        )
        contracts[slug] = contract
    if full_count != 1:
        _fail(
            f"{lock_path}.source.contracts",
            "a fixture lock needs exactly one full contract",
        )

    interface = _object(lock["interface"], f"{lock_path}.interface")
    _keys(
        interface,
        f"{lock_path}.interface",
        {
            "schema_version",
            "interface_revision",
            "sha256",
            "coordinate_system",
            "fixture_interface",
        },
    )
    if _integer(
        interface["schema_version"],
        f"{lock_path}.interface.schema_version",
        minimum=1,
    ) != 1:
        _fail(f"{lock_path}.interface.schema_version", "unsupported version")
    revision = _integer(
        interface["interface_revision"],
        f"{lock_path}.interface.interface_revision",
        minimum=1,
    )
    recorded_hash = _string(
        interface["sha256"],
        f"{lock_path}.interface.sha256",
        pattern=SHA256_RE,
    )
    actual_hash = fixture_interface_hash(lock)
    if recorded_hash != actual_hash:
        _fail(
            f"{lock_path}.interface.sha256",
            f"stale lock hash: recorded {recorded_hash}, computed {actual_hash}",
        )
    for slug, contract in contracts.items():
        if contract["resolved_interface_sha256"] != actual_hash:
            _fail(
                f"{lock_path}.source.contracts[{slug}]",
                "resolved hash does not match the locked interface",
            )

    coordinate = _object(
        interface["coordinate_system"],
        f"{lock_path}.interface.coordinate_system",
    )
    _keys(
        coordinate,
        "lock.interface.coordinate_system",
        {"units", "handedness", "origin", "axes"},
    )
    if (
        coordinate["units"] != "mm"
        or coordinate["handedness"] != "right_handed"
        or coordinate["origin"] != "rear_left_bottom_nominal_shell_datum"
    ):
        _fail(
            f"{lock_path}.interface.coordinate_system",
            "unsupported coordinate convention",
        )
    axes = _object(
        coordinate["axes"],
        f"{lock_path}.interface.coordinate_system.axes",
    )
    _keys(
        axes,
        f"{lock_path}.interface.coordinate_system.axes",
        {"x", "y", "z"},
    )
    if axes != {
        "x": "physical_left_to_right",
        "y": "physical_bottom_to_top",
        "z": "physical_rear_to_front",
    }:
        _fail(
            f"{lock_path}.interface.coordinate_system.axes",
            "unsupported axis directions",
        )

    fixture = _object(
        interface["fixture_interface"],
        f"{lock_path}.interface.fixture_interface",
    )
    _keys(
        fixture,
        f"{lock_path}.interface.fixture_interface",
        {
            "envelope",
            "local_depths",
            "contact_regions",
            "keepouts",
            "access_regions",
            "datums",
            "clearance_requirements",
        },
    )
    envelope = _object(fixture["envelope"], "lock.fixture_interface.envelope")
    bounds = _object(
        envelope.get("xy_bounds_mm"),
        "lock.fixture_interface.envelope.xy_bounds_mm",
    )
    _keys(bounds, "lock.fixture_interface.envelope.xy_bounds_mm", {"min", "max"})
    xy_min = _vector(bounds["min"], "lock.fixture_interface.envelope.min", 2)
    xy_max = _vector(bounds["max"], "lock.fixture_interface.envelope.max", 2)
    if xy_min != (Decimal(0), Decimal(0)):
        _fail(
            "lock.fixture_interface.envelope.min",
            "perimeter_j_hook_v1 requires a zero XY fixture origin",
        )
    if any(a >= b for a, b in zip(xy_min, xy_max)):
        _fail("lock.fixture_interface.envelope", "invalid XY bounds")

    depths = _id_map(fixture["local_depths"], "lock.fixture_interface.local_depths")
    contacts = _id_map(
        fixture["contact_regions"],
        "lock.fixture_interface.contact_regions",
    )
    access = _id_map(
        fixture["access_regions"],
        "lock.fixture_interface.access_regions",
    )
    datums = _id_map(fixture["datums"], "lock.fixture_interface.datums")
    clearances = _id_map(
        fixture["clearance_requirements"],
        "lock.fixture_interface.clearance_requirements",
    )
    _id_map(fixture["keepouts"], "lock.fixture_interface.keepouts")

    for contact_id, contact in contacts.items():
        contact_path = f"lock.fixture_interface.contacts.{contact_id}"
        _keys(
            contact,
            contact_path,
            {
                "id",
                "shape",
                "normal",
                "contact_modes",
                "local_depth_ref",
            },
        )
        shape = _object(
            contact.get("shape"),
            f"{contact_path}.shape",
        )
        _keys(
            shape,
            f"lock.fixture_interface.contacts.{contact_id}.shape",
            {"kind", "surface", "axis", "min_mm", "max_mm"},
        )
        if shape["kind"] != "edge_interval":
            _fail(
                f"lock.fixture_interface.contacts.{contact_id}.shape",
                "perimeter_j_hook_v1 requires edge_interval contacts",
            )
        surface = _string(
            shape["surface"],
            f"lock.fixture_interface.contacts.{contact_id}.surface",
        )
        if surface not in SURFACE_POSE:
            _fail(
                f"lock.fixture_interface.contacts.{contact_id}.surface",
                f"unsupported perimeter surface {surface!r}",
            )
        axis = _string(
            shape["axis"],
            f"lock.fixture_interface.contacts.{contact_id}.axis",
        )
        if axis != SURFACE_POSE[surface][0]:
            _fail(
                f"lock.fixture_interface.contacts.{contact_id}.axis",
                f"{surface} requires axis {SURFACE_POSE[surface][0]!r}",
            )
        lower = _number(
            shape["min_mm"],
            f"lock.fixture_interface.contacts.{contact_id}.min_mm",
        )
        upper = _number(
            shape["max_mm"],
            f"lock.fixture_interface.contacts.{contact_id}.max_mm",
        )
        if lower >= upper:
            _fail(
                f"lock.fixture_interface.contacts.{contact_id}",
                "contact interval must have positive length",
            )
        depth_ref = _string(
            contact.get("local_depth_ref"),
            f"lock.fixture_interface.contacts.{contact_id}.local_depth_ref",
        )
        if depth_ref not in depths:
            _fail(
                f"lock.fixture_interface.contacts.{contact_id}.local_depth_ref",
                f"unknown local depth {depth_ref!r}",
            )
        _vector(contact["normal"], f"{contact_path}.normal", 3)
        _string_list(
            contact["contact_modes"],
            f"{contact_path}.contact_modes",
            minimum=1,
            pattern=ID_RE,
        )

    return {
        "path": lock_path,
        "source": source,
        "contracts": contracts,
        "revision": revision,
        "hash": actual_hash,
        "fixture": fixture,
        "bounds": (xy_min, xy_max),
        "depths": depths,
        "contacts": contacts,
        "access": access,
        "datums": datums,
        "clearances": clearances,
    }


def _positive_object_numbers(
    value: Any,
    path: str,
    required: set[str],
) -> Mapping[str, Any]:
    obj = _object(value, path)
    _keys(obj, path, required)
    for key in required:
        _number(obj[key], f"{path}.{key}", exclusive_minimum=Decimal(0))
    return obj


def _validate_carrier(value: Any, path: str) -> Mapping[str, Any]:
    carrier = _object(value, path)
    _keys(
        carrier,
        path,
        {
            "plate_size_mm",
            "plate_thickness_mm",
            "plate_corner_radius_mm",
            "rear_service_corner_radius_mm",
            "frame_tie",
        },
    )
    _vector(
        carrier["plate_size_mm"],
        f"{path}.plate_size_mm",
        2,
        minimum=Decimal("0.000001"),
    )
    for key in (
        "plate_thickness_mm",
        "plate_corner_radius_mm",
        "rear_service_corner_radius_mm",
    ):
        _number(
            carrier[key],
            f"{path}.{key}",
            exclusive_minimum=Decimal(0),
        )
    frame = _object(carrier["frame_tie"], f"{path}.frame_tie")
    _keys(
        frame,
        f"{path}.frame_tie",
        {"slot_size_mm", "edge_inset_mm", "corner_offset_mm"},
    )
    _vector(
        frame["slot_size_mm"],
        f"{path}.frame_tie.slot_size_mm",
        2,
        minimum=Decimal("0.000001"),
    )
    _number(
        frame["edge_inset_mm"],
        f"{path}.frame_tie.edge_inset_mm",
        exclusive_minimum=Decimal(0),
    )
    _number(
        frame["corner_offset_mm"],
        f"{path}.frame_tie.corner_offset_mm",
        exclusive_minimum=Decimal(0),
    )
    return carrier


def _validate_retention(value: Any, path: str) -> Mapping[str, Any]:
    retention = _object(value, path)
    _keys(retention, path, {"hook", "fastener"})
    _positive_object_numbers(
        retention["hook"],
        f"{path}.hook",
        {
            "throat_mm",
            "width_mm",
            "wall_mm",
            "lip_depth_mm",
            "lip_thickness_mm",
            "support_depth_mm",
            "support_thickness_mm",
            "base_outward_mm",
            "base_inward_mm",
            "base_height_mm",
            "base_radius_mm",
            "adjustment_mm",
        },
    )
    fastener = _object(retention["fastener"], f"{path}.fastener")
    _keys(
        fastener,
        f"{path}.fastener",
        {
            "m3_clearance_mm",
            "nut_across_flats_mm",
            "nut_depth_mm",
            "nut_capture_wall_mm",
            "screw_offset_mm",
            "key_offset_mm",
            "key_size_mm",
            "key_clearance_mm",
            "keyway_depth_mm",
        },
    )
    for key in (
        "m3_clearance_mm",
        "nut_across_flats_mm",
        "nut_depth_mm",
        "nut_capture_wall_mm",
        "key_clearance_mm",
        "keyway_depth_mm",
    ):
        _number(
            fastener[key],
            f"{path}.fastener.{key}",
            exclusive_minimum=Decimal(0),
        )
    _vector(fastener["screw_offset_mm"], f"{path}.fastener.screw_offset_mm", 2)
    _vector(fastener["key_offset_mm"], f"{path}.fastener.key_offset_mm", 2)
    _vector(
        fastener["key_size_mm"],
        f"{path}.fastener.key_size_mm",
        2,
        minimum=Decimal("0.000001"),
    )
    return retention


def _validate_presentation(value: Any, path: str) -> Mapping[str, Any]:
    presentation = _object(value, path)
    _keys(
        presentation,
        path,
        {
            "device_corner_radius_mm",
            "screen_proxy_size_mm",
            "label_height_mm",
            "label_stroke_growth_mm",
            "title_box_size_mm",
            "title_box_center_mm",
            "title_font_size_mm",
            "orientation_font_size_mm",
            "carrier_body_color",
            "carrier_label_color",
        },
    )
    for key in (
        "device_corner_radius_mm",
        "label_height_mm",
        "label_stroke_growth_mm",
        "title_font_size_mm",
        "orientation_font_size_mm",
    ):
        _number(
            presentation[key],
            f"{path}.{key}",
            exclusive_minimum=Decimal(0),
        )
    for key in (
        "screen_proxy_size_mm",
        "title_box_size_mm",
    ):
        _vector(
            presentation[key],
            f"{path}.{key}",
            2,
            minimum=Decimal("0.000001"),
        )
    _vector(presentation["title_box_center_mm"], f"{path}.title_box_center_mm", 2)
    for key in ("carrier_body_color", "carrier_label_color"):
        color = _vector(
            presentation[key],
            f"{path}.{key}",
            3,
            minimum=Decimal(0),
        )
        if any(component > 1 for component in color):
            _fail(f"{path}.{key}", "RGB values must be in [0, 1]")
    return presentation


def _load_manifest(path: Path) -> Mapping[str, Any]:
    manifest = _object(load_json(path), str(path))
    if manifest.get("schema") != "pocketforge-qualified-geometry-v1":
        _fail(str(path), "unsupported qualification manifest")
    return manifest


def _validate_bound_fixture_inputs(
    lock_state: Mapping[str, Any],
    bindings: Mapping[str, Any],
    path: str,
) -> None:
    """Validate the locked values consumed by perimeter_j_hook_v1."""

    depth_id = bindings["local_depth"]
    depth = _object(
        lock_state["depths"][depth_id],
        f"{path}.local_depth",
    )
    _keys(
        depth,
        f"{path}.local_depth",
        {
            "id",
            "region_refs",
            "nominal_mm",
            "basis",
            "measurement_uncertainty_mm",
            "manufacturing_ready",
        },
    )
    _number(
        depth["nominal_mm"],
        f"{path}.local_depth.nominal_mm",
        exclusive_minimum=Decimal(0),
    )
    _string(depth["basis"], f"{path}.local_depth.basis", pattern=ID_RE)
    uncertainty = depth["measurement_uncertainty_mm"]
    if uncertainty is not None:
        _number(
            uncertainty,
            f"{path}.local_depth.measurement_uncertainty_mm",
            minimum=Decimal(0),
        )
    _boolean(
        depth["manufacturing_ready"],
        f"{path}.local_depth.manufacturing_ready",
    )

    xy_min, xy_max = lock_state["bounds"]
    access_id = bindings["rear_service_access"]
    access = _object(
        lock_state["access"][access_id],
        f"{path}.rear_service_access",
    )
    _keys(
        access,
        f"{path}.rear_service_access",
        {"id", "category", "shape", "must_remain_open"},
    )
    if access["category"] != "service":
        _fail(f"{path}.rear_service_access.category", "must be 'service'")
    if not _boolean(
        access["must_remain_open"],
        f"{path}.rear_service_access.must_remain_open",
    ):
        _fail(
            f"{path}.rear_service_access.must_remain_open",
            "must be true",
        )
    access_shape = _object(
        access["shape"],
        f"{path}.rear_service_access.shape",
    )
    _keys(
        access_shape,
        f"{path}.rear_service_access.shape",
        {"kind", "surface", "axes", "min_mm", "max_mm"},
    )
    if (
        access_shape["kind"] != "surface_rectangle"
        or access_shape["surface"] != "rear"
        or access_shape["axes"] != ["x", "y"]
    ):
        _fail(
            f"{path}.rear_service_access.shape",
            "must be a rear XY surface rectangle",
        )
    access_min = _vector(
        access_shape["min_mm"],
        f"{path}.rear_service_access.shape.min_mm",
        2,
    )
    access_max = _vector(
        access_shape["max_mm"],
        f"{path}.rear_service_access.shape.max_mm",
        2,
    )
    if any(
        lower >= upper
        or lower < bound_min
        or upper > bound_max
        for lower, upper, bound_min, bound_max in zip(
            access_min,
            access_max,
            xy_min,
            xy_max,
        )
    ):
        _fail(
            f"{path}.rear_service_access.shape",
            "must have positive area inside the locked device envelope",
        )

    for binding_name in ("camera_target", "shell_center"):
        datum_id = bindings[binding_name]
        datum_path = f"{path}.{binding_name}"
        datum = _object(lock_state["datums"][datum_id], datum_path)
        _keys(datum, datum_path, {"id", "kind", "axes", "value_mm"})
        if datum["kind"] != "point_2d" or datum["axes"] != ["x", "y"]:
            _fail(datum_path, "must be an XY point datum")
        point = _vector(datum["value_mm"], f"{datum_path}.value_mm", 2)
        if any(
            value < bound_min or value > bound_max
            for value, bound_min, bound_max in zip(point, xy_min, xy_max)
        ):
            _fail(
                f"{datum_path}.value_mm",
                "must lie inside the locked device envelope",
            )

    clearance_id = bindings["rear_clearance"]
    clearance_path = f"{path}.rear_clearance"
    clearance = _object(
        lock_state["clearances"][clearance_id],
        clearance_path,
    )
    _keys(
        clearance,
        clearance_path,
        {"id", "direction", "minimum_mm", "from_datum", "protects"},
    )
    if clearance["direction"] != "rearward":
        _fail(f"{clearance_path}.direction", "must be 'rearward'")
    _number(
        clearance["minimum_mm"],
        f"{clearance_path}.minimum_mm",
        exclusive_minimum=Decimal(0),
    )
    _string_list(
        clearance["protects"],
        f"{clearance_path}.protects",
        minimum=1,
        pattern=ID_RE,
    )
    support_id = _string(
        clearance["from_datum"],
        f"{clearance_path}.from_datum",
        pattern=ID_RE,
    )
    support_path = f"{clearance_path}.from_datum"
    support = _object(lock_state["datums"].get(support_id), support_path)
    _keys(support, support_path, {"id", "kind", "normal", "offset_mm"})
    if support["kind"] != "plane":
        _fail(support_path, "must reference a plane datum")
    if _vector(support["normal"], f"{support_path}.normal", 3) != (
        Decimal(0),
        Decimal(0),
        Decimal(-1),
    ):
        _fail(f"{support_path}.normal", "must face rearward")
    _number(support["offset_mm"], f"{support_path}.offset_mm")


@dataclass(frozen=True)
class ResolvedProfile:
    root: Path
    path: Path
    document: Mapping[str, Any]
    lock: Mapping[str, Any]
    lock_state: Mapping[str, Any]
    artifacts: Mapping[str, Any]
    variants: Mapping[str, Any]
    qualification_manifest: Mapping[str, Any] | None
    openscad_parameters: Mapping[str, Any]


def _validate_recipe(
    root: Path,
    value: Any,
    path: str,
) -> Mapping[str, Any]:
    recipe = _object(value, path)
    _keys(recipe, path, {"source", "part", "parameters"})
    source = _project_path(root, recipe["source"], f"{path}.source")
    if not source.is_file() or source.suffix != ".scad":
        _fail(f"{path}.source", "must name an existing OpenSCAD source")
    _string(recipe["part"], f"{path}.part", pattern=ID_RE)
    parameters = _object(recipe["parameters"], f"{path}.parameters")
    for parameter_name, parameter_value in parameters.items():
        _string(
            parameter_name,
            f"{path}.parameters key",
            pattern=re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$"),
        )
        openscad_literal(parameter_value)
    return recipe


def validate_profile(root: Path, profile_path: Path) -> ResolvedProfile:
    root = root.resolve()
    profile_path = profile_path.resolve()
    document = _object(load_json(profile_path), str(profile_path))
    _keys(
        document,
        str(profile_path),
        {
            "schema",
            "profile_id",
            "device_slugs",
            "device_variants",
            "fixture",
            "implementation",
            "artifacts",
            "qualification",
        },
    )
    if document["schema"] != PROFILE_SCHEMA:
        _fail(f"{profile_path}.schema", f"must be {PROFILE_SCHEMA!r}")
    profile_id = _string(
        document["profile_id"],
        f"{profile_path}.profile_id",
        pattern=SLUG_RE,
    )
    if profile_path.stem != profile_id:
        _fail(
            f"{profile_path}.profile_id",
            f"must match filename stem {profile_path.stem!r}",
        )
    device_slugs = _string_list(
        document["device_slugs"],
        f"{profile_path}.device_slugs",
        minimum=1,
        pattern=SLUG_RE,
    )
    variants: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(
        _array(document["device_variants"], f"{profile_path}.device_variants")
    ):
        variant_path = f"{profile_path}.device_variants[{index}]"
        variant = _object(item, variant_path)
        _keys(
            variant,
            variant_path,
            {"device_slug", "display_name", "production_carrier"},
        )
        slug = _string(
            variant["device_slug"],
            f"{variant_path}.device_slug",
            pattern=SLUG_RE,
        )
        if slug in variants:
            _fail(f"{variant_path}.device_slug", f"duplicate device {slug!r}")
        display_name = _string(
            variant["display_name"],
            f"{variant_path}.display_name",
        )
        if len(display_name) > 64:
            _fail(f"{variant_path}.display_name", "must be at most 64 characters")
        carrier = _validate_recipe(
            root,
            variant["production_carrier"],
            f"{variant_path}.production_carrier",
        )
        if carrier["part"] != "plate":
            _fail(
                f"{variant_path}.production_carrier.part",
                "must render the production plate",
            )
        required_parameters = {
            "SHOW_DEVICE": False,
            "SHOW_HOOKS": False,
            "SHOW_LABELS": True,
        }
        for name, expected in required_parameters.items():
            if carrier["parameters"].get(name) is not expected:
                _fail(
                    f"{variant_path}.production_carrier.parameters.{name}",
                    f"must be {str(expected).lower()}",
                )
        if carrier["parameters"].get("DEVICE_LABEL") != display_name:
            _fail(
                f"{variant_path}.production_carrier.parameters.DEVICE_LABEL",
                "must exactly match display_name",
            )
        variants[slug] = variant
    if set(variants) != set(device_slugs):
        _fail(
            f"{profile_path}.device_variants",
            "must map every device slug exactly once",
        )

    fixture_binding = _object(document["fixture"], f"{profile_path}.fixture")
    _keys(
        fixture_binding,
        f"{profile_path}.fixture",
        {"lock", "interface_sha256", "bindings"},
    )
    lock_path = _project_path(
        root,
        fixture_binding["lock"],
        f"{profile_path}.fixture.lock",
    )
    lock = _object(load_json(lock_path), str(lock_path))
    lock_state = validate_fixture_lock(root, lock_path, lock)
    interface_hash_value = _string(
        fixture_binding["interface_sha256"],
        f"{profile_path}.fixture.interface_sha256",
        pattern=SHA256_RE,
    )
    if interface_hash_value != lock_state["hash"]:
        _fail(
            f"{profile_path}.fixture.interface_sha256",
            "does not match the fixture lock",
        )
    if set(device_slugs) != set(lock_state["contracts"]):
        _fail(
            f"{profile_path}.device_slugs",
            "must exactly match the devices pinned by the family fixture lock",
        )

    bindings = _object(
        fixture_binding["bindings"],
        f"{profile_path}.fixture.bindings",
    )
    _keys(
        bindings,
        f"{profile_path}.fixture.bindings",
        {
            "local_depth",
            "rear_service_access",
            "camera_target",
            "shell_center",
            "rear_clearance",
        },
    )
    binding_targets = (
        ("local_depth", "depths"),
        ("rear_service_access", "access"),
        ("camera_target", "datums"),
        ("shell_center", "datums"),
        ("rear_clearance", "clearances"),
    )
    for binding_name, state_name in binding_targets:
        target = _string(
            bindings[binding_name],
            f"{profile_path}.fixture.bindings.{binding_name}",
            pattern=ID_RE,
        )
        if target not in lock_state[state_name]:
            _fail(
                f"{profile_path}.fixture.bindings.{binding_name}",
                f"unknown locked {state_name} id {target!r}",
            )
    _validate_bound_fixture_inputs(
        lock_state,
        bindings,
        f"{profile_path}.fixture.bindings",
    )

    implementation = _object(
        document["implementation"],
        f"{profile_path}.implementation",
    )
    kind = _string(
        implementation.get("kind"),
        f"{profile_path}.implementation.kind",
    )
    qualification = _object(
        document["qualification"],
        f"{profile_path}.qualification",
    )
    _keys(
        qualification,
        f"{profile_path}.qualification",
        {
            "status",
            "acceptance_ref",
            "accepted_on",
            "accepted_geometry_revision",
            "fixture_interface_sha256",
            "geometry_manifest",
            "artifact_names",
        },
    )
    status = _string(
        qualification["status"],
        f"{profile_path}.qualification.status",
    )
    if status not in {"unqualified", "physically_qualified"}:
        _fail(
            f"{profile_path}.qualification.status",
            "must be 'unqualified' or 'physically_qualified'",
        )
    if qualification["fixture_interface_sha256"] != lock_state["hash"]:
        _fail(
            f"{profile_path}.qualification.fixture_interface_sha256",
            "does not match the locked fixture interface",
        )

    if kind == "declarative":
        _keys(
            implementation,
            f"{profile_path}.implementation",
            {
                "kind",
                "mechanism_family",
                "source",
                "carrier",
                "contacts",
                "retention",
                "presentation",
            },
        )
        if implementation["mechanism_family"] != "perimeter_j_hook_v1":
            _fail(
                f"{profile_path}.implementation.mechanism_family",
                "unsupported declarative mechanism family",
            )
        source_path = _project_path(
            root,
            implementation["source"],
            f"{profile_path}.implementation.source",
        )
        if not source_path.is_file() or source_path.suffix != ".scad":
            _fail(
                f"{profile_path}.implementation.source",
                "must name an existing OpenSCAD source",
            )
        _validate_carrier(
            implementation["carrier"],
            f"{profile_path}.implementation.carrier",
        )
        _validate_retention(
            implementation["retention"],
            f"{profile_path}.implementation.retention",
        )
        _validate_presentation(
            implementation["presentation"],
            f"{profile_path}.implementation.presentation",
        )
        contact_rows: dict[str, Mapping[str, Any]] = {}
        for index, item in enumerate(
            _array(
                implementation["contacts"],
                f"{profile_path}.implementation.contacts",
            )
        ):
            item_path = f"{profile_path}.implementation.contacts[{index}]"
            contact = _object(item, item_path)
            _keys(
                contact,
                item_path,
                {
                    "fixture_contact_id",
                    "selected_coordinate_mm",
                    "designed_play_mm",
                },
            )
            contact_id = _string(
                contact["fixture_contact_id"],
                f"{item_path}.fixture_contact_id",
                pattern=ID_RE,
            )
            if contact_id in contact_rows:
                _fail(
                    f"{item_path}.fixture_contact_id",
                    f"duplicate selected contact {contact_id!r}",
                )
            locked_contact = lock_state["contacts"].get(contact_id)
            if locked_contact is None:
                _fail(
                    f"{item_path}.fixture_contact_id",
                    f"unknown fixture contact {contact_id!r}",
                )
            selected = _number(
                contact["selected_coordinate_mm"],
                f"{item_path}.selected_coordinate_mm",
            )
            _number(
                contact["designed_play_mm"],
                f"{item_path}.designed_play_mm",
                minimum=Decimal(0),
            )
            shape = locked_contact["shape"]
            lower = _number(shape["min_mm"], f"{item_path}.locked_min")
            upper = _number(shape["max_mm"], f"{item_path}.locked_max")
            if not lower <= selected <= upper:
                _fail(
                    f"{item_path}.selected_coordinate_mm",
                    f"{selected} is outside locked interval [{lower}, {upper}]",
                )
            if locked_contact["local_depth_ref"] != bindings["local_depth"]:
                _fail(
                    f"{item_path}.fixture_contact_id",
                    "contact does not use the bound local depth",
                )
            contact_rows[contact_id] = contact
        if set(contact_rows) != set(lock_state["contacts"]):
            missing = sorted(set(lock_state["contacts"]) - set(contact_rows))
            extra = sorted(set(contact_rows) - set(lock_state["contacts"]))
            _fail(
                f"{profile_path}.implementation.contacts",
                f"must select every locked contact once; missing={missing} extra={extra}",
            )
        if set(contact_rows) != set(PERIMETER_CONTACT_SURFACES):
            _fail(
                f"{profile_path}.implementation.contacts",
                "perimeter_j_hook_v1 requires exactly the six semantic "
                f"contacts {sorted(PERIMETER_CONTACT_SURFACES)}",
            )
        for contact_id, expected_surface in PERIMETER_CONTACT_SURFACES.items():
            actual_surface = lock_state["contacts"][contact_id]["shape"]["surface"]
            if actual_surface != expected_surface:
                _fail(
                    f"{profile_path}.implementation.contacts.{contact_id}",
                    f"requires surface {expected_surface!r}, got "
                    f"{actual_surface!r}",
                )
    elif kind == "custom_openscad":
        _keys(
            implementation,
            f"{profile_path}.implementation",
            {
                "kind",
                "source",
                "rationale",
                "reusable_family_followup",
            },
        )
        source_path = _project_path(
            root,
            implementation["source"],
            f"{profile_path}.implementation.source",
        )
        if not source_path.is_file() or source_path.suffix != ".scad":
            _fail(
                f"{profile_path}.implementation.source",
                "must name an existing OpenSCAD source",
            )
        _string(
            implementation["rationale"],
            f"{profile_path}.implementation.rationale",
        )
        _string(
            implementation["reusable_family_followup"],
            f"{profile_path}.implementation.reusable_family_followup",
        )
        if status != "unqualified":
            _fail(
                f"{profile_path}.qualification.status",
                "custom_openscad is an unqualified escape hatch; promote a reusable "
                "mechanism before physical qualification",
            )
    else:
        _fail(
            f"{profile_path}.implementation.kind",
            f"unsupported implementation kind {kind!r}",
        )

    artifacts = _object(document["artifacts"], f"{profile_path}.artifacts")
    if not artifacts:
        _fail(f"{profile_path}.artifacts", "must not be empty")
    for artifact_name, value in artifacts.items():
        _string(artifact_name, f"{profile_path}.artifacts key", pattern=ID_RE)
        artifact_path = f"{profile_path}.artifacts.{artifact_name}"
        _validate_recipe(root, value, artifact_path)

    manifest: Mapping[str, Any] | None = None
    artifact_names = _string_list(
        qualification["artifact_names"],
        f"{profile_path}.qualification.artifact_names",
    )
    if status == "physically_qualified":
        if kind != "declarative":
            _fail(
                f"{profile_path}.qualification.status",
                "only declarative reusable mechanisms may be qualified",
            )
        acceptance_ref = _string(
            qualification["acceptance_ref"],
            f"{profile_path}.qualification.acceptance_ref",
        )
        accepted_on = _string(
            qualification["accepted_on"],
            f"{profile_path}.qualification.accepted_on",
        )
        try:
            dt.date.fromisoformat(accepted_on)
        except ValueError as exc:
            _fail(
                f"{profile_path}.qualification.accepted_on",
                f"invalid ISO date: {exc}",
            )
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", accepted_on):
            _fail(
                f"{profile_path}.qualification.accepted_on",
                "must use YYYY-MM-DD form",
            )
        accepted_revision = _string(
            qualification["accepted_geometry_revision"],
            f"{profile_path}.qualification.accepted_geometry_revision",
            pattern=GIT_REV_RE,
        )
        manifest_path = _project_path(
            root,
            qualification["geometry_manifest"],
            f"{profile_path}.qualification.geometry_manifest",
        )
        manifest = _load_manifest(manifest_path)
        manifest_qualification = _object(
            manifest.get("qualification"),
            f"{manifest_path}.qualification",
        )
        if manifest_qualification.get("status") != "physically_accepted":
            _fail(str(manifest_path), "geometry manifest is not physically accepted")
        expected_linkage = {
            "acceptance_ref": acceptance_ref,
            "accepted_on": accepted_on,
            "accepted_source_revision": accepted_revision,
        }
        for key, expected in expected_linkage.items():
            if manifest_qualification.get(key) != expected:
                _fail(
                    f"{profile_path}.qualification.{key}",
                    f"does not match geometry manifest value "
                    f"{manifest_qualification.get(key)!r}",
                )
        if set(artifact_names) != set(artifacts) or set(artifact_names) != set(
            _object(manifest.get("artifacts"), f"{manifest_path}.artifacts")
        ):
            _fail(
                f"{profile_path}.qualification.artifact_names",
                "must exactly match profile and geometry-manifest artifacts",
            )
        if set(artifact_names) != QUALIFIED_ARTIFACTS:
            _fail(
                f"{profile_path}.qualification.artifact_names",
                f"qualified perimeter_j_hook_v1 requires {sorted(QUALIFIED_ARTIFACTS)}",
            )
        manifest_device_ids = _string_list(
            manifest_qualification.get("device_ids"),
            f"{manifest_path}.qualification.device_ids",
            minimum=1,
            pattern=SLUG_RE,
        )
        if set(manifest_device_ids) != set(device_slugs):
            _fail(
                f"{profile_path}.qualification",
                "device slugs do not match the qualified geometry manifest",
            )
        fit = _object(
            manifest_qualification.get("fit_parameters_mm"),
            f"{manifest_path}.qualification.fit_parameters_mm",
        )
        retention = implementation["retention"]
        hook = retention["hook"]
        fastener = retention["fastener"]
        clearance = lock_state["clearances"][bindings["rear_clearance"]]
        expected_fit = {
            "device_rear_gap": clearance["minimum_mm"],
            "hook_throat": hook["throat_mm"],
            "m3_nut_across_flats": fastener["nut_across_flats_mm"],
            "m3_nut_capture_wall": fastener["nut_capture_wall_mm"],
        }
        for manifest_key, actual_value in expected_fit.items():
            manifest_value = fit.get(manifest_key)
            if manifest_value is None or Decimal(str(manifest_value)) != _number(
                actual_value,
                f"profile.{manifest_key}",
            ):
                _fail(
                    f"{profile_path}.qualification",
                    f"{manifest_key} does not match qualified geometry manifest",
                )
    else:
        null_fields = {
            "acceptance_ref",
            "accepted_on",
            "accepted_geometry_revision",
            "geometry_manifest",
        }
        for key in null_fields:
            if qualification[key] is not None:
                _fail(
                    f"{profile_path}.qualification.{key}",
                    "must be null while unqualified",
                )
        if artifact_names:
            _fail(
                f"{profile_path}.qualification.artifact_names",
                "must be empty while unqualified",
            )

    parameters = (
        compile_declarative_parameters(document, lock_state)
        if kind == "declarative"
        else {}
    )
    return ResolvedProfile(
        root=root,
        path=profile_path,
        document=document,
        lock=lock,
        lock_state=lock_state,
        artifacts=artifacts,
        variants=variants,
        qualification_manifest=manifest,
        openscad_parameters=parameters,
    )


def compile_declarative_parameters(
    profile: Mapping[str, Any],
    lock_state: Mapping[str, Any],
) -> dict[str, Any]:
    implementation = profile["implementation"]
    carrier = implementation["carrier"]
    frame = carrier["frame_tie"]
    retention = implementation["retention"]
    hook = retention["hook"]
    fastener = retention["fastener"]
    presentation = implementation["presentation"]
    bindings = profile["fixture"]["bindings"]
    fixture = lock_state["fixture"]
    xy_min, xy_max = lock_state["bounds"]
    body_size = [xy_max[0] - xy_min[0], xy_max[1] - xy_min[1]]
    plate_size = carrier["plate_size_mm"]
    device_origin = [
        (plate_size[0] - body_size[0]) / 2,
        (plate_size[1] - body_size[1]) / 2,
    ]

    contacts = lock_state["contacts"]
    selected = {
        row["fixture_contact_id"]: row
        for row in implementation["contacts"]
    }
    clamp_poses: list[list[Any]] = []
    for contact_id in sorted(contacts):
        locked = contacts[contact_id]
        surface = locked["shape"]["surface"]
        coordinate = selected[contact_id]["selected_coordinate_mm"]
        play = selected[contact_id]["designed_play_mm"]
        if surface == "bottom_edge":
            point = [device_origin[0] + coordinate, device_origin[1]]
        elif surface == "top_edge":
            point = [
                device_origin[0] + coordinate,
                device_origin[1] + body_size[1],
            ]
        elif surface == "left_edge":
            point = [device_origin[0], device_origin[1] + coordinate]
        elif surface == "right_edge":
            point = [
                device_origin[0] + body_size[0],
                device_origin[1] + coordinate,
            ]
        else:
            raise ProfileError(f"unsupported contact surface: {surface}")
        clamp_poses.append(
            [contact_id, point, SURFACE_POSE[surface][1], play]
        )

    def interval(contact_id: str) -> tuple[Decimal, Decimal]:
        shape = contacts[contact_id]["shape"]
        return (
            _number(shape["min_mm"], f"contact.{contact_id}.min"),
            _number(shape["max_mm"], f"contact.{contact_id}.max"),
        )

    def right_inset_interval(
        contact_id: str,
    ) -> tuple[Decimal, Decimal]:
        lower, upper = interval(contact_id)
        return body_size[0] - upper, body_size[0] - lower

    access = lock_state["access"][bindings["rear_service_access"]]
    access_shape = access["shape"]
    access_min = access_shape["min_mm"]
    access_max = access_shape["max_mm"]
    rear_service_window = [
        access_max[0] - access_min[0],
        access_max[1] - access_min[1],
    ]
    local_depth = lock_state["depths"][bindings["local_depth"]]
    rear_clearance = lock_state["clearances"][bindings["rear_clearance"]]
    camera = lock_state["datums"][bindings["camera_target"]]["value_mm"]
    shell_center = lock_state["datums"][bindings["shell_center"]]["value_mm"]
    optical_offset = [
        camera[0] - shell_center[0],
        camera[1] - shell_center[1],
    ]

    return {
        "plate_size": plate_size,
        "plate_thickness": carrier["plate_thickness_mm"],
        "plate_corner_radius": carrier["plate_corner_radius_mm"],
        "frame_tie_slot": frame["slot_size_mm"],
        "frame_tie_edge_inset": frame["edge_inset_mm"],
        "frame_tie_corner_offset": frame["corner_offset_mm"],
        "device_body_size": body_size,
        "device_body_depth": local_depth["nominal_mm"],
        "device_corner_radius": presentation["device_corner_radius_mm"],
        "screen_size": presentation["screen_proxy_size_mm"],
        "optical_offset": optical_offset,
        "device_rear_gap": rear_clearance["minimum_mm"],
        "rear_service_window": rear_service_window,
        "rear_service_radius": carrier["rear_service_corner_radius_mm"],
        "top_left_safe": list(interval("top_left")),
        "top_right_safe": list(right_inset_interval("top_right")),
        "bottom_left_safe": list(interval("bottom_left")),
        "bottom_right_safe": list(right_inset_interval("bottom_right")),
        "clamp_poses": clamp_poses,
        "hook_throat": hook["throat_mm"],
        "hook_width": hook["width_mm"],
        "hook_wall": hook["wall_mm"],
        "hook_lip_depth": hook["lip_depth_mm"],
        "hook_lip_thickness": hook["lip_thickness_mm"],
        "hook_support_depth": hook["support_depth_mm"],
        "hook_support_thickness": hook["support_thickness_mm"],
        "hook_base_outward": hook["base_outward_mm"],
        "hook_base_inward": hook["base_inward_mm"],
        "hook_base_height": hook["base_height_mm"],
        "hook_base_radius": hook["base_radius_mm"],
        "hook_adjustment": hook["adjustment_mm"],
        "m3_clearance": fastener["m3_clearance_mm"],
        "m3_nut_across_flats": fastener["nut_across_flats_mm"],
        "m3_nut_depth": fastener["nut_depth_mm"],
        "m3_nut_capture_wall": fastener["nut_capture_wall_mm"],
        "hook_screw_offset": fastener["screw_offset_mm"],
        "hook_key_offset": fastener["key_offset_mm"],
        "hook_key_size": fastener["key_size_mm"],
        "hook_key_clearance": fastener["key_clearance_mm"],
        "hook_keyway_depth": fastener["keyway_depth_mm"],
        "label_height": presentation["label_height_mm"],
        "label_stroke_growth": presentation["label_stroke_growth_mm"],
        "title_box_size": presentation["title_box_size_mm"],
        "title_box_centre": presentation["title_box_center_mm"],
        "title_font_size": presentation["title_font_size_mm"],
        "orientation_font_size": presentation["orientation_font_size_mm"],
        "carrier_body_color": presentation["carrier_body_color"],
        "carrier_label_color": presentation["carrier_label_color"],
    }


def openscad_literal(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
        return _canonical_number(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(openscad_literal(item) for item in value) + "]"
    raise ProfileError(
        "OpenSCAD parameters may contain only finite numbers, booleans, "
        f"strings, and arrays; got {type(value).__name__}"
    )


def recipe_parameters(
    resolved: ResolvedProfile,
    recipe: Mapping[str, Any],
    parameter_overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    parameters = dict(resolved.openscad_parameters)
    parameters.update(recipe["parameters"])
    parameters["PART"] = recipe["part"]
    if parameter_overrides:
        parameters.update(parameter_overrides)
    return parameters


def recipe_command(
    resolved: ResolvedProfile,
    recipe: Mapping[str, Any],
    output: Path,
    *,
    openscad: str,
    parameter_overrides: Mapping[str, Any] | None = None,
) -> list[str]:
    source = _project_path(
        resolved.root,
        recipe["source"],
        "recipe.source",
    )
    output = output.resolve()
    parameters = recipe_parameters(resolved, recipe, parameter_overrides)
    command = [
        openscad,
        "--hardwarnings",
        "--check-parameters=true",
        "--check-parameter-ranges=true",
        "-o",
        str(output),
    ]
    for name in sorted(parameters):
        command.extend(["-D", f"{name}={openscad_literal(parameters[name])}"])
    command.append(str(source))
    return command


def artifact_command(
    resolved: ResolvedProfile,
    artifact_name: str,
    output: Path,
    *,
    openscad: str,
    parameter_overrides: Mapping[str, Any] | None = None,
) -> list[str]:
    artifact = resolved.artifacts.get(artifact_name)
    if not isinstance(artifact, dict):
        raise ProfileError(f"unknown profile artifact: {artifact_name}")
    return recipe_command(
        resolved,
        artifact,
        output,
        openscad=openscad,
        parameter_overrides=parameter_overrides,
    )


def render_artifact(
    resolved: ResolvedProfile,
    artifact_name: str,
    output: Path,
    *,
    openscad: str,
    parameter_overrides: Mapping[str, Any] | None = None,
) -> None:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    command = artifact_command(
        resolved,
        artifact_name,
        output,
        openscad=openscad,
        parameter_overrides=parameter_overrides,
    )
    try:
        result = subprocess.run(
            command,
            cwd=resolved.root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ProfileError(f"cannot run {openscad!r}: {exc}") from exc
    diagnostics = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    errors = [
        line for line in diagnostics.splitlines() if line.startswith("ERROR:")
    ]
    if result.returncode != 0 or errors:
        raise ProfileError(
            f"OpenSCAD failed for {artifact_name} rc={result.returncode}: "
            f"{diagnostics}"
        )
    if not output.is_file() or output.stat().st_size == 0:
        raise ProfileError(
            f"OpenSCAD produced no non-empty output for {artifact_name}"
        )
    print(
        f"holder_profile_render=pass profile={resolved.document['profile_id']} "
        f"artifact={artifact_name} output={output}"
    )


def check_qualified(
    resolved: ResolvedProfile,
    *,
    openscad: str,
) -> None:
    if resolved.qualification_manifest is None:
        raise ProfileError("profile is not physically qualified")
    manifest = resolved.qualification_manifest
    toolchain_path = _project_path(
        resolved.root,
        manifest["toolchain_lock"],
        "qualification.toolchain_lock",
    )
    check_toolchain(toolchain_path, openscad)
    manifest_artifacts = _object(
        manifest["artifacts"],
        "qualification.artifacts",
    )
    with tempfile.TemporaryDirectory(prefix="pf-holder-profile-") as tmp:
        temp_root = Path(tmp)
        for artifact_name in sorted(resolved.artifacts):
            output = temp_root / f"{artifact_name}.stl"
            render_artifact(
                resolved,
                artifact_name,
                output,
                openscad=openscad,
            )
            expected = _object(
                manifest_artifacts[artifact_name]["expected"],
                f"qualification.artifacts.{artifact_name}.expected",
            )
            mismatches = compare_artifact(artifact_name, output, expected)
            if mismatches:
                raise ProfileError(
                    "\n".join(
                        "holder_profile_qualified_mismatch "
                        f"artifact={artifact_name} {mismatch}"
                        for mismatch in mismatches
                    )
                )
            print(
                f"holder_profile_qualified=pass "
                f"profile={resolved.document['profile_id']} "
                f"artifact={artifact_name}"
            )


def check_mutation(
    resolved: ResolvedProfile,
    *,
    openscad: str,
) -> None:
    if resolved.qualification_manifest is None:
        raise ProfileError("profile is not physically qualified")
    expected = _object(
        resolved.qualification_manifest["artifacts"]["j_hook"]["expected"],
        "qualification.artifacts.j_hook.expected",
    )
    current = _number(
        resolved.openscad_parameters["hook_throat"],
        "compiled.hook_throat",
    )
    with tempfile.TemporaryDirectory(prefix="pf-holder-profile-mutation-") as tmp:
        output = Path(tmp) / "j_hook_throat_plus_0_1.stl"
        render_artifact(
            resolved,
            "j_hook",
            output,
            openscad=openscad,
            parameter_overrides={"hook_throat": current + Decimal("0.1")},
        )
        mismatches = compare_artifact("j_hook", output, expected)
        if not mismatches:
            raise ProfileError(
                "0.1 mm hook-throat mutation unexpectedly retained qualified geometry"
            )
    print(
        "holder_profile_mutation_guard=pass "
        f"profile={resolved.document['profile_id']} "
        f"case=hook_throat_{current}_to_{current + Decimal('0.1')}"
    )


def verify_source_pin(
    resolved: ResolvedProfile,
    platform_root: Path,
) -> None:
    platform_root = platform_root.resolve()
    if not (platform_root / ".git").exists():
        raise ProfileError(f"platform root is not a Git checkout: {platform_root}")
    revision = resolved.lock_state["source"]["revision"]
    try:
        commit = subprocess.run(
            ["git", "-C", str(platform_root), "rev-parse", f"{revision}^{{commit}}"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ProfileError(f"cannot run git: {exc}") from exc
    if commit.returncode != 0 or commit.stdout.strip() != revision:
        raise ProfileError(
            f"platform checkout does not contain pinned revision {revision}"
        )

    locked_interface = resolved.lock["interface"]
    full_seen = False
    for slug, contract in sorted(resolved.lock_state["contracts"].items()):
        source_path = contract["path"]
        result = subprocess.run(
            ["git", "-C", str(platform_root), "show", f"{revision}:{source_path}"],
            check=False,
            capture_output=True,
        )
        if result.returncode != 0:
            raise ProfileError(
                f"cannot read platform {revision}:{source_path}: "
                f"{result.stderr.decode(errors='replace').strip()}"
            )
        raw_hash = hashlib.sha256(result.stdout).hexdigest()
        if raw_hash != contract["raw_sha256"]:
            raise ProfileError(
                f"raw source mismatch for {slug}: "
                f"expected {contract['raw_sha256']}, got {raw_hash}"
            )
        source_document = _object(
            json.loads(
                result.stdout,
                parse_float=Decimal,
                parse_int=Decimal,
                parse_constant=_reject_constant,
            ),
            f"platform:{source_path}",
        )
        if source_document.get("kind") != contract["kind"]:
            raise ProfileError(f"contract kind mismatch for {slug}")
        if source_document.get("device", {}).get("slug") != slug:
            raise ProfileError(f"device slug mismatch for {slug}")
        if contract["kind"] == "fixture_interface":
            full_seen = True
            comparisons = {
                "schema_version": locked_interface["schema_version"],
                "interface_revision": locked_interface["interface_revision"],
                "fixture_interface_sha256": locked_interface["sha256"],
                "coordinate_system": locked_interface["coordinate_system"],
                "fixture_interface": locked_interface["fixture_interface"],
            }
            for key, expected in comparisons.items():
                if _canonical_json(source_document.get(key)) != _canonical_json(
                    expected
                ):
                    raise ProfileError(
                        f"locked {key} differs from platform source for {slug}"
                    )
        else:
            if (
                source_document.get("expected_fixture_interface_sha256")
                != locked_interface["sha256"]
            ):
                raise ProfileError(
                    f"alias {slug} does not resolve the locked interface"
                )
        print(
            f"holder_fixture_source=pass device={slug} "
            f"raw_sha256={raw_hash}"
        )
    if not full_seen:
        raise ProfileError("fixture lock contains no full source contract")


def discover_profiles(root: Path) -> list[Path]:
    return sorted(
        path
        for path in (root / "profiles").glob("*.json")
        if not path.name.endswith(".schema.json")
    )


def _resolve_profile_path(root: Path, path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def main(argv: Sequence[str] | None = None) -> int:
    default_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--profile", type=Path, action="append")

    source_revision_parser = subparsers.add_parser("source-revision")
    source_revision_parser.add_argument("--profile", type=Path, required=True)

    verify_parser = subparsers.add_parser("verify-source")
    verify_parser.add_argument("--profile", type=Path, required=True)
    verify_parser.add_argument("--platform-root", type=Path, required=True)

    command_parser = subparsers.add_parser("print-command")
    command_parser.add_argument("--profile", type=Path, required=True)
    command_parser.add_argument("--artifact", required=True)
    command_parser.add_argument("--output", type=Path, required=True)
    command_parser.add_argument("--openscad", default="openscad")

    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("--profile", type=Path, required=True)
    render_parser.add_argument("--artifact", required=True)
    render_parser.add_argument("--output", type=Path, required=True)
    render_parser.add_argument("--openscad", default="openscad")

    check_parser = subparsers.add_parser("check-qualified")
    check_parser.add_argument("--profile", type=Path, required=True)
    check_parser.add_argument("--openscad", default="openscad")

    mutation_parser = subparsers.add_parser("check-mutation")
    mutation_parser.add_argument("--profile", type=Path, required=True)
    mutation_parser.add_argument("--openscad", default="openscad")

    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        if args.command == "validate":
            paths = (
                [_resolve_profile_path(root, path) for path in args.profile]
                if args.profile
                else discover_profiles(root)
            )
            if not paths:
                raise ProfileError(f"no holder profiles discovered under {root}")
            ids: set[str] = set()
            for path in paths:
                resolved = validate_profile(root, path)
                profile_id = resolved.document["profile_id"]
                if profile_id in ids:
                    raise ProfileError(f"duplicate profile id: {profile_id}")
                ids.add(profile_id)
                print(
                    f"holder_profile=pass profile={profile_id} "
                    f"kind={resolved.document['implementation']['kind']} "
                    f"fixture_sha256={resolved.lock_state['hash']}"
                )
            print(f"holder_profiles=pass count={len(paths)}")
            return 0

        profile_path = _resolve_profile_path(root, args.profile)
        resolved = validate_profile(root, profile_path)
        if args.command == "source-revision":
            print(resolved.lock_state["source"]["revision"])
        elif args.command == "verify-source":
            verify_source_pin(resolved, args.platform_root)
        elif args.command == "print-command":
            print(
                shlex.join(
                    artifact_command(
                        resolved,
                        args.artifact,
                        args.output,
                        openscad=args.openscad,
                    )
                )
            )
        elif args.command == "render":
            render_artifact(
                resolved,
                args.artifact,
                args.output,
                openscad=args.openscad,
            )
        elif args.command == "check-qualified":
            check_qualified(resolved, openscad=args.openscad)
        else:
            check_mutation(resolved, openscad=args.openscad)
        return 0
    except (OSError, ProfileError, QualificationError) as exc:
        print(f"holder_profile_error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
