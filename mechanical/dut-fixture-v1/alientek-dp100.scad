/*
 * ALIENTEK DP100 compact programmable DC power supply
 *
 * Original, source-native reconstruction of Amazon ASIN B0CWRG6YFM.
 * No external mesh, listing image, manual artwork, or manufacturer CAD is
 * redistributed.
 *
 * Fit contract:
 *   installed enclosure: 94.60 x 62.20 x 17.20 mm
 *   published overall:   100.40 x 62.20 x 17.20 mm
 *   banana projection:   5.80 mm from the enclosure's -X edge
 *   orientation:         banana outputs -X, USB ports +X, controls -Y
 *
 * Preserved reference hashes:
 *   d1cc4a01bcb721d4008ab76b5ed69d7946b5a39c68044a902c942d604a63ae0f
 *   8878f9aa3be219964c41ad3a4e679526bea54946a262fc61f35ed965d7e5f97b
 *   b159077910e492e4b89ae799d4b1a33a58099f083935db80fc7cc7690488ad0f
 */

dp100_body = [94.60, 62.20, 17.20];
dp100_published_length = 100.40;
dp100_banana_projection = dp100_published_length - dp100_body.x;
dp100_corner_radius = 5.25;
dp100_front_run = 17.0;
dp100_front_low_z = 10.20;
dp100_front_angle = atan(
    (dp100_body.z - dp100_front_low_z) / dp100_front_run);
dp100_front_slope_length = sqrt(
    dp100_front_run * dp100_front_run +
    (dp100_body.z - dp100_front_low_z) *
    (dp100_body.z - dp100_front_low_z));
dp100_epsilon = 0.04;

function alientek_dp100_body_size() = dp100_body;
function alientek_dp100_overall_size() =
    [dp100_published_length, dp100_body.y, dp100_body.z];
function alientek_dp100_banana_projection() = dp100_banana_projection;
function alientek_dp100_banana_edge() = "-X";
function alientek_dp100_usb_edge() = "+X";
function alientek_dp100_controls_edge() = "-Y";
function alientek_dp100_amazon_reference_sha256() =
    "d1cc4a01bcb721d4008ab76b5ed69d7946b5a39c68044a902c942d604a63ae0f";
function alientek_dp100_manual_sha256() =
    "8878f9aa3be219964c41ad3a4e679526bea54946a262fc61f35ed965d7e5f97b";
function alientek_dp100_manual_appearance_sha256() =
    "b159077910e492e4b89ae799d4b1a33a58099f083935db80fc7cc7690488ad0f";

module dp100_rounded_prism(position, size, radius) {
    translate(position)
        linear_extrude(height = size.z)
            offset(r = radius)
                offset(delta = -radius)
                    square([size.x, size.y]);
}

// Removes the volume above a plane that rises from 10.2 mm at the -Y edge
// to the 17.2 mm top at Y=17 mm. The result is the listing's characteristic
// chamfered control face without changing the measured plan-view body.
module dp100_front_bevel_cut() {
    x0 = -1;
    x1 = dp100_body.x + 1;
    y0 = -1;
    y1 = dp100_front_run;
    z0 = dp100_front_low_z -
         (dp100_body.z - dp100_front_low_z) / dp100_front_run;
    z1 = dp100_body.z;
    z2 = dp100_body.z + 2;

    polyhedron(
        points = [
            [x0, y0, z0], [x1, y0, z0],
            [x1, y1, z1], [x0, y1, z1],
            [x0, y0, z2], [x1, y0, z2],
            [x1, y1, z2], [x0, y1, z2]
        ],
        faces = [
            [0, 1, 2, 3],
            [4, 7, 6, 5],
            [0, 4, 5, 1],
            [1, 5, 6, 2],
            [2, 6, 7, 3],
            [3, 7, 4, 0]
        ],
        convexity = 4);
}

module dp100_front_datum(z_offset = 0) {
    translate([0, 0, dp100_front_low_z + z_offset])
        rotate([dp100_front_angle, 0, 0])
            children();
}

module dp100_front_rounded_rect(position, size, radius, height = 0.20) {
    dp100_front_datum()
        translate([position.x, position.y, position.z])
            linear_extrude(height = height)
                offset(r = radius)
                    offset(delta = -radius)
                        square([size.x, size.y]);
}

module dp100_front_text(label, point, size, height = 0.07,
                        halign = "center", rotation = 0,
                        z_offset = 0.24) {
    dp100_front_datum(z_offset)
        translate([point.x, point.y, 0])
            rotate([0, 0, rotation])
                linear_extrude(height = height)
                    text(label, size = size, halign = halign,
                         valign = "center",
                         font = "Liberation Sans:style=Bold",
                         $fn = 8);
}

module dp100_banana_cylinder(y, diameter, x_start, length) {
    translate([x_start, y, dp100_body.z / 2])
        rotate([0, 90, 0])
            cylinder(d = diameter, h = length, $fn = 44);
}

module dp100_usb_a_frame() {
    difference() {
        translate([dp100_body.x - 0.22, 12.35, 5.10])
            cube([0.22, 13.10, 7.00]);
        translate([dp100_body.x - 0.30, 13.90, 6.25])
            cube([0.38, 10.00, 4.70]);
    }
}

module dp100_usb_c_shape(x_start, length, diameter = 4.10,
                         centre_distance = 3.60) {
    translate([x_start, 44.90, 8.60])
        rotate([0, 90, 0])
            hull() {
                translate([0, -centre_distance / 2, 0])
                    cylinder(d = diameter, h = length, $fn = 32);
                translate([0, centre_distance / 2, 0])
                    cylinder(d = diameter, h = length, $fn = 32);
            }
}

module dp100_usb_c_frame() {
    difference() {
        dp100_usb_c_shape(dp100_body.x - 0.22, 0.22, 4.30, 3.70);
        dp100_usb_c_shape(dp100_body.x - 0.30, 0.38, 2.35, 3.45);
    }
}

module alientek_dp100_shell() {
    difference() {
        dp100_rounded_prism(
            [0, 0, 0], dp100_body, dp100_corner_radius);
        dp100_front_bevel_cut();

        // A shallow split seam wraps the enclosure just above its base.
        difference() {
            translate([-dp100_epsilon, -dp100_epsilon, 2.55])
                linear_extrude(height = 0.34)
                    offset(r = dp100_corner_radius + dp100_epsilon)
                        offset(delta = -dp100_corner_radius)
                            square([
                                dp100_body.x + 2 * dp100_epsilon,
                                dp100_body.y + 2 * dp100_epsilon
                            ]);
            translate([0.45, 0.45, 2.45])
                linear_extrude(height = 0.54)
                    offset(r = dp100_corner_radius - 0.45)
                        offset(delta = -(dp100_corner_radius - 0.45))
                            square([
                                dp100_body.x - 0.90,
                                dp100_body.y - 0.90
                            ]);
        }

        // Connector recesses are cut into the two short enclosure edges.
        for (y = [18.20, 44.00])
            dp100_banana_cylinder(y, 8.80, -0.60, 1.25);
        translate([dp100_body.x - 0.70, 13.45, 5.65])
            cube([0.85, 11.00, 5.90]);
        dp100_usb_c_shape(dp100_body.x - 0.70, 0.85, 3.80, 3.55);

        // Seven cooling slots on the rear side reproduce the manual's vent
        // detail while keeping the top cover visually uncluttered.
        for (x = [34 : 4.5 : 61])
            translate([x, dp100_body.y - 0.55, 5.10])
                cube([2.00, 0.80, 7.00]);
    }
}

module alientek_dp100_dark() {
    // Inset control panel and display bezel.
    dp100_front_rounded_rect(
        [2.80, 1.30, 0], [89.00, 15.60], 2.50, 0.16);
    dp100_front_rounded_rect(
        [5.20, 2.50, 0.13], [29.50, 12.20], 1.35, 0.22);

    // Black negative ring, port interiors, seam, and cooling slots.
    dp100_banana_cylinder(44.00, 9.60, -3.55, 3.75);
    translate([dp100_body.x - 0.31, 13.90, 6.25])
        cube([0.31, 10.00, 4.70]);
    dp100_usb_c_shape(dp100_body.x - 0.31, 0.31, 2.35, 3.45);

    for (x = [34 : 4.5 : 61])
        translate([x, dp100_body.y - 0.38, 5.20])
            cube([2.00, 0.38, 6.80]);

    difference() {
        dp100_rounded_prism(
            [0, 0, 2.58],
            [dp100_body.x, dp100_body.y, 0.25],
            dp100_corner_radius);
        dp100_rounded_prism(
            [0.42, 0.42, 2.53],
            [dp100_body.x - 0.84, dp100_body.y - 0.84, 0.35],
            dp100_corner_radius - 0.42);
    }

    // Banana and USB contact cavities.
    dp100_banana_cylinder(
        18.20, 3.15, -dp100_banana_projection,
        dp100_banana_projection);
    dp100_banana_cylinder(
        44.00, 3.15, -dp100_banana_projection,
        dp100_banana_projection);
}

module alientek_dp100_controls() {
    // Three raised gray keys and the partially exposed transverse jog wheel.
    for (x = [44.50, 57.50, 70.50])
        dp100_front_datum(0.15)
            translate([x, 8.60, 0])
                cylinder(d = 7.70, h = 0.95, $fn = 40);

    intersection() {
        dp100_front_datum(0.20)
            translate([85.80, 5.00, 4.60])
                rotate([-90, 0, 0])
                    cylinder(d = 10.20, h = 7.60, $fn = 40);
        translate([79.0, -0.2, 8.0])
            cube([15.6, 18.0, dp100_body.z - 8.0]);
    }
}

module alientek_dp100_screen() {
    dp100_front_rounded_rect(
        [7.20, 3.55, 0.34], [25.50, 9.95], 0.65, 0.16);

    // Simple colored UI bands make the active 0.96-inch 160 x 80 IPS panel
    // read correctly at assembly-view scale without copying listing artwork.
    dp100_front_rounded_rect(
        [8.10, 4.40, 0.51], [5.00, 8.25], 0.18, 0.04);
    dp100_front_rounded_rect(
        [14.00, 10.30, 0.51], [17.70, 2.35], 0.18, 0.04);
}

module alientek_dp100_accent() {
    // Positive output insulation and the characteristic red screen/status cue.
    dp100_banana_cylinder(18.20, 9.60, -3.55, 3.75);
    dp100_front_rounded_rect(
        [14.00, 4.40, 0.56], [17.70, 1.70], 0.15, 0.04);
}

module alientek_dp100_metal() {
    // Gold-plated 4 mm banana interfaces. Their 5.8 mm projection reconciles
    // the 94.6 mm measured body with the official 100.4 mm overall length.
    for (y = [18.20, 44.00])
        difference() {
            dp100_banana_cylinder(
                y, 6.40, -dp100_banana_projection,
                dp100_banana_projection);
            dp100_banana_cylinder(
                y, 3.15, -dp100_banana_projection - dp100_epsilon,
                dp100_banana_projection + 2 * dp100_epsilon);
        }

    dp100_usb_a_frame();
    dp100_usb_c_frame();

    // A thin silver index on the adjustment roller.
    intersection() {
        dp100_front_datum(0.20)
            translate([85.35, 4.30, 8.90])
                cube([0.90, 9.00, 0.20]);
        cube(dp100_body);
    }
}

module alientek_dp100_markings() {
    dp100_front_text("ALIENTEK", [6.30, 8.60], 1.25,
                     halign = "center", rotation = 90);
    dp100_front_text("30.00V", [23.10, 11.30], 1.50,
                     z_offset = 0.73);
    dp100_front_text("3.000A", [23.10, 8.25], 1.35,
                     z_offset = 0.73);
    dp100_front_text("100.0W", [23.10, 5.35], 1.25,
                     z_offset = 0.73);
    dp100_front_text("DP100", [38.50, 14.25], 1.35);
    dp100_front_text("M", [44.50, 8.60], 2.10,
                     z_offset = 1.16);
    dp100_front_text("SET", [57.50, 8.60], 1.35,
                     z_offset = 1.16);
    dp100_front_text("O", [70.50, 8.60], 1.85,
                     z_offset = 1.16);

}

module alientek_dp100_complete() {
    color("#262a2e") alientek_dp100_shell();
    color("#090b0e") alientek_dp100_dark();
    color("#3d4248") alientek_dp100_controls();
    color("#123e51") alientek_dp100_screen();
    color("#c9342f") alientek_dp100_accent();
    color("#c89b3c") alientek_dp100_metal();
    color("#e8ece7") alientek_dp100_markings();
}
