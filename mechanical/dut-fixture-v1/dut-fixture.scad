/*
 * PocketForge DUT fixture plate v1
 *
 * Source measurements: owner caliper notes photographed 2026-07-18.
 * Coordinate system: X left-to-right, Y front-to-back, Z upward; millimetres.
 *
 * Export with, for example:
 *   openscad -o fixture.stl -D 'PART="plate"' dut-fixture.scad
 *
 * PART choices: preview, plate, presentation_relay, presentation_bpi,
 * presentation_boost, presentation_mosfet, presentation_dp100,
 * presentation_esp32,
 * presentation_c270,
 * presentation_antenna, presentation_powered_hub,
 * presentation_unpowered_hub,
 * presentation_components,
 * presentation_antenna_dark, presentation_antenna_metal,
 * presentation_antenna_markings,
 * presentation_vienon_shell, presentation_vienon_dark,
 * presentation_vienon_metal, presentation_vienon_blue,
 * presentation_vienon_led,
 * presentation_smays_shell, presentation_smays_dark,
 * presentation_smays_metal, presentation_smays_led,
 * presentation_smays_markings,
 * presentation_boost_pcb, presentation_boost_dark,
 * presentation_boost_adjuster, presentation_boost_metal,
 * presentation_boost_silkscreen,
 * presentation_mosfet_pcb, presentation_mosfet_blue,
 * presentation_mosfet_dark, presentation_mosfet_metal,
 * presentation_mosfet_led, presentation_mosfet_silkscreen,
 * presentation_dp100_shell, presentation_dp100_dark,
 * presentation_dp100_controls,
 * presentation_dp100_screen, presentation_dp100_accent,
 * presentation_dp100_metal, presentation_dp100_markings,
 * presentation_relay_pcb, presentation_relay_blue,
 * presentation_relay_dark, presentation_relay_metal,
 * presentation_relay_led, presentation_relay_silkscreen,
 * presentation_bpi_pcb, presentation_bpi_dark,
 * presentation_bpi_metal, presentation_bpi_gold,
 * presentation_bpi_silkscreen, presentation_esp32_pcb,
 * presentation_esp32_dark, presentation_esp32_metal,
 * presentation_esp32_gold, presentation_esp32_antenna,
 * presentation_esp32_silkscreen, presentation_c270_shell,
 * presentation_c270_dark, presentation_c270_glass,
 * presentation_c270_led, presentation_c270_labels,
 * presentation_labels, fit_coupon, plate_lower, plate_upper, joiner.
 */

use <bpi-m2-zero-v1.scad>;
use <elegoo-4-channel-relay.scad>;
use <esp32-s3-supermini-hw747-v0.0.2.scad>;
use <hiletgo-xl6009.scad>;
use <ceksezx-mtsd001.scad>;
use <alientek-dp100.scad>;
use <logitech-c270.scad>;
use <eightwood-ewua0205.scad>;
use <vienon-usb-001.scad>;
use <smays-microb-hub-8152.scad>;

PART = "preview";
SHOW_COMPONENTS = true;
SHOW_LABELS = true;

$fn = 48;
epsilon = 0.05;

// ---- Printer / plate -------------------------------------------------------
printer_bed = [250, 210];             // Prusa i3 MK3S advertised build area
printer_edge_margin = 1.5;            // proven necessary by physical slicer/bed fit
printable_bed = printer_bed - [2 * printer_edge_margin,
                               2 * printer_edge_margin];
plate_size = [200, 247];              // rotate 90°; retains 1.5 mm on every bed edge
plate_thickness = 3.2;
plate_corner_radius = 4;
// Eight frame anchors: one slot toward each adjacent rail at every corner.
// 12 x 5.5 mm accepts a common 4.8 mm heavy-duty tie with print clearance.
frame_tie_slot = [12.0, 5.5];
frame_tie_edge_inset = 8.0;
frame_tie_corner_offset = 19.0;
frame_tie_features = [
    ["frame_bottom_left_bottom", [frame_tie_corner_offset, frame_tie_edge_inset], 0],
    ["frame_bottom_left_left", [frame_tie_edge_inset, frame_tie_corner_offset], 90],
    ["frame_bottom_right_bottom",
     [plate_size.x - frame_tie_corner_offset, frame_tie_edge_inset], 0],
    ["frame_bottom_right_right",
     [plate_size.x - frame_tie_edge_inset, frame_tie_corner_offset], 90],
    ["frame_top_left_top",
     [frame_tie_corner_offset, plate_size.y - frame_tie_edge_inset], 0],
    ["frame_top_left_left",
     [frame_tie_edge_inset, plate_size.y - frame_tie_corner_offset], 90],
    ["frame_top_right_top",
     [plate_size.x - frame_tie_corner_offset, plate_size.y - frame_tie_edge_inset], 0],
    ["frame_top_right_right",
     [plate_size.x - frame_tie_edge_inset, plate_size.y - frame_tie_corner_offset], 90]
];

// Optional horizontal split follows the empty corridor below the top row.
// Three below-plate joiners bridge the seam without crossing a component.
split_y = 150.0;
joiner_centres_x = [7.0, 139.0, 192.0];
joiner_hole_y = [split_y - 6, split_y + 5];
joiner_hole_diameter = 3.4;            // M3 clearance
joiner_head_diameter = 6.0;            // keep-out for a typical M3 pan head

// ---- Printed fastener interfaces ------------------------------------------
standoff_outer_diameter = 7.0;
standoff_height = 6.0;
relay_standoff_outer_diameter = 9.0;  // wider base for the tall relay towers
relay_standoff_height = standoff_height + 20.0;
m25_pilot_diameter = 2.2;              // tune after printing fit_coupon
m2_pilot_diameter = 1.7;               // tune after printing fit_coupon
zip_slot = [7.0, 2.2];                 // common 2.0 mm-wide cable tie
zip_edge_gap = 2.0;

// ---- Component envelopes and measured interfaces --------------------------
// Hole spacing in the notes was measured far outside-edge to far outside-edge.
// Therefore centre spacing = noted spacing - hole diameter.

// Layout is organized around a central webcam, accessible hub ends, a clear
// 4040-frame perimeter, and compact functional groups.
relay_origin = [20, 152.7];
relay_size = [51.85, 72.70];
relay_hole_diameter = 3.0;
relay_hole_far_spacing = [48.03, 69.93];
relay_hole_centres = relay_hole_far_spacing - [relay_hole_diameter, relay_hole_diameter];
RELAY_MODEL_SCALE = 1.0;
RELAY_MODEL_HOLE_CENTRES = relay_hole_centres;
RELAY_MODEL_TERMINAL_EDGE = "+X";

bpi_origin = [14, 84.6];
bpi_size = [29.90, 65.00];
bpi_hole_diameter = 2.6;
bpi_hole_far_spacing = [25.60, 60.96];
bpi_hole_centres = bpi_hole_far_spacing - [bpi_hole_diameter, bpi_hole_diameter];
BPI_MODEL_SCALE = 1.0;
BPI_MODEL_HOLE_CENTRES = bpi_hole_centres;

// The diagonal holes have a 5 mm horizontal gap from the hole edge to the
// adjacent short board side. The sketch also records 1.1 mm at the top hole
// and 0.7 mm at the bottom hole. Convert those edge gaps to centre coordinates
// by adding the 1.5 mm radius of each 3 mm hole.
boost_origin = [149, 96];
boost_size = [43.16, 21.23];
boost_hole_diameter = 3.0;
boost_hole_side_clearance = 5.0;
boost_hole_top_clearance = 1.1;
boost_hole_bottom_clearance = 0.7;
boost_hole_radius = boost_hole_diameter / 2;
boost_hole_side_centre_inset = boost_hole_side_clearance + boost_hole_radius;
boost_hole_centres = [
    [boost_hole_side_centre_inset,
     boost_size.y - boost_hole_top_clearance - boost_hole_radius],
    [boost_size.x - boost_hole_side_centre_inset,
     boost_hole_bottom_clearance + boost_hole_radius]
];
BOOST_MODEL_SCALE = 1.0;
BOOST_MODEL_HOLE_CENTRES = boost_hole_centres;
BOOST_MODEL_INPUT_EDGE = "-X";

// The original sketch measured the mounting interface but treated the board
// outline as provisional. The exact listing/owner-photo match is a 34 x 17 mm
// MTSD001 board centred within this 35 x 18 mm collision envelope. Its two
// clipped holes remain on the existing printed standoff centres.
mosfet_origin = [157, 122];
mosfet_size = [35.0, 18.0];             // accepted collision/standoff envelope
mosfet_hole_diameter = 2.2;
mosfet_hole_centre_spacing = 15.58 - mosfet_hole_diameter;
mosfet_hole_x = mosfet_size.x - (mosfet_hole_diameter / 2 + 0.1);
mosfet_hole_centres = [
    [mosfet_hole_x, (mosfet_size.y - mosfet_hole_centre_spacing) / 2],
    [mosfet_hole_x, (mosfet_size.y + mosfet_hole_centre_spacing) / 2]
];
MOSFET_MODEL_SCALE = 1.0;
MOSFET_MODEL_BOARD = [34.0, 17.0];
MOSFET_MODEL_HOLE_CENTRES = mosfet_hole_centres;
MOSFET_MODEL_TERMINAL_EDGE = "-X";

// Exact Eightwood EWUA0205 paddle. Centre the listing's 114 x 15 mm body on
// the accepted physical tie datums; only one of the retail pair is installed.
antenna_origin = [40, 228.5];
antenna_size = [114.0, 15.0];
// Keep the accepted printable slots bit-for-bit at the old 110 x 14.3 mm
// proxy datum while centring the longer exact paddle over the same tie axes.
antenna_tie_origin = [42, 228.5];
antenna_tie_size = [110.0, 14.3];
antenna_tie_x = [25, 85];
antenna_model_tie_x = [27, 87];
ANTENNA_MODEL_SCALE = 1.0;
ANTENNA_MODEL_PANEL = eightwood_ewua0205_panel_size();
ANTENNA_MODEL_CABLE_EDGE = "+X";
antenna_install_lift = 0.20;
// A 0.1 mm inset lets the slots meet the antenna edge while preserving both
// the relay clearance below and over 2 mm of material at the plate's top edge.
antenna_tie_edge_gap = -0.1;

esp32_origin = [8, 54.9];
// Oriented with the 18.5 mm short/USB-C edge facing the bottom of the plate.
esp32_size = [18.5, 23.67];               // owner-measured physical envelope
ESP32_MODEL_SCALE = 1.0;
ESP32_MODEL_ENVELOPE = esp32_size;
ESP32_MODEL_USB_EDGE = "bottom";
esp32_install_lift = 0.65;                 // clears photographed reverse SMDs
// Two compact slots flank the connector on each short edge. These are smaller
// than the general fixture slot so the USB-C corridor remains unobstructed.
esp32_tie_slot = [3.0, 3.0];
esp32_tie_x = [3.25, esp32_size.x - 3.25];
esp32_tie_service_clearance = 0.25;
esp32_usb_service_depth = 20.0;
esp32_usb_service_width = 8.5;             // centred USB-C receptacle/cable corridor
esp32_usb_service_origin = [esp32_origin.x +
                            (esp32_size.x - esp32_usb_service_width) / 2,
                            esp32_origin.y - esp32_usb_service_depth];
esp32_usb_service_size = [esp32_usb_service_width, esp32_usb_service_depth];

// Owner-corrected caliper measurement of this physical DP100 revision.
dp100_origin = [89.5, 162];
dp100_size = [94.6, 62.2];
DP100_MODEL_SCALE = 1.0;
DP100_MODEL_BODY = [dp100_size.x, dp100_size.y, 17.2];
DP100_MODEL_BANANA_EDGE = "-X";
DP100_MODEL_USB_EDGE = "+X";
DP100_MODEL_CONTROLS_EDGE = "-Y";
dp100_install_lift = 0.20;
dp100_banana_service_depth = 6.0;
dp100_usb_service_depth = 15.0;
dp100_banana_service_origin = [
    dp100_origin.x - alientek_dp100_banana_projection() -
    dp100_banana_service_depth,
    dp100_origin.y + 10.0
];
dp100_banana_service_size = [
    dp100_banana_service_depth,
    dp100_size.y - 20.0
];
dp100_usb_service_origin = [
    dp100_origin.x + dp100_size.x,
    dp100_origin.y + 12.0
];
dp100_usb_service_size = [
    dp100_usb_service_depth,
    14.0
];
dp100_usb_c_service_origin = [
    dp100_origin.x + dp100_size.x,
    dp100_origin.y + 41.8
];
dp100_usb_c_service_size = [
    dp100_usb_service_depth,
    10.4
];
// The owner sketch has exactly one slot on each short side. The vertical
// offsets are measured down from the top edge in that sketch.
dp100_tie_features = [
    ["dp100_left_tie",
     [dp100_origin.x - zip_edge_gap - zip_slot.y / 2,
      dp100_origin.y + dp100_size.y - 21.0], 90, "dp100"],
    ["dp100_right_tie",
     [dp100_origin.x + dp100_size.x + zip_edge_gap + zip_slot.y / 2,
      dp100_origin.y + dp100_size.y - 25.0], 90, "dp100"]
];

webcam_keepout = [71.0, 31.55];
webcam_aperture_minimum = [44.75, 19.5];  // owner-corrected after physical fit
webcam_aperture = webcam_aperture_minimum;
webcam_aperture_clearance = 0.40;         // total diametral/width clearance
webcam_aperture_radius = 5.0;
webcam_centre = [plate_size.x / 2, 132.0];
webcam_origin = webcam_centre - webcam_keepout / 2;
webcam_lens_datum = webcam_origin + c270_lens_centre_xy();
webcam_lens_plane_z = c270_lens_plane_z();
C270_MODEL_FACE = c270_installed_face_size();
C270_MODEL_LENS_DIRECTION = c270_lens_direction();
webcam_below_clearance = 20.0;
webcam_below_service_origin = [webcam_origin.x,
                               webcam_origin.y - webcam_below_clearance];
webcam_below_service_size = [webcam_keepout.x, webcam_below_clearance];

// Each hub exposes one connector-bearing long edge toward clear space. The
// powered hub gets a full in-plate cable bay; the lower hub opens off the edge.
powered_hub_long_side_service_depth = 25.0;
powered_hub_end_service_depth = 18.0;
unpowered_hub_long_side_service_depth = 20.0;
unpowered_hub_end_service_depth = 20.0;
hub_end_service_width = 12.0;
powered_hub_connector_side = "top";
unpowered_hub_connector_side = "bottom";
hub_tie_service_clearance = 1.0;
powered_hub_origin = [66.9, 41.0];
powered_hub_size = [105.07, 24.0];
powered_hub_tie_slot = [7.0, 2.7];
// Important measured offsets: 24 mm from one end, 39 mm from the other.
powered_hub_tie_x = [24.0, powered_hub_size.x - 39.0];
POWERED_HUB_MODEL_SCALE = 1.0;
POWERED_HUB_MODEL_BODY = smays_microb_hub_body_size();
POWERED_HUB_MODEL_USB_EDGE = "+Y";
POWERED_HUB_MODEL_RJ45_EDGE = "-X";
POWERED_HUB_MODEL_OTG_EDGE = "+X";
POWERED_HUB_MODEL_DC_EDGE = "-Y";
powered_hub_install_lift = 0.20;

// The installed Usb-001 body sits 20 mm left of its original tie-envelope
// datum so the two existing ties land near its middle and +X end, exactly as
// shown in the owner's fixture photo. Its Y position remains 2 mm toward the
// open plate edge. The production tie slots stay bit-for-bit unchanged.
unpowered_hub_origin = [43.25, 5.0];
unpowered_hub_size = [100.0, 30.0];
unpowered_hub_tie_origin = [63.25, 7.0];
unpowered_hub_tie_size = [105.0, 24.0];
unpowered_hub_tie_x = [25.0, 80.0];
unpowered_hub_model_tie_x = [45.0, 100.0];
UNPOWERED_HUB_MODEL_SCALE = 1.0;
UNPOWERED_HUB_MODEL_BODY = vienon_usb001_body_size();
UNPOWERED_HUB_MODEL_USB_EDGE = "-Y";
UNPOWERED_HUB_MODEL_UPSTREAM_EDGE = "+X";
unpowered_hub_install_lift = 0.20;

// The Smays DC plug exits into the six-millimetre inter-hub gap, then bends
// outward from the plate and crosses above the thinner VIENON hub. A flat 2D
// keep-out would reject the assembly that physically fits, so preserve the
// real three-dimensional service volume and its minimum Z clearance.
powered_hub_dc_service_origin = [
    powered_hub_origin.x + smays_microb_hub_dc_exit_x() - 7.0,
    powered_hub_origin.y - 14.0,
    plate_thickness + unpowered_hub_install_lift +
    UNPOWERED_HUB_MODEL_BODY.z + 0.5
];
powered_hub_dc_service_size = [20.0, 14.0, 7.5];

// ---- Basic geometry --------------------------------------------------------
module rounded_rect_2d(size, radius) {
    offset(r = radius)
        offset(delta = -radius)
            square(size);
}

module rounded_prism(size, radius) {
    linear_extrude(height = size.z)
        rounded_rect_2d([size.x, size.y], radius);
}

module pill_2d(length, width) {
    hull() {
        translate([-(length - width) / 2, 0]) circle(d = width);
        translate([ (length - width) / 2, 0]) circle(d = width);
    }
}

module through_hole(point, diameter, depth = plate_thickness + standoff_height + 2) {
    translate([point.x, point.y, -1]) cylinder(d = diameter, h = depth);
}

module tie_slot(point, rotation = 0, dimensions = zip_slot) {
    translate([point.x, point.y, -1])
        linear_extrude(height = plate_thickness + 2)
            rotate(rotation)
                pill_2d(dimensions.x, dimensions.y);
}

// Standoff and bore modules deliberately share the same short coordinate loop.
module four_standoffs(origin, envelope, spacing, pilot, height = standoff_height,
                      outer_diameter = standoff_outer_diameter) {
    margin = (envelope - spacing) / 2;
    for (dx = [margin.x, margin.x + spacing.x])
        for (dy = [margin.y, margin.y + spacing.y])
            translate([origin.x + dx, origin.y + dy, plate_thickness])
                cylinder(d = outer_diameter, h = height);
}

module four_standoff_bores(origin, envelope, spacing, pilot, height = standoff_height) {
    margin = (envelope - spacing) / 2;
    for (dx = [margin.x, margin.x + spacing.x])
        for (dy = [margin.y, margin.y + spacing.y])
            through_hole([origin.x + dx, origin.y + dy], pilot,
                         plate_thickness + height + 2);
}

module point_standoffs(origin, points, pilot, height = standoff_height) {
    for (point = points)
        translate([origin.x + point.x, origin.y + point.y, plate_thickness])
            cylinder(d = standoff_outer_diameter, h = height);
}

module point_standoff_bores(origin, points, pilot) {
    for (point = points)
        through_hole([origin.x + point.x, origin.y + point.y], pilot);
}

module transverse_tie_slots(origin, envelope, offsets_x, dimensions = zip_slot,
                            edge_gap = zip_edge_gap) {
    // A strap crosses the component's short (Y) axis; slots run along X.
    for (x = offsets_x)
        for (y = [-edge_gap - dimensions.y / 2,
                  envelope.y + edge_gap + dimensions.y / 2])
            tie_slot([origin.x + x, origin.y + y], 0, dimensions);
}

module lateral_tie_slots(origin, envelope, offsets_y) {
    // A strap crosses the component's short (X) axis; slots run along Y.
    for (y = offsets_y)
        for (x = [-zip_edge_gap - zip_slot.y / 2,
                  envelope.x + zip_edge_gap + zip_slot.y / 2])
            tie_slot([origin.x + x, origin.y + y], 90);
}

module plate_solid() {
    rounded_prism([plate_size.x, plate_size.y, plate_thickness], plate_corner_radius);
}

module fixture_standoffs() {
    four_standoffs(relay_origin, relay_size, relay_hole_centres, m25_pilot_diameter,
                   relay_standoff_height, relay_standoff_outer_diameter);
    four_standoffs(bpi_origin, bpi_size, bpi_hole_centres, m25_pilot_diameter);
    point_standoffs(boost_origin, boost_hole_centres, m25_pilot_diameter);
    point_standoffs(mosfet_origin, mosfet_hole_centres, m2_pilot_diameter);
}

module fixture_cutouts() {
    // Eight independent anchors tie the plate to both adjacent 4040 rails at
    // every corner. Orthogonal slots make the intended tie direction obvious.
    for (feature = frame_tie_features)
        tie_slot(feature[1], feature[2], frame_tie_slot);

    // Joiner holes belong only to the optional split exports. The one-piece
    // plate stays unperforated at the seam.
    if (PART == "plate_lower" || PART == "plate_upper")
        for (x = joiner_centres_x)
            for (y = joiner_hole_y)
                through_hole([x, y], joiner_hole_diameter);

    four_standoff_bores(relay_origin, relay_size, relay_hole_centres, m25_pilot_diameter,
                        relay_standoff_height);
    four_standoff_bores(bpi_origin, bpi_size, bpi_hole_centres, m25_pilot_diameter);
    point_standoff_bores(boost_origin, boost_hole_centres, m25_pilot_diameter);
    point_standoff_bores(mosfet_origin, mosfet_hole_centres, m2_pilot_diameter);

    for (feature = dp100_tie_features)
        tie_slot(feature[1], feature[2]);
    transverse_tie_slots(antenna_tie_origin, antenna_tie_size, antenna_tie_x,
                         zip_slot, antenna_tie_edge_gap);
    transverse_tie_slots(esp32_origin, esp32_size, esp32_tie_x,
                         esp32_tie_slot);
    transverse_tie_slots(powered_hub_origin, powered_hub_size, powered_hub_tie_x,
                         powered_hub_tie_slot);
    transverse_tie_slots(unpowered_hub_tie_origin,
                         unpowered_hub_tie_size,
                         unpowered_hub_tie_x);

    // Webcam is offered from below; only the smaller rear housing protrudes.
    opening = webcam_aperture + [webcam_aperture_clearance, webcam_aperture_clearance];
    opening_origin = webcam_origin + (webcam_keepout - opening) / 2;
    translate([opening_origin.x, opening_origin.y, -1])
        linear_extrude(height = plate_thickness + 2)
            rounded_rect_2d(opening, webcam_aperture_radius);

}

module fixture_plate() {
    difference() {
        union() {
            plate_solid();
            fixture_standoffs();
        }
        fixture_cutouts();
    }
}

// ---- Labels and preview-only component envelopes --------------------------
module preview_text(label, point, size = 3.2, rotation = 0) {
    color("SeaGreen", 0.8)
        translate([point.x, point.y, plate_thickness + 0.2])
        linear_extrude(height = 0.4)
            rotate(rotation)
                text(label, size = size, halign = "left", valign = "baseline",
                     font = "Liberation Sans:style=Bold");
}

module fixture_labels() {
    preview_text("RELAY", [20, 159]);
    preview_text("BPI M2 ZERO", [10, 108], 3.0, 90);
    preview_text("BOOST", [149, 91]);
    preview_text("MOSFET", [157, 117]);
    preview_text("ANT", [88, 236]);
    preview_text("ESP32", [8, 51.9]);
    preview_text("DP100", [126, 159]);
    preview_text("WEBCAM (UNDER)", [76, 149]);
    preview_text("POWERED HUB", [89, 48]);
    preview_text("USB HUB", [103, 14]);
}

module envelope(origin, size, height, colour, radius = 2, lift = standoff_height) {
    color(colour, 0.45)
        translate([origin.x, origin.y, plate_thickness + lift + 0.2])
            rounded_prism([size.x, size.y, height], min(radius, min(size.x, size.y) / 2));
}

module service_keepout_preview(origin, size, colour = "Crimson") {
    color(colour, 0.20)
        translate([origin.x, origin.y, plate_thickness + 0.1])
            rounded_prism([size.x, size.y, 0.8], 1.5);
}

module service_keepout_volume_preview(origin, size, colour = "DeepPink") {
    color(colour, 0.22)
        translate(origin)
            rounded_prism(size, min(1.5, min(size.x, size.y) / 2));
}

module bpi_model_at_fixture_datum() {
    translate([bpi_origin.x, bpi_origin.y,
               plate_thickness + standoff_height + 0.2])
        children();
}

module relay_model_at_fixture_datum() {
    translate([relay_origin.x, relay_origin.y,
               plate_thickness + relay_standoff_height + 0.2])
        // Native listing +Y is the terminal side. Rotate clockwise so that
        // edge becomes installed +X while retaining the measured envelope.
        translate([0, elegoo_relay_board_size().x, 0])
            rotate([0, 0, -90])
                children();
}

module relay_model_preview() {
    relay_model_at_fixture_datum() elegoo_relay_complete();
}

module bpi_model_preview() {
    bpi_model_at_fixture_datum() bpi_m2_zero_complete();
}

module boost_model_at_fixture_datum() {
    translate([boost_origin.x, boost_origin.y,
               plate_thickness + standoff_height + 0.2])
        children();
}

module boost_model_preview() {
    boost_model_at_fixture_datum() hiletgo_xl6009_complete();
}

module mosfet_model_at_fixture_datum() {
    inset = (mosfet_size - ceksezx_mtsd001_board_size()) / 2;
    translate([
        mosfet_origin.x + mosfet_size.x - inset.x,
        mosfet_origin.y + mosfet_size.y - inset.y,
        plate_thickness + standoff_height + 0.2
    ])
        rotate([0, 0, 180])
            children();
}

module mosfet_model_preview() {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_complete();
}

module dp100_model_at_fixture_datum() {
    translate([dp100_origin.x, dp100_origin.y,
               plate_thickness + dp100_install_lift])
        children();
}

module dp100_model_preview() {
    dp100_model_at_fixture_datum() alientek_dp100_complete();
}

module esp32_model_at_fixture_datum() {
    translate([esp32_origin.x, esp32_origin.y,
               plate_thickness + esp32_install_lift])
        children();
}

module esp32_model_preview() {
    esp32_model_at_fixture_datum() esp32_s3_supermini_complete();
}

module c270_model_at_fixture_datum() {
    translate([webcam_origin.x, webcam_origin.y, 0])
        children();
}

module c270_model_preview() {
    c270_model_at_fixture_datum() c270_complete();
}

module antenna_model_at_fixture_datum() {
    translate([antenna_origin.x, antenna_origin.y,
               plate_thickness + antenna_install_lift])
        children();
}

module antenna_model_preview() {
    antenna_model_at_fixture_datum() eightwood_ewua0205_complete();
}

module powered_hub_model_at_fixture_datum() {
    translate([powered_hub_origin.x, powered_hub_origin.y,
               plate_thickness + powered_hub_install_lift])
        children();
}

module powered_hub_model_preview() {
    powered_hub_model_at_fixture_datum() smays_microb_hub_complete();
}

module unpowered_hub_model_at_fixture_datum() {
    translate([unpowered_hub_origin.x, unpowered_hub_origin.y,
               plate_thickness + unpowered_hub_install_lift])
        children();
}

module unpowered_hub_model_preview() {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_complete();
}

module transverse_retention_straps(origin, envelope, offsets_x,
                                   component_height, install_lift = 0.20,
                                   strap_width = 2.4) {
    for (x = offsets_x) {
        // Top span plus short side legs reproduce the installed black ties
        // without duplicating hidden under-plate geometry.
        translate([origin.x + x - strap_width / 2,
                   origin.y - 1.2,
                   plate_thickness + install_lift + component_height + 0.05])
            cube([strap_width, envelope.y + 2.4, 0.75]);
        for (y = [origin.y - 1.2, origin.y + envelope.y + 0.45])
            translate([origin.x + x - strap_width / 2, y,
                       plate_thickness + install_lift])
                cube([strap_width, 0.75, component_height + 0.10]);
    }
}

module final_component_retention_preview() {
    color("#121417") {
        transverse_retention_straps(
            antenna_origin, antenna_size, antenna_model_tie_x,
            ANTENNA_MODEL_PANEL.z, antenna_install_lift, 2.2);
        transverse_retention_straps(
            powered_hub_origin, powered_hub_size, powered_hub_tie_x,
            POWERED_HUB_MODEL_BODY.z, powered_hub_install_lift, 2.7);
        transverse_retention_straps(
            unpowered_hub_origin, unpowered_hub_size,
            unpowered_hub_model_tie_x,
            UNPOWERED_HUB_MODEL_BODY.z, unpowered_hub_install_lift, 2.4);
    }
}

module final_component_preview(show_service_keepouts = true) {
    antenna_model_preview();
    powered_hub_model_preview();
    unpowered_hub_model_preview();
    final_component_retention_preview();
    if (show_service_keepouts) {
        service_keepout_preview(webcam_below_service_origin,
                                webcam_below_service_size);
        service_keepout_preview(esp32_usb_service_origin,
                                esp32_usb_service_size, "DodgerBlue");
        service_keepout_preview(dp100_banana_service_origin,
                                dp100_banana_service_size, "Goldenrod");
        service_keepout_preview(dp100_usb_service_origin,
                                dp100_usb_service_size, "DodgerBlue");
        service_keepout_preview(dp100_usb_c_service_origin,
                                dp100_usb_c_service_size, "DodgerBlue");
        for (service = hub_service_envelopes)
            service_keepout_preview(service[1], service[2], "DodgerBlue");
        service_keepout_volume_preview(powered_hub_dc_service_origin,
                                       powered_hub_dc_service_size);
    }
}

module component_preview(show_service_keepouts = true) {
    final_component_preview(show_service_keepouts);
    relay_model_preview();
    bpi_model_preview();
    boost_model_preview();
    mosfet_model_preview();
    dp100_model_preview();
    esp32_model_preview();
    c270_model_preview();
}

// ---- Calibration coupon ----------------------------------------------------
coupon_size = [120, 50];
coupon_thickness = 3.2;
coupon_pilots = [1.6, 1.8, 2.0, 2.2, 2.4];
coupon_standoff_x = [8, 20, 32, 44, 56];
coupon_slot_sizes = [[6, 2.0], [7, 2.2], [8, 2.5]];

module fit_coupon() {
    difference() {
        union() {
            rounded_prism([coupon_size.x, coupon_size.y, coupon_thickness], 3);
            for (x = coupon_standoff_x)
                translate([x, 35, coupon_thickness])
                    cylinder(d = standoff_outer_diameter, h = standoff_height);
        }

        for (i = [0 : len(coupon_pilots) - 1])
            translate([coupon_standoff_x[i], 35, -1])
                cylinder(d = coupon_pilots[i], h = coupon_thickness + standoff_height + 2);

        for (i = [0 : len(coupon_slot_sizes) - 1])
            tie_slot([12 + i * 18, 13], 0, coupon_slot_sizes[i]);
        tie_slot([62, 13], 0, frame_tie_slot);

        opening = webcam_aperture + [webcam_aperture_clearance, webcam_aperture_clearance];
        translate([76, (coupon_size.y - opening.y) / 2, -1])
            linear_extrude(height = coupon_thickness + 2)
                rounded_rect_2d(opening, webcam_aperture_radius);

        // Engraved values remain readable after slicing and identify each test.
        for (i = [0 : len(coupon_pilots) - 1])
            translate([coupon_standoff_x[i], 26, coupon_thickness - 0.45])
                linear_extrude(height = 0.6)
                    text(str(coupon_pilots[i]), size = 3, halign = "center",
                         font = "Liberation Sans:style=Bold");
        engraved_coupon_text("ZIP", [5, 5], 3);
        engraved_coupon_text("FRAME", [56, 5], 2.3);
        engraved_coupon_text(str("CAMERA ", opening.x, " x ", opening.y),
                             [73, 5], 2.5);
    }
}

module engraved_coupon_text(label, point, size) {
    translate([point.x, point.y, coupon_thickness - 0.45])
        linear_extrude(height = 0.6)
            text(label, size = size, font = "Liberation Sans:style=Bold");
}

// ---- Split-print parts ------------------------------------------------------
fixture_max_height = plate_thickness + max(standoff_height,
                                            relay_standoff_height);

module plate_lower() {
    intersection() {
        fixture_plate();
        translate([-1, -1, -1])
            cube([plate_size.x + 2, split_y + 1, fixture_max_height + 2]);
    }
}

module plate_upper() {
    intersection() {
        fixture_plate();
        translate([-1, split_y, -1])
            cube([plate_size.x + 2, plate_size.y - split_y + 1,
                  fixture_max_height + 2]);
    }
}

module joiner() {
    difference() {
        rounded_prism([14, 25, 3], 2);
        for (y = [7, 18])
            translate([7, y, -1]) cylinder(d = joiner_hole_diameter, h = 5);
    }
}

function rectangle_fits_bed(size, bed) =
    (size.x <= bed.x && size.y <= bed.y) ||
    (size.x <= bed.y && size.y <= bed.x);
assert(rectangle_fits_bed(plate_size, printable_bed),
       "Fixture plate exceeds the printer bed after required edge margins");
function envelope_inside_plate(origin, size) =
    origin.x >= 0 && origin.y >= 0 &&
    origin.x + size.x <= plate_size.x && origin.y + size.y <= plate_size.y;
assert(envelope_inside_plate(relay_origin, relay_size), "Relay envelope exceeds plate");
assert(envelope_inside_plate(bpi_origin, bpi_size), "BPI envelope exceeds plate");
assert(envelope_inside_plate(boost_origin, boost_size), "Boost envelope exceeds plate");
assert(envelope_inside_plate(mosfet_origin, mosfet_size), "MOSFET envelope exceeds plate");
assert(envelope_inside_plate(antenna_origin, antenna_size), "Antenna envelope exceeds plate");
assert(envelope_inside_plate(esp32_origin, esp32_size), "ESP32 envelope exceeds plate");
assert(envelope_inside_plate(esp32_usb_service_origin, esp32_usb_service_size),
       "ESP32 USB service keep-out exceeds plate");
assert(envelope_inside_plate(dp100_origin, dp100_size), "DP100 envelope exceeds plate");
assert(envelope_inside_plate(dp100_banana_service_origin,
                             dp100_banana_service_size),
       "DP100 banana-output service keep-out exceeds plate");
assert(envelope_inside_plate(dp100_usb_service_origin,
                             dp100_usb_service_size),
       "DP100 USB-A service keep-out exceeds plate");
assert(envelope_inside_plate(dp100_usb_c_service_origin,
                             dp100_usb_c_service_size),
       "DP100 USB-C service keep-out exceeds plate");
assert(envelope_inside_plate(webcam_origin, webcam_keepout), "Webcam keep-out exceeds plate");
assert(envelope_inside_plate(webcam_below_service_origin, webcam_below_service_size),
       "Webcam below-clearance exceeds plate");
assert(envelope_inside_plate(powered_hub_origin, powered_hub_size), "Powered hub exceeds plate");
assert(envelope_inside_plate(unpowered_hub_origin, unpowered_hub_size), "USB hub exceeds plate");
assert(bpi_size == bpi_m2_zero_board_size(),
       str("Fixture and BPI board envelopes disagree: ", bpi_size,
           " vs ", bpi_m2_zero_board_size()));
assert(bpi_hole_diameter == bpi_m2_zero_hole_diameter(),
       str("Fixture and BPI hole diameters disagree: ", bpi_hole_diameter,
           " vs ", bpi_m2_zero_hole_diameter()));
assert(bpi_hole_centres == bpi_m2_zero_hole_centres(),
       str("Fixture and BPI mounting registration disagree: ",
           bpi_hole_centres, " vs ", bpi_m2_zero_hole_centres()));
assert(BPI_MODEL_SCALE == 1.0,
       str("BPI model scale/orientation changed: ", BPI_MODEL_SCALE));
assert(BPI_MODEL_HOLE_CENTRES == bpi_hole_centres,
       str("BPI mounting registration changed: ", BPI_MODEL_HOLE_CENTRES));
assert(relay_size == elegoo_relay_installed_size(),
       str("Fixture and ELEGOO relay envelopes disagree: ", relay_size,
           " vs ", elegoo_relay_installed_size()));
assert(relay_hole_diameter == elegoo_relay_hole_diameter(),
       str("Fixture and ELEGOO relay hole diameters disagree: ",
           relay_hole_diameter, " vs ", elegoo_relay_hole_diameter()));
assert(relay_hole_centres == elegoo_relay_installed_hole_centres(),
       str("Fixture and ELEGOO relay mounting registration disagree: ",
           relay_hole_centres, " vs ",
           elegoo_relay_installed_hole_centres()));
assert(RELAY_MODEL_SCALE == 1.0,
       str("ELEGOO relay model scale/envelope changed: ",
           RELAY_MODEL_SCALE));
assert(RELAY_MODEL_HOLE_CENTRES == relay_hole_centres,
       str("ELEGOO relay mounting registration changed: ",
           RELAY_MODEL_HOLE_CENTRES));
assert(RELAY_MODEL_TERMINAL_EDGE == "+X" &&
       RELAY_MODEL_TERMINAL_EDGE ==
       elegoo_relay_installed_terminal_edge(),
       str("ELEGOO relay terminal/header orientation changed: ",
           RELAY_MODEL_TERMINAL_EDGE));
assert(elegoo_relay_channel_count() == 4 &&
       elegoo_relay_terminal_count() == 12,
       "ELEGOO relay population must retain four channels and 12 terminals");
assert(elegoo_relay_amazon_main_sha256() ==
       "a8a405e23244346ee17a98e7b317e86a2b809719e8304e413bd249308405f144",
       "ELEGOO relay Amazon reference hash changed");
assert(elegoo_relay_thingiverse_preview_sha256() ==
       "d967bb2e60d35e36d019f55ab48bb20e838cf1b8e9ab65933090c9585f16ca67",
       "ELEGOO relay rejected-model reference hash changed");
assert(bpi_m2_zero_top_dxf_sha256() ==
       "7adbb58ab77addc91a5fc2ee84df689e5db62e7ed2b9b2b12b166684b1632833",
       "BPI top-DXF reference hash changed");
assert(bpi_m2_zero_bottom_dxf_sha256() ==
       "9d0815fd9bdb3cb5dd790d8dda1eb132a36802b586dc5eab696c79cea3dc592a",
       "BPI bottom-DXF reference hash changed");
assert(webcam_aperture.x + webcam_aperture_clearance <= webcam_keepout.x &&
       webcam_aperture.y + webcam_aperture_clearance <= webcam_keepout.y,
       "Webcam aperture exceeds its keep-out");
assert(webcam_aperture.x >= webcam_aperture_minimum.x &&
       webcam_aperture.y >= webcam_aperture_minimum.y,
       "Webcam aperture is smaller than the physically measured minimum");
assert(C270_MODEL_FACE == webcam_keepout,
       str("C270 model face/fixture keep-out changed: ",
           C270_MODEL_FACE, " vs ", webcam_keepout));
assert(C270_MODEL_LENS_DIRECTION == "-Z" &&
       C270_MODEL_LENS_DIRECTION == c270_lens_direction(),
       str("C270 lens orientation changed: ", C270_MODEL_LENS_DIRECTION));
assert(c270_rear_housing_size().x <= webcam_aperture.x &&
       c270_rear_housing_size().y <= webcam_aperture.y,
       "C270 rear housing no longer fits the proven fixture aperture");
assert(webcam_lens_datum ==
       webcam_origin + c270_lens_centre_xy(),
       "C270 optical registration changed");
assert(webcam_lens_plane_z == -15.0,
       str("C270 accepted lens plane changed: ", webcam_lens_plane_z));
assert(c270_front_reference_sha256() ==
       "c86bc28778c52877a07cbd6ab03082dfe505215617180eb5064455f139a718ae",
       "C270 Logitech front-reference hash changed");
assert(c270_qsg_reference_sha256() ==
       "ad802bc5705eceb6d75c2eb6ab4219e65e50c97678e1195910ac7b7566cd8d2b",
       "C270 Logitech QSG hash changed");
assert(c270_modified_step_sha256() ==
       "a69c4917c1f2964df2f6dc082827b46958a11e74ae3cda7a142e4d0bc9b4f3d8",
       "C270 modified-STEP reference hash changed");
assert(antenna_size ==
       [ANTENNA_MODEL_PANEL.x, ANTENNA_MODEL_PANEL.y] &&
       ANTENNA_MODEL_PANEL == [114.0, 15.0, 3.0] &&
       ANTENNA_MODEL_SCALE == 1.0,
       str("Eightwood EWUA0205 model scale/envelope changed: ",
           ANTENNA_MODEL_SCALE, " ", ANTENNA_MODEL_PANEL));
assert([for (x = antenna_tie_x) antenna_tie_origin.x + x] ==
       [for (x = antenna_model_tie_x) antenna_origin.x + x] &&
       antenna_tie_origin == [42, 228.5] &&
       antenna_tie_size == [110.0, 14.3],
       "Eightwood presentation moved the accepted printable tie slots");
assert(ANTENNA_MODEL_CABLE_EDGE ==
       eightwood_ewua0205_cable_edge() &&
       ANTENNA_MODEL_CABLE_EDGE == "+X" &&
       eightwood_ewua0205_installed_count() == 1 &&
       eightwood_ewua0205_package_count() == 2,
       "Eightwood antenna count or cable orientation changed");
assert(eightwood_ewua0205_cable_length() == 300.0 &&
       eightwood_ewua0205_cable_diameter() == 0.8 &&
       eightwood_ewua0205_connector_diameter() == 2.33,
       "Eightwood coax or MHF4 dimensions changed");
assert(eightwood_ewua0205_hero_sha256() ==
       "580d541c8ec83de2b863867c440c6d3ef0e778c35498bc6e53e412b1f3de4b15" &&
       eightwood_ewua0205_dimension_sha256() ==
       "75dcf6792c609f9e500244ad3f05d4b624a6149340f6061efd288f906b51d473",
       "Eightwood listing reference hash changed");
assert(powered_hub_size ==
       [POWERED_HUB_MODEL_BODY.x, POWERED_HUB_MODEL_BODY.y] &&
       POWERED_HUB_MODEL_BODY == [105.07, 24.0, 15.0] &&
       POWERED_HUB_MODEL_SCALE == 1.0,
       str("Smays hub model scale/envelope changed: ",
           POWERED_HUB_MODEL_SCALE, " ", POWERED_HUB_MODEL_BODY));
assert(smays_microb_hub_usb_port_count() == 3 &&
       POWERED_HUB_MODEL_USB_EDGE == smays_microb_hub_usb_edge() &&
       POWERED_HUB_MODEL_USB_EDGE == "+Y" &&
       POWERED_HUB_MODEL_RJ45_EDGE == smays_microb_hub_rj45_edge() &&
       POWERED_HUB_MODEL_RJ45_EDGE == "-X" &&
       POWERED_HUB_MODEL_OTG_EDGE == smays_microb_hub_otg_edge() &&
       POWERED_HUB_MODEL_OTG_EDGE == "+X" &&
       POWERED_HUB_MODEL_DC_EDGE == smays_microb_hub_dc_edge() &&
       POWERED_HUB_MODEL_DC_EDGE == "-Y",
       "Smays USB/RJ45/OTG/DC interface orientation changed");
assert(smays_microb_hub_owner_photo_sha256() ==
       "01ecb407d5862a442ac77eb52c60763db44b5067d2c55e2e0d08fc6aed7d51e5" &&
       smays_microb_hub_dimension_sha256() ==
       "35268f4c3e4f45a74d5b010440570d1ead0b20dd9a472ae11d9cfb2a803fb16",
       "Smays owner/listing reference hash changed");
assert(unpowered_hub_size ==
       [UNPOWERED_HUB_MODEL_BODY.x, UNPOWERED_HUB_MODEL_BODY.y] &&
       UNPOWERED_HUB_MODEL_BODY == [100.0, 30.0, 10.0] &&
       UNPOWERED_HUB_MODEL_SCALE == 1.0,
       str("VIENON hub model scale/envelope changed: ",
           UNPOWERED_HUB_MODEL_SCALE, " ", UNPOWERED_HUB_MODEL_BODY));
assert(vienon_usb001_port_count() == 4 &&
       vienon_usb001_usb3_port_count() == 1 &&
       vienon_usb001_usb2_port_count() == 3 &&
       UNPOWERED_HUB_MODEL_USB_EDGE == vienon_usb001_port_edge() &&
       UNPOWERED_HUB_MODEL_USB_EDGE == "-Y" &&
       UNPOWERED_HUB_MODEL_UPSTREAM_EDGE ==
       vienon_usb001_upstream_edge() &&
       UNPOWERED_HUB_MODEL_UPSTREAM_EDGE == "+X",
       "VIENON port population or orientation changed");
assert(vienon_usb001_hero_sha256() ==
       "3c751f1dbf784083af1d7ea2ee700e7ddbccd587d77e17dfada458fb3011dc63" &&
       vienon_usb001_internal_sha256() ==
       "f5161ac65919ef52bc03edad6fed35815246ff483af24d3269169fc67b3c423a",
       "VIENON listing reference hash changed");
assert(relay_origin.x == 20 && relay_standoff_height >= 26 &&
       relay_standoff_outer_diameter >= 9,
       "Relay must retain its DP100 clearance and physically verified tall standoffs");
relay_low_standoff_y = relay_origin.y +
                        (relay_size.y - relay_hole_centres.y) / 2 -
                        relay_standoff_outer_diameter / 2;
assert(relay_low_standoff_y >= split_y,
       "Split seam intersects a tall relay standoff");
assert(boost_hole_side_clearance == 5 &&
       boost_hole_side_centre_inset == 6.5 &&
       boost_hole_top_clearance == 1.1 &&
       boost_hole_bottom_clearance == 0.7,
       "Boost mounting holes do not match their measured edge clearances");
assert(boost_size == hiletgo_xl6009_board_size() &&
       BOOST_MODEL_SCALE == 1.0,
       str("HiLetgo XL6009 model scale/envelope changed: ",
           BOOST_MODEL_SCALE, " ", boost_size));
assert(BOOST_MODEL_HOLE_CENTRES == hiletgo_xl6009_hole_centres() &&
       boost_hole_diameter == hiletgo_xl6009_hole_diameter(),
       str("HiLetgo XL6009 mounting registration changed: ",
           BOOST_MODEL_HOLE_CENTRES));
assert(BOOST_MODEL_INPUT_EDGE == hiletgo_xl6009_input_edge() &&
       BOOST_MODEL_INPUT_EDGE == "-X",
       str("HiLetgo XL6009 input/output orientation changed: ",
           BOOST_MODEL_INPUT_EDGE));
assert(hiletgo_xl6009_complete_height() == 14.0,
       "HiLetgo XL6009 populated height changed");
assert(MOSFET_MODEL_SCALE == 1.0 &&
       MOSFET_MODEL_BOARD == ceksezx_mtsd001_board_size() &&
       MOSFET_MODEL_BOARD == [34.0, 17.0],
       str("Ceksezx MTSD001 model scale/envelope changed: ",
           MOSFET_MODEL_SCALE, " ", MOSFET_MODEL_BOARD));
assert(mosfet_hole_diameter == ceksezx_mtsd001_hole_diameter() &&
       MOSFET_MODEL_HOLE_CENTRES ==
       ceksezx_mtsd001_installed_hole_centres(mosfet_size),
       str("Ceksezx MTSD001 mounting registration changed: ",
           MOSFET_MODEL_HOLE_CENTRES));
assert(MOSFET_MODEL_TERMINAL_EDGE ==
       ceksezx_mtsd001_installed_terminal_edge() &&
       MOSFET_MODEL_TERMINAL_EDGE == "-X",
       str("Ceksezx MTSD001 terminal/control orientation changed: ",
           MOSFET_MODEL_TERMINAL_EDGE));
assert(ceksezx_mtsd001_complete_height() == 12.0 &&
       ceksezx_mtsd001_terminal_count() == 4 &&
       ceksezx_mtsd001_mosfet_count() == 2,
       "Ceksezx MTSD001 population/height changed");
assert(ceksezx_mtsd001_amazon_hero_sha256() ==
       "42a2bc3a51587a51649d885db1ae87d65b1166c204ddd6e5e669cb8f76c5fd69",
       "Ceksezx MTSD001 Amazon reference hash changed");
assert(ceksezx_mtsd001_dimension_view_sha256() ==
       "6706f3e1594e2b63a8366370717503e2b09ffabacd3650f80048e746d8538fc7",
       "Ceksezx MTSD001 dimensional reference hash changed");
assert(ceksezx_mtsd001_owner_photo_sha256() ==
       "cf2419bc0a5a33edcec808d35592dc417749536ee2e8cc67885f74a656c9e2a6",
       "Ceksezx MTSD001 owner-photo hash changed");
assert(dp100_size == [alientek_dp100_body_size().x,
                      alientek_dp100_body_size().y] &&
       DP100_MODEL_BODY == alientek_dp100_body_size() &&
       DP100_MODEL_SCALE == 1.0,
       str("ALIENTEK DP100 model scale/envelope changed: ",
           DP100_MODEL_SCALE, " ", DP100_MODEL_BODY));
assert(alientek_dp100_overall_size() == [100.4, 62.2, 17.2] &&
       abs(dp100_size.x + alientek_dp100_banana_projection() -
           alientek_dp100_overall_size().x) < epsilon,
       "ALIENTEK DP100 nominal-vs-installed length reconciliation changed");
assert(DP100_MODEL_BANANA_EDGE == alientek_dp100_banana_edge() &&
       DP100_MODEL_BANANA_EDGE == "-X" &&
       DP100_MODEL_USB_EDGE == alientek_dp100_usb_edge() &&
       DP100_MODEL_USB_EDGE == "+X" &&
       DP100_MODEL_CONTROLS_EDGE == alientek_dp100_controls_edge() &&
       DP100_MODEL_CONTROLS_EDGE == "-Y",
       str("ALIENTEK DP100 connector/control orientation changed: ",
           DP100_MODEL_BANANA_EDGE, " ", DP100_MODEL_USB_EDGE, " ",
           DP100_MODEL_CONTROLS_EDGE));
assert(dp100_origin.x - alientek_dp100_banana_projection() >= 0 &&
       dp100_origin.x + dp100_size.x + dp100_usb_service_depth <= plate_size.x,
       "ALIENTEK DP100 terminal or USB access exceeds the fixture plate");
assert(alientek_dp100_amazon_reference_sha256() ==
       "d1cc4a01bcb721d4008ab76b5ed69d7946b5a39c68044a902c942d604a63ae0f",
       "ALIENTEK DP100 Amazon reference hash changed");
assert(alientek_dp100_manual_sha256() ==
       "8878f9aa3be219964c41ad3a4e679526bea54946a262fc61f35ed965d7e5f97b",
       "ALIENTEK DP100 manual hash changed");
assert(alientek_dp100_manual_appearance_sha256() ==
       "b159077910e492e4b89ae799d4b1a33a58099f083935db80fc7cc7690488ad0f",
       "ALIENTEK DP100 appearance-diagram hash changed");
assert(len(frame_tie_features) == 8,
       "Exactly eight 4040-frame tie anchors are required");
assert(webcam_centre.x == plate_size.x / 2,
       "Webcam must remain centred left-to-right");
assert(webcam_below_clearance >= 20,
       "Webcam requires at least 20 mm clear immediately below");
assert(powered_hub_long_side_service_depth >= 25 &&
       powered_hub_end_service_depth >= 18 &&
       unpowered_hub_end_service_depth >= 20,
       "USB hub connector keep-outs are smaller than the physical-fit measurements");
assert(esp32_usb_service_depth >= 20,
       "ESP32 requires at least 20 mm USB connector clearance below");
assert(esp32_size.x < esp32_size.y,
       "ESP32 short USB-C edge must face the bottom of the plate");
assert(esp32_size == esp32_s3_supermini_envelope_size(),
       str("Fixture and ESP32 physical envelopes disagree: ", esp32_size,
           " vs ", esp32_s3_supermini_envelope_size()));
assert(ESP32_MODEL_SCALE == 1.0 &&
       ESP32_MODEL_ENVELOPE == esp32_s3_supermini_envelope_size(),
       str("ESP32 model scale/envelope changed: ", ESP32_MODEL_SCALE,
           " ", ESP32_MODEL_ENVELOPE));
assert(ESP32_MODEL_USB_EDGE == esp32_s3_supermini_usb_edge() &&
       ESP32_MODEL_USB_EDGE == "bottom",
       str("ESP32 USB-C orientation changed: ", ESP32_MODEL_USB_EDGE));
assert(esp32_s3_supermini_reference_sha256() ==
       "71e35b41584fda9bfad5da9fd9d21c9369f75a2d6a522343e97bd4de5327ae1d",
       "ESP32 listing reference hash changed");
assert(esp32_tie_slot.y >= 3,
       "ESP32 tie slots require the physically requested width allowance");
assert(esp32_usb_service_width <= esp32_size.x,
       "ESP32 USB-C service width exceeds its short edge");
assert(len(esp32_tie_x) == 2 &&
       abs(esp32_tie_x[0] + esp32_tie_x[1] - esp32_size.x) < epsilon,
       "ESP32 requires two mirrored slots on each short edge");
assert(esp32_tie_x[0] + esp32_tie_slot.x / 2 +
       esp32_tie_service_clearance <=
       (esp32_size.x - esp32_usb_service_width) / 2 &&
       esp32_tie_x[1] - esp32_tie_slot.x / 2 -
       esp32_tie_service_clearance >=
       (esp32_size.x + esp32_usb_service_width) / 2,
       "ESP32 USB-C corridor overlaps its short-edge tie slots");
assert(abs((esp32_usb_service_origin.x + esp32_usb_service_width / 2) -
           (esp32_origin.x + esp32_size.x / 2)) < epsilon &&
       abs(esp32_usb_service_origin.y + esp32_usb_service_depth -
           esp32_origin.y) < epsilon,
       "ESP32 USB-C keep-out must be centred on its bottom short edge");
assert(len(dp100_tie_features) == 2,
       "DP100 requires exactly two side tie slots");
assert(dp100_tie_features[0][1].x < dp100_origin.x &&
       dp100_tie_features[1][1].x > dp100_origin.x + dp100_size.x,
       "DP100 tie slots must remain on opposite short sides");
assert(powered_hub_connector_side == "top" &&
       unpowered_hub_connector_side == "bottom",
       "USB hub connector banks must face their physically verified clear sides");
assert(powered_hub_origin.y - (unpowered_hub_origin.y + unpowered_hub_size.y) <= 11 &&
       hub_end_service_width >= 12,
       "USB hubs must retain the compact physical-fit layout and end-cable width");
assert(powered_hub_origin.y -
       (unpowered_hub_origin.y + unpowered_hub_size.y) == 6.0,
       "Exact hubs must retain the photographed six-millimetre body gap");
assert(abs(powered_hub_origin.x - unpowered_hub_origin.x - 23.65) < epsilon,
       "Exact hubs must retain the photographed X stagger");
assert(unpowered_hub_origin.x + unpowered_hub_model_tie_x[0] ==
       unpowered_hub_tie_origin.x + unpowered_hub_tie_x[0] &&
       unpowered_hub_origin.x + unpowered_hub_model_tie_x[1] ==
       unpowered_hub_tie_origin.x + unpowered_hub_tie_x[1],
       "VIENON presentation ties must remain registered to printable slots");
assert(powered_hub_dc_service_origin.y +
       powered_hub_dc_service_size.y == powered_hub_origin.y &&
       powered_hub_dc_service_origin.z >=
       plate_thickness + unpowered_hub_install_lift +
       UNPOWERED_HUB_MODEL_BODY.z + 0.5,
       "Smays DC plug must rise above the VIENON body before crossing it");

// Transparent preview solids can visually hide intersections. Make layout
// safety machine-enforced instead: every exported part hard-fails if any two
// component envelopes have less than this edge-to-edge clearance.
component_clearance = 3.0;
component_envelopes = [
    ["relay", relay_origin, relay_size],
    ["bpi", bpi_origin, bpi_size],
    ["boost", boost_origin, boost_size],
    ["mosfet", mosfet_origin, mosfet_size],
    ["antenna", antenna_origin, antenna_size],
    ["esp32", esp32_origin, esp32_size],
    ["dp100", dp100_origin, dp100_size],
    ["webcam", webcam_origin, webcam_keepout],
    ["powered_hub", powered_hub_origin, powered_hub_size],
    ["usb_hub", unpowered_hub_origin, unpowered_hub_size]
];

function transverse_slot_envelopes(owner, origin, envelope, offsets_x,
                                   dimensions = zip_slot,
                                   edge_gap = zip_edge_gap) = [
    for (x = offsets_x)
        for (y = [-edge_gap - dimensions.y / 2,
                  envelope.y + edge_gap + dimensions.y / 2])
            [str(owner, "_tie_", x, "_", y),
             [origin.x + x - dimensions.x / 2,
              origin.y + y - dimensions.y / 2],
             dimensions, owner]
];
function lateral_slot_envelopes(owner, origin, envelope, offsets_y) = [
    for (y = offsets_y)
        for (x = [-zip_edge_gap - zip_slot.y / 2,
                  envelope.x + zip_edge_gap + zip_slot.y / 2])
            [str(owner, "_tie_", x, "_", y),
             [origin.x + x - zip_slot.y / 2, origin.y + y - zip_slot.x / 2],
             [zip_slot.y, zip_slot.x], owner]
];
function oriented_slot_envelope(feature, dimensions) =
    let(size = feature[2] == 0 ? dimensions : [dimensions.y, dimensions.x])
        [feature[0], feature[1] - size / 2, size, "frame"];
function owned_slot_envelope(feature, dimensions = zip_slot) =
    let(size = feature[2] == 0 ? dimensions : [dimensions.y, dimensions.x])
        [feature[0], feature[1] - size / 2, size, feature[3]];
frame_tie_feature_envelopes = [
    for (feature = frame_tie_features)
        oriented_slot_envelope(feature, frame_tie_slot)
];
retention_feature_envelopes = concat(
    [for (feature = dp100_tie_features) owned_slot_envelope(feature)],
    transverse_slot_envelopes("antenna", antenna_tie_origin,
                              antenna_tie_size,
                              antenna_tie_x, zip_slot, antenna_tie_edge_gap),
    transverse_slot_envelopes("esp32", esp32_origin, esp32_size,
                              esp32_tie_x, esp32_tie_slot),
    transverse_slot_envelopes("powered_hub", powered_hub_origin, powered_hub_size,
                              powered_hub_tie_x, powered_hub_tie_slot),
    transverse_slot_envelopes("usb_hub", unpowered_hub_tie_origin,
                              unpowered_hub_tie_size,
                              unpowered_hub_tie_x),
    frame_tie_feature_envelopes
);
retention_clearance = 1.0;
frame_tie_component_clearance = 5.0;

function long_side_service_segment(owner, origin, envelope, depth, side,
                                   index, start_x, end_x) =
    side == "bottom" ?
        [str(owner, "_long_side_connector_", index),
         [origin.x + start_x, max(0, origin.y - depth)],
         [end_x - start_x, min(depth, origin.y)], owner] :
        [str(owner, "_long_side_connector_", index),
         [origin.x + start_x, origin.y + envelope.y],
         [end_x - start_x, depth], owner];
function long_side_service_envelopes(owner, origin, envelope, depth, side,
                                     tie_offsets) =
    let(half_slot = zip_slot.x / 2 + hub_tie_service_clearance,
        starts = [0, tie_offsets[0] + half_slot,
                  tie_offsets[1] + half_slot],
        ends = [tie_offsets[0] - half_slot,
                tie_offsets[1] - half_slot, envelope.x])
        [for (i = [0 : 2]) if (ends[i] > starts[i])
            long_side_service_segment(owner, origin, envelope, depth, side,
                                      i, starts[i], ends[i])];
function end_service_envelope(owner, origin, envelope, depth, side,
                              corridor_width = hub_end_service_width) =
    side == "left" ?
        [str(owner, "_left_end_connector"),
         [origin.x - depth, origin.y + (envelope.y - corridor_width) / 2],
         [depth, corridor_width], owner] :
        [str(owner, "_right_end_connector"),
         [origin.x + envelope.x,
          origin.y + (envelope.y - corridor_width) / 2],
         [depth, corridor_width], owner];
hub_service_envelopes = concat(
    long_side_service_envelopes("powered_hub", powered_hub_origin,
                                powered_hub_size, powered_hub_long_side_service_depth,
                                powered_hub_connector_side, powered_hub_tie_x),
    long_side_service_envelopes("usb_hub", unpowered_hub_origin,
                                unpowered_hub_size, unpowered_hub_long_side_service_depth,
                                unpowered_hub_connector_side,
                                unpowered_hub_model_tie_x),
    [end_service_envelope("powered_hub", powered_hub_origin,
                          powered_hub_size, powered_hub_end_service_depth, "left"),
     end_service_envelope("powered_hub", powered_hub_origin,
                          powered_hub_size, powered_hub_end_service_depth, "right"),
     end_service_envelope("usb_hub", unpowered_hub_origin,
                          unpowered_hub_size, unpowered_hub_end_service_depth, "right")]
);
assert(len(powered_hub_tie_x) == 2 && len(unpowered_hub_tie_x) == 2,
       "Long-side hub service segmentation requires two tie offsets per hub");
assert(len(hub_service_envelopes) == 8,
       "USB hub long-side and end-connector keep-outs are incomplete");
service_envelopes = concat(
    [["webcam_below_service", webcam_below_service_origin,
      webcam_below_service_size, "webcam"],
     ["esp32_usb_service", esp32_usb_service_origin,
      esp32_usb_service_size, "esp32"],
     ["dp100_banana_service", dp100_banana_service_origin,
      dp100_banana_service_size, "dp100"],
     ["dp100_usb_a_service", dp100_usb_service_origin,
      dp100_usb_service_size, "dp100"],
     ["dp100_usb_c_service", dp100_usb_c_service_origin,
      dp100_usb_c_service_size, "dp100"]],
    hub_service_envelopes
);
component_volumes = [
    ["powered_hub",
     [powered_hub_origin.x, powered_hub_origin.y,
      plate_thickness + powered_hub_install_lift],
     POWERED_HUB_MODEL_BODY],
    ["usb_hub",
     [unpowered_hub_origin.x, unpowered_hub_origin.y,
      plate_thickness + unpowered_hub_install_lift],
     UNPOWERED_HUB_MODEL_BODY]
];
service_volumes = [
    ["powered_hub_dc_arch",
     powered_hub_dc_service_origin,
     powered_hub_dc_service_size,
     "powered_hub"]
];
service_clearance = 1.0;

function envelopes_violate_clearance(a, b, clearance) =
    !(a[1].x + a[2].x + clearance <= b[1].x ||
      b[1].x + b[2].x + clearance <= a[1].x ||
      a[1].y + a[2].y + clearance <= b[1].y ||
      b[1].y + b[2].y + clearance <= a[1].y);
function volumes_violate_clearance(a, b, clearance) =
    !(a[1].x + a[2].x + clearance <= b[1].x ||
      b[1].x + b[2].x + clearance <= a[1].x ||
      a[1].y + a[2].y + clearance <= b[1].y ||
      b[1].y + b[2].y + clearance <= a[1].y ||
      a[1].z + a[2].z + clearance <= b[1].z ||
      b[1].z + b[2].z + clearance <= a[1].z);

joiner_fastener_envelopes = [
    for (x = joiner_centres_x)
        for (y = joiner_hole_y)
            [str("joiner_fastener_", x, "_", y),
             [x - joiner_head_diameter / 2, y - joiner_head_diameter / 2],
             [joiner_head_diameter, joiner_head_diameter]]
];

for (i = [0 : len(component_envelopes) - 2])
    for (j = [i + 1 : len(component_envelopes) - 1])
        assert(!envelopes_violate_clearance(component_envelopes[i], component_envelopes[j],
                                            component_clearance),
               str("Component envelope clearance violation: ", component_envelopes[i][0],
                   " vs ", component_envelopes[j][0]));
for (feature = retention_feature_envelopes)
    assert(envelope_inside_plate(feature[1], feature[2]),
           str("Retention feature exceeds plate: ", feature[0]));
for (service = service_envelopes)
    assert(envelope_inside_plate(service[1], service[2]),
           str("Service keep-out exceeds plate: ", service[0]));
for (fastener = joiner_fastener_envelopes)
    for (component = component_envelopes)
        assert(!envelopes_violate_clearance(fastener, component, 0),
               str("Fastener keep-out violation: ", fastener[0], " vs ", component[0]));
for (feature = retention_feature_envelopes)
    for (component = component_envelopes)
        if (feature[3] != component[0])
            let(clearance = feature[3] == "frame" ?
                            frame_tie_component_clearance : retention_clearance)
            assert(!envelopes_violate_clearance([feature[0], feature[1], feature[2]], component,
                                                clearance),
                   str("Retention-feature clearance violation: ", feature[0],
                       " vs ", component[0]));
for (i = [0 : len(retention_feature_envelopes) - 2])
    for (j = [i + 1 : len(retention_feature_envelopes) - 1])
        assert(!envelopes_violate_clearance(retention_feature_envelopes[i],
                                            retention_feature_envelopes[j],
                                            retention_clearance),
               str("Retention-feature collision: ", retention_feature_envelopes[i][0],
                   " vs ", retention_feature_envelopes[j][0]));
for (service = service_envelopes) {
    for (component = component_envelopes)
        if (service[3] != component[0])
            assert(!envelopes_violate_clearance([service[0], service[1], service[2]],
                                                component, service_clearance),
                   str("Service keep-out violation: ", service[0],
                       " vs ", component[0]));
    for (feature = retention_feature_envelopes)
        let(clearance = service[3] == "esp32" && feature[3] == "esp32" ?
                        esp32_tie_service_clearance : service_clearance)
            assert(!envelopes_violate_clearance([service[0], service[1], service[2]],
                                                [feature[0], feature[1], feature[2]],
                                                clearance),
                   str("Service/retention collision: ", service[0],
                       " vs ", feature[0]));
    for (fastener = joiner_fastener_envelopes)
        assert(!envelopes_violate_clearance([service[0], service[1], service[2]],
                                            fastener, 0),
               str("Service/fastener collision: ", service[0],
                   " vs ", fastener[0]));
}
for (fastener = joiner_fastener_envelopes)
    for (feature = retention_feature_envelopes)
        assert(!envelopes_violate_clearance(fastener,
                                            [feature[0], feature[1], feature[2]], 0),
               str("Fastener/retention collision: ", fastener[0],
                   " vs ", feature[0]));
for (service = service_volumes)
    for (component = component_volumes)
        if (service[3] != component[0])
            assert(!volumes_violate_clearance(service, component, 0.49),
                   str("3D service-volume collision: ", service[0],
                       " vs ", component[0]));

if (PART == "plate") {
    fixture_plate();
} else if (PART == "presentation_bpi") {
    bpi_model_preview();
} else if (PART == "presentation_relay") {
    relay_model_preview();
} else if (PART == "presentation_boost") {
    boost_model_preview();
} else if (PART == "presentation_mosfet") {
    mosfet_model_preview();
} else if (PART == "presentation_dp100") {
    dp100_model_preview();
} else if (PART == "presentation_esp32") {
    esp32_model_preview();
} else if (PART == "presentation_c270") {
    c270_model_preview();
} else if (PART == "presentation_antenna") {
    antenna_model_preview();
} else if (PART == "presentation_powered_hub") {
    powered_hub_model_preview();
} else if (PART == "presentation_unpowered_hub") {
    unpowered_hub_model_preview();
} else if (PART == "presentation_components") {
    // Every former proxy now has a material-specific exact model. Preserve
    // this established semantic layer for the physical black retention ties.
    final_component_retention_preview();
} else if (PART == "presentation_antenna_dark") {
    antenna_model_at_fixture_datum() {
        eightwood_ewua0205_shell();
        eightwood_ewua0205_coax();
    }
} else if (PART == "presentation_antenna_body") {
    antenna_model_at_fixture_datum() eightwood_ewua0205_shell();
} else if (PART == "presentation_antenna_metal") {
    antenna_model_at_fixture_datum() eightwood_ewua0205_metal();
} else if (PART == "presentation_antenna_markings") {
    antenna_model_at_fixture_datum() eightwood_ewua0205_markings();
} else if (PART == "presentation_vienon_shell") {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_shell();
} else if (PART == "presentation_vienon_body") {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_body();
} else if (PART == "presentation_vienon_dark") {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_dark();
} else if (PART == "presentation_vienon_metal") {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_metal();
} else if (PART == "presentation_vienon_blue") {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_blue();
} else if (PART == "presentation_vienon_led") {
    unpowered_hub_model_at_fixture_datum() vienon_usb001_led();
} else if (PART == "presentation_smays_shell") {
    powered_hub_model_at_fixture_datum() smays_microb_hub_shell();
} else if (PART == "presentation_smays_body") {
    powered_hub_model_at_fixture_datum() smays_microb_hub_body();
} else if (PART == "presentation_smays_dark") {
    powered_hub_model_at_fixture_datum() smays_microb_hub_dark();
} else if (PART == "presentation_smays_metal") {
    powered_hub_model_at_fixture_datum() smays_microb_hub_metal();
} else if (PART == "presentation_smays_led") {
    powered_hub_model_at_fixture_datum() smays_microb_hub_led();
} else if (PART == "presentation_smays_markings") {
    powered_hub_model_at_fixture_datum() smays_microb_hub_markings();
} else if (PART == "presentation_boost_pcb") {
    boost_model_at_fixture_datum() hiletgo_xl6009_pcb();
} else if (PART == "presentation_boost_dark") {
    boost_model_at_fixture_datum() hiletgo_xl6009_dark();
} else if (PART == "presentation_boost_adjuster") {
    boost_model_at_fixture_datum() hiletgo_xl6009_adjuster();
} else if (PART == "presentation_boost_metal") {
    boost_model_at_fixture_datum() hiletgo_xl6009_metal();
} else if (PART == "presentation_boost_silkscreen") {
    boost_model_at_fixture_datum() hiletgo_xl6009_silkscreen();
} else if (PART == "presentation_mosfet_pcb") {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_pcb();
} else if (PART == "presentation_mosfet_blue") {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_blue();
} else if (PART == "presentation_mosfet_dark") {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_dark();
} else if (PART == "presentation_mosfet_metal") {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_metal();
} else if (PART == "presentation_mosfet_led") {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_led();
} else if (PART == "presentation_mosfet_silkscreen") {
    mosfet_model_at_fixture_datum() ceksezx_mtsd001_silkscreen();
} else if (PART == "presentation_dp100_shell") {
    dp100_model_at_fixture_datum() alientek_dp100_shell();
} else if (PART == "presentation_dp100_dark") {
    dp100_model_at_fixture_datum() alientek_dp100_dark();
} else if (PART == "presentation_dp100_controls") {
    dp100_model_at_fixture_datum() alientek_dp100_controls();
} else if (PART == "presentation_dp100_screen") {
    dp100_model_at_fixture_datum() alientek_dp100_screen();
} else if (PART == "presentation_dp100_accent") {
    dp100_model_at_fixture_datum() alientek_dp100_accent();
} else if (PART == "presentation_dp100_metal") {
    dp100_model_at_fixture_datum() alientek_dp100_metal();
} else if (PART == "presentation_dp100_markings") {
    dp100_model_at_fixture_datum() alientek_dp100_markings();
} else if (PART == "presentation_relay_pcb") {
    relay_model_at_fixture_datum() elegoo_relay_pcb();
} else if (PART == "presentation_relay_blue") {
    relay_model_at_fixture_datum() elegoo_relay_blue();
} else if (PART == "presentation_relay_dark") {
    relay_model_at_fixture_datum() elegoo_relay_dark();
} else if (PART == "presentation_relay_metal") {
    relay_model_at_fixture_datum() elegoo_relay_metal();
} else if (PART == "presentation_relay_led") {
    relay_model_at_fixture_datum() elegoo_relay_led();
} else if (PART == "presentation_relay_silkscreen") {
    relay_model_at_fixture_datum() elegoo_relay_silkscreen();
} else if (PART == "presentation_bpi_pcb") {
    bpi_model_at_fixture_datum()
        bpi_m2_zero_pcb(
            board_size = bpi_size * BPI_MODEL_SCALE,
            hole_centres = BPI_MODEL_HOLE_CENTRES,
            hole_diameter = bpi_hole_diameter);
} else if (PART == "presentation_bpi_dark") {
    bpi_model_at_fixture_datum() bpi_m2_zero_dark_components();
} else if (PART == "presentation_bpi_metal") {
    bpi_model_at_fixture_datum() bpi_m2_zero_metal();
} else if (PART == "presentation_bpi_gold") {
    bpi_model_at_fixture_datum() bpi_m2_zero_gold();
} else if (PART == "presentation_bpi_silkscreen") {
    bpi_model_at_fixture_datum() bpi_m2_zero_silkscreen();
} else if (PART == "presentation_esp32_pcb") {
    esp32_model_at_fixture_datum()
        esp32_s3_supermini_pcb(
            envelope_size = ESP32_MODEL_ENVELOPE,
            usb_edge = ESP32_MODEL_USB_EDGE);
} else if (PART == "presentation_esp32_dark") {
    esp32_model_at_fixture_datum() esp32_s3_supermini_dark_components();
} else if (PART == "presentation_esp32_metal") {
    esp32_model_at_fixture_datum() esp32_s3_supermini_metal();
} else if (PART == "presentation_esp32_gold") {
    esp32_model_at_fixture_datum() esp32_s3_supermini_gold();
} else if (PART == "presentation_esp32_antenna") {
    esp32_model_at_fixture_datum() esp32_s3_supermini_antenna();
} else if (PART == "presentation_esp32_silkscreen") {
    esp32_model_at_fixture_datum() esp32_s3_supermini_silkscreen();
} else if (PART == "presentation_c270_shell") {
    c270_model_at_fixture_datum() c270_shell();
} else if (PART == "presentation_c270_dark") {
    c270_model_at_fixture_datum() c270_dark();
} else if (PART == "presentation_c270_glass") {
    c270_model_at_fixture_datum() c270_glass();
} else if (PART == "presentation_c270_led") {
    c270_model_at_fixture_datum() c270_led();
} else if (PART == "presentation_c270_labels") {
    c270_model_at_fixture_datum() c270_labels();
} else if (PART == "presentation_labels") {
    fixture_labels();
} else if (PART == "fit_coupon") {
    fit_coupon();
} else if (PART == "plate_lower") {
    plate_lower();
} else if (PART == "plate_upper") {
    plate_upper();
} else if (PART == "joiner") {
    joiner();
} else {
    fixture_plate();
    // OpenSCAD's background modifier keeps positioning/service ghosts visible
    // in the editor while excluding the entire subtree from render and export.
    if (SHOW_COMPONENTS) %component_preview();
    if (SHOW_LABELS) %fixture_labels();
}
