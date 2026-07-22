/*
 * PocketForge reusable DUT cradle — TrimUI Smart Pro family profile
 *
 * Coordinates: X left-to-right, Y bottom-to-top, Z toward the webcam; mm.
 *
 * Examples:
 * Model wrappers set DEVICE_LABEL and include this family source:
 *   trimui-smart-pro-s-cradle.scad -> "TrimUI Smart Pro S"
 *   trimui-smart-pro-cradle.scad   -> "TrimUI Smart Pro"
 *
 * PART choices: assembly, plate, hook, hook_set, installed_hooks, fit_coupon.
 * The default assembly shows background-only DUT/hooks; even a manual STL
 * export of that view contains only the printable carrier plate.
 * `installed_hooks` is a presentation-only export in carrier coordinates. It
 * deliberately contains no plate or DUT geometry and is never a print group.
 */

include <lib/dut-cradle-library.scad>;

PART = "assembly";
SHOW_DEVICE = true;
SHOW_HOOKS = true;
SHOW_KEEP_OUTS = true;
SHOW_LABELS = true;

$fn = 48;
epsilon = 0.05;

// ---- Common carrier / printer datum --------------------------------------
printer_bed = [250, 210];
printer_edge_margin = 1.5;
printable_bed = printer_bed - [2 * printer_edge_margin,
                               2 * printer_edge_margin];
// Same physical envelope and eight 4040 anchors as the harness fixture, but
// landscape.  It fits the conservative 247 x 207 mm usable bed directly.
plate_size = [247, 200];
plate_thickness = 3.2;
plate_corner_radius = 4.0;

frame_tie_slot = [12.0, 5.5];
frame_tie_edge_inset = 8.0;
frame_tie_corner_offset = 19.0;
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

// ---- Smart Pro / Smart Pro S shared mechanical profile -------------------
// The family source remains directly renderable for development/linting, but
// production exports use one of the two tiny label-only wrappers.
device_name = is_undef(DEVICE_LABEL) ? "TrimUI Smart Pro S" : DEVICE_LABEL;
device_body_size = [188.35, 79.77];       // owner caliper measurement
// Preview proxy derived from the owner-fit 11.3 mm throat while preserving the
// original 0.6 mm passive clearance; the throat itself is authoritative.
device_body_depth = 10.7;
device_corner_radius = 35.0;             // preview outline; not a fit surface
device_origin = (plate_size - device_body_size) / 2;
device_centre = device_origin + device_body_size / 2;

// Keep camera registration independent of the shell datum.  The active area
// is provisional visualization only and can be corrected without moving the
// body or clamp interfaces.
screen_size = [110.8, 62.3];
optical_offset = [0, 0];

// The open/wired rear of the DUT must never touch the carrier.  Six perimeter
// shelves establish this gap and a large aperture leaves the centre accessible.
device_rear_gap = 11.0;                  // owner fit: +5 mm trigger clearance
rear_service_window = [158.0, 52.0];
rear_service_origin = device_centre - rear_service_window / 2;
rear_service_radius = 8.0;

/*
 * Interpreted owner safe-contact windows, measured inward from each end:
 *   top-left 35.41..50 mm; top-right 34..50 mm;
 *   both bottom windows 24..35 mm.
 * Clamp centres use each window midpoint.  These values stay explicit because
 * the nested dimension arrows in the paper sketch are the one remaining
 * measurement ambiguity.
 */
top_left_safe = [35.41, 50.0];
top_right_safe = [34.0, 50.0];
bottom_left_safe = [24.0, 35.0];
bottom_right_safe = [24.0, 35.0];

top_left_x = device_origin.x + (top_left_safe.x + top_left_safe.y) / 2;
top_right_x = device_origin.x + device_body_size.x -
              (top_right_safe.x + top_right_safe.y) / 2;
bottom_left_x = device_origin.x +
                (bottom_left_safe.x + bottom_left_safe.y) / 2;
bottom_right_x = device_origin.x + device_body_size.x -
                 (bottom_right_safe.x + bottom_right_safe.y) / 2;

// pose = [name, exact shell-edge contact point, inward angle, designed play]
// Local +X points into the DUT: bottom=+Y, top=-Y, left=+X, right=-X.
clamp_poses = [
    ["bottom_left", [bottom_left_x, device_origin.y], 90, 0.25],
    ["bottom_right", [bottom_right_x, device_origin.y], 90, 0.25],
    ["top_left", [top_left_x, device_origin.y + device_body_size.y], -90, 0.45],
    ["top_right", [top_right_x, device_origin.y + device_body_size.y], -90, 0.45],
    ["left_datum", [device_origin.x, device_centre.y], 0, 0.60],
    ["right_datum", [device_origin.x + device_body_size.x,
                     device_centre.y], 180, 0.60]
];

function pose_name(pose) = pose[0];
function pose_contact(pose) = pose[1];
function pose_angle(pose) = pose[2];
function pose_play(pose) = pose[3];
function pose_inward(pose) = pf_rotate_2d([1, 0], pose_angle(pose));
function pose_surface(pose) =
    pf_add_2d(pose_contact(pose),
              pf_scale_2d(-pose_play(pose), pose_inward(pose)));

// ---- Separately printed J-hook -------------------------------------------
hook_throat = 11.3;                      // owner-corrected internal capture gap
hook_width = 10.0;
hook_wall = 4.0;
hook_lip_depth = 2.8;
hook_lip_thickness = 4.0;
hook_support_depth = 4.0;
hook_support_thickness = 3.2;
hook_base_outward = 13.0;
hook_base_inward = 4.0;
hook_base_height = 4.4;
hook_base_radius = 1.5;

m3_clearance = 3.5;
m3_nut_across_flats = 5.6;               // second fit: another 0.1 mm per flat
m3_nut_depth = 2.8;
m3_nut_capture_wall = 2.4;               // three walls with a 0.8 mm nozzle
hook_screw_offset = [-8.0, -3.5];
hook_key_offset = [-8.0, 3.5];
hook_key_size = [4.0, 3.2];
hook_key_clearance = 0.35;
hook_keyway_depth = 1.2;
hook_adjustment = 8.0;

// ---- Raised labels, sized for the owner's 0.8 mm nozzle ------------------
// The generous stroke expansion and three-layer-at-0.4-mm emboss keep letter
// stems from disappearing when the slicer quantizes fine font geometry.
label_height = 1.2;
label_stroke_growth = 0.85;
title_box_size = [190, 24];
title_box_centre = [plate_size.x / 2, 176.5];
title_font_size = 14.4;
orientation_font_size = 9.0;

// ---- Design assertions ----------------------------------------------------
assert(plate_size.x <= printable_bed.x && plate_size.y <= printable_bed.y,
       "Carrier exceeds the conservative Prusa printable envelope");
assert(device_origin.x > hook_base_outward &&
       device_origin.y > hook_base_outward,
       "Insufficient plate margin outside DUT for clamps");
assert(device_rear_gap >= hook_base_height,
       "Rear shelf must sit above the clamp base");
assert(device_rear_gap >= 11.0,
       "Rear carrier gap must preserve the owner-validated trigger clearance");
assert(hook_throat > device_body_depth,
       "Hook throat must retain the DUT with positive clearance");
assert(m3_nut_capture_wall >= 2.4,
       "M3 nut capture wall must remain at least three 0.8 mm nozzle widths");
assert(hook_lip_depth <=
       min((device_body_size.x - screen_size.x) / 2,
           (device_body_size.y - screen_size.y) / 2),
       "Hook lip could cover the provisional active screen");
assert(rear_service_origin.x > device_origin.x &&
       rear_service_origin.y > device_origin.y &&
       rear_service_origin.x + rear_service_window.x <
           device_origin.x + device_body_size.x &&
       rear_service_origin.y + rear_service_window.y <
           device_origin.y + device_body_size.y,
       "Rear service aperture must remain inside the DUT footprint");
assert(top_left_x >= device_origin.x + top_left_safe.x &&
       top_left_x <= device_origin.x + top_left_safe.y,
       "Top-left clamp left its measured safe window");
assert(top_right_x >= device_origin.x + device_body_size.x - top_right_safe.y &&
       top_right_x <= device_origin.x + device_body_size.x - top_right_safe.x,
       "Top-right clamp left its measured safe window");
assert(bottom_left_x >= device_origin.x + bottom_left_safe.x &&
       bottom_left_x <= device_origin.x + bottom_left_safe.y,
       "Bottom-left clamp left its measured safe window");
assert(bottom_right_x >=
           device_origin.x + device_body_size.x - bottom_right_safe.y &&
       bottom_right_x <=
           device_origin.x + device_body_size.x - bottom_right_safe.x,
       "Bottom-right clamp left its measured safe window");

// ---- Carrier --------------------------------------------------------------
module label_box(centre, size, message, font_size) {
    translate([centre.x, centre.y, plate_thickness]) {
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
                         font = "Liberation Sans:style=Bold");
    }
}

module orientation_label(point, message, halign = "center") {
    translate([point.x, point.y, plate_thickness])
        linear_extrude(height = label_height)
            offset(delta = label_stroke_growth)
                text(message, size = orientation_font_size,
                     halign = halign, valign = "center",
                     font = "Liberation Sans:style=Bold");
}

module carrier_labels() {
    // label_box() is defined from its lower-left corner after translation.
    label_box(title_box_centre - title_box_size / 2,
              title_box_size, device_name, title_font_size);
    orientation_label([device_origin.x, 154.5], "TOP", "left");
    orientation_label([device_origin.x + device_body_size.x, 154.5],
                      "TOP", "right");
    orientation_label([device_origin.x, 38.0], "BOTTOM", "left");
    orientation_label([device_origin.x + device_body_size.x, 38.0],
                      "BOTTOM", "right");
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

            translate([rear_service_origin.x, rear_service_origin.y, -epsilon])
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

module one_hook_installed(pose, throat = hook_throat,
                          nut_af = m3_nut_across_flats) {
    pf_installed_j_hook(
        pose_surface(pose), pose_angle(pose), plate_thickness,
        throat, device_rear_gap, hook_width, hook_wall,
        hook_lip_depth, hook_lip_thickness, hook_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, nut_af, m3_nut_depth,
        m3_nut_capture_wall, hook_key_size, hook_keyway_depth, epsilon
    );
}

module one_hook_printable(throat = hook_throat,
                          nut_af = m3_nut_across_flats) {
    pf_print_oriented_j_hook(
        throat, device_rear_gap, hook_width, hook_wall,
        hook_lip_depth, hook_lip_thickness, hook_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, nut_af, m3_nut_depth,
        m3_nut_capture_wall, hook_key_size, hook_keyway_depth, epsilon
    );
}

module hook_set() {
    hook_pitch = [24, 34];
    for (column = [0 : 2])
        for (row = [0 : 1])
            translate([column * hook_pitch.x, row * hook_pitch.y, 0])
                one_hook_printable();
}

module mount_coupon_plate() {
    coupon_size = [30, 21];
    coupon_surface = [18, coupon_size.y / 2];
    difference() {
        pf_rounded_prism([coupon_size.x, coupon_size.y, plate_thickness], 2);
        pf_clamp_mount_cutouts(
            coupon_surface, 0, plate_thickness, hook_screw_offset,
            hook_key_offset, hook_adjustment, m3_clearance, hook_key_size,
            hook_key_clearance, hook_keyway_depth, epsilon
        );
    }
}

module fit_coupon() {
    // Left-to-right: 5.5, 5.6, and 5.7 mm nut-AF trials.  Hold the validated
    // 11.3 mm throat constant so the coupon changes only one fit variable.
    throat_trials = [hook_throat, hook_throat, hook_throat];
    nut_trials = [5.5, 5.6, 5.7];
    for (index = [0 : len(throat_trials) - 1])
        translate([index * 24, 0, 0])
            one_hook_printable(throat_trials[index], nut_trials[index]);
    translate([18, 34, 0]) mount_coupon_plate();
}

module safe_contact_window_preview() {
    preview_height = 0.8;
    preview_z = plate_thickness + device_rear_gap +
                device_body_depth + 0.7;
    color([0.15, 0.95, 0.35, 0.75]) {
        translate([device_origin.x + top_left_safe.x,
                   device_origin.y + device_body_size.y - 1, preview_z])
            cube([top_left_safe.y - top_left_safe.x, 2, preview_height]);
        translate([device_origin.x + device_body_size.x - top_right_safe.y,
                   device_origin.y + device_body_size.y - 1, preview_z])
            cube([top_right_safe.y - top_right_safe.x, 2, preview_height]);
        translate([device_origin.x + bottom_left_safe.x,
                   device_origin.y - 1, preview_z])
            cube([bottom_left_safe.y - bottom_left_safe.x, 2, preview_height]);
        translate([device_origin.x + device_body_size.x - bottom_right_safe.y,
                   device_origin.y - 1, preview_z])
            cube([bottom_right_safe.y - bottom_right_safe.x, 2,
                  preview_height]);
    }
}

// Presentation-only assembly geometry.  Keeping the six installed hooks in a
// dedicated export lets higher-level rack/chassis models show the accepted
// retention system without weakening assembly's preview-ghost export guard or
// accidentally creating one fused carrier-and-hooks production STL.
module installed_hooks() {
    for (pose = clamp_poses)
        one_hook_installed(pose);
}

module assembly() {
    carrier_plate();

    if (SHOW_DEVICE)
        %pf_device_preview(
            device_origin, device_body_size, device_body_depth,
            device_corner_radius, device_rear_gap, screen_size,
            optical_offset, plate_thickness
        );

    if (SHOW_KEEP_OUTS)
        %safe_contact_window_preview();

    if (SHOW_HOOKS)
        %installed_hooks();
}

if (PART == "assembly") {
    assembly();
} else if (PART == "plate") {
    carrier_plate();
} else if (PART == "hook") {
    one_hook_printable();
} else if (PART == "hook_set") {
    hook_set();
} else if (PART == "installed_hooks") {
    installed_hooks();
} else if (PART == "fit_coupon") {
    fit_coupon();
} else {
    assert(false, str("Unknown PART: ", PART));
}
