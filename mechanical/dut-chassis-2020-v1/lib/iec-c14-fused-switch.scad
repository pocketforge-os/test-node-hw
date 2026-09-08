/* Owner-measured fused switched IEC C14 inlet; dimensions in millimetres. */

function iecc14_faceplate_size() = [31, 50.3, 2];
function iecc14_body_profile_size() = [27, 46.86];
function iecc14_body_depth() = 21.8;
function iecc14_top_straight_length() = 16;
function iecc14_chamfer_edge_length() = 8;
function iecc14_chamfer_rise() = sqrt(pow(iecc14_chamfer_edge_length(), 2) - pow((iecc14_body_profile_size().x - iecc14_top_straight_length()) / 2, 2));
function iecc14_tab_widths() = [8, 5.5];
function iecc14_tab_height() = 5;
function iecc14_tab_top_setback() = 10.5;
function iecc14_tab_relief() = 1;
function iecc14_tab_lateral_inset() = 4.5;
// Provisional modeling assumption: the owner evidence establishes outward
// projection, but not its dimension. Replace this when it is measured.
function iecc14_unmeasured_resting_tab_projection_assumption() = 0.6;
function iecc14_tab_body_overlap() = 0.01;
function iecc14_tab_wall_x() = iecc14_body_profile_size().x / 2;
function iecc14_tab_y(side, width) = side == "left"
    ? -iecc14_body_profile_size().y / 2 + iecc14_tab_lateral_inset()
    : iecc14_body_profile_size().y / 2 - iecc14_tab_lateral_inset() - width;
function iecc14_tab_bounds(side, width) = [
    iecc14_tab_y(side, width), iecc14_tab_y(side, width) + width,
    iecc14_tab_top_setback(), iecc14_tab_top_setback() + iecc14_tab_height()
];
function iecc14_terminal_projection_known() = false;

module iecc14_contract() {
    assert(iecc14_faceplate_size() == [31, 50.3, 2], "IEC corrected faceplate envelope changed");
    assert(iecc14_body_profile_size() == [27, 46.86],
           "IEC physical-fit-corrected rigid body profile changed");
    assert(iecc14_body_depth() == 21.8, "IEC corrected plastic-body depth changed");
    assert(iecc14_tab_height() == 5, "IEC tab height is 5 mm, never the rejected 4.5 mm interpretation");
    assert(iecc14_tab_widths() == [8, 5.5],
           "IEC tab widths must remain on the 46.86 mm side-profile axis");
    assert(iecc14_tab_bounds("left", iecc14_tab_widths().x) == [-18.93, -10.93, 10.5, 15.5] &&
           iecc14_tab_bounds("right", iecc14_tab_widths().y) == [13.43, 18.93, 10.5, 15.5],
           "IEC tab bounds must preserve width, height, setback, and 4.5 mm outer edge insets");
    assert(iecc14_tab_wall_x() == 13.5,
           "Both IEC locking tabs must occupy the same photographed broad side wall");
    assert(iecc14_tab_relief() == 1 && iecc14_tab_top_setback() == 10.5,
           "IEC three-sided relief or top setback changed");
    assert(iecc14_unmeasured_resting_tab_projection_assumption() == 0.6,
           "IEC unmeasured resting tongue projection assumption changed");
    assert(iecc14_tab_body_overlap() > 0,
           "IEC tongue must overlap its parent wall for a manifold union");
    assert(abs(sqrt(pow((iecc14_body_profile_size().x - iecc14_top_straight_length()) / 2, 2) + pow(iecc14_chamfer_rise(), 2)) - 8) < 0.001,
           "IEC literal diagonal chamfer edges must remain 8 mm");
    assert(!iecc14_terminal_projection_known(), "IEC terminal projection remains unmeasured");
    children();
}

module iecc14_panel_profile_2d(clearance = 0) {
    assert(clearance >= 0, "IEC panel clearance cannot be negative");
    w = iecc14_body_profile_size().x;
    h = iecc14_body_profile_size().y;
    rise = iecc14_chamfer_rise();
    // Offset the whole nominal contour, rather than growing its bounding box:
    // this keeps clearance normal to the two diagonal edges as well as to the
    // horizontal and vertical edges. The zero-clearance polygon remains the
    // literal owner-measured 27 x 46.86 profile with 8 mm diagonals.
    offset(delta=clearance)
        polygon([[-w/2, -h/2], [w/2, -h/2], [w/2, h/2-rise],
                 [iecc14_top_straight_length()/2, h/2],
                 [-iecc14_top_straight_length()/2, h/2], [-w/2, h/2-rise]]);
}

// Independently callable panel negative, front face at Z=0 and body behind +Z.
module iecc14_panel_cutout_negative(depth = 24, clearance = 0) {
    iecc14_contract()
        iecc14_rigid_insertion_body_keepout(depth + 0.02, clearance, -0.01);
}

// Rigid/compressed insertion contract. This nominal 27 x 46.86 profile is the
// sole source for panel cutouts and insertion paths; relaxed tongues are absent.
module iecc14_rigid_insertion_body_keepout(
    depth = iecc14_body_depth(), clearance = 0, z_offset = 0
) {
    translate([0, 0, z_offset])
        linear_extrude(height = depth) iecc14_panel_profile_2d(clearance);
}

module iecc14_locking_tab(side = "left", width = 8) {
    assert(side == "left" || side == "right", "IEC tab side must be left or right");
    assert(width == 8 || width == 5.5, "IEC tab side-profile width changed");
    bounds = iecc14_tab_bounds(side, width);
    // Thin tongue remains connected at its bottom; the surrounding 1 mm gap
    // is represented in evidence by the contrasting parent side wall.
    projection = iecc14_unmeasured_resting_tab_projection_assumption();
    overlap = iecc14_tab_body_overlap();
    translate([iecc14_tab_wall_x() - overlap, bounds.x, bounds.z])
        cube([projection + overlap, bounds.y - bounds.x, bounds[3] - bounds.z]);
}

module iecc14_tab_relief_negatives(side = "left", width = 8) {
    bounds = iecc14_tab_bounds(side, width);
    cut_x = iecc14_tab_wall_x() - 1.19;
    // Side-profile relief: the top cut is toward the front face; the two
    // lateral cuts stop exactly at the tongue bottom so its full lower edge
    // remains joined to the photographed wall.
    translate([cut_x, bounds.x - iecc14_tab_relief(),
               bounds.z - iecc14_tab_relief()])
        cube([1.2, width + 2 * iecc14_tab_relief(), iecc14_tab_relief()]);
    for (y = [bounds.x - iecc14_tab_relief(), bounds.y])
        translate([cut_x, y, bounds.z - iecc14_tab_relief()])
            cube([1.2, iecc14_tab_relief(),
                  iecc14_tab_height() + iecc14_tab_relief()]);
}

// Presentation-only overlays make all three relieved edges distinguishable
// from the dark wall. Their dimensions derive from the actual negative; the
// unmarked bottom edge remains visibly attached.
module iecc14_tab_relief_evidence(side = "left", width = 8) {
    bounds = iecc14_tab_bounds(side, width);
    x = iecc14_tab_wall_x() + 0.61;
    color([1.0, 0.78, 0.18]) {
        translate([x, bounds.x - iecc14_tab_relief(), bounds.z - iecc14_tab_relief()])
            cube([0.05, width + 2 * iecc14_tab_relief(), iecc14_tab_relief()]);
        for (y = [bounds.x - iecc14_tab_relief(), bounds.y])
            translate([x, y, bounds.z])
                cube([0.05, iecc14_tab_relief(), iecc14_tab_height()]);
    }
}

// Complete relaxed/rest-state component contract for enclosure clearances.
module iecc14_complete_rest_state_keepout(include_schematic_terminals = false) {
    iecc14_contract() {
        union() {
            translate([-iecc14_faceplate_size().x/2, -iecc14_faceplate_size().y/2,
                       -iecc14_faceplate_size().z])
                cube(iecc14_faceplate_size());
            difference() {
                iecc14_rigid_insertion_body_keepout();
                iecc14_tab_relief_negatives("left", iecc14_tab_widths().x);
                iecc14_tab_relief_negatives("right", iecc14_tab_widths().y);
            }
            iecc14_locking_tab("left", iecc14_tab_widths().x);
            iecc14_locking_tab("right", iecc14_tab_widths().y);
            if (include_schematic_terminals)
                // Schematic only: not part of the measured keep-out contract.
                color([0.85, 0.55, 0.12]) translate([-7, -8, iecc14_body_depth()])
                    cube([14, 16, 3]);
        }
    }
}

// Stable downstream default: a complete physical envelope at rest.
module iecc14_keepout(include_schematic_terminals = false) {
    iecc14_complete_rest_state_keepout(include_schematic_terminals);
}

module iecc14_evidence(view = "front") {
    iecc14_contract() {
        if (view == "front") {
            color([0.12, 0.13, 0.14])
                difference() {
                    translate([-31/2, -50.3/2, -2]) cube(iecc14_faceplate_size());
                    translate([0, 0, -2.01]) linear_extrude(height = 2.02)
                        iecc14_panel_profile_2d();
                }
            color([0.25, 0.27, 0.29]) linear_extrude(height = 0.4) iecc14_panel_profile_2d();
        } else if (view == "side") {
            color([0.12, 0.13, 0.14]) iecc14_keepout();
            // Semantic overlay identifies tongues already present in the
            // printable/exported complete rest-state keep-out.
            color([0.90, 0.42, 0.10]) {
                iecc14_locking_tab("left", 8);
                iecc14_locking_tab("right", 5.5);
            }
            iecc14_tab_relief_evidence("left", 8);
            iecc14_tab_relief_evidence("right", 5.5);
        } else if (view == "rear") {
            color([0.12, 0.13, 0.14])
                linear_extrude(height = 0.8) iecc14_panel_profile_2d();
            // Orange rectangle is explicitly schematic, not a terminal
            // projection measurement or a keep-out claim.
            color([0.85, 0.55, 0.12])
                translate([-7, -8, 0.8]) cube([14, 16, 0.8]);
        } else assert(false, str("Unknown IEC C14 evidence view: ", view));
    }
}
