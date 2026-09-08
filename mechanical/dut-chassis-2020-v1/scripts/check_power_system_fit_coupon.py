#!/usr/bin/env python3
"""Focused source and generated-mesh contract for the power-system fit coupon."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "power-system-fit-coupon.scad").read_text()
sys.path.insert(0, str(ROOT / "scripts"))
from check_stl_topology import inspect_topology, triangles  # noqa: E402


def require(*fragments: str) -> None:
    missing = [item for item in fragments if item not in SOURCE]
    if missing:
        raise SystemExit(f"coupon source contract missing: {missing}")


require(
    "include <lib/alt-1205t-power-supply.scad>",
    "include <lib/iec-c14-fused-switch.scad>",
    "alt1205t_mounting_negatives(WALL_THICKNESS, coupon_m3_hole_diameter())",
    "iecc14_panel_cutout_negative(WALL_THICKNESS, IEC_CLEARANCE)",
    "coupon_iec_nominal_profile() = iecc14_body_profile_size()",
    "FIT COUPON — NO MAINS",
    "relaxed tongues are deliberately",
    "spring out and retain",
)

expected_defaults = {
    "IEC_CLEARANCE": "0.20",
    "M3_HOLE_CLEARANCE": "0.40",
    "NUT_TRAP_CLEARANCE": "0.25",
    "WALL_THICKNESS": "3.0",
    "LABEL_DEPTH": "0.35",
}
for name, expected in expected_defaults.items():
    match = re.search(rf"{name} = is_undef\({name}\) \? ([0-9.]+) : {name};", SOURCE)
    if not match or match.group(1) != expected:
        raise SystemExit(f"{name} default must be {expected} and explicitly overridable")

for assertion in (
    "alt1205t_base_size() == [77.5, 110]",
    "alt1205t_m3_centres() == [[23.8,29.9], [23.8,66], [51.8,66]]",
    "coupon_slot_origin() == [71.05, 2.94]",
    "coupon_iec_nominal_profile() == [27,41]",
    "[27 + 2*IEC_CLEARANCE, 41 + 2*IEC_CLEARANCE]",
    "coupon_nut_nominal_af() == 5.5",
    "coupon_nut_nominal_thickness() == 2.4",
):
    if assertion not in SOURCE:
        raise SystemExit(f"missing executable assertion: {assertion}")

# Every requested process variable must actually survive a non-default export;
# source-level is_undef declarations are insufficient if an assertion rejects it.

mesh = ROOT / "build/power-system-fit-coupon.stl"
topology = inspect_topology(mesh)
if topology["invalid_edges"] or topology["components"] != 1 or topology["degenerate_facets"]:
    raise SystemExit(f"coupon topology failure: {topology}")
points = [point for tri in triangles(mesh) for point in tri]
facets = triangles(mesh)
mins = tuple(min(p[axis] for p in points) for axis in range(3))
maxs = tuple(max(p[axis] for p in points) for axis in range(3))
if mins[2] != 0 or maxs[2] != 5:
    raise SystemExit(
        "coupon must lie flat at Z=0 with a 3.0 mm bed and 2.0 mm register, "
        f"got {mins[2]}..{maxs[2]}"
    )
if mins[0] > -36.5 or maxs[0] < 91 or mins[1] > -5 or maxs[1] < 112:
    raise SystemExit(f"coupon absolute L/datum bounds unexpectedly contracted: min={mins} max={maxs}")


def is_register_face(triangle, axis: int) -> bool:
    """Match a real vertical mesh face on a nominal PSU datum axis."""
    other = 1 - axis
    return (
        all(abs(point[axis]) < 1e-6 for point in triangle)
        and max(point[2] for point in triangle) == 5
        and min(point[2] for point in triangle) == 3
        and min(point[other] for point in triangle) >= 0
        and max(point[other] for point in triangle) >= 20
    )


if not any(is_register_face(triangle, 0) for triangle in facets):
    raise SystemExit("printable mesh lacks the PSU X=0 left registration shoulder")
if not any(is_register_face(triangle, 1) for triangle in facets):
    raise SystemExit("printable mesh lacks the PSU Y=0 top registration shoulder")
if any(x > 1e-6 and y > 1e-6 and z > 3 + 1e-6 for x, y, z in points):
    raise SystemExit("origin register overlaps the PSU plan envelope above its seating face")

print("power_system_fit_coupon_contract=pass wall_mm=3.0 register_axes=X0,Y0 register_height_mm=2.0 iec_clearance_per_side_mm=0.20 m3_hole_diameter_mm=3.4 nut_pocket_af_mm=5.75")
