/*
 * VIENON Usb-001 ultra-slim four-port USB hub
 *
 * Original, source-native reconstruction of Amazon ASIN B09MLRPTT2.
 * No marketplace artwork or third-party geometry is redistributed.
 *
 * Native coordinates match the installed fixture pose: X is the body length,
 * the four downstream ports open toward -Y, the fixed upstream lead leaves
 * +X, and Z rises from the body underside.
 *
 * Preserved reference hashes:
 *   3c751f1dbf784083af1d7ea2ee700e7ddbccd587d77e17dfada458fb3011dc63
 *   299d28ef6c14c95fc19dbe0de5367313f78e47066a62850ba105745512a0ebe7
 *   f5161ac65919ef52bc03edad6fed35815246ff483af24d3269169fc67b3c423a
 */

vienon_body = [100.0, 30.0, 10.0];
vienon_port_x = [11.0, 34.5, 58.0, 81.5];
vienon_port_size = [14.0, 5.7];
vienon_epsilon = 0.04;

function vienon_usb001_body_size() = vienon_body;
function vienon_usb001_port_count() = 4;
function vienon_usb001_usb3_port_count() = 1;
function vienon_usb001_usb2_port_count() = 3;
function vienon_usb001_port_edge() = "-Y";
function vienon_usb001_upstream_edge() = "+X";
function vienon_usb001_upstream_cable_length() = 304.8;
function vienon_usb001_hero_sha256() =
    "3c751f1dbf784083af1d7ea2ee700e7ddbccd587d77e17dfada458fb3011dc63";
function vienon_usb001_usage_sha256() =
    "299d28ef6c14c95fc19dbe0de5367313f78e47066a62850ba105745512a0ebe7";
function vienon_usb001_internal_sha256() =
    "f5161ac65919ef52bc03edad6fed35815246ff483af24d3269169fc67b3c423a";

module vienon_rounded_rect_2d(size, radius) {
    hull()
        for (x = [radius, size.x - radius])
            for (y = [radius, size.y - radius])
                translate([x, y]) circle(r = radius, $fn = 32);
}

module vienon_rounded_prism(origin, size, radius) {
    translate(origin)
        linear_extrude(height = size.z)
            vienon_rounded_rect_2d(
                [size.x, size.y],
                min(radius, min(size.x, size.y) / 2));
}

module vienon_tube_path(points, diameter, facets = 20) {
    for (i = [0 : len(points) - 2])
        hull()
            for (point = [points[i], points[i + 1]])
                translate(point) sphere(d = diameter, $fn = facets);
}

module vienon_port_recess(x) {
    translate([x, -vienon_epsilon, 2.15])
        cube([vienon_port_size.x, 0.72, vienon_port_size.y]);
}

module vienon_usb001_body() {
    // Rounded ABS body with a shallow top crown and visible perimeter seam.
    hull() {
        vienon_rounded_prism([0, 0, 0],
                             [vienon_body.x, vienon_body.y, 0.35], 4.0);
        vienon_rounded_prism([0.75, 0.75, vienon_body.z - 0.35],
                             [vienon_body.x - 1.5,
                              vienon_body.y - 1.5, 0.35], 3.4);
    }
}

module vienon_usb001_shell() {
    vienon_usb001_body();

    // Fixed cable strain relief at the photographed +X end.
    translate([vienon_body.x - 0.3, vienon_body.y / 2 - 2.8, 3.0])
        cube([5.2, 5.6, 4.0]);

    // Visible installed portion of the one-foot upstream lead and overmould.
    vienon_tube_path([
        [vienon_body.x + 3.5, vienon_body.y / 2, 5.0],
        [vienon_body.x + 8.0, vienon_body.y / 2, 5.1],
        [vienon_body.x + 13.0, vienon_body.y / 2 - 1.2, 5.2],
        [vienon_body.x + 18.0, vienon_body.y / 2 - 3.2, 5.3]
    ], 3.6);
    vienon_rounded_prism(
        [vienon_body.x + 16.0, vienon_body.y / 2 - 7.1, 1.8],
        [10.0, 7.8, 7.0], 1.6);
}

module vienon_usb001_dark() {
    for (x = vienon_port_x)
        vienon_port_recess(x);

    // Three USB 2.0 tongues; the first position is the blue USB 3.0 port.
    for (x = [vienon_port_x[1], vienon_port_x[2], vienon_port_x[3]])
        translate([x + 2.0, -0.10, 3.1])
            cube([10.0, 0.85, 1.0]);

    // Case seam and upstream overmould recess.
    translate([3.0, -0.02, 0.82])
        cube([vienon_body.x - 6.0, 0.22, 0.22]);
}

module vienon_usb001_metal() {
    for (x = vienon_port_x)
        translate([x + 0.65, -0.16, 2.55])
            difference() {
                cube([12.7, 0.45, 4.8]);
                translate([0.75, -vienon_epsilon, 0.70])
                    cube([11.2, 0.45 + 2 * vienon_epsilon, 3.4]);
            }

    // USB-A plug at the end of the visible upstream tail.
    translate([vienon_body.x + 25.2,
               vienon_body.y / 2 - 6.25, 2.75])
        cube([6.8, 6.1, 5.1]);
}

module vienon_usb001_blue() {
    translate([vienon_port_x[0] + 2.0, -0.18, 3.1])
        cube([10.0, 0.95, 1.0]);
}

module vienon_usb001_led() {
    translate([4.7, -0.20, 6.55])
        rotate([90, 0, 0])
            cylinder(d = 1.65, h = 0.55, $fn = 24);
}

module vienon_usb001_complete() {
    color("#15181c") vienon_usb001_shell();
    color("#080b0f") vienon_usb001_dark();
    color("#b9bec3") vienon_usb001_metal();
    color("#238ccc") vienon_usb001_blue();
    color("#3ba8ef") vienon_usb001_led();
}
