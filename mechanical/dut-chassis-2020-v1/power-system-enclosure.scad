/*
 * PocketForge single-supply mains enclosure, V2 print candidate.
 *
 * Three support-free printed parts: floor-down base, roof-down hood, and
 * broad-face-down IEC C14 cassette.  The separately fabricated 1.0 mm
 * terminal barrier remains part of the assembly.  This is a prototype, not a
 * certified mains enclosure.  Unplug before opening and never use printed
 * plastic as protective-earth continuity.
 */

include <lib/alt-1205t-power-supply.scad>
include <lib/iec-c14-fused-switch.scad>

PART = is_undef(PART) ? "assembly" : PART;
NOZZLE_DIAMETER = is_undef(NOZZLE_DIAMETER) ? 0.8 : NOZZLE_DIAMETER;

function nozzle_lines_at_least(v) = ceil(v / NOZZLE_DIAMETER) * NOZZLE_DIAMETER;
function printable_at_least(v) = max(NOZZLE_DIAMETER, nozzle_lines_at_least(v));

NOMINAL_WALL = 3.2;
WALL = printable_at_least(NOMINAL_WALL);
FLOOR = printable_at_least(4.0);
ROOF = WALL;
FRAME = printable_at_least(4.0);
RECEIVER_WALL = WALL;
POSITIVE_UNION = WALL;
LOCAL_UNION = NOZZLE_DIAMETER;
KEY_UNION = NOZZLE_DIAMETER;
IEC_CLEARANCE = 0.20;
IEC_SNAP_NOMINAL = 1.2;
IEC_SNAP_WALL = max(IEC_SNAP_NOMINAL, NOZZLE_DIAMETER);
M3_CLEARANCE_DIAMETER = 3.6;
HOOD_NUT_AF = 5.60;
HOOD_NUT_DEPTH = 2.80;
HOOD_NUT_LEAD_AF = 6.20;
HOOD_NUT_LEAD_DEPTH = 0.80;
HOOD_NUT_BACKSTOP = 2.40;
HOOD_NUT_RADIAL_CAPTURE = 2.40;
PSU_NUT_AF = 5.60;
PSU_NUT_DEPTH = 2.60;
SEAM_GAP = 0.60;
SEAM_OVERLAP = 6.40;
BARRIER_THICKNESS = 1.0;
BARRIER_CLEARANCE = 0.4;
BARRIER_GROOVE = BARRIER_THICKNESS + 2 * BARRIER_CLEARANCE;
BARRIER_HEIGHT = 46.0;
DC_BUSHING_DIAMETER = 8.0;
DC_BUNDLE_OD = 6.0;
DC_GLAND_CUTOUT_DIAMETER = 12.5;
DC_ROUTE_BEND_ENVELOPE = 10.0;
VENT_SLOT = min(1.6, 2 * NOZZLE_DIAMETER);
VENT_PITCH = 6.4;
SAFETY_DISTANCE = 8.0;
RAIL_STRUT = printable_at_least(1.6);

function enclosure_outer_min() = [190,160,0];
function enclosure_outer_max() = [322.8,288,60];
function enclosure_outer_size() = enclosure_outer_max()-enclosure_outer_min();
function enclosure_corner_radius() = 6;
function enclosure_base_wall_top() = 20;
function enclosure_hood_wall_bottom() = 20.2;
function enclosure_roof_bottom() = enclosure_outer_max().z-ROOF;
function enclosure_psu_origin() = [194,243.7,FLOOR];
function enclosure_psu_rotation() = [0,0,-90];
function enclosure_psu_keepout_min() = [194,166.2,FLOOR];
function enclosure_psu_keepout_max() = [304,243.7,FLOOR+36.86];
function enclosure_c14_origin() = [284,286,30];
function enclosure_c14_rotation_a() = [90,0,0];
function enclosure_c14_rotation_b() = [0,0,90];
function enclosure_c14_body_bounds() = [[260.57,264.2,16.5],[307.43,286,43.5]];
function enclosure_c14_faceplate_bounds() = [[258.85,286,14.5],[309.15,288,45.5]];
function enclosure_c14_terminal_bounds() = [[270,252.2,20],[298,264.2,40]];
function enclosure_partition_x() = [304,304+WALL];
function enclosure_partition_y() = [248.4,248.4+WALL];
function enclosure_barrier_x() = 318.2;
function enclosure_barrier_y() = [166.2,248.4];
function enclosure_barrier_z() = [FLOOR-2.0,FLOOR-2.0+BARRIER_HEIGHT];
function enclosure_groove_x() = [enclosure_barrier_x()-BARRIER_CLEARANCE,
                                  enclosure_barrier_x()+BARRIER_THICKNESS+BARRIER_CLEARANCE];
function enclosure_cassette_face_min() = [284-iecc14_faceplate_size().y/2-FRAME,
                                          30-iecc14_faceplate_size().x/2-FRAME];
function enclosure_cassette_face_max() = [284+iecc14_faceplate_size().y/2+FRAME,
                                          30+iecc14_faceplate_size().x/2+FRAME];
function enclosure_cassette_key_min_x() = enclosure_cassette_face_min().x-FRAME+KEY_UNION;
function enclosure_cassette_key_max_x() = enclosure_cassette_face_max().x+FRAME-KEY_UNION;
function enclosure_cassette_y() = [282.8,286];
function enclosure_cassette_key_y() = [278.8,enclosure_cassette_y().x+KEY_UNION];
function cassette_key_profile(side="left") = side=="left" ?
    [[enclosure_cassette_face_min().x+KEY_UNION,enclosure_cassette_key_y().y],
     [enclosure_cassette_face_min().x+2*KEY_UNION,enclosure_cassette_key_y().y],
     [enclosure_cassette_face_min().x+2*KEY_UNION,enclosure_cassette_key_y().x],
     [enclosure_cassette_key_min_x(),enclosure_cassette_key_y().x],
     [enclosure_cassette_key_min_x(),enclosure_cassette_key_y().y-FRAME]] :
    [[enclosure_cassette_face_max().x-KEY_UNION,enclosure_cassette_key_y().y],
     [enclosure_cassette_face_max().x-2*KEY_UNION,enclosure_cassette_key_y().y],
     [enclosure_cassette_face_max().x-2*KEY_UNION,enclosure_cassette_key_y().x],
     [enclosure_cassette_key_max_x(),enclosure_cassette_key_y().x],
     [enclosure_cassette_key_max_x(),enclosure_cassette_key_y().y-FRAME]];
function enclosure_front_fastener_x() = [215,300];
function enclosure_front_fastener_axis_y() = 163.8;
function enclosure_front_fastener_z() = 50.4;
function enclosure_front_post_root_y() = [162.4,166.0];
function enclosure_front_post_flare_z() = enclosure_psu_keepout_max().z+1.6;
function enclosure_fastener_outer_radius() = HOOD_NUT_AF/sqrt(3)+HOOD_NUT_RADIAL_CAPTURE;
function enclosure_fastener_stack() = HOOD_NUT_LEAD_DEPTH+HOOD_NUT_DEPTH+HOOD_NUT_BACKSTOP;
function enclosure_rail_x() = [318,322.8];
function enclosure_front_rail_y() = [141.73,170];
function enclosure_rear_rail_pad_y() = [[298,314],[322,338]];
function enclosure_rail_hole_yz() = [[149.73,10],[306,10],[330,10]];
function enclosure_print_bed() = [247,207];
function enclosure_base_print_size() = [338-141.73,322.8-190,enclosure_front_fastener_z()+enclosure_fastener_outer_radius()];
function enclosure_dc_bushing_centre() = [305.6,174,50];
function enclosure_gland_centre() = [270,160,50];

module enclosure_contract() {
    assert(NOZZLE_DIAMETER > 0, "NOZZLE_DIAMETER must be greater than zero");
    assert(WALL >= NOZZLE_DIAMETER && FLOOR >= NOZZLE_DIAMETER &&
           ROOF >= NOZZLE_DIAMETER && FRAME >= NOZZLE_DIAMETER &&
           RECEIVER_WALL >= NOZZLE_DIAMETER && POSITIVE_UNION >= NOZZLE_DIAMETER &&
           LOCAL_UNION >= NOZZLE_DIAMETER && KEY_UNION >= NOZZLE_DIAMETER,
           "Every intentional wall/positive structural connection must be at least one nozzle line");
    assert(WALL >= 3.2 && FRAME >= 4.0 && POSITIVE_UNION >= 3.2,
           "V2 broad structural unions must retain 3.2/4.0 mm minima");
    assert(IEC_SNAP_WALL == max(1.2,NOZZLE_DIAMETER),
           "C14 effective snap membrane must be max(1.2, NOZZLE_DIAMETER)");
    if (IEC_SNAP_WALL > 1.5)
        echo(str("WARNING: C14 snap membrane is ", IEC_SNAP_WALL,
                 " mm (>1.5 mm clip budget); owner-authorized sanding is required before fit qualification"));
    assert(enclosure_outer_min()==[190,160,0] && enclosure_outer_max()==[322.8,288,60],
           "V2 sealed envelope changed");
    assert(enclosure_outer_size().x<=132.8 && enclosure_outer_size().y<=128 &&
           enclosure_outer_size().z<=60, "V2 sealed envelope exceeds target");
    assert(enclosure_corner_radius()==6 && enclosure_base_wall_top()==20,
           "R6/base-wall contract changed");
    assert(enclosure_psu_origin()==[194,243.7,FLOOR] &&
           enclosure_psu_rotation()==[0,0,-90], "Approved V2 PSU transform changed");
    assert(alt1205t_upper_left_m3_centre()==[4.95,4.95] &&
           alt1205t_lower_left_m3_centre()==[6.75,98.6] &&
           alt1205t_m3_centres()==[[25.3,30.9],[25.3,67],[53.3,67]],
           "Physically accepted PSU hole pattern changed");
    assert(enclosure_c14_origin()==[284,286,30] &&
           iecc14_body_profile_size()==[27,46.86] &&
           iecc14_faceplate_size()==[31,50.3,2] && IEC_CLEARANCE==0.20,
           "Physically accepted horizontal C14 interface changed");
    assert(enclosure_c14_faceplate_bounds()[0].x>=enclosure_outer_min().x &&
           enclosure_c14_faceplate_bounds()[1].x<=enclosure_outer_max().x &&
           enclosure_c14_faceplate_bounds()[0].y>=enclosure_outer_min().y &&
           enclosure_c14_faceplate_bounds()[1].y<=enclosure_outer_max().y &&
           enclosure_c14_faceplate_bounds()[0].z>=0 &&
           enclosure_c14_faceplate_bounds()[1].z<=60,
           "C14 faceplate must remain entirely inside the sealed envelope");
    assert(enclosure_cassette_face_min()==[258.85-FRAME,14.5-FRAME] &&
           enclosure_cassette_face_max()==[309.15+FRAME,45.5+FRAME],
           "Cassette frame must derive from the exact faceplate plus FRAME");
    assert(enclosure_cassette_key_y().y-enclosure_cassette_y().x>=NOZZLE_DIAMETER-0.000001 &&
           KEY_UNION>=NOZZLE_DIAMETER-0.000001,
           "Cassette keys must share at least one nozzle line with the broad frame");
    assert(abs(enclosure_cassette_face_min().x+KEY_UNION-
                   enclosure_cassette_key_min_x()-FRAME)<0.000001 &&
           abs(enclosure_cassette_key_y().y-
                   (enclosure_cassette_key_y().y-FRAME)-FRAME)<0.000001,
           "Cassette key undersides must use matched 45-degree FRAME ramps");
    assert(enclosure_outer_max().z-enclosure_roof_bottom()>=NOZZLE_DIAMETER &&
           enclosure_outer_max().z-enclosure_roof_bottom()>=RECEIVER_WALL,
           "Cassette receivers and roof features need a broad positive roof union");
    assert(abs(BARRIER_GROOVE-1.8)<0.000001 &&
           norm(enclosure_groove_x()-[317.8,319.6])<0.000001,
           "Barrier groove must remain 1.8 mm with 0.4 mm per-side clearance");
    assert(enclosure_partition_y().x-enclosure_psu_keepout_max().y>=4.7-0.001,
           "Rear separation wall lost PSU clearance");
    assert(enclosure_c14_terminal_bounds()[0].y-enclosure_partition_y().y>=0.2-0.001,
           "C14 terminal projection lost separation-wall clearance");
    assert(enclosure_front_fastener_z()==50.4 && enclosure_fastener_stack()==6.0 &&
           HOOD_NUT_AF==5.60 && HOOD_NUT_DEPTH==2.80 &&
           HOOD_NUT_LEAD_AF==6.20 && HOOD_NUT_LEAD_DEPTH==0.80 &&
           HOOD_NUT_BACKSTOP>=2.4 && HOOD_NUT_RADIAL_CAPTURE>=2.4,
           "Qualified upper-plenum pressure-fit socket changed");
    assert(enclosure_front_post_flare_z()>=enclosure_psu_keepout_max().z+1.6,
           "Front posts may flare inward only 1.6 mm above the PSU");
    assert(enclosure_front_post_root_y().y<enclosure_psu_keepout_min().y,
           "Front-post root must remain ahead of the PSU keepout");
    assert(enclosure_front_fastener_z()+enclosure_fastener_outer_radius()<enclosure_roof_bottom(),
           "Front posts need explicit roof assembly clearance");
    assert(enclosure_rail_hole_yz()==[[149.73,10],[306,10],[330,10]],
           "Rail datums changed or retired Y=125.73 was restored");
    assert(len(enclosure_rear_rail_pad_y())==2 &&
           enclosure_front_rail_y()==[141.73,170] &&
           enclosure_rear_rail_pad_y()==[[298,314],[322,338]] &&
           enclosure_rear_rail_pad_y()[1].x-enclosure_rear_rail_pad_y()[0].y==8,
           "Rail attachment must be exactly three local pads with an 8 mm rear gap");
    assert(RAIL_STRUT>=1.6 && RAIL_STRUT>=NOZZLE_DIAMETER,
           "Each independent rear-rail load path needs a >=1.6 mm positive union");
    assert(enclosure_base_print_size().x<=enclosure_print_bed().x &&
           enclosure_base_print_size().y<=enclosure_print_bed().y,
           "Base does not fit the 247x207 bed in its declared rotation");
    assert(VENT_SLOT<=1.6, "Touch-resistant vent width exceeds 1.6 mm");
    echo(str("V2 nozzle=",NOZZLE_DIAMETER," wall=",WALL," frame=",FRAME,
             " snap=",IEC_SNAP_WALL," sealed=132.8x128x60 supports=OFF"));
    children();
}

module rounded_rect_2d(p=[0,0], q=[10,10], r=2) {
    translate([p.x+r,p.y+r])
        offset(r=r,$fn=48) square([q.x-p.x-2*r,q.y-p.y-2*r]);
}

module rounded_plate(p=[0,0], q=[10,10], r=2, z0=0, h=1) {
    translate([0,0,z0]) linear_extrude(height=h) rounded_rect_2d(p,q,r);
}

module rounded_ring(p=[0,0], q=[10,10], r=2, wall=WALL, z0=0, h=1) {
    translate([0,0,z0]) linear_extrude(height=h)
        difference() {
            rounded_rect_2d(p,q,r);
            rounded_rect_2d(p+[wall,wall],q-[wall,wall],max(0.2,r-wall));
        }
}

module hex_prism(af,h) { cylinder(r=af/sqrt(3),h=h,$fn=6); }

module in_psu_frame() {
    translate(enclosure_psu_origin()) rotate(enclosure_psu_rotation()) children();
}

module in_c14_frame() {
    translate(enclosure_c14_origin())
        rotate(enclosure_c14_rotation_a()) rotate(enclosure_c14_rotation_b()) children();
}

module psu_mount_negatives() {
    in_psu_frame() alt1205t_mounting_negatives(FLOOR,M3_CLEARANCE_DIAMETER,0.04);
    for (p=alt1205t_all_m3_centres()) {
        wp=[enclosure_psu_origin().x+p.y,enclosure_psu_origin().y-p.x];
        translate([wp.x,wp.y,FLOOR-PSU_NUT_DEPTH-0.01])
            hex_prism(PSU_NUT_AF,PSU_NUT_DEPTH+0.02);
    }
}

module rail_pad(y0,y1) {
    translate([enclosure_rail_x().x,y0,0])
        cube([enclosure_rail_x().y-enclosure_rail_x().x,y1-y0,20]);
}

module vertical_floor_strut(a,b,w=RAIL_STRUT) {
    // Constant-height hulls are vertical extrusions of their complete bed
    // footprint: no one-sided underside or bridge is introduced.
    hull() for (p=[a,b]) translate([p.x,p.y,0]) cube([w,w,20]);
}

module rear_rail_load_paths() {
    pads=enclosure_rear_rail_pad_y();
    for (span=pads) rail_pad(span.x,span.y);

    // Two genuinely independent floor-rooted paths replace the old rear
    // spine.  The farther path stays inboard until the first pad has ended.
    vertical_floor_strut([317,284.8],[318,298]);
    vertical_floor_strut([313.5,284.8],[313.5,315.6]);
    vertical_floor_strut([313.5,315.6],[318,322]);
}

module rail_mount_negatives() {
    for (p=enclosure_rail_hole_yz())
        translate([317.98,p.x,p.y]) rotate([0,90,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,h=4.84,$fn=36);
}

module barrier_floor_groove_negative() {
    translate([enclosure_groove_x().x,enclosure_barrier_y().x-0.4,FLOOR-2.2])
        cube([BARRIER_GROOVE,enclosure_barrier_y().y-enclosure_barrier_y().x+0.8,
              enclosure_barrier_z().y-(FLOOR-2.2)+0.1]);
}

module mains_selv_boundary() {
    union() {
        translate([enclosure_partition_x().x,enclosure_psu_keepout_min().y,FLOOR])
            cube([WALL,enclosure_partition_y().y-enclosure_psu_keepout_min().y+WALL,
                  enclosure_barrier_z().y-FLOOR]);
        translate([enclosure_partition_x().x,enclosure_partition_y().x,FLOOR])
            cube([enclosure_barrier_x()+BARRIER_THICKNESS-enclosure_partition_x().x,
                  WALL,enclosure_barrier_z().y-FLOOR]);
    }
}

module rear_hook(x) {
    // Bed-rooted locator: its inboard reach grows at less than 45 degrees.
    // The former y=284..284.8 horizontal underside has been removed.
    hull() {
        translate([x,284.8,17])
            cube([10,LOCAL_UNION,LOCAL_UNION]);
        translate([x,281.1,22.1-LOCAL_UNION])
            cube([10,LOCAL_UNION,LOCAL_UNION]);
    }
}

module front_post_outer(x) {
    r=enclosure_fastener_outer_radius();
    // Root stays wholly ahead of the PSU until its exact top + 1.6 mm.
    translate([x-r,enclosure_front_post_root_y().x,FLOOR])
        cube([2*r,enclosure_front_post_root_y().y-enclosure_front_post_root_y().x,
              enclosure_front_post_flare_z()-FLOOR]);
    // 45-degree floor-down flare supports the inward socket/backstop depth.
    translate([x-4.2,enclosure_front_post_root_y().y-LOCAL_UNION,
               enclosure_front_post_flare_z()-LOCAL_UNION])
        rotate([90,0,90]) linear_extrude(height=8.4)
            polygon([[0,0],[4.6,4.6],[4.6,8.8],[0,8.8]]);
    translate([x,enclosure_front_fastener_axis_y(),enclosure_front_fastener_z()])
        rotate([-90,0,0]) cylinder(r=r,h=HOOD_NUT_LEAD_DEPTH+HOOD_NUT_DEPTH,$fn=48);
    // Backstop narrows only after the hex pocket while retaining 2.4 mm
    // radial material around the screw bore.
    translate([x,enclosure_front_fastener_axis_y()+HOOD_NUT_LEAD_DEPTH+HOOD_NUT_DEPTH,
               enclosure_front_fastener_z()])
        rotate([-90,0,0]) cylinder(r=M3_CLEARANCE_DIAMETER/2+HOOD_NUT_RADIAL_CAPTURE,
                                   h=HOOD_NUT_BACKSTOP,$fn=48);
}

module front_post_negative(x) {
    translate([x,enclosure_front_fastener_axis_y()-0.02,enclosure_front_fastener_z()])
        rotate([-90,0,0]) hex_prism(HOOD_NUT_LEAD_AF,HOOD_NUT_LEAD_DEPTH+0.04);
    translate([x,enclosure_front_fastener_axis_y()+HOOD_NUT_LEAD_DEPTH-0.01,
               enclosure_front_fastener_z()])
        rotate([-90,0,0]) hex_prism(HOOD_NUT_AF,HOOD_NUT_DEPTH+0.02);
    translate([x,159.8,enclosure_front_fastener_z()]) rotate([-90,0,0])
        cylinder(d=M3_CLEARANCE_DIAMETER,h=10.05,$fn=36);
}

module front_fastener_structure() {
    for (x=enclosure_front_fastener_x()) front_post_outer(x);
}

module front_screw_sweep() {
    // A 0.05 mm radial proof margin avoids counting the intended bore skin.
    for (x=enclosure_front_fastener_x())
        translate([x,152,enclosure_front_fastener_z()]) rotate([-90,0,0])
            cylinder(d=M3_CLEARANCE_DIAMETER-0.1,h=18,$fn=36);
}

module front_tool_sweep() {
    // Driver body remains wholly outside the sealed wall; only the screw
    // continues through the dedicated clearance bore.
    for (x=enclosure_front_fastener_x())
        translate([x,151.5,enclosure_front_fastener_z()]) rotate([-90,0,0])
            cylinder(d=10,h=8.2,$fn=36);
}

module front_nut_loading_sweep() {
    // With the hood removed the qualified 6.20 AF lead is directly
    // approachable from the open front side of each upper-plenum post.
    for (x=enclosure_front_fastener_x())
        translate([x,159.8,enclosure_front_fastener_z()]) rotate([-90,0,0])
            hex_prism(HOOD_NUT_LEAD_AF,
                      enclosure_front_fastener_axis_y()-159.8-0.01);
}

module cassette_base_seat() {
    // The broad floor-rooted ledge supports the cassette at Z=10.5. The hood
    // stop later captures it; there is no blind pocket or support cavity.
    translate([enclosure_cassette_key_min_x()-0.3,278.5,FLOOR])
        cube([enclosure_cassette_key_max_x()-enclosure_cassette_key_min_x()+0.6,
              9.5,6.2]);
}

module base_wall_openings() {
    // Cassette opens at the rear without any outboard protrusion.
    translate([enclosure_cassette_face_min().x-0.3,284.4,10.2])
        cube([enclosure_cassette_face_max().x-enclosure_cassette_face_min().x+0.6,
              3.61,10.1]);
}

module enclosure_base_installed() {
    enclosure_contract()
    difference() {
        union() {
            difference() {
                union() {
                    rounded_plate(enclosure_outer_min(),enclosure_outer_max(),
                                  enclosure_corner_radius(),0,FLOOR);
                    rounded_ring(enclosure_outer_min(),enclosure_outer_max(),
                                 enclosure_corner_radius(),WALL,FLOOR,
                                 enclosure_base_wall_top()-FLOOR);
                }
                base_wall_openings();
            }
            mains_selv_boundary();
            cassette_base_seat();
            rail_pad(enclosure_front_rail_y().x,enclosure_front_rail_y().y);
            rear_rail_load_paths();
            for (x=enclosure_front_fastener_x()) front_post_outer(x);
            rear_hook(200); rear_hook(230);
        }
        psu_mount_negatives();
        barrier_floor_groove_negative();
        rail_mount_negatives();
        // Assembly-clearance notch where the roof-rooted right cassette
        // receiver passes the otherwise local rear rail pad.
        translate([317.7,277.9,enclosure_hood_wall_bottom()-SEAM_OVERLAP-0.3])
            cube([3.0,6.6,SEAM_OVERLAP+0.4]);
        for (x=enclosure_front_fastener_x()) front_post_negative(x);
        translate([303.8,enclosure_dc_bushing_centre().y,
                   enclosure_dc_bushing_centre().z]) rotate([0,90,0])
            cylinder(d=DC_BUSHING_DIAMETER,h=WALL+0.4,$fn=48);
    }
}

module hood_seam_lip() {
    z0=enclosure_hood_wall_bottom()-SEAM_OVERLAP;
    front_lip_y=enclosure_outer_min().y+WALL+SEAM_GAP;
    rear_lip_y=enclosure_outer_max().y-2*WALL-SEAM_GAP;
    left_lip_x=enclosure_outer_min().x+WALL+SEAM_GAP;
    ramp_root_z=enclosure_hood_wall_bottom()+4.6;
    ramp_tip_z=enclosure_hood_wall_bottom()-LOCAL_UNION;

    module front_or_rear_segment(x0,length,rear=false) {
        lip_y=rear ? rear_lip_y : front_lip_y;
        root_y=rear ? enclosure_outer_max().y-WALL :
                      enclosure_outer_min().y+WALL-LOCAL_UNION;
        union() {
            translate([x0,lip_y,z0]) cube([length,WALL,SEAM_OVERLAP]);
            // In roof-down orientation the one-nozzle root prints first and
            // expands to the inset lip over 4.6 mm: every free face <=45°.
            hull() {
                translate([x0,root_y,ramp_root_z])
                    cube([length,LOCAL_UNION,LOCAL_UNION]);
                translate([x0,lip_y,ramp_tip_z])
                    cube([length,WALL,LOCAL_UNION]);
            }
        }
    }

    for (seg=[[196,12.0],[222,71],[307.8,9.0]])
        front_or_rear_segment(seg.x,seg.y,false);
    for (seg=[[196,3.4],[210.6,18.8],[240.6,9.65]])
        front_or_rear_segment(seg.x,seg.y,true);

    union() {
        translate([left_lip_x,167,z0]) cube([WALL,114,SEAM_OVERLAP]);
        hull() {
            translate([enclosure_outer_min().x+WALL-LOCAL_UNION,167,ramp_root_z])
                cube([LOCAL_UNION,114,LOCAL_UNION]);
            translate([left_lip_x,167,ramp_tip_z])
                cube([WALL,114,LOCAL_UNION]);
        }
    }
}

module cassette_receiver_block(side="left") {
    xmin=side=="left" ? enclosure_cassette_key_min_x()-RECEIVER_WALL :
                         enclosure_cassette_face_max().x-KEY_UNION-0.3;
    xmax=side=="left" ? enclosure_cassette_face_min().x+KEY_UNION+0.3 :
                         enclosure_cassette_key_max_x()+RECEIVER_WALL;
    difference() {
        union() {
            // The front key reaction wall is a full receiver wall.  Above the
            // base/hood seam, the rear reaction wall grows into the complete
            // 3.2 mm rear shell rather than relying on a thin local tab.
            translate([xmin,275.3,enclosure_hood_wall_bottom()-SEAM_OVERLAP])
                cube([xmax-xmin,8.9,
                      enclosure_outer_max().z-(enclosure_hood_wall_bottom()-SEAM_OVERLAP)]);
            translate([xmin,284.2,enclosure_hood_wall_bottom()+SEAM_GAP])
                cube([xmax-xmin,3.8,
                      enclosure_outer_max().z-(enclosure_hood_wall_bottom()+SEAM_GAP)]);
        }
        // Matched dovetail is open at the hood lower edge.  offset() gives
        // true 0.30 mm normal clearance around every 45-degree key face.
        cassette_keyway_sweep(side);
        translate([enclosure_cassette_face_min().x-0.3,
                   282.5,enclosure_hood_wall_bottom()-SEAM_OVERLAP-0.01])
            cube([enclosure_cassette_face_max().x-
                      enclosure_cassette_face_min().x+0.6,
                  3.8,
                  enclosure_cassette_face_max().y-(enclosure_hood_wall_bottom()-SEAM_OVERLAP)+0.31]);
    }
}

module cassette_keyway_sweep(side="left") {
    z0=enclosure_hood_wall_bottom()-SEAM_OVERLAP-0.01;
    z1=enclosure_c14_faceplate_bounds()[1].z+0.5+0.3;
    translate([0,0,z0]) linear_extrude(height=z1-z0)
        offset(delta=0.3,chamfer=true) polygon(points=cassette_key_profile(side));
}

module cassette_key_insertion_sweep(side="left") {
    // Physical key silhouette swept from the open hood edge to the installed
    // stop.  The receiver subtracts the separate +0.30 mm normal envelope.
    z0=enclosure_hood_wall_bottom()-SEAM_OVERLAP;
    z1=enclosure_c14_faceplate_bounds()[1].z+0.5;
    translate([0,0,z0]) linear_extrude(height=z1-z0)
        polygon(points=cassette_key_profile(side));
}

module hood_openings() {
    // Rear cassette assembly opening, including its 0.30 mm running clearance.
    translate([enclosure_cassette_face_min().x-0.3,284.4,
               enclosure_cassette_face_min().y-0.3])
        cube([enclosure_cassette_face_max().x-enclosure_cassette_face_min().x+0.6,
              3.61,enclosure_cassette_face_max().y-enclosure_cassette_face_min().y+0.6]);
    // Only vertical <=1.6 mm slots: no former 72 mm unsupported ceilings.
    for (x=[231:VENT_PITCH:282])
        translate([x-VENT_SLOT/2,159.9,42]) cube([VENT_SLOT,WALL+0.2,11]);
    for (x=enclosure_front_fastener_x())
        translate([x,159.8,enclosure_front_fastener_z()]) rotate([-90,0,0])
            cylinder(d=M3_CLEARANCE_DIAMETER,h=WALL+4.8,$fn=36);
    translate([enclosure_gland_centre().x,159.8,enclosure_gland_centre().z])
        rotate([-90,0,0]) cylinder(d=DC_GLAND_CUTOUT_DIAMETER,h=WALL+0.4,$fn=48);
    // Clear the front shell around each base post; the separate local cap
    // below closes the nut mouth with 0.30 mm assembly clearance.
    for (x=enclosure_front_fastener_x())
        translate([x-enclosure_fastener_outer_radius()-0.3,162.1,19.9])
            cube([2*enclosure_fastener_outer_radius()+0.6,1.4,36.5]);
}

module roof_baffle() {
    // Roof-rooted <=45-degree drip/light baffle behind the front slots.
    for (span=[[228,35],[277,9]])
        translate([span.x,0,0]) rotate([90,0,90]) linear_extrude(height=span.y)
            polygon([[163.2,enclosure_roof_bottom()+LOCAL_UNION],
                     [169.6,enclosure_roof_bottom()+LOCAL_UNION],
                     [169.6,enclosure_roof_bottom()-6.4],
                     // Cross the roof plane by a full nozzle line rather
                     // than ending tangent to it.  Besides guaranteeing a
                     // printable root, this avoids a non-manifold T-edge in
                     // quantized STL consumers.
                     [163.2,enclosure_roof_bottom()-LOCAL_UNION]]);
}

module roof_open_cleats() {
    // Roof-down vertical tabs locate one side of the DC bundle while leaving
    // the other side completely open to fingers/pliers during service.
    for (x=[280,292])
        translate([x,177.5,47.2]) cube([WALL,2.0,enclosure_outer_max().z-47.2]);
}

module barrier_roof_compression_rib() {
    translate([enclosure_barrier_x()-0.8,enclosure_barrier_y().x,
               enclosure_barrier_z().y+0.4])
        cube([BARRIER_THICKNESS+1.6,
              enclosure_barrier_y().y-enclosure_barrier_y().x,
              enclosure_roof_bottom()-(enclosure_barrier_z().y+0.4)+LOCAL_UNION]);
}

module enclosure_hood_installed() {
    enclosure_contract()
    difference() {
        union() {
            difference() {
                union() {
                    rounded_ring(enclosure_outer_min(),enclosure_outer_max(),
                                 enclosure_corner_radius(),WALL,
                                 enclosure_hood_wall_bottom(),
                                 enclosure_roof_bottom()-enclosure_hood_wall_bottom());
                    rounded_plate(enclosure_outer_min(),enclosure_outer_max(),
                                  enclosure_corner_radius(),enclosure_roof_bottom(),ROOF);
                }
                hood_openings();
            }
            hood_seam_lip();
            cassette_receiver_block("left");
            cassette_receiver_block("right");
            roof_baffle();
            roof_open_cleats();
            barrier_roof_compression_rib();
            // Local front caps retain the loaded nuts while preserving screw access.
            for (x=enclosure_front_fastener_x())
                difference() {
                    translate([x-6,160,44])
                        cube([12,enclosure_front_fastener_axis_y()-0.3-160,12.4]);
                    translate([x,159.8,enclosure_front_fastener_z()]) rotate([-90,0,0])
                        cylinder(d=M3_CLEARANCE_DIAMETER,h=4,$fn=36);
                }
        }
        // The rear hook ramps remain outside the lip with 0.5 mm installed
        // clearance; no blind receiver or inaccessible support is required.
    }
}

module cassette_relief_negative() {
    // Back-relief leaves exactly the effective snap membrane at the front.
    translate([enclosure_c14_faceplate_bounds()[0].x,
               enclosure_cassette_y().x-0.01,
               enclosure_c14_faceplate_bounds()[0].z])
        cube([iecc14_faceplate_size().y,
              enclosure_cassette_y().y-enclosure_cassette_y().x-IEC_SNAP_WALL+0.01,
              iecc14_faceplate_size().x]);
}

module cassette_key(side="left") {
    translate([0,0,enclosure_c14_faceplate_bounds()[0].z-0.5])
        linear_extrude(height=iecc14_faceplate_size().x+1.0)
            polygon(points=cassette_key_profile(side));
}

module enclosure_c14_cassette_installed() {
    enclosure_contract()
    difference() {
        union() {
            translate([enclosure_cassette_face_min().x,enclosure_cassette_y().x,
                       enclosure_cassette_face_min().y])
                cube([enclosure_cassette_face_max().x-enclosure_cassette_face_min().x,
                      enclosure_cassette_y().y-enclosure_cassette_y().x,
                      enclosure_cassette_face_max().y-enclosure_cassette_face_min().y]);
            cassette_key("left"); cassette_key("right");
        }
        cassette_relief_negative();
        in_c14_frame() iecc14_panel_cutout_negative(4.0,IEC_CLEARANCE);
    }
}

module barrier_plate_keepout() {
    translate([enclosure_barrier_x(),enclosure_barrier_y().x,enclosure_barrier_z().x])
        cube([BARRIER_THICKNESS,enclosure_barrier_y().y-enclosure_barrier_y().x,
              enclosure_barrier_z().y-enclosure_barrier_z().x]);
}

module dc_route_keepout() {
    points=[[312,174,50],[305.6,174,50],[270,174,50],[270,164,50],[270,157,50]];
    for(i=[0:len(points)-2]) hull() for(p=[points[i],points[i+1]])
        translate(p) sphere(d=DC_BUNDLE_OD,$fn=24);
    for(p=[[270,174,50],[270,164,50]])
        translate(p) sphere(d=DC_ROUTE_BEND_ENVELOPE,$fn=24);
}

module ac_service_keepout() {
    points=[[312,240,36],[312,244,52],[312,256,52],[312,260,36]];
    for(i=[0:len(points)-2]) hull() for(p=[points[i],points[i+1]])
        translate(p) sphere(d=8,$fn=24);
}

module pe_lug_route_keepout() {
    points=[[311.5,238,37],[311.5,244,52],[311.5,258,52],[306,268,48]];
    for(i=[0:len(points)-2]) hull() for(p=[points[i],points[i+1]])
        translate(p) sphere(d=7,$fn=24);
}

module c14_terminal_keepout() {
    p=enclosure_c14_terminal_bounds()[0]; q=enclosure_c14_terminal_bounds()[1];
    translate(p) cube(q-p);
}

module cassette_insertion_path_keepout() {
    // Exact face/key silhouettes swept from the hood's open lower edge to the
    // installed stop. Receiver clearance is 0.30 mm normal to every face.
    union() {
        translate([enclosure_cassette_face_min().x,enclosure_cassette_y().x,
                   enclosure_hood_wall_bottom()-SEAM_OVERLAP])
            cube([enclosure_cassette_face_max().x-enclosure_cassette_face_min().x,
                  enclosure_cassette_y().y-enclosure_cassette_y().x,
                  enclosure_cassette_face_max().y-
                      (enclosure_hood_wall_bottom()-SEAM_OVERLAP)]);
        cassette_key_insertion_sweep("left");
        cassette_key_insertion_sweep("right");
    }
}

module installed_printed_assembly() {
    enclosure_base_installed(); enclosure_hood_installed(); enclosure_c14_cassette_installed();
}

module rendered_printed_assembly() {
    // Evidence scenes force each printable part through CGAL independently.
    // This removes OpenCSG epsilon/occlusion artifacts without unioning away
    // component colors or hiding the physical three-part split.
    render(convexity=20) enclosure_base_installed();
    render(convexity=20) enclosure_hood_installed();
    render(convexity=20) enclosure_c14_cassette_installed();
}

module installed_components() {
    color([0.62,0.65,0.68]) in_psu_frame() alt1205t_keepout();
    color([0.08,0.09,0.10]) in_c14_frame() iecc14_complete_rest_state_keepout();
    color([0.88,0.55,0.12,0.55]) c14_terminal_keepout();
    color([0.8,0.76,0.25,0.65]) barrier_plate_keepout();
    color([0.15,0.55,0.9,0.45]) dc_route_keepout();
}

module exploded_scene() {
    color([0.18,0.48,0.78]) render(convexity=20) enclosure_base_installed();
    color([0.80,0.82,0.86]) translate([0,0,20])
        render(convexity=20) enclosure_hood_installed();
    color([0.92,0.55,0.12]) translate([0,16,0])
        render(convexity=20) enclosure_c14_cassette_installed();
    installed_components();
}

module cassette_section_scene() {
    p=[248,276,8]; q=[321,290,52];
    color([0.18,0.48,0.78]) render(convexity=20) intersection() {
        enclosure_base_installed(); translate(p) cube(q-p);
    }
    color([0.80,0.82,0.86]) render(convexity=20) intersection() {
        enclosure_hood_installed(); translate(p) cube(q-p);
    }
    color([0.92,0.55,0.12]) render(convexity=20) intersection() {
        enclosure_c14_cassette_installed(); translate(p) cube(q-p);
    }
    color([0.08,0.09,0.10]) render(convexity=20) intersection() {
        in_c14_frame() iecc14_complete_rest_state_keepout();
        translate(p) cube(q-p);
    }
}

module barrier_seam_section_scene() {
    p=[300,200,0]; q=[323,208,60];
    color([0.18,0.48,0.78]) render(convexity=20) intersection() {
        enclosure_base_installed(); translate(p) cube(q-p);
    }
    color([0.80,0.82,0.86]) render(convexity=20) intersection() {
        enclosure_hood_installed(); translate(p) cube(q-p);
    }
    color([0.92,0.55,0.12]) render(convexity=20) intersection() {
        barrier_plate_keepout(); translate(p) cube(q-p);
    }
}

module front_fastener_hook_section_scene() {
    fp=[208,158,0]; fq=[222,172,58];
    hp=[195,278,12]; hq=[240,290,27];
    color([0.18,0.48,0.78]) render(convexity=20) intersection() {
        enclosure_base_installed(); translate(fp) cube(fq-fp);
    }
    color([0.80,0.82,0.86]) render(convexity=20) intersection() {
        enclosure_hood_installed(); translate(fp) cube(fq-fp);
    }
    color([0.2,0.75,0.35,0.55]) render(convexity=20) intersection() {
        front_nut_loading_sweep(); translate(fp) cube(fq-fp);
    }
    color([0.18,0.48,0.78]) render(convexity=20) intersection() {
        enclosure_base_installed(); translate(hp) cube(hq-hp);
    }
    color([0.80,0.82,0.86]) render(convexity=20) intersection() {
        enclosure_hood_installed(); translate(hp) cube(hq-hp);
    }
}

module support_risk_scene() {
    color([0.18,0.48,0.78]) render(convexity=20) enclosure_base_installed();
    color([0.82,0.84,0.88,0.55]) render(convexity=20) enclosure_hood_installed();
    color([0.95,0.5,0.1]) translate([-28,0,0])
        render(convexity=20) front_post_outer(enclosure_front_fastener_x().x);
    color([0.2,0.75,0.35]) translate([0,150,0])
        render(convexity=20) roof_baffle();
}

module old_size_reference() {
    color([0.85,0.18,0.15,0.12]) translate([190,160,0]) cube([136,140,78]);
    color([0.18,0.55,0.85,0.55]) rendered_printed_assembly();
}

module base_print_orientation() {
    translate([338,-190,0]) rotate([0,0,90]) enclosure_base_installed();
}

module hood_print_orientation() {
    translate([-190,288,60]) rotate([180,0,0]) enclosure_hood_installed();
}

module cassette_print_orientation() {
    translate([-enclosure_cassette_key_min_x(),-enclosure_cassette_face_min().y,286])
        rotate([-90,0,0]) enclosure_c14_cassette_installed();
}

enclosure_contract() {
    if (PART=="base") base_print_orientation();
    else if (PART=="hood") hood_print_orientation();
    else if (PART=="cassette") cassette_print_orientation();
    else if (PART=="assembly") rendered_printed_assembly();
    else if (PART=="installed_preview") { rendered_printed_assembly(); installed_components(); }
    else if (PART=="exploded") exploded_scene();
    else if (PART=="open_top") {
        render(convexity=20) enclosure_base_installed();
        render(convexity=20) enclosure_c14_cassette_installed();
        installed_components();
    }
    else if (PART=="rear") { rendered_printed_assembly(); installed_components(); }
    else if (PART=="cassette_section") cassette_section_scene();
    else if (PART=="barrier_seam_section") barrier_seam_section_scene();
    else if (PART=="front_fastener_hook_section") front_fastener_hook_section_scene();
    else if (PART=="support_risk") support_risk_scene();
    else if (PART=="print_orientations") {
        base_print_orientation(); translate([0,142,0]) hood_print_orientation();
        translate([140,142,0]) cassette_print_orientation();
    }
    else if (PART=="size_comparison") old_size_reference();
    else if (PART=="barrier_template")
        square([enclosure_barrier_y().y-enclosure_barrier_y().x,
                enclosure_barrier_z().y-enclosure_barrier_z().x]);
    else if (PART=="partition_slice") intersection() {
        mains_selv_boundary(); translate([300,160,20]) cube([20,100,1]);
    }
    else if (PART=="dc_route") dc_route_keepout();
    else if (PART=="base_hood_intersection") intersection() {
        enclosure_base_installed(); enclosure_hood_installed();
    }
    else if (PART=="base_psu_intersection") intersection() {
        enclosure_base_installed(); in_psu_frame() alt1205t_keepout();
    }
    else if (PART=="c14_print_intersection") intersection() {
        installed_printed_assembly(); in_c14_frame() iecc14_complete_rest_state_keepout();
    }
    else if (PART=="c14_terminal_intersection") intersection() {
        installed_printed_assembly(); c14_terminal_keepout();
    }
    else if (PART=="ac_service_intersection") intersection() {
        installed_printed_assembly(); ac_service_keepout();
    }
    else if (PART=="pe_route_intersection") intersection() {
        installed_printed_assembly(); pe_lug_route_keepout();
    }
    else if (PART=="dc_route_intersection") intersection() {
        installed_printed_assembly(); dc_route_keepout();
    }
    else if (PART=="barrier_intersection") intersection() {
        installed_printed_assembly(); barrier_plate_keepout();
    }
    else if (PART=="cassette_insertion_intersection") intersection() {
        enclosure_hood_installed(); cassette_insertion_path_keepout();
    }
    else if (PART=="cassette_hood_intersection") intersection() {
        enclosure_c14_cassette_installed(); enclosure_hood_installed();
    }
    else if (PART=="cassette_base_intersection") intersection() {
        enclosure_c14_cassette_installed(); enclosure_base_installed();
    }
    else if (PART=="front_fastener_keepout_intersection") union() {
        intersection() { front_fastener_structure(); in_psu_frame() alt1205t_keepout(); }
        intersection() { front_fastener_structure(); in_c14_frame() iecc14_complete_rest_state_keepout(); }
        intersection() { front_fastener_structure(); c14_terminal_keepout(); }
        intersection() { front_fastener_structure(); ac_service_keepout(); }
        intersection() { front_fastener_structure(); pe_lug_route_keepout(); }
        intersection() { front_fastener_structure(); dc_route_keepout(); }
        intersection() { front_fastener_structure(); barrier_plate_keepout(); }
        intersection() { front_fastener_structure(); cassette_insertion_path_keepout(); }
    }
    else if (PART=="front_fastener_service_intersection") union() {
        intersection() { installed_printed_assembly(); front_screw_sweep(); }
        intersection() { installed_printed_assembly(); front_tool_sweep(); }
        intersection() { enclosure_base_installed(); front_nut_loading_sweep(); }
    }
    else if (PART=="rear_hook_intersection") intersection() {
        union() { rear_hook(200); rear_hook(230); }
        enclosure_hood_installed();
    }
    else assert(false,str("Unknown PART selector: ",PART));
}
