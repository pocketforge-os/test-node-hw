#!/usr/bin/env python3
"""Focused source, mesh, and documentation contracts for enclosure V2."""

from __future__ import annotations

import math
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "power-system-enclosure.scad").read_text()
DOC = (ROOT / "POWER_SYSTEM_ENCLOSURE.md").read_text()
MAKEFILE = (ROOT / "Makefile").read_text()
sys.path.insert(0, str(ROOT / "scripts"))
from check_stl_topology import inspect_topology, triangles  # noqa: E402


def require(text: str, *fragments: str) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise SystemExit(f"power enclosure contract missing: {missing}")


require(
    SOURCE,
    'PART = is_undef(PART) ? "assembly" : PART;',
    "NOZZLE_DIAMETER = is_undef(NOZZLE_DIAMETER) ? 0.8 : NOZZLE_DIAMETER;",
    "function nozzle_lines_at_least(v)",
    "function printable_at_least(v)",
    "LOCAL_UNION = NOZZLE_DIAMETER;",
    "KEY_UNION = NOZZLE_DIAMETER;",
    "IEC_SNAP_WALL = max(IEC_SNAP_NOMINAL, NOZZLE_DIAMETER);",
    "WARNING: C14 snap membrane is",
    "function enclosure_outer_min() = [190,160,0]",
    "function enclosure_outer_max() = [322.8,288,60]",
    "function enclosure_corner_radius() = 6",
    "function enclosure_psu_origin() = [194,243.7,FLOOR]",
    "function enclosure_psu_rotation() = [0,0,-90]",
    "function enclosure_c14_origin() = [284,286,30]",
    "function enclosure_front_fastener_x() = [215,300]",
    "function enclosure_front_fastener_z() = 50.4",
    "function enclosure_rail_hole_yz() = [[149.73,10],[306,10],[330,10]]",
    "HOOD_NUT_AF = 5.60;",
    "HOOD_NUT_DEPTH = 2.80;",
    "HOOD_NUT_LEAD_AF = 6.20;",
    "HOOD_NUT_LEAD_DEPTH = 0.80;",
    "HOOD_NUT_BACKSTOP = 2.40;",
    "HOOD_NUT_RADIAL_CAPTURE = 2.40;",
    "BARRIER_GROOVE = BARRIER_THICKNESS + 2 * BARRIER_CLEARANCE;",
    "module mains_selv_boundary()",
    "module cassette_receiver_block",
    "module cassette_insertion_path_keepout()",
    "module roof_open_cleats()",
    "module roof_baffle()",
    "module rear_hook(x)",
    "module front_post_outer(x)",
    "module barrier_floor_groove_negative()",
    "module barrier_roof_compression_rib()",
    "module enclosure_base_installed()",
    "module enclosure_hood_installed()",
    "module enclosure_c14_cassette_installed()",
    'if (PART=="base") base_print_orientation();',
    'else if (PART=="hood") hood_print_orientation();',
    'else if (PART=="cassette") cassette_print_orientation();',
    'else if (PART=="support_risk") support_risk_scene();',
    'else if (PART=="cassette_insertion_intersection") intersection()',
    'else if (PART=="cassette_hood_intersection") intersection()',
    'else if (PART=="cassette_base_intersection") intersection()',
    'else if (PART=="front_fastener_keepout_intersection") union()',
    'else if (PART=="front_fastener_service_intersection") union()',
    'else if (PART=="rear_hook_intersection") intersection()',
    'else if (PART=="base_psu_intersection") intersection()',
    'else if (PART=="c14_print_intersection") intersection()',
)

for retired in (
    "module seam_tongue",
    "module rail_spine_blank",
    "module barrier_lower_capture",
    "module barrier_upper_capture",
    "module conductor_retention_saddle",
    "[125.73,10]",
    "cube([72",
):
    if retired in SOURCE:
        raise SystemExit(f"retired failed geometry restored: {retired}")

if "text(" in SOURCE:
    raise SystemExit("printable enclosure source must contain no text geometry")

require(
    MAKEFILE,
    "NOZZLE_DIAMETER ?= 0.8",
    "check-power-system-enclosure-nozzle:",
    'assert n>0, "NOZZLE_DIAMETER must be greater than zero"',
    "POWER_SYSTEM_ENCLOSURE_DEFINES := -D 'NOZZLE_DIAMETER=$(NOZZLE_DIAMETER)'",
    "POWER_SYSTEM_ENCLOSURE_CASSETTE",
    'PART="base"',
    'PART="hood"',
    'PART="cassette"',
    'PART="installed_preview"',
    'PART="exploded"',
    'PART="open_top"',
    'PART="cassette_section"',
    'PART="barrier_seam_section"',
    'PART="front_fastener_hook_section"',
    'PART="support_risk"',
    'PART="print_orientations"',
    'PART="size_comparison"',
    "NOZZLE_DIAMETER=1.6",
    "WARNING: C14 snap membrane is 1.6 mm",
    "$(PYTHON) $(FINGERPRINT) $$mesh",
)

require(
    DOC,
    "V2 pre-DUT02 mechanical prototype",
    "not a certified mains enclosure",
    "Always unplug",
    "132.8 × 128 × 60 mm",
    "supports off",
    "0.8 mm nozzle",
    "NOZZLE_DIAMETER",
    "max(1.2 mm, nozzle diameter)",
    "sanding is required",
    "0.02/0.04 mm",
    "1.8 mm top-open groove",
    "Y=149.73, 306, and 330 mm",
    "protective-earth",
    "Fuse remains TBD",
)


def signed_volume(facets) -> float:
    total = 0.0
    for a, b, c in facets:
        total += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            + a[1] * (b[2] * c[0] - b[0] * c[2])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
    return abs(total)


def require_quantized_manifold(name: str, facets) -> None:
    """Reject connections that disappear on the shared 0.0001 mm identity grid."""
    edge_counts: Counter[tuple[tuple[int, int, int], tuple[int, int, int]]] = Counter()
    degenerate = 0
    for facet in facets:
        triangle = tuple(
            tuple(int(round(coordinate * 10000)) for coordinate in point)
            for point in facet
        )
        if len(set(triangle)) != 3:
            degenerate += 1
            continue
        for start, end in ((0, 1), (1, 2), (2, 0)):
            edge_counts[tuple(sorted((triangle[start], triangle[end])))] += 1
    invalid_edges = sum(count != 2 for count in edge_counts.values())
    if degenerate or invalid_edges:
        raise SystemExit(
            f"0.0001 mm quantized topology failure for {name}: "
            f"degenerate_facets={degenerate} invalid_edges={invalid_edges}"
        )


def mesh_contract(
    name: str,
    expected_size: tuple[float, float, float],
    min_bed_area: float,
) -> float:
    path = ROOT / "build" / name
    topology = inspect_topology(path)
    if topology["invalid_edges"] or topology["components"] != 1 or topology["degenerate_facets"]:
        raise SystemExit(f"mesh topology failure for {name}: {topology}")
    facets = triangles(path)
    require_quantized_manifold(name, facets)
    points = [point for triangle in facets for point in triangle]
    mins = tuple(min(p[axis] for p in points) for axis in range(3))
    maxs = tuple(max(p[axis] for p in points) for axis in range(3))
    size = tuple(maxs[axis] - mins[axis] for axis in range(3))
    if any(not math.isclose(got, want, abs_tol=5e-3) for got, want in zip(size, expected_size)):
        raise SystemExit(f"mesh bounds changed for {name}: expected={expected_size} got={size}")
    if not math.isclose(mins[2], 0.0, abs_tol=1e-6):
        raise SystemExit(f"declared print orientation does not touch Z=0: {name} {mins}")
    bed_area = 0.0
    for triangle in facets:
        if all(math.isclose(point[2], 0.0, abs_tol=1e-6) for point in triangle):
            a, b, c = triangle
            bed_area += abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])) / 2
    if bed_area < min_bed_area:
        raise SystemExit(f"insufficient bed contact for {name}: {bed_area:.3f} mm2")
    return signed_volume(facets)


base_volume = mesh_contract("power-system-enclosure-base.stl", (196.27, 132.8, 56.033), 1000)
hood_volume = mesh_contract("power-system-enclosure-hood.stl", (132.8, 128.0, 46.2), 1000)
cassette_volume = mesh_contract("power-system-enclosure-c14-cassette.stl", (66.3, 39.0, 7.2), 500)
combined = base_volume + hood_volume + cassette_volume
if combined > 270000:
    raise SystemExit(f"combined printed volume exceeds 270000 mm3: {combined:.3f}")

for name in (
    "power-system-enclosure-base_psu_intersection.stl",
    "power-system-enclosure-c14_print_intersection.stl",
):
    path = ROOT / "build" / name
    if path.exists() and signed_volume(triangles(path)) > 1e-3:
        raise SystemExit(f"nominal contact selector has positive interference volume: {name}")

barrier_svg = (ROOT / "build/power-system-terminal-barrier-template.svg").read_text()
barrier_dxf = (ROOT / "build/power-system-terminal-barrier-template.dxf").read_text()
if barrier_svg.count("<path d=") != 1 or barrier_dxf.splitlines().count("LINE") != 4:
    raise SystemExit("terminal barrier template must be one continuous rectangle")

old_volume = 336547.259
reduction = 100 * (old_volume - combined) / old_volume
print(
    "power_enclosure_contract=pass "
    f"parts=3 combined_volume_mm3={combined:.3f} old_volume_mm3={old_volume:.3f} "
    f"volume_reduction_percent={reduction:.2f} sealed_mm=132.8x128x60 "
    "nozzle_default_mm=0.8 support_plan=off"
)
