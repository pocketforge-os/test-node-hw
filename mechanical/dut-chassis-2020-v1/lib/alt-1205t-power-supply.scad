/*
 * Source-owned semantic model of the owner-measured ALT-1205T 12 V / 5 A PSU.
 *
 * Datum: underside top-left corner; +X right, +Y down, +Z toward the label
 * side.  Dimensions are physical millimetres.  See alt-1205t-power-supply.md
 * for private-evidence provenance and deliberately unresolved measurements.
 */

function alt1205t_base_size() = [77.5, 110];
function alt1205t_label_side_size() = [110, 36.86];
function alt1205t_m3_nominal_diameter() = 3;
// The first coupon established that the photographed corner feature is an M3
// mount. The second physical fit moved that first-fit centre -2.5 mm X/left
// and +2.5 mm Y/down in the fixed underside datum.
function alt1205t_first_fit_upper_left_m3_centre() = [3.45, 3.45];
function alt1205t_second_fit_upper_left_m3_correction() = [-2.5, 2.5];
function alt1205t_upper_left_m3_centre() = [0.95, 5.95];
function alt1205t_upper_right_slot_size() = [3.3, 4.7];
function alt1205t_upper_right_slot_top_tangent() = 2.94;
function alt1205t_upper_right_slot_right_tangent() = 3.15;
function alt1205t_first_fit_m3_centres() =
    [[26.8, 32.9], [26.8, 69], [54.8, 69]];
function alt1205t_second_fit_internal_m3_correction() = [-1.5, -2];
function alt1205t_m3_centres() =
    [[25.3, 30.9], [25.3, 67], [53.3, 67]];
function alt1205t_lower_left_m3_left_tangent() = 5.75;
function alt1205t_lower_left_m3_bottom_centre_datum() = 10.4;
function alt1205t_first_fit_lower_left_m3_centre() = [
    alt1205t_lower_left_m3_left_tangent() +
        alt1205t_m3_nominal_diameter() / 2,
    alt1205t_base_size().y - alt1205t_lower_left_m3_bottom_centre_datum()
];
function alt1205t_second_fit_lower_left_m3_correction() = [-1.5, -2];
function alt1205t_lower_left_m3_centre() = [5.75, 97.6];
function alt1205t_all_m3_centres() = concat(
    [alt1205t_upper_left_m3_centre()],
    alt1205t_m3_centres(),
    [alt1205t_lower_left_m3_centre()]
);
function alt1205t_bottom_slot_left_tangent() = 2.28;
function alt1205t_bottom_slot_size() = [2.61, 4];
function alt1205t_bottom_slot_origin() = [
    alt1205t_bottom_slot_left_tangent(),
    alt1205t_base_size().y - alt1205t_bottom_slot_size().y
];
function alt1205t_label_upper_left_hole_diameter() = 3.4;
function alt1205t_label_upper_left_hole_centre() = [3.15, 6.6];
function alt1205t_label_second_m3_centre() = [8.5, 36.86 - 17.25];
function alt1205t_label_top_right_slot_height() = 6.9;
function alt1205t_label_top_right_slot_horizontal_depth_known() = false;
function alt1205t_label_lower_right_hole_diameter() = 4;
function alt1205t_label_lower_right_hole_centre() = [110 - 11.16, 36.86 - 12.32];
function alt1205t_upper_right_square_is_hole() = false;

module alt1205t_contract() {
    assert(alt1205t_base_size() == [77.5, 110], "ALT-1205T base datum changed");
    assert(alt1205t_label_side_size() == [110, 36.86], "ALT-1205T corrected label height changed");
    assert(alt1205t_m3_nominal_diameter() == 3 &&
           alt1205t_first_fit_upper_left_m3_centre() == [3.45, 3.45] &&
           alt1205t_second_fit_upper_left_m3_correction() == [-2.5, 2.5] &&
           norm(alt1205t_first_fit_upper_left_m3_centre() +
                alt1205t_second_fit_upper_left_m3_correction() - [0.95, 5.95]) < 0.000001 &&
           alt1205t_upper_left_m3_centre() == [0.95, 5.95],
           "ALT-1205T upper-left M3 centre datum changed");
    assert(alt1205t_upper_right_slot_size() == [3.3, 4.7] && alt1205t_upper_right_slot_top_tangent() == 2.94 && alt1205t_upper_right_slot_right_tangent() == 3.15, "ALT-1205T underside upper-right slot mapping changed");
    assert(alt1205t_first_fit_m3_centres() ==
               [[26.8, 32.9], [26.8, 69], [54.8, 69]] &&
           alt1205t_second_fit_internal_m3_correction() == [-1.5, -2] &&
           max([for (i = [0:2])
               norm(alt1205t_first_fit_m3_centres()[i] +
                    alt1205t_second_fit_internal_m3_correction() -
                    alt1205t_m3_centres()[i])]) < 0.000001 &&
           alt1205t_m3_centres() ==
               [[25.3, 30.9], [25.3, 67], [53.3, 67]],
           "ALT-1205T second-fit internal M3 coordinates changed");
    assert(alt1205t_lower_left_m3_left_tangent() == 5.75 &&
           alt1205t_lower_left_m3_bottom_centre_datum() == 10.4 &&
           alt1205t_first_fit_lower_left_m3_centre() == [7.25, 99.6] &&
           alt1205t_second_fit_lower_left_m3_correction() == [-1.5, -2] &&
           norm(alt1205t_first_fit_lower_left_m3_centre() +
                alt1205t_second_fit_lower_left_m3_correction() - [5.75, 97.6]) < 0.000001 &&
           alt1205t_lower_left_m3_centre() == [5.75, 97.6],
           "ALT-1205T second-fit lower-left M3 centre changed");
    assert(alt1205t_bottom_slot_left_tangent() == 2.28 &&
           alt1205t_bottom_slot_size() == [2.61, 4] &&
           alt1205t_bottom_slot_origin() == [2.28, 106],
           "ALT-1205T lower-left bottom-open slot changed");
    assert(alt1205t_label_upper_left_hole_diameter() == 3.4 && alt1205t_label_upper_left_hole_centre() == [3.15, 6.6], "ALT-1205T label upper-left hole mapping changed");
    assert(alt1205t_label_second_m3_centre() == [8.5, 19.61], "ALT-1205T label second M3 coordinate mapping changed");
    assert(alt1205t_label_top_right_slot_height() == 6.9 && !alt1205t_label_top_right_slot_horizontal_depth_known(), "ALT-1205T label top-right slot has known height but unknown horizontal depth");
    assert(alt1205t_label_lower_right_hole_diameter() == 4, "ALT-1205T label lower-right hole diameter changed");
    assert(alt1205t_label_lower_right_hole_centre() == [98.84, 24.54], "ALT-1205T corrected lower-right offsets changed");
    assert(len(alt1205t_m3_centres()) == 3 &&
           len(alt1205t_all_m3_centres()) == 5,
           "ALT-1205T coupon pattern must contain three internal and five total M3 checks");
    assert(!alt1205t_upper_right_square_is_hole(), "ALT-1205T upper-right square is explicitly not a hole");
    children();
}

module alt1205t_oblong_negative(size, depth) {
    hull()
        for (y = [size.x / 2, size.y - size.x / 2])
            translate([size.x / 2, y, -0.01])
                cylinder(d = size.x, h = depth + 0.02, $fn = 32);
}

// The photographed 2.61 x 4 mm slot has a round closed end and opens through
// the PSU's bottom edge. `outside_extension` lets a larger coupon outline keep
// that opening genuinely open instead of accidentally closing it with its
// registration margin.
module alt1205t_bottom_open_slot_2d(outside_extension = 0.02) {
    assert(outside_extension >= 0,
           "ALT-1205T bottom-slot extension cannot be negative");
    slot = alt1205t_bottom_slot_size();
    origin = alt1205t_bottom_slot_origin();
    radius = slot.x / 2;
    union() {
        translate([origin.x + radius, origin.y + radius])
            circle(d = slot.x, $fn = 32);
        translate([origin.x, origin.y + radius])
            square([slot.x, slot.y - radius + outside_extension]);
    }
}

module alt1205t_bottom_open_slot_negative(
    depth = 3, outside_extension = 0.02
) {
    translate([0, 0, -0.01])
        linear_extrude(height = depth + 0.02)
            alt1205t_bottom_open_slot_2d(outside_extension);
}

// Independently callable negative used by the later fit coupon.
module alt1205t_mounting_negatives(
    depth = 3, clearance_diameter = 3.4,
    bottom_slot_outside_extension = 0.02
) {
    alt1205t_contract() {
        for (centre = alt1205t_all_m3_centres())
            translate([centre.x, centre.y, -0.01])
                cylinder(d = clearance_diameter, h = depth + 0.02, $fn = 36);

        slot = alt1205t_upper_right_slot_size();
        translate([alt1205t_base_size().x - alt1205t_upper_right_slot_right_tangent() - slot.x,
                   alt1205t_upper_right_slot_top_tangent(), 0])
            alt1205t_oblong_negative(slot, depth);

        alt1205t_bottom_open_slot_negative(
            depth, bottom_slot_outside_extension);
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
            // Orange rings identify the two newly resolved edge M3 checks.
            for (centre = [alt1205t_upper_left_m3_centre(),
                           alt1205t_lower_left_m3_centre()])
                color([0.95, 0.55, 0.08, 0.85])
                    translate([centre.x, centre.y, 1.2])
                        linear_extrude(height = 0.35)
                            difference() {
                                circle(d = 4.5, $fn = 36);
                                circle(d = 3.4, $fn = 36);
                            }
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
