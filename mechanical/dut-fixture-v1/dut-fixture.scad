/*
 * PocketForge DUT fixture plate v1
 *
 * Source measurements: owner caliper notes photographed 2026-07-18.
 * Coordinate system: X left-to-right, Y front-to-back, Z upward; millimetres.
 *
 * Export with, for example:
 *   openscad -o fixture.stl -D 'PART="plate"' dut-fixture.scad
 *
 * PART choices: preview, plate, fit_coupon, plate_left, plate_right, joiner.
 */

PART = "preview";
SHOW_COMPONENTS = true;
SHOW_LABELS = true;

$fn = 48;
epsilon = 0.05;

// ---- Printer / plate -------------------------------------------------------
printer_bed = [250, 210];             // Prusa i3 MK3S advertised build area
plate_size = [240, 200];              // 5 mm margin on every bed edge
plate_thickness = 3.2;
plate_corner_radius = 4;
fixture_mount_diameter = 4.3;         // M4 clearance
fixture_mount_inset = 7.5;

// Optional split-plate joiners. The full plate also retains these useful holes.
split_x = plate_size.x / 2;
joiner_centres_y = [10, 86, 126, 190];
joiner_hole_x = [split_x - 6, split_x + 6];
joiner_hole_diameter = 3.4;            // M3 clearance

// ---- Printed fastener interfaces ------------------------------------------
standoff_outer_diameter = 7.0;
standoff_height = 6.0;
m25_pilot_diameter = 2.2;              // tune after printing fit_coupon
m2_pilot_diameter = 1.7;               // tune after printing fit_coupon
zip_slot = [7.0, 2.2];                 // common 2.0 mm-wide cable tie
zip_edge_gap = 2.0;

// ---- Component envelopes and measured interfaces --------------------------
// Hole spacing in the notes was measured far outside-edge to far outside-edge.
// Therefore centre spacing = noted spacing - hole diameter.

relay_origin = [8, 119];
relay_size = [51.85, 72.70];
relay_hole_diameter = 3.0;
relay_hole_far_spacing = [48.03, 69.93];
relay_hole_centres = relay_hole_far_spacing - [relay_hole_diameter, relay_hole_diameter];

bpi_origin = [8, 46];
bpi_size = [29.90, 65.00];
bpi_hole_diameter = 2.6;
bpi_hole_far_spacing = [25.60, 60.96];
bpi_hole_centres = bpi_hole_far_spacing - [bpi_hole_diameter, bpi_hole_diameter];

// The handwritten boost-board dimensions are clear; diagonal hole coordinates
// are an initial interpretation of the roughly 1 mm edge gaps in the sketch.
boost_origin = [8, 16];
boost_size = [43.16, 21.23];
boost_hole_diameter = 3.0;
boost_hole_centres = [[2.5, boost_size.y - 2.5], [boost_size.x - 2.5, 2.5]];

// Board outline was not dimensioned. The 2.2 mm holes and 15.58 mm far-edge
// spacing were; both holes are shown nearly touching the same board edge.
mosfet_origin = [58, 17];
mosfet_size = [35.0, 18.0];             // provisional envelope, easy to tune
mosfet_hole_diameter = 2.2;
mosfet_hole_centre_spacing = 15.58 - mosfet_hole_diameter;
mosfet_hole_x = mosfet_size.x - (mosfet_hole_diameter / 2 + 0.1);
mosfet_hole_centres = [
    [mosfet_hole_x, (mosfet_size.y - mosfet_hole_centre_spacing) / 2],
    [mosfet_hole_x, (mosfet_size.y + mosfet_hole_centre_spacing) / 2]
];

antenna_origin = [50, 45];
antenna_size = [14.3, 110.0];            // width measured; length provisional
antenna_tie_y = [15, 55, 95];

esp32_origin = [73, 72];
esp32_size = [24.0, 65.0];               // provisional dev-board envelope
esp32_tie_y = [8, 57];

// Owner-corrected caliper measurement of this physical DP100 revision.
dp100_origin = [137, 130];
dp100_size = [94.6, 62.2];
// Interpreted from the end-offset annotations; straps sit near the end caps.
dp100_tie_x = [21.0, dp100_size.x - 19.5];

webcam_origin = [124, 91];
webcam_keepout = [71.0, 31.55];
webcam_aperture = [37.0, 14.69];
webcam_aperture_clearance = 0.40;         // total diametral/width clearance
webcam_aperture_radius = 5.0;

powered_hub_origin = [124, 56];
powered_hub_size = [105.07, 24.0];
// Important measured offsets: 24 mm from one end, 39 mm from the other.
powered_hub_tie_x = [24.0, powered_hub_size.x - 39.0];

unpowered_hub_origin = [124, 20];
unpowered_hub_size = [105.0, 24.0];       // owner allowed an estimate
unpowered_hub_tie_x = [25.0, 80.0];

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
module four_standoffs(origin, envelope, spacing, pilot, height = standoff_height) {
    margin = (envelope - spacing) / 2;
    for (dx = [margin.x, margin.x + spacing.x])
        for (dy = [margin.y, margin.y + spacing.y])
            translate([origin.x + dx, origin.y + dy, plate_thickness])
                cylinder(d = standoff_outer_diameter, h = height);
}

module four_standoff_bores(origin, envelope, spacing, pilot, height = standoff_height) {
    margin = (envelope - spacing) / 2;
    for (dx = [margin.x, margin.x + spacing.x])
        for (dy = [margin.y, margin.y + spacing.y])
            through_hole([origin.x + dx, origin.y + dy], pilot);
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

module transverse_tie_slots(origin, envelope, offsets_x) {
    // A strap crosses the component's short (Y) axis; slots run along X.
    for (x = offsets_x)
        for (y = [-zip_edge_gap - zip_slot.y / 2,
                  envelope.y + zip_edge_gap + zip_slot.y / 2])
            tie_slot([origin.x + x, origin.y + y], 0);
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
    four_standoffs(relay_origin, relay_size, relay_hole_centres, m25_pilot_diameter);
    four_standoffs(bpi_origin, bpi_size, bpi_hole_centres, m25_pilot_diameter);
    point_standoffs(boost_origin, boost_hole_centres, m25_pilot_diameter);
    point_standoffs(mosfet_origin, mosfet_hole_centres, m2_pilot_diameter);
}

module fixture_cutouts() {
    // Whole-fixture mounting holes.
    for (x = [fixture_mount_inset, plate_size.x - fixture_mount_inset])
        for (y = [fixture_mount_inset, plate_size.y - fixture_mount_inset])
            through_hole([x, y], fixture_mount_diameter);

    // Split-print bridge holes (also useful general-purpose fixture holes).
    for (x = joiner_hole_x)
        for (y = joiner_centres_y)
            through_hole([x, y], joiner_hole_diameter);

    four_standoff_bores(relay_origin, relay_size, relay_hole_centres, m25_pilot_diameter);
    four_standoff_bores(bpi_origin, bpi_size, bpi_hole_centres, m25_pilot_diameter);
    point_standoff_bores(boost_origin, boost_hole_centres, m25_pilot_diameter);
    point_standoff_bores(mosfet_origin, mosfet_hole_centres, m2_pilot_diameter);

    transverse_tie_slots(dp100_origin, dp100_size, dp100_tie_x);
    lateral_tie_slots(antenna_origin, antenna_size, antenna_tie_y);
    lateral_tie_slots(esp32_origin, esp32_size, esp32_tie_y);
    transverse_tie_slots(powered_hub_origin, powered_hub_size, powered_hub_tie_x);
    transverse_tie_slots(unpowered_hub_origin, unpowered_hub_size, unpowered_hub_tie_x);

    // Webcam is offered from below; only the smaller rear housing protrudes.
    opening = webcam_aperture + [webcam_aperture_clearance, webcam_aperture_clearance];
    opening_origin = webcam_origin + (webcam_keepout - opening) / 2;
    translate([opening_origin.x, opening_origin.y, -1])
        linear_extrude(height = plate_thickness + 2)
            rounded_rect_2d(opening, webcam_aperture_radius);

    if (SHOW_LABELS)
        fixture_labels(engrave = true);
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
module engraved_text(label, point, size = 3.2, rotation = 0) {
    translate([point.x, point.y, plate_thickness - 0.45])
        linear_extrude(height = 0.6)
            rotate(rotation)
                text(label, size = size, halign = "left", valign = "baseline",
                     font = "Liberation Sans:style=Bold");
}

module fixture_labels(engrave = true) {
    engraved_text("RELAY", [8, 114]);
    engraved_text("BPI M2 ZERO", [8, 41]);
    engraved_text("BOOST", [8, 11]);
    engraved_text("MOSFET", [58, 12]);
    engraved_text("ANT", [46, 73], 3.0, 90);
    engraved_text("ESP32", [69, 91], 3.0, 90);
    engraved_text("DP100", [137, 125]);
    engraved_text("WEBCAM (UNDER)", [124, 86]);
    engraved_text("POWERED HUB", [124, 51]);
    engraved_text("USB HUB", [124, 15]);
}

module envelope(origin, size, height, colour, radius = 2) {
    color(colour, 0.45)
        translate([origin.x, origin.y, plate_thickness + standoff_height + 0.2])
            rounded_prism([size.x, size.y, height], min(radius, min(size.x, size.y) / 2));
}

module component_preview() {
    envelope(relay_origin, relay_size, 15, "RoyalBlue");
    envelope(bpi_origin, bpi_size, 7, "SteelBlue");
    envelope(boost_origin, boost_size, 12, "DarkOrange");
    envelope(mosfet_origin, mosfet_size, 8, "Teal");
    envelope(antenna_origin, antenna_size, 4, "DimGray", 4);
    envelope(esp32_origin, esp32_size, 8, "DarkSlateGray");
    envelope(dp100_origin, dp100_size, 17.2, "SlateGray", 5);
    // The webcam front body stays below the plate; render its keep-out ghosted.
    color("Black", 0.25)
        translate([webcam_origin.x, webcam_origin.y, -8])
            rounded_prism([webcam_keepout.x, webcam_keepout.y, 8], 8);
    envelope(powered_hub_origin, powered_hub_size, 15, "WhiteSmoke", 4);
    envelope(unpowered_hub_origin, unpowered_hub_size, 15, "Black", 4);
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
        engraved_coupon_text("CAMERA 37.4 x 15.09", [73, 5], 2.5);
    }
}

module engraved_coupon_text(label, point, size) {
    translate([point.x, point.y, coupon_thickness - 0.45])
        linear_extrude(height = 0.6)
            text(label, size = size, font = "Liberation Sans:style=Bold");
}

// ---- Split-print parts ------------------------------------------------------
module plate_left() {
    intersection() {
        fixture_plate();
        translate([-1, -1, -1]) cube([split_x + 1, plate_size.y + 2, 20]);
    }
}

module plate_right() {
    intersection() {
        fixture_plate();
        translate([split_x, -1, -1]) cube([plate_size.x - split_x + 1, plate_size.y + 2, 20]);
    }
}

module joiner() {
    difference() {
        rounded_prism([26, 14, 3], 2);
        for (x = [7, 19])
            translate([x, 7, -1]) cylinder(d = joiner_hole_diameter, h = 5);
    }
}

assert(plate_size.x <= printer_bed.x && plate_size.y <= printer_bed.y,
       "Fixture plate exceeds configured printer bed");
function envelope_inside_plate(origin, size) =
    origin.x >= 0 && origin.y >= 0 &&
    origin.x + size.x <= plate_size.x && origin.y + size.y <= plate_size.y;
assert(envelope_inside_plate(relay_origin, relay_size), "Relay envelope exceeds plate");
assert(envelope_inside_plate(bpi_origin, bpi_size), "BPI envelope exceeds plate");
assert(envelope_inside_plate(boost_origin, boost_size), "Boost envelope exceeds plate");
assert(envelope_inside_plate(mosfet_origin, mosfet_size), "MOSFET envelope exceeds plate");
assert(envelope_inside_plate(antenna_origin, antenna_size), "Antenna envelope exceeds plate");
assert(envelope_inside_plate(esp32_origin, esp32_size), "ESP32 envelope exceeds plate");
assert(envelope_inside_plate(dp100_origin, dp100_size), "DP100 envelope exceeds plate");
assert(envelope_inside_plate(webcam_origin, webcam_keepout), "Webcam keep-out exceeds plate");
assert(envelope_inside_plate(powered_hub_origin, powered_hub_size), "Powered hub exceeds plate");
assert(envelope_inside_plate(unpowered_hub_origin, unpowered_hub_size), "USB hub exceeds plate");
assert(webcam_aperture.x + webcam_aperture_clearance <= webcam_keepout.x &&
       webcam_aperture.y + webcam_aperture_clearance <= webcam_keepout.y,
       "Webcam aperture exceeds its keep-out");

if (PART == "plate") {
    fixture_plate();
} else if (PART == "fit_coupon") {
    fit_coupon();
} else if (PART == "plate_left") {
    plate_left();
} else if (PART == "plate_right") {
    plate_right();
} else if (PART == "joiner") {
    joiner();
} else {
    fixture_plate();
    if (SHOW_COMPONENTS) component_preview();
}
