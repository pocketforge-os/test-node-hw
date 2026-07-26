/*
 * ELEGOO four-channel 5 V optocoupled relay presentation model.
 *
 * This is an original, source-native reconstruction of the exact board sold
 * under Amazon ASIN B09ZQS2JRD / ELEGOO model US-EL-SM-Relay. No marketplace
 * artwork, EDA data, or third-party mesh is embedded. The board outline and
 * mounting registration come from the owner's physically fitted unit; visible
 * population is reconstructed from the saved listing gallery. See
 * ELEGOO-4-CHANNEL-RELAY-PROVENANCE.md.
 *
 * Native coordinates follow the listing's top view: X runs along the 72.70 mm
 * relay bank, Y runs from the logic-header edge toward the screw-terminal
 * edge, and Z points through the populated face. The fixture rotates this
 * source 90 degrees clockwise so the screw-terminal bank faces installed +X.
 * Millimetres.
 */

function elegoo_relay_board_size() = [72.70, 51.85];
function elegoo_relay_installed_size() = [51.85, 72.70];
function elegoo_relay_hole_diameter() = 3.00;
function elegoo_relay_hole_centres() = [66.93, 45.03];
function elegoo_relay_installed_hole_centres() = [45.03, 66.93];
function elegoo_relay_installed_terminal_edge() = "+X";
function elegoo_relay_channel_count() = 4;
function elegoo_relay_terminal_count() = 12;
function elegoo_relay_amazon_main_sha256() =
    "a8a405e23244346ee17a98e7b317e86a2b809719e8304e413bd249308405f144";
function elegoo_relay_thingiverse_preview_sha256() =
    "d967bb2e60d35e36d019f55ab48bb20e838cf1b8e9ab65933090c9585f16ca67";

relay_board = elegoo_relay_board_size();
relay_holes = elegoo_relay_hole_centres();
relay_hole_inset = (relay_board - relay_holes) / 2;
relay_board_thickness = 1.60;
relay_epsilon = 0.02;
relay_can_size = [15.25, 19.30, 15.30];
relay_can_x = [4.55, 21.25, 37.95, 54.65];
relay_terminal_x = [3.95, 20.15, 36.35, 52.55];
relay_channel_centre_x = [12.175, 28.875, 45.575, 62.275];

module relay_rounded_rect_2d(size, radius) {
    hull()
        for (x = [radius, size.x - radius])
            for (y = [radius, size.y - radius])
                translate([x, y]) circle(r = radius, $fn = 36);
}

module relay_rounded_prism(origin, size, radius = 0.5) {
    translate(origin)
        linear_extrude(height = size.z)
            relay_rounded_rect_2d(
                [size.x, size.y],
                min(radius, min(size.x, size.y) / 2));
}

module relay_board_text(label, point, size, rotation = 0,
                        height = 0.10, halign = "center") {
    translate([point.x, point.y, relay_board_thickness])
        rotate([0, 0, rotation])
            linear_extrude(height = height)
                text(label, size = size, halign = halign,
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module relay_can_text(label, point, size, rotation = 0) {
    translate([point.x, point.y,
               relay_board_thickness + relay_can_size.z])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.10)
                text(label, size = size, halign = "center",
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module elegoo_relay_pcb() {
    difference() {
        relay_rounded_prism(
            [0, 0, 0],
            [relay_board.x, relay_board.y, relay_board_thickness],
            2.8);

        for (x = [relay_hole_inset.x,
                  relay_board.x - relay_hole_inset.x])
            for (y = [relay_hole_inset.y,
                      relay_board.y - relay_hole_inset.y])
                translate([x, y, -relay_epsilon])
                    cylinder(
                        d = elegoo_relay_hole_diameter(),
                        h = relay_board_thickness + 2 * relay_epsilon,
                        $fn = 36);

        // The photographed board has four isolation slots between the
        // low-voltage driver side and the relay-contact side.
        for (x = relay_channel_centre_x)
            translate([x - 4.3, 19.25, -relay_epsilon])
                cube([8.6, 0.55,
                      relay_board_thickness + 2 * relay_epsilon]);
    }
}

module relay_screw_terminal(index) {
    x = relay_terminal_x[index];
    y = 42.85;
    z = relay_board_thickness;

    difference() {
        relay_rounded_prism([x, y, z], [15.75, 9.00, 9.20], 0.7);

        for (terminal = [0 : 2]) {
            terminal_x = x + 2.80 + terminal * 5.08;

            // Vertical screw well and cable-entry mouth.
            translate([terminal_x, y + 4.25, z + 6.65])
                cylinder(d = 3.55, h = 2.80, $fn = 28);
            translate([terminal_x, relay_board.y + 0.10, z + 4.15])
                rotate([90, 0, 0])
                    cylinder(d = 2.75, h = 2.15, $fn = 28);
        }
    }
}

module relay_can(index) {
    relay_rounded_prism(
        [relay_can_x[index], 21.65, relay_board_thickness],
        relay_can_size, 0.65);

    // Shallow lid step and the two characteristic moulding pips.
    relay_rounded_prism(
        [relay_can_x[index] + 0.35, 22.00,
         relay_board_thickness + relay_can_size.z - 0.20],
        [relay_can_size.x - 0.70, relay_can_size.y - 0.70, 0.20],
        0.50);
    for (x = [relay_can_x[index] + 1.20,
              relay_can_x[index] + relay_can_size.x - 1.20])
        translate([x, 39.55,
                   relay_board_thickness + relay_can_size.z - 0.10])
            cylinder(d = 0.65, h = 0.16, $fn = 16);
}

module relay_pin(position, height = 5.50) {
    translate([position.x - 0.32, position.y - 0.32,
               relay_board_thickness])
        cube([0.64, 0.64, height]);
}

module elegoo_relay_blue() {
    for (channel = [0 : elegoo_relay_channel_count() - 1]) {
        relay_can(channel);
        relay_screw_terminal(channel);
    }

    // Stock blue shunt joining JD-VCC to VCC.
    relay_rounded_prism(
        [65.90, 8.45, relay_board_thickness + 1.10],
        [2.85, 5.10, 4.20], 0.35);
}

module elegoo_relay_dark() {
    for (channel = [0 : elegoo_relay_channel_count() - 1]) {
        centre_x = relay_channel_centre_x[channel];

        // PC817-style optocoupler, relay flyback diode, SOT-23 driver,
        // and the visible paired resistor population.
        relay_rounded_prism(
            [centre_x - 3.25, 10.65, relay_board_thickness],
            [6.50, 4.65, 3.55], 0.35);
        relay_rounded_prism(
            [centre_x - 2.20, 17.70, relay_board_thickness],
            [4.40, 1.85, 1.35], 0.30);
        relay_rounded_prism(
            [centre_x - 1.45, 6.65, relay_board_thickness],
            [2.90, 1.45, 1.10], 0.20);
        for (y = [5.05, 16.10])
            relay_rounded_prism(
                [centre_x - 1.15, y, relay_board_thickness],
                [2.30, 0.95, 0.72], 0.18);
    }

    // Six-pin MCU input header and the separate three-pin power header.
    relay_rounded_prism(
        [32.55, 0.65, relay_board_thickness],
        [15.25, 2.35, 2.30], 0.22);
    relay_rounded_prism(
        [65.85, 7.15, relay_board_thickness],
        [2.35, 7.65, 2.30], 0.22);
}

module relay_slotted_screw(centre) {
    difference() {
        translate([centre.x, centre.y, 10.50])
            cylinder(d = 3.25, h = 0.42, $fn = 32);
        translate([centre.x - 1.25, centre.y - 0.18, 10.78])
            cube([2.50, 0.36, 0.25]);
    }
}

module elegoo_relay_metal() {
    // Twelve plated screw heads and the contact plates visible through the
    // cable mouths.
    for (channel = [0 : elegoo_relay_channel_count() - 1])
        for (terminal = [0 : 2]) {
            x = relay_terminal_x[channel] + 2.80 + terminal * 5.08;
            relay_slotted_screw([x, 47.10]);
            translate([x - 1.30, 50.72, 5.10])
                cube([2.60, 0.55, 1.35]);
        }

    // Six MCU pins, three relay-power pins, and four plated mounting rings.
    for (pin = [0 : 5])
        relay_pin([33.82 + pin * 2.54, 1.82]);
    for (pin = [0 : 2])
        relay_pin([67.02, 8.42 + pin * 2.54]);

    for (x = [relay_hole_inset.x,
              relay_board.x - relay_hole_inset.x])
        for (y = [relay_hole_inset.y,
                  relay_board.y - relay_hole_inset.y])
            translate([x, y, relay_board_thickness - 0.03])
                difference() {
                    cylinder(d = 4.55, h = 0.08, $fn = 36);
                    translate([0, 0, -relay_epsilon])
                        cylinder(
                            d = elegoo_relay_hole_diameter(),
                            h = 0.08 + 2 * relay_epsilon, $fn = 36);
                }
}

module elegoo_relay_led() {
    for (x = relay_channel_centre_x)
        relay_rounded_prism(
            [x - 0.90, 19.55, relay_board_thickness],
            [1.80, 0.95, 0.75], 0.22);

    // Power indicator beside the JD-VCC/VCC header.
    relay_rounded_prism(
        [62.25, 7.10, relay_board_thickness],
        [1.85, 1.00, 0.78], 0.22);
}

module elegoo_relay_silkscreen() {
    // Board identification and channel/interface labels.
    relay_board_text("4 Relay Module", [1.60, 25.0], 2.00, 90);
    for (channel = [0 : elegoo_relay_channel_count() - 1]) {
        centre_x = relay_channel_centre_x[channel];
        relay_board_text(
            str("K", channel + 1), [centre_x, 20.55], 1.05);
        relay_board_text(
            channel == 0 ? "NC  C  NO" : "NC C NO",
            [centre_x, 41.70], 0.82);

        relay_can_text(
            "SRD-05VDC", [centre_x, 33.80], 1.28);
        relay_can_text(
            "SL-C", [centre_x, 31.75], 1.10);
        relay_can_text(
            "10A 250VAC", [centre_x, 29.80], 0.76);
    }

    for (pin = [0 : 5])
        relay_board_text(
            ["IN1", "IN2", "IN3", "IN4", "GND", "VCC"][pin],
            [33.82 + pin * 2.54, 3.65], 0.72, 90);

    relay_board_text("JD-VCC", [63.95, 12.30], 0.78, 90);
    relay_board_text("VCC", [63.95, 7.95], 0.78, 90);
    relay_board_text("PWR", [60.85, 7.60], 0.72, 90);
    relay_board_text(
        "LOW LEVEL TRIGGER", [37.0, 8.65], 0.90);
}

module elegoo_relay_complete() {
    color("#0d6f9f") elegoo_relay_pcb();
    color("#1688c5") elegoo_relay_blue();
    color("#15191d") elegoo_relay_dark();
    color("#c5c9cc") elegoo_relay_metal();
    color("#d72828") elegoo_relay_led();
    color("#eef2ed") elegoo_relay_silkscreen();
}
