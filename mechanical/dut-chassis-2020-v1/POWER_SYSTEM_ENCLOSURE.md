# Single-supply enclosure V2 candidate

This package is a **V2 pre-DUT02 mechanical prototype**, not a certified mains enclosure. It is a secondary mount and finger guard around the PSU's metal shell and a separately fabricated terminal barrier. Do not install or energize mains wiring until every pre-power gate below is closed by a competent reviewer. Always unplug the IEC cord before removing the hood or servicing the fuse drawer.

## What changed after the full ABS print

The first full enclosure print is retired. Its rail-side seam used three adjacent structures, its barrier tongue positively occluded the intended slot, and its C14 reinforcement reached outside the true shell. Most importantly, the C14 disconnect was caused by only **0.02/0.04 mm** modeled overlap at its structural joins. It was not caused by the accepted 1.2 mm snap membrane. A trapped roof-down support pocket behind that holder also had no plier access.

V2 is a coherent three-part architecture:

- a rounded, floor-down base/tray;
- a rounded hood printed roof-exterior-down;
- a separate C14 cassette printed broad-face-down and inserted into open-bottom hood keyways;
- the existing nonprinted terminal barrier remains separate.

The sealed case is 132.8 × 128 × 60 mm (world X=190..322.8, Y=160..288, Z=0..60) with continuous R6 plan corners. The former case was 136 × 140 × 78 mm before its long rail spine. V2 deletes that spine and the redundant full-height seam walls.

## Build and nozzle control

The default flow is qualified around a **0.8 mm nozzle**:

```sh
make power-system-enclosure
make validate-power-system-enclosure
make validate-power-system-supports
```

Override the nozzle explicitly when exporting:

```sh
make power-system-enclosure NOZZLE_DIAMETER=0.4
openscad -o cassette.stl -D 'NOZZLE_DIAMETER=1.2' -D 'PART="cassette"' power-system-enclosure.scad
```

`NOZZLE_DIAMETER` must be greater than zero. Structural walls and positive joins are quantized upward to at least one complete nozzle line while retaining the 3.2 mm shell/receiver and 4.0 mm cassette-frame minima. The effective C14 snap membrane is exactly **max(1.2 mm, nozzle diameter)**; the normal cutout clearance remains exactly +0.20 mm. If the chosen nozzle makes the membrane thicker than the accepted 1.5 mm clip budget, the export emits a conspicuous warning. It will still generate, but owner-authorized sanding is required before fit can be claimed. There is no printable text.

Print the base floor-down, the hood roof-exterior-down, and the cassette on its broad exterior face, with **supports off**. The base print envelope is 196.27 × 132.8 × 56.033 mm after its declared 90-degree bed rotation; the hood is 132.8 × 128 × 46.2 mm; the cassette is 64.7 × 39 × 7.2 mm. Together they occupy 242,349.860 mm³, a 27.99% reduction from the retired 336,547.259 mm³ print. Use a brim for ABS. The R6 corners, shallow 60 mm sealed height, short rail pads, vertical 1.6 mm vent slots, 45-degree baffles/gussets, and open-side cable cleats reduce warp and eliminate trapped support cavities.

`validate-power-system-supports` first rejects large horizontal downward faces and the exact print-Z bands of the three retired defects. It then slices all three artifacts with PrusaSlicer 2.9.6, the committed 0.8 mm nozzle / 0.4 mm layer ABS audit profile, and supports disabled. It fails on `Floating bridge anchors` or `Long bridging extrusions`. Set `PRUSA_SLICER` to an alternate command path when needed; the strict local gate requires the exact slicer version. CI may explicitly report a slicer skip only when that binary is unavailable, while the geometric rejection remains mandatory. The audit profile is not a production printer/material profile and does not authorize powered use.

All three exports are connected and manifold both at source precision and on the repository's 0.0001 mm fingerprint grid.

## Component and assembly datums

The accepted PSU hole pattern remains source-owned by `alt-1205t-power-supply.scad`. V2 installs it at:

```scad
translate([194,243.7,4]) rotate([0,0,-90])
```

The measured metal keepout is X=194..304, Y=166.2..243.7, Z=4..40.86. Five 5.60 mm-AF direct top-open pressure sockets remain visible before the PSU is installed; there is no underside nut feeder.

The accepted horizontal C14 geometry remains source-owned by `iec-c14-fused-switch.scad` and is installed at:

```scad
translate([284,286,30]) rotate([90,0,0]) rotate([0,0,90])
```

Its cable points toward the DUT rear wall (+Y). The nominal cutout remains 27 × 46.86 mm with true +0.20 mm normal clearance. The 31 × 50.3 × 2 mm faceplate is entirely inside the sealed envelope. The visible cassette frame provides at least 4.0 mm continuous material around it and never projects beyond the box. Hidden keys have 0.30 mm per-side running clearance, load through keyways open at the hood's lower edge, stop under the roof, and rest on the base seat after assembly.

Two operator/front M3 screws are at X=215 and 300, Y=160, Z=50.4. With the hood removed, each standard M3 nut loads into a directly visible horizontal socket with a 6.20 mm-AF × 0.80 mm lead, 5.60 mm-AF × 2.80 mm pocket, 2.40 mm blind backstop, and at least 2.40 mm radial capture. Each base post is rooted continuously in the floor/front structure. It stays ahead of the PSU below the metal top, then flares inward only after 1.6 mm additional vertical clearance. The hood cap closes the loading mouth with assembly clearance and exposes only the 3.6 mm screw bore. Two rear bed-rooted 45-degree locator hooks register the other edge without a blind receiver.

Rail mounting uses three retained axes at world Y=149.73, 306, and 330 mm, all Z=10 mm. The old Y=125.73 axis is deleted. There are exactly **three local rail pads**: the front pad spans Y=141.73..170, while independent rear pads span Y=298..314 and Y=322..338, leaving an 8 mm clear gap. Each positively overlaps the composite rail-side wall and has its own floor-rooted load path of at least 1.6 mm; no continuous 220 mm spine remains. Physical rail load, fastener creep, and driver access are owner gates.

## Separation, cable routing, and barrier

One printed L-shaped mains/SELV boundary follows the PSU terminal side at X=304..307.2 nominal and turns across Y=248.4..251.6 at the default nozzle. The accepted 1.0 mm barrier loads into a **1.8 mm top-open groove** with 0.4 mm clearance on both sides. The groove cuts every intersecting base/pad solid, has zero tongue occlusion, and is compressed by a roof-rooted rib with a deliberate vertical gap. There are no duplicate full-height barrier rails or rail spine.

The provisional insulated DC bushing is centered near X=305.6, Y=174, Z=50. The provisional front gland was raised to X=270, Y=160, Z=50 after collision audit proved the old Z=31 route could not pass between the shifted PSU and front wall. The modeled 6 mm bundle now stays in the upper plenum and uses a 10 mm bend envelope only at its two actual bends. Roof-rooted cleats are open on one side for inspection and removal.

AC terminal/bend, IEC terminal projection, PE-lug/service, PE route, PSU, DC route, C14 body/faceplate, barrier, base/hood fit, cassette insertion, fastener, nut, and tool sweeps have dedicated selectors. The support-risk evidence shows the complete front posts from bed-root to sockets plus the roof baffle and print orientations. These checks are geometry evidence, not electrical certification.

Printed parts and fasteners are never part of protective-earth continuity. Use a dedicated green/yellow conductor and suitable metal lug/anti-loosening hardware from C14 PE to PSU PE. No PSU chassis bonding hole is invented by the model. Fuse remains TBD until the actual nameplate, load, and inrush are reviewed.

## Required pre-power and rollout gates

1. Confirm the PSU and inlet approvals/ratings, load and inrush, conductor insulation/gauge, terminals, and an appropriately selected fuse. **Fuse remains TBD.**
2. Confirm the actual C14 rear terminals, dressed AC bend/slack, PE lug, PE route, insulating bushing, DC cable, and gland against every service volume.
3. Fabricate the continuous barrier only from approved 1.0 mm G10/FR-4 or appropriately rated polycarbonate; confirm fit in the unoccluded groove and roof compression rib.
4. Approve the polymer/process for temperature and flammability. Perform a full-load thermal/ventilation test with the hood fitted and supports off print surfaces inspected.
5. Verify all five PSU sockets, both hood pressure sockets, screw lengths, hood mouth caps, rear hooks, cassette seat/stop/key engagement, and rail driver access. Perform the physical rail-load and ABS-creep gate.
6. Establish direct metal protective-earth bonding, torque/retain its hardware, and record a PE continuity test. The print must never carry fault current.
7. Verify strain relief and that no finger/tool path reaches energized terminals. Unplug before fuse service or hood removal; never work live.
8. Complete the separately authorized DUT02 physical fit, unpowered wiring inspection, powered thermal test, and owner sign-off before production docs, website parts lists, or fleet retrofit instructions change.

No certification, powered-use approval, production release, or fleet rollout is claimed by these files.
