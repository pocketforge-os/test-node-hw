/*
 * PocketForge standard 2020 DUT-node chassis.
 *
 * Coordinates: X left-to-right, Y camera-to-DUT (front-to-rear), Z upward.
 * The external frame envelope starts at [0, 0, 0].  All dimensions are mm.
 *
 * PART choices:
 *   assembly, presentation, stacked_assembly, corner_joint_detail, placard,
 *   placard_riser, placard_riser_pair,
 *   placard_spacer, placard_spacer_pair,
 *   plate_spacer, plate_spacer_set, registration_tab,
 *   registration_tab_set, gantry_joint_plate, gantry_joint_plate_set,
 *   rear_carrier_link_top, rear_carrier_link_bottom,
 *   rear_carrier_link_fit_pair, rear_carrier_link_set,
 *   gantry_splice_shell, gantry_splice_shell_pair,
 *   gantry_splice_shell_set, gantry_splice_internal_bar,
 *   gantry_splice_internal_bar_set, gantry_splice_test_set,
 *   gantry_splice_installed_preview,
 *   gantry_splice_coupon,
 *   rail_fit_coupon, m3_slide_nut, m3_slide_nut_set,
 *   m3_slide_nut_coupon, print_group_calibration,
 *   print_group_gantry_hardware, print_group_nut_bars,
 *   print_group_plate_mounts,
 *   print_group_stacking_guides, print_group_device_label,
 *   print_group_gantry_splices, print_group_gantry_splice_bars, cutlist
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
fixture_components_presentation_mesh =
    "build/imports/pocketforge-dut-fixture-components.stl";
fixture_labels_presentation_mesh =
    "build/imports/pocketforge-dut-fixture-labels.stl";
cradle_body_presentation_mesh =
    "build/imports/trimui-smart-pro-family-carrier-body.stl";
cradle_s_labels_presentation_mesh =
    "build/imports/trimui-smart-pro-s-labels.stl";
cradle_base_labels_presentation_mesh =
    "build/imports/trimui-smart-pro-labels.stl";
cradle_labels_presentation_mesh = EXAMPLE_DEVICE_VARIANT == "smart_pro_s" ?
                                  cradle_s_labels_presentation_mesh :
                                  cradle_base_labels_presentation_mesh;
cradle_hooks_presentation_mesh =
    "build/imports/trimui-smart-pro-family-installed-hooks.stl";

$fn = 48;
epsilon = 0.02;

// ---- Standard chassis contract ------------------------------------------
profile_size = 20.0;

// The delivered B08C9Q2TGW connector is a cap-and-two-tongue joint, not a
// 20 mm corner cube. Width/depth rails butt into the sides of the vertical
// posts. A physically cut 360.00 mm post with one connector at each end
// measures 368 mm outside-to-outside, so each cap contributes 4 mm beyond the
// aluminum. The horizontal rails terminate flush against adjacent faces of
// each vertical post; they do not overlap one another or pass through a
// fictitious 20 mm corner cube. The compact fleet standard deliberately uses
// a rectangular frame: 318 mm width rails retain 35.5 mm around the limiting
// 247 mm carrier, 306 mm depth rails preserve the C270 framing guard after the
// rear carrier is fixed to the outer frame, and the accepted 360 mm post is
// reused unchanged. The exact six-stick packer deliberately distributes the
// cuts so the shortest nominal remainder is 36.4 mm instead of relying on a
// risky 360 + 318 + 306 mm near-full-stick pattern.
structural_x_length = 318.0;
structural_y_length = 306.0;
structural_z_length = 360.0;
connector_end_overhang = 4.0;
frame_outer = [structural_x_length + 2 * profile_size,
               structural_y_length + 2 * profile_size,
               structural_z_length + 2 * connector_end_overhang];
frame_aluminum_z_min = connector_end_overhang;
frame_aluminum_z_max = frame_aluminum_z_min + structural_z_length;
// The horizontal-rail outer faces are flush with the connector-cap planes.
// They are not inset to the cut ends of the vertical aluminum posts.
outer_rail_z = [profile_size / 2,
                frame_outer.z - profile_size / 2];
frame_clear = [structural_x_length,
               structural_y_length,
               frame_outer.z - 2 * profile_size];
join_topology = "three_way_cap_flush_side_butt_B08C9Q2TGW_measured";

// SeekLiny B0DY7FKKMT is a nominal 20-series V-slot profile.  These interface
// dimensions come from the owner's delivered rail, not a generic "2020"
// drawing: A=mouth, B=depth, C=widest pocket, D=lip depth, E=web thickness,
// and F=the narrow channel face at the extrusion web.
extrusion_slot_opening = 6.73;
extrusion_slot_depth = 6.48;
extrusion_slot_pocket_width = 12.15;
extrusion_slot_lip_depth = 1.66;
extrusion_web_thickness = 1.20;
extrusion_slot_deep_width = 6.66;
extrusion_centre_bore = 4.2; // preview-only 20-series nominal

stock_length = 1000.0;
// Deliberately wide provisional allowance. The fullest selected pattern is
// 318 + 318 + 318 mm, so validation includes all three cut kerfs and retains
// 36.4 mm against a nominal 1 m stick. Measure actual stock and make a single
// witnessed test cut before batch cutting.
cut_kerf = 3.2;

// Only the electronics/webcam fixture needs a three-axis gantry. It adds two
// split vertical uprights and two continuous horizontal crossbars. The DUT
// carrier is fixed directly to the rear outer width rails with printed links;
// its device-specific CAD already puts every screen on the shared optical
// datum. The cap-flush top/bottom depth rails leave a 328 mm clear upright.
// Keeping the uprights in the outer depth-rail X planes makes the end joints
// flat; their 164 mm halves pack into the six-stick plan.
gantry_crossbar_length = structural_x_length;
gantry_upright_length = frame_clear.z;
gantry_upright_segment_count = 2;
gantry_upright_segment_length = gantry_upright_length /
                                gantry_upright_segment_count;
gantry_clear_z_min = outer_rail_z.x + profile_size / 2;
gantry_clear_z_max = outer_rail_z.y - profile_size / 2;
gantry_upright_splice_z = gantry_clear_z_min +
                          gantry_upright_segment_length;
gantry_upright_x = [profile_size / 2,
                    frame_outer.x - profile_size / 2];
gantry_y_limits = [profile_size + profile_size / 2,
                   frame_outer.y - profile_size - profile_size / 2];

// ---- Existing plate interfaces and optical registration -----------------
fixture_plate_size = [200.0, 247.0, 3.2];
fixture_webcam_datum = [100.0, 132.0];
fixture_slot_inset = [19.0, 8.0];

cradle_plate_size = [247.0, 200.0, 3.2];
cradle_screen_datum = [123.5, 100.0];
cradle_slot_inset = [19.0, 8.0];

// Center the taller 247 mm fixture plate inside the 328 mm clear height while
// preserving its measured webcam datum. The carrier then shares that optical
// axis and retains even more vertical service margin.
optical_datum_z = gantry_clear_z_min +
                  (frame_clear.z - fixture_plate_size.y) / 2 +
                  fixture_webcam_datum.y;
optical_datum = [frame_outer.x / 2, optical_datum_z]; // [X, Z]
plate_mount_gap = 5.0;
fixture_front_service_gap = 5.0;

// Mount the fixture board on the front side of its movable gantry. Its front
// face retains 5 mm behind the front outer rail, while the C270 body can pass
// harmlessly between the two widely separated crossbars. The rear carrier is
// fixed 5 mm ahead of the rear outer width rails by four printed links.
fixture_gantry_y = profile_size + fixture_front_service_gap +
                   fixture_plate_size.z + plate_mount_gap +
                   profile_size / 2;
rear_carrier_rail_y = frame_outer.y - profile_size / 2;

// Moving the fixture gantry changes camera distance without changing the
// fixed carrier or its optical registration.
fixture_plane_y = fixture_gantry_y - profile_size / 2 - plate_mount_gap;
fixture_origin = [optical_datum.x - fixture_webcam_datum.x,
                  fixture_plane_y,
                  optical_datum.y - fixture_webcam_datum.y];

// The DUT carrier's hooks/device face -Y toward the webcam.
cradle_plane_y = rear_carrier_rail_y - profile_size / 2 - plate_mount_gap;
cradle_origin = [optical_datum.x - cradle_screen_datum.x,
                 cradle_plane_y,
                 optical_datum.y - cradle_screen_datum.y];

fixture_crossbar_z = [fixture_origin.z + fixture_slot_inset.y,
                      fixture_origin.z + fixture_plate_size.y -
                      fixture_slot_inset.y];
fixture_mount_x = [fixture_origin.x + fixture_slot_inset.x,
                   fixture_origin.x + fixture_plate_size.x -
                   fixture_slot_inset.x];
cradle_mount_x = [cradle_origin.x + cradle_slot_inset.x,
                  cradle_origin.x + cradle_plate_size.x -
                  cradle_slot_inset.x];
cradle_mount_z = [cradle_origin.z + cradle_slot_inset.y,
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
camera_coverage = [2 * optical_distance * tan(camera_assumed_hfov / 2),
                   2 * optical_distance * tan(camera_assumed_vfov / 2)];
camera_edge_margin = [(camera_coverage.x - device_body.x) / 2,
                      (camera_coverage.y - device_body.y) / 2];

// ---- Printable interface parameters -------------------------------------
m3_clearance = 3.6;
m5_clearance = 5.5;
spacer_size = [18.0, 14.0];
spacer_corner_radius = 2.0;
plate_spacer_thickness = plate_mount_gap;

// Four broad-face-down ABS links fix the carrier to the rear outer width
// rails. Two upper links carry the light plate; two lower links prevent swing
// and racking. A round, keyed rail hole is the dimensional datum. The carrier
// end has 10 mm of vertical adjustment and clamps through the carrier's
// existing corner slot with an ordinary metal M3 nut and wide washers.
rear_carrier_link_width = 18.0;
rear_carrier_link_end_margin = 12.0;
rear_carrier_link_thickness = plate_mount_gap;
rear_carrier_link_adjustment = 10.0;
rear_carrier_link_key_length = 12.0;
rear_carrier_bottom_span = cradle_mount_z.x - outer_rail_z.x;
rear_carrier_top_span = outer_rail_z.y - cradle_mount_z.y;
rear_carrier_bottom_length = rear_carrier_bottom_span +
                             2 * rear_carrier_link_end_margin;
rear_carrier_top_length = rear_carrier_top_span +
                          2 * rear_carrier_link_end_margin;
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
m3_slide_nut_length = 30.0;
m3_slide_nut_bearing_width = 11.75;
// Owner physically accepted both pass-3 bars on 2026-07-22. The wider,
// two-scallop 6.46 mm candidate is the production profile because it retains
// the most bearing material while still travelling freely in the real rail.
m3_slide_nut_deep_width = 6.46;
m3_slide_nut_height = 4.40;
m3_slide_nut_flange_height = 0.40;
m3_slide_nut_corner_chamfer = 3.0;
// Third physical pass: the 11.75 mm bearing face reaches the under-lip pocket,
// but the shared 8.90 mm deep face collided with the rail and its delayed
// taper did not follow the channel.  F measures 6.66 mm; the two candidates
// bracket the same -0.30 mm process compensation selected by the rail coupon.
m3_slide_nut_coupon_deep_widths = [6.26, 6.46];
m3_slide_nut_coupon_copies = 1;
m3_slide_nut_required_count = 18; // 8 gantry + 4 fixture + 4 carrier + 2 placard
m3_slide_nut_spare_count = 6;     // pre-load before rail ends are closed
m3_slide_nut_set_count = m3_slide_nut_required_count +
                         m3_slide_nut_spare_count;
m3_slide_nut_set_columns = 4;

function m3_slide_nut_width_at_height(
    z,
    bearing_width = m3_slide_nut_bearing_width,
    deep_width = m3_slide_nut_deep_width
) = z <= m3_slide_nut_flange_height ? bearing_width :
    bearing_width + (deep_width - bearing_width) *
    ((z - m3_slide_nut_flange_height) /
     (m3_slide_nut_height - m3_slide_nut_flange_height));

// Two non-structural fixture-gantry uprights are each made from two 164 mm
// stock-plan segments. One support-free four-piece splice aligns each central
// butt joint:
// two broad external shells plus two long, channel-matched internal bars. The
// owner physically selected the one-notch 0.20 mm external clearance. Each bar
// captures one metal M3 nut in each rail half, so opposed shell/bar pairs bridge
// both the outside and inside without drilling aluminum or printing a tall
// closed sleeve.
gantry_splice_length = 80.0;
gantry_splice_wall = 4.8;
gantry_splice_wing_depth = 8.0;
gantry_splice_external_clearance = 0.20;
gantry_splice_inner_width = profile_size +
                             gantry_splice_external_clearance;
gantry_splice_fastener_x = 24.0;
gantry_splice_internal_bar_length = 80.0;
gantry_splice_internal_nut_x = [-gantry_splice_fastener_x,
                                 gantry_splice_fastener_x];
gantry_splice_internal_bar_count = 4; // two opposed bars x two uprights
gantry_splice_internal_bar_columns = 2;
gantry_splice_shell_count = 4; // two opposed shells x two uprights
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
placard_rail_mount_z = outer_rail_z.y;
placard_center_z = placard_rail_mount_z -
                   2 * placard_riser_hole_offset;
placard_riser_center_z = (placard_rail_mount_z + placard_center_z) / 2;

registration_tab_size = [24.0, 72.0, 4.0];
registration_above_frame = 12.0;
registration_lower_slot = [9.0, m5_clearance];
registration_lower_hole_y = [12.0, 28.0];
registration_upper_lock_y = 66.0;

// ---- Derived-fit guards --------------------------------------------------
minimum_routing_margin = 35.0;
inner_min = [profile_size, gantry_clear_z_min];
inner_max = [frame_outer.x - profile_size,
             gantry_clear_z_max];
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
assert(frame_outer == [structural_x_length + 2 * profile_size,
                       structural_y_length + 2 * profile_size,
                       structural_z_length +
                           2 * connector_end_overhang],
       "Frame envelope must derive from the measured cap-and-side-butt joint");
assert(outer_rail_z.x - profile_size / 2 == 0 &&
       outer_rail_z.y + profile_size / 2 == frame_outer.z,
       "Horizontal rail outer faces must be flush with both connector caps");
assert(min(fixture_margins) >= minimum_routing_margin,
       str("Fixture routing margin fell below ", minimum_routing_margin,
           " mm: ", fixture_margins));
assert(min(cradle_margins) >= minimum_routing_margin,
       str("Cradle routing margin fell below ", minimum_routing_margin,
           " mm: ", cradle_margins));
assert(fixture_gantry_y >= gantry_y_limits.x &&
       fixture_gantry_y <= gantry_y_limits.y,
       str("Fixture gantry Y is outside legal travel: ", fixture_gantry_y));
assert(fixture_plane_y - fixture_plate_size.z - profile_size >=
       fixture_front_service_gap,
       "Fixture board must clear the rear face of the front outer rail");
assert((rear_carrier_rail_y - profile_size / 2) - cradle_plane_y ==
       plate_mount_gap,
       "Rear carrier links must bridge the declared rail-to-plate gap");
assert(frame_outer.y - cradle_plane_y >= 25.0,
       "Rear carrier must retain approximately one inch of cable service space");
assert(gantry_upright_segment_count == 2 &&
       2 * gantry_upright_segment_length == gantry_upright_length,
       "Each movable gantry upright must be two equal offcut segments");
assert(gantry_splice_length < gantry_upright_segment_length,
       "Upright splice must leave exposed aluminum on both segments");
assert(min([for (z = fixture_crossbar_z)
                abs(z - gantry_upright_splice_z)]) >=
       gantry_splice_length / 2 + profile_size / 2,
       "Central upright splice must not collide with a plate crossbar");
assert(min(fixture_crossbar_z) >= gantry_clear_z_min + profile_size / 2 &&
       max(fixture_crossbar_z) <= gantry_clear_z_max - profile_size / 2,
       str("Fixture crossbar Z is outside gantry travel: ",
           fixture_crossbar_z));
assert(rear_carrier_bottom_span > rear_carrier_link_adjustment &&
       rear_carrier_top_span > rear_carrier_link_adjustment,
       "Rear carrier links need positive spans beyond their adjustment slots");
assert(rear_carrier_link_key_length > m3_clearance &&
       slot_key_width > m3_clearance,
       "Rear carrier rail key must retain printable material around M3");
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
       m3_nut_pocket_across_flats + 0.5,
       "Deep face must clear the metal nut across flats");
assert(m3_slide_nut_deep_width < extrusion_slot_deep_width,
       "Deep face must clear measured rail dimension F");
assert(m3_slide_nut_deep_width < m3_slide_nut_bearing_width,
       "End-loaded carrier must taper inward away from its bearing face");
assert(min(m3_slide_nut_coupon_deep_widths) >
           m3_nut_pocket_across_flats + 0.5 &&
       max(m3_slide_nut_coupon_deep_widths) < extrusion_slot_deep_width,
       "Every coupon deep face must clear both nut and measured rail");
assert(len(m3_slide_nut_coupon_deep_widths) *
       m3_slide_nut_coupon_copies == 2,
       "Third-pass nut-bar coupon must contain exactly two pieces");
assert(m3_slide_nut_height <
       extrusion_slot_depth - extrusion_slot_lip_depth,
       "End-loaded carrier must fit behind the measured slot lip");
assert(m3_slide_nut_flange_height > 0 &&
       m3_slide_nut_flange_height < m3_slide_nut_height,
       "Nut-bar bearing flange must fit inside its total channel depth");
assert(m3_slide_nut_length >= 24.0,
       "End-loaded carrier must retain useful nut walls and handling length");
assert(m3_slide_nut_height - m3_nut_pocket_depth >= 1.6,
       "End-loaded carrier needs at least four 0.4 mm floor layers");
assert(m3_slide_nut_width_at_height(
           m3_slide_nut_height - m3_nut_pocket_depth) >=
       m3_nut_pocket_across_flats + 2 * 1.6,
       "Nut-pocket floor needs two printable side walls");
assert(gantry_splice_inner_width > profile_size,
       "Splice clamshell needs positive external rail clearance");
assert(2 * gantry_splice_wing_depth < profile_size,
       "Opposed splice-shell wings need a service gap");
assert(gantry_splice_fastener_x + m3_clearance / 2 <
       gantry_splice_length / 2,
       "Splice fasteners must remain inside the shell length");
assert(gantry_splice_internal_bar_length == gantry_splice_length,
       "Internal splice bar and external shell must bridge the same seam");
assert(max([for (x = gantry_splice_internal_nut_x) abs(x)]) +
           m3_nut_pocket_across_flats / 2 <
       gantry_splice_internal_bar_length / 2,
       "Internal splice nuts need printable end walls");
assert(len(gantry_splice_fit_clearances) * gantry_splice_fit_copies >= 6,
       "Small ABS splice-fit batches need at least six parts for cooling");
assert(gantry_joint_plate_size.x > gantry_joint_key_length &&
       gantry_joint_plate_size.y >
       2 * gantry_joint_hole_offset + gantry_joint_slot.y,
       "Gantry joint plate must surround both keyed fastener interfaces");
assert(placard_center_z + placard_size.y / 2 <
       outer_rail_z.y - profile_size / 2,
       "Front placard must remain completely below the top front rail");
assert(registration_above_frame > 0 &&
       registration_above_frame < profile_size,
       "Registration guide must engage, but not exceed, one upper post width");
registration_guide_bottom = frame_outer.z -
                            (registration_tab_size.y -
                             registration_above_frame);
assert(registration_guide_bottom + max(registration_lower_hole_y) <
       outer_rail_z.y - profile_size / 2,
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
    // The vertical posts are the stems of the delivered three-way joints.
    // Connector caps add 4 mm beyond each aluminum end.
    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
            translate([x, y, frame_aluminum_z_min])
                extrusion(structural_z_length, "z");

    // Width and depth rails butt into the post side faces. Their top/bottom
    // outer faces align with the connector-cap planes, with zero Z inset.
    for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
        for (z = outer_rail_z)
            translate([profile_size, y, z])
                extrusion(structural_x_length, "x");

    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        for (z = outer_rail_z)
            translate([x, profile_size, z])
                extrusion(structural_y_length, "y");
}

module fixture_gantry() {
    // Uprights share the X planes of the outer depth rails.  This lets one
    // flat keyed plate bridge each T joint while the complete gantry slides
    // anywhere along the depth-rail slots.
    for (x = gantry_upright_x)
        for (segment = [0 : gantry_upright_segment_count - 1])
            translate([x, fixture_gantry_y,
                       gantry_clear_z_min +
                       segment * gantry_upright_segment_length])
                extrusion(gantry_upright_segment_length, "z");

    // Concealed metal L-connectors let each crossbar slide vertically on the
    // uprights; plate fasteners then slide horizontally in these crossbars.
    for (z = fixture_crossbar_z)
        translate([profile_size, fixture_gantry_y, z])
            extrusion(gantry_crossbar_length, "x");
}

module three_way_end_connector_proxy(x_right = false,
                                     y_rear = false,
                                     top = false) {
    // BLCCLOY B08C9Q2TGW proxy corrected from the physical joint: a square cap
    // sits on the vertical-post end and two thin tongues run inward along the
    // width/depth rail slots. Fine ribs and M4 set screws are omitted.
    cap_thickness = connector_end_overhang;
    tongue_length = 28.0;
    tongue_width = 8.0;
    tongue_thickness = 3.2;
    x0 = x_right ? frame_outer.x - profile_size : 0;
    y0 = y_rear ? frame_outer.y - profile_size : 0;
    cap_z = top ? frame_aluminum_z_max : 0;
    tongue_z = top ? frame_aluminum_z_max - tongue_thickness :
                     frame_aluminum_z_min;
    color([0.08, 0.08, 0.09]) {
        translate([x0, y0, cap_z])
            cube([profile_size, profile_size, cap_thickness]);

        translate([x_right ? x0 - tongue_length : x0 + profile_size,
                   y0 + (profile_size - tongue_width) / 2,
                   tongue_z])
            cube([tongue_length, tongue_width, tongue_thickness]);

        translate([x0 + (profile_size - tongue_width) / 2,
                   y_rear ? y0 - tongue_length : y0 + profile_size,
                   tongue_z])
            cube([tongue_width, tongue_length, tongue_thickness]);
    }
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
    for (x_right = [false, true])
        for (y_rear = [false, true])
            for (top = [false, true])
                three_way_end_connector_proxy(x_right, y_rear, top);
}

module gantry_crossbar_connector_proxies() {
    for (z = fixture_crossbar_z)
        for (right = [false, true])
            gantry_l_connector_proxy(fixture_gantry_y, z, right);
}

module installed_gantry_joint_plate(y, top = false, right = false) {
    joint_z = top ? gantry_clear_z_max : gantry_clear_z_min;
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
        for (top = [false, true])
            for (right = [false, true])
                installed_gantry_joint_plate(fixture_gantry_y, top, right);
}

module fixture_mesh_at_installed_datum(mesh_path) {
    translate(fixture_origin)
        rotate([90, 0, 0])
            import(mesh_path, convexity = 10);
}

module fixture_plate_preview(detail = PLATE_DETAIL) {
    if (detail == "mesh") {
        color([0.90, 0.90, 0.86])
            fixture_mesh_at_installed_datum(fixture_presentation_mesh);

        // Presentation-only populated harness geometry is exported separately
        // from the fixture source. It remains impossible to leak these
        // component envelopes into the production fixture STL.
        color([0.16, 0.28, 0.38])
            fixture_mesh_at_installed_datum(
                fixture_components_presentation_mesh);
        color([0.08, 0.48, 0.32])
            fixture_mesh_at_installed_datum(
                fixture_labels_presentation_mesh);
    } else {
        color([0.90, 0.90, 0.86])
            translate([fixture_origin.x,
                       fixture_origin.y - fixture_plate_size.z,
                       fixture_origin.z])
                cube([fixture_plate_size.x,
                      fixture_plate_size.z,
                      fixture_plate_size.y]);
    }
}

module cradle_mesh_at_installed_datum(mesh_path) {
    translate(cradle_origin)
        rotate([90, 0, 0])
            import(mesh_path, convexity = 10);
}

module cradle_plate_preview(detail = PLATE_DETAIL) {
    if (detail == "mesh") {
        color([0.88, 0.88, 0.84])
            cradle_mesh_at_installed_datum(cradle_body_presentation_mesh);

        // The physical carrier changes filament at the first raised-label
        // layer.  Separate touching meshes preserve that exact black material
        // region without overlaying coincident faces on a unified STL.
        color([0.02, 0.02, 0.02])
            cradle_mesh_at_installed_datum(
                cradle_labels_presentation_mesh);

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

module installed_fixture_plate_spacer(point) {
    color([0.95, 0.53, 0.12])
        translate([point.x - spacer_size.x / 2,
                   fixture_plane_y,
                   point.y - spacer_size.y / 2])
            cube([spacer_size.x, plate_spacer_thickness, spacer_size.y]);
}

module installed_rear_carrier_link(x, plate_z, rail_z) {
    span = abs(rail_z - plate_z);
    center_z = (rail_z + plate_z) / 2;
    rail_above = rail_z > plate_z;

    color([0.95, 0.53, 0.12])
        multmatrix(rail_above ? [
            [1, 0, 0, x],
            [0, 0, 1, cradle_plane_y],
            [0, 1, 0, center_z],
            [0, 0, 0, 1]
        ] : [
            [1, 0, 0, x],
            [0, 0, 1, cradle_plane_y],
            [0, -1, 0, center_z],
            [0, 0, 0, 1]
        ]) rear_carrier_link(span);
}

module plate_mount_previews() {
    for (x = fixture_mount_x)
        for (z = fixture_crossbar_z)
            installed_fixture_plate_spacer([x, z]);

    for (x = cradle_mount_x)
        for (index = [0, 1])
            installed_rear_carrier_link(x, cradle_mount_z[index],
                                        outer_rail_z[index]);
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
        for (column = [0, 1])
            translate([column * 24.0, row * 20.0, 0]) plate_spacer();
}

// Parametric fixed rear-carrier link. Local -Y is the carrier end; local +Y
// is the rear-rail end. The rail end carries the same physically validated
// 6.43 mm registration key used elsewhere. The base and key only get smaller
// as Z rises, so the exported orientation is support-free.
module rear_carrier_link(span) {
    link_length = span + 2 * rear_carrier_link_end_margin;
    rail_hole_y = span / 2;
    carrier_hole_y = -span / 2;

    assert(span > rear_carrier_link_adjustment,
           "Rear carrier link span is too short for its adjustment slot");

    difference() {
        union() {
            linear_extrude(height = rear_carrier_link_thickness)
                pf_rounded_rect_2d([rear_carrier_link_width,
                                    link_length], 2.5);
            translate([0, rail_hole_y,
                       rear_carrier_link_thickness - epsilon])
                linear_extrude(height = slot_key_height + epsilon)
                    pf_rounded_rect_2d(
                        [rear_carrier_link_key_length,
                         slot_key_width], 1.0);
        }

        translate([0, rail_hole_y, -epsilon])
            cylinder(d = m3_clearance,
                     h = rear_carrier_link_thickness +
                         slot_key_height + 2 * epsilon,
                     $fn = 28);

        translate([0, carrier_hole_y, -epsilon])
            linear_extrude(height = rear_carrier_link_thickness +
                                    2 * epsilon)
                rotate(90)
                    pf_capsule_2d(rear_carrier_link_adjustment,
                                  m3_clearance);
    }
}

module rear_carrier_link_top() {
    rear_carrier_link(rear_carrier_top_span);
}

module rear_carrier_link_bottom() {
    rear_carrier_link(rear_carrier_bottom_span);
}

module rear_carrier_link_set() {
    for (copy = [0, 1]) {
        translate([copy * 24.0, 0, 0]) rear_carrier_link_top();
        translate([48.0 + copy * 24.0, 0, 0])
            rear_carrier_link_bottom();
    }
}

module rear_carrier_link_fit_pair() {
    translate([0, 0, 0]) rear_carrier_link_top();
    translate([24.0, 0, 0]) rear_carrier_link_bottom();
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
        for (column = [0, 1])
            translate([column * (gantry_joint_plate_size.x + 6.0),
                       row * (gantry_joint_plate_size.y + 6.0), 0])
                gantry_joint_plate();
}

// One half of a support-free external clamshell for the central butt joint in
// a gantry upright. Two identical halves oppose each other on the rail. Each
// has two M3 clearance holes that pull against a channel-matched internal bar;
// one metal nut lands in each rail segment. The shallow rail key and side
// wings align the seam while the inside/outside bridges resist bending.
module gantry_splice_shell(clearance = gantry_splice_external_clearance,
                           shell_length = gantry_splice_length,
                           with_fastener_holes = true,
                           witness_notches = 0) {
    inner_width = profile_size + clearance;
    outer_width = inner_width + 2 * gantry_splice_wall;

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
        }

        if (with_fastener_holes)
            for (x = gantry_splice_internal_nut_x)
                translate([x, 0, -epsilon])
                    cylinder(d = m3_clearance,
                             h = gantry_splice_wall + slot_key_height +
                                 2 * epsilon,
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

// A long version of the physically accepted 11.75 / 6.46 mm M3 nut bar.
// It slides halfway into the first open rail, the second rail slides over its
// exposed half, and its two metal nuts land on opposite sides of the seam.
// Print the broad bearing face down exactly like the accepted 30 mm bars.
module gantry_splice_internal_bar() {
    m3_slide_nut_carrier(
        m3_slide_nut_bearing_width,
        m3_slide_nut_deep_width,
        0,
        gantry_splice_internal_bar_length,
        gantry_splice_internal_nut_x);
}

module gantry_splice_internal_bar_set() {
    for (index = [0 : gantry_splice_internal_bar_count - 1])
        translate([(index % gantry_splice_internal_bar_columns) *
                       (gantry_splice_internal_bar_length + 4.0),
                   floor(index / gantry_splice_internal_bar_columns) *
                       15.0, 0])
            gantry_splice_internal_bar();
}

module gantry_splice_shell_pair() {
    translate([0, -25.0, 0]) gantry_splice_shell();
    translate([0,  25.0, 0]) gantry_splice_shell();
}

module gantry_splice_shell_set() {
    for (index = [0 : gantry_splice_shell_count - 1])
        translate([(index % 2) * 82.0,
                   floor(index / 2) * 49.0, 0])
            gantry_splice_shell();
}

// One complete physical-validation joint: two opposed external shells and two
// internal double-nut bars. All four pieces lie broad-face down; no supports
// and no vertically printed sleeve are required.
module gantry_splice_test_set() {
    translate([0, -25.0, 0]) gantry_splice_shell();
    translate([0,  25.0, 0]) gantry_splice_shell();
    translate([95.0, -9.0, 0]) gantry_splice_internal_bar();
    translate([95.0,  9.0, 0]) gantry_splice_internal_bar();
}

// Cutaway-style visual proof of the assembled load path. The two 60 mm rail
// fragments are translucent and meet at X=0; both 80 mm bars visibly bridge
// that seam inside opposite channels while the selected shells bridge it
// outside. This is a presentation part only and must never be exported for
// printing.
module gantry_splice_installed_preview() {
    demo_rail_half = 60.0;
    rail_center_z = gantry_splice_wall + profile_size / 2;
    internal_bar_z = gantry_splice_wall + extrusion_slot_lip_depth;

    color([0.12, 0.38, 0.70, 0.42]) {
        gantry_splice_shell();
        translate([0, 0, 2 * rail_center_z])
            mirror([0, 0, 1]) gantry_splice_shell();
    }

    color([0.68, 0.71, 0.75, 0.20]) {
        translate([-demo_rail_half, 0, rail_center_z])
            extrusion(demo_rail_half, "x");
        translate([0, 0, rail_center_z])
            extrusion(demo_rail_half, "x");
    }

    // Draw the internal bars last as an X-ray overlay so their hidden seam
    // bridge remains legible in the generated OpenCSG preview.
    #color([0.96, 0.52, 0.08]) {
        translate([0, 0, internal_bar_z])
            gantry_splice_internal_bar();
        translate([0, 0, 2 * rail_center_z])
            mirror([0, 0, 1])
                translate([0, 0, internal_bar_z])
                    gantry_splice_internal_bar();
    }

}

// Six short U sections calibrated the external 2020 face width. The owner's
// one-notch 0.20 mm sample fit perfectly and now controls production.
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
        for (x = gantry_upright_x)
            for (front = [false, true])
                installed_gantry_splice_half(x, fixture_gantry_y, front);
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
    // Flat hanging straps bolt to the front slot at Z=354 and put the placard
    // holes at Z=318.  The complete sign remains beneath the top front rail,
    // faces the operator at the camera/front side, and never moves with
    // the movable fixture gantry.
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

// Large end-loaded sliding T-nut bar.  This is intentionally a 30 mm handling
// bar, not a commercial-nut-sized nubbin: it nearly fills the delivered slot,
// cannot rotate, and is easy to position with a loose screw as a handle.  The
// bearing face gets one 0.4 mm print layer before a rail-matched keystone
// tapers toward measured dimension F at the extrusion web. It has no spring ears,
// printed threads, or sub-nozzle details.  Print the solid bearing face down
// and pull an ordinary M3 nut into the upward hex pocket with a screw and
// washer.  The open pocket faces the rail center.  The metal nut carries the
// thread; ABS only spreads light clamp load.  Never use this part for frame,
// stacking, or safety loads.
module m3_slide_nut_outline(body_width,
                            length = m3_slide_nut_length) {
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
                            witness_notches = 0,
                            length = m3_slide_nut_length,
                            nut_positions = [0]) {
    pocket_floor_z = m3_slide_nut_height - m3_nut_pocket_depth;
    pocket_floor_width =
        pocket_floor_z <= m3_slide_nut_flange_height ? bearing_width :
        bearing_width + (deep_width - bearing_width) *
        ((pocket_floor_z - m3_slide_nut_flange_height) /
         (m3_slide_nut_height - m3_slide_nut_flange_height));

    assert(bearing_width > extrusion_slot_opening,
           "Coupon slider bearing face must bridge the measured slot mouth");
    assert(bearing_width < extrusion_slot_pocket_width,
           "Coupon slider bearing face must fit inside the measured slot pocket");
    assert(deep_width >
           m3_nut_pocket_across_flats + 0.5,
           "Coupon deep face must clear the metal nut");
    assert(deep_width < extrusion_slot_deep_width,
           "Coupon deep face must clear measured rail dimension F");
    assert(deep_width < bearing_width,
           "Coupon slider must taper inward away from its bearing face");
    assert(pocket_floor_width >=
           m3_nut_pocket_across_flats + 2 * 1.6,
           "Coupon nut-pocket floor needs two printable side walls");
    assert(min([for (x = nut_positions)
                    length / 2 - abs(x) -
                    m3_nut_pocket_across_flats / 2]) >= 3.0,
           "Every captured nut needs a printable end wall");

    difference() {
        union() {
            // A full-width under-lip flange makes the section obvious and
            // spreads clamp load.  The body then tapers inward.  Both stages
            // print support-free because every layer is equal or smaller than
            // the one below it.
            linear_extrude(height = m3_slide_nut_flange_height)
                m3_slide_nut_outline(bearing_width, length);
            translate([0, 0, m3_slide_nut_flange_height])
                linear_extrude(
                    height = m3_slide_nut_height -
                             m3_slide_nut_flange_height,
                    scale = [1, deep_width / bearing_width])
                    m3_slide_nut_outline(bearing_width, length);
        }

        for (x = nut_positions) {
            translate([x, 0, -epsilon])
                cylinder(d = m3_clearance,
                         h = m3_slide_nut_height + 2 * epsilon,
                         $fn = 28);

            translate([x, 0,
                       m3_slide_nut_height - m3_nut_pocket_depth])
                cylinder(d = m3_nut_pocket_across_flats / cos(30),
                         h = m3_nut_pocket_depth + epsilon,
                         $fn = 6);
        }

        // Large end scallops survive a 0.8 mm nozzle. One/two marks identify
        // 6.26/6.46 mm deep-face widths after parts leave the
        // bed.
        if (witness_notches > 0)
            for (notch = [0 : witness_notches - 1])
                translate([length / 2,
                           (notch - (witness_notches - 1) / 2) * 2.4,
                           -epsilon])
                    cylinder(d = 2.0,
                             h = m3_slide_nut_height + 2 * epsilon,
                             $fn = 20);
    }
}

module m3_slide_nut_carrier_set() {
    for (index = [0 : m3_slide_nut_set_count - 1])
        translate([(index % m3_slide_nut_set_columns) *
                       (m3_slide_nut_length + 2.0),
                   floor(index / m3_slide_nut_set_columns) * 15.0,
                   0])
            m3_slide_nut_carrier();
}

// The 30 mm bars have enough layer time for the owner's ABS process, so this
// third pass needs only one of each bracketing deep-face width.
module m3_slide_nut_fit_coupon() {
    for (index = [0 : len(m3_slide_nut_coupon_deep_widths) - 1])
        for (copy = [0 : m3_slide_nut_coupon_copies - 1])
            translate([index * (m3_slide_nut_length + 4.0),
                       copy * 15.0, 0])
                m3_slide_nut_carrier(
                    m3_slide_nut_bearing_width,
                    m3_slide_nut_coupon_deep_widths[index],
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

module print_group_gantry_splice_bars() {
    gantry_splice_internal_bar_set();
}

module print_group_plate_mounts() {
    plate_spacer_set();
    translate([80.0, 0, 0]) placard_riser_pair();
    translate([45.0, 45.0, 0]) placard_spacer_pair();
    translate([125.0, 65.0, 0]) rear_carrier_link_set();
}

module print_group_stacking_guides() {
    registration_tab_set();
}

module print_group_device_label() {
    device_id_placard();
}

module cutlist_echo() {
    echo(str("PFFRAME|", frame_outer.x, "|", frame_outer.y, "|",
             frame_outer.z, "|", frame_clear.x, "|", frame_clear.y, "|",
             frame_clear.z));
    echo(str("PFCUT|outer_vertical_rail|4|", structural_z_length,
             "|connector stem; measured caps add 4 mm per end"));
    echo(str("PFCUT|outer_width_rail|4|", structural_x_length,
             "|butts between vertical-post side faces"));
    echo(str("PFCUT|outer_depth_rail|4|", structural_y_length,
             "|butts between vertical-post side faces"));
    echo(str("PFCUT|fixture_gantry_upright_half|4|",
             gantry_upright_segment_length,
             "|two halves plus reinforced splice form each fixture upright"));
    echo(str("PFCUT|fixture_gantry_crossbar|2|", gantry_crossbar_length,
             "|two height-adjustable fixture crossbars"));
    echo(str("PFSTOCK|", stock_length, "|", cut_kerf,
             "|", join_topology));
}

module assembly(plate_detail = PLATE_DETAIL) {
    outer_frame();
    fixture_gantry();
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

// Presentation-only close-up of the measured three-way corner topology. The
// vertical post owns the 20 x 20 mm corner footprint. Width and depth rails
// terminate flush against its two adjacent side faces, exactly as in the
// owner's assembled-corner photo; they never overlap each other.
module corner_joint_detail() {
    detail_length = 110.0;

    translate([profile_size / 2, profile_size / 2,
               frame_aluminum_z_min])
        extrusion(detail_length, "z");
    translate([profile_size, profile_size / 2, outer_rail_z.x])
        extrusion(detail_length, "x");
    translate([profile_size / 2, profile_size, outer_rail_z.x])
        extrusion(detail_length, "y");
    three_way_end_connector_proxy(false, false, false);
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
} else if (PART == "corner_joint_detail") {
    corner_joint_detail();
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
} else if (PART == "rear_carrier_link_top") {
    rear_carrier_link_top();
} else if (PART == "rear_carrier_link_bottom") {
    rear_carrier_link_bottom();
} else if (PART == "rear_carrier_link_fit_pair") {
    rear_carrier_link_fit_pair();
} else if (PART == "rear_carrier_link_set") {
    rear_carrier_link_set();
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
} else if (PART == "gantry_splice_internal_bar") {
    gantry_splice_internal_bar();
} else if (PART == "gantry_splice_internal_bar_set") {
    gantry_splice_internal_bar_set();
} else if (PART == "gantry_splice_test_set") {
    gantry_splice_test_set();
} else if (PART == "gantry_splice_installed_preview") {
    gantry_splice_installed_preview();
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
} else if (PART == "print_group_gantry_splice_bars") {
    print_group_gantry_splice_bars();
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
