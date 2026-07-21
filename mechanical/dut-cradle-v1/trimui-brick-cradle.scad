/*
 * PocketForge reusable DUT cradle — TrimUI Brick profile
 *
 * Coordinates: X left-to-right, Y bottom-to-top, Z toward the webcam; mm.
 * The Brick has a stepped rear shell.  Per-hook rear shelves compensate for
 * that step so the front glass remains parallel to the carrier and camera.
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

// The extra right/left margin reserves a collision-free vertical label lane
// while the portrait plate remains materially smaller than the Smart Pro one.
plate_size = [148, 180];
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

// ---- Owner-measured Brick mechanical profile -----------------------------
device_name = "TrimUI Brick";
device_body_size = [72.8, 110.75];
device_bottom_corner_radius = 8.5;
device_origin = (plate_size - device_body_size) / 2;
device_centre = device_origin + device_body_size / 2;

// The lower 20 mm of the shell is 20 mm deep; the upper shell is 12 mm deep.
// Supporting the two regions 8 mm apart holds their shared front face flat.
lower_region_height = 20.0;
lower_body_depth = 20.0;
upper_body_depth = 12.0;
minimum_rear_clearance = 8.0;
lower_rear_gap = 10.0;
upper_rear_gap = lower_rear_gap + lower_body_depth - upper_body_depth;

// 3.2-inch 4:3 panel geometry.  Only the top margin is a hook safety datum;
// the rest is a preview until a direct glass measurement is needed.
screen_size = [65.02, 48.77];
screen_top_margin = 1.8;
screen_origin = [
    device_origin.x + (device_body_size.x - screen_size.x) / 2,
    device_origin.y + device_body_size.y - screen_top_margin - screen_size.y
];

// Large open back for trigger testing, airflow, wiring, and a finger behind
// the DUT.  The remaining perimeter carries all five clamp interfaces.
rear_service_window = [56.0, 86.0];
rear_service_origin = device_centre - rear_service_window / 2;
rear_service_radius = 7.0;

// ---- Five passive contacts -----------------------------------------------
// Four lower contacts share one physically proven hook geometry.  Bottom
// hooks carry weight; side hooks are loose datums.  The narrow upper hook is
// offset left of the centred USB-host path and only prevents escape.
bottom_contact_inset = 18.0;
// Keep the complete 9 mm side-contact band above the 8.5 mm lower corner arc.
lower_side_contact_height = 14.0;
upper_contact_inset = 17.0;

lower_throat = lower_body_depth + 0.6;
upper_throat = upper_body_depth + 0.6;

// pose = [name, exact shell-edge contact point, inward angle, play, kind]
clamp_poses = [
    ["bottom_left",
     [device_origin.x + bottom_contact_inset, device_origin.y],
     90, 0.25, "lower"],
    ["bottom_right",
     [device_origin.x + device_body_size.x - bottom_contact_inset,
      device_origin.y],
     90, 0.25, "lower"],
    ["left_lower_datum",
     [device_origin.x, device_origin.y + lower_side_contact_height],
     0, 0.60, "lower"],
    ["right_lower_datum",
     [device_origin.x + device_body_size.x,
      device_origin.y + lower_side_contact_height],
     180, 0.60, "lower"],
    ["upper_retainer",
     [device_origin.x + upper_contact_inset,
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
lower_hook_width = 9.0;
upper_hook_width = 6.0;
hook_wall = 4.0;
lower_lip_depth = 3.0;
upper_lip_depth = 1.2;
hook_lip_thickness = 4.0;
lower_support_depth = 4.0;
upper_support_depth = 3.0;
hook_support_thickness = 3.2;
hook_base_outward = 13.0;
hook_base_inward = 4.0;
hook_base_height = 4.4;
hook_base_radius = 1.5;

m3_clearance = 3.5;
m3_nut_across_flats = 5.6;               // Smart Pro owner-validated press fit
m3_nut_depth = 2.8;
m3_nut_capture_wall = 2.4;
hook_screw_offset = [-8.0, -3.5];
hook_key_offset = [-8.0, 3.5];
hook_key_size = [4.0, 3.2];
hook_key_clearance = 0.35;
hook_keyway_depth = 1.2;
hook_adjustment = 8.0;

// ---- Labels for the 0.8 mm nozzle ----------------------------------------
label_height = 1.2;
label_stroke_growth = 1.10;
title_font_size = 13.0;
orientation_font_size = 10.5;
label_feature_clearance = 2.4;  // three 0.8 mm nozzle widths

title_label_center = [plate_size.x - 13.0, plate_size.y / 2];
title_label_half_length = 50.0; // conservative lane for "TrimUI Brick"
top_label_center = [plate_size.x / 2 + 12.0, plate_size.y - 18.0];
bottom_label_center = [plate_size.x / 2, 11.5];

// ---- Explicit mechanical invariants --------------------------------------
lower_front_datum = lower_rear_gap + lower_throat;
upper_front_datum = upper_rear_gap + upper_throat;
top_usb_keepout = [
    device_origin.x + device_body_size.x / 2 - 8.0,
    device_origin.x + device_body_size.x / 2 + 8.0
];
upper_contact_window = [
    device_origin.x + upper_contact_inset - upper_hook_width / 2,
    device_origin.x + upper_contact_inset + upper_hook_width / 2
];
right_side_surface = pose_surface(clamp_poses[3]);
right_side_screw_point = pf_add_2d(
    right_side_surface,
    pf_rotate_2d(hook_screw_offset, pose_angle(clamp_poses[3]))
);
right_side_mount_outer_x = max(
    right_side_surface.x + hook_base_outward,
    right_side_screw_point.x + (hook_adjustment + m3_clearance) / 2
);
title_label_inner_x = title_label_center.x -
                      title_font_size / 2 - label_stroke_growth;
bottom_label_outer_y = bottom_label_center.y +
                       orientation_font_size / 2 + label_stroke_growth;
bottom_left_surface = pose_surface(clamp_poses[0]);
bottom_left_screw_point = pf_add_2d(
    bottom_left_surface,
    pf_rotate_2d(hook_screw_offset, pose_angle(clamp_poses[0]))
);
bottom_mount_inner_y = bottom_left_screw_point.y -
                       (hook_adjustment + m3_clearance) / 2;

assert(plate_size.x <= printable_bed.x && plate_size.y <= printable_bed.y,
       "Brick carrier exceeds the conservative Prusa printable envelope");
assert(lower_rear_gap >= minimum_rear_clearance,
       "Brick lower rear gap must preserve finger access");
assert(upper_rear_gap >= minimum_rear_clearance,
       "Brick upper rear gap must preserve trigger access");
assert(abs(lower_front_datum - upper_front_datum) < 0.01,
       "Brick front contact plane must remain flat across shell step");
assert(lower_throat > lower_body_depth && upper_throat > upper_body_depth,
       "Brick hook throats must retain positive passive clearance");
assert(upper_lip_depth < screen_top_margin,
       "Brick upper lip could cover active screen pixels");
assert(upper_contact_window.y < top_usb_keepout.x,
       "Brick upper retainer entered the centred USB-host keep-out");
assert(title_label_inner_x >= right_side_mount_outer_x +
           label_feature_clearance,
       "Brick side title entered the right hook mount or adjustment sweep");
assert(title_label_center.y - title_label_half_length >=
           frame_tie_corner_offset + frame_tie_slot.x / 2 +
           label_feature_clearance &&
       title_label_center.y + title_label_half_length <=
           plate_size.y - frame_tie_corner_offset -
           frame_tie_slot.x / 2 - label_feature_clearance,
       "Brick side title entered a right-side 4040 frame slot lane");
assert(bottom_label_outer_y + label_feature_clearance <=
           bottom_mount_inner_y,
       "Brick BOTTOM label entered a lower hook adjustment sweep");
assert(lower_side_contact_height - lower_hook_width / 2 >
           device_bottom_corner_radius &&
       lower_side_contact_height + lower_hook_width / 2 <
           lower_region_height,
       "The complete Brick side-contact band must land on the straight thick shell");
assert(m3_nut_capture_wall >= 2.4,
       "Brick M3 nut capture wall must remain at least three nozzle widths");
assert(rear_service_origin.x > device_origin.x &&
       rear_service_origin.y > device_origin.y &&
       rear_service_origin.x + rear_service_window.x <
           device_origin.x + device_body_size.x &&
       rear_service_origin.y + rear_service_window.y <
           device_origin.y + device_body_size.y,
       "Brick service aperture must remain inside the DUT footprint");

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

module carrier_labels() {
    embossed_text(title_label_center, device_name,
                  title_font_size, 90);
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
        hook_keyway_depth, epsilon
    );
}

module lower_hook_printable(throat = lower_throat) {
    pf_print_oriented_j_hook(
        throat, lower_rear_gap, lower_hook_width, hook_wall,
        lower_lip_depth, hook_lip_thickness, lower_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, m3_nut_across_flats,
        m3_nut_depth, m3_nut_capture_wall, hook_key_size,
        hook_keyway_depth, epsilon
    );
}

module upper_hook_printable(throat = upper_throat) {
    pf_print_oriented_j_hook(
        throat, upper_rear_gap, upper_hook_width, hook_wall,
        upper_lip_depth, hook_lip_thickness, upper_support_depth,
        hook_support_thickness, hook_base_outward, hook_base_inward,
        hook_base_height, hook_base_radius, hook_screw_offset,
        hook_key_offset, m3_clearance, m3_nut_across_flats,
        m3_nut_depth, m3_nut_capture_wall, hook_key_size,
        hook_keyway_depth, epsilon
    );
}

module hook_set() {
    for (column = [0 : 1])
        for (row = [0 : 1])
            translate([column * 23, row * 40, 0])
                lower_hook_printable();
    translate([46, 0, 0]) upper_hook_printable();
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
    lower_hook_printable();
    translate([24, 0, 0]) upper_hook_printable();
    translate([10, 42, 0]) mount_coupon_plate();
}

// ---- Preview-only device / keep-outs -------------------------------------
module brick_outline_2d() {
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

module brick_device_preview() {
    front_plane = plate_thickness + lower_front_datum - 0.6;

    color([0.12, 0.14, 0.16, 0.62]) {
        translate([device_origin.x, device_origin.y,
                   plate_thickness + lower_rear_gap])
            intersection() {
                linear_extrude(height = lower_body_depth)
                    brick_outline_2d();
                cube([device_body_size.x, lower_region_height,
                      lower_body_depth]);
            }

        translate([device_origin.x, device_origin.y,
                   plate_thickness + upper_rear_gap])
            intersection() {
                linear_extrude(height = upper_body_depth)
                    brick_outline_2d();
                translate([0, lower_region_height, 0])
                    cube([device_body_size.x,
                          device_body_size.y - lower_region_height,
                          upper_body_depth]);
            }
    }

    color([0.10, 0.55, 0.88, 0.78])
        translate([screen_origin.x, screen_origin.y, front_plane + 0.05])
            cube([screen_size.x, screen_size.y, 0.35]);
}

module keep_out_preview() {
    front_plane = plate_thickness + lower_front_datum;

    // Active-screen top edge and the selected narrow contact window.
    color([0.15, 0.95, 0.35, 0.80])
        translate([upper_contact_window.x,
                   device_origin.y + device_body_size.y - 1,
                   front_plane + 0.5])
            cube([upper_contact_window.y - upper_contact_window.x,
                  2, 0.8]);

    // Centred top USB-host cable path; all orange/red volumes are keep-outs.
    color([1.0, 0.50, 0.08, 0.68])
        translate([top_usb_keepout.x,
                   device_origin.y + device_body_size.y - 2,
                   plate_thickness + upper_rear_gap + 2])
            cube([top_usb_keepout.y - top_usb_keepout.x, 9,
                  upper_body_depth - 4]);

    // Rear shoulder triggers project toward the carrier in the thin region.
    color([0.95, 0.12, 0.20, 0.70])
        for (trigger_x = [device_origin.x + 11,
                          device_origin.x + device_body_size.x - 24])
            translate([trigger_x,
                       device_origin.y + device_body_size.y - 18,
                       plate_thickness + upper_rear_gap - 4])
                cube([13, 12, 4]);

    // Side controls and bottom connector group remain unobstructed.
    color([1.0, 0.50, 0.08, 0.68]) {
        translate([device_origin.x - 2, device_origin.y + 77,
                   front_plane - 8])
            cube([4, 18, 8]);
        translate([device_origin.x + device_body_size.x - 2,
                   device_origin.y + 77, front_plane - 8])
            cube([4, 18, 8]);
        translate([device_centre.x - 21, device_origin.y - 6,
                   plate_thickness + lower_rear_gap + 3])
            cube([42, 8, 11]);
    }
}

module assembly() {
    carrier_plate();

    if (SHOW_DEVICE)
        %brick_device_preview();

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
