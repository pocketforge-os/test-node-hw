/*
 * Logitech C270 HD webcam presentation model.
 *
 * This is an original, source-native reconstruction of the stock webcam in
 * the PocketForge fixture. No third-party mesh or Logitech artwork is
 * embedded. The installed face and aperture registration come from the
 * owner's physically proven fixture; shell population and the articulated
 * clip were reconstructed from Logitech's official product gallery. A GPLv3
 * modified-camera STEP was used only as a non-shipped shape cross-check. See
 * LOGITECH-C270-PROVENANCE.md for immutable hashes and source details.
 *
 * Local coordinates match the fixture plate: X is left-to-right, Y is
 * bottom-to-top, and Z is normal to the plate. The camera looks along -Z.
 * The stock body remains on the DUT side (negative Z); the compactly parked
 * universal clip passes through the owner-fit aperture to positive Z.
 * Millimetres.
 */

function c270_installed_face_size() = [71.00, 31.55];
function c270_official_overall_envelope() = [72.91, 31.91, 66.64];
function c270_rear_housing_size() = [37.00, 14.69];
function c270_lens_centre_xy() = [19.20, 15.775];
function c270_lens_plane_z() = -15.00;
function c270_lens_direction() = "-Z";
function c270_diagonal_fov() = 55.0;
function c270_front_reference_sha256() =
    "c86bc28778c52877a07cbd6ab03082dfe505215617180eb5064455f139a718ae";
function c270_qsg_reference_sha256() =
    "ad802bc5705eceb6d75c2eb6ab4219e65e50c97678e1195910ac7b7566cd8d2b";
function c270_modified_step_sha256() =
    "a69c4917c1f2964df2f6dc082827b46958a11e74ae3cda7a142e4d0bc9b4f3d8";

c270_face = c270_installed_face_size();
c270_lens_xy = c270_lens_centre_xy();
c270_body_front_z = -18.00;
c270_body_rear_z = -0.45;
c270_epsilon = 0.02;

module c270_rounded_rect_2d(size, radius, center = false) {
    translated = center ? -size / 2 : [0, 0];
    translate(translated)
        hull()
            for (x = [radius, size.x - radius])
                for (y = [radius, size.y - radius])
                    translate([x, y]) circle(r = radius, $fn = 48);
}

module c270_rounded_prism(origin, size, radius = 0.5) {
    translate(origin)
        linear_extrude(height = size.z)
            c270_rounded_rect_2d(
                [size.x, size.y],
                min(radius, min(size.x, size.y) / 2));
}

module c270_body_slice(origin, size, radius, thickness = 0.20) {
    c270_rounded_prism(origin, [size.x, size.y, thickness], radius);
}

module c270_barrel_x(centre, length, diameter) {
    translate([centre.x - length / 2, centre.y, centre.z])
        rotate([0, 90, 0])
            cylinder(d = diameter, h = length, $fn = 48);
}

module c270_arm_between(first, second, width, thickness) {
    hull()
        for (point = [first, second])
            translate([c270_face.x / 2 - width / 2,
                       point.x - thickness / 2,
                       point.y - thickness / 2])
                cube([width, thickness, thickness]);
}

module c270_cable_between(first, second, diameter) {
    hull()
        for (point = [first, second])
            translate(point) sphere(d = diameter, $fn = 24);
}

module c270_front_text(label, point, size, z,
                       font = "Liberation Sans:style=Bold") {
    // The camera's installed front view is local -Z. OpenSCAD's text outline
    // already reads correctly from that rendered side in this coordinate
    // convention, so do not apply a second mirror here.
    translate([point.x, point.y, z])
        linear_extrude(height = 0.10)
            text(label, size = size, halign = "center",
                 valign = "center", font = font);
}

module c270_back_text(label, point, size, z) {
    translate([point.x, point.y, z])
        linear_extrude(height = 0.10)
            text(label, size = size, halign = "center",
                 valign = "center",
                 font = "Liberation Sans:style=Bold");
}

module c270_shell_body() {
    difference() {
        // Three nested slices reproduce the C270's domed front and tapered
        // rear while the middle slice retains the owner-fit 71 x 31.55 bound.
        hull() {
            c270_body_slice([1.35, 1.15, c270_body_front_z],
                            [68.30, 29.25], 13.6);
            c270_body_slice([0, 0, -7.30],
                            c270_face, 14.9);
            c270_body_slice([2.20, 1.85, c270_body_rear_z - 0.20],
                            [66.60, 27.85], 12.9);
        }

        // The physical lens is recessed behind the front bezel.
        translate([c270_lens_xy.x, c270_lens_xy.y,
                   c270_body_front_z - 1])
            cylinder(d = 17.2, h = 7.2, $fn = 64);
    }
}

module c270_shell() {
    c270_shell_body();

    // The measured rear housing is the only stock body section that passes
    // through the fixture opening.
    rear = c270_rear_housing_size();
    c270_rounded_prism(
        [(c270_face.x - rear.x) / 2,
         (c270_face.y - rear.y) / 2,
         -1.10],
        [rear.x, rear.y, 6.70], 5.6);

    // Stock camera pivot, compactly parked arm, distal hinge, and broad foot.
    c270_barrel_x([c270_face.x / 2, c270_face.y / 2, 4.15],
                  27.0, 9.4);
    c270_arm_between([c270_face.y / 2, 6.4],
                     [c270_face.y / 2, 24.0],
                     25.5, 6.6);
    c270_barrel_x([c270_face.x / 2, c270_face.y / 2, 24.2],
                  28.8, 8.6);
    c270_rounded_prism([20.1, 1.55, 25.0],
                       [30.8, 28.45, 5.0], 5.2);

    // Raised toe visible on the stock universal monitor clip.
    c270_rounded_prism([20.1, 1.55, 29.6],
                       [30.8, 6.4, 2.1], 2.5);
}

module c270_dark() {
    // Recessed black front island.
    translate([7.15, 6.15, c270_body_front_z - 0.42])
        linear_extrude(height = 0.62)
            difference() {
                c270_rounded_rect_2d([32.90, 19.25], 7.8);
                translate([c270_lens_xy.x - 7.15,
                           c270_lens_xy.y - 6.15])
                    circle(d = 16.9, $fn = 64);
            }

    // Concentric fixed-focus barrel and ridges.
    translate([c270_lens_xy.x, c270_lens_xy.y,
               c270_body_front_z - 0.35])
        difference() {
            cylinder(d = 16.5, h = 3.35, $fn = 64);
            translate([0, 0, -c270_epsilon])
                cylinder(d = 10.2, h = 3.35 + 2 * c270_epsilon,
                         $fn = 64);
        }
    for (ring = [[14.6, 12.8, -17.90],
                 [12.4, 10.6, -17.35],
                 [10.8, 9.8, -16.75]])
        translate([c270_lens_xy.x, c270_lens_xy.y, ring[2]])
            difference() {
                cylinder(d = ring[0], h = 0.32, $fn = 64);
                translate([0, 0, -c270_epsilon])
                    cylinder(d = ring[1],
                             h = 0.32 + 2 * c270_epsilon, $fn = 64);
            }

    // Nine microphone perforations in the official 3 x 3 grid.
    for (x = [31.15, 33.45, 35.75])
        for (y = [13.45, 15.775, 18.10])
            translate([x, y, c270_body_front_z - 0.72])
                cylinder(d = 0.88, h = 0.38, $fn = 18);

    // Hinge end caps and the clip's soft monitor-contact pad.
    for (x = [22.0, 49.0])
        c270_barrel_x([x, c270_face.y / 2, 4.15], 0.7, 7.0);
    c270_rounded_prism([21.9, 3.25, 29.95],
                       [27.2, 22.0, 0.55], 4.2);

    // Stock strain relief and a short, routed cable segment stay inside the
    // fixture envelope while making the attached lead unmistakable.
    c270_cable_between([43.8, 20.2, 1.7], [48.8, 21.2, 7.8], 3.8);
    c270_cable_between([48.8, 21.2, 7.8], [57.8, 23.2, 13.2], 3.8);
    c270_cable_between([57.8, 23.2, 13.2], [68.0, 25.0, 16.2], 3.8);
}

module c270_glass() {
    // Glass is deliberately placed at the existing authoritative optical
    // plane; the lens looks from here toward local -Z.
    translate([c270_lens_xy.x, c270_lens_xy.y,
               c270_lens_plane_z() - 0.16])
        cylinder(d = 9.55, h = 0.16, $fn = 64);
    translate([c270_lens_xy.x - 1.2, c270_lens_xy.y + 1.1,
               c270_lens_plane_z() - 0.19])
        cylinder(d = 1.7, h = 0.20, $fn = 32);
}

module c270_led() {
    // The lime activity indicator is a narrow vertical arc left of the lens.
    translate([10.25, c270_lens_xy.y, c270_body_front_z - 0.78])
        linear_extrude(height = 0.42)
            intersection() {
                difference() {
                    scale([0.68, 1.0]) circle(d = 10.4, $fn = 64);
                    scale([0.68, 1.0]) circle(d = 7.6, $fn = 64);
                }
                translate([-5.2, -6.0]) square([3.1, 12.0]);
            }
}

module c270_labels() {
    c270_front_text("720p", [27.2, 15.775], 2.25,
                     c270_body_front_z - 0.79);
    c270_front_text("logi", [52.2, 15.775], 5.5,
                     c270_body_front_z - 0.79);
    c270_back_text("C270", [c270_face.x / 2, 17.1], 2.7, 30.02);
}

module c270_complete() {
    color("#3b4147") c270_shell();
    color("#101317") c270_dark();
    color("#101d29") c270_glass();
    color("#b9d532") c270_led();
    color("#eceeea") c270_labels();
}
