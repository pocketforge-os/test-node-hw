#!/usr/bin/env python3
"""Focused source contract for the owner-approved power component models."""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSU = (ROOT / "lib/alt-1205t-power-supply.scad").read_text()
IEC = (ROOT / "lib/iec-c14-fused-switch.scad").read_text()
DISPATCH = (ROOT / "power-system-models.scad").read_text()


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
    "module alt1205t_keepout()", "module alt1205t_mounting_negatives",
), "ALT-1205T")

require(IEC, (
    "function iecc14_tab_wall_x() = iecc14_body_profile_size().x / 2",
    'iecc14_tab_bounds("left", iecc14_tab_widths().x) == [-16, -8, 10.5, 15.5]',
    'iecc14_tab_bounds("right", iecc14_tab_widths().y) == [10.5, 16, 10.5, 15.5]',
    'for (y = [bounds.x - iecc14_tab_relief(), bounds.y])',
    "iecc14_tab_height() + iecc14_tab_relief()",
    "module iecc14_keepout", "module iecc14_panel_cutout_negative",
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
check_equal(m3, [[23.8, 29.9], [23.8, 66], [51.8, 66]], "ALT M3 coordinates")
check_equal(literal_function(PSU, "alt1205t_upper_left_aperture_size"), [3.45, 3.45], "ALT upper-left aperture")
check_equal(literal_function(PSU, "alt1205t_upper_right_slot_size"), [3.3, 4.7], "ALT underside slot axes")
check_equal(literal_function(PSU, "alt1205t_upper_right_slot_top_tangent"), 2.94, "ALT underside slot top tangent")
check_equal(literal_function(PSU, "alt1205t_upper_right_slot_right_tangent"), 3.15, "ALT underside slot right tangent")
check_equal(literal_function(PSU, "alt1205t_label_upper_left_hole_diameter"), 3.4, "ALT label upper-left diameter")
check_equal(literal_function(PSU, "alt1205t_label_lower_right_hole_diameter"), 4, "ALT label lower-right diameter")
check_equal(literal_function(PSU, "alt1205t_label_top_right_slot_height"), 6.9, "ALT label slot height")
check_equal(literal_function(PSU, "alt1205t_label_top_right_slot_horizontal_depth_known"), False, "ALT unknown label slot depth")

profile = literal_function(IEC, "iecc14_body_profile_size")
check_equal(literal_function(IEC, "iecc14_faceplate_size"), [31, 50.3, 2], "IEC faceplate axes")
check_equal(profile, [27, 41], "IEC body profile axes")
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
check_equal([left, right], [[-16, -8, 10.5, 15.5], [10.5, 16, 10.5, 15.5]], "IEC tongue extents")
check_equal(relief, 1, "IEC three-sided relief")
if "iecc14_tab_wall_x() + 0.61" not in IEC or "bounds.z])" not in IEC:
    raise SystemExit("IEC evidence must map both tongues and three-sided relief to the photographed wall")
if "square([3.5, alt1205t_label_top_right_slot_height()])" in PSU:
    raise SystemExit("ALT label evidence must not invent a 3.5 mm slot depth")

print("power_system_model_contract=pass psu_datum=top-left-underbody iec_face_datum=z0")
