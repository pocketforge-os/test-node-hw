/*
 * HiLetgo / Flying-Fish XL6009 boost module
 *
 * Original, source-native reconstruction of Amazon ASIN B07BNHR4HW.
 * No external mesh, EDA file, or listing artwork is redistributed.
 *
 * Fit contract:
 *   PCB: 43.16 x 21.23 x 1.60 mm
 *   holes: two diagonal 3.00 mm bores at [6.50, 18.63] and [36.66, 2.20]
 *   orientation: IN pads on -X; OUT pads on +X
 *   maximum populated height: 14.00 mm
 *
 * Preserved listing-reference hashes:
 *   128d0d2eac3f0d467e77d895d95eb716cdc16737294c689b6d9f0a57f89b3284
 *   4027c0a0f5677449a640507069633a8299516dff8770f56ad484b8fb3ee45e52
 *   53aa07b5b5a19d188791895feee68050200ffec113aa7e6bb2c0419c497a2d4b
 */

xl6009_board = [43.16, 21.23];
xl6009_board_thickness = 1.60;
xl6009_height = 14.00;
xl6009_hole_diameter = 3.00;
xl6009_holes = [[6.50, 18.63], [36.66, 2.20]];
xl6009_epsilon = 0.04;

function hiletgo_xl6009_board_size() = xl6009_board;
function hiletgo_xl6009_board_thickness() = xl6009_board_thickness;
function hiletgo_xl6009_complete_height() = xl6009_height;
function hiletgo_xl6009_hole_diameter() = xl6009_hole_diameter;
function hiletgo_xl6009_hole_centres() = xl6009_holes;
function hiletgo_xl6009_input_edge() = "-X";
function hiletgo_xl6009_output_edge() = "+X";

module xl6009_rounded_prism(position, size, radius) {
    translate(position)
        linear_extrude(height = size.z)
            offset(r = radius)
                offset(delta = -radius)
                    square([size.x, size.y]);
}

module xl6009_board_text(label, point, size, rotation = 0,
                         halign = "center") {
    translate([point.x, point.y, xl6009_board_thickness - 0.01])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.06)
                text(label, size = size, halign = halign,
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module xl6009_top_text(label, point, z, size, rotation = 0) {
    translate([point.x, point.y, z])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.05)
                text(label, size = size, halign = "center",
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module xl6009_electrolytic_crescent(centre) {
    translate([centre.x, centre.y, 13.89])
        intersection() {
            cylinder(d = 7.35, h = 0.06, $fn = 40);
            translate([-3.8, 0, -xl6009_epsilon])
                cube([7.6, 3.8, 0.06 + 2 * xl6009_epsilon]);
        }
}

module hiletgo_xl6009_pcb() {
    difference() {
        cube([xl6009_board.x, xl6009_board.y,
              xl6009_board_thickness]);

        for (hole = xl6009_holes)
            translate([hole.x, hole.y, -xl6009_epsilon])
                cylinder(
                    d = xl6009_hole_diameter,
                    h = xl6009_board_thickness + 2 * xl6009_epsilon,
                    $fn = 36);
    }
}

module hiletgo_xl6009_dark() {
    // 470-marked shielded 47 uH inductor.
    xl6009_rounded_prism(
        [12.55, 4.20, xl6009_board_thickness],
        [9.30, 9.10, 7.35], 0.85);
    xl6009_rounded_prism(
        [13.10, 4.75, xl6009_board_thickness + 7.25],
        [8.20, 8.00, 0.28], 0.70);

    // XL6009E1 TO-263-5L body, SS34-class Schottky diode, and visible
    // feedback/control population from the listing orthographic view.
    xl6009_rounded_prism(
        [23.10, 4.15, xl6009_board_thickness],
        [9.75, 8.15, 3.55], 0.45);
    xl6009_rounded_prism(
        [25.25, 15.10, xl6009_board_thickness],
        [4.75, 2.40, 1.25], 0.28);
    xl6009_rounded_prism(
        [29.35, 12.45, xl6009_board_thickness],
        [3.10, 1.70, 1.10], 0.20);

    for (part = [
        [9.70, 3.00, 2.45, 1.15],
        [20.95, 16.65, 2.10, 1.00],
        [23.55, 16.70, 2.10, 1.00],
        [30.60, 18.00, 2.15, 1.00],
        [33.10, 17.95, 2.15, 1.00],
        [34.35, 4.00, 1.90, 0.95]
    ])
        xl6009_rounded_prism(
            [part[0], part[1], xl6009_board_thickness],
            [part[2], part[3], 0.72], 0.14);

    // The photographed aluminum electrolytics have a black polarity crescent
    // folded over each scored top.
    xl6009_electrolytic_crescent([7.75, 7.40]);
    xl6009_electrolytic_crescent([36.05, 13.50]);
}

module hiletgo_xl6009_adjuster() {
    // Blue 3296-style W103 multi-turn trimmer.
    xl6009_rounded_prism(
        [12.15, 13.55, xl6009_board_thickness],
        [7.15, 7.25, 9.15], 0.35);
    xl6009_rounded_prism(
        [12.45, 19.25, xl6009_board_thickness + 6.70],
        [3.15, 1.50, 2.20], 0.25);
}

module xl6009_plated_ring(centre) {
    translate([centre.x, centre.y,
               xl6009_board_thickness - 0.03])
        intersection() {
            difference() {
                cylinder(d = 5.15, h = 0.10, $fn = 40);
                translate([0, 0, -xl6009_epsilon])
                    cylinder(
                        d = xl6009_hole_diameter,
                        h = 0.10 + 2 * xl6009_epsilon, $fn = 36);
            }
            // The lower-right annulus is factory-clipped by the board edge.
            translate([-centre.x, -centre.y, -xl6009_epsilon])
                cube([xl6009_board.x, xl6009_board.y,
                      0.10 + 2 * xl6009_epsilon]);
        }
}

module xl6009_electrolytic_can(centre) {
    // White insulating foot plus bare aluminum can. The 12.4 mm can height
    // establishes the listing/manual's 14.0 mm populated height.
    translate([centre.x, centre.y, xl6009_board_thickness])
        cylinder(d = 8.25, h = 0.65, $fn = 44);
    translate([centre.x, centre.y, xl6009_board_thickness + 0.55])
        cylinder(d = 7.75, h = 11.80, $fn = 44);
}

module hiletgo_xl6009_metal() {
    for (hole = xl6009_holes)
        xl6009_plated_ring(hole);

    // Four large edge solder pads: IN+/IN- on -X, OUT+/OUT- on +X.
    for (pad = [
        [0.35, 16.30, 3.05, 3.70],
        [0.35, 0.65, 3.05, 3.70],
        [39.76, 16.30, 3.05, 3.70],
        [39.76, 0.65, 3.05, 3.70]
    ])
        translate([pad[0], pad[1], xl6009_board_thickness - 0.03])
            cube([pad[2], pad[3], 0.10]);

    xl6009_electrolytic_can([7.75, 7.40]);
    xl6009_electrolytic_can([36.05, 13.50]);

    // Five gull-wing leads and the heat-spreader tab of the TO-263 package.
    for (pin = [0 : 4])
        translate([24.00 + pin * 1.68, 2.35,
                   xl6009_board_thickness + 0.10])
            cube([0.62, 2.25, 0.45]);
    translate([25.05, 12.00, xl6009_board_thickness + 0.15])
        cube([5.85, 2.05, 0.35]);

    // Trimmer adjustment screw with a real screwdriver slot.
    difference() {
        translate([14.00, 19.75, xl6009_board_thickness + 8.50])
            cylinder(d = 2.75, h = 1.35, $fn = 32);
        translate([12.85, 19.57, xl6009_board_thickness + 9.62])
            cube([2.30, 0.36, 0.30]);
    }

    // Component terminations give the small passives their photographed
    // silver-ended appearance.
    for (end = [
        [9.45, 3.00], [11.90, 3.00],
        [20.75, 16.65], [22.85, 16.65],
        [23.35, 16.70], [25.45, 16.70],
        [30.40, 18.00], [32.55, 18.00],
        [32.90, 17.95], [35.05, 17.95]
    ])
        translate([end[0], end[1],
                   xl6009_board_thickness + 0.18])
            cube([0.35, 1.00, 0.34]);
}

module hiletgo_xl6009_silkscreen() {
    xl6009_board_text("IN+", [1.45, 14.55], 1.20, 90);
    xl6009_board_text("IN-", [1.45, 6.15], 1.20, 90);
    xl6009_board_text("OUT+", [41.75, 14.10], 1.10, 90);
    xl6009_board_text("OUT-", [41.75, 6.15], 1.10, 90);
    xl6009_board_text(
        "Flying-Fish-XL6009", [27.10, 19.20], 1.00);
    xl6009_board_text("DC-DC  XL6009E1", [22.10, 1.60], 0.85);

    // Board-edge polarity bars and component-outline cues visible in the
    // orthographic listing image.
    for (line = [
        [0.45, 15.55, 3.10, 0.18],
        [0.45, 4.90, 3.10, 0.18],
        [39.60, 15.55, 3.10, 0.18],
        [39.60, 4.90, 3.10, 0.18]
    ])
        translate([line[0], line[1],
                   xl6009_board_thickness - 0.01])
            cube([line[2], line[3], 0.06]);

    xl6009_top_text("470", [17.20, 8.80], 9.13, 1.65);
    xl6009_top_text("XL6009E1", [27.95, 8.25], 5.15, 0.82, 90);
    xl6009_top_text("W103", [15.70, 16.65], 10.75, 0.92, 90);
    xl6009_top_text("220", [7.75, 7.05], 13.95, 0.80);
    xl6009_top_text("100", [36.05, 13.15], 13.95, 0.80);
}

module hiletgo_xl6009_complete() {
    color("#0c559f") hiletgo_xl6009_pcb();
    color("#131820") hiletgo_xl6009_dark();
    color("#176fce") hiletgo_xl6009_adjuster();
    color("#c2c8cd") hiletgo_xl6009_metal();
    color("#eef1eb") hiletgo_xl6009_silkscreen();
}
