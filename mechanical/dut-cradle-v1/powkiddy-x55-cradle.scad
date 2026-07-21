/*
 * PocketForge reusable DUT cradle — Powkiddy X55 profile
 *
 * Coordinates: X left-to-right, Y bottom-to-top, Z toward the webcam; mm.
 * Owner-caliper dimensions govern every retention surface. Manufacturer data
 * is retained separately as a preview/reference envelope only.
 *
 * PART choices: assembly, plate, bottom_hook, top_hook, side_hook, hook_set,
 * fit_coupon. Preview geometry is background-only and cannot enter an STL.
 */

include <lib/dut-cradle-library.scad>;

PART = "assembly";
SHOW_DEVICE = true;
SHOW_HOOKS = true;
SHOW_KEEP_OUTS = true;
SHOW_LABELS = true;

$fn = 48;
epsilon = 0.05;

// ---- Carrier / printer datum ---------------------------------------------
printer_bed = [250, 210];
printer_edge_margin = 1.5;
printable_bed = printer_bed - [2 * printer_edge_margin,
                               2 * printer_edge_margin];
plate_size = [247, 175];
plate_thickness = 3.2;
plate_corner_radius = 4.0;

frame_tie_slot = [12.0, 5.5];
frame_tie_edge_inset = 7.0;
frame_tie_corner_offset = 18.0;
frame_tie_features = [
    ["bottom_left_bottom", [frame_tie_corner_offset, frame_tie_edge_inset], 0],
    ["bottom_left_left", [frame_tie_edge_inset, frame_tie_corner_offset], 90],
    ["bottom_right_bottom",
     [plate_size.x - frame_tie_corner_offset, frame_tie_edge_inset], 0],
    ["bottom_right_right",
     [plate_size.x - frame_tie_edge_inset, frame_tie_corner_offset], 90],
    ["top_left_top",
     [frame_tie_corner_offset, plate_size.y - frame_tie_edge_inset], 0],
    ["top_left_left",
     [frame_tie_edge_inset, plate_size.y - frame_tie_corner_offset], 90],
    ["top_right_top",
     [plate_size.x - frame_tie_corner_offset,
      plate_size.y - frame_tie_edge_inset], 0],
    ["top_right_right",
     [plate_size.x - frame_tie_edge_inset,
      plate_size.y - frame_tie_corner_offset], 90]
];

// ---- X55 measured/reference profile --------------------------------------
device_name = "Powkiddy X55";

// Owner trace/calipers: fit authority for the front shell and hooks.
device_max_width = 210.0;
device_reference_width = 200.0;          // immediately below shoulder keys
device_body_height = 88.76;
device_body_size = [device_max_width, device_body_height];

// Powkiddy publishes 212.5 x 94.5 x 19 mm. The extra XY envelope belongs to
// shoulders/edge protrusions, not the owner's traced hook-contact shell.
manufacturer_envelope = [212.5, 94.5, 19.0];
manufacturer_side_overhang =
    (manufacturer_envelope.x - device_max_width) / 2;
shoulder_preview_height = 6.0;
shoulder_preview_origin_y = device_body_height -
    (shoulder_preview_height -
     (manufacturer_envelope.y - device_body_height));
device_body_depth = manufacturer_envelope.z;
passive_depth_clearance = 0.60;
hook_throat = device_body_depth + passive_depth_clearance;

// Ten millimetres behind the nominal back shell follows the accepted fleet
// service datum. This remains deliberately named because the owner must still
// confirm the X55's maximum rear/trigger depth with calipers before printing.
minimum_rear_access = 10.0;
device_rear_gap = minimum_rear_access;
device_front_plane_from_carrier = device_rear_gap + device_body_depth;

device_origin = [(plate_size.x - device_max_width) / 2, 40.0];
device_centre = device_origin + device_body_size / 2;

// Exact 5.5-inch, 16:9 active-area proxy derived from the published diagonal.
screen_diagonal = 139.7;
screen_size = [
    screen_diagonal * 16 / sqrt(16 * 16 + 9 * 9),
    screen_diagonal * 9 / sqrt(16 * 16 + 9 * 9)
];
screen_centre = [device_centre.x, device_centre.y + 1.0];
screen_origin = screen_centre - screen_size / 2;

rear_service_window = [176.0, 62.0];
rear_service_origin = device_centre - rear_service_window / 2;
rear_service_radius = 9.0;

// ---- Owner-annotated contact windows and keep-outs -----------------------
// The 200 mm reference line is inset 5 mm from each 210 mm shell extreme.
reference_edge_inset = (device_max_width - device_reference_width) / 2;
left_reference_x = reference_edge_inset;
right_reference_x = device_max_width - reference_edge_inset;

// Top-left annotation, outward to inward: 33.48 shoulder exclusion, 7.8 mm
// power key, 16.36 mm clear band, then a 9 mm connector.
left_shoulder_keepout = [left_reference_x,
                         left_reference_x + 33.48];
left_power_keepout = [left_shoulder_keepout.y,
                      left_shoulder_keepout.y + 7.8];
top_left_safe = [left_power_keepout.y,
                 left_power_keepout.y + 16.36];
left_usb_keepout = [top_left_safe.y, top_left_safe.y + 9.0];

// Top-right annotation identifies a 33.87..38.59 mm reset/control feature.
// The adjacent 15 mm inboard span is the widest explicit clear top band.
right_shoulder_keepout = [right_reference_x - 33.87, right_reference_x];
right_reset_keepout = [right_reference_x - 38.59,
                       right_reference_x - 33.87];
top_right_safe = [right_reference_x - 53.59,
                  right_reference_x - 38.59];
right_audio_keepout = [right_reference_x - 61.59,
                       right_reference_x - 53.59];

// Bottom drawing: a centered 58 mm dual-TF exclusion, with explicitly safe
// 28 mm and 20 mm contact regions immediately to its left and right.
bottom_card_keepout = [device_max_width / 2 - 29.0,
                       device_max_width / 2 + 29.0];
bottom_left_safe = [bottom_card_keepout.x - 28.0,
                    bottom_card_keepout.x];
bottom_right_safe = [bottom_card_keepout.y,
                     bottom_card_keepout.y + 20.0];

top_left_contact_x = (top_left_safe.x + top_left_safe.y) / 2;
top_right_contact_x = (top_right_safe.x + top_right_safe.y) / 2;
bottom_left_contact_x = (bottom_left_safe.x + bottom_left_safe.y) / 2;
bottom_right_contact_x = (bottom_right_safe.x + bottom_right_safe.y) / 2;
side_contact_height = 45.0;              // widest, control-free side tangent

// pose = [name, shell-edge contact, inward angle, passive play, hook kind]
clamp_poses = [
    ["bottom_left",
     [device_origin.x + bottom_left_contact_x, device_origin.y],
     90, 0.25, "bottom"],
    ["bottom_right",
     [device_origin.x + bottom_right_contact_x, device_origin.y],
     90, 0.25, "bottom"],
    ["left_side",
     [device_origin.x, device_origin.y + side_contact_height],
     0, 0.50, "side"],
    ["right_side",
     [device_origin.x + device_max_width,
      device_origin.y + side_contact_height],
     180, 0.50, "side"],
    ["top_left",
     [device_origin.x + top_left_contact_x,
      device_origin.y + device_body_height],
     -90, 0.45, "top"],
    ["top_right",
     [device_origin.x + top_right_contact_x,
      device_origin.y + device_body_height],
     -90, 0.45, "top"]
];

function pose_name(pose) = pose[0];
function pose_contact(pose) = pose[1];
function pose_angle(pose) = pose[2];
function pose_play(pose) = pose[3];
function pose_kind(pose) = pose[4];
function pose_inward(pose) = pf_rotate_2d([1, 0], pose_angle(pose));
function pose_surface(pose) =
    pf_add_2d(pose_contact(pose),
              pf_scale_2d(-pose_play(pose), pose_inward(pose)));

// ---- Shared hook hardware / edge-specific contact profiles ---------------
bottom_hook_width = 8.0;
top_hook_width = 8.0;
side_hook_width = 8.0;
hook_wall = 4.0;
bottom_lip_depth = 3.0;
top_lip_depth = 1.6;
side_lip_depth = 2.4;
hook_lip_thickness = 4.0;
bottom_support_depth = 10.0;
top_support_depth = 7.0;
side_support_depth = 8.0;
hook_support_thickness = 3.2;
hook_base_outward = 13.0;
hook_base_inward = 4.0;
hook_base_height = 4.4;
hook_base_radius = 1.5;
hook_spine_width = 10.4;

m3_clearance = 3.5;
m3_nut_across_flats = 5.6;
m3_nut_depth = 2.8;
m3_nut_capture_wall = 2.4;
hook_screw_offset = [-8.0, -3.5];
hook_key_offset = [-8.0, 3.5];
hook_key_size = [4.0, 3.2];
hook_key_clearance = 0.35;
hook_keyway_depth = 1.2;
hook_adjustment = 8.0;
print_face_margin = 0.10;
hook_set_column_spacing = 29.0;
hook_set_row_spacing = 38.0;

// ---- Fleet-standard labels for the 0.8 mm nozzle -------------------------
label_height = 1.2;
label_stroke_growth = 1.10;
title_box_size = [176.0, 23.0];
title_box_centre = [plate_size.x / 2, plate_size.y - 14.5];
title_font_size = 14.4;
orientation_font_size = 9.5;
label_feature_clearance = 2.4;
top_label_center = [plate_size.x / 2, 139.0];
bottom_label_center = [plate_size.x / 2, 11.0];

// ---- Explicit mechanical invariants --------------------------------------
top_left_x = device_origin.x + top_left_contact_x;
top_right_x = device_origin.x + top_right_contact_x;
bottom_left_x = device_origin.x + bottom_left_contact_x;
bottom_right_x = device_origin.x + bottom_right_contact_x;
title_box_min = title_box_centre - title_box_size / 2;
title_box_max = title_box_centre + title_box_size / 2;
top_left_slot_outer_x = frame_tie_corner_offset + frame_tie_slot.x / 2;
top_right_slot_inner_x = plate_size.x - frame_tie_corner_offset -
                         frame_tie_slot.x / 2;
top_left_surface = pose_surface(clamp_poses[4]);
top_left_screw_point = pf_add_2d(
    top_left_surface,
    pf_rotate_2d(hook_screw_offset, pose_angle(clamp_poses[4]))
);
top_mount_outer_y = top_left_screw_point.y +
                    (hook_adjustment + m3_clearance) / 2;
bottom_left_surface = pose_surface(clamp_poses[0]);
bottom_left_screw_point = pf_add_2d(
    bottom_left_surface,
    pf_rotate_2d(hook_screw_offset, pose_angle(clamp_poses[0]))
);
bottom_mount_inner_y = bottom_left_screw_point.y -
                       (hook_adjustment + m3_clearance) / 2;

assert(plate_size.x <= printable_bed.x && plate_size.y <= printable_bed.y,
       "X55 carrier exceeds the conservative Prusa printable envelope");
assert(abs(device_max_width - 210.0) < 0.01 &&
       abs(device_body_height - 88.76) < 0.01 &&
       abs(device_reference_width - 200.0) < 0.01,
       "X55 profile must preserve owner 210/200/88.76 mm shell datums");
assert(abs(manufacturer_envelope.x - 212.5) < 0.01 &&
       abs(manufacturer_envelope.y - 94.5) < 0.01 &&
       abs(manufacturer_envelope.z - 19.0) < 0.01,
       "X55 manufacturer reference envelope changed unexpectedly");
assert(abs(shoulder_preview_origin_y + shoulder_preview_height -
           manufacturer_envelope.y) < 0.01,
       "X55 shoulder preview must reach the published overall height");
assert(device_origin.x >= hook_base_outward,
       "X55 carrier lacks lateral clamp margin");
assert(device_rear_gap >= minimum_rear_access &&
       minimum_rear_access >= 10.0,
       "X55 rear service gap must remain at least 10 mm");
assert(hook_throat > device_body_depth,
       "X55 hook throat must retain positive passive clearance");
assert(top_left_contact_x - top_hook_width / 2 >= top_left_safe.x &&
       top_left_contact_x + top_hook_width / 2 <= top_left_safe.y,
       "X55 top-left hook left its measured safe band");
assert(top_right_contact_x - top_hook_width / 2 >= top_right_safe.x &&
       top_right_contact_x + top_hook_width / 2 <= top_right_safe.y,
       "X55 top-right hook left its measured safe band");
assert(bottom_left_contact_x - bottom_hook_width / 2 >=
           bottom_left_safe.x &&
       bottom_left_contact_x + bottom_hook_width / 2 <=
           bottom_left_safe.y,
       "X55 bottom-left hook left its measured safe band");
assert(bottom_right_contact_x - bottom_hook_width / 2 >=
           bottom_right_safe.x &&
       bottom_right_contact_x + bottom_hook_width / 2 <=
           bottom_right_safe.y,
       "X55 bottom-right hook left its measured safe band");
assert(bottom_left_contact_x + bottom_hook_width / 2 <=
           bottom_card_keepout.x &&
       bottom_right_contact_x - bottom_hook_width / 2 >=
           bottom_card_keepout.y,
       "X55 lower hooks entered the 58 mm dual-TF keep-out");
assert(side_contact_height > 30 && side_contact_height < 60,
       "X55 side datums left the widest control-free shell band");
assert(title_box_min.x >= top_left_slot_outer_x + label_feature_clearance &&
       title_box_max.x <= top_right_slot_inner_x - label_feature_clearance,
       "X55 title box entered a top 4040 frame slot lane");
assert(title_box_min.y >= top_mount_outer_y + label_feature_clearance,
       "X55 title box entered the top-hook adjustment sweep");
assert(bottom_label_center.y + orientation_font_size / 2 +
           label_stroke_growth + label_feature_clearance <=
           bottom_mount_inner_y,
       "X55 BOTTOM label entered a lower-hook adjustment sweep");
assert(m3_nut_capture_wall >= 2.4,
       "X55 M3 nut capture wall must remain at least three nozzle widths");
assert(hook_key_offset.y + hook_key_size.y / 2 + print_face_margin <=
           hook_spine_width / 2,
       "X55 anti-rotation key must not protrude below the broad print face");
assert(hook_set_row_spacing >= device_rear_gap + hook_throat +
           hook_lip_thickness + hook_keyway_depth + 2.0,
       "X55 arranged hook rows must remain discrete printable parts");
assert(rear_service_origin.x >= device_origin.x + 10 &&
       rear_service_origin.y >= device_origin.y + 8 &&
       rear_service_origin.x + rear_service_window.x <=
           device_origin.x + device_max_width - 10 &&
       rear_service_origin.y + rear_service_window.y <=
           device_origin.y + device_body_height - 8,
       "X55 service aperture escaped the structural shell perimeter");

// ---- Carrier --------------------------------------------------------------
module embossed_text(point, message, size, halign = "center") {
    translate([point.x, point.y, plate_thickness])
        linear_extrude(height = label_height)
            offset(delta = label_stroke_growth)
                text(message, size = size, halign = halign,
                     valign = "center",
                     font = "Liberation Sans Narrow:style=Bold");
}

module label_box(centre, size, message, font_size) {
    translate([centre.x - size.x / 2,
               centre.y - size.y / 2,
               plate_thickness]) {
        linear_extrude(height = label_height)
            difference() {
                pf_rounded_rect_2d(size, 2.0);
                translate([1.2, 1.2])
                    pf_rounded_rect_2d(size - [2.4, 2.4], 1.2);
            }
        translate([size.x / 2, size.y / 2, 0])
            linear_extrude(height = label_height)
                offset(delta = label_stroke_growth)
                    text(message, size = font_size,
                         halign = "center", valign = "center",
                         font = "Liberation Sans Narrow:style=Bold");
    }
}

module carrier_labels() {
    label_box(title_box_centre, title_box_size,
              device_name, title_font_size);
    embossed_text(top_label_center, "TOP", orientation_font_size);
    embossed_text(bottom_label_center, "BOTTOM",
                  orientation_font_size);
}

module carrier_plate() {
    union() {
        difference() {
            pf_rounded_prism(
                [plate_size.x, plate_size.y, plate_thickness],
                plate_corner_radius
            );

            pf_frame_tie_holes(
                frame_tie_features, frame_tie_slot,
                plate_thickness + 2 * epsilon
            );

            translate([rear_service_origin.x, rear_service_origin.y,
                       -epsilon])
                linear_extrude(height = plate_thickness + 2 * epsilon)
                    pf_rounded_rect_2d(rear_service_window,
                                       rear_service_radius);

            for (pose = clamp_poses)
                pf_clamp_mount_cutouts(
                    pose_surface(pose), pose_angle(pose), plate_thickness,
                    hook_screw_offset, hook_key_offset, hook_adjustment,
                    m3_clearance, hook_key_size, hook_key_clearance,
                    hook_keyway_depth, epsilon
                );
        }

        if (SHOW_LABELS)
            carrier_labels();
    }
}

function hook_width(kind) =
    kind == "bottom" ? bottom_hook_width :
    kind == "top" ? top_hook_width : side_hook_width;
function hook_lip_depth(kind) =
    kind == "bottom" ? bottom_lip_depth :
    kind == "top" ? top_lip_depth : side_lip_depth;
function hook_support_depth(kind) =
    kind == "bottom" ? bottom_support_depth :
    kind == "top" ? top_support_depth : side_support_depth;

module one_hook_installed(pose) {
    kind = pose_kind(pose);
    pf_installed_j_hook(
        pose_surface(pose), pose_angle(pose), plate_thickness,
        hook_throat, device_rear_gap, hook_width(kind), hook_wall,
        hook_lip_depth(kind), hook_lip_thickness,
        hook_support_depth(kind), hook_support_thickness,
        hook_base_outward, hook_base_inward, hook_base_height,
        hook_base_radius, hook_screw_offset, hook_key_offset,
        m3_clearance, m3_nut_across_flats, m3_nut_depth,
        m3_nut_capture_wall, hook_key_size, hook_keyway_depth,
        epsilon, hook_spine_width
    );
}

module one_hook_printable(kind) {
    pf_print_oriented_j_hook(
        hook_throat, device_rear_gap, hook_width(kind), hook_wall,
        hook_lip_depth(kind), hook_lip_thickness,
        hook_support_depth(kind), hook_support_thickness,
        hook_base_outward, hook_base_inward, hook_base_height,
        hook_base_radius, hook_screw_offset, hook_key_offset,
        m3_clearance, m3_nut_across_flats, m3_nut_depth,
        m3_nut_capture_wall, hook_key_size, hook_keyway_depth,
        epsilon, hook_spine_width
    );
}

module hook_set() {
    for (column = [0 : 2])
        translate([column * hook_set_column_spacing, 0, 0])
            one_hook_printable(column == 0 ? "bottom" :
                               column == 1 ? "top" : "side");
    for (column = [0 : 2])
        translate([column * hook_set_column_spacing,
                   hook_set_row_spacing, 0])
            one_hook_printable(column == 0 ? "bottom" :
                               column == 1 ? "top" : "side");
}

module coupon_plate() {
    coupon_size = [118, 36];
    contact_y = 20;
    production_spacing = bottom_right_contact_x - bottom_left_contact_x;
    left_x = coupon_size.x / 2 - production_spacing / 2;
    right_x = coupon_size.x / 2 + production_spacing / 2;
    difference() {
        pf_rounded_prism([coupon_size.x, coupon_size.y, plate_thickness], 3);
        for (contact_x = [left_x, right_x])
            pf_clamp_mount_cutouts(
                [contact_x, contact_y - 0.25], 90, plate_thickness,
                hook_screw_offset, hook_key_offset, hook_adjustment,
                m3_clearance, hook_key_size, hook_key_clearance,
                hook_keyway_depth, epsilon
            );
    }
}

module fit_coupon() {
    coupon_plate();
    translate([22, 43, 0]) one_hook_printable("bottom");
    translate([64, 43, 0]) one_hook_printable("bottom");
}

// ---- Preview-only high-fidelity device proxy -----------------------------
// The polygon follows the owner trace: 210 mm maximum width, a 200 mm upper
// reference width, and the X55's shallow lower waist / broad hand grips.
module x55_outline_2d() {
    polygon(points = [
        [35, 0], [58, 0.2], [82, 0.8], [105, 0.4], [128, 0.8],
        [152, 0.2], [175, 0], [188, 2], [198, 7], [204, 14],
        [207, 22], [209, 32], [210, 45], [209, 62], [207, 73],
        [204, 80], [200, 84], [196, 86.5], [190, 88],
        [178, 88.76], [32, 88.76], [20, 88], [14, 86.5],
        [10, 84], [6, 80], [3, 73], [1, 62], [0, 45], [1, 32],
        [3, 22], [6, 14], [12, 7], [22, 2]
    ]);
}

module cross_control(point, size, z) {
    color([0.10, 0.11, 0.12, 0.95])
        translate([point.x, point.y, z])
            linear_extrude(height = 1.2)
                union() {
                    translate([-size / 2, -size / 6])
                        square([size, size / 3]);
                    translate([-size / 6, -size / 2])
                        square([size / 3, size]);
                }
}

module x55_device_preview() {
    rear_z = plate_thickness + device_rear_gap;
    front_z = plate_thickness + device_front_plane_from_carrier;

    color([0.15, 0.17, 0.18, 0.72])
        translate([device_origin.x, device_origin.y, rear_z])
            linear_extrude(height = device_body_depth)
                x55_outline_2d();

    color([0.08, 0.42, 0.78, 0.80])
        translate([screen_origin.x, screen_origin.y, front_z + 0.05])
            cube([screen_size.x, screen_size.y, 0.35]);

    // Analog controls, face buttons, D-pad, and four function keys.
    color([0.08, 0.09, 0.10, 0.96]) {
        for (point = [[22, 68], [184, 35]])
            translate([device_origin.x + point.x,
                       device_origin.y + point.y, front_z + 0.4])
                cylinder(d = 18, h = 1.8);
        for (point = [[181, 71], [194, 64], [181, 57], [168, 64]])
            translate([device_origin.x + point.x,
                       device_origin.y + point.y, front_z + 0.4])
                cylinder(d = 7.2, h = 1.4);
        for (point = [[15, 12], [31, 12], [179, 12], [195, 12]])
            translate([device_origin.x + point.x,
                       device_origin.y + point.y, front_z + 0.4])
                cylinder(d = 6.6, h = 1.2);
    }
    cross_control([device_origin.x + 22, device_origin.y + 38],
                  20, front_z + 0.4);

    // Shoulder stacks extend the traced front shell toward the published
    // 212.5 x 94.5 mm overall envelope.
    color([0.05, 0.06, 0.07, 0.92])
        for (x_pair = [[-manufacturer_side_overhang, 38.5],
                       [171.5,
                        device_max_width + manufacturer_side_overhang]])
            translate([device_origin.x + x_pair.x,
                       device_origin.y + shoulder_preview_origin_y,
                       rear_z + device_body_depth - 4])
                linear_extrude(height = 4.2)
                    hull() {
                        translate([3, 1]) circle(r = 3);
                        translate([x_pair.y - x_pair.x - 3, 3]) circle(r = 3);
                    }

    // Back grip pads make the pronounced rear palm contours visible without
    // claiming an unmeasured extra Z depth.
    color([0.45, 0.18, 0.65, 0.62])
        for (x = [device_origin.x + 7,
                  device_origin.x + device_max_width - 30])
            translate([x, device_origin.y + 9, rear_z - 0.15])
                linear_extrude(height = 0.3)
                    pf_rounded_rect_2d([23, 54], 9);
}

module band_preview(range, y, width, color_value, z) {
    color(color_value)
        translate([device_origin.x + range.x, y, z])
            cube([range.y - range.x, width, 0.8]);
}

module keep_out_preview() {
    front_z = plate_thickness + device_front_plane_from_carrier;
    green = [0.15, 0.95, 0.35, 0.80];
    orange = [1.0, 0.50, 0.08, 0.76];
    red = [0.95, 0.12, 0.20, 0.76];

    // Green contact bands reproduce the four annotated safe regions.
    band_preview(top_left_safe,
                 device_origin.y + device_body_height - 1, 2,
                 green, front_z + 0.8);
    band_preview(top_right_safe,
                 device_origin.y + device_body_height - 1, 2,
                 green, front_z + 0.8);
    band_preview(bottom_left_safe, device_origin.y - 1, 2,
                 green, front_z + 0.8);
    band_preview(bottom_right_safe, device_origin.y - 1, 2,
                 green, front_z + 0.8);
    color(green)
        for (x = [device_origin.x - 1,
                  device_origin.x + device_max_width - 1])
            translate([x, device_origin.y + side_contact_height -
                       side_hook_width / 2, front_z + 0.8])
                cube([2, side_hook_width, 0.8]);

    // Orange port/button features come directly from the owner's top-edge
    // caliper chain; red is reserved for shoulder/dual-card exclusions.
    for (range = [left_power_keepout, left_usb_keepout,
                  right_reset_keepout, right_audio_keepout])
        band_preview(range, device_origin.y + device_body_height - 2,
                     4, orange, front_z + 1.0);
    for (range = [left_shoulder_keepout, right_shoulder_keepout])
        band_preview(range, device_origin.y + device_body_height - 3,
                     6, red, front_z + 1.2);
    band_preview(bottom_card_keepout, device_origin.y - 3, 6,
                 red, front_z + 1.2);
}

module assembly() {
    carrier_plate();

    if (SHOW_DEVICE)
        %x55_device_preview();

    if (SHOW_KEEP_OUTS)
        %keep_out_preview();

    if (SHOW_HOOKS)
        for (pose = clamp_poses)
            %one_hook_installed(pose);
}

if (PART == "assembly") {
    assembly();
} else if (PART == "plate") {
    carrier_plate();
} else if (PART == "bottom_hook") {
    one_hook_printable("bottom");
} else if (PART == "top_hook") {
    one_hook_printable("top");
} else if (PART == "side_hook") {
    one_hook_printable("side");
} else if (PART == "hook_set") {
    hook_set();
} else if (PART == "fit_coupon") {
    fit_coupon();
} else {
    assert(false, str("Unknown PART: ", PART));
}
