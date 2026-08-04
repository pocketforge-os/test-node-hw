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
                          centre_bore = 4.2,
                          slot_pocket_width = 12.0,
                          slot_lip_depth = 1.6,
                          slot_deep_width = 6.4,
                          web_thickness = 1.2,
                          corner_radius = 0.8) {
    assert(profile_size > 0, "Extrusion profile must be positive");
    assert(slot_opening > 0 && slot_opening < profile_size,
           "Slot opening must fit inside the extrusion profile");
    assert(slot_depth > 0 && slot_depth < profile_size / 2,
           "Slot depth must fit inside the extrusion profile");
    assert(slot_pocket_width > slot_opening &&
           slot_pocket_width < profile_size,
           "Slot pocket must be wider than the mouth");
    assert(slot_lip_depth > 0 && slot_lip_depth < slot_depth,
           "Slot lip must fit inside the slot depth");
    assert(slot_deep_width > 0 &&
           slot_deep_width <= slot_pocket_width,
           "Deep slot width must fit inside the pocket");
    assert(web_thickness > 0 && web_thickness < slot_opening,
           "Profile web must fit inside the slot opening");
    assert(corner_radius >= 0 && corner_radius < profile_size / 2,
           "Corner radius must fit inside the profile");
    assert(detail == "envelope" || detail == "slot",
           "Extrusion detail must be envelope or slot");

    if (detail == "envelope") {
        square([profile_size, profile_size], center = true);
    } else {
        difference() {
            union() {
                difference() {
                    pf_rounded_rect_2d([profile_size, profile_size],
                                       corner_radius);

                    // End-on teaching profile.  Each face has a narrow slot
                    // mouth, retaining lips, and a wider internal pocket.
                    // Keeping those three widths visually distinct makes one
                    // extrusion read as a coherent V-slot rail instead of
                    // three stacked rectangular bars.
                    for (angle = [0 : 90 : 270])
                        rotate(angle)
                            polygon([
                                [-slot_opening / 2,
                                 profile_size / 2 + 0.02],
                                [-slot_opening / 2,
                                 profile_size / 2 - slot_lip_depth],
                                [-slot_pocket_width / 2,
                                 profile_size / 2 -
                                 min(slot_depth,
                                     slot_lip_depth + 1.25)],
                                [-slot_pocket_width / 2,
                                 profile_size / 2 -
                                 slot_depth + 0.9],
                                [-slot_deep_width / 2,
                                 profile_size / 2 - slot_depth],
                                [ slot_deep_width / 2,
                                 profile_size / 2 - slot_depth],
                                [ slot_pocket_width / 2,
                                 profile_size / 2 -
                                 slot_depth + 0.9],
                                [ slot_pocket_width / 2,
                                 profile_size / 2 -
                                 min(slot_depth,
                                     slot_lip_depth + 1.25)],
                                [ slot_opening / 2,
                                 profile_size / 2 - slot_lip_depth],
                                [ slot_opening / 2,
                                 profile_size / 2 + 0.02]
                            ]);
                }

                // A centre hub and diagonal webs make the end face read as
                // one extrusion.  They are presentation structure only; the
                // measured mouth, pocket, lip, and deep-channel dimensions
                // above remain the interface contract for printed parts.
                circle(d = centre_bore + 2 * web_thickness, $fn = 32);
                for (angle = [45 : 90 : 315])
                    rotate(angle)
                        translate([centre_bore / 2,
                                   -web_thickness / 2])
                            square([
                                profile_size / 2 -
                                centre_bore / 2 -
                                corner_radius,
                                web_thickness
                            ]);
            }
            circle(d = centre_bore, $fn = 32);
        }
    }
}

module pf_2020_extrusion(length,
                         axis = "z",
                         profile_size = 20,
                         detail = "slot",
                         slot_opening = 6.2,
                         slot_depth = 6.1,
                         centre_bore = 4.2,
                         slot_pocket_width = 12.0,
                         slot_lip_depth = 1.6,
                         slot_deep_width = 6.4,
                         web_thickness = 1.2,
                         corner_radius = 0.8) {
    assert(length > 0, "Extrusion length must be positive");
    assert(axis == "x" || axis == "y" || axis == "z",
           "Extrusion axis must be x, y, or z");

    module along_z() {
        linear_extrude(height = length, convexity = 8)
            pf_2020_profile_2d(profile_size, detail, slot_opening,
                               slot_depth, centre_bore,
                               slot_pocket_width, slot_lip_depth,
                               slot_deep_width, web_thickness,
                               corner_radius);
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
