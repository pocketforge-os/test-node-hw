/*
 * Eightwood EWUA0205 internal dual-band Wi-Fi antenna
 *
 * Original, source-native reconstruction of Amazon ASIN B0CRDVS774.
 * No marketplace artwork or third-party geometry is redistributed.
 *
 * Native coordinates follow the installed fixture pose: X runs along the
 * paddle from the sealed end to the coax exit, Y spans the paddle, and Z
 * rises from its adhesive back. The retail package contains two antennas;
 * the PocketForge fixture uses one.
 *
 * Preserved reference hashes:
 *   580d541c8ec83de2b863867c440c6d3ef0e778c35498bc6e53e412b1f3de4b15
 *   75dcf6792c609f9e500244ad3f05d4b624a6149340f6061efd288f906b51d473
 *   e53110549ae998606e33fba5751d817f83719f8bbabb342f8550e0f572d0edd2
 */

ewua0205_panel = [114.0, 15.0, 3.0];
ewua0205_cable_diameter = 0.8;
ewua0205_connector_diameter = 2.33;
ewua0205_visible_tail = 24.0;

function eightwood_ewua0205_panel_size() = ewua0205_panel;
function eightwood_ewua0205_cable_length() = 300.0;
function eightwood_ewua0205_cable_diameter() = ewua0205_cable_diameter;
function eightwood_ewua0205_connector_diameter() =
    ewua0205_connector_diameter;
function eightwood_ewua0205_installed_count() = 1;
function eightwood_ewua0205_package_count() = 2;
function eightwood_ewua0205_cable_edge() = "+X";
function eightwood_ewua0205_hero_sha256() =
    "580d541c8ec83de2b863867c440c6d3ef0e778c35498bc6e53e412b1f3de4b15";
function eightwood_ewua0205_dimension_sha256() =
    "75dcf6792c609f9e500244ad3f05d4b624a6149340f6061efd288f906b51d473";
function eightwood_ewua0205_connector_sha256() =
    "e53110549ae998606e33fba5751d817f83719f8bbabb342f8550e0f572d0edd2";

module ewua0205_panel_outline() {
    polygon([
        [0.0, 5.0], [2.2, 3.6], [7.8, 2.8], [10.4, 0.0],
        [103.6, 0.0], [106.2, 2.8], [111.8, 3.6], [114.0, 5.0],
        [114.0, 10.0], [111.8, 11.4], [106.2, 12.2],
        [103.6, 15.0], [10.4, 15.0], [7.8, 12.2], [2.2, 11.4],
        [0.0, 10.0]
    ]);
}

module ewua0205_tube_path(points, diameter, facets = 18) {
    for (i = [0 : len(points) - 2])
        hull()
            for (point = [points[i], points[i + 1]])
                translate(point) sphere(d = diameter, $fn = facets);
}

module ewua0205_top_text(label, point, size, rotation = 0) {
    translate([point.x, point.y, ewua0205_panel.z - 0.01])
        rotate([0, 0, rotation])
            linear_extrude(height = 0.08)
                text(label, size = size, halign = "center",
                     valign = "center",
                     font = "Liberation Sans:style=Regular",
                     $fn = 8);
}

module eightwood_ewua0205_shell() {
    linear_extrude(height = ewua0205_panel.z)
        ewua0205_panel_outline();

    // Heat-shrink neck around the cable exit.
    translate([108.5, 5.45, 0.35])
        cube([5.5, 4.1, 2.3]);
}

module eightwood_ewua0205_coax() {
    // A short installed service tail is shown rather than coiling the entire
    // 300 mm retail lead across the presentation plate.
    ewua0205_tube_path([
        [114.0, 7.5, 1.50],
        [120.0, 7.5, 1.50],
        [126.0, 6.7, 1.45],
        [132.0, 4.1, 1.40],
        [ewua0205_panel.x + ewua0205_visible_tail, 3.0, 1.35]
    ], ewua0205_cable_diameter);
}

module eightwood_ewua0205_metal() {
    translate([ewua0205_panel.x + ewua0205_visible_tail - 0.6,
               3.0, 1.35])
        rotate([0, 90, 0])
            difference() {
                cylinder(d = ewua0205_connector_diameter,
                         h = 3.2, $fn = 24);
                translate([0, 0, 2.45])
                    cylinder(d = 1.1, h = 0.9, $fn = 18);
            }
}

module eightwood_ewua0205_markings() {
    ewua0205_top_text("Y", [3.4, 7.5], 1.45, 90);
    ewua0205_top_text("E239589", [31.0, 7.5], 2.25);
    ewua0205_top_text("cRU  &  RU", [58.0, 7.5], 1.8);
    ewua0205_top_text("DLK-1  TUBE", [87.0, 7.5], 2.1);
    ewua0205_top_text("125C", [106.0, 7.5], 1.75);
}

module eightwood_ewua0205_complete() {
    color("#17191c") eightwood_ewua0205_shell();
    color("#111316") eightwood_ewua0205_coax();
    color("#caa43a") eightwood_ewua0205_metal();
    color("#a9acaf") eightwood_ewua0205_markings();
}
