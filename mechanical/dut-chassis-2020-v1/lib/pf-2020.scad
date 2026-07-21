/*
 * PocketForge generic 20 mm T-slot extrusion preview library.
 *
 * This is deliberately an interface model, not a vendor-specific structural
 * section.  "envelope" is the authoritative collision volume.  "slot" adds
 * the measured slot opening/depth and centre bore for useful assembly views.
 * Printed interfaces must be calibrated with the fit coupon because products
 * sold as "2020" do not share one universal slot geometry.
 */

module pf_rounded_rect_2d(size, radius) {
    assert(size.x > 2 * radius && size.y > 2 * radius,
           "Rounded rectangle radius exceeds its envelope");
    offset(r = radius)
        square(size - [2 * radius, 2 * radius], center = true);
}

module pf_capsule_2d(length, width) {
    assert(length >= width, "Capsule length must be at least its width");
    hull() {
        translate([-(length - width) / 2, 0]) circle(d = width, $fn = 32);
        translate([ (length - width) / 2, 0]) circle(d = width, $fn = 32);
    }
}

module pf_2020_profile_2d(profile_size = 20,
                          detail = "slot",
                          slot_opening = 6.2,
                          slot_depth = 6.1,
                          centre_bore = 4.2) {
    assert(profile_size > 0, "Extrusion profile must be positive");
    assert(slot_opening > 0 && slot_opening < profile_size,
           "Slot opening must fit inside the extrusion profile");
    assert(slot_depth > 0 && slot_depth < profile_size / 2,
           "Slot depth must fit inside the extrusion profile");
    assert(detail == "envelope" || detail == "slot",
           "Extrusion detail must be envelope or slot");

    if (detail == "envelope") {
        square([profile_size, profile_size], center = true);
    } else {
        difference() {
            square([profile_size, profile_size], center = true);
            circle(d = centre_bore, $fn = 32);

            // Conservative straight channels: enough detail to expose face
            // orientation and slot access without claiming a vendor section.
            for (angle = [0 : 90 : 270])
                rotate(angle)
                    translate([-slot_opening / 2,
                               profile_size / 2 - slot_depth])
                        square([slot_opening, slot_depth + 0.02]);
        }
    }
}

module pf_2020_extrusion(length,
                         axis = "z",
                         profile_size = 20,
                         detail = "slot",
                         slot_opening = 6.2,
                         slot_depth = 6.1,
                         centre_bore = 4.2) {
    assert(length > 0, "Extrusion length must be positive");
    assert(axis == "x" || axis == "y" || axis == "z",
           "Extrusion axis must be x, y, or z");

    module along_z() {
        linear_extrude(height = length, convexity = 8)
            pf_2020_profile_2d(profile_size, detail, slot_opening,
                               slot_depth, centre_bore);
    }

    if (axis == "x")
        rotate([0, 90, 0]) along_z();
    else if (axis == "y")
        rotate([-90, 0, 0]) along_z();
    else
        along_z();
}

module pf_m3_washer_proxy(outer_diameter = 9,
                          thickness = 0.8,
                          clearance = 3.6) {
    difference() {
        cylinder(d = outer_diameter, h = thickness, $fn = 40);
        translate([0, 0, -0.01])
            cylinder(d = clearance, h = thickness + 0.02, $fn = 28);
    }
}
