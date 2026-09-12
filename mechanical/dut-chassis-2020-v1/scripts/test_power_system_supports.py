#!/usr/bin/env python3
"""Regression tests for the enclosure's geometric support-risk gate."""

from __future__ import annotations

from check_power_system_supports import audit_facets


def downward_rectangle(x: float, y: float, z: float):
    # Clockwise winding viewed from +Z produces an outward/downward normal.
    return [
        ((0, 0, z), (x, y, z), (x, 0, z)),
        ((0, 0, z), (0, y, z), (x, y, z)),
    ]


for part, facets in (
    ("base", downward_rectangle(4.0, 13.6, 4.0)),
    ("hood", downward_rectangle(71.0, 3.8, 39.0)),
    ("cassette", downward_rectangle(4.0, 32.0, 2.4)),
):
    try:
        audit_facets(part, facets)
    except ValueError:
        pass
    else:
        raise SystemExit(f"support-risk regression was not rejected: {part}")

# A short 1.6 mm vent roof remains a slicer-qualified local bridge, not one of
# the long/floating structural undersides this gate excludes.
audit_facets("hood", downward_rectangle(1.6, 3.2, 18.0))

print("power_system_support_gate_tests=pass blockers=3 local_vent_bridge=accepted")
