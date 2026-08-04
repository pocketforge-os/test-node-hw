/*
 * Parametric 90-degree checker for extrusion-frame assembly.
 *
 * Print flat, label side up. The long inside and outside faces are the
 * reference surfaces; the two corner reliefs keep burrs and debris out of
 * the virtual 90-degree intersections.
 *
 * SPDX-License-Identifier: MIT
 */

// [Main dimensions]

// Overall length of both equal legs.
leg_length = 150; // [80:5:195]

// Width of each arm. The 25 mm default fully spans a 20 mm extrusion face.
arm_width = 25; // [16:1:45]

// Flat printed thickness.
thickness = 5; // [3:0.5:8]

// [Corner reliefs]

// Radius removed at the concave corner so burrs cannot create a false gap.
inside_corner_relief_radius = 4; // [1:0.5:10]

// 45-degree chamfer at the convex corner for checking an inside corner.
outside_corner_chamfer = 2; // [0:0.5:8]

// [Label]

// Recess a label into the top face. It is clipped away from every reference edge.
show_label = true;

// Leave empty to derive the label from leg_length.
label_text = "";

label_size = 7; // [4:0.5:12]
label_depth = 0.6; // [0.4:0.1:1]
label_margin = 3; // [2:0.5:6]

// [Printer envelope]

// Conservative printable X/Y envelope used by the chassis project.
print_bed = [247, 207];
bed_margin = 5; // [0:1:15]

/* [Hidden] */

epsilon = 0.02;
relief_facets = 96;
usable_inside_reference_length =
    leg_length - arm_width - inside_corner_relief_radius;
usable_outside_reference_length =
    leg_length - outside_corner_chamfer;
effective_label_text =
    label_text == ""
        ? str("90 DEG / ", leg_length, " MM")
        : label_text;
label_safe_start =
    arm_width + inside_corner_relief_radius + label_margin;
label_safe_end = leg_length - label_margin;
label_center = (label_safe_start + label_safe_end) / 2;

assert(leg_length >= 80,
       "leg_length must be at least 80 mm");
assert(arm_width >= 16,
       "arm_width must be at least 16 mm");
assert(arm_width <= leg_length / 3,
       "arm_width must not exceed one third of leg_length");
assert(thickness >= 3,
       "thickness must be at least 3 mm");
assert(inside_corner_relief_radius >= 1
       && inside_corner_relief_radius <= arm_width / 3,
       "inside_corner_relief_radius must be between 1 mm and one third of arm_width");
assert(outside_corner_chamfer >= 0
       && outside_corner_chamfer <= arm_width / 3,
       "outside_corner_chamfer must be between zero and one third of arm_width");
assert(usable_inside_reference_length >= 60,
       "inside reference faces must remain at least 60 mm long");
assert(usable_outside_reference_length >= 60,
       "outside reference faces must remain at least 60 mm long");
assert(len(print_bed) == 2
       && print_bed[0] > 0
       && print_bed[1] > 0,
       "print_bed must contain two positive dimensions");
assert(bed_margin >= 0,
       "bed_margin must not be negative");
assert(leg_length <= min(print_bed) - 2 * bed_margin,
       "leg_length must fit the square footprint inside print_bed and bed_margin");
assert(!show_label || label_depth >= 0.4,
       "label_depth must be at least 0.4 mm when the label is enabled");
assert(!show_label || label_depth <= thickness / 3,
       "label_depth must not exceed one third of thickness");
assert(!show_label || label_size + 2 * label_margin <= arm_width,
       "label_size and margins must fit inside arm_width");
assert(!show_label || label_safe_end - label_safe_start >= 3 * label_size,
       "label needs a safe span separated from the inside relief and leg tip");

module checker_profile_2d() {
    difference() {
        union() {
            square([leg_length, arm_width]);
            square([arm_width, leg_length]);
        }

        // The circle opens into the missing quadrant, making a debris-relief
        // notch rather than a closed hole.
        translate([arm_width, arm_width])
            circle(r = inside_corner_relief_radius,
                   $fn = relief_facets);

        if (outside_corner_chamfer > 0)
            polygon([
                [-epsilon, -epsilon],
                [outside_corner_chamfer + epsilon, -epsilon],
                [-epsilon, outside_corner_chamfer + epsilon]
            ]);
    }
}

module safe_label_2d() {
    intersection() {
        translate([label_center, arm_width / 2])
            text(effective_label_text,
                 size = label_size,
                 halign = "center",
                 valign = "center");

        translate([label_safe_start, label_margin])
            square([
                label_safe_end - label_safe_start,
                arm_width - 2 * label_margin
            ]);
    }
}

module right_angle_checker() {
    difference() {
        linear_extrude(height = thickness, convexity = 10)
            checker_profile_2d();

        if (show_label)
            translate([0, 0, thickness - label_depth])
                linear_extrude(height = label_depth + epsilon,
                               convexity = 10)
                    safe_label_2d();
    }
}

color([0.95, 0.42, 0.08])
    right_angle_checker();
