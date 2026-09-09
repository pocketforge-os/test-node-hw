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
HOOD_NUT_AF = is_undef(HOOD_NUT_AF) ? 5.60 : HOOD_NUT_AF;
HOOD_NUT_DEPTH = is_undef(HOOD_NUT_DEPTH) ? 2.80 : HOOD_NUT_DEPTH;
HOOD_NUT_LEAD_AF = is_undef(HOOD_NUT_LEAD_AF) ? 6.20 : HOOD_NUT_LEAD_AF;
HOOD_NUT_LEAD_DEPTH = is_undef(HOOD_NUT_LEAD_DEPTH) ? 0.80 : HOOD_NUT_LEAD_DEPTH;
HOOD_NUT_CAPTURE_WALL = is_undef(HOOD_NUT_CAPTURE_WALL) ? 2.40 : HOOD_NUT_CAPTURE_WALL;
PSU_NUT_MEASURED_DEPTH = is_undef(PSU_NUT_MEASURED_DEPTH) ? 2.30 : PSU_NUT_MEASURED_DEPTH;
PSU_NUT_AF = is_undef(PSU_NUT_AF) ? 5.60 : PSU_NUT_AF;
PSU_NUT_DEPTH = is_undef(PSU_NUT_DEPTH) ? 2.60 : PSU_NUT_DEPTH;
SEAM_GAP = is_undef(SEAM_GAP) ? 0.8 : SEAM_GAP;
SEAM_OVERLAP = is_undef(SEAM_OVERLAP) ? 6.4 : SEAM_OVERLAP;
SAFETY_DISTANCE = is_undef(SAFETY_DISTANCE) ? 8.0 : SAFETY_DISTANCE;

BARRIER_THICKNESS = is_undef(BARRIER_THICKNESS) ? 1.0 : BARRIER_THICKNESS;
BARRIER_CLEARANCE = is_undef(BARRIER_CLEARANCE) ? 0.4 : BARRIER_CLEARANCE;
BARRIER_HEIGHT = is_undef(BARRIER_HEIGHT) ? 46.0 : BARRIER_HEIGHT;
DC_BUSHING_DIAMETER = is_undef(DC_BUSHING_DIAMETER) ? 8.0 : DC_BUSHING_DIAMETER;
DC_BUSHING_CENTRE = is_undef(DC_BUSHING_CENTRE) ? [305.6,191,54] : DC_BUSHING_CENTRE;
DC_ROUTE_BEND_ENVELOPE = is_undef(DC_ROUTE_BEND_ENVELOPE) ? 10.0 : DC_ROUTE_BEND_ENVELOPE;

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
function enclosure_hood_screw_z() = 25.6;
function enclosure_hood_nut_boss_min_x(side) = side=="left" ? 194.0 : 312.0;
function enclosure_hood_nut_boss_max_x(side) = side=="left" ? 200.4 : 318.8;
function enclosure_hood_nut_mouth_x(side) = side=="left" ?
    enclosure_hood_nut_boss_min_x(side) : enclosure_hood_nut_boss_max_x(side);
function enclosure_hood_nut_direction(side) = side=="left" ? 1 : -1;
function enclosure_hood_nut_pocket_inner_x(side) =
    enclosure_hood_nut_mouth_x(side) + enclosure_hood_nut_direction(side) *
        (HOOD_NUT_LEAD_DEPTH+HOOD_NUT_DEPTH);
function enclosure_hood_nut_backstop_depth(side) = side=="left" ?
    enclosure_hood_nut_boss_max_x(side)-enclosure_hood_nut_pocket_inner_x(side) :
    enclosure_hood_nut_pocket_inner_x(side)-enclosure_hood_nut_boss_min_x(side);
function enclosure_hood_nut_boss_top() = 32.0;
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
function enclosure_upper_service_max_x() = min(
    enclosure_partition_x().x+AC_TERMINAL_PROJECTION,
    enclosure_barrier_world_x()
        -(BARRIER_THICKNESS+2*BARRIER_CLEARANCE)/2-WALL
);

module hex_prism(af, height) {
    cylinder(r=af/sqrt(3), h=height, $fn=6);
}

module tapered_hex_prism(start_af, end_af, height) {
    linear_extrude(height=height, scale=end_af/start_af)
        circle(r=start_af/sqrt(3),$fn=6);
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
    assert(DC_BUSHING_DIAMETER == 8.0 && DC_BUSHING_CENTRE == [305.6,191,54],
           "Provisional insulated DC bushing contract changed");
    assert(DC_ROUTE_BEND_ENVELOPE >= DC_BUNDLE_OD,
           "DC bend envelope must contain the complete bundle");
    assert(enclosure_upper_service_max_x()-(304+WALL) >= DC_BUNDLE_OD,
           "Upper terminal service corridor must fit the provisional DC bundle");
    assert(DC_CONDUCTOR_COUNT >= 2 && DC_BUNDLE_OD > 0 &&
           DC_GLAND_CUTOUT_DIAMETER == 12.5,
           "Provisional DC conductor/gland contract changed");
    assert(HOOD_NUT_AF == 5.60 && HOOD_NUT_DEPTH == 2.80 &&
           HOOD_NUT_LEAD_AF == 6.20 && HOOD_NUT_LEAD_DEPTH == 0.80 &&
           HOOD_NUT_CAPTURE_WALL == 2.40,
           "Qualified hood M3 pressure-fit geometry changed");
    assert(PSU_NUT_MEASURED_DEPTH == 2.30 && PSU_NUT_AF == 5.60 &&
           PSU_NUT_DEPTH == 2.60 && FLOOR-PSU_NUT_DEPTH == 1.40,
           "PSU top-loaded nut socket/floor contract changed");
    assert(enclosure_hood_screw_z() == 25.6 &&
           enclosure_hood_nut_boss_top() == 32.0,
           "Hood screw axes/boss tops must remain above the rail");
    assert(enclosure_hood_screw_z()-HOOD_NUT_LEAD_AF/sqrt(3)-
               enclosure_rail_max().z >= 2.0,
           "Rail-side nut lead-in needs at least 2.0 mm vertical clearance");
    assert(6-HOOD_NUT_AF/sqrt(3) >= HOOD_NUT_CAPTURE_WALL &&
           enclosure_hood_nut_boss_top()-enclosure_hood_screw_z()-
               HOOD_NUT_AF/sqrt(3) >= HOOD_NUT_CAPTURE_WALL &&
           enclosure_hood_nut_backstop_depth("left") >= HOOD_NUT_CAPTURE_WALL &&
           enclosure_hood_nut_backstop_depth("right") >= HOOD_NUT_CAPTURE_WALL,
           "Hood nut sockets need complete 2.4 mm capture/backstop material");
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

module psu_top_pressure_nut_negative(world_p) {
    // The measured 2.30 mm nut loads visibly from the top before the PSU.
    // A 2.60 mm-deep qualified-AF pocket preserves 1.40 mm of the 4 mm floor.
    translate([world_p.x,world_p.y,FLOOR-PSU_NUT_DEPTH])
        hex_prism(PSU_NUT_AF,PSU_NUT_DEPTH+0.02);
}

module psu_mount_negatives() {
    in_psu_frame()
        alt1205t_mounting_negatives(FLOOR,M3_CLEARANCE_DIAMETER,0.02);
    for (p=alt1205t_all_m3_centres())
        psu_top_pressure_nut_negative(enclosure_psu_point_world(p));
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
    x0=enclosure_hood_nut_boss_min_x(side);
    w=enclosure_hood_nut_boss_max_x(side)-x0;
    translate([x0,y-6,FLOOR-0.02])
        cube([w,12,enclosure_hood_nut_boss_top()-(FLOOR-0.02)]);
}

module vertical_nut_insert_negative(side,y) {
    z=enclosure_hood_screw_z();
    face=enclosure_hood_nut_mouth_x(side);
    inner=enclosure_hood_nut_pocket_inner_x(side);
    // Broad-face axial insertion copies the owner-qualified 5.60-AF pocket.
    // The provisional 0.8 mm taper starts the nut square; there is no rigid
    // undersized throat, bed-facing mouth, support-filled chute, or hidden turn.
    if (side=="left")
        translate([face-0.01,y,z]) rotate([0,90,0]) {
            tapered_hex_prism(HOOD_NUT_LEAD_AF,HOOD_NUT_AF,
                              HOOD_NUT_LEAD_DEPTH+0.02);
            translate([0,0,HOOD_NUT_LEAD_DEPTH])
                hex_prism(HOOD_NUT_AF,HOOD_NUT_DEPTH+0.02);
        }
    else
        translate([face+0.01,y,z]) rotate([0,-90,0]) {
            tapered_hex_prism(HOOD_NUT_LEAD_AF,HOOD_NUT_AF,
                              HOOD_NUT_LEAD_DEPTH+0.02);
            translate([0,0,HOOD_NUT_LEAD_DEPTH])
                hex_prism(HOOD_NUT_AF,HOOD_NUT_DEPTH+0.02);
        }
    // The bore reaches 0.4 mm beyond the nut for full thread engagement, then
    // stops inside the solid boss so no opening reaches the protected cavity.
    if (side=="left")
        translate([189.99,y,z]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,
                     h=inner+0.4-189.99,$fn=36);
    else
        translate([inner-0.4,y,z]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,
                     h=326.01-(inner-0.4),$fn=36);
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

module partition_dc_bushing_negative(clearance=0) {
    c=DC_BUSHING_CENTRE;
    translate([enclosure_partition_x().x-0.01,c.y,c.z])
        rotate([0,90,0])
            cylinder(d=DC_BUSHING_DIAMETER+2*clearance,
                     h=WALL+0.02,$fn=48);
}

module terminal_partition_required_solid() {
    // Complete X=304 boundary from the PSU metal-shell top to the roof-side
    // partition.  The DC bushing below is the only intentional breach.
    translate([enclosure_partition_x().x,177.98,
               enclosure_psu_keepout_max().z])
        cube([WALL,81.54,74.02-enclosure_psu_keepout_max().z]);
}

module separation_partition() {
    // Composite L-shaped boundary.  The removable nonprinted plate fills the
    // lower gap over the PSU's entire terminal edge; printed wall continues
    // above it and around both ends.
    x0=enclosure_partition_x().x;
    translate([x0,160,FLOOR]) cube([WALL,18.02,FLOOR+BARRIER_HEIGHT]);
    translate([x0,259.48,FLOOR]) cube([WALL,5.54,70.02]);
    difference() {
        terminal_partition_required_solid();
        partition_dc_bushing_negative();
    }
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
    // Continuous finger shield: insulated DC now crosses the printed X=304
    // partition above the PSU instead of entering the former dead side gap.
    square(enclosure_barrier_size());
}

module installed_barrier() {
    y0=enclosure_barrier_world_y().x;
    z0=enclosure_barrier_world_z().x;
    translate([enclosure_barrier_world_x()-BARRIER_THICKNESS/2,y0,z0])
        cube([BARRIER_THICKNESS,enclosure_barrier_size().x,enclosure_barrier_size().y]);
}

function dc_route_points() = [
    [312,191,54], [300,191,54], [270,191,54], [270,173,54],
    [270,173,38], [270,164,31], [270,157,31]
];

module dc_bundle_route_keepout() {
    pts=dc_route_points();
    // A connected 6 mm sweep crosses only the named partition bushing and
    // front gland.  Enlarged elbow envelopes reserve provisional bend space.
    color([0.1,0.55,0.95,0.42]) {
        for (i=[0:len(pts)-2])
            hull() for (p=[pts[i],pts[i+1]])
                translate(p) sphere(d=DC_BUNDLE_OD,$fn=32);
        for (p=[pts[2],pts[4]])
            translate(p) sphere(d=DC_ROUTE_BEND_ENVELOPE,$fn=32);
    }
}

module ac_terminal_service_keepout() {
    // Full projection below the PSU top; above it the envelope steps outward
    // to X>=307.2 so the continuous printed partition remains honest.
    color([1,0.3,0.05,0.25]) {
        translate([304,180,8])
            cube([AC_TERMINAL_PROJECTION,77.5,
                  enclosure_psu_keepout_max().z-8]);
        translate([304+WALL,180,enclosure_psu_keepout_max().z])
            cube([enclosure_upper_service_max_x()-(304+WALL),77.5,
                  FLOOR+BARRIER_HEIGHT-enclosure_psu_keepout_max().z]);
    }
}

module ac_terminal_service_clearance_core() {
    // The 0.02 mm inset removes intentional tangencies from the interference
    // proof while retaining the complete two-level service-volume topology.
    translate([304.02,180.02,8.02])
        cube([AC_TERMINAL_PROJECTION-0.04,77.46,
              enclosure_psu_keepout_max().z-8.04]);
    translate([304+WALL+0.02,180.02,
               enclosure_psu_keepout_max().z+0.02])
        cube([enclosure_upper_service_max_x()-(304+WALL)-0.04,77.46,
              FLOOR+BARRIER_HEIGHT-enclosure_psu_keepout_max().z-0.04]);
}

module service_keepouts() {
    // Transparent evidence volumes; every value is an overridable assumption.
    ac_terminal_service_keepout();
    color([1,0.75,0.05,0.22])
        translate([296,270,25]) cube([24,AC_WIRE_BEND_RADIUS,35]);
    color([0.95,0.8,0.15,0.30])
        translate([302,276,38]) sphere(d=PE_LUG_SERVICE_DIAMETER,$fn=32);
    dc_bundle_route_keepout();
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

module partition_missing_material() {
    difference() {
        difference() {
            terminal_partition_required_solid();
            partition_dc_bushing_negative();
        }
        installed_hood();
    }
}

module terminal_partition_slice() {
    intersection() {
        terminal_partition_required_solid();
        installed_hood();
    }
}

module terminal_service_hood_interference() {
    intersection() {
        ac_terminal_service_clearance_core();
        installed_hood();
    }
}

module dc_route_hood_interference() {
    intersection() {
        dc_bundle_route_keepout();
        installed_hood();
    }
}

module dc_route_psu_interference() {
    intersection() {
        dc_bundle_route_keepout();
        in_psu_frame() alt1205t_keepout();
    }
}

module psu_forbidden_interior() {
    // The partition intentionally begins on the PSU shell's Z=40.86 boundary
    // so the metal top and printed wall close the vestibule together.  Test
    // the keepout interior, inset by 0.01 mm, to distinguish that shared
    // zero-thickness boundary from a forbidden positive-volume intrusion.
    p=enclosure_psu_keepout_min();
    q=enclosure_psu_keepout_max();
    translate(p+[0.01,0.01,0.01]) cube(q-p-[0.02,0.02,0.02]);
}

module hood_nut_cap_required_solid(side,y) {
    z=enclosure_hood_screw_z();
    difference() {
        if (side=="left")
            translate([190,y,z]) rotate([0,90,0])
                hex_prism(HOOD_NUT_LEAD_AF,WALL);
        else
            translate([319.6,y,z]) rotate([0,90,0])
                hex_prism(HOOD_NUT_LEAD_AF,WALL);
        if (side=="left")
            translate([189.99,y,z]) rotate([0,90,0])
                cylinder(d=M3_CLEARANCE_DIAMETER,h=WALL+0.02,$fn=36);
        else
            translate([319.59,y,z]) rotate([0,90,0])
                cylinder(d=M3_CLEARANCE_DIAMETER,h=WALL+0.02,$fn=36);
    }
}

module hood_nut_backstop_required_solid(side,y) {
    z=enclosure_hood_screw_z();
    inner=enclosure_hood_nut_pocket_inner_x(side);
    depth=enclosure_hood_nut_backstop_depth(side);
    required_radius=HOOD_NUT_AF/sqrt(3)+HOOD_NUT_CAPTURE_WALL;
    if (side=="left")
        translate([inner+0.02,y,z]) rotate([0,90,0])
            difference() {
                cylinder(r=required_radius,h=depth-0.04,$fn=48);
                translate([0,0,-0.01])
                    cylinder(d=M3_CLEARANCE_DIAMETER+0.04,h=0.46,$fn=36);
            }
    else
        translate([inner-0.02,y,z]) rotate([0,-90,0])
            difference() {
                cylinder(r=required_radius,h=depth-0.04,$fn=48);
                translate([0,0,-0.01])
                    cylinder(d=M3_CLEARANCE_DIAMETER+0.04,h=0.46,$fn=36);
            }
}

module hood_nut_cap_missing() {
    for (side=["left","right"], y=enclosure_hood_screw_y())
        difference() {
            hood_nut_cap_required_solid(side,y);
            installed_hood();
        }
}

module hood_nut_backstop_missing() {
    for (side=["left","right"], y=enclosure_hood_screw_y())
        difference() {
            hood_nut_backstop_required_solid(side,y);
            installed_base();
        }
}

module psu_nut_floor_missing() {
    // Inset proof volume under each complete socket.  It must remain solid so
    // the 2.60 mm top opening cannot become a bed-facing feeder or fall path.
    for (p=alt1205t_all_m3_centres())
        let (w=enclosure_psu_point_world(p))
            difference() {
                translate([w.x,w.y,0.02])
                    hex_prism(PSU_NUT_AF,1.36);
                installed_base();
            }
}

module installed_right_hood_nut_coupon_base() {
    // Exact right/front base neighborhood: floor, socket boss, 3.2 mm gap,
    // and the frozen 20 mm rail obstruction.  It remains floor-down.
    difference() {
        union() {
            translate([310,164,0]) cube([16,12,FLOOR]);
            vertical_nut_insert_boss("right",170);
            translate([322.8,164,0]) cube([3.2,12,20]);
        }
        vertical_nut_insert_negative("right",170);
    }
}

module installed_right_hood_cap_coupon() {
    // Exact local hood-wall/bore crop.  The coupon keeps the production
    // roof-down orientation but translates this remote wall segment to Z=0.
    intersection() {
        installed_hood();
        translate([313.2,164,20]) cube([9.6,12,12]);
    }
}

module psu_nut_coupon() {
    difference() {
        translate([0,0,0]) cube([12,12,FLOOR]);
        psu_top_pressure_nut_negative([6,6]);
    }
}

module nut_fit_coupon() {
    // Three support-free, text-free pieces in the production orientations:
    // exact right base socket/rail, roof-down hood cap, and floor-down PSU pad.
    translate([-162,-120,0])
        translate([338,-190,0]) rotate([0,0,90])
            installed_right_hood_nut_coupon_base();
    translate([20-129.6,-124,-46])
        translate([-190,300,78]) rotate([180,0,0])
            installed_right_hood_cap_coupon();
    translate([38,0,0]) psu_nut_coupon();
}

module hood_nut_proxy(side,y) {
    // Evidence-only measured nut proxy, centered in the 2.8 mm pocket.
    inner=enclosure_hood_nut_pocket_inner_x(side);
    if (side=="left")
        translate([inner-HOOD_NUT_DEPTH+0.2,y,enclosure_hood_screw_z()])
            rotate([0,90,0]) hex_prism(5.5,2.4);
    else
        translate([inner+HOOD_NUT_DEPTH-0.2,y,enclosure_hood_screw_z()])
            rotate([0,-90,0]) hex_prism(5.5,2.4);
}

module nut_socket_section_evidence() {
    // Direct half-section through the rail-side mouth, pressure-fit nut,
    // hood cap, screw path and rail clearance.  Evidence only; no text.
    color([0.18,0.48,0.78])
        intersection() {
            installed_base();
            translate([308,170,0]) cube([19,6,36]);
        }
    color([0.78,0.82,0.86,0.72])
        intersection() {
            installed_hood();
            translate([308,170,20]) cube([19,6,16]);
        }
    color([0.85,0.56,0.12])
        intersection() {
            hood_nut_proxy("right",170);
            translate([308,170,0]) cube([19,6,36]);
        }
    color([0.68,0.70,0.74])
        translate([318.4,170,enclosure_hood_screw_z()]) rotate([0,90,0])
            cylinder(d=3,h=7.8,$fn=32);
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
else if (PART == "partition_missing_material") partition_missing_material();
else if (PART == "partition_slice") terminal_partition_slice();
else if (PART == "terminal_service_hood_interference") terminal_service_hood_interference();
else if (PART == "dc_route_keepout") dc_bundle_route_keepout();
else if (PART == "dc_route_hood_interference") dc_route_hood_interference();
else if (PART == "dc_route_psu_interference") dc_route_psu_interference();
else if (PART == "hood_nut_cap_missing") hood_nut_cap_missing();
else if (PART == "hood_nut_backstop_missing") hood_nut_backstop_missing();
else if (PART == "psu_nut_floor_missing") psu_nut_floor_missing();
else if (PART == "nut_fit_coupon") nut_fit_coupon();
else if (PART == "evidence_nut_section") nut_socket_section_evidence();
else if (PART == "hood_psu_interference") intersection() {
    installed_hood(); psu_forbidden_interior();
}
else assert(false,str("Unknown power-system enclosure PART: ",PART));
