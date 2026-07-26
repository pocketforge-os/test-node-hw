/*
 * Smays microb-hub-8152 powered OTG/Ethernet hub
 *
 * Original, source-native reconstruction of Amazon ASIN B00L32UUJK,
 * model SMAYS-ETHERNET-ADAPTOR-HUB. No marketplace artwork or third-party
 * geometry is redistributed.
 *
 * Native coordinates match the installed fixture pose: RJ45 opens toward -X,
 * the fixed micro-USB OTG lead exits +X, three USB-A ports open toward +Y,
 * the 3.5 mm 5 V DC jack opens toward -Y, and Z rises from the underside.
 *
 * Preserved reference hashes:
 *   c5600a55adcf666a92c37a2af2c99cc611d47b4fa8738257b04a655e0b69478f
 *   35268f4c3e4f45a74d5b010440570d1ead0b20dd9a472ae11d9cfb2a803fb16
 *   01ecb407d5862a442ac77eb52c60763db44b5067d2c55e2e0d08fc6aed7d51e5
 */

smays_body = [105.07, 24.0, 15.0];
smays_usb_x = [24.0, 47.0, 70.0];
smays_usb_size = [13.4, 5.5];
smays_dc_x = 88.0;
smays_epsilon = 0.04;

function smays_microb_hub_body_size() = smays_body;
function smays_microb_hub_usb_port_count() = 3;
function smays_microb_hub_usb_edge() = "+Y";
function smays_microb_hub_rj45_edge() = "-X";
function smays_microb_hub_otg_edge() = "+X";
function smays_microb_hub_dc_edge() = "-Y";
function smays_microb_hub_dc_exit_x() = smays_dc_x;
function smays_microb_hub_dc_diameter() = 3.5;
function smays_microb_hub_otg_cable_length() = 250.0;
function smays_microb_hub_owner_photo_sha256() =
    "01ecb407d5862a442ac77eb52c60763db44b5067d2c55e2e0d08fc6aed7d51e5";
function smays_microb_hub_hero_sha256() =
    "c5600a55adcf666a92c37a2af2c99cc611d47b4fa8738257b04a655e0b69478f";
function smays_microb_hub_dimension_sha256() =
    "35268f4c3e4f45a74d5b010440570d1ead0b20dd9a472ae11d9cfb2a803fb16";

module smays_rounded_rect_2d(size, radius) {
    hull()
        for (x = [radius, size.x - radius])
            for (y = [radius, size.y - radius])
                translate([x, y]) circle(r = radius, $fn = 32);
}

module smays_rounded_prism(origin, size, radius) {
    translate(origin)
        linear_extrude(height = size.z)
            smays_rounded_rect_2d(
                [size.x, size.y],
                min(radius, min(size.x, size.y) / 2));
}

module smays_tube_path(points, diameter, facets = 20) {
    for (i = [0 : len(points) - 2])
        hull()
            for (point = [points[i], points[i + 1]])
                translate(point) sphere(d = diameter, $fn = facets);
}

module smays_top_text(label, point, size, rotation = 0) {
    translate([point.x, point.y, smays_body.z - 0.01])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.09)
                text(label, size = size, halign = "center",
                     valign = "center",
                     font = "Liberation Serif:style=Regular",
                     $fn = 8);
}

module smays_microb_hub_body() {
    // The measured body is wider than inconsistent catalog metadata; its
    // shallow chamfered crown matches the owner and listing photographs.
    hull() {
        smays_rounded_prism([0, 0, 0],
                            [smays_body.x, smays_body.y, 0.40], 2.5);
        smays_rounded_prism([0.85, 1.05, smays_body.z - 0.40],
                            [smays_body.x - 1.70,
                             smays_body.y - 2.10, 0.40], 1.7);
    }
}

module smays_microb_hub_shell() {
    smays_microb_hub_body();

    // Fixed OTG lead and molded strain relief at +X.
    smays_rounded_prism(
        [smays_body.x - 0.25, smays_body.y / 2 - 3.1, 4.3],
        [6.0, 6.2, 6.4], 1.8);
    smays_tube_path([
        [smays_body.x + 4.8, smays_body.y / 2, 7.5],
        [smays_body.x + 13.0, smays_body.y / 2 + 0.7, 7.7],
        [smays_body.x + 19.0, smays_body.y / 2 + 3.0, 8.1],
        [smays_body.x + 24.0, smays_body.y / 2 + 6.0, 8.4]
    ], 3.2);

    // The owner's installed DC lead climbs immediately out of the six
    // millimetre inter-hub gap, then crosses above the black hub. Capturing
    // that three-dimensional arch is the important rewiring constraint.
    smays_tube_path([
        [smays_dc_x, 0.0, 7.5],
        [smays_dc_x, -3.8, 14.0],
        [smays_dc_x + 4.0, -10.0, 17.0],
        [smays_dc_x + 12.0, -17.0, 18.0]
    ], 3.2);
    smays_tube_path([
        [smays_dc_x, -0.8, 8.3],
        [smays_dc_x, -3.8, 14.0]
    ], 6.0);
}

module smays_microb_hub_dark() {
    // Three downstream USB recesses.
    for (x = smays_usb_x)
        translate([x, smays_body.y - 0.55, 4.2])
            cube([smays_usb_size.x, 0.65, smays_usb_size.y]);

    // RJ45 cavity and 3.5 mm DC jack.
    translate([-0.12, 5.05, 3.0])
        cube([0.72, 13.9, 8.9]);
    translate([smays_dc_x, -0.18, 7.5])
        rotate([-90, 0, 0])
            difference() {
                cylinder(d = 5.4, h = 0.70, $fn = 30);
                translate([0, 0, -smays_epsilon])
                    cylinder(d = 3.5, h = 0.70 + 2 * smays_epsilon,
                             $fn = 24);
            }

    // Case seam.
    translate([2.0, -0.02, 1.00])
        cube([smays_body.x - 4.0, 0.22, 0.25]);
}

module smays_microb_hub_metal() {
    for (x = smays_usb_x)
        translate([x + 0.55, smays_body.y - 0.18, 4.65])
            difference() {
                cube([12.3, 0.40, 4.6]);
                translate([0.65, -smays_epsilon, 0.65])
                    cube([11.0, 0.40 + 2 * smays_epsilon, 3.3]);
            }

    // RJ45 shield/bezel and visible contact row.
    translate([-0.18, 4.45, 2.45])
        difference() {
            cube([0.50, 15.1, 10.0]);
            translate([-smays_epsilon, 1.10, 1.15])
                cube([0.50 + 2 * smays_epsilon, 12.9, 7.7]);
        }
    for (y = [7.2 : 1.35 : 16.65])
        translate([-0.25, y, 4.2])
            cube([0.35, 0.45, 2.2]);
}

module smays_microb_hub_led() {
    for (x = smays_usb_x)
        translate([x + smays_usb_size.x / 2,
                   smays_body.y + 0.02, 3.45])
            rotate([90, 0, 0])
                cylinder(d = 1.0, h = 0.30, $fn = 18);
}

module smays_microb_hub_markings() {
    smays_top_text("SMAYS", [54.0, 12.2], 7.2, 180);
    translate([smays_dc_x + 6.0, 0.06, 9.0])
        rotate([90, 0, 0])
            linear_extrude(height = 0.08)
                text("DC5V", size = 1.8, halign = "center",
                     valign = "center",
                     font = "Liberation Sans:style=Regular");
}

module smays_microb_hub_complete() {
    color("#eceeec") smays_microb_hub_shell();
    color("#171a1d") smays_microb_hub_dark();
    color("#9ca4a8") smays_microb_hub_metal();
    color("#41c06f") smays_microb_hub_led();
    color("#7b7f81") smays_microb_hub_markings();
}
