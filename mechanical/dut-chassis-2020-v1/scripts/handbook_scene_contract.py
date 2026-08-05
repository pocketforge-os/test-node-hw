"""Validate the layout binding for the canonical handbook scene."""

from __future__ import annotations

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
