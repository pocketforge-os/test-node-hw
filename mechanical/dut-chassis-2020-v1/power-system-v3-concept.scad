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
H = 64;
WALL = 4;
FLOOR = 4;
LID = 4;
SNAP = 1.2;
FIT = 0.20;
JOINT = 0.4;
ORIGIN = [178,156,0];
// Offset 11 mm from panel midline and raise 4 mm to clear the rear carrier
// link and bottom rail with the provisional plug corridor. Still well inboard.
IEC_CENTRE = [W/2-11,38]; // panel X / installed Z
PSU_ORIGIN = [8,91.5,6.4];
RIGHT_MOUNTS = [149.73-ORIGIN.y,306-ORIGIN.y];
REAR_RAIL = 338-ORIGIN.y;
REAR_MOUNT_X = 24;
PANEL_X = [16,W-16];
PANEL_Z = [30,52]; // lower drivers also clear the 24 mm rear mounting pad
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
            translate([REAR_MOUNT_X-12,REAR_RAIL-8,0]) cube([24,8,24]);
            for(x=[REAR_MOUNT_X-12,REAR_MOUNT_X+8])
                hull() {
                    translate([x,D,0]) cube([4,1,4]);
                    translate([x,REAR_RAIL-8,0]) cube([4,8,20]);
                }
            // Top-access rear-rail fastener avoids trapping a horizontal
            // screwdriver between the box and rear rail. The external pad
            // needs an accessible support strategy before print release.
            translate([REAR_MOUNT_X-12,REAR_RAIL-8,20]) cube([24,24,4]);
            translate([REAR_MOUNT_X-7,REAR_RAIL+6.9,17.6]) cube([14,6.2,3.2]);
        }
        translate([REAR_MOUNT_X,REAR_RAIL+10,16]) cylinder(d=3.6,h=10);
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
                translate(concat(psu_hole(p),[3.2])) cylinder(d=12,h=3.2);
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
        }
        for(p=alt1205t_all_m3_centres()) {
            xy=psu_hole(p);
            translate([xy.x,xy.y,3.8]) hex_pocket(5.6,3);
        }
        for(p=LID_POINTS) {
            translate([p.x,p.y,H-2.8]) hex_pocket(5.6,3);
            translate([p.x,p.y,H-6]) cylinder(d=3.6,h=7);
        }
        for(x=PANEL_X,z=PANEL_Z) {
            translate([x,D-WALL,z]) rotate([90,0,0]) hex_pocket(5.6,2.8);
            translate([x,D-WALL+0.02,z]) rotate([90,0,0]) cylinder(d=3.6,h=6);
        }
        // Receiver clearance for the panel's overlap; preserves full 4 mm
        // outer walls at the rear screw blocks.
        panel_transform() {
            for(x=[WALL,W-2*WALL-0.8])
                translate([x,FLOOR,4]) cube([WALL+0.8,H-12.0,6.4]);
            translate([WALL,FLOOR,4]) cube([W-2*WALL,WALL+0.8,6.4]);
        }
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
        }
        for(p=LID_POINTS)
            translate([p.x,p.y,H-5]) cylinder(d=3.6,h=10);
    }
}
module components() {
    color([0.62,0.66,0.70]) psu_transform() alt1205t_keepout();
    color([0.12,0.14,0.17]) inlet_transform() iecc14_keepout();
}
module service_volumes() {
    // Orange = provisional space, not a measured terminal model.
    color([1,0.52,0.08,0.35]) {
        translate([118,14,8]) cube([24,77.5,40]);
        translate([IEC_CENTRE.x-27,D-42,IEC_CENTRE.y-18]) cube([54,20.2,36]);
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
    translate([REAR_MOUNT_X,REAR_RAIL+10,26]) cylinder(d=8,h=100);
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
    color([0.26,0.48,0.55]) translate([0,explode?30:0,0]) rear_panel();
    if(!open) color([0.80,0.83,0.83]) translate([0,0,explode?42:0]) lid();
    components();
    if(!explode && !open) screw_markers();
    if(services) service_volumes();
}
module printable_solids() { tray(); rear_panel(); lid(); }

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
else if(PART=="lid") translate([0,D,H+LID]) rotate([180,0,0]) lid();
else if(PART=="collision_parts") {
    intersection() { tray(); rear_panel(); }
    intersection() { tray(); lid(); }
    intersection() { rear_panel(); lid(); }
}
else if(PART=="collision_components") intersection() {
    printable_solids();
    union() { psu_transform() alt1205t_keepout(); inlet_transform() iecc14_keepout(); }
}
else if(PART=="collision_service") intersection() {
    printable_solids(); service_volumes();
}
else if(PART=="collision_chassis") intersection() {
    printable_solids(); existing_chassis();
}
else if(PART=="collision_plug") intersection() {
    plug_access(); union() { printable_solids(); existing_chassis(); }
}
else if(PART=="collision_drivers") intersection() {
    driver_access(); union() { printable_solids(); existing_chassis(); }
}
else assert(false,str("Unknown PART: ",PART));
