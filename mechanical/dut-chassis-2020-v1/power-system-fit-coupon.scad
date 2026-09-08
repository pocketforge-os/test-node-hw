/*
 * Disposable, support-free ALT-1205T / IEC C14 / M3 process fit coupon.
 *
 * FIT COUPON ONLY -- NEVER A MAINS ENCLOSURE OR POWERED-WIRE GUARD.
 * PSU coordinates retain the component library's underside top-left datum.
 */

include <lib/alt-1205t-power-supply.scad>
include <lib/iec-c14-fused-switch.scad>

IEC_CLEARANCE = is_undef(IEC_CLEARANCE) ? 0.20 : IEC_CLEARANCE; // per side
M3_HOLE_CLEARANCE = is_undef(M3_HOLE_CLEARANCE) ? 0.40 : M3_HOLE_CLEARANCE; // on diameter
NUT_TRAP_CLEARANCE = is_undef(NUT_TRAP_CLEARANCE) ? 0.25 : NUT_TRAP_CLEARANCE; // across flats
WALL_THICKNESS = is_undef(WALL_THICKNESS) ? 3.0 : WALL_THICKNESS;
LABEL_DEPTH = is_undef(LABEL_DEPTH) ? 0.35 : LABEL_DEPTH;
EVIDENCE = is_undef(EVIDENCE) ? false : EVIDENCE;

function coupon_m3_nominal_diameter() = 3.0;
function coupon_m3_hole_diameter() = coupon_m3_nominal_diameter() + M3_HOLE_CLEARANCE;
function coupon_nut_nominal_af() = 5.5;
function coupon_nut_nominal_thickness() = 2.4;
function coupon_nut_pocket_af() = coupon_nut_nominal_af() + NUT_TRAP_CLEARANCE;
function coupon_nut_pocket_depth() = coupon_nut_nominal_thickness() + 0.20;
function coupon_iec_nominal_profile() = iecc14_body_profile_size();
function coupon_iec_clearanced_profile() = [
    coupon_iec_nominal_profile().x + 2 * IEC_CLEARANCE,
    coupon_iec_nominal_profile().y + 2 * IEC_CLEARANCE
];
function coupon_slot_origin() = [
    alt1205t_base_size().x - alt1205t_upper_right_slot_right_tangent()
        - alt1205t_upper_right_slot_size().x,
    alt1205t_upper_right_slot_top_tangent()
];
function coupon_iec_centre() = [-19, 80];
function coupon_panel_size() = [35, 54];
function coupon_nut_centre() = [85, 8];
function coupon_rib_width() = 7;
function coupon_pad_diameter() = 11;
function coupon_register_height() = 2.0;
function coupon_register_thickness() = 2.0;
function coupon_register_length() = 24;

module coupon_contract() {
    assert(alt1205t_base_size() == [77.5, 110], "PSU absolute datum outline changed");
    assert(alt1205t_m3_centres() == [[23.8,29.9], [23.8,66], [51.8,66]],
           "PSU coupon centres changed");
    assert(coupon_slot_origin() == [71.05, 2.94] &&
           coupon_slot_origin().x + alt1205t_upper_right_slot_size().x ==
               alt1205t_base_size().x - 3.15,
           "PSU slot tangent contract changed");
    assert(coupon_iec_nominal_profile() == [27,41] &&
           coupon_iec_clearanced_profile() ==
               [27 + 2*IEC_CLEARANCE, 41 + 2*IEC_CLEARANCE],
           "IEC nominal and clearanced profiles must remain distinct");
    assert(WALL_THICKNESS > 0, "Coupon wall thickness must be positive");
    assert(IEC_CLEARANCE >= 0 && M3_HOLE_CLEARANCE >= 0 && NUT_TRAP_CLEARANCE >= 0,
           "Print clearances cannot be negative");
    assert(LABEL_DEPTH > 0 && LABEL_DEPTH < WALL_THICKNESS,
           "Label depth must remain within the coupon wall");
    assert(coupon_m3_hole_diameter() == 3 + M3_HOLE_CLEARANCE,
           "M3 clearance must apply to the nominal diameter");
    assert(coupon_nut_nominal_af() == 5.5 && coupon_nut_nominal_thickness() == 2.4 &&
           coupon_nut_pocket_af() == 5.5 + NUT_TRAP_CLEARANCE &&
           coupon_nut_pocket_depth() == 2.6,
           "M3 nut-trap nominal or clearance mapping changed");
    assert(coupon_nut_pocket_depth() < WALL_THICKNESS,
           "Nut pocket must retain a printable floor");
    children();
}

module rib_between(a, b, width = coupon_rib_width()) {
    hull() for (p = [a,b]) translate(p) circle(d=width, $fn=24);
}

module psu_sparse_outline_2d() {
    centres = alt1205t_m3_centres();
    slot_centre = coupon_slot_origin() + alt1205t_upper_right_slot_size()/2;
    union() {
        // Exact top/left outline references make the absolute datum physical.
        translate([-2, -2]) square([alt1205t_base_size().x + 4, 6]);
        translate([-2, -2]) square([6, alt1205t_base_size().y + 4]);
        // Datum marker remains positive even though the library's corner aperture
        // is part of the mounting-negative call below.
        translate([-5, -5]) square([8, 8]);
        for (p = centres) translate(p) circle(d=coupon_pad_diameter(), $fn=36);
        rib_between([2,2], centres[0]);
        rib_between(centres[0], centres[1]);
        rib_between(centres[1], centres[2]);
        rib_between([2,2], slot_centre);
        translate(slot_centre) circle(d=9, $fn=30);
    }
}

module iec_panel_2d() {
    translate(coupon_iec_centre()) square(coupon_panel_size(), center=true);
}

module nut_sampler_2d() {
    translate(coupon_nut_centre()) circle(d=13, $fn=36);
    rib_between([alt1205t_base_size().x - 2, 2], coupon_nut_centre(), 6);
}

module coupon_blank() {
    union() {
        linear_extrude(height=WALL_THICKNESS)
            union() { psu_sparse_outline_2d(); iec_panel_2d(); nut_sampler_2d(); }
        // The PSU sits on the Z=WALL_THICKNESS face and is pushed up/left.
        // These outside-only legs expose crisp inside faces at the exact X=0
        // and Y=0 datum axes without occupying any of the PSU plan envelope.
        translate([-coupon_register_thickness(), 0, WALL_THICKNESS])
            cube([coupon_register_thickness(), coupon_register_length(),
                  coupon_register_height()]);
        translate([0, -coupon_register_thickness(), WALL_THICKNESS])
            cube([coupon_register_length(), coupon_register_thickness(),
                  coupon_register_height()]);
        translate([-coupon_register_thickness(), -coupon_register_thickness(),
                   WALL_THICKNESS])
            cube([coupon_register_thickness(), coupon_register_thickness(),
                  coupon_register_height()]);
    }
}

module hex_prism(af, height) {
    cylinder(r=af/sqrt(3), h=height, $fn=6);
}

module recessed_label(label, at, size=3.0, halign="center") {
    translate([at.x, at.y, WALL_THICKNESS - LABEL_DEPTH])
        linear_extrude(height=LABEL_DEPTH + 0.01)
            text(label, size=size, halign=halign, valign="center", font="Liberation Sans:style=Bold");
}

module printable_coupon() {
    coupon_contract()
    difference() {
        coupon_blank();
        // Use the reviewed PSU library negative; sparse material selects only
        // connected holes/slot needed by this coupon.
        alt1205t_mounting_negatives(WALL_THICKNESS, coupon_m3_hole_diameter());
        // Use only the rigid insertion negative: relaxed tongues are deliberately
        // excluded so the real tongues must compress, pass, spring out and retain.
        translate([coupon_iec_centre().x, coupon_iec_centre().y, 0])
            iecc14_panel_cutout_negative(WALL_THICKNESS, IEC_CLEARANCE);
        translate([coupon_nut_centre().x, coupon_nut_centre().y, -0.01])
            cylinder(d=coupon_m3_hole_diameter(), h=WALL_THICKNESS + 0.02, $fn=36);
        translate([coupon_nut_centre().x, coupon_nut_centre().y,
                   WALL_THICKNESS - coupon_nut_pocket_depth()])
            hex_prism(coupon_nut_pocket_af(), coupon_nut_pocket_depth() + 0.01);
        recessed_label("PSU DATUM", [7,18], 2.6, "left");
        recessed_label("IEC 27x41 NOM +0.20/SIDE", coupon_iec_centre()+[0,-25], 2.2);
        recessed_label("WALL 3.0", coupon_iec_centre()+[0,25], 2.4);
        recessed_label("M3 NUT +0.25 AF", [74,15], 2.1);
    }
}

module evidence_overlay() {
    color([0.05,0.42,0.82,0.45])
        translate([0,0,WALL_THICKNESS+0.02])
            linear_extrude(height=0.12) difference() {
                square(alt1205t_base_size());
                offset(delta=-0.35) square(alt1205t_base_size());
            }
    for (p=alt1205t_m3_centres())
        color([1,0.45,0.05]) translate([p.x,p.y,WALL_THICKNESS+0.04]) cylinder(d=1,h=0.16,$fn=20);
    for (i=[0:len(alt1205t_m3_centres())-1]) {
        p=alt1205t_m3_centres()[i];
        color([0.1,0.1,0.1]) translate([p.x+3,p.y-3,WALL_THICKNESS+0.04])
            linear_extrude(height=0.16) text(str("(",p.x,",",p.y,")"),size=2.2);
    }
    color([0.1,0.1,0.1]) translate([coupon_slot_origin().x-13,8,WALL_THICKNESS+0.04])
        linear_extrude(height=0.16) text("SLOT 3.3x4.7 / T 2.94 / R 3.15",size=2.0);
    color([0.1,0.75,0.35,0.55]) translate([coupon_iec_centre().x,coupon_iec_centre().y,WALL_THICKNESS+0.03])
        linear_extrude(height=0.14) difference() {
            iecc14_panel_profile_2d(IEC_CLEARANCE);
            iecc14_panel_profile_2d(0);
        }
    color([0.85,0.05,0.05]) translate([-35,109,WALL_THICKNESS+0.04])
        linear_extrude(height=0.16) text("FIT COUPON — NO MAINS", size=4.2, font="Liberation Sans:style=Bold");
    color([0.55,0.05,0.75]) translate([3,9,WALL_THICKNESS+coupon_register_height()+0.04])
        linear_extrude(height=0.16) text("SLIDE -X / -Y TO REGISTER", size=2.2,
                                         font="Liberation Sans:style=Bold");
    color([0.15,0.15,0.15]) translate([-37,105,WALL_THICKNESS+0.04])
        linear_extrude(height=0.16) text("orange=PSU centres  green=IEC +0.20/side", size=2.5);
    color([0.1,0.1,0.1]) translate([-35,55,WALL_THICKNESS+0.04])
        linear_extrude(height=0.16) text("IEC NOM 27x41",size=2.5);
    color([0.1,0.1,0.1]) translate([-35,101,WALL_THICKNESS+0.04])
        linear_extrude(height=0.16) text("WALL 3.0 / CLEAR +0.20 SIDE",size=2.1);
    color([0.1,0.1,0.1]) translate([72,18,WALL_THICKNESS+0.04])
        linear_extrude(height=0.16) text("M3 NUT 5.5 +0.25 AF",size=2.1);
}

printable_coupon();
if (EVIDENCE) evidence_overlay();
