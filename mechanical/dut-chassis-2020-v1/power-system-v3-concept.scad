/* Layout study, not a qualified print or electrical enclosure.
 * Coordinates: local +Y rearward, +Z up; installed origin [178,156,0].
 * Keep measured component models separate from this new enclosure architecture.
 */
use <lib/alt-1205t-power-supply.scad>
use <lib/iec-c14-fused-switch.scad>
use <pocketforge-node-chassis-usb-c.scad>

PART = is_undef(PART) ? "assembly" : PART;
$fn = 48;
W = 148;
D = 144;
H = 96;
WALL = 4;
FLOOR = 4;
LID = 4;
SNAP = 1.2;
FIT = 0.20;
JOINT = 0.4;
ORIGIN = [178,156,0];
// Keep the proven lateral offset. Raise the inlet above the PSU to admit
// the owner-authorized 35 mm generic connection allowance behind its body.
IEC_CENTRE = [W/2-11,68]; // panel X / installed Z
PSU_ORIGIN = [8,91.5,8];
RIGHT_MOUNTS = [149.73-ORIGIN.y,306-ORIGIN.y];
REAR_RAIL = 338-ORIGIN.y;
REAR_MOUNT_X = 24;
PANEL_X = [16,W-16];
PANEL_Z = [30,84]; // lower drivers also clear the 24 mm rear mounting pad
LID_POINTS = [[12,7],[W-12,7],[16,126],[W-16,126]];

assert(WALL >= 4 && FLOOR >= 4);
assert(SNAP == 1.2 && FIT == 0.20);
assert(IEC_CENTRE.y-31/2-FLOOR >= 10);
assert(H-(IEC_CENTRE.y+31/2) >= 10);
assert(min(IEC_CENTRE.x-50.3/2,W-IEC_CENTRE.x-50.3/2) >= 35);
assert(ORIGIN.x+W == 326 && ORIGIN.y+REAR_RAIL == 338);

module hex_pocket(af,depth) {
    cylinder(d=af/cos(30),h=depth,$fn=6);
}
module round_plan(w,d,r=4) {
    // Front corners round; the separate flat rear panel has square returns.
    union() {
        translate([0,r]) square([w,d-r]);
        translate([r,0]) square([w-2*r,r]);
        for(x=[r,w-r]) translate([x,r]) circle(r=r);
    }
}
module skirt_outline() {
    // Step around front fastener pillars, so the overlap never cuts a nut
    // pocket. Rear fasteners sit clear of the ordinary side overlap.
    polygon([[4.4,12.4],[20.4,12.4],[20.4,4.4],[W-20.4,4.4],
             [W-20.4,12.4],[W-4.4,12.4],[W-4.4,D-4.4],[4.4,D-4.4]]);
}
module skirt_profile() {
    difference() { skirt_outline(); offset(delta=-3.2) skirt_outline(); }
}
module psu_transform() {
    translate(PSU_ORIGIN) rotate([0,0,-90]) children();
}
module panel_transform() {
    translate([0,D,0]) rotate([90,0,0]) children();
}
module inlet_transform() {
    panel_transform() translate([IEC_CENTRE.x,IEC_CENTRE.y,0])
        rotate([0,0,90]) children();
}
function psu_hole(p) = [PSU_ORIGIN.x+p.y,PSU_ORIGIN.y-p.x];

// Full rear panel, printed exterior-face-down. Only the small seating island
// is thin. Its surrounding frame and overlaps are integral, positive solids.
module rear_panel_flat() {
    difference() {
        union() {
            translate([0,FLOOR,0]) cube([W,H-FLOOR,WALL]);
            // Broad U-shaped internal overlap, clear of tray walls by JOINT.
            for(x=[WALL+JOINT,W-2*WALL-JOINT])
                translate([x,FLOOR+JOINT,3.2]) cube([WALL,H-8.4-4,6.8]);
            translate([WALL+JOINT,FLOOR+JOINT,3.2])
                cube([W-2*(WALL+JOINT),WALL,6.8]);
        }
        translate([IEC_CENTRE.x,IEC_CENTRE.y,-0.02]) rotate([0,0,90])
            iecc14_panel_cutout_negative(depth=12,clearance=FIT);
        // Rear relief leaves an uninterrupted 1.2 mm membrane under the
        // complete faceplate footprint, with 1 mm extra clip working space.
        translate([IEC_CENTRE.x-26.15,IEC_CENTRE.y-16.5,SNAP])
            cube([52.3,33,12]);
        for(x=PANEL_X,z=PANEL_Z)
            translate([x,z,-0.02]) cylinder(d=3.6,h=12);
    }
}
module rear_panel() { panel_transform() rear_panel_flat(); }

// Right rail ears grow from the sidewall and floor. Positive slot keys
// resist rotation; they use the measured 6.73 mm rail opening.
module right_ear(y,front=false) {
    lo = front ? y-10 : D+0.4;
    hi = front ? 12 : y+10;
    difference() {
        union() {
            translate([W-8,lo,0]) cube([8,hi-lo,20]);
            translate([W-16,front?lo:D-14,0]) cube([16,front?hi-lo:hi-D+14,4]);
            translate([W-1,y-5,6.9]) cube([3.4,10,6.2]);
        }
        translate([W-18,y,10]) rotate([0,90,0]) cylinder(d=3.6,h=22);
    }
}
module rear_brace() {
    difference() {
        union() {
            translate([REAR_MOUNT_X-12,D-12,0]) cube([24,12,4]);
            translate([REAR_MOUNT_X-12,D-0.8,0]) cube([24,REAR_RAIL-D+0.8,4]);
            translate([REAR_MOUNT_X-12,REAR_RAIL-18,0]) cube([24,18,20]);
            for(x=[REAR_MOUNT_X-12,REAR_MOUNT_X+8])
                hull() {
                    translate([x,D,0]) cube([4,1,4]);
                    translate([x,REAR_RAIL-18,0]) cube([4,8,20]);
                }
        }
        for(x=[REAR_MOUNT_X-8,REAR_MOUNT_X+8]) {
            translate([x,REAR_RAIL-14,17.2]) hex_pocket(5.6,3);
            translate([x,REAR_RAIL-14,13]) cylinder(d=3.6,h=8);
        }
    }
}
// Separate top bridge prints broad face down: the rail key grows upward,
// removing the inaccessible underside overhang from the large tray.
module rail_bridge() {
    difference() {
        union() {
            translate([REAR_MOUNT_X-12,REAR_RAIL-18,20]) cube([24,34,4]);
            translate([REAR_MOUNT_X-7,REAR_RAIL+6.9,17.6]) cube([14,6.2,3.2]);
        }
        for(p=[[REAR_MOUNT_X-8,REAR_RAIL-14],
               [REAR_MOUNT_X+8,REAR_RAIL-14],
               [REAR_MOUNT_X,REAR_RAIL+10]])
            translate([p.x,p.y,16]) cylinder(d=3.6,h=10);
    }
}
// Lower front intake: offset slots in two vertical walls, with substantial
// ribs connecting the inner baffle. Eight mm bridges when upright.
module intake_baffle() {
    difference() {
        union() {
            translate([28,8,4]) cube([80,3.2,32]);
            for(x=[28:16:108]) translate([x-1.6,3.2,4]) cube([3.2,8,32]);
        }
        for(x=[32:16:96],z=[14,26])
            translate([x,7.9,z]) cube([8,3.4,2.4]);
    }
}
module roof_baffle() {
    difference() {
        union() {
            translate([24,24,H-10.4]) cube([84,54,3.2]);
            for(x=[24:12:108]) translate([x-1.6,24,H-10.4]) cube([3.2,54,11.4]);
            for(y=[24,74.8]) translate([24,y,H-10.4]) cube([84,3.2,11.4]);
            // In roof-down orientation these 45-degree corbels grow from
            // both ribs, replacing the former 8.8 mm horizontal ceilings.
            for(x=[25.6:12:97.6])
                translate([x,78,0]) rotate([90,0,0]) linear_extrude(54) {
                    polygon([[0,H-7.3],[4.5,H-7.3],[0,H-2.8]]);
                    polygon([[4.3,H-7.3],[8.8,H-7.3],[8.8,H-2.8]]);
                }
        }
        // Slots offset 6 mm from outer vents; cut through the corbels too.
        // Small 2.4 mm slot edges remain short, accessible bridges.
        for(x=[27.2:12:99.2],y=[36,48,60,72])
            translate([x,y,H-10.5]) cube([5.6,2.4,10.5]);
    }
}

module tray() {
    difference() {
        union() {
            linear_extrude(FLOOR) round_plan(W,D);
            // Three tall walls; full rear panel closes the fourth side.
            intersection() {
                linear_extrude(H) round_plan(W,D);
                union() {
                    cube([W,WALL,H]);
                    cube([WALL,D-WALL,H]);
                    translate([W-WALL,0,0]) cube([WALL,D-WALL,H]);
                }
            }
            for(p=alt1205t_all_m3_centres())
                translate(concat(psu_hole(p),[3.2])) cylinder(d=12,h=4.8);
            // Front lid pillars are outside the PSU footprint.
            intersection() {
                linear_extrude(H) round_plan(W,D);
                for(x=[0,W-20]) translate([x,0,0]) cube([20,12,H]);
            }
            // Rear blocks support both lid and rear-panel fasteners.
            for(x=[0,W-24]) translate([x,118,0]) cube([24,22,H]);
            right_ear(RIGHT_MOUNTS[0],true);
            right_ear(RIGHT_MOUNTS[1]);
            rear_brace();
            intake_baffle();
            dc_vestibule();
            ac_tie_bridges();
        }
        for(p=alt1205t_all_m3_centres()) {
            xy=psu_hole(p);
            // Screw heads load from beneath; the PSU already has threaded
            // fittings. Upper relief accommodates their unmeasured projection.
            translate([xy.x,xy.y,-0.1]) cylinder(d=7,h=2.5);
            translate([xy.x,xy.y,-0.1]) cylinder(d=3.6,h=8.2);
            translate([xy.x,xy.y,5.6]) cylinder(d=7,h=2.5);
        }
        for(p=LID_POINTS) {
            translate([p.x,p.y,H-2.8]) hex_pocket(5.6,3);
            translate([p.x,p.y,H-6]) cylinder(d=3.6,h=7);
        }
        for(x=PANEL_X,z=PANEL_Z) {
            translate([x,D-WALL,z]) rotate([90,0,0]) hex_pocket(5.6,2.8);
            translate([x,D-WALL+0.02,z]) rotate([90,0,0]) cylinder(d=3.6,h=6);
        }
        for(x=[32:16:96],z=[8,20])
            translate([x,-0.1,z]) cube([8,4.2,2.4]);
        dc_port_negatives();
        // Receiver clearance for the panel's overlap; preserves full 4 mm
        // outer walls at the rear screw blocks.
        panel_transform() {
            for(x=[WALL,W-2*WALL-0.8])
                translate([x,FLOOR,4]) cube([WALL+0.8,H-12.0,6.4]);
            // Bottom overlap receiver is cut separately with a ramped roof.
        }
        // Rear-facing bottom receiver: a 45-degree roof removes the
        // former 6.4 mm-deep horizontal ledge over the panel overlap.
        translate([WALL,0,0]) rotate([90,0,90]) linear_extrude(W-2*WALL)
            polygon([[133.6,4],[140,4],[140,15.2],[133.6,8.8]]);
        // Lid skirt receivers at corner pillars.
        translate([0,0,H-4.4]) linear_extrude(4.5)
            offset(delta=0.4) skirt_profile();
    }
}
module lid() {
    difference() {
        union() {
            translate([0,0,H]) linear_extrude(LID) round_plan(W,D);
            translate([0,0,H-4]) linear_extrude(5) skirt_profile();
            roof_baffle();
            for(p=SHIELD_FIXINGS) translate([p.x,p.y,91.6]) cylinder(d=12,h=H-90.6);
        }
        for(x=[27.2:12:99.2],y=[30,42,54,66])
            translate([x,y,H-0.1]) cube([5.6,2.4,4.2]);
        for(p=LID_POINTS)
            translate([p.x,p.y,H-5]) cylinder(d=3.6,h=10);
        for(p=SHIELD_FIXINGS) {
            translate([p.x,p.y,89]) cylinder(d=3.6,h=16);
            translate([p.x,p.y,H+LID-2.8]) hex_pocket(5.6,3);
        }
    }
}
// Owner-authorized conservative allowances; these are NOT measurements of
// the generic assortment. 35 mm includes projecting lugs, insulated crimp and
// a wire turn behind the measured 21.8 mm insertion body.
IEC_CONNECTION_DEPTH = 35;
SHEET = 1.6;
SHIELD_FIXINGS = [[130,30],[130,80],[63,108]];
assert(IEC_CENTRE.y-18 > 8+36.86+4);
assert(IEC_CENTRE.y+18 < 90);
assert(H == 96 && SHEET == 1.6);

// A separate, blind DC vestibule below the inlet. Its roof is a nonprinted
// sheet dropped into open rebates, tucked under a ramped right lip and
// retained by tabs on the bolted outlet insert. No long enclosed feed slot.
module dc_vestibule() {
    difference() {
        union() {
            translate([3.2,92.4,4]) cube([114,4.8,45.6]);
            translate([3.2,118,4]) cube([114,3.2,45.6]);
            translate([114,94,4]) cube([3.2,27.2,48]);
            // Two staggered walls form the accessible cable labyrinth.
            translate([20,97.2,4]) cube([3.2,20.8,28]);
            translate([36,97.2,4]) cube([3.2,20.8,42]);
            for(y=[98,116]) {
                translate([0,y,42]) rotate([0,90,0]) cylinder(d=12,h=11.2);
                // Grow each horizontal nut boss on a 45-degree underside.
                translate([0,y+4,0]) rotate([90,0,0]) linear_extrude(8)
                    polygon([[3.2,28],[11.2,36],[11.2,42],[3.2,42]]);
            }
            // Solid tie bridges: the slots open sideways, never through floor.
            for(x=[53,77]) translate([x,102,4]) cube([12,10,7]);
        }
        dc_roof_rebate();
        // Open-top cable notch: the separate sheet supplies its roof,
        // so no 16.8 mm bridge or trapped supports are printed here.
        translate([35.9,99.2,34]) cube([3.4,16.8,20]);
        // Intentional insulated DC transfer to the terminal bay. Use sleeve.
        translate([113.9,107,36]) rotate([0,90,0]) cylinder(d=14.8,h=3.4);
        for(x=[53,77]) translate([x+3,101.9,5.6]) cube([6,10.2,3.2]);
    }
}
module ac_tie_bridges() {
    for(y=[72,100]) difference() {
        // Attached to the sidewall; 6 mm projection with a ramped underside.
        hull() {
            translate([143.6,y,48.4]) cube([0.4,10,18]);
            translate([138,y,54.4]) cube([6,10,12]);
        }
        translate([139.6,y-0.1,57.6]) cube([2.8,10.2,5.6]);
    }
}
module dc_port_shape() {
    // 15.8 x 8.8 mm capsule: allowance for one 8 mm or two 6 mm jackets.
    hull() for(y=[104,111]) translate([0,y,26]) rotate([0,90,0]) cylinder(d=8.8,h=1);
}
// Extrude an X/Z section along Y. Open rebates permit a tilted top-loading
// sheet. The right retaining lip has a 45-degree underside (1.2 mm reach).
// Cutting through the rear block removes its otherwise hidden overhang too.
module dc_roof_rebate() {
    translate([0,119.6,0]) rotate([90,0,0]) linear_extrude(24)
        polygon([[4,46],[115.2,46],[115.2,48],[114,49.2],
                 [114,H+1],[4,H+1]]);
}
module dc_retaining_tabs(clearance=0) {
    for(y=[100,111])
        translate([-0.8-clearance,y-clearance,48-clearance])
            cube([8.8+2*clearance,3+2*clearance,2+2*clearance]);
}
module dc_port_negatives() {
    translate([-4.1,0,0]) scale([8.3,1,1]) dc_port_shape();
    dc_roof_rebate();
    dc_retaining_tabs(0.2);
    for(y=[98,116]) {
        translate([-0.1,y,42]) rotate([0,90,0]) cylinder(d=3.6,h=12);
        translate([8.4,y,42]) rotate([0,90,0]) hex_pocket(5.6,3);
    }
}
module dc_insert() {
    difference() {
        union() {
            translate([-4,92,10]) cube([4,30,42]);
            dc_retaining_tabs();
        }
        translate([-4.1,0,0]) scale([4.3,1,1]) dc_port_shape();
        for(y=[98,116]) translate([-4.1,y,42]) rotate([0,90,0]) cylinder(d=3.6,h=4.2);
    }
}
module dc_roof_template() { square([110.6,23.6]); }
module dc_roof_sheet() {
    translate([4.2,95.8,46.2]) linear_extrude(SHEET) dc_roof_template();
}
// Flat insulating sheet carried below the lid. It covers both the PSU
// terminal bay and the inlet wiring; three exterior-loaded captive nuts.
module terminal_shield_template() {
    difference() {
        union() {
            translate([118,12]) square([24,106]);
            translate([28,94]) square([96,44]);
        }
        for(p=SHIELD_FIXINGS) translate(p) circle(d=3.6);
    }
}
// The roof sheet installs before the inlet wiring and outlet insert. The
// convex swept segments cover lowering, tuck and sampled rotation.
// One-degree chords differ from the arc by <0.005 mm, below the collision
// audit's 0.02 mm qualification floor.
module dc_roof_install_pose(angle=0,dx=0,dz=0) {
    translate([114.8+dx,0,47+dz]) rotate([0,angle,0])
        translate([-114.8,0,-47]) dc_roof_sheet();
}
module dc_roof_install_sweep() {
    hull() { dc_roof_install_pose(14,-2,60); dc_roof_install_pose(14,-2,0); }
    hull() { dc_roof_install_pose(14,-2,0); dc_roof_install_pose(14,0,0); }
    for(a=[0:1:13]) hull() { dc_roof_install_pose(a); dc_roof_install_pose(a+1); }
}
module terminal_shield_sheet() {
    translate([0,0,90]) linear_extrude(SHEET) terminal_shield_template();
}
module route(points,diameter) {
    for(i=[0:len(points)-2]) hull() {
        translate(points[i]) sphere(d=diameter,$fn=20);
        translate(points[i+1]) sphere(d=diameter,$fn=20);
    }
}
module dc_wire_route(d=8,dy=0) {
    translate([0,dy,0]) route([[-12,107,26],[10,107,26],[16,107,38],[30,107,39],[46,107,39],[64,107,18],[93,107,18],[105,107,36],[130,107,36]],d);
}
module wire_routes() {
    // Illustrative route allowances, not an electrical wiring diagram.
    color([0.85,0.25,0.10]) route([[80,100,64],[104,100,64],[130,100,64],[130,80,64],[130,80,40]],8);
    color([0.10,0.65,0.85]) dc_wire_route();
}

module components() {
    color([0.62,0.66,0.70]) psu_transform() alt1205t_keepout();
    color([0.12,0.14,0.17]) inlet_transform() iecc14_keepout();
}
module service_volumes() {
    // Orange = provisional space, not a measured terminal model.
    color([1,0.52,0.08,0.35]) {
        translate([118,14,8]) cube([24,77.5,40]);
        translate([IEC_CENTRE.x-27,D-21.8-IEC_CONNECTION_DEPTH,IEC_CENTRE.y-18])
            cube([54,IEC_CONNECTION_DEPTH,36]);
    }
}
module plug_access() {
    // Deliberately provisional 50 W x 32 H x 80 mm straight access corridor.
    // Actual cable plug/boot and bend radius have not been measured.
    translate([IEC_CENTRE.x-25,D+2,IEC_CENTRE.y-16]) cube([50,80,32]);
}
module driver_access() {
    // 8 mm driver barrel. This proves straight access, not screw lengths.
    for(p=LID_POINTS)
        translate([p.x,p.y,H+LID+2]) cylinder(d=8,h=100);
    for(x=PANEL_X,z=PANEL_Z)
        translate([x,D+2,z]) rotate([-90,0,0]) cylinder(d=8,h=100);
    for(y=RIGHT_MOUNTS)
        translate([W-10,y,10]) rotate([0,-90,0]) cylinder(d=8,h=70);
    for(p=[[REAR_MOUNT_X-8,REAR_RAIL-14],[REAR_MOUNT_X+8,REAR_RAIL-14],
           [REAR_MOUNT_X,REAR_RAIL+10]])
        translate([p.x,p.y,26]) cylinder(d=8,h=100);
}
module rail_context() {
    color([0.57,0.61,0.65]) translate(-ORIGIN) {
        difference() {
            translate([326,20,0]) cube([20,318,20]);
            translate([325.99,20,6.635]) cube([6.49,318,6.73]);
        }
        difference() {
            translate([20,338,0]) cube([306,20,20]);
            translate([20,337.99,6.635]) cube([306,6.49,6.73]);
        }
    }
}
module existing_chassis() {
    translate(-ORIGIN) {
        outer_frame_bottom();
        cradle_plate_preview("proxy");
        fixture_plate_preview("proxy");
        plate_mount_previews();
    }
}
module screw_markers() {
    color([0.82,0.83,0.85]) {
        for(p=LID_POINTS) translate([p.x,p.y,H+LID]) cylinder(d=6,h=2);
        for(x=PANEL_X,z=PANEL_Z)
            translate([x,D,z]) rotate([-90,0,0]) cylinder(d=6,h=2);
        for(y=RIGHT_MOUNTS)
            translate([W-8,y,10]) rotate([0,-90,0]) cylinder(d=6,h=2);
        translate([REAR_MOUNT_X,REAR_RAIL+10,24]) cylinder(d=6,h=2);
    }
}
module assembly(open=false,explode=false,services=false) {
    color([0.17,0.34,0.43]) tray();
    color([0.26,0.48,0.55]) translate([0,0,explode?15:0]) rail_bridge();
    color([0.26,0.48,0.55]) translate([0,explode?30:0,0]) rear_panel();
    if(!open) color([0.80,0.83,0.83]) translate([0,0,explode?42:0]) lid();
    components();
    color([0.30,0.52,0.57]) dc_insert();
    color([0.70,0.62,0.25]) dc_roof_sheet();
    if(!open) color([0.70,0.62,0.25]) translate([0,0,explode?42:0]) terminal_shield_sheet();
    if(!explode && !open) screw_markers();
    if(services) service_volumes();
}
module printable_solids() { tray(); rear_panel(); lid(); rail_bridge(); dc_insert(); }
module fitted_solids() { printable_solids(); dc_roof_sheet(); terminal_shield_sheet(); }

// A 0.01 mm translated self-intersection insets each SOLID before comparing
// the pair, so nominal mating sheets are never formed as intermediate geometry.
// Clearances/penetrations below 0.02 mm are not qualified by this audit.
// All exported collision results must then be CLEAN EMPTY, never invalid STL.
module positive_thickness() {
    intersection() {
        children();
        translate([0.01,0,0]) children();
        translate([0,0.01,0]) children();
        translate([0,0,0.01]) children();
    }
}
module positive_overlap() {
    intersection() {
        positive_thickness() children(0);
        positive_thickness() children(1);
    }
}
module raw_collision(part) {
if(part=="collision_parts") union() {
    positive_overlap() { tray(); rear_panel(); }
    positive_overlap() { tray(); lid(); }
    positive_overlap() { rear_panel(); lid(); }
    positive_overlap() { rail_bridge(); union() { tray(); rear_panel(); lid(); } }
    positive_overlap() { dc_insert(); union() { tray(); rear_panel(); lid(); } }
    positive_overlap() { dc_roof_sheet(); printable_solids(); }
    positive_overlap() { terminal_shield_sheet(); printable_solids(); }
}
else if(part=="collision_components") positive_overlap() {
    fitted_solids();
    union() { psu_transform() alt1205t_keepout(); inlet_transform() iecc14_keepout(); }
}
else if(part=="collision_guard_install") positive_overlap() {
    dc_roof_install_sweep();
    union() { tray(); psu_transform() alt1205t_keepout(); }
}
else if(part=="collision_wires") positive_overlap() {
    fitted_solids(); union() { wire_routes(); for(dy=[-3.5,3.5]) dc_wire_route(6,dy); }
}
else if(part=="collision_service") positive_overlap() {
    fitted_solids(); service_volumes();
}
else if(part=="collision_chassis") positive_overlap() {
    printable_solids(); existing_chassis();
}
else if(part=="collision_plug") positive_overlap() {
    plug_access(); union() { printable_solids(); existing_chassis(); }
}
else if(part=="collision_drivers") positive_overlap() {
    driver_access(); union() { printable_solids(); existing_chassis(); }
}
    else assert(false,str("Unknown collision selector: ",part));
}
module collision_control(offset_x) {
    positive_overlap() {
        cube([10,10,10]); translate([offset_x,0,0]) cube([10,10,10]);
    }
}

if(PART=="assembly") assembly();
else if(PART=="open") assembly(open=true,services=true);
else if(PART=="exploded") assembly(explode=true);
else if(PART=="frame") { rail_context(); assembly(); }
else if(PART=="frame_open") { rail_context(); assembly(open=true); }
else if(PART=="chassis") { existing_chassis(); assembly(); }
else if(PART=="plug_access") {
    existing_chassis(); assembly(); color([1,0.52,0.08,0.35]) plug_access();
}
else if(PART=="panel") rear_panel_flat();
else if(PART=="panel_section") intersection() {
    rear_panel_flat(); translate([0,IEC_CENTRE.y-0.5,-1]) cube([W,1,14]);
}
else if(PART=="tray") tray();
else if(PART=="bridge") translate([-(REAR_MOUNT_X-12),REAR_RAIL+16,24]) rotate([180,0,0]) rail_bridge();
else if(PART=="bottom") rotate([0,180,0]) assembly(open=true);
else if(PART=="vent_section") intersection() {
    assembly(); translate([39,-1,0]) cube([1,D+2,H+LID+4]);
}
else if(PART=="dc_insert") translate([52,-92,4]) rotate([0,-90,0]) dc_insert();
else if(PART=="dc_roof_template") dc_roof_template();
else if(PART=="terminal_shield_template") terminal_shield_template();
else if(PART=="internals") { assembly(open=true); wire_routes(); }
else if(PART=="dc_section") intersection() {
    union() { tray(); dc_insert(); dc_roof_sheet(); wire_routes(); }
    translate([-5,105.5,0]) cube([124,1,55]);
}
else if(PART=="guard_install") {
    color([0.17,0.34,0.43]) tray();
    color([0.70,0.62,0.25]) dc_roof_install_pose(14,-2,0);
}
else if(PART=="shield") { terminal_shield_sheet(); dc_roof_sheet(); }
else if(PART=="lid_print_section") intersection() {
    translate([0,D,H+LID]) rotate([180,0,0]) lid();
    translate([0,103.5,-1]) cube([W,1,20]);
}
else if(PART=="lid") translate([0,D,H+LID]) rotate([180,0,0]) lid();
else if(PART=="collision_control_contact") collision_control(10);
else if(PART=="collision_control_gap") collision_control(10.1);
else if(PART=="collision_control_overlap") collision_control(9);
else if(PART=="collision_control_thin") collision_control(9.98);
else if(PART=="collision_parts" || PART=="collision_components" ||
        PART=="collision_service" || PART=="collision_chassis" ||
        PART=="collision_plug" || PART=="collision_drivers" || PART=="collision_wires" || PART=="collision_guard_install")
    raw_collision(PART);
else assert(false,str("Unknown PART: ",PART));
