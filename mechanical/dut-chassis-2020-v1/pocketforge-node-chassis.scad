/*
 * PocketForge standard 2020 test-node chassis.
 *
 * Coordinates: X left-to-right, Y camera-to-DUT (front-to-rear), Z upward.
 * The external frame envelope starts at [0, 0, 0].  All dimensions are mm.
 *
 * PART choices:
 *   assembly, presentation, stacked_assembly, corner_joint_detail, placard,
 *   placard_holder, placard_insert, placard_slide_fit_coupon,
 *   placard_system_preview,
 *   power_strip_mount_block, power_strip_mount_block_pair,
 *   power_strip_fit_coupon_set, power_strip_system_preview,
 *   ironing_test_coupon, ironing_test_coupon_set,
 *   placard_riser, placard_riser_pair,
 *   placard_spacer, placard_spacer_pair,
 *   plate_spacer, plate_spacer_set, registration_tab,
 *   registration_tab_set, gantry_joint_plate, gantry_joint_plate_set,
 *   rear_carrier_link_top, rear_carrier_link_bottom,
 *   rear_carrier_link_fit_pair, rear_carrier_link_set,
 *   gantry_splice_internal_bar,
 *   gantry_splice_full_collar,
 *   gantry_splice_full_collar_internal_bar,
 *   gantry_splice_full_collar_internal_bar_pair,
 *   gantry_splice_installed_preview,
 *   rail_fit_coupon, m3_slide_nut, m3_slide_nut_set,
 *   m3_slide_nut_coupon,
 *   production_batch_00_calibration,
 *   production_batch_01_ironed_interfaces,
 *   production_batch_02_splice_collars,
 *   production_batch_03_movable_mounts,
 *   production_batch_04_frame_hardware,
 *   production_batch_05_placard_holder,
 *   production_batch_06_device_nameplate,
 *   production_batch_06_device_nameplate_body,
 *   production_batch_06_device_nameplate_labels,
 *   production_batch_06_device_nameplate_preview,
 *   guide_step_01_splice_uprights, guide_step_02_build_gantry,
 *   guide_step_03_open_frame, guide_step_04_install_gantry,
 *   guide_step_05_close_frame, guide_step_06_mount_carrier,
 *   guide_step_07_mount_fixture, guide_step_08_complete,
 *   guide_preload_channel_bar, guide_preload_map,
 *   guide_layer_aluminum, guide_layer_connectors,
 *   guide_layer_printed_hardware, guide_layer_fixture_plate,
 *   guide_layer_fixture_components, guide_layer_fixture_labels,
 *   guide_layer_carrier_body, guide_layer_carrier_labels,
 *   guide_layer_carrier_hooks, guide_layer_device_shell,
 *   guide_layer_device_controls, guide_layer_device_screen,
 *   guide_layer_webcam, guide_layer_power_strip,
 *   guide_layer_placard_holder, guide_layer_placard_insert,
 *   guide_layer_camera_frustum, cutlist
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
SHOW_POWER_STRIP = true;

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
device_shell_presentation_mesh =
    "build/imports/trimui-smart-pro-device-shell.stl";
device_controls_presentation_mesh =
    "build/imports/trimui-smart-pro-device-controls.stl";
device_screen_presentation_mesh =
    "build/imports/trimui-smart-pro-device-screen.stl";

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
// a rectangular frame: the already-cut 306 mm rails become width rails and
// retain 29.5 mm on each side of the limiting 247 mm carrier; the already-cut
// 318 mm rails become depth rails, adding camera/cable space. The accepted
// 360 mm posts are reused unchanged. Only the two fixture crossbars are
// trimmed from their already-cut 318 mm length to the derived 306 mm width.
structural_x_length = 306.0;
structural_y_length = 318.0;
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
// Deliberately wide provisional allowance. It is retained for reproducible
// future-node stock planning even though node 1 reuses already-finished rails
// and needs only two 12 mm crossbar trim cuts.
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

// Direction contract—do not translate "front/back" into coordinates:
//   Y=0             = human/operator-side outer frame plane
//   increasing Y    = toward the DUT and wall
//   Y=frame_outer.y = wall-side outer frame plane
//
// The electronics/webcam gantry is intentionally advanced 45 mm wallward from
// its legal human-side stop. This leaves a real service bay between the
// operator-side rail and the populated board while retaining the complete DUT
// plus more than 10 mm on every edge in the conservative C270 model. The
// movable gantry remains the camera-distance adjustment; the DUT carrier stays
// fixed to the wall-side frame.
fixture_default_gantry_y = 75.0;
fixture_gantry_y = fixture_default_gantry_y;
rear_carrier_rail_y = frame_outer.y - profile_size / 2;
rear_carrier_service_gap = profile_size + plate_mount_gap;

// Moving the fixture gantry changes camera distance without changing the
// fixed carrier or its optical registration.
fixture_plane_y = fixture_gantry_y - profile_size / 2 - plate_mount_gap;
fixture_origin = [optical_datum.x - fixture_webcam_datum.x,
                  fixture_plane_y,
                  optical_datum.y - fixture_webcam_datum.y];
human_side_inner_face_y = profile_size;
fixture_human_service_depth =
    fixture_plane_y - fixture_plate_size.z - human_side_inner_face_y;

// The DUT carrier's hooks/device face -Y toward the webcam and human side.
cradle_plane_y = frame_outer.y - rear_carrier_service_gap;
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
// Only the complete device body is a hard framing requirement. Carrier
// orientation labels may crop. Ten millimetres is the asserted minimum on
// every edge; the derived default coverage remains larger in both axes.
framing_margin = [10.0, 10.0];
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

// Four broad-face-down ABS links fix the carrier to the wall-side outer width
// rails. Two upper links carry the light plate; two lower links prevent swing
// and racking. A round, keyed rail hole is the dimensional datum. The carrier
// end has 10 mm of vertical adjustment and clamps through the carrier's
// existing corner slot with an ordinary metal M3 nut and wide washers.
rear_carrier_link_width = 18.0;
rear_carrier_link_end_margin = 12.0;
rear_carrier_link_thickness =
    (rear_carrier_rail_y - profile_size / 2) - cradle_plane_y;
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
m3_slide_nut_required_count = 22; // +4 operator power-strip block fasteners
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
// stock-plan segments. One accepted full-wrap collar plus two long,
// channel-matched internal bars aligns each central butt joint. The owner
// physically validated the 0.20 mm collar clearance, self-indexing pusher, and
// corrected asymmetric bars. Each bar captures one metal M3 nut in each rail
// half, so the collar and opposed internal bars bridge the joint without
// drilling aluminum.
gantry_splice_length = 80.0;
gantry_splice_wall = 4.8;
gantry_splice_external_clearance = 0.20;
gantry_splice_inner_width = profile_size +
                             gantry_splice_external_clearance;
gantry_splice_fastener_x = 24.0;
gantry_splice_internal_bar_length = 80.0;
gantry_splice_internal_nut_x = [-gantry_splice_fastener_x,
                                 gantry_splice_fastener_x];
gantry_splice_internal_bar_count = 4; // two opposed bars x two uprights
gantry_splice_collar_hole_diameter = 4.2;
gantry_splice_collar_corner_relief = 2.4;
gantry_splice_collar_entry_relief = 0.8;
gantry_splice_collar_entry_depth = 1.2;
// Two opposed keys at the collar's trailing end act as a moving depth stop.
// Dimensions are multiples of the lab's 0.8 mm nozzle where practical.  The
// narrowed 1.6 mm lead-in avoids first-layer elephant-foot binding, while the
// full 6.43 mm section reuses the physically accepted slot-key fit.
gantry_splice_collar_pusher_length = 3.2;
gantry_splice_collar_pusher_depth = 2.4;
gantry_splice_collar_pusher_lead = 1.6;
gantry_splice_collar_pusher_tip_inset = 0.8;
// The pusher occupies the first 3.2 mm of the collar/rail span. A regular
// 80 mm bar therefore protrudes 3.2 mm into the rail butt joint and its holes
// cannot align. The collar-specific bar removes exactly that material from
// its pusher end while retaining the collar's established +/-24 mm hole
// datums. Its geometric center consequently sits 1.6 mm toward rail B.
gantry_splice_collar_internal_bar_length =
    gantry_splice_internal_bar_length - gantry_splice_collar_pusher_length;
gantry_splice_collar_internal_bar_center_offset =
    gantry_splice_collar_pusher_length / 2;
gantry_splice_collar_internal_nut_x =
    [for (x = gantry_splice_internal_nut_x)
        x - gantry_splice_collar_internal_bar_center_offset];

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

// Reusable fleet ID system. A 230 mm holder is the largest clean standard that
// fits the conservative 247 mm Prusa X envelope. Only the cartridge changes with
// the DUT. Long labels shrink deterministically; ordinary names retain the
// coarse-nozzle-proven 13.5 mm text instead of being stretched to fill space.
placard_size = [230.0, 38.0, 7.0];
placard_corner_radius = 4.0;
placard_hole_spacing = 190.0;
placard_text_nominal_size = 13.5;
placard_text_minimum_size = 8.5;
placard_text_horizontal_margin = 10.0;
placard_text_width_factor = 0.78;
placard_text_relief = 1.2;
placard_holder_base_thickness = 3.2;
placard_holder_rail_height = 3.8;
placard_holder_rail_lower_inner = 15.0;
placard_holder_rail_upper_inner = 13.2;
placard_holder_end_stop = 3.2;
placard_holder_rail_end_inset = placard_corner_radius;
placard_mount_countersink_diameter = 7.0;
placard_mount_countersink_depth = 2.2;
placard_insert_thickness = 2.4;
placard_insert_base_width = 29.0;
placard_insert_top_width = 25.6;
placard_insert_body_length = placard_size.x -
                             2 * placard_holder_rail_end_inset -
                             placard_holder_end_stop - 0.4;
placard_insert_body_center_x = placard_holder_end_stop / 2;
placard_insert_tab_size = [12.0, 12.0];
placard_insert_tab_overlap = 2.0;
placard_insert_pull_hole_diameter = 4.0;
placard_holder_color = [0.16, 0.28, 0.42];
placard_insert_color = [0.96, 0.96, 0.93];
// Match the rear carrier's dark raised-label treatment. The printable insert
// remains one fused mesh; this split exists only at presentation boundaries.
placard_label_color = [0.02, 0.02, 0.02];
placard_spacer_thickness = 3.0;
placard_riser_size = [18.0, 58.0, 4.0];
placard_riser_hole_offset = 18.0;
placard_riser_slot = [10.0, m3_clearance];
placard_rail_mount_z = outer_rail_z.y;
placard_center_z = placard_rail_mount_z -
                   2 * placard_riser_hole_offset;
placard_riser_center_z = (placard_rail_mount_z + placard_center_z) / 2;

// ---- Inboard human-side lower-cross-rail power-strip interface -----------
// The strip lies horizontally across the INSIDE face of the lower human-side
// width rail. Its long axis follows X, its measured 48.5 mm short axis stays
// below the fixture board, and its preview-only enclosure depth projects +Y
// into the service bay. This is deliberately not attached to either side post.
//
// Two independently sliding blocks avoid treating the unmeasured long-axis
// keyhole pitch as authoritative. Each block accepts two of the strip's four
// supplied mounting screws at the measured symmetric 27.6 mm transverse pitch.
power_strip_body_size = [204.27, 32.0, 48.5]; // X, provisional Y depth, Z
power_strip_body_depth_is_preview_only = true;
power_strip_cable_keepout = [36.0, 36.0, 14.0];
power_strip_bottom_z = 0.0;
power_strip_inside_rail_face_y = profile_size;
power_strip_center_x = frame_outer.x / 2;
power_strip_left_x = power_strip_center_x - power_strip_body_size.x / 2;
power_strip_right_x = power_strip_center_x + power_strip_body_size.x / 2;
power_strip_keyhole_bore = 3.3;
power_strip_keyhole_head = 5.5;
power_strip_small_hole_diameter = 3.4;
// Owner measured 31 mm from the far outside edges of the two 3.4 mm holes.
power_strip_small_hole_centres = 31.0 - power_strip_small_hole_diameter;
// This is a drill-start guide, not a final thread-size promise. Start with the
// printed 2 mm pilot and enlarge only if the supplied screw's root diameter or
// insertion torque requires it. The 23 mm blind depth leaves 3 mm of ABS
// between the screw and the extrusion.
power_strip_screw_pilot_diameter = 2.0;
power_strip_screw_pilot_depth = 23.0;
power_strip_screw_pilot_entry_diameter = 3.2;
power_strip_screw_pilot_entry_depth = 1.2;
// Local block X becomes installed world Z; local Y becomes world X. Retaining
// the 54 x 40 x 26 mm printed envelope therefore yields a 40 mm wide,
// 54 mm tall block on the human-side lower cross rail.
power_strip_mount_plate_size = [54.0, 40.0, 26.0];
power_strip_mount_face_y =
    power_strip_inside_rail_face_y + power_strip_mount_plate_size.z;
power_strip_body_front_y =
    power_strip_mount_face_y + power_strip_body_size.y;
power_strip_mount_block_center_z = power_strip_mount_plate_size.x / 2;
// The rail slot center is Z=10. The strip's transverse hole pair is centered
// on its measured 48.5 mm body, not on the slightly taller 54 mm ABS block.
power_strip_rail_center_offset =
    profile_size / 2 - power_strip_mount_block_center_z;
power_strip_screw_row_center_offset =
    power_strip_body_size.z / 2 - power_strip_mount_block_center_z;
power_strip_rail_hole_pitch = 24.0;
power_strip_rail_countersink_diameter = 6.4;
power_strip_rail_countersink_depth = 1.8;
power_strip_end_keyhole_inset = 12.0; // assembly-preview only; blocks slide
power_strip_block_x = [power_strip_left_x + power_strip_end_keyhole_inset,
                       power_strip_right_x - power_strip_end_keyhole_inset];
power_strip_pilot_coupon_diameters = [1.6, 1.8, 2.0];
power_strip_coupon_base_thickness = 8.0;
power_strip_pilot_coupon_depth = 6.0;
power_strip_pilot_coupon_size = [18.0, 18.0];
power_strip_coupon_corner_radius = 2.0;
power_strip_coupon_witness_diameter = 3.2;
power_strip_coupon_witness_pitch = 4.0;
// Preview-only representation of one of the strip's supplied screws.
power_strip_supplied_screw_shank_diameter =
    min(3.0, power_strip_keyhole_bore - 0.3);
power_strip_coupon_stud_head_diameter = power_strip_keyhole_head - 0.3;
power_strip_coupon_stud_head_height = 2.4;
power_strip_supplied_screw_head_gap = 1.6;

function placard_fitted_text_size(label_text) =
    min(placard_text_nominal_size,
        (placard_insert_body_length -
         2 * placard_text_horizontal_margin) /
        (max(1, len(label_text)) * placard_text_width_factor));

// Broad, uninterrupted top surfaces for slicer ironing calibration. Six
// disconnected coupons keep a small ABS job thermally well behaved and may be
// split into objects for per-object slicer overrides. Semicircular edge marks
// identify coupons 1..6 without changing the surface being evaluated.
ironing_coupon_size = [45.0, 30.0, 3.2];
ironing_coupon_corner_radius = 3.0;
ironing_coupon_notch_diameter = 3.2;
ironing_coupon_notch_pitch = 4.0;
ironing_coupon_columns = 3;
ironing_coupon_rows = 2;
ironing_coupon_gap = [10.0, 10.0];
ironing_coupon_count = ironing_coupon_columns * ironing_coupon_rows;

registration_tab_size = [24.0, 72.0, 4.0];
registration_above_frame = 12.0;
registration_lower_slot = [9.0, m5_clearance];
registration_lower_hole_y = [12.0, 28.0];
registration_upper_lock_y = 66.0;

// ---- Derived-fit guards --------------------------------------------------
// The axis swap intentionally accepts 29.5 mm on each side of the widest
// 247 mm carrier so every finished outer-frame rail can be reused.
minimum_routing_margin = 29.0;
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
assert(fixture_plane_y - fixture_plate_size.z >= 0,
       "Fixture board must not project beyond the human-side frame plane");
assert(fixture_human_service_depth >= 30.0,
       str("Fixture board must leave at least 30 mm of human-side service bay; ",
           "actual ", fixture_human_service_depth, " mm"));
assert((rear_carrier_rail_y - profile_size / 2) - cradle_plane_y ==
       rear_carrier_link_thickness,
       "Rear carrier links must bridge the derived rail-to-plate depth");
assert(frame_outer.y - cradle_plane_y == rear_carrier_service_gap,
       "Rear carrier must retain the declared wall-side mounting offset");
assert(rear_carrier_link_thickness >= plate_mount_gap,
       "Wall-mounted rear carrier still needs a positive rail bridge");
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
       "Splice collar needs positive external rail clearance");
assert(gantry_splice_fastener_x + m3_clearance / 2 <
       gantry_splice_length / 2,
       "Splice fasteners must remain inside the collar length");
assert(gantry_splice_internal_bar_length == gantry_splice_length,
       "Base internal splice bar and collar must bridge the same seam");
assert(max([for (x = gantry_splice_internal_nut_x) abs(x)]) +
           m3_nut_pocket_across_flats / 2 <
       gantry_splice_internal_bar_length / 2,
       "Internal splice nuts need printable end walls");
assert(gantry_splice_collar_hole_diameter >= m3_clearance,
       "Horizontally printed collar holes must clear M3 hardware");
assert(gantry_splice_collar_entry_depth > 0 &&
       gantry_splice_collar_entry_depth < gantry_splice_wall,
       "Collar entry relief must remain a shallow lead-in");
assert(gantry_splice_collar_pusher_length >
       gantry_splice_collar_pusher_lead,
       "Collar pusher needs a full-width bearing section after its lead-in");
assert(gantry_splice_collar_pusher_tip_inset > 0 &&
       gantry_splice_collar_pusher_tip_inset < slot_key_width,
       "Collar pusher tip inset must leave a positive lead-in width");
assert(gantry_splice_collar_pusher_depth >
       extrusion_slot_lip_depth +
       gantry_splice_external_clearance / 2,
       "Collar pusher must overlap the internal bar behind the rail lip");
assert(gantry_splice_collar_pusher_depth < extrusion_slot_depth,
       "Collar pusher must remain inside the measured rail channel");
assert(abs(gantry_splice_collar_internal_bar_length +
           gantry_splice_collar_pusher_length - gantry_splice_length) <
           epsilon,
       "Collar pusher plus shortened bar must exactly fill one rail half");
assert(max([for (index = [0 :
                          len(gantry_splice_internal_nut_x) - 1])
                abs(gantry_splice_collar_internal_nut_x[index] +
                    gantry_splice_collar_internal_bar_center_offset -
                    gantry_splice_internal_nut_x[index])]) < epsilon,
       "Shortened collar-bar nuts must remain aligned to collar holes");
assert(gantry_joint_plate_size.x > gantry_joint_key_length &&
       gantry_joint_plate_size.y >
       2 * gantry_joint_hole_offset + gantry_joint_slot.y,
       "Gantry joint plate must surround both keyed fastener interfaces");
assert(placard_center_z + placard_size.y / 2 <
       outer_rail_z.y - profile_size / 2,
       "Front placard must remain completely below the top front rail");
assert(placard_size.z == placard_holder_base_thickness +
                          placard_holder_rail_height,
       "Placard holder envelope must equal its base plus rail height");
assert(placard_insert_base_width <
           2 * placard_holder_rail_lower_inner &&
       placard_insert_top_width <
           2 * placard_holder_rail_upper_inner,
       "Placard cartridge needs positive dovetail sliding clearance");
assert(placard_insert_thickness < placard_holder_rail_height,
       "Placard cartridge must fit beneath the retaining rails");
assert(placard_insert_body_length > placard_hole_spacing,
       "Placard cartridge must span both hidden holder fasteners");
assert(placard_fitted_text_size(DEVICE_LABEL) >=
           placard_text_minimum_size,
       "Device label is too long for the fleet placard at minimum text size");
assert(placard_size.x <= 247.0,
       "Fleet placard holder must fit the conservative Prusa X envelope");
assert(max(power_strip_pilot_coupon_diameters) <
           power_strip_small_hole_diameter,
       "Power-strip pilot variants must remain below the supplied screw path");
assert(power_strip_coupon_stud_head_diameter < power_strip_keyhole_head,
       "Power-strip preview screw head must fit the measured keyhole opening");
assert(power_strip_screw_pilot_depth <
           power_strip_mount_plate_size.z,
       "Power-strip screw pilots must stop before the aluminum extrusion");
assert(power_strip_screw_pilot_depth +
           2.0 <= power_strip_mount_plate_size.z,
       "Power-strip screw pilots need at least 2 mm of closed ABS floor");
assert(power_strip_screw_pilot_entry_depth <
           power_strip_screw_pilot_depth,
       "Power-strip pilot entry chamfer must remain inside the pilot");
assert(abs(power_strip_screw_row_center_offset) +
           power_strip_small_hole_centres / 2 +
           power_strip_screw_pilot_entry_diameter / 2 <
           power_strip_mount_plate_size.x / 2,
       "Power-strip supplied-screw pilots need printable side walls");
assert(abs(power_strip_rail_center_offset) +
           power_strip_rail_countersink_diameter / 2 <
           power_strip_mount_plate_size.x / 2,
       "Power-strip rail countersinks need printable side walls");
assert(power_strip_rail_hole_pitch / 2 +
           power_strip_rail_countersink_diameter / 2 <
           power_strip_mount_plate_size.y / 2,
       "Power-strip rail countersinks need printable end walls");
assert(sqrt(pow(power_strip_rail_center_offset -
                    (power_strip_screw_row_center_offset -
                     power_strip_small_hole_centres / 2), 2) +
            pow(power_strip_rail_hole_pitch / 2, 2)) >
           power_strip_rail_countersink_diameter / 2 +
           power_strip_screw_pilot_entry_diameter / 2 + 2.0,
       "Power-strip rail and supplied-screw holes need a 2 mm ABS web");
assert(power_strip_left_x >= profile_size &&
       power_strip_right_x <= frame_outer.x - profile_size,
       "Power strip must fit between the human-side corner posts");
assert(power_strip_bottom_z >= 0 &&
       power_strip_bottom_z + power_strip_body_size.z + 5.0 <=
           fixture_origin.z,
       "Lower-rail power strip needs 5 mm vertical clearance below fixture");
assert(power_strip_inside_rail_face_y >= profile_size &&
       power_strip_body_front_y <= frame_outer.y - profile_size,
       "Power-strip envelope must remain inside the front/rear frame faces");
assert(2 * len(power_strip_pilot_coupon_diameters) >= 6,
       "Small ABS power-strip fit bed needs at least six cooling objects");
assert(ironing_coupon_count >= 6,
       "Small ABS ironing batches need at least six coupons for cooling");
assert((ironing_coupon_count - 1) * ironing_coupon_notch_pitch <
           ironing_coupon_size.y - 2 * ironing_coupon_corner_radius,
       "Ironing coupon edge marks must remain clear of rounded corners");
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

module extrusion(length, axis, tint = [0.72, 0.74, 0.77]) {
    color(tint)
        pf_2020_extrusion(length, axis, profile_size,
                          EXTRUSION_DETAIL, extrusion_slot_opening,
                          extrusion_slot_depth, extrusion_centre_bore,
                          extrusion_slot_pocket_width,
                          extrusion_slot_lip_depth,
                          extrusion_slot_deep_width,
                          extrusion_web_thickness);
}

module outer_frame_bottom(tint = [0.72, 0.74, 0.77]) {
    for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
        translate([profile_size, y, outer_rail_z.x])
            extrusion(structural_x_length, "x", tint);

    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        translate([x, profile_size, outer_rail_z.x])
            extrusion(structural_y_length, "y", tint);
}

module outer_frame_posts(tint = [0.72, 0.74, 0.77]) {
    // The vertical posts are the stems of the delivered three-way joints.
    // Connector caps add 4 mm beyond each aluminum end.
    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
            translate([x, y, frame_aluminum_z_min])
                extrusion(structural_z_length, "z", tint);
}

module outer_frame_top(tint = [0.72, 0.74, 0.77]) {
    for (y = [profile_size / 2, frame_outer.y - profile_size / 2])
        translate([profile_size, y, outer_rail_z.y])
            extrusion(structural_x_length, "x", tint);

    for (x = [profile_size / 2, frame_outer.x - profile_size / 2])
        translate([x, profile_size, outer_rail_z.y])
            extrusion(structural_y_length, "y", tint);
}

module outer_frame(tint = [0.72, 0.74, 0.77]) {
    // Width and depth rails butt into the post side faces. Their top/bottom
    // outer faces align with the connector-cap planes, with zero Z inset.
    outer_frame_bottom(tint);
    outer_frame_posts(tint);
    outer_frame_top(tint);
}

module fixture_gantry(tint = [0.72, 0.74, 0.77]) {
    // Uprights share the X planes of the outer depth rails.  This lets one
    // flat keyed plate bridge each T joint while the complete gantry slides
    // anywhere along the depth-rail slots.
    for (x = gantry_upright_x)
        for (segment = [0 : gantry_upright_segment_count - 1])
            translate([x, fixture_gantry_y,
                       gantry_clear_z_min +
                       segment * gantry_upright_segment_length])
                extrusion(gantry_upright_segment_length, "z", tint);

    // Concealed metal L-connectors let each crossbar slide vertically on the
    // uprights; plate fasteners then slide horizontally in these crossbars.
    for (z = fixture_crossbar_z)
        translate([profile_size, fixture_gantry_y, z])
            extrusion(gantry_crossbar_length, "x", tint);
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

module outer_corner_connector_proxies(top_values = [false, true]) {
    for (x_right = [false, true])
        for (y_rear = [false, true])
            for (top = top_values)
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

module device_preview(detail = PLATE_DETAIL) {
    // The canonical platform model and the carrier use the same local axes:
    // X left/right, Y bottom/top, Z rear/front. Its rear is held 11 mm ahead
    // of the carrier datum, which keeps the detailed screen/front surface on
    // the same analytical optical plane used by the FOV guard.
    if (detail == "mesh") {
        color([0.15, 0.16, 0.17, 0.98])
            device_model_mesh_at_installed_datum(
                device_shell_presentation_mesh);
        color([0.025, 0.03, 0.035, 1.0])
            device_model_mesh_at_installed_datum(
                device_controls_presentation_mesh, 0.03);
        color([0.015, 0.10, 0.15, 1.0])
            device_model_mesh_at_installed_datum(
                device_screen_presentation_mesh, 0.06);
    } else {
        // Lightweight envelope keeps lint and ordinary assembly preview free
        // of generated presentation assets.
        color([0.08, 0.09, 0.10, 0.88])
            translate([optical_datum.x - device_body.x / 2,
                       device_screen_y,
                       optical_datum.y - device_body.y / 2])
                cube([device_body.x, device_body.z, device_body.y]);
    }

}

module webcam_preview() {
    // Webcam body is intentionally an installed keep-out envelope; its lens
    // datum and FOV are the authoritative interfaces for this chassis.
    color([0.10, 0.10, 0.11, 0.9])
        translate([optical_datum.x - camera_installed_keepout.x / 2,
                   fixture_plane_y,
                   optical_datum.y - camera_installed_keepout.z / 2])
            cube(camera_installed_keepout);
    color([0.10, 0.16, 0.22])
        translate([optical_datum.x, camera_lens_y, optical_datum.y])
            rotate([-90, 0, 0]) cylinder(d = 12, h = 5);
}

module device_and_camera_preview(detail = PLATE_DETAIL) {
    device_preview(detail);
    webcam_preview();
}

module device_model_mesh_at_installed_datum(mesh_path,
                                             front_offset = 0) {
    translate(cradle_origin)
        rotate([90, 0, 0])
            translate([
                (cradle_plate_size.x - device_body.x) / 2,
                (cradle_plate_size.y - device_body.y) / 2,
                device_rear_gap + front_offset
            ])
                import(mesh_path, convexity = 10);
}

module camera_frustum_geometry() {
    lens = [optical_datum.x, camera_lens_y, optical_datum.y];
    target_y = device_screen_y - 0.2;
    coverage_half_width = optical_distance * tan(camera_assumed_hfov / 2);
    coverage_half_height = optical_distance * tan(camera_assumed_vfov / 2);
    hull() {
        translate(lens) sphere(d = 2.0, $fn = 16);
        for (x = [-coverage_half_width, coverage_half_width])
            for (z = [-coverage_half_height, coverage_half_height])
                translate([optical_datum.x + x, target_y,
                           optical_datum.y + z])
                    sphere(d = 1.0, $fn = 12);
    }
}

module camera_frustum_preview() {
    %color([0.18, 0.72, 0.92, 0.18])
        camera_frustum_geometry();
}

module placard_text(relief = placard_text_relief,
                    label_text = DEVICE_LABEL,
                    center_x = placard_insert_body_center_x) {
    fitted_size = placard_fitted_text_size(label_text);
    assert(fitted_size >= placard_text_minimum_size,
           str("Placard label does not fit at the ",
               placard_text_minimum_size, " mm fleet minimum: ",
               label_text));
    translate([center_x, 0, placard_insert_thickness])
        linear_extrude(height = relief)
            text(label_text, size = fitted_size,
                 font = "Liberation Sans:style=Bold",
                 halign = "center", valign = "center");
}

// One support-free retaining rail. The inner face grows inward gradually as
// Z rises, producing a coarse-nozzle-friendly dovetail without support.
module placard_holder_rail(side = 1, holder_length = placard_size.x) {
    rail_left = -holder_length / 2 + placard_holder_rail_end_inset;
    rail_right = holder_length / 2 - placard_holder_rail_end_inset;
    rail_length = rail_right - rail_left;
    outer_y = placard_size.y / 2;
    lower_y = side > 0 ? placard_holder_rail_lower_inner : -outer_y;
    upper_y = side > 0 ? placard_holder_rail_upper_inner : -outer_y;
    lower_width = outer_y - placard_holder_rail_lower_inner;
    upper_width = outer_y - placard_holder_rail_upper_inner;

    hull() {
        translate([rail_left, lower_y,
                   placard_holder_base_thickness])
            cube([rail_length, lower_width, 0.4]);
        translate([rail_left, upper_y,
                   placard_size.z - 0.8])
            cube([rail_length, upper_width, 0.8]);
    }
}

module placard_holder(holder_length = placard_size.x,
                      with_mount_holes = true) {
    rail_left = -holder_length / 2 + placard_holder_rail_end_inset;

    difference() {
        union() {
            linear_extrude(height = placard_holder_base_thickness)
                pf_rounded_rect_2d([holder_length, placard_size.y],
                                   placard_corner_radius);

            placard_holder_rail(-1, holder_length);
            placard_holder_rail(1, holder_length);

            // Closed left end; the right side stays open for cartridge swaps.
            translate([rail_left, -placard_holder_rail_lower_inner,
                       placard_holder_base_thickness])
                cube([placard_holder_end_stop,
                      2 * placard_holder_rail_lower_inner,
                      placard_holder_rail_height]);
        }

        if (with_mount_holes)
            for (x = [-placard_hole_spacing / 2,
                       placard_hole_spacing / 2]) {
                translate([x, 0, -epsilon])
                    cylinder(d = m3_clearance,
                             h = placard_holder_base_thickness +
                                 2 * epsilon,
                             $fn = 28);
                translate([x, 0,
                           placard_holder_base_thickness -
                           placard_mount_countersink_depth])
                    cylinder(d1 = m3_clearance,
                             d2 = placard_mount_countersink_diameter,
                             h = placard_mount_countersink_depth + epsilon,
                             $fn = 32);
            }
    }
}

module placard_insert_blank(
    body_length = placard_insert_body_length,
    body_center_x = placard_insert_body_center_x,
    with_pull_tab = true) {
    body_right = body_center_x + body_length / 2;
    tab_center_x = body_right + placard_insert_tab_size.x / 2 -
                   placard_insert_tab_overlap;

    difference() {
        union() {
            hull() {
                translate([body_center_x, 0, 0])
                    linear_extrude(height = 0.4)
                        pf_rounded_rect_2d(
                            [body_length, placard_insert_base_width], 2.0);
                translate([body_center_x, 0,
                           placard_insert_thickness - 0.4])
                    linear_extrude(height = 0.4)
                        pf_rounded_rect_2d(
                            [body_length, placard_insert_top_width], 1.6);
            }

            if (with_pull_tab)
                hull() {
                    translate([tab_center_x, 0, 0])
                        linear_extrude(height = 0.4)
                            pf_rounded_rect_2d(placard_insert_tab_size, 2.0);
                    translate([tab_center_x, 0,
                               placard_insert_thickness - 0.4])
                        linear_extrude(height = 0.4)
                            pf_rounded_rect_2d(
                                [placard_insert_tab_size.x - 1.0,
                                 placard_insert_tab_size.y - 1.0], 1.6);
                }
        }

        if (with_pull_tab)
            translate([tab_center_x + 1.0, 0, -epsilon])
                cylinder(d = placard_insert_pull_hole_diameter,
                         h = placard_insert_thickness + 2 * epsilon,
                         $fn = 24);
    }
}

module placard_insert(label_text = DEVICE_LABEL,
                      body_length = placard_insert_body_length,
                      body_center_x = placard_insert_body_center_x,
                      with_pull_tab = true,
                      with_text = true) {
    union() {
        placard_insert_blank(body_length, body_center_x, with_pull_tab);
        if (with_text)
            placard_text(placard_text_relief, label_text, body_center_x);
    }
}

// Backward-compatible name for the device-specific printable piece.
module device_id_placard() {
    placard_insert();
}

// Short coupon for validating the dovetail clearance before printing the
// permanent fleet-standard holder. Both pieces are broad-face-down and
// support-free.
module placard_slide_fit_coupon() {
    coupon_holder_length = 45.0;
    coupon_rail_left = -coupon_holder_length / 2 +
                       placard_holder_rail_end_inset;
    coupon_body_left = coupon_rail_left + placard_holder_end_stop + 0.4;
    coupon_body_right = coupon_holder_length / 2 -
                        placard_holder_rail_end_inset;
    coupon_body_length = coupon_body_right - coupon_body_left;
    coupon_body_center = (coupon_body_left + coupon_body_right) / 2;

    placard_holder(coupon_holder_length, false);
    translate([0, 55.0, 0])
        placard_insert("FIT", coupon_body_length,
                       coupon_body_center, true, true);
}

module placard_system_detail_preview() {
    color(placard_holder_color) placard_holder();
    // Shown partially withdrawn to make the permanent/changeable split clear.
    translate([28.0, 0, placard_holder_base_thickness])
        placard_insert_material_preview();
}

// Coarse half-round edge marks identify otherwise similar fit coupons after
// they leave the print bed. They are deliberately much larger than a 0.8 mm
// extrusion line and never disturb the feature under test.
module power_strip_coupon_witnesses(size, height, count) {
    for (index = [0 : count - 1])
        translate([size.x / 2,
                   (index - (count - 1) / 2) *
                       power_strip_coupon_witness_pitch,
                   -epsilon])
            cylinder(d = power_strip_coupon_witness_diameter,
                     h = height + 2 * epsilon,
                     $fn = 24);
}

// Optional direct-drive test block. Its blind hole uses the same print
// direction as the production screw pilots. Two copies of each diameter keep
// the small ABS batch thermally stable; production remains a drill-start
// guide and does not require this coupon.
module power_strip_pilot_fit_coupon(pilot_diameter,
                                    witness_notches = 1) {
    difference() {
        linear_extrude(height = power_strip_coupon_base_thickness)
            pf_rounded_rect_2d(power_strip_pilot_coupon_size,
                               power_strip_coupon_corner_radius);

        translate([0, 0,
                   power_strip_coupon_base_thickness -
                       power_strip_pilot_coupon_depth])
            cylinder(d = pilot_diameter,
                     h = power_strip_pilot_coupon_depth + epsilon,
                     $fn = 24);
        power_strip_coupon_witnesses(power_strip_pilot_coupon_size,
                                     power_strip_coupon_base_thickness,
                                     witness_notches);
    }
}

// Six disconnected support-free objects: two rows each repeat the
// 1.6/1.8/2.0 mm screw-pilot choices. Printing this set is optional if the
// production 2 mm holes will be used only as drill centers.
module power_strip_fit_coupon_set() {
    coupon_pitch = power_strip_pilot_coupon_size.x + 8.0;
    for (row = [0, 1])
        for (index = [0 : len(power_strip_pilot_coupon_diameters) - 1])
            translate([
                power_strip_pilot_coupon_size.x / 2 +
                    index * coupon_pitch,
                power_strip_pilot_coupon_size.y / 2 +
                    row * coupon_pitch,
                0
            ])
                power_strip_pilot_fit_coupon(
                    power_strip_pilot_coupon_diameters[index], index + 1);
}

// One substantial end block: two countersunk M3 holes clamp it to preloaded
// rail nut bars. The second measured pair receives two of the strip's supplied
// wall-mount screws. Those are 2 mm blind drill-start pilots—not printed
// threads—and stop 3 mm before the aluminum. Both blocks are identical and
// print broad-face down without support.
module power_strip_mount_block() {
    difference() {
        linear_extrude(height = power_strip_mount_plate_size.z)
            pf_rounded_rect_2d([power_strip_mount_plate_size.x,
                                power_strip_mount_plate_size.y], 3.0);

        for (y = [-power_strip_rail_hole_pitch / 2,
                   power_strip_rail_hole_pitch / 2]) {
            translate([power_strip_rail_center_offset, y, -epsilon])
                cylinder(d = m3_clearance,
                         h = power_strip_mount_plate_size.z + 2 * epsilon,
                         $fn = 28);
            translate([power_strip_rail_center_offset, y,
                       power_strip_mount_plate_size.z -
                           power_strip_rail_countersink_depth])
                cylinder(d1 = m3_clearance,
                         d2 = power_strip_rail_countersink_diameter,
                         h = power_strip_rail_countersink_depth + epsilon,
                         $fn = 32);
        }

        for (x = [power_strip_screw_row_center_offset -
                       power_strip_small_hole_centres / 2,
                   power_strip_screw_row_center_offset +
                       power_strip_small_hole_centres / 2]) {
            translate([x, 0,
                       power_strip_mount_plate_size.z -
                           power_strip_screw_pilot_depth])
                cylinder(d = power_strip_screw_pilot_diameter,
                         h = power_strip_screw_pilot_depth + epsilon,
                         $fn = 24);
            translate([x, 0,
                       power_strip_mount_plate_size.z -
                           power_strip_screw_pilot_entry_depth])
                cylinder(d1 = power_strip_screw_pilot_diameter,
                         d2 = power_strip_screw_pilot_entry_diameter,
                         h = power_strip_screw_pilot_entry_depth + epsilon,
                         $fn = 28);
        }
    }
}

module power_strip_mount_block_pair() {
    translate([power_strip_mount_plate_size.x / 2,
               power_strip_mount_plate_size.y / 2, 0])
        power_strip_mount_block();
    translate([1.5 * power_strip_mount_plate_size.x + 8.0,
               power_strip_mount_plate_size.y / 2, 0])
        power_strip_mount_block();
}

module installed_power_strip_bracket(bracket_x) {
    // Local X -> world Z, local Y -> world X, local Z -> world Y. The block's
    // two rail holes therefore follow the lower cross-rail slot in X, while
    // the supplied-screw pilots reproduce the strip's transverse Z spacing.
    multmatrix([
        [0, 1, 0, bracket_x],
        [0, 0, 1, power_strip_inside_rail_face_y],
        [1, 0, 0, power_strip_mount_block_center_z],
        [0, 0, 0, 1]
    ]) {
            color([0.95, 0.53, 0.12]) power_strip_mount_block();

            // Presentation-only supplied screw heads. The printable block
            // contains only blind drill-start pilots.
            color([0.58, 0.60, 0.63])
                for (x = [power_strip_screw_row_center_offset -
                               power_strip_small_hole_centres / 2,
                           power_strip_screw_row_center_offset +
                               power_strip_small_hole_centres / 2])
                    translate([x, 0,
                               power_strip_mount_plate_size.z]) {
                    cylinder(d = power_strip_supplied_screw_shank_diameter,
                             h = power_strip_supplied_screw_head_gap,
                             $fn = 28);
                    translate([0, 0, power_strip_supplied_screw_head_gap])
                        cylinder(d = power_strip_coupon_stud_head_diameter,
                                 h = power_strip_coupon_stud_head_height,
                                 $fn = 32);
                }
        }
}

module power_strip_mounts_preview() {
    for (bracket_x = power_strip_block_x)
        installed_power_strip_bracket(bracket_x);
}

module power_strip_body_preview() {
    // The measured X/Z envelope is authoritative. Y depth remains a clearly
    // documented preview proxy until a side-profile measurement is needed.
    // Its back hangs on the two lower-rail blocks at
    // power_strip_mount_face_y; the complete proxy projects inward (+Y).
    color([0.91, 0.91, 0.88, 0.96])
        translate([power_strip_left_x,
                   power_strip_mount_face_y,
                   power_strip_bottom_z])
            cube(power_strip_body_size);

    // Fixed cable exits the left short end. This keep-out remains completely
    // inside the frame and clear of the fixture board.
    %color([0.92, 0.20, 0.16, 0.28])
        translate([power_strip_left_x - power_strip_cable_keepout.x,
                   power_strip_mount_face_y,
                   power_strip_bottom_z +
                       (power_strip_body_size.z -
                        power_strip_cable_keepout.z) / 2])
            cube(power_strip_cable_keepout);
}

module power_strip_system_preview() {
    power_strip_mounts_preview();
    power_strip_body_preview();
}

module ironing_test_coupon(witness_notches = 1) {
    difference() {
        linear_extrude(height = ironing_coupon_size.z)
            pf_rounded_rect_2d([ironing_coupon_size.x,
                                ironing_coupon_size.y],
                               ironing_coupon_corner_radius);

        // Put all identifiers on one short edge. The cylinder centers sit on
        // that edge, leaving clean half-round scallops and a broad top face.
        for (index = [0 : witness_notches - 1])
            translate([ironing_coupon_size.x / 2,
                       (index - (witness_notches - 1) / 2) *
                           ironing_coupon_notch_pitch,
                       -epsilon])
                cylinder(d = ironing_coupon_notch_diameter,
                         h = ironing_coupon_size.z + 2 * epsilon,
                         $fn = 24);
    }
}

module ironing_test_coupon_set() {
    for (index = [0 : ironing_coupon_count - 1]) {
        column = index % ironing_coupon_columns;
        row = floor(index / ironing_coupon_columns);
        translate([ironing_coupon_size.x / 2 +
                       column * (ironing_coupon_size.x +
                                 ironing_coupon_gap.x),
                   ironing_coupon_size.y / 2 +
                       row * (ironing_coupon_size.y +
                              ironing_coupon_gap.y),
                   0])
            ironing_test_coupon(index + 1);
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

// A long version of the physically accepted 11.75 / 6.46 mm M3 nut bar.
// It slides halfway into the first open rail, the second rail slides over its
// exposed half, and its two metal nuts land on opposite sides of the seam.
// Print the broad bearing face down exactly like the accepted 30 mm bars.
module gantry_splice_internal_bar(
    bar_length = gantry_splice_internal_bar_length,
    nut_positions = gantry_splice_internal_nut_x,
    witness_notches = 0
) {
    m3_slide_nut_carrier(
        m3_slide_nut_bearing_width,
        m3_slide_nut_deep_width,
        witness_notches,
        bar_length,
        nut_positions);
}

// The full-wrap collar's self-indexing foot consumes 3.2 mm at the trailing
// end. This asymmetric double-nut bar stops against that foot, ends exactly at
// the open rail seam, then tracks the collar holes as both slide into place.
module gantry_splice_full_collar_internal_bar() {
    gantry_splice_internal_bar(
        gantry_splice_collar_internal_bar_length,
        gantry_splice_collar_internal_nut_x,
        1);
}

module gantry_splice_full_collar_internal_bar_pair() {
    for (row = [0, 1])
        translate([0, row * 18.0, 0])
            gantry_splice_full_collar_internal_bar();
}

// The accepted one-piece, 360-degree splice collar is end-loaded before the
// second rail half is joined. Two opposed internal double-nut bars provide the
// metal-threaded clamp points. It uses the physically validated 0.20 mm total
// face clearance. Small corner
// dogbones prevent rounded printed inside corners from stealing that clearance;
// shallow enlarged entries tolerate first-layer elephant foot. Two opposed
// pusher keys at the trailing end enter the same channels as the internal bars:
// they first stop each bar fully inside rail A, then move the bars with the
// collar to a centered 40/40 mm seam bridge.
module gantry_splice_full_collar(
    clearance = gantry_splice_external_clearance,
    collar_length = gantry_splice_length
) {
    inner_width = profile_size + clearance;
    outer_width = inner_width + 2 * gantry_splice_wall;
    entry_width = inner_width + gantry_splice_collar_entry_relief;
    pusher_tip_width = slot_key_width -
                       gantry_splice_collar_pusher_tip_inset;

    assert(clearance > 0,
           "Full splice collar needs positive rail clearance");
    assert(collar_length > 2 * gantry_splice_wall,
           "Full splice collar is too short for its wall thickness");

    union() {
        difference() {
            translate([-collar_length / 2, -outer_width / 2,
                       -outer_width / 2])
                cube([collar_length, outer_width, outer_width]);

            translate([-collar_length / 2 - epsilon,
                       -inner_width / 2, -inner_width / 2])
                cube([collar_length + 2 * epsilon,
                      inner_width, inner_width]);

            // Dogbone the four internal corners along the rail axis.
            for (side_y = [-1, 1])
                for (side_z = [-1, 1])
                    translate([-collar_length / 2 - epsilon,
                               side_y * inner_width / 2,
                               side_z * inner_width / 2])
                        rotate([0, 90, 0])
                            cylinder(d = gantry_splice_collar_corner_relief,
                                     h = collar_length + 2 * epsilon,
                                     $fn = 20);

            // Relief at both open ends eases insertion without loosening the
            // 77.6 mm central bearing length.
            translate([-collar_length / 2 - epsilon,
                       -entry_width / 2, -entry_width / 2])
                cube([gantry_splice_collar_entry_depth + epsilon,
                      entry_width, entry_width]);
            translate([collar_length / 2 -
                           gantry_splice_collar_entry_depth,
                       -entry_width / 2, -entry_width / 2])
                cube([gantry_splice_collar_entry_depth + epsilon,
                      entry_width, entry_width]);

            // Two aligned bores create four outer-wall openings. Each side
            // uses its own short M3 screw into the adjacent internal-bar nut;
            // no screw passes through the aluminum extrusion.
            for (x = gantry_splice_internal_nut_x)
                translate([x, 0, -outer_width / 2 - epsilon])
                    cylinder(d = gantry_splice_collar_hole_diameter,
                             h = outer_width + 2 * epsilon,
                             $fn = 12);
        }

        // Self-indexing pusher keys. The collar prints with this trailing end
        // on the bed. Each key starts narrow, grows support-free to the
        // accepted 6.43 mm slot width, and reaches just beyond the rail lip to
        // contact (but not climb over) its internal bar. Extending outward to
        // entry_width keeps the keys joined through the insertion relief.
        for (side_z = [-1, 1])
            hull() {
                translate([
                    -collar_length / 2,
                    -pusher_tip_width / 2,
                    side_z > 0 ?
                        inner_width / 2 -
                            gantry_splice_collar_pusher_depth :
                        -entry_width / 2 - epsilon
                ])
                    cube([
                        2 * epsilon,
                        pusher_tip_width,
                        gantry_splice_collar_pusher_depth +
                            gantry_splice_collar_entry_relief / 2 + epsilon
                    ]);

                translate([
                    -collar_length / 2 +
                        gantry_splice_collar_pusher_lead,
                    -slot_key_width / 2,
                    side_z > 0 ?
                        inner_width / 2 -
                            gantry_splice_collar_pusher_depth :
                        -entry_width / 2 - epsilon
                ])
                    cube([
                        gantry_splice_collar_pusher_length -
                            gantry_splice_collar_pusher_lead,
                        slot_key_width,
                        gantry_splice_collar_pusher_depth +
                            gantry_splice_collar_entry_relief / 2 + epsilon
                    ]);
            }
    }
}

// Stand the accepted collar on its indexed open end. This is its support-free
// production orientation. The lab's validated ABS process needs no brim.
// The collar is restricted to the light fixture gantry; it is never an
// outer-frame or stacking load-path part.
module gantry_splice_full_collar_print() {
    outer_width = gantry_splice_inner_width + 2 * gantry_splice_wall;
    translate([0, 0, gantry_splice_length / 2])
        rotate([0, -90, 0])
            gantry_splice_full_collar();
}

// Cutaway-style visual proof of the selected assembled load path. The two
// 60 mm rail fragments are translucent and meet at X=0; both corrected
// 76.8 mm bars visibly bridge that seam inside opposite channels while the
// accepted full-wrap collar bridges it outside. This is presentation-only.
module gantry_splice_installed_preview() {
    demo_rail_half = 60.0;
    rail_center_z = gantry_splice_wall + profile_size / 2;
    internal_bar_z = gantry_splice_wall + extrusion_slot_lip_depth;
    collar_outer_width = gantry_splice_inner_width +
                         2 * gantry_splice_wall;
    cutaway_y_min = -collar_outer_width / 2 - epsilon;
    cutaway_y_size = collar_outer_width / 2 + 2 * epsilon;

    // Remove the camera-facing half of both the collar and aluminum. This is
    // a literal section view, not alpha-only x-ray trickery, so the opposed
    // orange bars remain unmistakable in static handbook renders.
    color([0.12, 0.38, 0.70, 0.82])
        difference() {
            translate([0, 0, rail_center_z])
                gantry_splice_full_collar();
            translate([-gantry_splice_length / 2 - epsilon,
                       cutaway_y_min, -epsilon])
                cube([gantry_splice_length + 2 * epsilon,
                      cutaway_y_size,
                      2 * rail_center_z + 2 * epsilon]);
        }

    color([0.68, 0.71, 0.75, 0.52]) {
        difference() {
            translate([-demo_rail_half, 0, rail_center_z])
                extrusion(demo_rail_half, "x");
            translate([-demo_rail_half - epsilon,
                       -profile_size / 2 - epsilon,
                       rail_center_z - profile_size / 2 - epsilon])
                cube([demo_rail_half + 2 * epsilon,
                      profile_size / 2 + 2 * epsilon,
                      profile_size + 2 * epsilon]);
        }
        difference() {
            translate([0, 0, rail_center_z])
                extrusion(demo_rail_half, "x");
            translate([-epsilon,
                       -profile_size / 2 - epsilon,
                       rail_center_z - profile_size / 2 - epsilon])
                cube([demo_rail_half + 2 * epsilon,
                      profile_size / 2 + 2 * epsilon,
                      profile_size + 2 * epsilon]);
        }
    }

    // Draw the internal bars last as an X-ray overlay so their hidden seam
    // bridge remains legible in the generated OpenCSG preview.
    color([0.96, 0.40, 0.04]) {
        translate([gantry_splice_collar_internal_bar_center_offset,
                   0, internal_bar_z])
            gantry_splice_full_collar_internal_bar();
        translate([0, 0, 2 * rail_center_z])
            mirror([0, 0, 1])
                translate([
                    gantry_splice_collar_internal_bar_center_offset,
                    0, internal_bar_z])
                    gantry_splice_full_collar_internal_bar();
    }

}

module installed_gantry_splice_collar(x, y) {
    // Local X follows the upright's world Z axis; local Y/Z become its X/Y
    // cross-section. One accepted full-wrap collar replaces the obsolete pair
    // of external U-shells at each upright seam.
    multmatrix([
        [0, 1, 0, x],
        [0, 0, 1, y],
        [1, 0, 0, gantry_upright_splice_z],
        [0, 0, 0, 1]
    ]) gantry_splice_full_collar();
}

module gantry_splice_previews() {
    color([0.94, 0.47, 0.10])
        for (x = gantry_upright_x)
            installed_gantry_splice_collar(x, fixture_gantry_y);
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

module placard_risers_preview() {
    // Flat hanging straps bolt to the front slot at Z=354 and put the reusable
    // holder at Z=318. The holder remains beneath the top front rail and never
    // moves with the fixture gantry; only its labeled cartridge slides out.
    color([0.94, 0.47, 0.10])
        for (x = [frame_outer.x / 2 - placard_hole_spacing / 2,
                  frame_outer.x / 2 + placard_hole_spacing / 2])
            translate([x,
                       -placard_spacer_thickness,
                       placard_riser_center_z])
                rotate([90, 0, 0])
                    rotate([0, 0, 180]) placard_riser();
}

module placard_holder_preview() {
    color(placard_holder_color)
        translate([frame_outer.x / 2,
                   -(placard_spacer_thickness + placard_riser_size.z),
                   placard_center_z])
            rotate([90, 0, 0]) placard_holder();
}

// Presentation-only material split at the real slicer filament-change plane.
// Production continues to call placard_insert(), which fuses these solids.
module placard_insert_material_preview() {
    color(placard_insert_color) placard_insert_blank();
    color(placard_label_color) placard_text();
}

module placard_insert_at_installed_datum(x_offset = 0) {
    translate([frame_outer.x / 2 + x_offset,
               -(placard_spacer_thickness + placard_riser_size.z +
                 placard_holder_base_thickness),
               placard_center_z])
        rotate([90, 0, 0])
            children();
}

module placard_insert_preview() {
    placard_insert_at_installed_datum()
        placard_insert_material_preview();
}

module placard_assembly_preview() {
    placard_risers_preview();
    placard_holder_preview();
    placard_insert_preview();
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

// Canonical production beds. Every object is already in its documented
// support-free orientation and every bed fits the conservative 247 x 207 mm
// Prusa envelope. Individual exports remain available for replacement parts.
//
// Batch 00 is optional after any printer, nozzle, material, slicer, or rail
// supplier change. It is not part of a repeat build on the accepted process.
module production_batch_00_calibration() {
    translate([36.0, 18.0, 0]) rail_fit_coupon();
    translate([34.0, 50.0, 0]) m3_slide_nut_fit_coupon();
    translate([132.0, 46.0, 0]) placard_slide_fit_coupon();
}

// All rail-channel interfaces share one ironing-enabled bed. Twenty-eight
// 30 mm M3 nut bars cover 22 active locations plus six deliberately parked
// service spares. Four 76.8 mm double-nut bars reinforce the two gantry
// upright splices. Print every broad bearing face on the bed.
module production_batch_01_ironed_interfaces() {
    for (index = [0 : m3_slide_nut_set_count - 1])
        translate([17.0 + (index % 7) * 34.0,
                   8.0 + floor(index / 7) * 15.0, 0])
            m3_slide_nut_carrier();

    for (index = [0 : gantry_splice_internal_bar_count - 1])
        translate([40.0 + (index % 2) * 84.0,
                   74.0 + floor(index / 2) * 18.0, 0])
            gantry_splice_full_collar_internal_bar();
}

// Two accepted full-wrap collars. They stand on their indexed open end and
// need neither support nor a brim on the physically validated ABS process.
module production_batch_02_splice_collars() {
    for (index = [0, 1])
        translate([20.0 + index * 50.0, 20.0, 0])
            gantry_splice_full_collar_print();
}

// Hardware that makes the gantry and both tooling plates adjustable: four
// keyed gantry joint plates, four fixture spacers, and the four fixed-carrier
// links (two upper, two lower).
module production_batch_03_movable_mounts() {
    translate([22.0, 25.0, 0]) gantry_joint_plate_set();
    translate([105.0, 15.0, 0]) plate_spacer_set();
    translate([150.0, 66.0, 0]) rear_carrier_link_set();
}

// Frame completion hardware: eight stacking registration tabs, the placard's
// two risers and keyed spacers, and the two power-strip blocks.
module production_batch_04_frame_hardware() {
    translate([6.0, 6.0, 0]) registration_tab_set();
    translate([145.0, 38.0, 0]) placard_riser_pair();
    translate([145.0, 85.0, 0]) placard_spacer_pair();
    translate([130.0, 112.0, 0]) power_strip_mount_block_pair();
}

// The reusable fleet-width holder is an ordinary one-color print. Keeping it
// off the nameplate bed lets that device-specific part own its filament swap.
module production_batch_05_placard_holder() {
    translate([115.0, 22.0, 0]) placard_holder();
}

// The device-specific slide-in cartridge is the only object on this bed.
// Print the fused production mesh in white, then change to black at
// placard_insert_thickness for the raised device name.
module production_batch_06_device_nameplate() {
    translate([109.0, 22.0, 0]) device_id_placard();
}

module production_batch_06_device_nameplate_body() {
    translate([109.0, 22.0, 0]) placard_insert_blank();
}

module production_batch_06_device_nameplate_labels() {
    translate([109.0, 22.0, 0]) placard_text();
}

module production_batch_06_device_nameplate_preview() {
    color(placard_insert_color)
        production_batch_06_device_nameplate_body();
    color(placard_label_color)
        production_batch_06_device_nameplate_labels();
}

// ---- Handbook scenes and semantic web-model layers ----------------------
// Static guide views use a restrained IKEA-like state language: completed
// aluminum is gray, the parts added in the current step are orange, and metal
// connectors remain dark. Fine callouts stay in SVG/HTML rather than becoming
// fragile OpenSCAD text.
guide_complete_tint = [0.66, 0.69, 0.72];
guide_new_tint = [0.96, 0.43, 0.08];
guide_spare_tint = [0.12, 0.52, 0.78];
guide_metal_tint = [0.38, 0.40, 0.43];

// A loaded production short bar shown in its rail-installation orientation.
// The printed bar's broad bearing face is up, toward the slot mouth; the open
// metal-nut pocket faces down, toward the extrusion centre.
module guide_loaded_short_bar() {
    color(guide_new_tint)
        m3_slide_nut_carrier();
    color(guide_metal_tint)
        translate([0, 0,
                   m3_slide_nut_height - m3_nut_measured_thickness])
            cylinder(
                d = m3_nut_measured_across_flats / cos(30),
                h = m3_nut_measured_thickness,
                $fn = 6
            );
}

module guide_arrow_x(start_x, length, z) {
    shaft_length = length - 8.0;
    color(guide_spare_tint) {
        translate([start_x, 0, z])
            rotate([0, 90, 0])
                cylinder(d = 3.0, h = shaft_length, $fn = 24);
        translate([start_x + shaft_length, 0, z])
            rotate([0, 90, 0])
                cylinder(d1 = 8.0, d2 = 0.0, h = 8.0, $fn = 24);
    }
}

// Reusable direction arrow for assembly illustrations.  The local arrow
// points +X from its origin; rotations map it onto the six chassis directions.
module guide_axis_arrow(origin = [0, 0, 0], axis = "x",
                        direction = 1, length = 40.0) {
    shaft_length = length - 8.0;
    rotation =
        axis == "x" ? (direction > 0 ? [0, 0, 0] : [0, 0, 180]) :
        axis == "y" ? (direction > 0 ? [0, 0, 90] : [0, 0, -90]) :
                      (direction > 0 ? [0, -90, 0] : [0, 90, 0]);

    color(guide_spare_tint)
        translate(origin)
            rotate(rotation) {
                rotate([0, 90, 0])
                    cylinder(d = 3.0, h = shaft_length, $fn = 24);
                translate([shaft_length, 0, 0])
                    rotate([0, 90, 0])
                        cylinder(d1 = 8.0, d2 = 0.0,
                                 h = 8.0, $fn = 24);
            }
}

module guide_label(label_text, position, size = 8.0,
                   rotation = [0, 0, 0],
                   tint = [0.12, 0.16, 0.20]) {
    color(tint)
        translate(position)
            rotate(rotation)
                linear_extrude(height = 0.5)
                    text(label_text, size = size,
                         font = "Liberation Sans:style=Bold",
                         halign = "center", valign = "center");
}

module guide_segment(start, finish, diameter = 2.5,
                     tint = guide_spare_tint) {
    color(tint)
        hull() {
            translate(start) sphere(d = diameter, $fn = 20);
            translate(finish) sphere(d = diameter, $fn = 20);
        }
}

// Handbook close-up: the exact short bar and captured M3 nut are aligned with
// an open rail end. The exploded gap is intentional so both profiles remain
// legible. Nothing in this scene is a production part.
module guide_preload_channel_bar() {
    rail_start_x = 22.0;
    rail_length = 72.0;
    rail_center_z = profile_size / 2;
    bar_center_x = 0.0;
    bar_bearing_z = profile_size - 0.4;

    translate([rail_start_x, 0, rail_center_z])
        extrusion(rail_length, "x", [0.82, 0.84, 0.87]);
    // A slightly darker cut face separates the real cross-section from the
    // long satin-anodized surfaces without changing any rail geometry.
    translate([rail_start_x - 0.08, 0, rail_center_z])
        extrusion(0.28, "x", [0.66, 0.69, 0.73]);

    translate([bar_center_x, 0, bar_bearing_z])
        rotate([180, 0, 0])
            guide_loaded_short_bar();

    // Direction arrow sits above the slot so it cannot be confused with a
    // printable or retained component.
    guide_arrow_x(-28.0, 48.0, profile_size + 12.0);
}

// Symbolic bar markers for the whole-frame preload map. Their orientation
// follows the host rail. They sit just outside the slot mouth so the hidden
// captive-bar inventory remains visible in a static handbook render.
module guide_preload_marker(position, axis = "x",
                            tint = guide_new_tint) {
    marker_length = 24.0;
    marker_width = 5.0;
    marker_height = 8.0;
    color(tint)
        translate(position)
            if (axis == "x")
                cube([marker_length, marker_width, marker_height],
                     center = true);
            else if (axis == "y")
                cube([marker_width, marker_length, marker_height],
                     center = true);
            else
                cube([marker_width, marker_height, marker_length],
                     center = true);
}

module guide_preload_markers() {
    operator_y = profile_size / 2;
    device_y = frame_outer.y - profile_size / 2;
    left_x = profile_size / 2;
    right_x = frame_outer.x - profile_size / 2;
    lower_z = outer_rail_z.x;
    upper_z = outer_rail_z.y;
    face_offset = profile_size / 2 + 3.0;
    spare_depth_y = frame_outer.y - 46.0;

    // WIDTH-O-L: four power-strip fasteners on its inboard (+Y) face.
    for (x = [82.0, 126.0, frame_outer.x - 126.0,
              frame_outer.x - 82.0])
        guide_preload_marker(
            [x, operator_y + face_offset, lower_z], "x");

    // WIDTH-O-U: two placard fasteners on its outboard (-Y) face.
    for (x = [frame_outer.x / 2 - placard_hole_spacing / 2,
              frame_outer.x / 2 + placard_hole_spacing / 2])
        guide_preload_marker(
            [x, operator_y - face_offset, upper_z], "x");

    // Device-side lower/upper width rails: two carrier-link fasteners each,
    // on their inboard/operator-facing (-Y) faces.
    for (x = cradle_mount_x) {
        guide_preload_marker(
            [x, device_y - face_offset, lower_z], "x");
        guide_preload_marker(
            [x, device_y - face_offset, upper_z], "x");
    }

    // Four depth rails: one active gantry-joint bar near the fixture gantry
    // plus one blue service spare parked near the device-side end.
    for (x = [left_x, right_x])
        for (z = [lower_z, upper_z]) {
            interior_x = x == left_x ? x + face_offset :
                                      x - face_offset;
            guide_preload_marker(
                [interior_x, fixture_gantry_y, z], "y");
            guide_preload_marker(
                [interior_x, spare_depth_y, z], "y",
                guide_spare_tint);
        }

    // Two active bars on the interior face of each gantry upright.
    for (x = gantry_upright_x)
        for (z = fixture_crossbar_z)
            guide_preload_marker(
                [x == left_x ? x + face_offset : x - face_offset,
                 fixture_gantry_y, z], "z");

    // Two active fixture-plate bars per crossbar plus one blue service spare
    // on the operator-facing side of each crossbar.
    for (z = fixture_crossbar_z)
        for (x = fixture_mount_x)
            guide_preload_marker(
                [x, fixture_gantry_y - face_offset, z], "x");
    guide_preload_marker(
        [45.0, fixture_gantry_y - face_offset,
         fixture_crossbar_z.y], "x", guide_spare_tint);
    guide_preload_marker(
        [frame_outer.x - 45.0, fixture_gantry_y - face_offset,
         fixture_crossbar_z.x], "x", guide_spare_tint);
}

// Handbook overview: ghosted rails reveal the conceptual short-bar inventory.
// Orange markers are used by an installed mount; blue markers are parked
// replacements. Marker positions are intentionally visible outside each slot
// mouth rather than falsely claiming that captive parts sit outside the rail.
module guide_preload_map() {
    outer_frame([0.70, 0.72, 0.75, 0.42]);
    fixture_gantry([0.70, 0.72, 0.75, 0.42]);
    guide_preload_markers();
}

module guide_uprights(tint = guide_new_tint) {
    for (x = gantry_upright_x)
        for (segment = [0 : gantry_upright_segment_count - 1])
            translate([x, fixture_gantry_y,
                       gantry_clear_z_min +
                       segment * gantry_upright_segment_length])
                extrusion(gantry_upright_segment_length, "z", tint);
}

module guide_step_01_splice_uprights() {
    guide_uprights();
    gantry_splice_previews();
}

module guide_step_02_build_gantry() {
    fixture_gantry(guide_new_tint);
    gantry_crossbar_connector_proxies();
    gantry_joint_plate_previews();
    gantry_splice_previews();
}

module guide_step_03_open_frame() {
    outer_frame_bottom(guide_complete_tint);
    outer_frame_posts(guide_new_tint);
    outer_corner_connector_proxies([false]);
}

module guide_step_04_install_gantry() {
    outer_frame_bottom(guide_complete_tint);
    outer_frame_posts(guide_complete_tint);
    outer_corner_connector_proxies([false]);
    fixture_gantry(guide_new_tint);
    gantry_crossbar_connector_proxies();
    gantry_joint_plate_previews();
    gantry_splice_previews();
}

module guide_step_05_close_frame() {
    outer_frame_bottom(guide_complete_tint);
    outer_frame_posts(guide_complete_tint);
    outer_frame_top(guide_new_tint);
    outer_corner_connector_proxies();
    fixture_gantry(guide_complete_tint);
    gantry_crossbar_connector_proxies();
    gantry_joint_plate_previews();
    gantry_splice_previews();
}

module guide_step_06_mount_carrier() {
    guide_layer_aluminum();
    guide_layer_connectors();
    gantry_joint_plate_previews();
    gantry_splice_previews();

    color(guide_new_tint)
        cradle_mesh_at_installed_datum(cradle_body_presentation_mesh);
    color(guide_new_tint)
        cradle_mesh_at_installed_datum(cradle_hooks_presentation_mesh);
    for (x = cradle_mount_x)
        for (index = [0, 1])
            installed_rear_carrier_link(x, cradle_mount_z[index],
                                        outer_rail_z[index]);
}

module guide_step_07_mount_fixture() {
    guide_layer_aluminum();
    guide_layer_connectors();
    gantry_joint_plate_previews();
    gantry_splice_previews();

    color(guide_complete_tint)
        cradle_mesh_at_installed_datum(cradle_body_presentation_mesh);
    color([0.28, 0.29, 0.31])
        cradle_mesh_at_installed_datum(cradle_hooks_presentation_mesh);
    for (x = cradle_mount_x)
        for (index = [0, 1])
            installed_rear_carrier_link(x, cradle_mount_z[index],
                                        outer_rail_z[index]);

    color(guide_new_tint)
        fixture_mesh_at_installed_datum(fixture_presentation_mesh);
    color([0.16, 0.28, 0.38])
        fixture_mesh_at_installed_datum(
            fixture_components_presentation_mesh);
    for (x = fixture_mount_x)
        for (z = fixture_crossbar_z)
            installed_fixture_plate_spacer([x, z]);
    webcam_preview();
}

module guide_step_08_complete() {
    assembly("mesh");
}

// ---- Focused LEGO-style handbook panels --------------------------------
// The section-level renders above show the desired end state.  These smaller
// scenes expose the hidden interface, motion, or measurement that a completed
// overview cannot communicate.

// One lower-left gantry corner.  The translucent extrusion exposes the
// concealed metal L connector that joins a crossbar to an upright.
module guide_detail_02_crossbar_corner() {
    crossbar_z = fixture_crossbar_z.x;
    translate([0, 0, -crossbar_z]) {
        translate([gantry_upright_x.x, fixture_gantry_y,
                   gantry_clear_z_min])
            extrusion(120.0, "z", [0.66, 0.69, 0.72, 0.42]);
        translate([profile_size, fixture_gantry_y, crossbar_z])
            extrusion(130.0, "x", [0.66, 0.69, 0.72, 0.42]);
        gantry_l_connector_proxy(fixture_gantry_y, crossbar_z, false);
    }
}

// Top-down rail naming diagram.  Labels derive from the same frame dimensions
// as the production geometry, so the human/device and left/right contract
// cannot drift from the CAD.
module guide_detail_03_lower_frame_layout() {
    label_z = profile_size + 1.0;
    outer_frame_bottom(guide_complete_tint);

    guide_label("WIDTH-O-L",
                [frame_outer.x / 2, profile_size / 2, label_z], 10.0);
    guide_label("WIDTH-D-L",
                [frame_outer.x / 2,
                 frame_outer.y - profile_size / 2, label_z], 10.0);
    guide_label("DEPTH-L-L",
                [profile_size / 2, frame_outer.y / 2, label_z], 9.0,
                [0, 0, 90]);
    guide_label("DEPTH-R-L",
                [frame_outer.x - profile_size / 2,
                 frame_outer.y / 2, label_z], 9.0,
                [0, 0, -90]);
    guide_label("OPERATOR",
                [frame_outer.x / 2, -24.0, label_z], 11.0,
                [0, 0, 0], guide_spare_tint);
    guide_label("DEVICE / WALL",
                [frame_outer.x / 2, frame_outer.y + 24.0, label_z], 11.0,
                [0, 0, 0], guide_spare_tint);
}

// The complete gantry hovers above its final position.  Two arrows show that
// it must be lowered between the four still-open posts before the top ring is
// installed.
module guide_detail_04_lower_gantry() {
    lift = 54.0;
    outer_frame_bottom(guide_complete_tint);
    outer_frame_posts(guide_complete_tint);
    outer_corner_connector_proxies([false]);

    translate([0, 0, lift]) {
        fixture_gantry(guide_new_tint);
        gantry_crossbar_connector_proxies();
        gantry_joint_plate_previews();
        gantry_splice_previews();
    }

    for (x = [frame_outer.x * 0.32, frame_outer.x * 0.68])
        guide_axis_arrow([x, fixture_gantry_y - 18.0,
                          frame_outer.z + 44.0],
                         "z", -1, 48.0);
}

// Exact lower-left indexing plate relationship: one key enters the gantry
// upright; the perpendicular key enters the outer depth rail.
module guide_detail_04_joint_plate() {
    translate([gantry_upright_x.x, 0, outer_rail_z.x])
        extrusion(135.0, "y", [0.66, 0.69, 0.72, 0.42]);
    translate([gantry_upright_x.x, fixture_gantry_y,
               gantry_clear_z_min])
        extrusion(105.0, "z", [0.66, 0.69, 0.72, 0.42]);
    color(guide_new_tint)
        installed_gantry_joint_plate(fixture_gantry_y, false, false);
}

// Top-down placement datum for the movable gantry.  The blue arrow starts at
// the operator-side outside plane and ends at the upright centerline.
module guide_detail_04_gantry_position() {
    outer_frame_bottom([0.66, 0.69, 0.72, 0.42]);
    fixture_gantry(guide_new_tint);
    guide_axis_arrow([frame_outer.x / 2, 0, profile_size + 7.0],
                     "y", 1, fixture_gantry_y);
    guide_label("75 mm",
                [frame_outer.x / 2 - 30.0,
                 fixture_gantry_y / 2, profile_size + 8.0], 9.0,
                [0, 0, 90], guide_spare_tint);
    guide_label("OPERATOR PLANE",
                [frame_outer.x / 2, -24.0, profile_size + 8.0], 10.0,
                [0, 0, 0], guide_spare_tint);
}

// The upper ring is intentionally exploded above the four posts.  It is
// lowered as one subassembly only after the gantry is captive.
module guide_detail_05_lower_top_ring() {
    lift = 58.0;
    outer_frame_bottom(guide_complete_tint);
    outer_frame_posts(guide_complete_tint);
    outer_corner_connector_proxies([false]);
    fixture_gantry(guide_complete_tint);
    gantry_crossbar_connector_proxies();
    gantry_joint_plate_previews();
    gantry_splice_previews();

    translate([0, 0, lift]) {
        outer_frame_top(guide_new_tint);
        outer_corner_connector_proxies([true]);
    }

    for (x = [frame_outer.x * 0.28, frame_outer.x * 0.72])
        guide_axis_arrow([x, frame_outer.y / 2,
                          frame_outer.z + lift + 28.0],
                         "z", -1, 42.0);
}

// Top-down diagonal equality check used to square both rings.
module guide_detail_05_square_diagonals() {
    z = profile_size + 3.0;
    inset = profile_size / 2;
    outer_frame_bottom(guide_complete_tint);
    guide_segment([inset, inset, z],
                  [frame_outer.x - inset,
                   frame_outer.y - inset, z], 3.2);
    guide_segment([frame_outer.x - inset, inset, z],
                  [inset, frame_outer.y - inset, z], 3.2,
                  [0.96, 0.43, 0.08]);
    guide_label("A",
                [frame_outer.x * 0.30, frame_outer.y * 0.30, z + 1.0],
                13.0, [0, 0, 0], guide_spare_tint);
    guide_label("B",
                [frame_outer.x * 0.70, frame_outer.y * 0.30, z + 1.0],
                13.0, [0, 0, 0], guide_new_tint);
    guide_label("A AND B WITHIN 2 mm",
                [frame_outer.x / 2, frame_outer.y / 2, z + 1.0], 11.0);
}

// The two carrier-link lengths are easy to confuse on the bench.  This
// broad-face view uses the exact printable modules and derived lengths.
module guide_detail_06_carrier_link_lengths() {
    color(guide_new_tint) {
        translate([0, 30.0, 0])
            rotate([0, 0, 90]) rear_carrier_link_top();
        translate([0, -42.0, 0])
            rotate([0, 0, 90]) rear_carrier_link_bottom();
    }
    guide_label(str("UPPER  ", rear_carrier_top_length, " mm"),
                [0, 48.0, rear_carrier_link_thickness + 1.0], 8.5);
    guide_label(str("LOWER  ", rear_carrier_bottom_length, " mm"),
                [0, -23.0, rear_carrier_link_thickness + 1.0], 8.5);
}

// Side/exploded view of the exact fixture plate, its two crossbars, and all
// four keyed 5 mm spacers.  Blue arrows point from the plate toward the
// crossbar slots.
module guide_detail_07_fixture_spacers() {
    for (z = fixture_crossbar_z)
        translate([profile_size, fixture_gantry_y, z])
            extrusion(gantry_crossbar_length, "x",
                      [0.66, 0.69, 0.72, 0.46]);
    color([0.88, 0.88, 0.84, 0.30])
        fixture_mesh_at_installed_datum(fixture_presentation_mesh);
    for (x = fixture_mount_x)
        for (z = fixture_crossbar_z) {
            installed_fixture_plate_spacer([x, z]);
            guide_axis_arrow([x, fixture_plane_y - 16.0, z],
                             "y", 1, 14.0);
        }
}

// Optical-orientation proof without the surrounding frame.  The camera cone
// begins at the C270 lens and terminates at the complete DUT envelope.
module guide_detail_07_optical_axis() {
    color([0.88, 0.88, 0.84, 0.45])
        fixture_mesh_at_installed_datum(fixture_presentation_mesh);
    color([0.88, 0.88, 0.84, 0.45])
        cradle_mesh_at_installed_datum(cradle_body_presentation_mesh);
    color([0.15, 0.16, 0.17, 0.86])
        device_model_mesh_at_installed_datum(
            device_shell_presentation_mesh);
    webcam_preview();
    color([0.18, 0.72, 0.92, 0.20])
        camera_frustum_geometry();
}

// Installed operator-side placard interface.  The cartridge is intentionally
// withdrawn to the right and the arrow shows its insertion direction.
module guide_detail_08_placard() {
    insert_offset = 52.0;
    translate([profile_size, profile_size / 2, outer_rail_z.y])
        extrusion(structural_x_length, "x", guide_complete_tint);
    placard_risers_preview();
    placard_holder_preview();
    placard_insert_at_installed_datum(insert_offset)
        placard_insert_material_preview();
    guide_axis_arrow(
        [frame_outer.x / 2 + placard_size.x / 2 + 84.0,
         -(placard_spacer_thickness + placard_riser_size.z + 12.0),
         placard_center_z],
        "x", -1, 58.0);
}

// The mount blocks stay on the lower operator rail while the translucent
// power strip approaches their supplied screw heads from inside the chassis.
module guide_detail_08_power_strip() {
    exploded_y = 58.0;
    translate([profile_size, profile_size / 2, outer_rail_z.x])
        extrusion(structural_x_length, "x", guide_complete_tint);
    power_strip_mounts_preview();
    color([0.91, 0.91, 0.88, 0.50])
        translate([power_strip_left_x,
                   power_strip_mount_face_y + exploded_y,
                   power_strip_bottom_z])
            cube(power_strip_body_size);
    for (x = power_strip_block_x)
        guide_axis_arrow(
            [x, power_strip_mount_face_y + exploded_y - 4.0,
             power_strip_body_size.z / 2],
            "y", -1, exploded_y - 8.0);
}

// One exact upper corner shows the two perpendicular registration tabs and a
// ghosted lower corner of the chassis above.  The blue arrow is the stack
// direction; broad frame faces meet before the tab can carry vertical load.
module guide_detail_08_stacking_corner() {
    detail_length = 105.0;

    translate([profile_size / 2, profile_size / 2,
               frame_outer.z - 105.0])
        extrusion(detail_length, "z", guide_complete_tint);
    translate([profile_size, profile_size / 2, outer_rail_z.y])
        extrusion(detail_length, "x", guide_complete_tint);
    translate([profile_size / 2, profile_size, outer_rail_z.y])
        extrusion(detail_length, "y", guide_complete_tint);
    three_way_end_connector_proxy(false, false, true);

    color(guide_new_tint) {
        multmatrix([
            [0, 0, -1, 0],
            [1, 0, 0, 0],
            [0, 1, 0, registration_guide_bottom],
            [0, 0, 0, 1]
        ]) registration_tab();
        multmatrix([
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, registration_guide_bottom],
            [0, 0, 0, 1]
        ]) registration_tab();
    }

    color([0.66, 0.69, 0.72, 0.34]) {
        translate([profile_size / 2, profile_size / 2,
                   frame_outer.z + frame_aluminum_z_min])
            extrusion(90.0, "z");
        translate([profile_size, profile_size / 2,
                   frame_outer.z + outer_rail_z.x])
            extrusion(detail_length, "x");
        translate([profile_size / 2, profile_size,
                   frame_outer.z + outer_rail_z.x])
            extrusion(detail_length, "y");
    }
    guide_axis_arrow([62.0, 62.0, frame_outer.z + 88.0],
                     "z", -1, 55.0);
}

// These world-positioned layers are intentionally colorless STL exports. The
// pinned web-asset builder assigns one PBR material per named layer, retains
// semantic nodes in the GLB, and converts millimetres to metres.
module guide_layer_aluminum() {
    outer_frame();
    fixture_gantry();
}

module guide_layer_connectors() {
    outer_corner_connector_proxies();
    gantry_crossbar_connector_proxies();
}

module guide_layer_printed_hardware() {
    gantry_joint_plate_previews();
    gantry_splice_previews();
    plate_mount_previews();
    installed_registration_guides();
    power_strip_mounts_preview();
    placard_risers_preview();
}

module guide_layer_fixture_plate() {
    fixture_mesh_at_installed_datum(fixture_presentation_mesh);
}

module guide_layer_fixture_components() {
    fixture_mesh_at_installed_datum(
        fixture_components_presentation_mesh);
}

module guide_layer_fixture_labels() {
    fixture_mesh_at_installed_datum(fixture_labels_presentation_mesh);
}

module guide_layer_carrier_body() {
    cradle_mesh_at_installed_datum(cradle_body_presentation_mesh);
}

module guide_layer_carrier_labels() {
    cradle_mesh_at_installed_datum(cradle_labels_presentation_mesh);
}

module guide_layer_carrier_hooks() {
    cradle_mesh_at_installed_datum(cradle_hooks_presentation_mesh);
}

module guide_layer_device_shell() {
    device_model_mesh_at_installed_datum(device_shell_presentation_mesh);
}

module guide_layer_device_controls() {
    device_model_mesh_at_installed_datum(
        device_controls_presentation_mesh, 0.03);
}

module guide_layer_device_screen() {
    device_model_mesh_at_installed_datum(
        device_screen_presentation_mesh, 0.06);
}

module guide_layer_webcam() {
    webcam_preview();
}

module guide_layer_power_strip() {
    power_strip_body_preview();
}

module guide_layer_placard_holder() {
    placard_holder_preview();
}

module guide_layer_placard_insert() {
    placard_insert_at_installed_datum()
        placard_insert_blank();
}

module guide_layer_placard_labels() {
    placard_insert_at_installed_datum()
        placard_text();
}

module guide_layer_camera_frustum() {
    camera_frustum_geometry();
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
    if (SHOW_DEVICE) device_and_camera_preview(plate_detail);
    if (SHOW_CAMERA_FRUSTUM) camera_frustum_preview();
    if (SHOW_REGISTRATION_GUIDES) installed_registration_guides();
    if (SHOW_POWER_STRIP) power_strip_system_preview();
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
} else if (PART == "placard_holder") {
    placard_holder();
} else if (PART == "placard_insert") {
    placard_insert();
} else if (PART == "placard_slide_fit_coupon") {
    placard_slide_fit_coupon();
} else if (PART == "placard_system_preview") {
    placard_system_detail_preview();
} else if (PART == "power_strip_fit_coupon_set") {
    power_strip_fit_coupon_set();
} else if (PART == "power_strip_mount_block") {
    power_strip_mount_block();
} else if (PART == "power_strip_mount_block_pair") {
    power_strip_mount_block_pair();
} else if (PART == "power_strip_system_preview") {
    power_strip_system_preview();
} else if (PART == "ironing_test_coupon") {
    ironing_test_coupon();
} else if (PART == "ironing_test_coupon_set") {
    ironing_test_coupon_set();
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
} else if (PART == "gantry_splice_internal_bar") {
    gantry_splice_internal_bar();
} else if (PART == "gantry_splice_full_collar") {
    gantry_splice_full_collar_print();
} else if (PART == "gantry_splice_full_collar_internal_bar") {
    gantry_splice_full_collar_internal_bar();
} else if (PART == "gantry_splice_full_collar_internal_bar_pair") {
    gantry_splice_full_collar_internal_bar_pair();
} else if (PART == "gantry_splice_installed_preview") {
    gantry_splice_installed_preview();
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
} else if (PART == "production_batch_00_calibration") {
    production_batch_00_calibration();
} else if (PART == "production_batch_01_ironed_interfaces") {
    production_batch_01_ironed_interfaces();
} else if (PART == "production_batch_02_splice_collars") {
    production_batch_02_splice_collars();
} else if (PART == "production_batch_03_movable_mounts") {
    production_batch_03_movable_mounts();
} else if (PART == "production_batch_04_frame_hardware") {
    production_batch_04_frame_hardware();
} else if (PART == "production_batch_05_placard_holder") {
    production_batch_05_placard_holder();
} else if (PART == "production_batch_06_device_nameplate") {
    production_batch_06_device_nameplate();
} else if (PART == "production_batch_06_device_nameplate_body") {
    production_batch_06_device_nameplate_body();
} else if (PART == "production_batch_06_device_nameplate_labels") {
    production_batch_06_device_nameplate_labels();
} else if (PART == "production_batch_06_device_nameplate_preview") {
    production_batch_06_device_nameplate_preview();
} else if (PART == "guide_step_01_splice_uprights") {
    guide_step_01_splice_uprights();
} else if (PART == "guide_step_02_build_gantry") {
    guide_step_02_build_gantry();
} else if (PART == "guide_step_03_open_frame") {
    guide_step_03_open_frame();
} else if (PART == "guide_step_04_install_gantry") {
    guide_step_04_install_gantry();
} else if (PART == "guide_step_05_close_frame") {
    guide_step_05_close_frame();
} else if (PART == "guide_step_06_mount_carrier") {
    guide_step_06_mount_carrier();
} else if (PART == "guide_step_07_mount_fixture") {
    guide_step_07_mount_fixture();
} else if (PART == "guide_step_08_complete") {
    guide_step_08_complete();
} else if (PART == "guide_preload_channel_bar") {
    guide_preload_channel_bar();
} else if (PART == "guide_preload_map") {
    guide_preload_map();
} else if (PART == "guide_detail_02_crossbar_corner") {
    guide_detail_02_crossbar_corner();
} else if (PART == "guide_detail_03_lower_frame_layout") {
    guide_detail_03_lower_frame_layout();
} else if (PART == "guide_detail_04_lower_gantry") {
    guide_detail_04_lower_gantry();
} else if (PART == "guide_detail_04_joint_plate") {
    guide_detail_04_joint_plate();
} else if (PART == "guide_detail_04_gantry_position") {
    guide_detail_04_gantry_position();
} else if (PART == "guide_detail_05_lower_top_ring") {
    guide_detail_05_lower_top_ring();
} else if (PART == "guide_detail_05_square_diagonals") {
    guide_detail_05_square_diagonals();
} else if (PART == "guide_detail_06_carrier_link_lengths") {
    guide_detail_06_carrier_link_lengths();
} else if (PART == "guide_detail_07_fixture_spacers") {
    guide_detail_07_fixture_spacers();
} else if (PART == "guide_detail_07_optical_axis") {
    guide_detail_07_optical_axis();
} else if (PART == "guide_detail_08_placard") {
    guide_detail_08_placard();
} else if (PART == "guide_detail_08_power_strip") {
    guide_detail_08_power_strip();
} else if (PART == "guide_detail_08_stacking_corner") {
    guide_detail_08_stacking_corner();
} else if (PART == "guide_layer_aluminum") {
    guide_layer_aluminum();
} else if (PART == "guide_layer_connectors") {
    guide_layer_connectors();
} else if (PART == "guide_layer_printed_hardware") {
    guide_layer_printed_hardware();
} else if (PART == "guide_layer_fixture_plate") {
    guide_layer_fixture_plate();
} else if (PART == "guide_layer_fixture_components") {
    guide_layer_fixture_components();
} else if (PART == "guide_layer_fixture_labels") {
    guide_layer_fixture_labels();
} else if (PART == "guide_layer_carrier_body") {
    guide_layer_carrier_body();
} else if (PART == "guide_layer_carrier_labels") {
    guide_layer_carrier_labels();
} else if (PART == "guide_layer_carrier_hooks") {
    guide_layer_carrier_hooks();
} else if (PART == "guide_layer_device_shell") {
    guide_layer_device_shell();
} else if (PART == "guide_layer_device_controls") {
    guide_layer_device_controls();
} else if (PART == "guide_layer_device_screen") {
    guide_layer_device_screen();
} else if (PART == "guide_layer_webcam") {
    guide_layer_webcam();
} else if (PART == "guide_layer_power_strip") {
    guide_layer_power_strip();
} else if (PART == "guide_layer_placard_holder") {
    guide_layer_placard_holder();
} else if (PART == "guide_layer_placard_insert") {
    guide_layer_placard_insert();
} else if (PART == "guide_layer_placard_labels") {
    guide_layer_placard_labels();
} else if (PART == "guide_layer_camera_frustum") {
    guide_layer_camera_frustum();
} else if (PART == "cutlist") {
    cutlist_echo();
    cube([0.1, 0.1, 0.1]);
} else {
    assert(false, str("Unknown PART: ", PART));
}
