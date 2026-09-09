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
    "iecc14_panel_cutout_negative(coupon_iec_snap_wall_target(), IEC_CLEARANCE)",
    "coupon_iec_nominal_profile() = iecc14_body_profile_size()",
    "function coupon_iec_faceplate_overlap_per_side()",
    "function coupon_iec_snap_wall_target() = 1.2",
    "function coupon_iec_surface_allowance() = 0.1",
    "function coupon_iec_budgeted_wall_max() = 1.3",
    "function coupon_iec_owner_wall_hard_limit() = 1.5",
    "coupon_upper_left_register_clearance_negative();",
    "linear_extrude(height=coupon_iec_snap_wall_target()) iec_panel_2d();",
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
    "[[25.3,30.9], [25.3,67], [53.3,67]]",
    "alt1205t_upper_left_m3_centre() == [4.95,4.95]",
    "alt1205t_lower_left_m3_centre() == [6.75,98.6]",
    "[[4.95,4.95], [25.3,30.9], [25.3,67], [53.3,67], [6.75,98.6]]",
    "coupon_slot_origin() == [71.05, 2.94]",
    "coupon_bottom_slot_origin() == [2.28,106]",
    "coupon_bottom_slot_size() == [2.61,4]",
    "coupon_iec_nominal_profile() == [27,46.86]",
    "[27 + 2*IEC_CLEARANCE, 46.86 + 2*IEC_CLEARANCE]",
    "coupon_iec_centre() == [-19,80] && coupon_panel_size() == [35,54]",
    "coupon_nut_nominal_af() == 5.5",
    "coupon_nut_nominal_thickness() == 2.4",
    "coupon_nut_centre() == [85,8]",
    "coupon_register_height() == 2.0",
    "coupon_iec_snap_wall_target() + coupon_iec_surface_allowance() ==",
    "coupon_iec_budgeted_wall_max()",
    "coupon_iec_budgeted_wall_max() < coupon_iec_owner_wall_hard_limit()",
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
approved_frozen_bounds = ((-36.5, -5.0, 0.0), (91.5, 112.0, 5.0))
if (mins, maxs) != approved_frozen_bounds:
    raise SystemExit(
        "third-fit correction changed the frozen coupon bounds: "
        f"expected={approved_frozen_bounds} got={(mins, maxs)}"
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
approved_pre_release_volume_mm3 = 7994.313
expected_release_volume_mm3 = 7994.985
if not math.isclose(volume_mm3, expected_release_volume_mm3, abs_tol=0.01):
    raise SystemExit(
        "release coupon solid volume drifted after the isolated upper-left move: "
        f"baseline={approved_pre_release_volume_mm3} "
        f"expected={expected_release_volume_mm3} got={volume_mm3:.3f}"
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
# physical M3 checks at the owner-confirmed final-fit centers. OpenSCAD's
# 36-sided cylinders give complete rims at Z=0 and the 3.0 mm wall top.
m3_centres = ((4.95, 4.95), (25.3, 30.9), (25.3, 67),
              (53.3, 67), (6.75, 98.6))
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

# Freeze the approved upper-right 3.3 x 4.7 oblong slot in the generated mesh,
# including the 2.94 top and 3.15 right tangencies. These are the six cardinal
# points of the two D=3.3 end circles at Y=4.59 and Y=5.99.
mesh_points = set(points)
upper_right_slot_cardinals = (
    (71.05, 4.59), (71.05, 5.99),
    (74.35, 4.59), (74.35, 5.99),
    (72.7, 2.94), (72.7, 7.64),
)
for x, y in upper_right_slot_cardinals:
    for z in (0.0, 3.0):
        if (x, y, z) not in mesh_points:
            raise SystemExit(
                "approved upper-right slot mesh cardinal is missing: "
                f"{(x, y, z)}"
            )

# Freeze the IEC XY/profile/clearance at the six vertices of the true 0.20 mm
# contour-offset cavity. Only their top Z changes with the local panel target.
iec_clearanced_profile_xy = (
    (-32.7, 56.37), (-32.7, 97.7002),
    (-27.0861, 103.63), (-10.9139, 103.63),
    (-5.3, 97.7002), (-5.3, 56.37),
)
for x, y in iec_clearanced_profile_xy:
    for z in (0.0, 1.2):
        if (x, y, z) not in mesh_points:
            raise SystemExit(
                "frozen IEC +0.20 mm contour vertex is missing: "
                f"{(x, y, z)}"
            )

# Freeze the separate nut sampler directly in the exported mesh: outside
# D=13 cardinals, D=3.4 screw rim/floor, and 5.75 mm-AF pocket corners.
for x, y in ((91.5, 8), (78.5, 8), (85, 1.5), (85, 14.5)):
    for z in (0.0, 3.0):
        if (x, y, z) not in mesh_points:
            raise SystemExit(f"frozen nut-sampler outer cardinal is missing: {(x,y,z)}")
nut_rim = {
    point for point in points
    if math.isclose(math.hypot(point[0] - 85, point[1] - 8), 1.7, abs_tol=5e-4)
}
if len(nut_rim) < 60 or {point[2] for point in nut_rim} != {0.0, 0.4}:
    raise SystemExit("frozen nut-sampler M3 rim or retained floor changed")
nut_hex_xy = (
    (88.3198, 8.0), (86.6599, 10.875), (83.3401, 10.875),
    (81.6802, 8.0), (83.3401, 5.125), (86.6599, 5.125),
)
for x, y in nut_hex_xy:
    for z in (0.4, 3.0):
        if (x, y, z) not in mesh_points:
            raise SystemExit(f"frozen nut-sampler hex vertex is missing: {(x,y,z)}")

# The inlet's whole faceplate/tab seating footprint must be the local 1.2 mm
# snap panel: 3.0 mm structural material may connect outside this footprint but
# may not intrude into it. Surface roughness allowance is a process budget, not
# modeled thickness, so 1.2 + 0.1 produces a 1.3 mm budget below the owner's
# hard 1.5 mm maximum.
iec_snap_wall_target = 1.2
iec_surface_allowance = 0.1
iec_budgeted_wall_max = 1.3
iec_owner_wall_hard_limit = 1.5
if not math.isclose(
    iec_snap_wall_target + iec_surface_allowance,
    iec_budgeted_wall_max,
    abs_tol=1e-9,
):
    raise SystemExit("IEC local wall and surface allowance must total 1.3 mm")
if iec_budgeted_wall_max >= iec_owner_wall_hard_limit:
    raise SystemExit("IEC 1.3 mm budget must remain below owner 1.5 mm limit")
faceplate_bounds = (-34.5, -3.5, 54.85, 105.15)
faceplate_points = {
    point for point in points
    if faceplate_bounds[0] - 1e-6 <= point[0] <= faceplate_bounds[1] + 1e-6
    and faceplate_bounds[2] - 1e-6 <= point[1] <= faceplate_bounds[3] + 1e-6
}
faceplate_z = {point[2] for point in faceplate_points}
if not faceplate_points or faceplate_z != {0.0, iec_snap_wall_target}:
    raise SystemExit(
        "IEC faceplate/tab seating footprint is not exclusively the local "
        f"1.2 mm panel: z={sorted(faceplate_z)}"
    )
if any(point[2] > iec_snap_wall_target + 1e-6 for point in faceplate_points):
    raise SystemExit("3.0 mm coupon structure intrudes into the IEC retention envelope")
if not any(math.isclose(point[2], 3.0, abs_tol=1e-6) for point in points):
    raise SystemExit("structural PSU/nut coupon wall no longer reaches 3.0 mm")

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

print(f"power_system_fit_coupon_contract=pass physical_text=none evidence_annotations=isolated structural_wall_mm=3.0 iec_snap_wall_mm=1.2 iec_surface_allowance_mm=0.1 iec_budgeted_wall_max_mm=1.3 iec_owner_wall_hard_limit_mm=1.5 iec_retention_intrusion=none register_axes=X0,Y0 register_height_mm=2.0 iec_profile_mm=27x46.86 iec_clearance_per_side_mm=0.20 m3_centres={m3_centres} m3_hole_diameter_mm=3.4 upper_right_slot=frozen bottom_open_slot_mm=2.61x4 nut_pocket_af_mm=5.75 volume_mm3={volume_mm3:.3f}")
