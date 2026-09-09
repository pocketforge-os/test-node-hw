/*
 * PocketForge single-supply enclosure candidate.
 *
 * This is a pre-DUT02 prototype, not a certified mains enclosure.  The PSU's
 * metal shell and a separately fabricated 1.0 mm inner barrier remain primary
 * electrical safeguards.  Unplug the IEC lead before removing the hood.
 * Never use the printed structure as protective-earth continuity.
 */

include <lib/alt-1205t-power-supply.scad>
include <lib/iec-c14-fused-switch.scad>

PART = is_undef(PART) ? "assembly" : PART;

WALL = is_undef(WALL) ? 3.2 : WALL;
FLOOR = is_undef(FLOOR) ? 4.0 : FLOOR;
ROOF = is_undef(ROOF) ? 4.0 : ROOF;
IEC_CLEARANCE = is_undef(IEC_CLEARANCE) ? 0.20 : IEC_CLEARANCE;
IEC_SNAP_WALL = is_undef(IEC_SNAP_WALL) ? 1.2 : IEC_SNAP_WALL;
M3_CLEARANCE_DIAMETER = is_undef(M3_CLEARANCE_DIAMETER) ? 3.6 : M3_CLEARANCE_DIAMETER;
M3_NUT_AF = is_undef(M3_NUT_AF) ? 5.75 : M3_NUT_AF;
M3_NUT_DEPTH = is_undef(M3_NUT_DEPTH) ? 2.6 : M3_NUT_DEPTH;
M3_NUT_RETAINING_OPENING_AF = is_undef(M3_NUT_RETAINING_OPENING_AF) ? 5.2 : M3_NUT_RETAINING_OPENING_AF;
M3_NUT_RETAINING_LIP = is_undef(M3_NUT_RETAINING_LIP) ? 0.8 : M3_NUT_RETAINING_LIP;
SEAM_GAP = is_undef(SEAM_GAP) ? 0.8 : SEAM_GAP;
SEAM_OVERLAP = is_undef(SEAM_OVERLAP) ? 6.4 : SEAM_OVERLAP;
SAFETY_DISTANCE = is_undef(SAFETY_DISTANCE) ? 8.0 : SAFETY_DISTANCE;

BARRIER_THICKNESS = is_undef(BARRIER_THICKNESS) ? 1.0 : BARRIER_THICKNESS;
BARRIER_CLEARANCE = is_undef(BARRIER_CLEARANCE) ? 0.4 : BARRIER_CLEARANCE;
BARRIER_HEIGHT = is_undef(BARRIER_HEIGHT) ? 46.0 : BARRIER_HEIGHT;
BARRIER_DC_BUSHING_DIAMETER = is_undef(BARRIER_DC_BUSHING_DIAMETER) ? 8.0 : BARRIER_DC_BUSHING_DIAMETER;
BARRIER_DC_BUSHING_LOCAL = is_undef(BARRIER_DC_BUSHING_LOCAL) ? [13.0, 13.0] : BARRIER_DC_BUSHING_LOCAL;

DC_CONDUCTOR_COUNT = is_undef(DC_CONDUCTOR_COUNT) ? 2 : DC_CONDUCTOR_COUNT;
DC_CONDUCTOR_GAUGE_AWG = is_undef(DC_CONDUCTOR_GAUGE_AWG) ? 18 : DC_CONDUCTOR_GAUGE_AWG;
DC_BUNDLE_OD = is_undef(DC_BUNDLE_OD) ? 6.0 : DC_BUNDLE_OD;
DC_GLAND_CUTOUT_DIAMETER = is_undef(DC_GLAND_CUTOUT_DIAMETER) ? 12.5 : DC_GLAND_CUTOUT_DIAMETER;
DC_GLAND_FLAT = is_undef(DC_GLAND_FLAT) ? 11.8 : DC_GLAND_FLAT;

AC_TERMINAL_PROJECTION = is_undef(AC_TERMINAL_PROJECTION) ? 14.0 : AC_TERMINAL_PROJECTION;
AC_WIRE_BEND_RADIUS = is_undef(AC_WIRE_BEND_RADIUS) ? 18.0 : AC_WIRE_BEND_RADIUS;
IEC_TERMINAL_PROJECTION = is_undef(IEC_TERMINAL_PROJECTION) ? 12.0 : IEC_TERMINAL_PROJECTION;
PE_LUG_SERVICE_DIAMETER = is_undef(PE_LUG_SERVICE_DIAMETER) ? 12.0 : PE_LUG_SERVICE_DIAMETER;
VENT_SLOT = is_undef(VENT_SLOT) ? 1.6 : VENT_SLOT;
VENT_PITCH = is_undef(VENT_PITCH) ? 4.8 : VENT_PITCH;
VENT_PLENUM = is_undef(VENT_PLENUM) ? 10.0 : VENT_PLENUM;

// Coordinator-reviewed expansion: the provisional X=191 wall would overlap
// the exact PSU keepout by 0.2 mm.  X=190 preserves the 3.2 mm wall and leaves
// a nominal 0.8 mm PSU-side clearance without moving the approved component.
function enclosure_outer_min() = [190, 160, 0];
function enclosure_outer_max() = [326, 300, 78];
function enclosure_case_max_x() = 322.8;
function enclosure_rail_min() = [322.8, 117.73, 0];
function enclosure_rail_max() = [326, 338, 20];
function enclosure_rail_hole_yz() = [[125.73,10], [149.73,10], [306,10], [330,10]];
function enclosure_psu_origin() = [194, 257.5, 4];
function enclosure_psu_rotation() = [0,0,-90];
function enclosure_psu_keepout_min() = [194,180,4];
function enclosure_psu_keepout_max() = [304,257.5,40.86];
function enclosure_c14_origin() = [308,300,49.15];
function enclosure_c14_rotation() = [90,0,0];
function enclosure_c14_face_direction() = [0,1,0];
function enclosure_barrier_world_y() = [178,259.5];
function enclosure_barrier_world_z() = [4,4+BARRIER_HEIGHT];
function enclosure_barrier_world_x() = 318.6;
function enclosure_partition_x() = [304,304+WALL];
function enclosure_partition_y() = [261.8,261.8+WALL];
function enclosure_hood_screw_y() = [170,290];
function enclosure_hood_screw_z() = 13;
function enclosure_front_vent_x() = [210,282];
function enclosure_front_vent_z0() = 46;
function enclosure_gland_centre() = [270,160,31];
function enclosure_print_bed() = [247,207];
function enclosure_base_print_size() = [338-117.73,326-190,20];
function enclosure_hood_print_size() = [300-160,326-190,78-4];
function enclosure_psu_point_world(p) = [enclosure_psu_origin().x + p.y,
                                         enclosure_psu_origin().y - p.x];
function enclosure_barrier_size() = [enclosure_barrier_world_y().y-enclosure_barrier_world_y().x,
                                     BARRIER_HEIGHT];

module hex_prism(af, height) {
    cylinder(r=af/sqrt(3), h=height, $fn=6);
}

module enclosure_contract() {
    assert(WALL == 3.2 && FLOOR == 4.0 && ROOF == 4.0,
           "Structural wall/floor/roof contract changed");
    assert(enclosure_outer_min() == [190,160,0] && enclosure_outer_max() == [326,300,78],
           "Enclosure world bounds changed");
    assert(enclosure_psu_keepout_min().x-(enclosure_outer_min().x+WALL) >= 0.8,
           "Expanded X-min must preserve at least 0.8 mm beside the PSU");
    assert(enclosure_rail_min() == [322.8,117.73,0] &&
           enclosure_rail_max() == [326,338,20], "Rail-spine bounds changed");
    assert(enclosure_rail_hole_yz() == [[125.73,10],[149.73,10],[306,10],[330,10]],
           "Existing rail M3 datums changed");
    assert(enclosure_psu_origin() == [194,257.5,4] && enclosure_psu_rotation() == [0,0,-90],
           "Approved PSU transform changed");
    assert(enclosure_psu_keepout_min() == [194,180,4] &&
           enclosure_psu_keepout_max() == [304,257.5,40.86],
           "PSU world keepout changed");
    assert(alt1205t_upper_left_m3_centre() == [4.95,4.95] &&
           alt1205t_lower_left_m3_centre() == [6.75,98.6] &&
           alt1205t_m3_centres() == [[25.3,30.9],[25.3,67],[53.3,67]],
           "Physically approved PSU pattern changed");
    assert(enclosure_c14_origin() == [308,300,49.15] &&
           enclosure_c14_rotation() == [90,0,0] &&
           enclosure_c14_face_direction() == [0,1,0],
           "Rear/wall-facing C14 transform changed");
    assert(iecc14_body_profile_size() == [27,46.86] &&
           iecc14_faceplate_size() == [31,50.3,2] && IEC_CLEARANCE == 0.20,
           "Physically approved C14 interface changed");
    assert(IEC_SNAP_WALL == 1.2 && IEC_SNAP_WALL < WALL,
           "C14 snap island must remain exactly 1.2 mm");
    assert(SEAM_GAP <= 1.0 && SEAM_OVERLAP >= 2*WALL,
           "Labyrinth seam gap/overlap contract failed");
    assert(VENT_SLOT <= 1.6 && VENT_PLENUM >= 10,
           "Touch-resistant vent/plenum guard failed");
    assert(SAFETY_DISTANCE >= 8,
           "Prototype AC separation guard may not be reduced below 8 mm");
    assert(BARRIER_THICKNESS > 0 && BARRIER_HEIGHT > alt1205t_label_side_size().y,
           "Separate barrier must cover the full PSU terminal edge");
    assert(DC_CONDUCTOR_COUNT >= 2 && DC_BUNDLE_OD > 0 &&
           DC_GLAND_CUTOUT_DIAMETER == 12.5,
           "Provisional DC conductor/gland contract changed");
    assert(M3_NUT_AF == 5.75 && M3_NUT_DEPTH == 2.6 &&
           M3_NUT_RETAINING_OPENING_AF < M3_NUT_AF,
           "Positive M3 nut-retention geometry changed");
    assert(enclosure_base_print_size().x <= enclosure_print_bed().x &&
           enclosure_base_print_size().y <= enclosure_print_bed().y,
           "Base does not fit the 247 x 207 bed in declared orientation");
    assert(enclosure_hood_print_size().x <= enclosure_print_bed().x &&
           enclosure_hood_print_size().y <= enclosure_print_bed().y,
           "Hood does not fit the 247 x 207 bed in declared orientation");
    children();
}

module in_psu_frame() {
    translate(enclosure_psu_origin()) rotate(enclosure_psu_rotation()) children();
}

module in_c14_frame() {
    translate(enclosure_c14_origin()) rotate(enclosure_c14_rotation()) children();
}

module rail_spine_blank() {
    p=enclosure_rail_min(); q=enclosure_rail_max();
    translate(p) cube(q-p);
}

module rail_mount_negatives() {
    for (p=enclosure_rail_hole_yz())
        translate([enclosure_rail_min().x-0.01,p.x,p.y])
            rotate([0,90,0]) cylinder(d=M3_CLEARANCE_DIAMETER,h=3.22,$fn=36);
}

module underside_retained_nut_negative(world_p) {
    translate([world_p.x,world_p.y,-0.01])
        hex_prism(M3_NUT_RETAINING_OPENING_AF,M3_NUT_RETAINING_LIP+0.02);
    translate([world_p.x,world_p.y,M3_NUT_RETAINING_LIP])
        hex_prism(M3_NUT_AF,M3_NUT_DEPTH);
}

module psu_mount_negatives() {
    in_psu_frame()
        alt1205t_mounting_negatives(FLOOR,M3_CLEARANCE_DIAMETER,0.02);
    for (p=alt1205t_all_m3_centres())
        underside_retained_nut_negative(enclosure_psu_point_world(p));
}

module seam_tongue() {
    z0=FLOOR-0.02;
    h=SEAM_OVERLAP+0.02;
    // One continuous inset tongue forces two direction changes at the joint.
    // The left run breaks around the exact PSU envelope; the PSU metal shell
    // blocks that local seam from ever becoming a path to its terminal end.
    translate([194,164,z0]) cube([3.2,16,h]);
    // The rear left run clears the transverse AC/SELV partition on both
    // sides; the partition itself closes that short portion of the joint.
    translate([194,257.5,z0]) cube([3.2,3.5,h]);
    translate([194,265.8,z0]) cube([3.2,30.2,h]);
    translate([315.6,164,z0]) cube([3.2,132,h]);
    // The front run likewise clears the longitudinal partition.  Keeping the
    // tongue and hood volume-disjoint avoids assembly force and slicer scars.
    translate([197.2,164,z0]) cube([106.0,3.2,h]);
    translate([308.0,164,z0]) cube([7.6,3.2,h]);
    translate([197.2,292.8,z0]) cube([118.4,3.2,h]);
}

module barrier_lower_capture() {
    y0=enclosure_barrier_world_y().x;
    len=enclosure_barrier_size().x;
    gap=BARRIER_THICKNESS+2*BARRIER_CLEARANCE;
    translate([enclosure_barrier_world_x()-gap/2-WALL,y0,FLOOR-0.02]) cube([WALL,len,4.02]);
    translate([enclosure_barrier_world_x()+gap/2,y0,FLOOR-0.02]) cube([WALL,len,4.02]);
}

module vertical_nut_insert_boss(side,y) {
    x0=side=="left" ? 193.2 : 313.2;
    w=side=="left" ? 7.2 : 6.4;
    translate([x0,y-6,FLOOR-0.02]) cube([w,12,14.02]);
}

module vertical_nut_insert_negative(side,y) {
    z=enclosure_hood_screw_z();
    // Horizontal nut axis, but insertion rises from the safe underside.
    xnut=side=="left" ? 195.0 : 316.0;
    translate([xnut,y,z]) rotate([0,90,0]) hex_prism(M3_NUT_AF,M3_NUT_DEPTH);
    translate([xnut,y-M3_NUT_AF/2,-0.01])
        cube([M3_NUT_DEPTH,M3_NUT_AF,z+0.02]);
    if (side=="left")
        translate([189.99,y,z]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,h=xnut-189.99+M3_NUT_DEPTH+0.2,$fn=36);
    else
        translate([xnut-0.2,y,z]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,h=326.01-(xnut-0.2),$fn=36);
}

module conductor_retention_saddle(p=[310,272,4]) {
    difference() {
        translate(p) cube([8,9,10]);
        translate([p.x-0.01,p.y+2.5,p.z+4]) cube([8.02,4,2.4]);
    }
}

module installed_base() {
    enclosure_contract()
    difference() {
        union() {
            translate(enclosure_outer_min()) cube([136,140,FLOOR]);
            rail_spine_blank();
            seam_tongue();
            barrier_lower_capture();
            for (side=["left","right"], y=enclosure_hood_screw_y())
                vertical_nut_insert_boss(side,y);
            // Separate retention points for IEC/PE and insulated DC routing.
            conductor_retention_saddle([309,268,FLOOR-0.02]);
            conductor_retention_saddle([309,244,FLOOR-0.02]);
            conductor_retention_saddle([286,168,FLOOR-0.02]);
        }
        rail_mount_negatives();
        psu_mount_negatives();
        for (side=["left","right"], y=enclosure_hood_screw_y())
            vertical_nut_insert_negative(side,y);
    }
}

module c14_faceplate_recess_negative() {
    // Recess only below the 31 x 50.3 faceplate, leaving a 1.2 mm snap island.
    translate([308-iecc14_faceplate_size().x/2,296.79,
               49.15-iecc14_faceplate_size().y/2])
        cube([iecc14_faceplate_size().x, WALL-IEC_SNAP_WALL+0.01,
              iecc14_faceplate_size().y]);
}

module c14_panel_negative() {
    in_c14_frame() iecc14_panel_cutout_negative(IEC_SNAP_WALL,IEC_CLEARANCE);
}

module hood_screw_negatives() {
    z=enclosure_hood_screw_z();
    for (y=enclosure_hood_screw_y()) {
        translate([189.99,y,z]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,h=8,$fn=36);
        translate([318.8,y,z]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,h=7.22,$fn=36);
    }
}

module front_outer_vent_negatives() {
    for (z=[enclosure_front_vent_z0():VENT_PITCH:65])
        translate([enclosure_front_vent_x().x,159.99,z])
            cube([enclosure_front_vent_x().y-enclosure_front_vent_x().x,
                  WALL+0.02,VENT_SLOT]);
}

module front_inner_baffle_negative() {
    // Half-pitch shift prevents a straight tool/finger line through both banks.
    for (z=[enclosure_front_vent_z0()+VENT_PITCH/2:VENT_PITCH:67])
        translate([enclosure_front_vent_x().x,166.39,z])
            cube([enclosure_front_vent_x().y-enclosure_front_vent_x().x,
                  WALL+0.02,VENT_SLOT]);
}

module gland_negative() {
    c=enclosure_gland_centre();
    translate([c.x,159.99,c.z]) rotate([-90,0,0])
        intersection() {
            cylinder(d=DC_GLAND_CUTOUT_DIAMETER,h=WALL+0.02,$fn=48);
            translate([-DC_GLAND_FLAT/2,-DC_GLAND_CUTOUT_DIAMETER/2,-0.01])
                cube([DC_GLAND_FLAT,DC_GLAND_CUTOUT_DIAMETER,WALL+0.04]);
        }
}

module barrier_lower_capture_clearance_negative() {
    // The base's outboard barrier rail keys into this hood-wall pocket.  The
    // rail itself replaces the removed wall segment, creating a stepped joint
    // instead of two printable parts occupying the same volume.
    translate([319.4,177.8,FLOOR-0.2]) cube([3.42,81.9,4.4]);
}

module separation_partition() {
    // Composite L-shaped boundary.  The removable nonprinted plate fills the
    // lower gap over the PSU's entire terminal edge; printed wall continues
    // above it and around both ends.
    x0=enclosure_partition_x().x;
    translate([x0,160,FLOOR]) cube([WALL,18.02,FLOOR+BARRIER_HEIGHT]);
    translate([x0,259.48,FLOOR]) cube([WALL,5.54,70.02]);
    translate([x0,177.98,FLOOR+BARRIER_HEIGHT-0.02])
        cube([WALL,81.54,74-(FLOOR+BARRIER_HEIGHT)+0.04]);
    translate([190,enclosure_partition_y().x,FLOOR])
        cube([117.22,WALL,70.02]);
}

module barrier_upper_capture() {
    y0=enclosure_barrier_world_y().x;
    len=enclosure_barrier_size().x;
    gap=BARRIER_THICKNESS+2*BARRIER_CLEARANCE;
    z0=FLOOR+BARRIER_HEIGHT-4;
    translate([enclosure_barrier_world_x()-gap/2-WALL,y0,z0]) cube([WALL,len+0.02,4.02]);
    translate([enclosure_barrier_world_x()+gap/2,y0,z0]) cube([WALL,len+0.02,4.02]);
    // Bridges enter the already-solid partition at its upper/rear corner.
    translate([enclosure_barrier_world_x()-gap/2-WALL,259.48,z0])
        cube([2*WALL+gap,0.04,4.02]);
}

module hood_shell_blank() {
    // Roof and four walls.  The wall depth below the tongue creates a
    // 6.4 mm overlap; the 0.8 mm lateral gap never forms a direct seam.
    translate([190,160,74]) cube([132.8,140,ROOF]);
    translate([190,160,FLOOR]) cube([WALL,140,70.02]);
    translate([319.6,160,FLOOR]) cube([WALL,140,70.02]);
    translate([193.18,160,FLOOR]) cube([126.44,WALL,70.02]);
    translate([193.18,296.8,FLOOR]) cube([126.44,WALL,70.02]);
    // Local rear reinforcement supports the complete 31 mm faceplate while
    // preserving the global X=326 box/rail bound.
    translate([319.58,296.8,23.98]) cube([6.42,WALL,50.34]);
    separation_partition();
    barrier_upper_capture();
    // Staggered inner baffle is separated from the front skin by 3.2 mm air.
    translate([enclosure_front_vent_x().x-WALL,166.4,43])
        cube([enclosure_front_vent_x().y-enclosure_front_vent_x().x+2*WALL,
              WALL,31.02]);
}

module installed_hood() {
    enclosure_contract()
    difference() {
        hood_shell_blank();
        c14_faceplate_recess_negative();
        c14_panel_negative();
        hood_screw_negatives();
        front_outer_vent_negatives();
        front_inner_baffle_negative();
        gland_negative();
        barrier_lower_capture_clearance_negative();
    }
}

module barrier_template_2d() {
    size=enclosure_barrier_size();
    difference() {
        square(size);
        translate(BARRIER_DC_BUSHING_LOCAL)
            circle(d=BARRIER_DC_BUSHING_DIAMETER,$fn=48);
    }
}

module installed_barrier() {
    y0=enclosure_barrier_world_y().x;
    z0=enclosure_barrier_world_z().x;
    difference() {
        translate([enclosure_barrier_world_x()-BARRIER_THICKNESS/2,y0,z0])
            cube([BARRIER_THICKNESS,enclosure_barrier_size().x,enclosure_barrier_size().y]);
        translate([enclosure_barrier_world_x()-BARRIER_THICKNESS/2-0.01,
                   y0+BARRIER_DC_BUSHING_LOCAL.x,z0+BARRIER_DC_BUSHING_LOCAL.y])
            rotate([0,90,0]) cylinder(d=BARRIER_DC_BUSHING_DIAMETER,
                                      h=BARRIER_THICKNESS+0.02,$fn=48);
    }
}

module service_keepouts() {
    // Transparent evidence volumes; every value is an overridable assumption.
    color([1,0.3,0.05,0.25])
        translate([304,180,8]) cube([AC_TERMINAL_PROJECTION,77.5,36]);
    color([1,0.75,0.05,0.22])
        translate([296,270,25]) cube([24,AC_WIRE_BEND_RADIUS,35]);
    color([0.95,0.8,0.15,0.30])
        translate([302,276,38]) sphere(d=PE_LUG_SERVICE_DIAMETER,$fn=32);
    color([0.1,0.55,0.95,0.20])
        translate([enclosure_gland_centre().x,170,enclosure_gland_centre().z])
            rotate([90,0,0]) cylinder(d=DC_BUNDLE_OD,h=20,$fn=32);
    color([0.85,0.4,0.12,0.18])
        translate([294.5,278.2-IEC_TERMINAL_PROJECTION,25.72])
            cube([27,IEC_TERMINAL_PROJECTION,46.86]);
    // Reserved direct copper PE route: C14 PE lug to the PSU PE terminal
    // region.  Endpoint screw coordinates remain deliberately unspecified.
    color([0.95,0.75,0.05,0.70]) {
        hull() for (p=[[310,276,49],[312,266,43]])
            translate(p) sphere(d=3.2,$fn=24);
        hull() for (p=[[312,266,43],[312,244,34]])
            translate(p) sphere(d=3.2,$fn=24);
    }
}

module open_top_evidence() {
    color([0.18,0.48,0.78]) installed_base();
    color([0.78,0.82,0.86,0.38])
        intersection() {
            installed_hood();
            translate([189,159,3.9]) cube([138,142,70]);
        }
    color([0.70,0.72,0.74]) in_psu_frame() alt1205t_keepout();
    color([0.10,0.11,0.12]) in_c14_frame() iecc14_keepout();
    color([0.95,0.75,0.12,0.72]) installed_barrier();
    service_keepouts();
}

module assembly_evidence(section=false,show_service=false) {
    if (section) {
        color([0.18,0.48,0.78]) installed_base();
        color([0.78,0.82,0.86,0.72])
            difference() {
                installed_hood();
                // Evidence-only front/left corner removal exposes the PSU,
                // L-partition, terminal shield and both routing volumes.
                translate([189,159,3.9]) cube([131,111,75]);
            }
        color([0.70,0.72,0.74]) in_psu_frame() alt1205t_keepout();
        color([0.10,0.11,0.12]) in_c14_frame() iecc14_keepout();
        color([0.95,0.75,0.12,0.72]) installed_barrier();
        if (show_service) service_keepouts();
    } else {
        color([0.18,0.48,0.78]) installed_base();
        color([0.78,0.82,0.86,0.68]) installed_hood();
        color([0.70,0.72,0.74]) in_psu_frame() alt1205t_keepout();
        color([0.10,0.11,0.12]) in_c14_frame() iecc14_keepout();
        color([0.95,0.75,0.12,0.72]) installed_barrier();
        if (show_service) service_keepouts();
    }
}

module installed_preview() {
    assembly_evidence(false,true);
    // Existing 20-series rail datum proxy only; no legacy chassis source edit.
    color([0.6,0.62,0.65,0.45])
        translate([322.8,117.73,0]) cube([20,220.27,20]);
}

module base_hood_forbidden_intersection() {
    // Seating faces at the floor, rail spine and captive-nut bosses are
    // intentional boundary contacts.  These interior base features must have
    // no volume in common with the hood or its internal partitions.
    intersection() {
        union() {
            seam_tongue();
            barrier_lower_capture();
            conductor_retention_saddle([309,268,FLOOR-0.02]);
            conductor_retention_saddle([309,244,FLOOR-0.02]);
            conductor_retention_saddle([286,168,FLOOR-0.02]);
        }
        installed_hood();
    }
}

module printable_base() {
    // Floor down; long rail spine becomes printer X (220.27 x 136 mm).
    translate([338,-190,0]) rotate([0,0,90]) installed_base();
}

module printable_hood() {
    // Roof down; 140 x 136 mm footprint, no support material intended.
    translate([-190,300,78]) rotate([180,0,0]) installed_hood();
}

if (PART == "base") printable_base();
else if (PART == "hood") printable_hood();
else if (PART == "barrier_template") barrier_template_2d();
else if (PART == "assembly") assembly_evidence(false);
else if (PART == "installed_preview") installed_preview();
else if (PART == "evidence_top") open_top_evidence();
else if (PART == "evidence_rear") assembly_evidence(false,true);
else if (PART == "evidence_section") assembly_evidence(true,true);
else if (PART == "base_hood_interference") base_hood_forbidden_intersection();
else if (PART == "hood_psu_interference") intersection() {
    installed_hood(); in_psu_frame() alt1205t_keepout();
}
else assert(false,str("Unknown power-system enclosure PART: ",PART));
