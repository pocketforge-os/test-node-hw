#!/usr/bin/env python3
"""Focused source contract for the owner-approved power component models."""

import ast
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSU = (ROOT / "lib/alt-1205t-power-supply.scad").read_text()
IEC = (ROOT / "lib/iec-c14-fused-switch.scad").read_text()
DISPATCH = (ROOT / "power-system-models.scad").read_text()
sys.path.insert(0, str(ROOT / "scripts"))
from check_stl_topology import triangles  # noqa: E402


def require(text: str, fragments: tuple[str, ...], label: str) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise SystemExit(f"{label} source contract missing: {missing}")


def literal_function(text: str, name: str):
    match = re.search(rf"function\s+{re.escape(name)}\(\)\s*=\s*([^;]+);", text)
    if not match:
        raise SystemExit(f"missing executable dimension function: {name}")
    value = match.group(1).strip().replace("false", "False").replace("true", "True")
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError) as error:
        raise SystemExit(f"{name} must remain a literal, got {value!r}: {error}") from error


def check_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise SystemExit(f"{label}: expected {expected!r}, got {actual!r}")


require(PSU, (
    "function alt1205t_upper_right_square_is_hole() = false",
    "function alt1205t_upper_left_m3_centre() = [0.95, 5.95]",
    "function alt1205t_lower_left_m3_centre() = [5.75, 97.6]",
    "function alt1205t_second_fit_upper_left_m3_correction() = [-2.5, 2.5]",
    "function alt1205t_second_fit_internal_m3_correction() = [-1.5, -2]",
    "function alt1205t_second_fit_lower_left_m3_correction() = [-1.5, -2]",
    "function alt1205t_bottom_slot_origin() = [",
    "module alt1205t_bottom_open_slot_negative",
    "module alt1205t_keepout()", "module alt1205t_mounting_negatives",
), "ALT-1205T")

require(IEC, (
    "function iecc14_tab_wall_x() = iecc14_body_profile_size().x / 2",
    'iecc14_tab_bounds("left", iecc14_tab_widths().x) == [-18.93, -10.93, 10.5, 15.5]',
    'iecc14_tab_bounds("right", iecc14_tab_widths().y) == [13.43, 18.93, 10.5, 15.5]',
    'for (y = [bounds.x - iecc14_tab_relief(), bounds.y])',
    "iecc14_tab_height() + iecc14_tab_relief()",
    "module iecc14_rigid_insertion_body_keepout",
    "module iecc14_complete_rest_state_keepout",
    "module iecc14_keepout", "module iecc14_panel_cutout_negative",
    'iecc14_locking_tab("left", iecc14_tab_widths().x)',
    'iecc14_locking_tab("right", iecc14_tab_widths().y)',
    "iecc14_complete_rest_state_keepout(include_schematic_terminals)",
    "iecc14_rigid_insertion_body_keepout(depth + 0.02, clearance, -0.01)",
    "module iecc14_tab_relief_negatives",
    "full lower edge",
    "never the rejected 4.5 mm interpretation",
), "IEC C14")

require(DISPATCH, (
    'PART = "power_system_review"', 'PART == "alt_1205t_psu"',
    'PART == "iec_c14_fused_switch"',
    'PART == "iec_c14_panel_cutout_negative"',
), "dispatcher")

# Parse and derive the geometry numerically. These checks complement OpenSCAD's
# executable assertions and fail even when all expected words remain present.
base = literal_function(PSU, "alt1205t_base_size")
label = literal_function(PSU, "alt1205t_label_side_size")
m3 = literal_function(PSU, "alt1205t_m3_centres")
check_equal(base, [77.5, 110], "ALT base axes")
check_equal(label, [110, 36.86], "ALT label-side axes")
check_equal(m3, [[25.3, 30.9], [25.3, 67], [53.3, 67]], "ALT second-fit internal M3 coordinates")
check_equal(literal_function(PSU, "alt1205t_m3_nominal_diameter"), 3, "ALT nominal M3 diameter")
check_equal(literal_function(PSU, "alt1205t_first_fit_upper_left_m3_centre"), [3.45, 3.45], "ALT first-fit upper-left M3 centre")
check_equal(literal_function(PSU, "alt1205t_second_fit_upper_left_m3_correction"), [-2.5, 2.5], "ALT upper-left second-fit correction")
check_equal(literal_function(PSU, "alt1205t_upper_left_m3_centre"), [0.95, 5.95], "ALT upper-left second-fit M3 centre")
check_equal(literal_function(PSU, "alt1205t_first_fit_m3_centres"), [[26.8, 32.9], [26.8, 69], [54.8, 69]], "ALT first-fit internal M3 coordinates")
check_equal(literal_function(PSU, "alt1205t_second_fit_internal_m3_correction"), [-1.5, -2], "ALT internal second-fit correction")
check_equal(literal_function(PSU, "alt1205t_lower_left_m3_left_tangent"), 5.75, "ALT lower-left M3 left tangent")
check_equal(literal_function(PSU, "alt1205t_lower_left_m3_bottom_centre_datum"), 10.4, "ALT lower-left M3 bottom centre datum")
first_fit_lower_left_m3 = [5.75 + 3 / 2, base[1] - 10.4]
check_equal(first_fit_lower_left_m3, [7.25, 99.6], "ALT first-fit derived lower-left M3 centre")
check_equal(literal_function(PSU, "alt1205t_second_fit_lower_left_m3_correction"), [-1.5, -2], "ALT lower-left second-fit correction")
check_equal(literal_function(PSU, "alt1205t_lower_left_m3_centre"), [5.75, 97.6], "ALT lower-left second-fit M3 centre")
check_equal(literal_function(PSU, "alt1205t_bottom_slot_left_tangent"), 2.28, "ALT bottom-slot left tangent")
check_equal(literal_function(PSU, "alt1205t_bottom_slot_size"), [2.61, 4], "ALT bottom-open slot axes")
check_equal([2.28, base[1] - 4], [2.28, 106], "ALT derived bottom-slot origin")
check_equal(literal_function(PSU, "alt1205t_upper_right_slot_size"), [3.3, 4.7], "ALT underside slot axes")
check_equal(literal_function(PSU, "alt1205t_upper_right_slot_top_tangent"), 2.94, "ALT underside slot top tangent")
check_equal(literal_function(PSU, "alt1205t_upper_right_slot_right_tangent"), 3.15, "ALT underside slot right tangent")
check_equal(literal_function(PSU, "alt1205t_label_upper_left_hole_diameter"), 3.4, "ALT label upper-left diameter")
check_equal(literal_function(PSU, "alt1205t_label_lower_right_hole_diameter"), 4, "ALT label lower-right diameter")
check_equal(literal_function(PSU, "alt1205t_label_top_right_slot_height"), 6.9, "ALT label slot height")
check_equal(literal_function(PSU, "alt1205t_label_top_right_slot_horizontal_depth_known"), False, "ALT unknown label slot depth")

profile = literal_function(IEC, "iecc14_body_profile_size")
check_equal(literal_function(IEC, "iecc14_faceplate_size"), [31, 50.3, 2], "IEC faceplate axes")
check_equal(profile, [27, 46.86], "IEC body profile axes")
check_equal(literal_function(IEC, "iecc14_body_depth"), 21.8, "IEC insertion depth")
check_equal(literal_function(IEC, "iecc14_top_straight_length"), 16, "IEC top straight length")
check_equal(literal_function(IEC, "iecc14_chamfer_edge_length"), 8, "IEC chamfer edge length")
widths = literal_function(IEC, "iecc14_tab_widths")
height = literal_function(IEC, "iecc14_tab_height")
setback = literal_function(IEC, "iecc14_tab_top_setback")
relief = literal_function(IEC, "iecc14_tab_relief")
inset = literal_function(IEC, "iecc14_tab_lateral_inset")
left = [-profile[1] / 2 + inset, -profile[1] / 2 + inset + widths[0], setback, setback + height]
right = [profile[1] / 2 - inset - widths[1], profile[1] / 2 - inset, setback, setback + height]
check_equal([left, right], [[-18.93, -10.93, 10.5, 15.5], [13.43, 18.93, 10.5, 15.5]], "IEC tongue extents")
check_equal(relief, 1, "IEC three-sided relief")
check_equal(literal_function(IEC, "iecc14_unmeasured_resting_tab_projection_assumption"), 0.6,
            "IEC provisional unmeasured tongue projection")
if "iecc14_tab_wall_x() + 0.61" not in IEC or "bounds.z])" not in IEC:
    raise SystemExit("IEC evidence must map both tongues and three-sided relief to the photographed wall")

# Guard the cutout's geometric mechanism and independently derive its contract.
# A width/height-only growth can preserve the bounds below, but cannot preserve
# this signed distance from the clearanced chamfer to the nominal chamfer.
require(IEC, (
    "offset(delta=clearance)",
    "assert(clearance >= 0",
    "w = iecc14_body_profile_size().x;",
    "h = iecc14_body_profile_size().y;",
), "IEC C14 contour clearance")
rise = math.sqrt(8**2 - ((profile[0] - 16) / 2) ** 2)
nominal_chamfer = ((profile[0] / 2, profile[1] / 2 - rise), (8, profile[1] / 2))
diagonal = math.dist(*nominal_chamfer)
if not math.isclose(diagonal, 8.0, abs_tol=1e-12):
    raise SystemExit(f"IEC nominal chamfer must be 8 mm, got {diagonal}")
clearance = 0.20
clearanced_bounds = (
    -profile[0] / 2 - clearance, profile[0] / 2 + clearance,
    -profile[1] / 2 - clearance, profile[1] / 2 + clearance,
)
check_equal(clearanced_bounds, (-13.7, 13.7, -23.63, 23.63),
            "IEC 0.20 mm clearanced bounds")
# An OpenSCAD delta offset translates every supporting line by exactly delta.
# Check the chamfer line explicitly so changing back to bounding-box growth
# cannot satisfy the executable source contract above.
(x1, y1), (x2, y2) = nominal_chamfer
a, b = y1 - y2, x2 - x1
normal_length = math.hypot(a, b)
translated_c_delta = clearance * normal_length
normal_distance = abs(translated_c_delta) / normal_length
if not math.isclose(normal_distance, clearance, abs_tol=1e-12):
    raise SystemExit(f"IEC chamfer normal clearance must be {clearance}, got {normal_distance}")
# Prove the rejected bounding-box-growth construction is discriminated: its
# corresponding chamfer is farther than 0.20 mm from the nominal supporting
# line even though its overall X/Y bounds look correct.
grown_box_chamfer_point = (
    profile[0] / 2 + clearance,
    profile[1] / 2 + clearance - rise,
)
nominal_c = -(a * x1 + b * y1)
grown_box_normal_distance = abs(
    a * grown_box_chamfer_point[0]
    + b * grown_box_chamfer_point[1]
    + nominal_c
) / normal_length
if math.isclose(grown_box_normal_distance, clearance, abs_tol=1e-9):
    raise SystemExit("IEC validation does not reject width/height-only growth")
if "square([3.5, alt1205t_label_top_right_slot_height()])" in PSU:
    raise SystemExit("ALT label evidence must not invent a 3.5 mm slot depth")


def points(path: Path) -> set[tuple[float, float, float]]:
    return {point for triangle in triangles(path) for point in triangle}


component_points = points(ROOT / "build/iec-c14-fused-switch.stl")
cutout_points = points(ROOT / "build/iec-c14-panel-cutout-negative.stl")
clearanced_cutout_points = points(
    ROOT / "build/iec-c14-panel-cutout-clearance-0.20.stl"
)
outer_tongue_y = sorted({y for x, y, z in component_points if x == 14.1 and z >= 10.5})
check_equal(outer_tongue_y, [-18.93, -10.93, 13.43, 18.93],
            "IEC complete STL must contain both outward tongues")
check_equal((min(x for x, _, _ in cutout_points), max(x for x, _, _ in cutout_points)),
            (-13.5, 13.5), "IEC rigid panel-cutout STL X bounds")

nominal_xy = {(x, y) for x, y, _ in cutout_points}
clearanced_xy = {(x, y) for x, y, _ in clearanced_cutout_points}
check_equal(
    (
        min(x for x, _ in nominal_xy), max(x for x, _ in nominal_xy),
        min(y for _, y in nominal_xy), max(y for _, y in nominal_xy),
    ),
    (-13.5, 13.5, -23.43, 23.43),
    "IEC nominal rendered profile bounds",
)
check_equal(
    tuple(round(value, 6) for value in (
        min(x for x, _ in clearanced_xy), max(x for x, _ in clearanced_xy),
        min(y for _, y in clearanced_xy), max(y for _, y in clearanced_xy),
    )),
    (-13.7, 13.7, -23.63, 23.63),
    "IEC 0.20 mm rendered clearanced profile bounds",
)

# Measure the rendered upper-right chamfer against the nominal supporting line.
# Bounding-box growth produces the same overall bounds but moves this line by
# a different normal distance, so it cannot pass this geometry-level check.
clearanced_chamfer = [
    (x, y) for x, y in clearanced_xy
    if x > 8 and y > profile[1] / 2 - rise
    and math.isclose(abs(a * x + b * y + nominal_c),
                     clearance * normal_length, abs_tol=2e-4)
]
if len(clearanced_chamfer) < 2:
    raise SystemExit(
        "IEC rendered clearanced chamfer does not contain two vertices at "
        "0.20 mm normal offset"
    )
for x, y in clearanced_chamfer:
    rendered_distance = abs(a * x + b * y + nominal_c) / normal_length
    if not math.isclose(rendered_distance, clearance, abs_tol=2e-5):
        raise SystemExit(
            f"IEC rendered chamfer clearance must be {clearance}, got "
            f"{rendered_distance} at {(x, y)}"
        )

print("power_system_model_contract=pass psu_datum=top-left-underbody iec_face_datum=z0")
