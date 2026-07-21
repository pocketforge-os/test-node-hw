/*
 * PocketForge reusable DUT-cradle geometry.
 *
 * Device dimensions, keep-outs, and clamp poses belong in a profile/wrapper
 * such as ../trimui-smart-pro-s-cradle.scad.  This file deliberately contains
 * no device-specific measurements.
 */

function pf_rotate_2d(point, angle) =
    [point.x * cos(angle) - point.y * sin(angle),
     point.x * sin(angle) + point.y * cos(angle)];

function pf_add_2d(a, b) = [a.x + b.x, a.y + b.y];
function pf_scale_2d(value, point) = [value * point.x, value * point.y];

module pf_rounded_rect_2d(size, radius) {
    offset(r = radius)
        offset(delta = -radius)
            square(size);
}

module pf_rounded_prism(size, radius) {
    linear_extrude(height = size.z)
        pf_rounded_rect_2d([size.x, size.y], radius);
}

module pf_pill_2d(length, width) {
    hull() {
        translate([-(length - width) / 2, 0]) circle(d = width);
        translate([ (length - width) / 2, 0]) circle(d = width);
    }
}

module pf_pill_hole(point, rotation, length, width, depth, z = -0.05) {
    translate([point.x, point.y, z])
        linear_extrude(height = depth)
            rotate(rotation)
                pf_pill_2d(length, width);
}

module pf_frame_tie_holes(features, slot, depth) {
    for (feature = features)
        pf_pill_hole(feature[1], feature[2], slot.x, slot.y, depth);
}

/*
 * One adjustable clamp interface comprises:
 *   - an M3 through-slot, along the local inward/outward axis; and
 *   - a shallow parallel keyway that prevents the hook rotating on one screw.
 *
 * surface is the nominal inner face of the hook stem.  angle rotates local +X
 * toward the DUT.  Offsets are expressed in the hook's local XY coordinates.
 */
module pf_clamp_mount_cutouts(
    surface,
    angle,
    plate_thickness,
    screw_offset,
    key_offset,
    adjustment,
    m3_clearance,
    key_size,
    key_clearance,
    keyway_depth,
    epsilon = 0.05
) {
    screw_point = pf_add_2d(surface, pf_rotate_2d(screw_offset, angle));
    key_point = pf_add_2d(surface, pf_rotate_2d(key_offset, angle));

    pf_pill_hole(
        screw_point,
        angle,
        adjustment + m3_clearance,
        m3_clearance,
        plate_thickness + 2 * epsilon,
        -epsilon
    );

    keyway_size = [adjustment + key_size.x + key_clearance,
                   key_size.y + key_clearance];
    translate([key_point.x, key_point.y,
               plate_thickness - keyway_depth - epsilon])
        linear_extrude(height = keyway_depth + 2 * epsilon)
            rotate(angle)
                translate(-keyway_size / 2)
                    pf_rounded_rect_2d(
                        keyway_size, min(key_size.y / 3, 0.8)
                    );
}

/*
 * A passive edge-capture hook.  Tightening the M3 screw locks the hook to the
 * carrier; it must not be used to squeeze the DUT.  The device rests on the
 * rear shelf at z=rear_gap and is retained by a short front lip at
 * z=rear_gap+throat.
 *
 * Installed coordinate system:
 *   +X points inward into the DUT, +Y follows its edge, +Z faces the webcam.
 *   The device edge begins just inward of X=0.  The screw and anti-rotation key
 *   sit outward at negative X, safely away from the shell.
 */
module pf_j_hook_installed(
    throat,
    rear_gap,
    width,
    wall,
    lip_depth,
    lip_thickness,
    support_depth,
    support_thickness,
    base_outward,
    base_inward,
    base_height,
    base_radius,
    screw_offset,
    key_offset,
    m3_clearance,
    nut_across_flats,
    nut_depth,
    nut_capture_wall,
    key_size,
    keyway_depth,
    epsilon = 0.05,
    spine_width = undef
) {
    total_height = rear_gap + throat + lip_thickness;
    nut_circumradius = nut_across_flats / (2 * cos(30));
    nut_capture_radius = nut_circumradius + nut_capture_wall;
    body_width = is_undef(spine_width) ? width : spine_width;

    assert(nut_capture_wall > 0,
           "Nut capture wall must be positive");

    difference() {
        union() {
            translate([-base_outward, -body_width / 2, 0])
                linear_extrude(height = base_height)
                    pf_rounded_rect_2d(
                        [base_outward + base_inward, body_width], base_radius
                    );

            // The screw is deliberately offset from the anti-rotation key.
            // Give its top-loading nut a complete local perimeter rather than
            // allowing the hex pocket to break through the narrow hook base.
            translate([screw_offset.x, screw_offset.y, 0])
                cylinder(r = nut_capture_radius, h = base_height, $fn = 48);

            // Continuous stem; the generous section is intentional for a
            // 0.8 mm nozzle and survives repeated device servicing.
            translate([-wall, -body_width / 2, 0])
                cube([wall, body_width, total_height]);

            // Rear shelf.  A sloped underside avoids an abrupt stress riser.
            translate([0, -width / 2, rear_gap - support_thickness])
                cube([support_depth, width, support_thickness]);
            hull() {
                translate([-wall, -width / 2,
                           rear_gap - support_thickness - 1.5])
                    cube([0.8, width, 1.5]);
                translate([support_depth - 0.8, -width / 2,
                           rear_gap - support_thickness])
                    cube([0.8, width, 0.8]);
            }

            // Short front lip: enough to capture the edge without covering
            // the display or controls.  A top gusset strengthens the root.
            translate([0, -width / 2, rear_gap + throat])
                cube([lip_depth, width, lip_thickness]);
            hull() {
                translate([-wall, -width / 2,
                           rear_gap + throat + lip_thickness - 1.0])
                    cube([0.8, width, 1.0]);
                translate([lip_depth - 0.8, -width / 2,
                           rear_gap + throat + lip_thickness - 0.8])
                    cube([0.8, width, 0.8]);
            }

            // Rectangular key rides in the carrier's shallow keyway.
            translate([key_offset.x - key_size.x / 2,
                       key_offset.y - key_size.y / 2,
                       -keyway_depth])
                cube([key_size.x, key_size.y, keyway_depth + epsilon]);
        }

        // Rear-access screw rises through the carrier into a top-loading M3
        // nut.  Any excess screw length remains outside the device perimeter.
        translate([screw_offset.x, screw_offset.y, -keyway_depth - epsilon])
            cylinder(d = m3_clearance,
                     h = base_height + keyway_depth + 2 * epsilon);
        translate([screw_offset.x, screw_offset.y,
                   base_height - nut_depth])
            cylinder(d = nut_across_flats / cos(30),
                     h = nut_depth + epsilon, $fn = 6);
    }
}

module pf_installed_j_hook(
    surface,
    angle,
    plate_thickness,
    throat,
    rear_gap,
    width,
    wall,
    lip_depth,
    lip_thickness,
    support_depth,
    support_thickness,
    base_outward,
    base_inward,
    base_height,
    base_radius,
    screw_offset,
    key_offset,
    m3_clearance,
    nut_across_flats,
    nut_depth,
    nut_capture_wall,
    key_size,
    keyway_depth,
    epsilon = 0.05,
    spine_width = undef
) {
    translate([surface.x, surface.y, plate_thickness])
        rotate([0, 0, angle])
            pf_j_hook_installed(
                throat, rear_gap, width, wall, lip_depth, lip_thickness,
                support_depth, support_thickness, base_outward, base_inward,
                base_height, base_radius, screw_offset, key_offset,
                m3_clearance, nut_across_flats, nut_depth, nut_capture_wall,
                key_size, keyway_depth, epsilon, spine_width
            );
}

/* Rotate a hook onto its broad side so layer lines run through the J profile. */
module pf_print_oriented_j_hook(
    throat,
    rear_gap,
    width,
    wall,
    lip_depth,
    lip_thickness,
    support_depth,
    support_thickness,
    base_outward,
    base_inward,
    base_height,
    base_radius,
    screw_offset,
    key_offset,
    m3_clearance,
    nut_across_flats,
    nut_depth,
    nut_capture_wall,
    key_size,
    keyway_depth,
    epsilon = 0.05,
    spine_width = undef
) {
    total_height = rear_gap + throat + lip_thickness;
    nut_circumradius = nut_across_flats / (2 * cos(30));
    nut_capture_radius = nut_circumradius + nut_capture_wall;
    body_width = is_undef(spine_width) ? width : spine_width;
    print_x_offset = max(base_outward,
                         -screw_offset.x + nut_capture_radius);
    print_z_offset = max(body_width / 2,
                         key_offset.y + key_size.y / 2,
                         screw_offset.y + nut_capture_radius);
    // Rest the unmodified broad face on the bed.  The asymmetric nut boss then
    // grows upward instead of becoming a low point that would require support.
    translate([print_x_offset, keyway_depth, print_z_offset])
        rotate([-90, 0, 0])
            pf_j_hook_installed(
                throat, rear_gap, width, wall, lip_depth, lip_thickness,
                support_depth, support_thickness, base_outward, base_inward,
                base_height, base_radius, screw_offset, key_offset,
                m3_clearance, nut_across_flats, nut_depth, nut_capture_wall,
                key_size, keyway_depth, epsilon, spine_width
            );
}

module pf_device_preview(
    origin,
    body_size,
    body_depth,
    body_radius,
    rear_gap,
    screen_size,
    optical_offset,
    plate_thickness
) {
    color([0.12, 0.14, 0.16, 0.60])
        translate([origin.x, origin.y, plate_thickness + rear_gap])
            pf_rounded_prism(
                [body_size.x, body_size.y, body_depth], body_radius
            );

    screen_origin = [
        origin.x + (body_size.x - screen_size.x) / 2 + optical_offset.x,
        origin.y + (body_size.y - screen_size.y) / 2 + optical_offset.y
    ];
    color([0.10, 0.55, 0.88, 0.75])
        translate([screen_origin.x, screen_origin.y,
                   plate_thickness + rear_gap + body_depth + 0.05])
            cube([screen_size.x, screen_size.y, 0.35]);
}
