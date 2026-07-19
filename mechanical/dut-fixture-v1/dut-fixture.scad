/*
 * PocketForge DUT fixture plate v1
 *
 * Source measurements: owner caliper notes photographed 2026-07-18.
 * Coordinate system: X left-to-right, Y front-to-back, Z upward; millimetres.
 *
 * Export with, for example:
 *   openscad -o fixture.stl -D 'PART="plate"' dut-fixture.scad
 *
 * PART choices: preview, plate, fit_coupon, plate_lower, plate_upper, joiner.
 */

PART = "preview";
SHOW_COMPONENTS = true;
SHOW_LABELS = true;

$fn = 48;
epsilon = 0.05;

// ---- Printer / plate -------------------------------------------------------
printer_bed = [250, 210];             // Prusa i3 MK3S advertised build area
plate_size = [200, 240];              // portrait like sketch; rotate 90° to print
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
split_y = 152.5;
joiner_centres_x = [7.0, 139.0, 192.0];
joiner_hole_y = [split_y - 6, split_y + 5];
joiner_hole_diameter = 3.4;            // M3 clearance
joiner_head_diameter = 6.0;            // keep-out for a typical M3 pan head

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

// Layout is organized around a central webcam, accessible hub ends, a clear
// 4040-frame perimeter, and compact functional groups.
relay_origin = [30, 154.9];
relay_size = [51.85, 72.70];
relay_hole_diameter = 3.0;
relay_hole_far_spacing = [48.03, 69.93];
relay_hole_centres = relay_hole_far_spacing - [relay_hole_diameter, relay_hole_diameter];

bpi_origin = [14, 86.8];
bpi_size = [29.90, 65.00];
bpi_hole_diameter = 2.6;
bpi_hole_far_spacing = [25.60, 60.96];
bpi_hole_centres = bpi_hole_far_spacing - [bpi_hole_diameter, bpi_hole_diameter];

// The handwritten boost-board dimensions are clear; diagonal hole coordinates
// are an initial interpretation of the roughly 1 mm edge gaps in the sketch.
boost_origin = [149, 96];
boost_size = [43.16, 21.23];
boost_hole_diameter = 3.0;
boost_hole_centres = [[2.5, boost_size.y - 2.5], [boost_size.x - 2.5, 2.5]];

// Board outline was not dimensioned. The 2.2 mm holes and 15.58 mm far-edge
// spacing were; both holes are shown nearly touching the same board edge.
mosfet_origin = [157, 122];
mosfet_size = [35.0, 18.0];             // provisional envelope, easy to tune
mosfet_hole_diameter = 2.2;
mosfet_hole_centre_spacing = 15.58 - mosfet_hole_diameter;
mosfet_hole_x = mosfet_size.x - (mosfet_hole_diameter / 2 + 0.1);
mosfet_hole_centres = [
    [mosfet_hole_x, (mosfet_size.y - mosfet_hole_centre_spacing) / 2],
    [mosfet_hole_x, (mosfet_size.y + mosfet_hole_centre_spacing) / 2]
];

antenna_origin = [42, 8];
antenna_size = [110.0, 14.3];             // width measured; length provisional
antenna_tie_x = [25, 85];

esp32_origin = [8, 62];
esp32_size = [23.67, 18.5];               // owner-measured physical envelope
// Two narrow straps near the ends, matching the four surrounding slots in the
// owner's sketch while retaining 1 mm from each board end to the slot edge.
esp32_tie_y = [4.5, esp32_size.y - 4.5];
esp32_usb_service_depth = 20.0;
esp32_usb_service_origin = [esp32_origin.x,
                            esp32_origin.y - esp32_usb_service_depth];
esp32_usb_service_size = [esp32_size.x, esp32_usb_service_depth];

// Owner-corrected caliper measurement of this physical DP100 revision.
dp100_origin = [89.5, 162];
dp100_size = [94.6, 62.2];
// Interpreted from the end-offset annotations; straps sit near the end caps.
dp100_tie_x = [21.0, dp100_size.x - 19.5];

webcam_keepout = [71.0, 31.55];
webcam_aperture = [37.0, 14.69];
webcam_aperture_clearance = 0.40;         // total diametral/width clearance
webcam_aperture_radius = 5.0;
webcam_centre = [plate_size.x / 2, 132.0];
webcam_origin = webcam_centre - webcam_keepout / 2;
webcam_below_clearance = 20.0;
webcam_below_service_origin = [webcam_origin.x,
                               webcam_origin.y - webcam_below_clearance];
webcam_below_service_size = [webcam_keepout.x, webcam_below_clearance];

hub_end_service_depth = 30.0;
powered_hub_origin = [66.9, 61.7];
powered_hub_size = [105.07, 24.0];
// Important measured offsets: 24 mm from one end, 39 mm from the other.
powered_hub_tie_x = [24.0, powered_hub_size.x - 39.0];

unpowered_hub_origin = [66.9, 27.6];
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
    // Eight independent anchors tie the plate to both adjacent 4040 rails at
    // every corner. Orthogonal slots make the intended tie direction obvious.
    for (feature = frame_tie_features)
        tie_slot(feature[1], feature[2], frame_tie_slot);

    // Split-print bridge holes (also useful general-purpose fixture holes).
    for (x = joiner_centres_x)
        for (y = joiner_hole_y)
            through_hole([x, y], joiner_hole_diameter);

    four_standoff_bores(relay_origin, relay_size, relay_hole_centres, m25_pilot_diameter);
    four_standoff_bores(bpi_origin, bpi_size, bpi_hole_centres, m25_pilot_diameter);
    point_standoff_bores(boost_origin, boost_hole_centres, m25_pilot_diameter);
    point_standoff_bores(mosfet_origin, mosfet_hole_centres, m2_pilot_diameter);

    transverse_tie_slots(dp100_origin, dp100_size, dp100_tie_x);
    transverse_tie_slots(antenna_origin, antenna_size, antenna_tie_x);
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
    engraved_text("RELAY", [30, 159]);
    engraved_text("BPI M2 ZERO", [10, 108], 3.0, 90);
    engraved_text("BOOST", [149, 91]);
    engraved_text("MOSFET", [157, 117]);
    engraved_text("ANT", [88, 13]);
    engraved_text("ESP32", [8, 59]);
    engraved_text("DP100", [126, 159]);
    engraved_text("WEBCAM (UNDER)", [76, 149]);
    engraved_text("POWERED HUB", [89, 74]);
    engraved_text("USB HUB", [103, 38]);
}

module envelope(origin, size, height, colour, radius = 2) {
    color(colour, 0.45)
        translate([origin.x, origin.y, plate_thickness + standoff_height + 0.2])
            rounded_prism([size.x, size.y, height], min(radius, min(size.x, size.y) / 2));
}

module service_keepout_preview(origin, size, colour = "Crimson") {
    color(colour, 0.20)
        translate([origin.x, origin.y, plate_thickness + 0.1])
            rounded_prism([size.x, size.y, 0.8], 1.5);
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
    service_keepout_preview(webcam_below_service_origin, webcam_below_service_size);
    service_keepout_preview(esp32_usb_service_origin, esp32_usb_service_size,
                            "DodgerBlue");
    for (service = hub_service_envelopes)
        service_keepout_preview(service[1], service[2], "DodgerBlue");
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
        engraved_coupon_text("CAMERA 37.4 x 15.09", [73, 5], 2.5);
    }
}

module engraved_coupon_text(label, point, size) {
    translate([point.x, point.y, coupon_thickness - 0.45])
        linear_extrude(height = 0.6)
            text(label, size = size, font = "Liberation Sans:style=Bold");
}

// ---- Split-print parts ------------------------------------------------------
module plate_lower() {
    intersection() {
        fixture_plate();
        translate([-1, -1, -1]) cube([plate_size.x + 2, split_y + 1, 20]);
    }
}

module plate_upper() {
    intersection() {
        fixture_plate();
        translate([-1, split_y, -1])
            cube([plate_size.x + 2, plate_size.y - split_y + 1, 20]);
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
assert(rectangle_fits_bed(plate_size, printer_bed),
       "Fixture plate exceeds configured printer bed in both orientations");
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
assert(envelope_inside_plate(webcam_origin, webcam_keepout), "Webcam keep-out exceeds plate");
assert(envelope_inside_plate(webcam_below_service_origin, webcam_below_service_size),
       "Webcam below-clearance exceeds plate");
assert(envelope_inside_plate(powered_hub_origin, powered_hub_size), "Powered hub exceeds plate");
assert(envelope_inside_plate(unpowered_hub_origin, unpowered_hub_size), "USB hub exceeds plate");
assert(webcam_aperture.x + webcam_aperture_clearance <= webcam_keepout.x &&
       webcam_aperture.y + webcam_aperture_clearance <= webcam_keepout.y,
       "Webcam aperture exceeds its keep-out");
assert(len(frame_tie_features) == 8,
       "Exactly eight 4040-frame tie anchors are required");
assert(webcam_centre.x == plate_size.x / 2,
       "Webcam must remain centred left-to-right");
assert(webcam_below_clearance >= 20,
       "Webcam requires at least 20 mm clear immediately below");
assert(hub_end_service_depth >= 30,
       "USB hubs require at least 30 mm connector clearance at both ends");
assert(esp32_usb_service_depth >= 20,
       "ESP32 requires at least 20 mm USB connector clearance below");

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

function transverse_slot_envelopes(owner, origin, envelope, offsets_x) = [
    for (x = offsets_x)
        for (y = [-zip_edge_gap - zip_slot.y / 2,
                  envelope.y + zip_edge_gap + zip_slot.y / 2])
            [str(owner, "_tie_", x, "_", y),
             [origin.x + x - zip_slot.x / 2, origin.y + y - zip_slot.y / 2],
             [zip_slot.x, zip_slot.y], owner]
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
frame_tie_feature_envelopes = [
    for (feature = frame_tie_features)
        oriented_slot_envelope(feature, frame_tie_slot)
];
retention_feature_envelopes = concat(
    transverse_slot_envelopes("dp100", dp100_origin, dp100_size, dp100_tie_x),
    transverse_slot_envelopes("antenna", antenna_origin, antenna_size, antenna_tie_x),
    lateral_slot_envelopes("esp32", esp32_origin, esp32_size, esp32_tie_y),
    transverse_slot_envelopes("powered_hub", powered_hub_origin, powered_hub_size,
                              powered_hub_tie_x),
    transverse_slot_envelopes("usb_hub", unpowered_hub_origin, unpowered_hub_size,
                              unpowered_hub_tie_x),
    frame_tie_feature_envelopes
);
retention_clearance = 1.0;
frame_tie_component_clearance = 5.0;

function end_service_envelopes(owner, origin, envelope, depth) = [
    // Outside the plate is inherently clear, so edge-adjacent service zones
    // are clipped to printable area while still reserving `depth` in reality.
    [str(owner, "_left_connector"), [max(0, origin.x - depth), origin.y],
     [min(depth, origin.x), envelope.y], owner],
    [str(owner, "_right_connector"), [origin.x + envelope.x, origin.y],
     [min(depth, plate_size.x - (origin.x + envelope.x)), envelope.y], owner]
];
hub_service_envelopes = concat(
    end_service_envelopes("powered_hub", powered_hub_origin, powered_hub_size,
                          hub_end_service_depth),
    end_service_envelopes("usb_hub", unpowered_hub_origin, unpowered_hub_size,
                          hub_end_service_depth)
);
service_envelopes = concat(
    [["webcam_below_service", webcam_below_service_origin,
      webcam_below_service_size, "webcam"],
     ["esp32_usb_service", esp32_usb_service_origin,
      esp32_usb_service_size, "esp32"]],
    hub_service_envelopes
);
service_clearance = 1.0;

function envelopes_violate_clearance(a, b, clearance) =
    !(a[1].x + a[2].x + clearance <= b[1].x ||
      b[1].x + b[2].x + clearance <= a[1].x ||
      a[1].y + a[2].y + clearance <= b[1].y ||
      b[1].y + b[2].y + clearance <= a[1].y);

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
        assert(!envelopes_violate_clearance([service[0], service[1], service[2]],
                                            [feature[0], feature[1], feature[2]],
                                            service_clearance),
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

if (PART == "plate") {
    fixture_plate();
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
}
