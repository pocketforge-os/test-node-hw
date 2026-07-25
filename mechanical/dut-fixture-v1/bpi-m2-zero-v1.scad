/*
 * Banana Pi BPI-M2 Zero V1.0 presentation model.
 *
 * This is an original, source-native reconstruction of the populated board in
 * the PocketForge fixture. No third-party mesh or DXF geometry is embedded.
 * Interface dimensions come from owner caliper measurements; connector and
 * component registration was cross-checked against Sinovoip's public V1.0
 * top/bottom DXF and the owner's 2026-07-18 fixture photograph. See
 * BPI-M2-ZERO-PROVENANCE.md for immutable reference hashes and URLs.
 *
 * Local coordinates: X across the 29.90 mm short axis, Y along the 65.00 mm
 * long axis from CSI end to antenna end, Z upward from the PCB underside.
 * Values are millimetres.
 */

function bpi_m2_zero_board_size() = [29.90, 65.00];
function bpi_m2_zero_hole_diameter() = 2.60;
function bpi_m2_zero_hole_centres() = [23.00, 58.36];
function bpi_m2_zero_board_thickness() = 1.60;
function bpi_m2_zero_top_dxf_sha256() =
    "7adbb58ab77addc91a5fc2ee84df689e5db62e7ed2b9b2b12b166684b1632833";
function bpi_m2_zero_bottom_dxf_sha256() =
    "9d0815fd9bdb3cb5dd790d8dda1eb132a36802b586dc5eab696c79cea3dc592a";

bpi_board = bpi_m2_zero_board_size();
bpi_hole_pitch = bpi_m2_zero_hole_centres();
bpi_hole_d = bpi_m2_zero_hole_diameter();
bpi_pcb_t = bpi_m2_zero_board_thickness();
bpi_corner_radius = 3.0;
bpi_epsilon = 0.02;

module bpi_rounded_rect_2d(size, radius) {
    hull()
        for (x = [radius, size.x - radius])
            for (y = [radius, size.y - radius])
                translate([x, y]) circle(r = radius, $fn = 32);
}

module bpi_rounded_prism(origin, size, radius = 0.35) {
    translate(origin)
        linear_extrude(height = size.z)
            bpi_rounded_rect_2d([size.x, size.y],
                               min(radius, min(size.x, size.y) / 2));
}

module bpi_chip(origin, size, height, radius = 0.45) {
    bpi_rounded_prism([origin.x, origin.y, bpi_pcb_t],
                      [size.x, size.y, height], radius);
}

module bpi_pin_grid_plastic() {
    // The installed node has a populated 2x20 2.54 mm header. Individual
    // insulators retain the characteristic castellated black edge in close-up.
    for (column = [0 : 1])
        for (row = [0 : 19])
            bpi_rounded_prism(
                [24.20 + column * 2.54, 7.10 + row * 2.54, bpi_pcb_t],
                [2.25, 2.25, 2.45], 0.18);
}

module bpi_pin_grid_metal() {
    for (column = [0 : 1])
        for (row = [0 : 19])
            translate([25.325 + column * 2.54,
                       8.225 + row * 2.54,
                       bpi_pcb_t + 0.15])
                cube([0.64, 0.64, 6.25], center = true);
}

module bpi_m2_zero_pcb(
    board_size = bpi_m2_zero_board_size(),
    hole_centres = bpi_m2_zero_hole_centres(),
    hole_diameter = bpi_m2_zero_hole_diameter()
) {
    assert(board_size == bpi_m2_zero_board_size(),
           str("BPI model scale/orientation changed: ", board_size));
    assert(hole_centres == bpi_m2_zero_hole_centres(),
           str("BPI mounting registration changed: ", hole_centres));
    assert(hole_diameter == bpi_m2_zero_hole_diameter(),
           str("BPI mounting-hole diameter changed: ", hole_diameter));

    hole_margin = (board_size - hole_centres) / 2;
    difference() {
        linear_extrude(height = bpi_pcb_t)
            bpi_rounded_rect_2d(board_size, bpi_corner_radius);
        for (x = [hole_margin.x, hole_margin.x + hole_centres.x])
            for (y = [hole_margin.y, hole_margin.y + hole_centres.y])
                translate([x, y, -bpi_epsilon])
                    cylinder(d = hole_diameter,
                             h = bpi_pcb_t + 2 * bpi_epsilon, $fn = 32);
    }
}

module bpi_m2_zero_dark_components() {
    // Allwinner H2+ and the adjacent DDR3 package match the PocketForge node.
    bpi_chip([3.80, 18.25], [13.70, 13.70], 1.15, 0.55);
    bpi_chip([5.00, 7.15], [14.70, 7.40], 0.95, 0.35);

    // Populated 40-pin header, power/reset switches, and visible SMD bodies.
    bpi_pin_grid_plastic();
    bpi_chip([0.35, 34.45], [3.20, 3.70], 1.45, 0.30);
    bpi_chip([0.35, 27.15], [3.20, 3.70], 1.45, 0.30);
    bpi_chip([18.60, 37.20], [3.40, 4.00], 0.85, 0.25);
    bpi_chip([18.55, 30.85], [3.50, 4.10], 0.85, 0.25);
    bpi_chip([17.85, 17.15], [4.30, 4.65], 0.95, 0.25);
    bpi_chip([4.65, 56.00], [4.90, 3.20], 0.80, 0.25);

    for (point = [[3.2, 15.4], [20.4, 24.2], [20.2, 42.7],
                  [3.9, 39.4], [17.6, 57.3], [11.8, 56.4]])
        bpi_chip(point, [2.10, 1.25], 0.55, 0.18);
}

module bpi_m2_zero_metal() {
    // K016/AP6212 radio shield fitted to the photographed board.
    bpi_rounded_prism([4.90, 39.65, bpi_pcb_t],
                      [12.80, 15.90, 1.45], 0.70);

    // Mini-HDMI, USB OTG, and 5 V DC-in receptacles along the long edge.
    bpi_rounded_prism([-1.05, 48.10, bpi_pcb_t],
                      [5.40, 10.20, 3.25], 0.55);
    bpi_rounded_prism([-0.85, 21.30, bpi_pcb_t],
                      [7.45, 5.90, 2.85], 0.45);
    bpi_rounded_prism([-0.85, 7.70, bpi_pcb_t],
                      [7.45, 5.90, 2.85], 0.45);

    // The micro-SD cage is on the back of the board.
    bpi_rounded_prism([13.45, 43.80, -1.25],
                      [14.55, 13.20, 1.25], 0.35);

    // Header pins and the two low-profile edge switches.
    bpi_pin_grid_metal();
    bpi_rounded_prism([-0.20, 35.20, bpi_pcb_t + 0.20],
                      [1.35, 2.20, 0.85], 0.15);
    bpi_rounded_prism([-0.20, 27.90, bpi_pcb_t + 0.20],
                      [1.35, 2.20, 0.85], 0.15);
}

module bpi_m2_zero_gold() {
    hole_margin = (bpi_board - bpi_hole_pitch) / 2;

    // u.FL antenna socket and exposed mounting/header pad rings.
    translate([2.35, 60.05, bpi_pcb_t])
        difference() {
            cylinder(d = 3.25, h = 1.20, $fn = 32);
            translate([0, 0, -bpi_epsilon])
                cylinder(d = 1.35, h = 1.20 + 2 * bpi_epsilon, $fn = 24);
        }
    for (x = [hole_margin.x, hole_margin.x + bpi_hole_pitch.x])
        for (y = [hole_margin.y, hole_margin.y + bpi_hole_pitch.y])
            translate([x, y, bpi_pcb_t])
                difference() {
                    cylinder(d = 4.10, h = 0.08, $fn = 32);
                    translate([0, 0, -bpi_epsilon])
                        cylinder(d = bpi_hole_d,
                                 h = 0.08 + 2 * bpi_epsilon, $fn = 32);
                }
}

module bpi_silk_text(label, point, size, z, rotation = 90) {
    translate([point.x, point.y, z])
        linear_extrude(height = 0.10)
            rotate(rotation)
                text(label, size = size,
                     font = "Liberation Sans:style=Bold");
}

module bpi_m2_zero_silkscreen() {
    silk_z = bpi_pcb_t + 0.025;

    // White CSI FFC body at the short edge.
    bpi_rounded_prism([5.00, -0.55, bpi_pcb_t],
                      [16.80, 4.30, 2.10], 0.30);

    // Board and connector markings present in the manufacturer V1.0 artwork.
    bpi_silk_text("BPI-M2-ZERO-V1.0", [22.10, 13.20], 0.82, silk_z);
    bpi_silk_text("HDMI", [6.85, 49.00], 0.72, silk_z);
    bpi_silk_text("PWR", [3.75, 35.00], 0.68, silk_z);
    bpi_silk_text("RST", [3.75, 27.80], 0.68, silk_z);
    bpi_silk_text("OTG", [6.80, 22.10], 0.68, silk_z);
    bpi_silk_text("DC IN", [6.80, 7.85], 0.68, silk_z);
    bpi_silk_text("CSI", [6.25, 4.25], 0.72, silk_z, 0);
    bpi_silk_text("1", [22.70, 57.65], 0.72, silk_z, 0);
    bpi_silk_text("40", [21.70, 5.05], 0.72, silk_z, 0);

    // Package markings make the installed H2+/K016 population recognizable.
    bpi_silk_text("H2+", [7.50, 23.00], 2.35,
                  bpi_pcb_t + 1.15 + 0.03, 0);
    bpi_silk_text("K016", [6.55, 46.25], 1.75,
                  bpi_pcb_t + 1.45 + 0.03, 0);
}

module bpi_m2_zero_complete() {
    color("#1769a8") bpi_m2_zero_pcb();
    color("#171a1e") bpi_m2_zero_dark_components();
    color("#b7bcc2") bpi_m2_zero_metal();
    color("#d9aa32") bpi_m2_zero_gold();
    color("#e9ece6") bpi_m2_zero_silkscreen();
}
