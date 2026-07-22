/*
 * PocketForge standard 2020 DUT-node chassis.
 *
 * Coordinates: X left-to-right, Y camera-to-DUT (front-to-rear), Z upward.
 * The external frame envelope starts at [0, 0, 0].  All dimensions are mm.
 *
 * PART choices:
 *   assembly, presentation, stacked_assembly, placard,
 *   placard_riser, placard_riser_pair,
 *   placard_spacer, placard_spacer_pair,
 *   plate_spacer, plate_spacer_set, registration_tab,
 *   registration_tab_set, gantry_joint_plate, gantry_joint_plate_set,
 *   gantry_splice_shell, gantry_splice_shell_pair,
 *   gantry_splice_shell_set, gantry_splice_coupon,
 *   rail_fit_coupon, m3_slide_nut, m3_slide_nut_set,
 *   m3_slide_nut_coupon, print_group_calibration,
 *   print_group_gantry_hardware, print_group_nut_bars,
 *   print_group_plate_mounts,
 *   print_group_stacking_guides, print_group_device_label,
 *   print_group_gantry_splices, cutlist
 */

include <lib/pf-2020.scad>;

PART = "assembly";
EXAMPLE_DEVICE_VARIANT = "smart_pro"; // smart_pro or smart_pro_s
DEVICE_LABEL = EXAMPLE_DEVICE_VARIANT == "smart_pro_s" ?
               "TrimUI Smart Pro S" : "TrimUI Smart Pro";
PLATE_DETAIL = "proxy";       // proxy or mesh
EXTRUSION_DETAIL = "slot";    // envelope or slot
SHOW_PLATES = true;
SHOW_DEVICE = true;
SHOW_CAMERA_FRUSTUM = true;
SHOW_CONNECTOR_PROXIES = true;
SHOW_REGISTRATION_GUIDES = true;

// `make preview` stages these exact production meshes beside this source so
// presentation mode is portable with the Desktop export.  Proxy mode never
// opens them and remains safe for clean-checkout linting.
fixture_presentation_mesh =
    "build/imports/pocketforge-dut-fixture-v1.stl";
cradle_s_presentation_mesh =
    "build/imports/trimui-smart-pro-s-carrier.stl";
cradle_base_presentation_mesh =
    "build/imports/trimui-smart-pro-carrier.stl";
cradle_presentation_mesh = EXAMPLE_DEVICE_VARIANT == "smart_pro_s" ?
                           cradle_s_presentation_mesh :
                           cradle_base_presentation_mesh;
cradle_hooks_presentation_mesh =
    "build/imports/trimui-smart-pro-family-installed-hooks.stl";

$fn = 48;
epsilon = 0.02;

// ---- Standard chassis contract ------------------------------------------
profile_size = 20.0;
frame_outer = [400.0, 400.0, 400.0];
frame_clear = frame_outer - [2 * profile_size,
                             2 * profile_size,
                             2 * profile_size];
join_topology = "three_way_end_corners_B08C9Q2TGW";

// SeekLiny B0DY7FKKMT is a nominal 20-series V-slot profile.  These interface
// dimensions come from the owner's delivered rail, not a generic "2020"
// drawing: A=mouth, B=depth, C=widest pocket, D=lip depth, E=web thickness.
// F=6.66 mm is retained in the measurement record but is not needed by the
// simplified assembly preview or printed slot hardware.
extrusion_slot_opening = 6.73;
extrusion_slot_depth = 6.48;
extrusion_slot_pocket_width = 12.15;
extrusion_slot_lip_depth = 1.66;
extrusion_web_thickness = 1.20;
extrusion_centre_bore = 4.2; // preview-only 20-series nominal

stock_length = 1000.0;
// Deliberately wide provisional allowance.  Each nominal 1 m stick must yield
// 360 + 360 + 180 mm, so validation includes all three cut kerfs.
cut_kerf = 3.2;

// Eight 20 mm three-way end connectors occupy the outer corners, so all 12
// perimeter rails terminate between corner blocks.  Two independent internal
// plate gantries each add two split vertical uprights and two continuous
// horizontal crossbars. Keeping the uprights in the same X planes as the outer
// depth rails makes the end joints flat; their 180 mm halves consume the
// otherwise stranded remainder after two 360 mm cuts.
structural_x_length = frame_outer.x - 2 * profile_size;
structural_y_length = frame_outer.y - 2 * profile_size;
structural_z_length = frame_outer.z - 2 * profile_size;
gantry_upright_length = structural_z_length;
gantry_crossbar_length = structural_x_length;
gantry_upright_segment_count = 2;
gantry_upright_segment_length = gantry_upright_length /
                                gantry_upright_segment_count;
gantry_upright_splice_z = profile_size + gantry_upright_segment_length;
gantry_upright_x = [profile_size / 2,
                    frame_outer.x - profile_size / 2];
gantry_y_limits = [profile_size + profile_size / 2,
                   frame_outer.y - profile_size - profile_size / 2];
fixture_gantry_y = gantry_y_limits.x;
cradle_gantry_y = gantry_y_limits.y;

// ---- Existing plate interfaces and optical registration -----------------
fixture_plate_size = [200.0, 247.0, 3.2];
fixture_webcam_datum = [100.0, 132.0];
fixture_slot_inset = [19.0, 8.0];

cradle_plate_size = [247.0, 200.0, 3.2];
cradle_screen_datum = [123.5, 100.0];
cradle_slot_inset = [19.0, 8.0];

optical_datum = [frame_outer.x / 2, 202.0]; // [X, Z]
plate_mount_gap = 5.0;

// Each optical plane follows its gantry Y datum.  The fixture plate sits just
// behind the rear face of its crossbars; the DUT carrier sits just ahead of
// the front face of its crossbars.  Moving either entire gantry therefore
// preserves its plate mount while changing camera-to-DUT distance.
fixture_plane_y = fixture_gantry_y + profile_size / 2 + plate_mount_gap +
                  fixture_plate_size.z;
fixture_origin = [optical_datum.x - fixture_webcam_datum.x,
                  fixture_plane_y,
                  optical_datum.y - fixture_webcam_datum.y];

// The DUT carrier's hooks/device face -Y toward the webcam.
cradle_plane_y = cradle_gantry_y - profile_size / 2 - plate_mount_gap;
cradle_origin = [optical_datum.x - cradle_screen_datum.x,
                 cradle_plane_y,
                 optical_datum.y - cradle_screen_datum.y];

fixture_crossbar_z = [fixture_origin.z + fixture_slot_inset.y,
                      fixture_origin.z + fixture_plate_size.y -
                      fixture_slot_inset.y];
cradle_crossbar_z = [cradle_origin.z + cradle_slot_inset.y,
                     cradle_origin.z + cradle_plate_size.y -
                     cradle_slot_inset.y];

// Camera/device preview values.  The mounted C270 keep-out was measured on the
// fixture; Logitech's full clip envelope is larger and is documented in the
// README.  The current C270 product specification gives a conservative 55
// degree diagonal FOV for widescreen capture, from which H/V FOV are derived.
camera_model = "Logitech C270 HD";
camera_installed_keepout = [71.0, 24.0, 31.55]; // [X width, Y depth, Z height]
camera_lens_y = fixture_plane_y + 15.0;
camera_diagonal_fov = 55.0;
camera_capture_aspect = [16.0, 9.0];
camera_aspect_diagonal = sqrt(pow(camera_capture_aspect.x, 2) +
                              pow(camera_capture_aspect.y, 2));
camera_assumed_hfov =
    2 * atan(tan(camera_diagonal_fov / 2) * camera_capture_aspect.x /
             camera_aspect_diagonal);
camera_assumed_vfov =
    2 * atan(tan(camera_diagonal_fov / 2) * camera_capture_aspect.y /
             camera_aspect_diagonal);
device_body = [188.35, 79.77, 10.7];
device_rear_gap = 11.0;
device_screen_y = cradle_plane_y - device_rear_gap - device_body.z;
optical_distance = device_screen_y - camera_lens_y;
framing_margin = [20.0, 20.0];
framing_target = [device_body.x + 2 * framing_margin.x,
                  device_body.y + 2 * framing_margin.y];
required_hfov = 2 * atan((framing_target.x / 2) / optical_distance);
required_vfov = 2 * atan((framing_target.y / 2) / optical_distance);

// ---- Printable interface parameters -------------------------------------
m3_clearance = 3.6;
m5_clearance = 5.5;
spacer_size = [18.0, 14.0];
spacer_corner_radius = 2.0;
plate_spacer_thickness = plate_mount_gap;
// Physical ABS coupon result with the lab's 0.8 mm nozzle: 6.43 mm slides
// cleanly; 6.63 mm is too large and 6.23 mm is the loose snap-in fallback.
slot_key_clearance = 0.30;
slot_key_width = extrusion_slot_opening - slot_key_clearance;
slot_key_height = 1.2;

// Ordinary metal M3 nut captured inside a large, end-loaded ABS nut bar.  The
// 5.6 x 2.8 mm pocket is the already print-validated DUT-hook fit for the
// owner's measured 5.36 x 2.30 mm nuts.  Unlike the retired twist-in carrier,
// this body is deliberately too wide to pass through the slot mouth: slide it
// into the open end of an extrusion before the frame end is assembled.  Its
// broad bearing face nearly fills the measured 12.15 mm under-lip pocket and
// tapers toward the extrusion web, following the delivered rail's channel
// instead of inheriting a narrow commercial T-nut envelope.
m3_nut_measured_across_flats = 5.36;
m3_nut_measured_thickness = 2.30;
m3_nut_pocket_across_flats = 5.60;
m3_nut_pocket_depth = 2.80;
m3_slide_nut_length = 60.0;
m3_slide_nut_bearing_width = 11.85;
m3_slide_nut_deep_width = 8.90;
m3_slide_nut_height = 4.40;
m3_slide_nut_flange_height = 1.20;
m3_slide_nut_corner_chamfer = 3.0;
// The middle candidate applies the same -0.30 mm compensation that physically
// selected the 6.43 mm key for the measured 6.73 mm slot mouth.
m3_slide_nut_coupon_bearing_widths = [11.55, 11.85, 12.05];
m3_slide_nut_coupon_copies = 2;
m3_slide_nut_required_count = 26; // 16 gantry + 8 plate + 2 placard interfaces
m3_slide_nut_spare_count = 6;     // pre-load before rail ends are closed
m3_slide_nut_set_count = m3_slide_nut_required_count +
                         m3_slide_nut_spare_count;
m3_slide_nut_set_columns = 4;

// Four non-structural gantry uprights are each made from two 180 mm offcut
// segments.  One support-free two-half clamshell aligns each central butt
// joint.  Its broad face prints on the bed; shallow wings wrap the extrusion
// without meeting, and four M3 bolts pass through external ears beside (never
// through) the aluminum.  The validated 6.43 mm rail key bridges the seam on
// each of two opposite slot faces.
gantry_splice_length = 80.0;
gantry_splice_wall = 4.8;
gantry_splice_wing_depth = 8.0;
gantry_splice_external_clearance = 0.40;
gantry_splice_inner_width = profile_size +
                             gantry_splice_external_clearance;
gantry_splice_ear_extension = 8.0;
gantry_splice_ear_length = 14.0;
gantry_splice_bolt_x = 25.0;
gantry_splice_fit_clearances = [0.20, 0.40, 0.60];
gantry_splice_fit_copies = 2;

// One identical flat ABS indexing plate locates every gantry-upright endpoint
// against an outer depth rail.  Perpendicular rear keys enter the two slots to
// square the joint; ordinary M3 screws and captured metal nuts provide clamp
// force.  These light-duty plates position payload gantries only and never
// enter the outer-frame or stacking load path.
gantry_joint_plate_size = [36.0, 44.0, 4.8];
gantry_joint_corner_radius = 3.0;
gantry_joint_hole_offset = 10.0;
gantry_joint_slot = [8.0, m3_clearance];
gantry_joint_key_length = 18.0;
gantry_joint_key_height = slot_key_height;

placard_size = [166.0, 38.0, 3.2];
placard_corner_radius = 4.0;
placard_hole_spacing = 140.0;
placard_text_size = 13.5;
placard_text_relief = 1.2;
placard_spacer_thickness = 3.0;
placard_riser_size = [18.0, 58.0, 4.0];
placard_riser_hole_offset = 18.0;
placard_riser_slot = [10.0, m3_clearance];
placard_rail_mount_z = frame_outer.z - profile_size / 2;
placard_center_z = placard_rail_mount_z -
                   2 * placard_riser_hole_offset;
placard_riser_center_z = (placard_rail_mount_z + placard_center_z) / 2;

registration_tab_size = [24.0, 72.0, 4.0];
registration_above_frame = 12.0;
registration_lower_slot = [9.0, m5_clearance];
registration_lower_hole_y = [12.0, 28.0];
registration_upper_lock_y = 66.0;

// ---- Derived-fit guards --------------------------------------------------
inner_min = [profile_size, profile_size];
inner_max = [frame_outer.x - profile_size,
             frame_outer.z - profile_size];
fixture_margins = [fixture_origin.x - inner_min.x,
                   inner_max.x - (fixture_origin.x + fixture_plate_size.x),
                   fixture_origin.z - inner_min.y,
                   inner_max.y - (fixture_origin.z + fixture_plate_size.y)];
cradle_margins = [cradle_origin.x - inner_min.x,
                  inner_max.x - (cradle_origin.x + cradle_plate_size.x),
                  cradle_origin.z - inner_min.y,
                  inner_max.y - (cradle_origin.z + cradle_plate_size.y)];

assert(EXAMPLE_DEVICE_VARIANT == "smart_pro" ||
       EXAMPLE_DEVICE_VARIANT == "smart_pro_s",
       str("Unknown example device variant: ", EXAMPLE_DEVICE_VARIANT));
assert(frame_outer.x == frame_outer.y && frame_outer.y == frame_outer.z,
       "Standard chassis must remain a cube unless the rack class changes");
assert(min(fixture_margins) >= 50.0,
       str("Fixture routing margin fell below 50 mm: ", fixture_margins));
assert(min(cradle_margins) >= 50.0,
       str("Cradle routing margin fell below 50 mm: ", cradle_margins));
assert(fixture_gantry_y >= gantry_y_limits.x &&
       fixture_gantry_y <= gantry_y_limits.y,
       str("Fixture gantry Y is outside legal travel: ", fixture_gantry_y));
assert(cradle_gantry_y >= gantry_y_limits.x &&
       cradle_gantry_y <= gantry_y_limits.y,
       str("Cradle gantry Y is outside legal travel: ", cradle_gantry_y));
assert(fixture_gantry_y + profile_size <= cradle_gantry_y,
       "Fixture and cradle gantries must not intersect");
assert(gantry_upright_segment_count == 2 &&
       2 * gantry_upright_segment_length == gantry_upright_length,
       "Each movable gantry upright must be two equal offcut segments");
assert(gantry_splice_length < gantry_upright_segment_length,
       "Upright splice must leave exposed aluminum on both segments");
assert(min([for (z = concat(fixture_crossbar_z, cradle_crossbar_z))
                abs(z - gantry_upright_splice_z)]) >=
       gantry_splice_length / 2 + profile_size / 2,
       "Central upright splice must not collide with a plate crossbar");
assert(min(fixture_crossbar_z) >= profile_size + profile_size / 2 &&
       max(fixture_crossbar_z) <= frame_outer.z -
                                  profile_size - profile_size / 2,
       str("Fixture crossbar Z is outside gantry travel: ",
           fixture_crossbar_z));
assert(min(cradle_crossbar_z) >= profile_size + profile_size / 2 &&
       max(cradle_crossbar_z) <= frame_outer.z -
                                 profile_size - profile_size / 2,
       str("Cradle crossbar Z is outside gantry travel: ",
           cradle_crossbar_z));
assert(optical_distance > 0, "Camera must remain in front of the DUT");
assert(camera_assumed_hfov >= required_hfov,
       str("Estimated horizontal FOV is too narrow; required ", required_hfov));
assert(camera_assumed_vfov >= required_vfov,
       str("Estimated vertical FOV is too narrow; required ", required_vfov));
assert(slot_key_width > m3_clearance,
       "T-slot key must remain wider than the M3 clearance hole");
assert(m3_nut_pocket_across_flats >= m3_nut_measured_across_flats,
       "M3 nut pocket must not be smaller than the measured nut");
assert(m3_nut_pocket_depth >= m3_nut_measured_thickness,
       "M3 nut pocket must not be shallower than the measured nut");
assert(m3_slide_nut_bearing_width > extrusion_slot_opening,
       "End-loaded carrier bearing face must be wider than the slot mouth");
assert(m3_slide_nut_bearing_width < extrusion_slot_pocket_width,
       "End-loaded carrier bearing face must fit inside the measured slot pocket");
assert(m3_slide_nut_deep_width >
       m3_nut_pocket_across_flats + 2 * 1.6,
       "End-loaded carrier needs printable deep-face walls around the metal nut");
assert(m3_slide_nut_deep_width < m3_slide_nut_bearing_width,
       "End-loaded carrier must taper inward away from its bearing face");
assert(min(m3_slide_nut_coupon_bearing_widths) > extrusion_slot_opening &&
       max(m3_slide_nut_coupon_bearing_widths) < extrusion_slot_pocket_width,
       "Every end-loaded coupon bearing face must bridge the mouth and fit pocket");
assert(len(m3_slide_nut_coupon_bearing_widths) *
       m3_slide_nut_coupon_copies >= 6,
       "Small ABS fit batches need at least six parts for inter-part cooling");
assert(m3_slide_nut_height <
       extrusion_slot_depth - extrusion_slot_lip_depth,
       "End-loaded carrier must fit behind the measured slot lip");
assert(m3_slide_nut_flange_height > 0 &&
       m3_slide_nut_flange_height < m3_slide_nut_height,
       "Nut-bar bearing flange must fit inside its total channel depth");
assert(m3_slide_nut_length >= 40.0,
       "End-loaded nut bar must remain a large, easy-handling mount point");
assert(m3_slide_nut_height - m3_nut_pocket_depth >= 1.6,
       "End-loaded carrier needs at least four 0.4 mm floor layers");
assert(gantry_splice_inner_width > profile_size,
       "Splice clamshell needs positive external rail clearance");
assert(2 * gantry_splice_wing_depth < profile_size,
       "Opposed splice-shell wings need a service gap");
assert(gantry_splice_bolt_x + gantry_splice_ear_length / 2 <
       gantry_splice_length / 2,
       "Splice clamp ears must remain inside the shell length");
assert(len(gantry_splice_fit_clearances) * gantry_splice_fit_copies >= 6,
       "Small ABS splice-fit batches need at least six parts for cooling");
assert(gantry_joint_plate_size.x > gantry_joint_key_length &&
       gantry_joint_plate_size.y >
       2 * gantry_joint_hole_offset + gantry_joint_slot.y,
       "Gantry joint plate must surround both keyed fastener interfaces");
assert(placard_center_z + placard_size.y / 2 <
       frame_outer.z - profile_size,
       "Front placard must remain completely below the top front rail");
assert(registration_above_frame > 0 &&
       registration_above_frame < profile_size,
       "Registration guide must engage, but not exceed, one upper post width");
registration_guide_bottom = frame_outer.z -
                            (registration_tab_size.y -
                             registration_above_frame);
assert(registration_guide_bottom + max(registration_lower_hole_y) <
       frame_outer.z - profile_size,
       "Registration lower screws must land in the vertical extrusion");
assert(registration_guide_bottom + registration_upper_lock_y > frame_outer.z,
       "Registration upper lock must land in the stacked frame");

module extrusion(length, axis) {
    color([0.72, 0.74, 0.77])
        pf_2020_extrusion(length, axis, profile_size,
                          EXTRUSION_DETAIL, extrusion_slot_opening,
                          extrusion_slot_depth, extrusion_centre_bore);
}

module outer_frame() {
    // All perimeter rails butt between the 20 mm three-way corner blocks.
    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
            translate([x, y, profile_size])
                extrusion(structural_z_length, "z");

    // Width and depth rails butt between the posts.
    for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
        for (z = [profile_size / 2, frame_outer.z - profile_size / 2])
            translate([profile_size, y, z])
                extrusion(structural_x_length, "x");

    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        for (z = [profile_size / 2, frame_outer.z - profile_size / 2])
            translate([x, profile_size, z])
                extrusion(structural_y_length, "y");
}

module plate_gantry(y, crossbar_zs) {
    // Uprights share the X planes of the outer depth rails.  This lets one
    // flat keyed plate bridge each T joint while the complete gantry slides
    // anywhere along the depth-rail slots.
    for (x = gantry_upright_x)
        for (segment = [0 : gantry_upright_segment_count - 1])
            translate([x, y,
                       profile_size +
                       segment * gantry_upright_segment_length])
                extrusion(gantry_upright_segment_length, "z");

    // Concealed metal L-connectors let each crossbar slide vertically on the
    // uprights; plate fasteners then slide horizontally in these crossbars.
    for (z = crossbar_zs)
        translate([profile_size, y, z])
            extrusion(gantry_crossbar_length, "x");
}

module plate_gantries() {
    plate_gantry(fixture_gantry_y, fixture_crossbar_z);
    plate_gantry(cradle_gantry_y, cradle_crossbar_z);
}

module three_way_end_connector_proxy(position) {
    // BLCCLOY B08C9Q2TGW: zinc-alloy 20 x 20 mm corner body.  Slot tongues and
    // M4 set screws are omitted; the occupied corner cube controls rail cuts.
    color([0.08, 0.08, 0.09])
        translate(position) cube([profile_size, profile_size, profile_size]);
}

module gantry_l_connector_proxy(y, z, right = false) {
    // BLCCLOY B08D6T9CGN: concealed zinc 26 x 26 x 9.5 mm L connector.
    connector_length = 26.0;
    connector_width = 9.5;
    connector_thickness = 3.0;
    x_origin = right ? frame_outer.x - profile_size : profile_size;

    color([0.10, 0.10, 0.11])
        translate([x_origin, y - profile_size / 2 - connector_thickness,
                   z - connector_width / 2])
            if (right)
                mirror([1, 0, 0])
                    union() {
                        cube([connector_length, connector_thickness,
                              connector_width]);
                        cube([connector_width, connector_thickness,
                              connector_length]);
                    }
            else
                union() {
                    cube([connector_length, connector_thickness,
                          connector_width]);
                    translate([-connector_width, 0, 0])
                        cube([connector_width, connector_thickness,
                              connector_length]);
                }
}

module connector_proxies() {
    outer_corner_connector_proxies();
    gantry_crossbar_connector_proxies();
    gantry_joint_plate_previews();
    gantry_splice_previews();
}

module outer_corner_connector_proxies() {
    for (x = [0, frame_outer.x - profile_size])
        for (y = [0, frame_outer.y - profile_size])
            for (z = [0, frame_outer.z - profile_size])
                three_way_end_connector_proxy([x, y, z]);
}

module gantry_crossbar_connector_proxies() {
    for (z = fixture_crossbar_z)
        for (right = [false, true])
            gantry_l_connector_proxy(fixture_gantry_y, z, right);
    for (z = cradle_crossbar_z)
        for (right = [false, true])
            gantry_l_connector_proxy(cradle_gantry_y, z, right);
}

module installed_gantry_joint_plate(y, top = false, right = false) {
    joint_z = top ? frame_outer.z - profile_size : profile_size;
    keyed_depth = gantry_joint_plate_size.z + gantry_joint_key_height;
    face_x = right ? frame_outer.x - profile_size : profile_size;

    // Local X -> world Y, local Y -> world Z.  The top instance reverses
    // local Y so the horizontal key always enters the outer depth rail and
    // the vertical key always enters the gantry upright.  Local +Z points
    // toward the aluminum, leaving the broad plate in the clear interior.
    multmatrix([
        [0, 0, right ? 1 : -1,
         right ? face_x - keyed_depth : face_x + keyed_depth],
        [1, 0, 0, y],
        [0, top ? -1 : 1, 0, joint_z],
        [0, 0, 0, 1]
    ]) gantry_joint_plate();
}

module gantry_joint_plate_previews() {
    color([0.94, 0.47, 0.10])
        for (y = [fixture_gantry_y, cradle_gantry_y])
            for (top = [false, true])
                for (right = [false, true])
                    installed_gantry_joint_plate(y, top, right);
}

module fixture_plate_preview(detail = PLATE_DETAIL) {
    color([0.90, 0.90, 0.86])
        if (detail == "mesh")
            translate(fixture_origin)
                rotate([90, 0, 0])
                    import(fixture_presentation_mesh,
                           convexity = 10);
        else
            translate([fixture_origin.x,
                       fixture_origin.y - fixture_plate_size.z,
                       fixture_origin.z])
                cube([fixture_plate_size.x,
                      fixture_plate_size.z,
                      fixture_plate_size.y]);
}

module cradle_mesh_at_installed_datum(mesh_path) {
    translate(cradle_origin)
        rotate([90, 0, 0])
            import(mesh_path, convexity = 10);
}

module cradle_plate_preview(detail = PLATE_DETAIL) {
    if (detail == "mesh") {
        color([0.88, 0.88, 0.84])
            cradle_mesh_at_installed_datum(cradle_presentation_mesh);

        // The hooks are a distinct presentation-only export from the accepted
        // cradle source. They remain independently printable/serviceable and
        // cannot leak into any chassis or carrier production STL.
        color([0.94, 0.47, 0.10])
            cradle_mesh_at_installed_datum(
                cradle_hooks_presentation_mesh);
    } else {
        color([0.88, 0.88, 0.84])
            translate([cradle_origin.x,
                       cradle_origin.y - cradle_plate_size.z,
                       cradle_origin.z])
                cube([cradle_plate_size.x,
                      cradle_plate_size.z,
                      cradle_plate_size.y]);
    }
}

module installed_plate_spacer(point, rear = false) {
    color([0.95, 0.53, 0.12])
        translate([point.x - spacer_size.x / 2,
                   rear ? cradle_plane_y :
                          fixture_plane_y - fixture_plate_size.z -
                          plate_spacer_thickness,
                   point.y - spacer_size.y / 2])
            cube([spacer_size.x, plate_spacer_thickness, spacer_size.y]);
}

module plate_mount_previews() {
    fixture_mount_x = [fixture_origin.x + fixture_slot_inset.x,
                       fixture_origin.x + fixture_plate_size.x -
                       fixture_slot_inset.x];
    cradle_mount_x = [cradle_origin.x + cradle_slot_inset.x,
                      cradle_origin.x + cradle_plate_size.x -
                      cradle_slot_inset.x];

    for (x = fixture_mount_x)
        for (z = fixture_crossbar_z)
            installed_plate_spacer([x, z]);
    for (x = cradle_mount_x)
        for (z = cradle_crossbar_z)
            installed_plate_spacer([x, z], true);
}

module device_and_camera_preview() {
    // Device front plane is the optical target; its rear faces the carrier.
    color([0.08, 0.09, 0.10, 0.88])
        translate([optical_datum.x - device_body.x / 2,
                   device_screen_y,
                   optical_datum.y - device_body.y / 2])
            cube([device_body.x, device_body.z, device_body.y]);

    // Webcam body is intentionally only an envelope pending model/FOV ID.
    color([0.10, 0.10, 0.11, 0.9])
        translate([optical_datum.x - camera_installed_keepout.x / 2,
                   fixture_plane_y,
                   optical_datum.y - camera_installed_keepout.z / 2])
            cube(camera_installed_keepout);
    color([0.10, 0.16, 0.22])
        translate([optical_datum.x, camera_lens_y, optical_datum.y])
            rotate([-90, 0, 0]) cylinder(d = 12, h = 5);
}

module camera_frustum_preview() {
    lens = [optical_datum.x, camera_lens_y, optical_datum.y];
    target_y = device_screen_y - 0.2;
    coverage_half_width = optical_distance * tan(camera_assumed_hfov / 2);
    coverage_half_height = optical_distance * tan(camera_assumed_vfov / 2);
    %color([0.18, 0.72, 0.92, 0.18])
        hull() {
            translate(lens) sphere(d = 2.0, $fn = 16);
            for (x = [-coverage_half_width, coverage_half_width])
                for (z = [-coverage_half_height, coverage_half_height])
                    translate([optical_datum.x + x, target_y,
                               optical_datum.y + z])
                        sphere(d = 1.0, $fn = 12);
        }
}

module placard_text(relief = placard_text_relief) {
    translate([0, 0, placard_size.z])
        linear_extrude(height = relief)
            text(DEVICE_LABEL, size = placard_text_size,
                 font = "Liberation Sans:style=Bold",
                 halign = "center", valign = "center");
}

module device_id_placard() {
    difference() {
        union() {
            linear_extrude(height = placard_size.z)
                pf_rounded_rect_2d([placard_size.x, placard_size.y],
                                   placard_corner_radius);
            placard_text();
        }
        for (x = [-placard_hole_spacing / 2,
                   placard_hole_spacing / 2])
            translate([x, 0, -epsilon])
                cylinder(d = m3_clearance,
                         h = placard_size.z +
                             placard_text_relief + 2 * epsilon);
    }
}

module keyed_spacer(thickness, dimensions = spacer_size) {
    difference() {
        union() {
            linear_extrude(height = thickness)
                pf_rounded_rect_2d(dimensions, spacer_corner_radius);
            translate([0, 0, thickness])
                linear_extrude(height = slot_key_height)
                    pf_rounded_rect_2d([dimensions.x - 3.0,
                                        slot_key_width], 1.0);
        }
        translate([0, 0, -epsilon])
            cylinder(d = m3_clearance,
                     h = thickness + slot_key_height + 2 * epsilon);
    }
}

module plate_spacer() {
    keyed_spacer(plate_spacer_thickness);
}

module plate_spacer_set() {
    for (row = [0, 1])
        for (column = [0 : 3])
            translate([column * 24.0, row * 20.0, 0]) plate_spacer();
}

module placard_spacer() {
    keyed_spacer(placard_spacer_thickness, [18.0, 14.0]);
}

module placard_spacer_pair() {
    translate([-12, 0, 0]) placard_spacer();
    translate([ 12, 0, 0]) placard_spacer();
}

module placard_riser() {
    difference() {
        linear_extrude(height = placard_riser_size.z)
            pf_rounded_rect_2d([placard_riser_size.x,
                                placard_riser_size.y], 2.5);
        translate([0, -placard_riser_hole_offset, -epsilon])
            linear_extrude(height = placard_riser_size.z + 2 * epsilon)
                rotate(90)
                    pf_capsule_2d(placard_riser_slot.x,
                                  placard_riser_slot.y);
        translate([0, placard_riser_hole_offset, -epsilon])
            cylinder(d = m3_clearance,
                     h = placard_riser_size.z + 2 * epsilon);
    }
}

module placard_riser_pair() {
    translate([-12, 0, 0]) placard_riser();
    translate([ 12, 0, 0]) placard_riser();
}

module gantry_joint_plate() {
    total_depth = gantry_joint_plate_size.z + gantry_joint_key_height;

    difference() {
        union() {
            linear_extrude(height = gantry_joint_plate_size.z)
                pf_rounded_rect_2d([gantry_joint_plate_size.x,
                                    gantry_joint_plate_size.y],
                                   gantry_joint_corner_radius);

            // Horizontal key locates the outer depth-rail slot.
            translate([0, -gantry_joint_hole_offset,
                       gantry_joint_plate_size.z])
                linear_extrude(height = gantry_joint_key_height)
                    pf_rounded_rect_2d([gantry_joint_key_length,
                                        slot_key_width], 1.0);

            // Perpendicular key locates the gantry-upright slot and prevents
            // the two-screw joint from racking while it is tightened.
            translate([0, gantry_joint_hole_offset,
                       gantry_joint_plate_size.z])
                linear_extrude(height = gantry_joint_key_height)
                    pf_rounded_rect_2d([slot_key_width,
                                        gantry_joint_key_length], 1.0);
        }

        for (y = [-gantry_joint_hole_offset,
                   gantry_joint_hole_offset])
            translate([0, y, -epsilon])
                linear_extrude(height = total_depth + 2 * epsilon)
                    pf_capsule_2d(gantry_joint_slot.x,
                                  gantry_joint_slot.y);
    }
}

module gantry_joint_plate_set() {
    for (row = [0, 1])
        for (column = [0 : 3])
            translate([column * (gantry_joint_plate_size.x + 6.0),
                       row * (gantry_joint_plate_size.y + 6.0), 0])
                gantry_joint_plate();
}

// One half of a support-free external clamshell for the central butt joint in
// a gantry upright.  Two identical halves oppose each other on the rail.  The
// M3 clamp bolts live entirely outside the extrusion envelope, so no drilling
// or printed T-slot thread carries this joint.  A rail key on each half bridges
// the seam and positively aligns two 180 mm segments before tightening.
module gantry_splice_shell(clearance = gantry_splice_external_clearance,
                           shell_length = gantry_splice_length,
                           with_ears = true,
                           witness_notches = 0) {
    inner_width = profile_size + clearance;
    outer_width = inner_width + 2 * gantry_splice_wall;
    ear_center_y = outer_width / 2 +
                   gantry_splice_ear_extension / 2;

    assert(clearance > 0,
           "Gantry splice shell needs positive rail clearance");
    assert(shell_length > 2 * gantry_splice_wall,
           "Gantry splice shell is too short for its wall thickness");

    difference() {
        union() {
            translate([-shell_length / 2, -outer_width / 2, 0])
                cube([shell_length, outer_width, gantry_splice_wall]);

            for (side = [-1, 1])
                translate([-shell_length / 2,
                           side * (inner_width / 2 +
                                   gantry_splice_wall / 2) -
                           gantry_splice_wall / 2,
                           gantry_splice_wall])
                    cube([shell_length, gantry_splice_wall,
                          gantry_splice_wing_depth]);

            translate([0, 0, gantry_splice_wall])
                linear_extrude(height = slot_key_height)
                    pf_rounded_rect_2d(
                        [shell_length - 2 * gantry_splice_wall,
                         slot_key_width], 1.0);

            if (with_ears)
                for (x = [-gantry_splice_bolt_x,
                           gantry_splice_bolt_x])
                    for (side = [-1, 1])
                        translate([x - gantry_splice_ear_length / 2,
                                   side * ear_center_y -
                                   gantry_splice_ear_extension / 2,
                                   0])
                            cube([gantry_splice_ear_length,
                                  gantry_splice_ear_extension,
                                  gantry_splice_wall]);
        }

        if (with_ears)
            for (x = [-gantry_splice_bolt_x,
                       gantry_splice_bolt_x])
                for (side = [-1, 1])
                    translate([x, side * ear_center_y, -epsilon])
                        cylinder(d = m3_clearance,
                                 h = gantry_splice_wall + 2 * epsilon,
                                 $fn = 28);

        if (witness_notches > 0)
            for (notch = [0 : witness_notches - 1])
                translate([shell_length / 2,
                           (notch - (witness_notches - 1) / 2) * 3.0,
                           -epsilon])
                    cylinder(d = 2.4,
                             h = gantry_splice_wall + 2 * epsilon,
                             $fn = 20);
    }
}

module gantry_splice_shell_pair() {
    translate([0, -25.0, 0]) gantry_splice_shell();
    translate([0,  25.0, 0]) gantry_splice_shell();
}

module gantry_splice_shell_set() {
    for (index = [0 : 7])
        translate([(index % 3) * 82.0,
                   floor(index / 3) * 49.0, 0])
            gantry_splice_shell();
}

// Six short U sections calibrate the only new fit: external 2020 face width.
// Two copies per clearance improve ABS cooling and expose print repeatability.
module gantry_splice_fit_coupon() {
    for (index = [0 : len(gantry_splice_fit_clearances) - 1])
        for (copy = [0 : gantry_splice_fit_copies - 1])
            translate([index * 30.0, copy * 35.0, 0])
                gantry_splice_shell(
                    gantry_splice_fit_clearances[index],
                    25.0, false, index + 1);
}

module installed_gantry_splice_half(x, y, front = true) {
    multmatrix(front ? [
        [0, 1, 0, x],
        [0, 0, 1, y - profile_size / 2 - gantry_splice_wall],
        [1, 0, 0, gantry_upright_splice_z],
        [0, 0, 0, 1]
    ] : [
        [0, 1, 0, x],
        [0, 0, -1, y + profile_size / 2 + gantry_splice_wall],
        [1, 0, 0, gantry_upright_splice_z],
        [0, 0, 0, 1]
    ]) gantry_splice_shell();
}

module gantry_splice_previews() {
    color([0.94, 0.47, 0.10])
        for (y = [fixture_gantry_y, cradle_gantry_y])
            for (x = gantry_upright_x)
                for (front = [false, true])
                    installed_gantry_splice_half(x, y, front);
}

module registration_tab() {
    difference() {
        linear_extrude(height = registration_tab_size.z)
            polygon([[0, 0],
                     [registration_tab_size.x, 0],
                     [registration_tab_size.x,
                      registration_tab_size.y - 5.0],
                     [registration_tab_size.x - 3.0,
                      registration_tab_size.y],
                     [3.0, registration_tab_size.y],
                     [0, registration_tab_size.y - 5.0]]);
        for (y = registration_lower_hole_y)
            translate([registration_tab_size.x / 2, y, -epsilon])
                linear_extrude(height = registration_tab_size.z + 2 * epsilon)
                    rotate(90)
                        pf_capsule_2d(registration_lower_slot.x,
                                      registration_lower_slot.y);
        // Optional positive lock into the bottom 2020 post of the upper frame.
        translate([registration_tab_size.x / 2,
                   registration_upper_lock_y, -epsilon])
            cylinder(d = m5_clearance,
                     h = registration_tab_size.z + 2 * epsilon);
    }
}

module registration_tab_set() {
    for (row = [0, 1])
        for (column = [0 : 3])
            translate([column * 30.0, row * 78.0, 0])
                registration_tab();
}

module installed_registration_guides() {
    color([0.96, 0.47, 0.10, 0.90])
        for (x_side = [0, frame_outer.x])
            for (y_side = [0, frame_outer.y]) {
                // One flat tab on each exterior post face.  Their upper 12 mm
                // form an open lead-in; aluminum top faces carry stack weight.
                translate([x_side == 0 ? -registration_tab_size.z :
                                         frame_outer.x,
                           y_side == 0 ? 0 : frame_outer.y - profile_size,
                           registration_guide_bottom])
                    cube([registration_tab_size.z,
                          profile_size,
                          registration_tab_size.y]);
                translate([x_side == 0 ? 0 : frame_outer.x - profile_size,
                           y_side == 0 ? -registration_tab_size.z :
                                         frame_outer.y,
                           registration_guide_bottom])
                    cube([profile_size,
                          registration_tab_size.z,
                          registration_tab_size.y]);
            }
}

module placard_assembly_preview() {
    // Flat hanging straps bolt to the front slot at Z=390 and put the placard
    // holes at Z=354.  The complete sign remains beneath the top front rail,
    // faces the operator at the camera/front side, and never moves with
    // either payload gantry.
    color([0.94, 0.47, 0.10])
        for (x = [frame_outer.x / 2 - placard_hole_spacing / 2,
                  frame_outer.x / 2 + placard_hole_spacing / 2])
            translate([x,
                       -placard_spacer_thickness,
                       placard_riser_center_z])
                rotate([90, 0, 0])
                    rotate([0, 0, 180]) placard_riser();

    color([0.16, 0.28, 0.42])
        translate([frame_outer.x / 2,
                   -(placard_spacer_thickness + placard_riser_size.z),
                   placard_center_z])
            rotate([90, 0, 0]) device_id_placard();
    // Contrasting preview overlay; production remains one material/mesh and
    // can use a slicer filament change at the 3.2 mm text layer if desired.
    %color([0.96, 0.72, 0.12])
        translate([frame_outer.x / 2,
                   -(placard_spacer_thickness + placard_riser_size.z + 0.03),
                   placard_center_z])
            rotate([90, 0, 0])
                placard_text(placard_text_relief + 0.03);
}

module rail_fit_key(width, message) {
    base = [18.0, 24.0, 3.2];
    union() {
        linear_extrude(height = base.z)
            pf_rounded_rect_2d([base.x, base.y], 2.0);
        translate([0, 2.0, base.z])
            linear_extrude(height = min(extrusion_slot_depth - 0.6, 5.0))
                pf_rounded_rect_2d([width, 10.0], 0.8);
        translate([0, -6.0, base.z])
            linear_extrude(height = 0.8)
                text(message, size = 4.3,
                     font = "Liberation Sans:style=Bold",
                     halign = "center", valign = "center");
    }
}

module rail_fit_coupon() {
    widths = [extrusion_slot_opening - 0.50,
              extrusion_slot_opening - 0.30,
              extrusion_slot_opening - 0.10];
    for (index = [0 : 2])
        translate([index * 24.0, 0, 0])
            rail_fit_key(widths[index], str(widths[index]));
}

// Large end-loaded sliding T-nut bar.  This is intentionally a 60 mm handling
// bar, not a commercial-nut-sized nubbin: it nearly fills the delivered slot,
// cannot rotate, and is easy to position with a loose screw as a handle.  The
// broad flange bears behind the lips for its first 1.2 mm; above that, a
// pronounced keystone tapers toward the extrusion web.  It has no spring ears,
// printed threads, or sub-nozzle details.  Print the solid bearing face down
// and pull an ordinary M3 nut into the upward hex pocket with a screw and
// washer.  The open pocket faces the rail center.  The metal nut carries the
// thread; ABS only spreads light clamp load.  Never use this part for frame,
// stacking, or safety loads.
module m3_slide_nut_outline(body_width) {
    length = m3_slide_nut_length;
    chamfer = min(m3_slide_nut_corner_chamfer,
                  min(length, body_width) / 3);
    polygon([[-length / 2 + chamfer, -body_width / 2],
             [ length / 2 - chamfer, -body_width / 2],
             [ length / 2, -body_width / 2 + chamfer],
             [ length / 2,  body_width / 2 - chamfer],
             [ length / 2 - chamfer,  body_width / 2],
             [-length / 2 + chamfer,  body_width / 2],
             [-length / 2,  body_width / 2 - chamfer],
             [-length / 2, -body_width / 2 + chamfer]]);
}

module m3_slide_nut_carrier(
                            bearing_width = m3_slide_nut_bearing_width,
                            deep_width = m3_slide_nut_deep_width,
                            witness_notches = 0) {
    assert(bearing_width > extrusion_slot_opening,
           "Coupon slider bearing face must bridge the measured slot mouth");
    assert(bearing_width < extrusion_slot_pocket_width,
           "Coupon slider bearing face must fit inside the measured slot pocket");
    assert(deep_width >
           m3_nut_pocket_across_flats + 2 * 1.6,
           "Coupon slider needs printable deep-face walls around the nut");
    assert(deep_width < bearing_width,
           "Coupon slider must taper inward away from its bearing face");

    difference() {
        union() {
            // A full-width under-lip flange makes the section obvious and
            // spreads clamp load.  The body then tapers inward.  Both stages
            // print support-free because every layer is equal or smaller than
            // the one below it.
            linear_extrude(height = m3_slide_nut_flange_height)
                m3_slide_nut_outline(bearing_width);
            translate([0, 0, m3_slide_nut_flange_height])
                linear_extrude(
                    height = m3_slide_nut_height -
                             m3_slide_nut_flange_height,
                    scale = [1, deep_width / bearing_width])
                    m3_slide_nut_outline(bearing_width);
        }

        translate([0, 0, -epsilon])
            cylinder(d = m3_clearance,
                     h = m3_slide_nut_height + 2 * epsilon,
                     $fn = 28);

        translate([0, 0,
                   m3_slide_nut_height - m3_nut_pocket_depth])
            cylinder(d = m3_nut_pocket_across_flats / cos(30),
                     h = m3_nut_pocket_depth + epsilon,
                     $fn = 6);

        // Large end scallops survive a 0.8 mm nozzle.  One/two/three marks
        // identify 11.55/11.85/12.05 mm bearing widths after parts leave the
        // bed.
        if (witness_notches > 0)
            for (notch = [0 : witness_notches - 1])
                translate([m3_slide_nut_length / 2,
                           (notch - (witness_notches - 1) / 2) * 2.4,
                           -epsilon])
                    cylinder(d = 2.0,
                             h = m3_slide_nut_height + 2 * epsilon,
                             $fn = 20);
    }
}

module m3_slide_nut_carrier_set() {
    for (index = [0 : m3_slide_nut_set_count - 1])
        translate([(index % m3_slide_nut_set_columns) * 62.0,
                   floor(index / m3_slide_nut_set_columns) * 15.0,
                   0])
            m3_slide_nut_carrier();
}

// Six pieces are intentional: ABS gets enough inter-part cooling time even
// when the only requested output is a tiny fit test.  Two copies of each width
// also provide a repeatability check instead of trusting one lucky print.
module m3_slide_nut_fit_coupon() {
    for (index = [0 : len(m3_slide_nut_coupon_bearing_widths) - 1])
        for (copy = [0 : m3_slide_nut_coupon_copies - 1])
            translate([index * 64.0, copy * 15.0, 0])
                m3_slide_nut_carrier(
                    m3_slide_nut_coupon_bearing_widths[index],
                    m3_slide_nut_deep_width,
                    index + 1);
}

// Ready-to-slice production groups.  Every object is already in its
// documented support-free orientation and every group fits the conservative
// 247 x 207 mm Prusa envelope.  Individual exports remain available for
// replacement parts and fit-test iteration.
module print_group_calibration() {
    rail_fit_coupon();
    translate([0, 30.0, 0]) m3_slide_nut_fit_coupon();
}

module print_group_gantry_hardware() {
    gantry_joint_plate_set();
}

module print_group_nut_bars() {
    m3_slide_nut_carrier_set();
}

module print_group_gantry_splices() {
    gantry_splice_shell_set();
}

module print_group_plate_mounts() {
    plate_spacer_set();
    translate([110.0, 0, 0]) placard_riser_pair();
    translate([48.0, 45.0, 0]) placard_spacer_pair();
}

module print_group_stacking_guides() {
    registration_tab_set();
}

module print_group_device_label() {
    device_id_placard();
}

module cutlist_echo() {
    echo(str("PFCUT|outer_vertical_rail|4|", structural_z_length,
             "|between three-way end connectors"));
    echo(str("PFCUT|outer_width_rail|4|", structural_x_length,
             "|between three-way end connectors"));
    echo(str("PFCUT|outer_depth_rail|4|", structural_y_length,
             "|between three-way end connectors"));
    echo(str("PFCUT|plate_gantry_upright_half|8|",
             gantry_upright_segment_length,
             "|two offcut halves plus one clamshell form each upright"));
    echo(str("PFCUT|plate_gantry_crossbar|4|", gantry_crossbar_length,
             "|two height-adjustable crossbars per plate gantry"));
    echo(str("PFSTOCK|", stock_length, "|", cut_kerf,
             "|", join_topology));
}

module assembly(plate_detail = PLATE_DETAIL) {
    outer_frame();
    plate_gantries();
    if (SHOW_CONNECTOR_PROXIES) connector_proxies();
    if (SHOW_PLATES) {
        fixture_plate_preview(plate_detail);
        cradle_plate_preview(plate_detail);
        plate_mount_previews();
    }
    if (SHOW_DEVICE) device_and_camera_preview();
    if (SHOW_CAMERA_FRUSTUM) camera_frustum_preview();
    if (SHOW_REGISTRATION_GUIDES) installed_registration_guides();
    placard_assembly_preview();
}

module stacked_assembly() {
    assembly();
    // Second empty chassis proves that registration parts remain outside the
    // aluminum compression plane.  Its payload is intentionally omitted.
    translate([0, 0, frame_outer.z]) {
        outer_frame();
        if (SHOW_CONNECTOR_PROXIES) outer_corner_connector_proxies();
        if (SHOW_REGISTRATION_GUIDES) installed_registration_guides();
    }
}

if (PART == "assembly") {
    assembly();
} else if (PART == "presentation") {
    // Exact production plate and accepted installed-hook meshes plus
    // analytical overlays. In particular, the C270 frustum remains a separate,
    // visible CAD datum rather than being baked into an imported STL.
    assembly("mesh");
} else if (PART == "stacked_assembly") {
    stacked_assembly();
} else if (PART == "placard") {
    device_id_placard();
} else if (PART == "placard_riser") {
    placard_riser();
} else if (PART == "placard_riser_pair") {
    placard_riser_pair();
} else if (PART == "placard_spacer") {
    placard_spacer();
} else if (PART == "placard_spacer_pair") {
    placard_spacer_pair();
} else if (PART == "plate_spacer") {
    plate_spacer();
} else if (PART == "plate_spacer_set") {
    plate_spacer_set();
} else if (PART == "gantry_joint_plate") {
    gantry_joint_plate();
} else if (PART == "gantry_joint_plate_set") {
    gantry_joint_plate_set();
} else if (PART == "gantry_splice_shell") {
    gantry_splice_shell();
} else if (PART == "gantry_splice_shell_pair") {
    gantry_splice_shell_pair();
} else if (PART == "gantry_splice_shell_set") {
    gantry_splice_shell_set();
} else if (PART == "gantry_splice_coupon") {
    gantry_splice_fit_coupon();
} else if (PART == "registration_tab") {
    registration_tab();
} else if (PART == "registration_tab_set") {
    registration_tab_set();
} else if (PART == "rail_fit_coupon") {
    rail_fit_coupon();
} else if (PART == "m3_slide_nut") {
    m3_slide_nut_carrier();
} else if (PART == "m3_slide_nut_set") {
    m3_slide_nut_carrier_set();
} else if (PART == "m3_slide_nut_coupon") {
    m3_slide_nut_fit_coupon();
} else if (PART == "print_group_calibration") {
    print_group_calibration();
} else if (PART == "print_group_gantry_hardware") {
    print_group_gantry_hardware();
} else if (PART == "print_group_nut_bars") {
    print_group_nut_bars();
} else if (PART == "print_group_gantry_splices") {
    print_group_gantry_splices();
} else if (PART == "print_group_plate_mounts") {
    print_group_plate_mounts();
} else if (PART == "print_group_stacking_guides") {
    print_group_stacking_guides();
} else if (PART == "print_group_device_label") {
    print_group_device_label();
} else if (PART == "cutlist") {
    cutlist_echo();
    cube([0.1, 0.1, 0.1]);
} else {
    assert(false, str("Unknown PART: ", PART));
}
