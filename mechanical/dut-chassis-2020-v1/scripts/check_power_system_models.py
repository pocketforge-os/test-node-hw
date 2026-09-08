#!/usr/bin/env python3
"""Focused source contract for the owner-approved power component models."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSU = (ROOT / "lib/alt-1205t-power-supply.scad").read_text()
IEC = (ROOT / "lib/iec-c14-fused-switch.scad").read_text()
DISPATCH = (ROOT / "power-system-models.scad").read_text()


def require(text: str, fragments: tuple[str, ...], label: str) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise SystemExit(f"{label} source contract missing: {missing}")


require(PSU, (
    "function alt1205t_base_size() = [77.5, 110]",
    "function alt1205t_label_side_size() = [110, 36.86]",
    "function alt1205t_upper_right_slot_size() = [3.3, 4.7]",
    "function alt1205t_upper_right_slot_top_tangent() = 2.94",
    "function alt1205t_upper_right_slot_right_tangent() = 3.15",
    "[[23.8, 29.9], [23.8, 66], [51.8, 66]]",
    "[3.15, 6.6]", "[8.5, 36.86 - 17.25]", "6.9",
    "[110 - 11.16, 36.86 - 12.32]",
    "[5.75, 4, 10.4, 2.28, 2.61]",
    "function alt1205t_upper_right_square_is_hole() = false",
    "module alt1205t_keepout()", "module alt1205t_mounting_negatives",
), "ALT-1205T")

require(IEC, (
    "function iecc14_faceplate_size() = [31, 50.3, 2]",
    "function iecc14_body_profile_size() = [27, 41]",
    "function iecc14_body_depth() = 21.8",
    "function iecc14_top_straight_length() = 16",
    "function iecc14_chamfer_edge_length() = 8",
    "function iecc14_tab_depth_widths() = [8, 5.5]",
    "function iecc14_tab_height() = 5",
    "function iecc14_tab_top_setback() = 10.5",
    "function iecc14_tab_relief() = 1",
    "function iecc14_tab_lateral_inset_assumption() = 4.5",
    "module iecc14_keepout", "module iecc14_panel_cutout_negative",
    "module iecc14_tab_relief_negatives",
    "entire lower edge left joined to the parent wall",
    "never the rejected 4.5 mm interpretation",
), "IEC C14")

require(DISPATCH, (
    'PART = "power_system_review"', 'PART == "alt_1205t_psu"',
    'PART == "iec_c14_fused_switch"',
    'PART == "iec_c14_panel_cutout_negative"',
), "dispatcher")

print("power_system_model_contract=pass psu_datum=top-left-underbody iec_face_datum=z0")
