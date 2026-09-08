/*
 * Source-owned semantic model of the owner-measured ALT-1205T 12 V / 5 A PSU.
 *
 * Datum: underside top-left corner; +X right, +Y down, +Z toward the label
 * side.  Dimensions are physical millimetres.  See alt-1205t-power-supply.md
 * for private-evidence provenance and deliberately unresolved measurements.
 */

function alt1205t_base_size() = [77.5, 110];
function alt1205t_label_side_size() = [110, 36.86];
function alt1205t_upper_left_aperture_size() = [3.45, 3.45];
function alt1205t_upper_right_slot_size() = [3.3, 4.7];
function alt1205t_upper_right_slot_top_tangent() = 2.94;
function alt1205t_upper_right_slot_right_tangent() = 3.15;
function alt1205t_m3_centres() = [[23.8, 29.9], [23.8, 66], [51.8, 66]];
function alt1205t_label_upper_left_hole_diameter() = 3.4;
function alt1205t_label_upper_left_hole_centre() = [3.15, 6.6];
function alt1205t_label_second_m3_centre() = [8.5, 36.86 - 17.25];
function alt1205t_label_top_right_slot_height() = 6.9;
function alt1205t_label_top_right_slot_horizontal_depth_known() = false;
function alt1205t_label_lower_right_hole_diameter() = 4;
function alt1205t_label_lower_right_hole_centre() = [110 - 11.16, 36.86 - 12.32];
function alt1205t_lower_left_unresolved_leaders() = [5.75, 4, 10.4, 2.28, 2.61];
function alt1205t_upper_right_square_is_hole() = false;

module alt1205t_contract() {
    assert(alt1205t_base_size() == [77.5, 110], "ALT-1205T base datum changed");
    assert(alt1205t_label_side_size() == [110, 36.86], "ALT-1205T corrected label height changed");
    assert(alt1205t_upper_left_aperture_size() == [3.45, 3.45], "ALT-1205T upper-left aperture axes changed");
    assert(alt1205t_upper_right_slot_size() == [3.3, 4.7] && alt1205t_upper_right_slot_top_tangent() == 2.94 && alt1205t_upper_right_slot_right_tangent() == 3.15, "ALT-1205T underside upper-right slot mapping changed");
    assert(alt1205t_m3_centres() == [[23.8, 29.9], [23.8, 66], [51.8, 66]], "ALT-1205T underside M3 coordinate mapping changed");
    assert(alt1205t_label_upper_left_hole_diameter() == 3.4 && alt1205t_label_upper_left_hole_centre() == [3.15, 6.6], "ALT-1205T label upper-left hole mapping changed");
    assert(alt1205t_label_second_m3_centre() == [8.5, 19.61], "ALT-1205T label second M3 coordinate mapping changed");
    assert(alt1205t_label_top_right_slot_height() == 6.9 && !alt1205t_label_top_right_slot_horizontal_depth_known(), "ALT-1205T label top-right slot has known height but unknown horizontal depth");
    assert(alt1205t_label_lower_right_hole_diameter() == 4, "ALT-1205T label lower-right hole diameter changed");
    assert(alt1205t_label_lower_right_hole_centre() == [98.84, 24.54], "ALT-1205T corrected lower-right offsets changed");
    assert(alt1205t_lower_left_unresolved_leaders() == [5.75, 4, 10.4, 2.28, 2.61], "ALT-1205T unresolved lower-left evidence values changed");
    assert(len(alt1205t_m3_centres()) == 3, "ALT-1205T coupon pattern must contain exactly three unequivocal M3 holes");
    assert(!alt1205t_upper_right_square_is_hole(), "ALT-1205T upper-right square is explicitly not a hole");
    children();
}

module alt1205t_oblong_negative(size, depth) {
    hull()
        for (y = [size.x / 2, size.y - size.x / 2])
            translate([size.x / 2, y, -0.01])
                cylinder(d = size.x, h = depth + 0.02, $fn = 32);
}

// Independently callable negative used by the later fit coupon.
module alt1205t_mounting_negatives(depth = 3, clearance_diameter = 3.4) {
    alt1205t_contract() {
        for (centre = alt1205t_m3_centres())
            translate([centre.x, centre.y, -0.01])
                cylinder(d = clearance_diameter, h = depth + 0.02, $fn = 36);

        translate([0, 0, 0])
            cube([alt1205t_upper_left_aperture_size().x,
                  alt1205t_upper_left_aperture_size().y, depth]);

        slot = alt1205t_upper_right_slot_size();
        translate([alt1205t_base_size().x - alt1205t_upper_right_slot_right_tangent() - slot.x,
                   alt1205t_upper_right_slot_top_tangent(), 0])
            alt1205t_oblong_negative(slot, depth);
    }
}

// Conservative solid keep-out: measured metal envelope only. Terminal/wire
// projection is intentionally excluded because no trustworthy envelope exists.
module alt1205t_keepout() {
    alt1205t_contract()
        cube([alt1205t_base_size().x, alt1205t_base_size().y,
              alt1205t_label_side_size().y]);
}

module alt1205t_evidence(view = "underside") {
    alt1205t_contract() {
        if (view == "underside") {
            color([0.68, 0.70, 0.72])
                difference() {
                    cube([alt1205t_base_size().x, alt1205t_base_size().y, 1.2]);
                    alt1205t_mounting_negatives(1.2);
                }
            // Ambiguous lower-left leaders: evidence marker, never a hole.
            color([0.95, 0.55, 0.08, 0.75])
                translate([5, 104, 1.2]) cube([11, 4, 0.35]);
        } else if (view == "label_side") {
            color([0.68, 0.70, 0.72])
                linear_extrude(height = 1.2)
                    difference() {
                            square(alt1205t_label_side_size());
                            translate(alt1205t_label_upper_left_hole_centre())
                                circle(d = alt1205t_label_upper_left_hole_diameter(), $fn = 32);
                            translate(alt1205t_label_second_m3_centre()) circle(d = 3, $fn = 32);
                            translate(alt1205t_label_lower_right_hole_centre())
                                circle(d = alt1205t_label_lower_right_hole_diameter(), $fn = 32);
                    }
            // Only the 6.9 mm vertical extent is measured. This orange edge
            // marker is semantic evidence; unknown horizontal depth creates
            // no aperture or keep-out claim.
            color([0.95, 0.55, 0.08])
                translate([alt1205t_label_side_size().x - 0.35, 0, 1.2])
                    cube([0.35, alt1205t_label_top_right_slot_height(), 0.35]);
        } else if (view == "side") {
            color([0.68, 0.70, 0.72]) alt1205t_keepout();
        } else assert(false, str("Unknown ALT-1205T evidence view: ", view));
    }
}
