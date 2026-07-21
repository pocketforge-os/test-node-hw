/*
 * PocketForge reusable DUT cradle — Anbernic RG353V profile
 *
 * Coordinates: X left-to-right, Y bottom-to-top, Z toward the webcam; mm.
 * The RG353V has a strongly rounded lower grip while its upper display edge
 * permits only shallow contact. Per-hook shelves share one measured shell
 * depth and one rear datum so the front glass remains parallel to the camera.
 *
 * PART choices: assembly, plate, lower_hook, upper_hook, hook_set, fit_coupon.
 * Preview geometry is background-only and cannot leak into printable exports.
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

// Match the accepted portrait-device convention and leave a dedicated top
// title lane. The carrier fits the conservative 247 x 207 mm bed envelope.
plate_size = [180, 205];
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

// ---- RG353V measured / manufacturer mechanical profile -------------------
device_name = "Anbernic RG353V";
// Anbernic publishes 12.6 x 8.3 x 2.1 cm. The owner's local depth and contact
// measurements below govern the fit; confirm this front envelope by caliper.
device_body_size = [83.0, 126.0];
device_bottom_corner_radius = 14.0;       // preview proxy, not a fit surface
// Lower the DUT slightly from plate centre to make room for top-edge hook
// adjustment while retaining the fleet-standard title lane.
device_origin = [(plate_size.x - device_body_size.x) / 2, 34.0];
device_centre = device_origin + device_body_size / 2;

// Owner-caliper shell thickness. The lower grip/control region rises about
// 70 mm, but does not establish a different hook capture depth.
lower_region_height = 70.0;
measured_body_depth = 18.77;
lower_body_depth = measured_body_depth;
upper_body_depth = measured_body_depth;

// Ten millimetres behind the shell clears the beefy rear grips and triggers,
// provides airflow, and admits a finger. Both hook families share this datum.
minimum_rear_clearance = 10.0;
lower_rear_gap = 10.0;
upper_rear_gap = lower_rear_gap;
passive_depth_clearance = 0.60;
lower_throat = lower_body_depth + passive_depth_clearance;
upper_throat = upper_body_depth + passive_depth_clearance;

// Owner annotated approximately 55 mm of display height and an 8 mm safe
// front-bezel band. Width remains preview-only.
screen_size = [77.0, 55.0];
screen_top_margin = 2.0;
screen_origin = [
    device_origin.x + (device_body_size.x - screen_size.x) / 2,
    device_origin.y + device_body_size.y - screen_top_margin - screen_size.y
];
upper_safe_bezel_band = 8.0;

// Open back for triggers, airflow, wiring, and a finger behind the DUT.
rear_service_window = [59.0, 102.0];
rear_service_origin = device_centre - rear_service_window / 2;
rear_service_radius = 8.0;

// ---- Four top/bottom contacts / explicit keep-outs -----------------------
// Top and bottom contact centres are each 31 mm inward from the corresponding
// device edge, exactly matching the owner sketch (therefore 21 mm apart).
bottom_contact_inset = 31.0;
top_contact_inset = 31.0;
bottom_port_keepout_width = 13.0;
top_center_keepout_width = 13.0;
top_shoulder_keepout_width = 24.0;

// Manufacturer imagery shows rear shoulder triggers at the outer top corners,
// a left volume rocker, and a right power/reset/dual-TF stack. Owner calipers
// put the side/grip depth anywhere from 19 to 29 mm. Both sides therefore stay
// completely contact-free.
trigger_keepout_y = [60.0, 82.0];
left_volume_keepout_y = [82.0, 106.0];
right_power_keepout_y = [96.0, 108.0];
right_reset_keepout_y = [79.0, 92.0];
right_tf1_keepout_y = [50.0, 67.0];
right_tf2_keepout_y = [25.0, 42.0];

// pose = [name, exact shell-edge contact point, inward angle, play, kind]
clamp_poses = [
    ["bottom_left",
     [device_origin.x + bottom_contact_inset, device_origin.y],
     90, 0.25, "lower"],
    ["bottom_right",
     [device_origin.x + device_body_size.x - bottom_contact_inset,
      device_origin.y],
     90, 0.25, "lower"],
    ["top_left",
     [device_origin.x + top_contact_inset,
      device_origin.y + device_body_size.y],
     -90, 0.45, "upper"],
    ["top_right",
     [device_origin.x + device_body_size.x - top_contact_inset,
      device_origin.y + device_body_size.y],
     -90, 0.45, "upper"]
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

// ---- Shared hook hardware / two contact profiles -------------------------
// Eight-millimetre bottom contacts leave an exact 13 mm centre cable lane at
// the owner-specified 31 mm support centres. The wider structural spine below
// still supplies the broad, support-free print face.
lower_hook_width = 8.0;
upper_hook_width = 8.0;
hook_wall = 4.0;
lower_lip_depth = 3.0;
upper_lip_depth = 1.2;
hook_lip_thickness = 4.0;
// Long lower shelves reach beneath the owner's annotated curved profile.
lower_support_depth = 12.0;
upper_support_depth = 7.0;
hook_support_thickness = 3.2;
hook_base_outward = 13.0;
hook_base_inward = 4.0;
hook_base_height = 4.4;
hook_base_radius = 1.5;
// The structural spine remains wide enough to put a continuous broad face on
// layer one; shell-contact shelves/lips retain their narrower safe widths.
hook_spine_width = 10.4;

m3_clearance = 3.5;
m3_nut_across_flats = 5.6;               // accepted shared press-fit datum
m3_nut_depth = 2.8;
m3_nut_capture_wall = 2.4;
hook_screw_offset = [-8.0, -3.5];
hook_key_offset = [-8.0, 3.5];
hook_key_size = [4.0, 3.2];
hook_key_clearance = 0.35;
hook_keyway_depth = 1.2;
hook_adjustment = 8.0;
print_face_margin = 0.10;

// ---- Fleet-standard labels for the 0.8 mm nozzle -------------------------
label_height = 1.2;
label_stroke_growth = 1.10;
title_box_size = [124.0, 24.0];
title_box_centre = [plate_size.x / 2, plate_size.y - 15.0];
title_font_size = 14.4;
orientation_font_size = 10.5;
label_feature_clearance = 2.4;

top_label_center = [plate_size.x - 25.0, plate_size.y - 38.0];
bottom_label_center = [plate_size.x / 2, 10.5];

// ---- Explicit mechanical invariants --------------------------------------
lower_front_datum = lower_rear_gap + lower_throat;
upper_front_datum = upper_rear_gap + upper_throat;
bottom_left_x = device_origin.x + bottom_contact_inset;
bottom_right_x = device_origin.x + device_body_size.x - bottom_contact_inset;
top_left_x = device_origin.x + top_contact_inset;
top_right_x = device_origin.x + device_body_size.x - top_contact_inset;
bottom_port_keepout = [
    device_origin.x + (device_body_size.x - bottom_port_keepout_width) / 2,
    device_origin.x + (device_body_size.x + bottom_port_keepout_width) / 2
];
top_center_keepout = [
    device_origin.x + (device_body_size.x - top_center_keepout_width) / 2,
    device_origin.x + (device_body_size.x + top_center_keepout_width) / 2
];
title_box_min = title_box_centre - title_box_size / 2;
title_box_max = title_box_centre + title_box_size / 2;
top_left_slot_outer_x = frame_tie_corner_offset + frame_tie_slot.x / 2;
top_right_slot_inner_x = plate_size.x - frame_tie_corner_offset -
                         frame_tie_slot.x / 2;
top_label_outer_y = top_label_center.y +
                    orientation_font_size / 2 + label_stroke_growth;
bottom_label_outer_y = bottom_label_center.y +
                       orientation_font_size / 2 + label_stroke_growth;
bottom_left_surface = pose_surface(clamp_poses[0]);
bottom_left_screw_point = pf_add_2d(
    bottom_left_surface,
    pf_rotate_2d(hook_screw_offset, pose_angle(clamp_poses[0]))
);
bottom_mount_inner_y = bottom_left_screw_point.y -
                       (hook_adjustment + m3_clearance) / 2;
top_left_surface = pose_surface(clamp_poses[2]);
top_left_screw_point = pf_add_2d(
    top_left_surface,
    pf_rotate_2d(hook_screw_offset, pose_angle(clamp_poses[2]))
);
top_mount_outer_y = top_left_screw_point.y +
                    (hook_adjustment + m3_clearance) / 2;
side_contact_count = len([
    for (pose = clamp_poses)
        if (abs(pose_inward(pose).x) > 0.5) 1
]);

assert(plate_size.x <= printable_bed.x && plate_size.y <= printable_bed.y,
       "RG353V carrier exceeds the conservative Prusa printable envelope");
assert(device_origin.x > hook_base_outward &&
       device_origin.y > hook_base_outward,
       "RG353V carrier lacks clamp margin outside the DUT");
assert(lower_rear_gap >= minimum_rear_clearance &&
       upper_rear_gap >= minimum_rear_clearance,
       "RG353V rear gaps must preserve hand, trigger, and wiring access");
assert(abs(lower_front_datum - upper_front_datum) < 0.01,
       "RG353V hook families must share one flat front contact plane");
assert(lower_throat > lower_body_depth && upper_throat > upper_body_depth,
       "RG353V hook throats must retain positive passive clearance");
assert(lower_support_depth >= 10.0,
       "RG353V curved lower shell requires long support shelves");
assert(lower_lip_depth < bottom_contact_inset -
       device_bottom_corner_radius,
       "RG353V bottom lips entered the rounded corner transition");
assert(side_contact_count == 0,
       "RG353V variable-depth sides must remain completely contact-free");
assert(top_left_x - upper_hook_width / 2 >=
           device_origin.x + top_shoulder_keepout_width &&
       top_right_x + upper_hook_width / 2 <=
           device_origin.x + device_body_size.x -
           top_shoulder_keepout_width,
       "RG353V top supports entered an outer shoulder-trigger keep-out");
assert(upper_lip_depth < min(upper_safe_bezel_band,
                            (device_body_size.x - screen_size.x) / 2),
       "RG353V upper lip could cover active screen pixels");
assert(abs((bottom_left_x - device_origin.x) -
           (device_origin.x + device_body_size.x - bottom_right_x)) < 0.01,
       "RG353V bottom supports must remain symmetric");
assert(abs((top_left_x - device_origin.x) -
           (device_origin.x + device_body_size.x - top_right_x)) < 0.01,
       "RG353V top supports must remain symmetric");
assert(abs(top_left_x - bottom_left_x) < 0.01 &&
       abs(top_right_x - bottom_right_x) < 0.01,
       "RG353V top and bottom supports must share vertical datums");
assert(bottom_left_x + lower_hook_width / 2 <= bottom_port_keepout.x &&
       bottom_right_x - lower_hook_width / 2 >= bottom_port_keepout.y,
       "RG353V bottom supports entered the center USB-C cable keep-out");
assert(top_left_x + upper_hook_width / 2 <= top_center_keepout.x &&
       top_right_x - upper_hook_width / 2 >= top_center_keepout.y,
       "RG353V top supports entered the center port keep-out");
assert(title_box_min.x >= top_left_slot_outer_x + label_feature_clearance &&
       title_box_max.x <= top_right_slot_inner_x - label_feature_clearance,
       "RG353V title box entered a top 4040 frame slot lane");
assert(title_box_min.y >= device_origin.y + device_body_size.y +
       label_feature_clearance,
       "RG353V title box entered the DUT envelope");
assert(top_mount_outer_y + label_feature_clearance <= title_box_min.y,
       "RG353V top hook adjustment entered the device title box");
assert(top_label_outer_y + label_feature_clearance <= title_box_min.y,
       "RG353V TOP label entered the device title box");
assert(bottom_label_outer_y + label_feature_clearance <=
       bottom_mount_inner_y,
       "RG353V BOTTOM label entered a lower hook adjustment sweep");
assert(m3_nut_capture_wall >= 2.4,
       "RG353V M3 nut capture wall must remain at least three nozzle widths");
assert(hook_key_offset.y + hook_key_size.y / 2 + print_face_margin <=
           hook_spine_width / 2,
       "RG353V anti-rotation keys must not protrude below the broad print face");
assert(rear_service_origin.x > device_origin.x &&
       rear_service_origin.y > device_origin.y &&
       rear_service_origin.x + rear_service_window.x <
           device_origin.x + device_body_size.x &&
       rear_service_origin.y + rear_service_window.y <
           device_origin.y + device_body_size.y,
       "RG353V service aperture must remain inside the DUT footprint");

// ---- Carrier --------------------------------------------------------------
module embossed_text(point, message, size, rotation = 0,
                     halign = "center") {
    translate([point.x, point.y, plate_thickness])
        linear_extrude(height = label_height)
            rotate(rotation)
                offset(delta = label_stroke_growth)
                    text(message, size = size, halign = halign,
                         valign = "center",
                         font = "Liberation Sans:style=Bold");
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

module one_hook_installed(pose) {
    upper = pose_kind(pose) == "upper";
    pf_installed_j_hook(
        pose_surface(pose), pose_angle(pose), plate_thickness,
        upper ? upper_throat : lower_throat,
        upper ? upper_rear_gap : lower_rear_gap,
        upper ? upper_hook_width : lower_hook_width,
        hook_wall,
        upper ? upper_lip_depth : lower_lip_depth,
        hook_lip_thickness,
        upper ? upper_support_depth : lower_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, m3_nut_across_flats,
        m3_nut_depth, m3_nut_capture_wall, hook_key_size,
        hook_keyway_depth, epsilon, hook_spine_width
    );
}

module lower_hook_printable() {
    pf_print_oriented_j_hook(
        lower_throat, lower_rear_gap, lower_hook_width, hook_wall,
        lower_lip_depth, hook_lip_thickness, lower_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, m3_nut_across_flats,
        m3_nut_depth, m3_nut_capture_wall, hook_key_size,
        hook_keyway_depth, epsilon, hook_spine_width
    );
}

module upper_hook_printable() {
    pf_print_oriented_j_hook(
        upper_throat, upper_rear_gap, upper_hook_width, hook_wall,
        upper_lip_depth, hook_lip_thickness, upper_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, m3_nut_across_flats,
        m3_nut_depth, m3_nut_capture_wall, hook_key_size,
        hook_keyway_depth, epsilon, hook_spine_width
    );
}

module hook_set() {
    for (column = [0 : 1])
        translate([column * 27, 0, 0]) lower_hook_printable();
    translate([0, 43, 0]) upper_hook_printable();
    translate([27, 43, 0]) upper_hook_printable();
}

// Two bottom mount interfaces at their production 21 mm separation. Printing
// this small plate plus two lower hooks validates the curved lower shell before
// spending filament on the full carrier.
module curved_bottom_coupon_plate() {
    coupon_size = [70, 36];
    contact_y = 20;
    left_contact_x = coupon_size.x / 2 -
                     (device_body_size.x - 2 * bottom_contact_inset) / 2;
    right_contact_x = coupon_size.x / 2 +
                      (device_body_size.x - 2 * bottom_contact_inset) / 2;
    difference() {
        pf_rounded_prism([coupon_size.x, coupon_size.y, plate_thickness], 3);
        for (contact_x = [left_contact_x, right_contact_x])
            pf_clamp_mount_cutouts(
                [contact_x, contact_y - 0.25], 90, plate_thickness,
                hook_screw_offset, hook_key_offset, hook_adjustment,
                m3_clearance, hook_key_size, hook_key_clearance,
                hook_keyway_depth, epsilon
            );
    }
}

module fit_coupon() {
    curved_bottom_coupon_plate();
    translate([8, 42, 0]) lower_hook_printable();
    translate([36, 42, 0]) lower_hook_printable();
}

// ---- Preview-only device / controls / keep-outs --------------------------
module rg353v_outline_2d() {
    radius = device_bottom_corner_radius;
    union() {
        translate([0, radius])
            square([device_body_size.x, device_body_size.y - radius]);
        translate([radius, 0])
            square([device_body_size.x - 2 * radius, radius]);
        translate([radius, radius]) circle(r = radius);
        translate([device_body_size.x - radius, radius]) circle(r = radius);
    }
}

module rg353v_device_preview() {
    front_plane = plate_thickness + lower_rear_gap + lower_body_depth;

    color([0.12, 0.14, 0.16, 0.62]) {
        translate([device_origin.x, device_origin.y,
                   plate_thickness + lower_rear_gap])
            intersection() {
                linear_extrude(height = lower_body_depth)
                    rg353v_outline_2d();
                cube([device_body_size.x, lower_region_height,
                      lower_body_depth]);
            }

        translate([device_origin.x, device_origin.y,
                   plate_thickness + upper_rear_gap])
            intersection() {
                linear_extrude(height = upper_body_depth)
                    rg353v_outline_2d();
                translate([0, lower_region_height, 0])
                    cube([device_body_size.x,
                          device_body_size.y - lower_region_height,
                          upper_body_depth]);
            }
    }

    color([0.10, 0.55, 0.88, 0.78])
        translate([screen_origin.x, screen_origin.y, front_plane + 0.05])
            cube([screen_size.x, screen_size.y, 0.35]);

    // Front-control proxies make accidental lip overlap obvious.
    color([0.30, 0.32, 0.34, 0.90]) {
        translate([device_origin.x + 22, device_origin.y + 26,
                   front_plane + 0.45]) cylinder(d = 20, h = 1.2);
        translate([device_origin.x + device_body_size.x - 22,
                   device_origin.y + 26, front_plane + 0.45])
            cylinder(d = 20, h = 1.2);
    }
}

module keep_out_preview() {
    front_plane = plate_thickness + lower_rear_gap + lower_body_depth;

    // Safe top/bottom contact bands are green.
    color([0.15, 0.95, 0.35, 0.78]) {
        for (bottom_x = [bottom_left_x, bottom_right_x])
            translate([bottom_x - lower_hook_width / 2,
                       device_origin.y - 1, front_plane + 0.7])
                cube([lower_hook_width, 2, 0.8]);
        for (top_x = [top_left_x, top_right_x])
            translate([top_x - upper_hook_width / 2,
                       device_origin.y + device_body_size.y - 1,
                       front_plane + 0.7])
                cube([upper_hook_width, 2, 0.8]);
    }

    // Rear triggers occupy both the side transition and outer top corners.
    color([0.95, 0.12, 0.20, 0.72]) {
        for (side_x = [device_origin.x - 3,
                       device_origin.x + device_body_size.x - 2])
            translate([side_x,
                       device_origin.y + trigger_keepout_y.x,
                       plate_thickness + lower_rear_gap - 4])
                cube([5, trigger_keepout_y.y - trigger_keepout_y.x, 6]);
        for (top_x = [device_origin.x,
                      device_origin.x + device_body_size.x -
                      top_shoulder_keepout_width])
            translate([top_x,
                       device_origin.y + device_body_size.y - 3,
                       front_plane - 8])
                cube([top_shoulder_keepout_width, 6, 8]);
    }

    // Orange side-control/TF exclusions come from Anbernic product imagery.
    color([1.0, 0.50, 0.08, 0.72]) {
        translate([bottom_port_keepout.x, device_origin.y - 4,
                   front_plane - 8])
            cube([bottom_port_keepout_width, 6, 8]);
        translate([top_center_keepout.x,
                   device_origin.y + device_body_size.y - 2,
                   front_plane - 8])
            cube([top_center_keepout_width, 6, 8]);
        translate([device_origin.x - 3,
                   device_origin.y + left_volume_keepout_y.x,
                   front_plane - 8])
            cube([5, left_volume_keepout_y.y - left_volume_keepout_y.x, 8]);
        for (band = [right_power_keepout_y, right_reset_keepout_y,
                     right_tf1_keepout_y, right_tf2_keepout_y])
            translate([device_origin.x + device_body_size.x - 2,
                       device_origin.y + band.x, front_plane - 8])
                cube([5, band.y - band.x, 8]);
    }
}

module assembly() {
    carrier_plate();

    if (SHOW_DEVICE)
        %rg353v_device_preview();

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
} else if (PART == "lower_hook") {
    lower_hook_printable();
} else if (PART == "upper_hook") {
    upper_hook_printable();
} else if (PART == "hook_set") {
    hook_set();
} else if (PART == "fit_coupon") {
    fit_coupon();
} else {
    assert(false, str("Unknown PART: ", PART));
}
