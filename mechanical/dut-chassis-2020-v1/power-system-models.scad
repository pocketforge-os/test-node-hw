use <lib/alt-1205t-power-supply.scad>
use <lib/iec-c14-fused-switch.scad>

PART = "power_system_review";
VIEW = "front";
IEC_CLEARANCE = is_undef(IEC_CLEARANCE) ? 0 : IEC_CLEARANCE;

if (PART == "alt_1205t_psu")
    alt1205t_keepout();
else if (PART == "alt_1205t_psu_mounting_negatives")
    alt1205t_mounting_negatives();
else if (PART == "alt_1205t_psu_evidence")
    alt1205t_evidence(VIEW);
else if (PART == "iec_c14_fused_switch")
    iecc14_keepout();
else if (PART == "iec_c14_panel_cutout_negative")
    iecc14_panel_cutout_negative(clearance=IEC_CLEARANCE);
else if (PART == "iec_c14_fused_switch_evidence")
    iecc14_evidence(VIEW);
else if (PART == "power_system_review") {
    translate([-58, -55, 0]) alt1205t_evidence("underside");
    translate([58, 0, 2]) iecc14_evidence("front");
} else
    assert(false, str("Unknown power-system PART: ", PART));
