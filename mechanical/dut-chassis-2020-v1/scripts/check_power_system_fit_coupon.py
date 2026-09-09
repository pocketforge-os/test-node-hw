#!/usr/bin/env python3
"""Focused source and generated-mesh contract for the power-system fit coupon."""

from pathlib import Path
import math
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
    "alt1205t_mounting_negatives(",
    "coupon_psu_outline_margin() + 0.02",
    "iecc14_panel_cutout_negative(WALL_THICKNESS, IEC_CLEARANCE)",
    "coupon_iec_nominal_profile() = iecc14_body_profile_size()",
    "function coupon_iec_faceplate_overlap_per_side()",
    "IEC faceplate must cover the clearanced panel opening on every side",
    'PART = is_undef(PART) ? "printable_coupon" : PART;',
    'if (PART == "printable_coupon") printable_coupon();',
    'else if (PART == "evidence")',
    'text("FIT COUPON"',
    'text("NO MAINS"',
    "relaxed tongues are deliberately",
    "spring out and retain",
    'text("NUT SAMPLE"',
    'text("NOT PSU"',
)

# Printable geometry and evidence annotations are deliberately separated. The
# default selector reaches only modules defined before evidence_overlay(), so a
# text primitive cannot become physical geometry without this contract failing.
evidence_marker = "module evidence_overlay()"
if SOURCE.count(evidence_marker) != 1:
    raise SystemExit("coupon must define exactly one evidence-only annotation module")
printable_source, evidence_source = SOURCE.split(evidence_marker, 1)
if "text(" in printable_source:
    raise SystemExit("printable coupon path contains text-derived geometry")
if "evidence_overlay" in printable_source:
    raise SystemExit("printable coupon path calls the evidence annotation module")
for retired in ("LABEL_DEPTH", "recessed_label", "EVIDENCE"):
    if retired in SOURCE:
        raise SystemExit(f"retired printable label path remains: {retired}")
if "text(" not in evidence_source:
    raise SystemExit("evidence selector unexpectedly lost its non-printable annotations")

expected_defaults = {
    "IEC_CLEARANCE": "0.20",
    "M3_HOLE_CLEARANCE": "0.40",
    "NUT_TRAP_CLEARANCE": "0.25",
    "WALL_THICKNESS": "3.0",
}
for name, expected in expected_defaults.items():
    match = re.search(rf"{name} = is_undef\({name}\) \? ([0-9.]+) : {name};", SOURCE)
    if not match or match.group(1) != expected:
        raise SystemExit(f"{name} default must be {expected} and explicitly overridable")

for assertion in (
    "alt1205t_base_size() == [77.5, 110]",
    "alt1205t_m3_centres() == [[26.8,32.9], [26.8,69], [54.8,69]]",
    "alt1205t_upper_left_m3_centre() == [3.45,3.45]",
    "alt1205t_lower_left_m3_centre() == [7.25,99.6]",
    "[[3.45,3.45], [26.8,32.9], [26.8,69], [54.8,69], [7.25,99.6]]",
    "coupon_slot_origin() == [71.05, 2.94]",
    "coupon_bottom_slot_origin() == [2.28,106]",
    "coupon_bottom_slot_size() == [2.61,4]",
    "coupon_iec_nominal_profile() == [27,46.86]",
    "[27 + 2*IEC_CLEARANCE, 46.86 + 2*IEC_CLEARANCE]",
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
facets = triangles(mesh)
points = [point for tri in facets for point in tri]
mins = tuple(min(p[axis] for p in points) for axis in range(3))
maxs = tuple(max(p[axis] for p in points) for axis in range(3))
approved_corrected_bounds = ((-36.5, -5.0, 0.0), (91.5, 112.0, 5.0))
if (mins, maxs) != approved_corrected_bounds:
    raise SystemExit(
        "label removal changed the approved corrected coupon bounds: "
        f"expected={approved_corrected_bounds} got={(mins, maxs)}"
    )


def signed_volume(triangle) -> float:
    """Return one triangle's signed tetrahedral volume against the origin."""
    a, b, c = triangle
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) / 6


volume_mm3 = abs(sum(signed_volume(triangle) for triangle in facets))
approved_corrected_recessed_text_volume_mm3 = 9114.568
if volume_mm3 <= approved_corrected_recessed_text_volume_mm3:
    raise SystemExit(
        "removing recessed text must restore solid material without changing "
        f"the mating envelope: baseline={approved_corrected_recessed_text_volume_mm3} "
        f"got={volume_mm3:.3f}"
    )
expected_label_free_volume_mm3 = 9127.349
if not math.isclose(volume_mm3, expected_label_free_volume_mm3, abs_tol=0.01):
    raise SystemExit(
        "label-free solid volume drifted from its reviewed geometry: "
        f"expected={expected_label_free_volume_mm3} got={volume_mm3:.3f}"
    )


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

# Prove that the rendered coupon, not just its source text, contains the five
# physical M3 checks at the corrected/reinterpreted centers. OpenSCAD's 36-sided
# cylinders give 36 vertices at each of the Z=0 and Z=3 rim planes.
m3_centres = ((3.45, 3.45), (26.8, 32.9), (26.8, 69),
              (54.8, 69), (7.25, 99.6))
m3_radius = 1.7
for centre in m3_centres:
    rim = {
        point for point in points
        if math.isclose(
            math.hypot(point[0] - centre[0], point[1] - centre[1]),
            m3_radius,
            abs_tol=5e-4,
        )
    }
    rim_planes = {point[2] for point in rim}
    if len(rim) < 60 or rim_planes != {0.0, 3.0}:
        raise SystemExit(
            f"coupon lacks a complete 3.4 mm through-hole rim at {centre}: "
            f"vertices={len(rim)} z={sorted(rim_planes)}"
        )

# The measured 2.61 x 4.0 mm lower slot must remain an actual +Y edge opening,
# even though the sparse coupon adds a 2 mm registration outline around the PSU.
slot_xs = (2.28, 2.28 + 2.61)
for slot_x in slot_xs:
    side_vertices = {
        point for point in points
        if math.isclose(point[0], slot_x, abs_tol=1e-6)
        and point[1] >= 106
    }
    if not side_vertices or max(point[1] for point in side_vertices) != 112:
        raise SystemExit(
            f"bottom-slot side at X={slot_x} does not reach the coupon edge"
        )
    if {point[2] for point in side_vertices} != {0.0, 3.0}:
        raise SystemExit(f"bottom-slot side at X={slot_x} is not through-wall")
if any(
    all(math.isclose(point[1], 112, abs_tol=1e-6) for point in triangle)
    and min(point[0] for point in triangle) >= slot_xs[0] - 1e-6
    and max(point[0] for point in triangle) <= slot_xs[1] + 1e-6
    and max(point[2] for point in triangle) - min(point[2] for point in triangle) > 2.9
    for triangle in facets
):
    raise SystemExit("bottom slot is closed by a vertical face at the coupon edge")

print(f"power_system_fit_coupon_contract=pass physical_text=none evidence_annotations=isolated wall_mm=3.0 register_axes=X0,Y0 register_height_mm=2.0 iec_profile_mm=27x46.86 iec_clearance_per_side_mm=0.20 m3_checks=5 m3_hole_diameter_mm=3.4 bottom_open_slot_mm=2.61x4 nut_pocket_af_mm=5.75 volume_mm3={volume_mm3:.3f}")
