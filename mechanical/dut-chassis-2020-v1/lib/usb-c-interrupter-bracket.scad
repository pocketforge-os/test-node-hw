/*
 * Candidate rail bracket for the owner's USB-C interrupter.
 *
 * Local coordinates are the print coordinates and intentionally match the
 * exported STL: X follows the 20.09 mm face, Y points from the interrupter up
 * toward the rail, and Z grows from the bed/rail-contact plane toward the
 * operator. Print this broad rail-contact face down, with supports disabled.
 *
 * This is a source-only physical-fit candidate. The photographed face was
 * measured as 20.09 x 6.59 mm with two nominal 2 mm holes on 16 mm centres.
 * The separately measured 2.23 / 2.54 mm long-edge margins sum to 6.77 mm
 * after including the 2 mm hole, so the candidate centres the hole row on the
 * 6.59 mm face. The 2 mm face holes retain 0.15 mm radial freedom around an
 * M1.7 screw for that measurement uncertainty.
 */

function usbci_face_size() = [20.09, 6.59];
function usbci_face_hole_diameter() = 2.0;
function usbci_face_hole_spacing() = 16.0;
function usbci_face_hole_centres() = [-8.0, 8.0];
function usbci_rear_board_depth() = 12.0;
function usbci_connector_depth() = 6.0;

function usbci_m17_pilot_diameter() = 1.35;
function usbci_m17_pilot_depth() = 5.0;
function usbci_m17_pilot_entry_diameter() = 2.0;
function usbci_m17_pilot_entry_depth() = 0.6;
function usbci_m3_clearance() = 3.6;
function usbci_m3_hole_centres() = [-7.0, 7.0];

function usbci_mount_pad_size() = [24.8, 20.0, 4.0];
function usbci_mount_pad_centre_y() = 18.0;
function usbci_retention_depth() = 5.6;
function usbci_retention_floor() =
    usbci_retention_depth() - usbci_m17_pilot_depth();
function usbci_retention_inner_x() = 6.5;
function usbci_retention_outer_x() = 11.5;
function usbci_retention_bottom_y() = -2.8;
function usbci_retention_top_y() = 10.0;
function usbci_rear_board_opening_width() =
    2 * usbci_retention_inner_x();
function usbci_print_size() = [
    usbci_mount_pad_size().x,
    usbci_mount_pad_centre_y() + usbci_mount_pad_size().y / 2 -
        usbci_retention_bottom_y(),
    usbci_retention_depth()
];

module usbci_rounded_rect_2d(size, radius) {
    assert(size.x > 2 * radius && size.y > 2 * radius,
           "USB-C interrupter rounded rectangle needs positive core size");
    offset(r = radius)
        square([size.x - 2 * radius, size.y - 2 * radius],
               center = true);
}

module usbci_mount_pad() {
    translate([0, usbci_mount_pad_centre_y(), 0])
        linear_extrude(height = usbci_mount_pad_size().z)
            usbci_rounded_rect_2d(
                [usbci_mount_pad_size().x, usbci_mount_pad_size().y],
                2.0);
}

module usbci_retention_leg(right = false) {
    inner_x = usbci_retention_inner_x();
    outer_x = usbci_retention_outer_x();
    leg_size = [outer_x - inner_x,
                usbci_retention_top_y() - usbci_retention_bottom_y()];
    leg_centre = [(inner_x + outer_x) / 2,
                  (usbci_retention_bottom_y() +
                   usbci_retention_top_y()) / 2];

    translate([right ? leg_centre.x : -leg_centre.x,
               leg_centre.y, 0])
        linear_extrude(height = usbci_retention_depth())
            usbci_rounded_rect_2d(leg_size, 1.2);
}

module usbci_m17_blind_pilot(x, pilot_diameter) {
    pilot_start_z = usbci_retention_floor();
    entry_start_z = usbci_retention_depth() -
                    usbci_m17_pilot_entry_depth();

    translate([x, 0, pilot_start_z])
        cylinder(d = pilot_diameter,
                 h = usbci_m17_pilot_depth() + 0.02, $fn = 32);
    translate([x, 0, entry_start_z])
        cylinder(d1 = pilot_diameter,
                 d2 = usbci_m17_pilot_entry_diameter(),
                 h = usbci_m17_pilot_entry_depth() + 0.02, $fn = 32);
}

module usb_c_interrupter_bracket(
    pilot_diameter = usbci_m17_pilot_diameter()
) {
    assert(abs(usbci_face_hole_centres().y -
               usbci_face_hole_centres().x) ==
               usbci_face_hole_spacing(),
           "USB-C interrupter retention holes must remain on 16 mm centres");
    assert(usbci_face_size().x / 2 -
               usbci_face_hole_spacing() / 2 -
               usbci_face_hole_diameter() / 2 >= 1.0,
           "USB-C interrupter face needs at least 1 mm beyond each hole");
    assert(pilot_diameter < 1.7 && pilot_diameter >= 1.2,
           "M1.7 self-tapper pilot must remain a conservative starter hole");
    assert(usbci_retention_floor() >= 0.6 - 0.001,
           "M1.7 blind pilots need a 0.6 mm closed floor");
    assert(usbci_rear_board_opening_width() >= 13.0,
           "Rear PCB opening needs 0.5 mm per side around the 12 mm board");
    assert(usbci_mount_pad_size().y == 20.0,
           "Rail pad must span the full 20 mm extrusion face");

    difference() {
        union() {
            usbci_mount_pad();
            usbci_retention_leg(false);
            usbci_retention_leg(true);
        }

        for (x = usbci_m3_hole_centres())
            translate([x, usbci_mount_pad_centre_y(), -0.02])
                cylinder(d = usbci_m3_clearance(),
                         h = usbci_mount_pad_size().z + 0.04, $fn = 36);

        for (x = usbci_face_hole_centres())
            usbci_m17_blind_pilot(x, pilot_diameter);
    }
}

// Conservative visual proxy only. The centre board uses the supplied 12 mm
// dimension both for face-parallel width and rearward depth so the installed
// scene proves the bracket's narrowest central opening. It is never exported
// in the printable STL.
module usb_c_interrupter_proxy() {
    face_thickness = 1.0;
    board_thickness = 1.6;
    board_width = 12.0;
    connector_face = [9.0, 3.4];

    color([0.10, 0.12, 0.13])
        difference() {
            translate([0, 0,
                       usbci_retention_depth() + face_thickness / 2])
                cube([usbci_face_size().x, usbci_face_size().y,
                      face_thickness], center = true);
            for (x = usbci_face_hole_centres())
                translate([x, 0, usbci_retention_depth() - 0.02])
                    cylinder(d = usbci_face_hole_diameter(),
                             h = face_thickness + 0.04, $fn = 32);
        }

    color([0.08, 0.42, 0.22])
        translate([0, 0,
                   usbci_retention_depth() -
                   usbci_rear_board_depth() / 2])
            cube([board_width, board_thickness,
                  usbci_rear_board_depth()], center = true);

    color([0.64, 0.67, 0.68])
        translate([0, 0,
                   usbci_retention_depth() -
                   usbci_connector_depth() / 2])
            cube([connector_face.x, connector_face.y,
                  usbci_connector_depth()], center = true);
    color([0.015, 0.018, 0.020])
        translate([0, 0, usbci_retention_depth() + face_thickness + 0.25])
            linear_extrude(height = 0.5)
                usbci_rounded_rect_2d(connector_face, 1.5);
}
