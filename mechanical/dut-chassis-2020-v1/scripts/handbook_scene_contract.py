"""Validate the layout binding for the canonical handbook scene."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def validate_layout_binding(
    *,
    device_slug: str,
    registered_layout: object,
    layout_relative: str,
    layout: dict[str, Any],
) -> dict[str, Any]:
    """Validate the binding and return its qualification provenance."""

    layout_id = layout.get("layout_id")
    if not isinstance(layout_id, str) or not layout_id:
        raise ValueError("layout record has no layout_id")

    qualification = layout.get("qualification")
    if not isinstance(qualification, dict):
        raise ValueError(f"{layout_id} has no layout qualification")
    if device_slug not in qualification.get("device_slugs", []):
        raise ValueError(
            f"{device_slug} is outside {layout_id} qualification scope"
        )

    if registered_layout == layout_relative:
        return qualification
    if not isinstance(registered_layout, str) or not registered_layout:
        raise ValueError(f"{device_slug} has no active registered layout")
    if qualification.get("status") != "physically_qualified":
        raise ValueError(
            f"{device_slug} selects {registered_layout!r}; historical "
            f"handbook layout {layout_relative!r} is not physically qualified"
        )
    return qualification


def digest(path: Path) -> str:
    """Return the SHA-256 digest used by handbook scene provenance."""

    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_scene_contract(arguments: Any, repository_root: Path) -> dict[str, Any]:
    """Load and assemble the source-owned handbook scene contract."""

    registry_path = arguments.device_registry.resolve()
    layout_path = arguments.layout_record.resolve()
    device_model_path = arguments.device_model_source.resolve()
    for path in (registry_path, layout_path, device_model_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    layout_relative = layout_path.relative_to(repository_root).as_posix()
    registered_layout = (
        registry.get("devices", {})
        .get(arguments.device_slug, {})
        .get("layout")
    )
    qualification = validate_layout_binding(
        device_slug=arguments.device_slug,
        registered_layout=registered_layout,
        layout_relative=layout_relative,
        layout=layout,
    )
    layout_id = layout["layout_id"]
    artifact_variants = {
        artifact.get("parameters", {}).get("CHASSIS_VARIANT")
        for artifact in layout.get("artifacts", [])
    }
    if artifact_variants != {arguments.chassis_variant}:
        raise ValueError(
            f"{layout_id} artifact variants {artifact_variants!r} do not "
            f"match {arguments.chassis_variant!r}"
        )

    actual_device_model_sha256 = digest(device_model_path)
    if actual_device_model_sha256 != arguments.device_model_sha256:
        raise ValueError(
            "device model SHA-256 mismatch: "
            f"{actual_device_model_sha256} != "
            f"{arguments.device_model_sha256}"
        )

    return {
        "device_slug": arguments.device_slug,
        "chassis_variant": arguments.chassis_variant,
        "layout_id": layout_id,
        "layout_record": layout_relative,
        "layout_sha256": digest(layout_path),
        "device_registry": registry_path.relative_to(
            repository_root
        ).as_posix(),
        "device_registry_sha256": digest(registry_path),
        "qualification": {
            "status": qualification.get("status"),
            "acceptance_ref": qualification.get("acceptance_ref"),
        },
        "device_model": {
            "source_repository": arguments.device_model_url,
            "source_commit": arguments.device_model_commit,
            "source_sha256": actual_device_model_sha256,
        },
    }
