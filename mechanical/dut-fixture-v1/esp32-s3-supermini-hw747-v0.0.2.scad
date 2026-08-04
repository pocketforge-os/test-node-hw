/*
 * ACEIRMC ESP32-S3 SuperMini / HW-747 V0.0.2 presentation model.
 *
 * This is an original, source-native reconstruction of the populated board in
 * the PocketForge fixture. No third-party mesh, footprint, or listing artwork
 * is embedded. The outer envelope comes from the owner's physical caliper
 * measurement. Component registration and markings were reconstructed from
 * the Amazon ASIN B0GS1X97DZ listing photographs saved on 2026-07-26. See
 * ESP32-S3-SUPERMINI-PROVENANCE.md for immutable reference hashes and URLs.
 *
 * Local coordinates: X across the short axis, Y from the protruding USB-C tip
 * to the antenna edge, and Z upward from the PCB underside. This deliberately
 * makes USB-C the local "bottom" edge so fixture placement cannot silently
 * rotate the service connector away from its cable corridor. Millimetres.
 */

function esp32_s3_supermini_envelope_size() = [18.50, 23.67];
function esp32_s3_supermini_usb_edge() = "bottom";
function esp32_s3_supermini_pcb_thickness() = 1.00;
function esp32_s3_supermini_reference_sha256() =
    "71e35b41584fda9bfad5da9fd9d21c9369f75a2d6a522343e97bd4de5327ae1d";

esp32_envelope = esp32_s3_supermini_envelope_size();
esp32_pcb_t = esp32_s3_supermini_pcb_thickness();
esp32_pcb_origin_y = 1.37;
esp32_pcb_size = [esp32_envelope.x,
                  esp32_envelope.y - esp32_pcb_origin_y];
esp32_pcb_radius = 0.55;
esp32_hole_d = 1.00;
esp32_pad_d = 2.05;
esp32_pad_pitch = 2.54;
esp32_pad_rows = 9;
esp32_pad_x = [1.05, esp32_envelope.x - 1.05];
// Nine rows at 2.54 mm pitch; the two end annuli land exactly inside the
// owner's measured overall envelope rather than inflating it.
esp32_pad_first_y = 2.325;
esp32_usb_size = [9.25, 5.55, 3.20];
esp32_usb_origin = [(esp32_envelope.x - esp32_usb_size.x) / 2, 0,
                    esp32_pcb_t];
esp32_chip_centre = [esp32_envelope.x / 2, 13.25];
esp32_chip_size = [7.05, 7.05];
esp32_epsilon = 0.02;

module esp32_rounded_rect_2d(size, radius, center = false) {
    translated = center ? -size / 2 : [0, 0];
    translate(translated)
        hull()
            for (x = [radius, size.x - radius])
                for (y = [radius, size.y - radius])
                    translate([x, y]) circle(r = radius, $fn = 24);
}

module esp32_rounded_prism(origin, size, radius = 0.25) {
    translate(origin)
        linear_extrude(height = size.z)
            esp32_rounded_rect_2d(
                [size.x, size.y],
                min(radius, min(size.x, size.y) / 2));
}

module esp32_rotated_prism(centre, size, height, angle = 0,
                           z = esp32_pcb_t, radius = 0.25) {
    translate([centre.x, centre.y, z])
        rotate([0, 0, angle])
            linear_extrude(height = height)
                esp32_rounded_rect_2d(size, radius, true);
}

module esp32_chip(origin, size, height = 0.65, radius = 0.18,
                  z = esp32_pcb_t) {
    esp32_rounded_prism([origin.x, origin.y, z],
                        [size.x, size.y, height], radius);
}

module esp32_s3_supermini_pcb(
    envelope_size = esp32_s3_supermini_envelope_size(),
    usb_edge = esp32_s3_supermini_usb_edge()
) {
    assert(envelope_size == esp32_s3_supermini_envelope_size(),
           str("ESP32 model envelope changed: ", envelope_size));
    assert(usb_edge == "bottom",
           str("ESP32 USB-C orientation changed: ", usb_edge));

    difference() {
        translate([0, esp32_pcb_origin_y])
            linear_extrude(height = esp32_pcb_t)
                esp32_rounded_rect_2d(esp32_pcb_size, esp32_pcb_radius);
        for (x = esp32_pad_x)
            for (row = [0 : esp32_pad_rows - 1])
                translate([x, esp32_pad_first_y + row * esp32_pad_pitch,
                           -esp32_epsilon])
                    cylinder(d = esp32_hole_d,
                             h = esp32_pcb_t + 2 * esp32_epsilon, $fn = 20);
    }
}

module esp32_s3_supermini_dark_components() {
    // The listing's ESP32-S3FH4R2 package is the board's dominant diagonal.
    esp32_rotated_prism(esp32_chip_centre, esp32_chip_size, 0.72, 45,
                        esp32_pcb_t, 0.32);

    // Black BOOT/RST caps on their metal tactile-switch frames.
    for (centre = [[3.92, 6.65], [14.58, 6.65]])
        esp32_rotated_prism(centre, [1.55, 1.55], 0.75, 0,
                            esp32_pcb_t + 0.65, 0.28);

    // Regulator, charger, oscillator driver, and the visible SMD population.
    esp32_chip([1.95, 8.55], [3.15, 2.35], 0.72, 0.20);
    esp32_chip([13.45, 8.70], [2.35, 2.65], 0.70, 0.18);
    esp32_chip([7.45, 5.15], [3.25, 1.45], 0.62, 0.15);
    esp32_chip([1.90, 16.80], [2.25, 1.55], 0.60, 0.15);
    esp32_chip([14.35, 16.65], [2.15, 1.60], 0.60, 0.15);

    for (item = [
        [[2.35, 11.65], [1.35, 0.72]],
        [[2.45, 13.05], [1.25, 0.68]],
        [[3.20, 15.10], [1.55, 0.72]],
        [[5.05, 7.95], [1.15, 0.62]],
        [[5.35, 10.15], [1.35, 0.68]],
        [[6.05, 17.25], [1.25, 0.68]],
        [[7.15, 19.05], [1.10, 0.62]],
        [[10.15, 5.20], [1.15, 0.62]],
        [[11.65, 7.95], [1.30, 0.68]],
        [[12.25, 18.50], [1.25, 0.66]],
        [[14.35, 11.70], [1.35, 0.68]],
        [[14.75, 14.35], [1.25, 0.66]]
    ])
        esp32_chip(item[0], item[1], 0.42, 0.10);

    // Low-profile underside population visible in the listing's reverse view.
    esp32_chip([3.65, 13.75], [2.15, 1.15], 0.45, 0.12, -0.45);
    esp32_chip([11.85, 15.20], [2.05, 1.20], 0.45, 0.12, -0.45);
    esp32_chip([7.95, 18.15], [2.55, 1.35], 0.45, 0.12, -0.45);
}

module esp32_s3_supermini_metal() {
    // USB-C receptacle, centred on and protruding from the bottom short edge.
    esp32_rounded_prism(esp32_usb_origin, esp32_usb_size, 0.45);

    // Two square tactile-switch frames, a crystal, and metallic SMD caps.
    for (centre = [[3.92, 6.65], [14.58, 6.65]])
        esp32_rotated_prism(centre, [3.55, 3.55], 0.72, 0,
                            esp32_pcb_t, 0.30);
    esp32_rounded_prism([5.65, 8.25, esp32_pcb_t],
                        [2.55, 1.55, 0.62], 0.15);
    esp32_rounded_prism([11.25, 18.10, esp32_pcb_t],
                        [2.35, 1.55, 0.58], 0.14);

    for (item = [
        [[2.10, 5.00], [1.25, 0.72]],
        [[5.15, 11.20], [1.15, 0.64]],
        [[6.05, 18.55], [1.20, 0.66]],
        [[11.40, 5.05], [1.15, 0.64]],
        [[13.35, 7.70], [1.20, 0.66]],
        [[14.95, 15.25], [1.15, 0.64]]
    ])
        esp32_rounded_prism([item[0].x, item[0].y, esp32_pcb_t],
                            [item[1].x, item[1].y, 0.42], 0.10);
}

module esp32_pad_ring(point, z, downward = false) {
    translate([point.x, point.y, z])
        if (downward)
            mirror([0, 0, 1])
                difference() {
                    cylinder(d = esp32_pad_d, h = 0.07, $fn = 24);
                    translate([0, 0, -esp32_epsilon])
                        cylinder(d = esp32_hole_d,
                                 h = 0.07 + 2 * esp32_epsilon, $fn = 20);
                }
        else
            difference() {
                cylinder(d = esp32_pad_d, h = 0.07, $fn = 24);
                translate([0, 0, -esp32_epsilon])
                    cylinder(d = esp32_hole_d,
                             h = 0.07 + 2 * esp32_epsilon, $fn = 20);
            }
}

module esp32_s3_supermini_gold() {
    // All 18 plated through-holes and annuli, on both PCB faces.
    for (x = esp32_pad_x)
        for (row = [0 : esp32_pad_rows - 1]) {
            point = [x, esp32_pad_first_y + row * esp32_pad_pitch];
            esp32_pad_ring(point, esp32_pcb_t);
            esp32_pad_ring(point, 0, true);
        }

    // Battery and factory-test pads exposed on the reverse.
    for (point = [[6.55, 19.80], [8.30, 19.80],
                  [10.20, 19.80], [11.95, 19.80]])
        translate([point.x, point.y, -0.07])
            cylinder(d = 1.20, h = 0.07, $fn = 20);
    for (point = [[5.25, 17.25], [9.25, 20.85], [13.10, 17.55]])
        translate([point.x, point.y, esp32_pcb_t])
            cylinder(d = 0.95, h = 0.08, $fn = 20);
}

module esp32_s3_supermini_antenna() {
    // The photographed HW-747 carries a red ceramic antenna marked "C3".
    esp32_rounded_prism([6.42, 20.83, esp32_pcb_t],
                        [5.66, 2.45, 0.78], 0.22);
}

module esp32_silk_text(label, point, size, z, rotation = 0,
                       halign = "center", downward = false) {
    translate([point.x, point.y, z])
        if (downward)
            mirror([0, 0, 1])
                linear_extrude(height = 0.08)
                    rotate(rotation)
                        text(label, size = size, halign = halign,
                             valign = "center",
                             font = "Liberation Sans:style=Bold");
        else
            linear_extrude(height = 0.08)
                rotate(rotation)
                    text(label, size = size, halign = halign,
                         valign = "center",
                         font = "Liberation Sans:style=Bold");
}

module esp32_s3_supermini_silkscreen() {
    top_z = esp32_pcb_t + 0.02;
    left_labels = ["5V", "GND", "3V3", "13", "12", "11", "10", "9", "8"];
    right_labels = ["TX", "RX", "1", "2", "3", "4", "5", "6", "7"];

    for (row = [0 : esp32_pad_rows - 1]) {
        y = esp32_pad_first_y + row * esp32_pad_pitch;
        esp32_silk_text(left_labels[row], [2.30, y], 0.50, top_z, 0, "left");
        esp32_silk_text(right_labels[row], [16.20, y], 0.50, top_z, 0, "right");
    }
    esp32_silk_text("RST", [3.92, 4.38], 0.55, top_z);
    esp32_silk_text("BOOT", [14.58, 4.38], 0.52, top_z);
    esp32_silk_text("48", [13.20, 19.65], 0.52, top_z);
    esp32_silk_text("C3", [9.25, 22.05], 0.85,
                    esp32_pcb_t + 0.80);

    translate([esp32_chip_centre.x, esp32_chip_centre.y,
               esp32_pcb_t + 0.74])
        rotate([0, 0, 45])
            linear_extrude(height = 0.07)
                text("ESP32-S3", size = 0.72, halign = "center",
                     valign = "center",
                     font = "Liberation Sans:style=Bold");

    // Reverse markings identify the exact board revision in the listing.
    esp32_silk_text("HW-747 V0.0.2", [9.25, 6.85], 0.80, -0.02,
                    0, "center", true);
    esp32_silk_text("ESP32-S3", [9.25, 9.15], 0.85, -0.02,
                    0, "center", true);
    esp32_silk_text("Super Mini", [9.25, 11.25], 0.82, -0.02,
                    0, "center", true);
}

module esp32_s3_supermini_complete() {
    color("#15191d") esp32_s3_supermini_pcb();
    color("#111317") esp32_s3_supermini_dark_components();
    color("#b9bec4") esp32_s3_supermini_metal();
    color("#d6a83a") esp32_s3_supermini_gold();
    color("#c62326") esp32_s3_supermini_antenna();
    color("#eceee8") esp32_s3_supermini_silkscreen();
}
