/*
 * Ceksezx MTSD001 dual-MOSFET trigger switch module
 *
 * Original, source-native reconstruction of Amazon ASIN B0FMJH3DML.
 * No marketplace artwork, EDA file, or third-party geometry is redistributed.
 *
 * Native coordinates follow the listing top view:
 *   PCB: 34.00 x 17.00 x 1.60 mm
 *   holes: two clipped 2.20 mm bores on the -X control edge
 *   terminal bank: +X
 *   control pads: -X
 *   maximum populated height: 12.00 mm
 *
 * The fixture rotates this source 180 degrees and centres it inside the
 * original 35 x 18 mm analytical envelope. This preserves the printed
 * standoff centres while placing the photographed terminal bank at -X.
 *
 * Preserved reference hashes:
 *   42a2bc3a51587a51649d885db1ae87d65b1166c204ddd6e5e669cb8f76c5fd69
 *   6706f3e1594e2b63a8366370717503e2b09ffabacd3650f80048e746d8538fc7
 *   cf2419bc0a5a33edcec808d35592dc417749536ee2e8cc67885f74a656c9e2a6
 */

mtsd001_board = [34.00, 17.00];
mtsd001_board_thickness = 1.60;
mtsd001_height = 12.00;
mtsd001_hole_diameter = 2.20;
mtsd001_holes = [[0.70, 15.19], [0.70, 1.81]];
mtsd001_epsilon = 0.04;
mtsd001_terminal_screw_x = [27.45, 31.65];
mtsd001_terminal_screw_y = [4.25, 12.75];

function ceksezx_mtsd001_board_size() = mtsd001_board;
function ceksezx_mtsd001_board_thickness() = mtsd001_board_thickness;
function ceksezx_mtsd001_complete_height() = mtsd001_height;
function ceksezx_mtsd001_hole_diameter() = mtsd001_hole_diameter;
function ceksezx_mtsd001_native_hole_centres() = mtsd001_holes;
function ceksezx_mtsd001_installed_hole_centres(
    analytical_envelope = [35.00, 18.00]) =
    let(inset = (analytical_envelope - mtsd001_board) / 2)
        [for (hole = mtsd001_holes)
            inset + mtsd001_board - hole];
function ceksezx_mtsd001_native_terminal_edge() = "+X";
function ceksezx_mtsd001_installed_terminal_edge() = "-X";
function ceksezx_mtsd001_terminal_count() = 4;
function ceksezx_mtsd001_mosfet_count() = 2;
function ceksezx_mtsd001_amazon_hero_sha256() =
    "42a2bc3a51587a51649d885db1ae87d65b1166c204ddd6e5e669cb8f76c5fd69";
function ceksezx_mtsd001_dimension_view_sha256() =
    "6706f3e1594e2b63a8366370717503e2b09ffabacd3650f80048e746d8538fc7";
function ceksezx_mtsd001_owner_photo_sha256() =
    "cf2419bc0a5a33edcec808d35592dc417749536ee2e8cc67885f74a656c9e2a6";

module mtsd001_rounded_rect_2d(size, radius) {
    hull()
        for (x = [radius, size.x - radius])
            for (y = [radius, size.y - radius])
                translate([x, y]) circle(r = radius, $fn = 28);
}

module mtsd001_rounded_prism(origin, size, radius = 0.25) {
    translate(origin)
        linear_extrude(height = size.z)
            mtsd001_rounded_rect_2d(
                [size.x, size.y],
                min(radius, min(size.x, size.y) / 2));
}

module mtsd001_board_text(label, point, size, rotation = 0,
                          halign = "center") {
    translate([point.x, point.y, mtsd001_board_thickness - 0.01])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.07)
                text(label, size = size, halign = halign,
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module mtsd001_top_text(label, point, z, size, rotation = 0) {
    translate([point.x, point.y, z])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.06)
                text(label, size = size, halign = "center",
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module mtsd001_plated_ring(centre, outside_diameter = 3.55,
                           inside_diameter = mtsd001_hole_diameter) {
    translate([centre.x, centre.y, mtsd001_board_thickness - 0.03])
        intersection() {
            difference() {
                cylinder(d = outside_diameter, h = 0.10, $fn = 32);
                translate([0, 0, -mtsd001_epsilon])
                    cylinder(
                        d = inside_diameter,
                        h = 0.10 + 2 * mtsd001_epsilon, $fn = 28);
            }
            translate([-centre.x, -centre.y, -mtsd001_epsilon])
                cube([mtsd001_board.x, mtsd001_board.y,
                      0.10 + 2 * mtsd001_epsilon]);
        }
}

module mtsd001_terminal_cell(origin) {
    difference() {
        mtsd001_rounded_prism(
            origin, [4.20, 7.55, mtsd001_height -
                     mtsd001_board_thickness], 0.45);

        translate([origin.x + 2.10, origin.y + 3.75,
                   mtsd001_height - 3.15])
            cylinder(d = 3.25, h = 3.35, $fn = 28);

        // Wire-entry mouth and the moulded inspection slot visible in the
        // oblique listing views.
        translate([origin.x + 1.10, origin.y - 0.05,
                   mtsd001_board_thickness + 2.65])
            cube([2.00, 1.25, 2.75]);
        translate([origin.x + 1.55, origin.y + 7.05,
                   mtsd001_board_thickness + 4.10])
            cube([1.10, 0.75, 1.75]);
    }
}

module ceksezx_mtsd001_pcb() {
    difference() {
        cube([mtsd001_board.x, mtsd001_board.y,
              mtsd001_board_thickness]);

        for (hole = mtsd001_holes)
            translate([hole.x, hole.y, -mtsd001_epsilon])
                cylinder(
                    d = mtsd001_hole_diameter,
                    h = mtsd001_board_thickness +
                        2 * mtsd001_epsilon, $fn = 32);

        // Six unpopulated J1 control through-holes.
        for (x = [2.35, 5.05])
            for (y = [5.75, 8.50, 11.25])
                translate([x, y, -mtsd001_epsilon])
                    cylinder(
                        d = 1.05,
                        h = mtsd001_board_thickness +
                            2 * mtsd001_epsilon, $fn = 24);
    }
}

module ceksezx_mtsd001_blue() {
    // The photographed terminal bank is a compact 2 x 2 set of joined cells.
    for (x = [25.35, 29.55])
        for (y = [0.45, 9.00])
            mtsd001_terminal_cell(
                [x, y, mtsd001_board_thickness]);

    // Shallow blue bridge rails join the cells at the board edge.
    translate([25.20, 0.35, mtsd001_board_thickness])
        cube([8.80, 0.55, 2.10]);
    translate([25.20, 16.10, mtsd001_board_thickness])
        cube([8.80, 0.55, 2.10]);
}

module mtsd001_mosfet_body(y) {
    // DPAK-class AOD4184 body and the characteristic moulded circular pip.
    mtsd001_rounded_prism(
        [16.35, y, mtsd001_board_thickness],
        [7.55, 6.05, 2.40], 0.42);
    translate([20.10, y + 3.00,
               mtsd001_board_thickness + 2.36])
        cylinder(d = 0.55, h = 0.10, $fn = 16);
}

module ceksezx_mtsd001_dark() {
    mtsd001_mosfet_body(1.50);
    mtsd001_mosfet_body(9.45);

    // R3/R1 gate network, R2, and the small driver/passive population.
    for (part = [
        [8.05, 13.40, 2.15, 1.05, 0.76],
        [10.85, 13.40, 2.15, 1.05, 0.76],
        [9.10, 8.00, 2.70, 1.20, 0.82],
        [13.25, 12.60, 1.75, 1.15, 0.92],
        [13.25, 3.25, 1.75, 1.15, 0.92]
    ])
        mtsd001_rounded_prism(
            [part[0], part[1], mtsd001_board_thickness],
            [part[2], part[3], part[4]], 0.15);
}

module mtsd001_slotted_screw(centre) {
    difference() {
        translate([centre.x, centre.y, mtsd001_height - 0.36])
            cylinder(d = 3.05, h = 0.36, $fn = 30);
        translate([centre.x - 1.15, centre.y - 0.16,
                   mtsd001_height - 0.08])
            cube([2.30, 0.32, 0.20]);
    }
}

module mtsd001_mosfet_metal(y) {
    // Three gull-wing leads, source tab, and the bright exposed drain tab.
    for (pin_y = [y + 0.75, y + 3.00, y + 5.25])
        translate([15.10, pin_y,
                   mtsd001_board_thickness + 0.15])
            cube([1.85, 0.60, 0.42]);
    translate([23.45, y + 0.55,
               mtsd001_board_thickness + 0.15])
        cube([1.55, 4.95, 0.42]);
    translate([22.75, y + 0.80,
               mtsd001_board_thickness + 2.05])
        cube([1.15, 4.45, 0.35]);
}

module ceksezx_mtsd001_metal() {
    for (hole = mtsd001_holes)
        mtsd001_plated_ring(hole);

    for (x = [2.35, 5.05])
        for (y = [5.75, 8.50, 11.25])
            mtsd001_plated_ring([x, y], 1.75, 1.05);

    mtsd001_mosfet_metal(1.50);
    mtsd001_mosfet_metal(9.45);

    for (x = mtsd001_terminal_screw_x)
        for (y = mtsd001_terminal_screw_y)
            mtsd001_slotted_screw([x, y]);

    // Silver termination caps on the visible resistors/passives.
    for (end = [
        [7.85, 13.40], [10.00, 13.40],
        [10.65, 13.40], [12.80, 13.40],
        [8.90, 8.00], [11.55, 8.00],
        [13.10, 12.60], [14.85, 12.60],
        [13.10, 3.25], [14.85, 3.25]
    ])
        translate([end[0], end[1],
                   mtsd001_board_thickness + 0.18])
            cube([0.35, 1.00, 0.34]);
}

module ceksezx_mtsd001_led() {
    mtsd001_rounded_prism(
        [7.55, 2.35, mtsd001_board_thickness],
        [2.10, 1.15, 0.85], 0.22);
}

module ceksezx_mtsd001_silkscreen() {
    // Control-edge outline, component designators, and terminal identities.
    translate([1.55, 4.55, mtsd001_board_thickness - 0.01])
        difference() {
            cube([4.65, 7.90, 0.07]);
            translate([0.25, 0.25, -mtsd001_epsilon])
                cube([4.15, 7.40, 0.07 + 2 * mtsd001_epsilon]);
        }

    mtsd001_board_text("J1", [2.65, 2.95], 1.05);
    mtsd001_board_text("LED", [6.55, 1.45], 0.88, 90);
    mtsd001_board_text("R3", [8.70, 15.15], 0.82);
    mtsd001_board_text("R1", [11.50, 15.15], 0.82);
    mtsd001_board_text("R2", [9.85, 9.80], 0.82);
    mtsd001_board_text("Q1", [14.55, 12.20], 1.15);
    mtsd001_board_text("Q2", [14.55, 4.70], 1.15);
    mtsd001_board_text("PWM+", [3.85, 13.90], 0.60);
    mtsd001_board_text("GND", [3.85, 3.10], 0.60);
    mtsd001_board_text("OUT-", [27.40, 16.15], 0.54);
    mtsd001_board_text("OUT+", [31.55, 16.15], 0.54);
    mtsd001_board_text("DC-", [27.40, 0.85], 0.58);
    mtsd001_board_text("DC+", [31.55, 0.85], 0.58);

    mtsd001_top_text(
        "PD4184", [19.65, 4.55],
        mtsd001_board_thickness + 2.42, 0.70, 90);
    mtsd001_top_text(
        "GA4D1K", [21.00, 4.55],
        mtsd001_board_thickness + 2.42, 0.58, 90);
    mtsd001_top_text(
        "PD4184", [19.65, 12.45],
        mtsd001_board_thickness + 2.42, 0.70, 90);
    mtsd001_top_text(
        "GA4D1K", [21.00, 12.45],
        mtsd001_board_thickness + 2.42, 0.58, 90);

    // White component-outline cues and the dotted source/drain trace row.
    translate([15.75, 0.95, mtsd001_board_thickness - 0.01])
        cube([8.80, 0.16, 0.07]);
    translate([15.75, 15.90, mtsd001_board_thickness - 0.01])
        cube([8.80, 0.16, 0.07]);
    for (x = [12.50 : 1.25 : 23.75])
        translate([x, 0.62, mtsd001_board_thickness - 0.01])
            cylinder(d = 0.34, h = 0.07, $fn = 12);
}

module ceksezx_mtsd001_complete() {
    color("#0d65a7") ceksezx_mtsd001_pcb();
    color("#177fd0") ceksezx_mtsd001_blue();
    color("#171a1e") ceksezx_mtsd001_dark();
    color("#c4c9cd") ceksezx_mtsd001_metal();
    color("#dce99b") ceksezx_mtsd001_led();
    color("#eef2ed") ceksezx_mtsd001_silkscreen();
}
