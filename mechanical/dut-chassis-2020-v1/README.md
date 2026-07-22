# PocketForge stackable 2020 DUT chassis v1

This project is the mechanical **standard rack** around one PocketForge test
node. It holds the camera/electronics fixture and DUT carrier on two independent
three-axis positioning gantries, aligned to one optical axis, inside a stackable
20 × 20 mm aluminum extrusion chassis.

The initial frame is a true **400 × 400 × 400 mm external cube**. With 20 mm
posts, each face has a 360 × 360 mm clear opening. That leaves at least 50 mm
of routing/service margin around both existing printed plates:

- electronics/webcam fixture: 200 × 247 mm;
- TrimUI Smart Pro carrier: 247 × 200 mm.

The 400 mm value is a named parameter, not a magic cut dimension. The selected
three-way end connectors occupy the eight 20 mm corner cubes. Every perimeter
rail and gantry crossbar is a 360 mm finished piece. Each of the four light-duty
gantry uprights is assembled from two 180 mm halves, allowing every 1 m stick
to yield two 360 mm pieces plus one upright half instead of stranding a 273 mm
offcut.
Do not batch-cut extrusion until one physical connector is dry-fitted. Actual
stock length and saw kerf must also confirm the complete 360 + 360 + 180 mm
pattern; the current conservative 3.2 mm kerf still leaves 90.4 mm per stick.

## Why OpenSCAD works here

OpenSCAD does not have a built-in `2020()` hardware primitive, but this is a
natural parametric assembly: a 2D section is linearly extruded to each derived
rail length and transformed onto X/Y/Z. There are public alternatives such as
[NopSCADlib](https://github.com/nophead/NopSCADlib) and the
[OpenSCAD Connectors library](https://github.com/adgaudio/OpenSCAD_connectors).
For v1 we keep a tiny self-contained interface model instead:

- `envelope` detail is the authoritative 20 × 20 mm collision volume;
- `slot` detail adds the measured 6.73 mm V-slot opening, 6.48 mm depth,
  and nominal center bore for useful assembly previews;
- printed interfaces remain coupon-calibrated because “2020” is not one
  universal T-slot/V-slot section.

No external geometry or third-party library code is vendored.

## Identified bench hardware

Product identity was recorded on 2026-07-21; physical measurements and fit
coupons override marketplace prose:

- [SeekLiny B0DY7FKKMT](https://www.amazon.com/dp/B0DY7FKKMT): nominal
  20 x 20 mm European-standard V-slot extrusion, 1000 mm listing length;
- [BLCCLOY B08C9Q2TGW](https://www.amazon.com/dp/B08C9Q2TGW): eight zinc-alloy
  three-way 2020 end connectors for 6 mm slots, supplied with M4 x 5 mm set
  screws;
- [BLCCLOY B08D6T9CGN](https://www.amazon.com/dp/B08D6T9CGN): twenty concealed
  26 x 26 x 9.5 mm zinc L-connectors for 6 mm slots, supplied with M5 x 6 mm
  set screws;
- [BLCCLOY B09GX9P79F](https://www.amazon.com/dp/B09GX9P79F): eight optional
  60 x 60 x 4 mm aluminum T-plates with M5 x 8 mm screws and M5 drop-in nuts;
- [Logitech C270 HD](https://www.logitech.com/en-ae/products/webcams/c270-hd-webcam.html):
  720p/30 fps, fixed focus, 55-degree diagonal widescreen FOV.

The delivered extrusion measures 20.00 mm face-to-face. The owner's labeled
end-section measurements are retained directly in CAD: 6.73 mm slot mouth
(A), approximately 6.48 mm slot depth (B), 12.15 mm widest internal pocket
(C), 1.66 mm lip depth (D), 1.20 mm diagonal web thickness (E), and 6.66 mm
narrow channel width at the extrusion web (F). This is a 20-series, nominal
slot-6 T/V-slot profile, but those measured interfaces—not another
manufacturer's “2020” drawing—control printed fit.

## Mechanical architecture

### Structural frame

The default `three_way_end_corners_B08C9Q2TGW` topology uses:

| Piece | Qty | Provisional length | Purpose |
|---|---:|---:|---|
| Vertical rail | 4 | 360 mm | Between lower/upper three-way connectors |
| Width rail | 4 | 360 mm | Between left/right three-way connectors |
| Depth rail | 4 | 360 mm | Between front/rear three-way connectors |
| Plate-gantry upright half | 8 | 180 mm | Two halves form each of four uprights |
| Plate-gantry crossbar | 4 | 360 mm | Two height-adjustable bars per gantry |

Eight BLCCLOY B08C9Q2TGW zinc-alloy three-way connectors and their M4 set
screws close the perimeter corners. Eight BLCCLOY B08D6T9CGN concealed zinc
L-connectors and their M5 set screws attach the four gantry crossbars to the
four gantry uprights.
Printed 90-degree/three-way frame connectors are intentionally not part of the
production design: layer adhesion and polymer creep are poor tradeoffs when
complete DUT nodes may be stacked. If useful later, we can add a printable
**squaring jig** that positions metal joints without becoming one.

The 60 x 60 mm B09GX9P79F aluminum T-plates are retained as optional anti-rack
reinforcement after the first dry assembly. They are not required by the
baseline and should only be added where they do not obstruct a carrier plate,
cable, or service path.

### Three-axis plate gantries

Each printed plate mounts to its own complete 2020 gantry: two vertical uprights
bridge the outer top/bottom depth rails, and two horizontal crossbars bridge
those uprights. Each upright is two equal 180 mm offcut halves joined at its
unloaded center; the crossbars remain continuous 360 mm aluminum. Four broad,
flat keyed ABS plates locate each gantry's upright ends. Every indexing plate
uses two M3 screws, wide washers, and printed end-loaded nut bars holding
ordinary metal M3 nuts—one fastener in the outer depth rail and one in the
upright. Perpendicular printed keys engage both slots to keep the joint square
while tightening. These parts position payload only; the outer aluminum cube
and metal corner connectors remain the stack load path.

The complete mount adjusts in all three axes:

- loosen the eight gantry-end M3 fasteners to slide the complete gantry along
  the outer depth rails (Y / camera distance);
- loosen the four concealed zinc L-connectors to slide its two crossbars
  vertically along the uprights (Z);
- slide the four plate fasteners along the crossbars (X);
- the existing elongated plate slot absorbs print and assembly tolerance.

The fixture and DUT gantries are independent. Their default centers are
30 mm and 370 mm from the front respectively, preserving the validated C270
framing, and either may move from Y=30 through Y=370 as long as their 20 mm
extrusion envelopes do not intersect. Plate optical planes derive from those
gantry positions; CAD rejects an out-of-range or overlapping setup.

There is no 50 mm printed cantilever to measure perfectly or flex under the
plate. Zip ties remain an excellent emergency/service fallback, but are no
longer the primary mount.

Print `gantry-joint-plate.stl` with its broad 36 × 44 mm face on the bed and
the two perpendicular slot keys upward; it needs no support. The eight-part
set fits comfortably on the Prusa bed. Start with M3 × 12 mm screws and wide
washers, then select the exact stocked length after the rail/carrier coupon is
dry-fitted. Install the horizontal-key end against the outer depth rail and the
vertical-key end against the gantry upright; rotate the same physical part
180° for a top joint. Tighten by hand only—the captured metal nut provides the
thread, while the ABS plate provides alignment and bearing area.

#### Offcut upright clamshell

The center of each gantry upright uses one two-piece external clamshell. Both
halves are the same support-free print. An 80 mm-long broad face spans the butt
joint, a validated 6.43 mm key bridges the joint inside the front or rear slot,
and shallow side wings wrap 8 mm around the extrusion. Opposed halves leave a
4 mm service gap on both side faces rather than pretending to be a structural
aluminum sleeve. Four M3 bolts pass through external ears beside the aluminum;
the extrusion is never drilled and no T-slot fastener carries the splice.

The joint sits at the upright midpoint, clear of both crossbars and plate mount
hardware. It is acceptable here because the upright only positions a light DUT
plate; it is forbidden on any of the twelve outer-frame rails or any stacking
load path.

1. Print `gantry-upright-splice-fit-coupon.stl` broad-face down with no
   supports. It contains two samples each at 0.20, 0.40, and 0.60 mm external
   rail clearance, identified by one, two, or three large end scallops.
2. Select the smallest pair that both slide over the real 20 mm rail without
   force while their 6.43 mm keys enter the slots. The provisional default is
   the two-scallop 0.40 mm clearance.
3. Butt two 180 mm segments together on a flat surface. Place one selected
   shell on the front and one on the rear with both keys bridging the seam.
4. Install four M3 × 40 mm screws, wide washers, and ordinary nuts through the
   external ears. Tighten evenly by hand; do not crush the ABS.
5. Repeat for all four uprights. The production set is eight identical shell
   halves, forming four complete clamshells.

The spacer keys use the measured 6.73 mm mouth with 0.30 mm nominal clearance.
The owner physically selected the resulting 6.43 mm key with the production
ABS/0.8 mm-nozzle process: it slides exactly as intended. The 6.63 mm coupon is
rejected as too large, while 6.23 mm remains a loose snap-in fallback. Reprint
the rail coupon only after changing material, nozzle, extrusion supplier, or
dimensional compensation.

### Captured M3 end-loaded nut bar—light duty only

The gantries, fixture, cradle, and placard need 26 M3 slot fasteners per
chassis. The initial twist-in coupon was physically rejected: its miniature
wedging geometry did not reproduce reliably with the lab's 0.8 mm nozzle. The
replacement is a 30 mm long, chamfer-ended sliding nut bar with no spring ears
or printed threads. It is deliberately large enough to grab and position,
cannot rotate in the channel, and spreads clamp load far beyond a commercial
nut-sized nubbin. Its 11.75 mm bearing face uses nearly the entire 12.15 mm
under-lip channel. After one 0.4 mm print layer, the body follows the channel
taper toward the measured 6.66 mm deep face. It is intentionally too wide for
the 6.73 mm mouth and must enter from a cut rail end before the corner
connector closes that end.

The bar reuses the ordinary metal M3 nut already validated in the DUT-hook
system: owner-measured 5.36 mm across flats by 2.30 mm thick, in the proven
5.60 × 2.80 mm printed pocket. The metal nut carries the thread. The ABS body
locates it and spreads light plate/placard clamp load behind the rail opening.
The body is 4.4 mm deep. The first physical taper used an 8.9 mm pocket-facing
side and a 1.2 mm straight flange; the owner's end-on fit photo showed that
both missed the delivered channel. The third pass holds the accepted-near
11.75 mm bearing face, reduces the straight section to one 0.4 mm print layer,
and tests deep faces around the measured 6.66 mm dimension F. The delivered
extrusion, not a nominal commercial T-nut, is the dimensional authority.

Installation:

1. Print `m3-slide-nut-fit-coupon.stl` flat, with the nut pockets upward. Its
   third physical pass contains exactly two independent 30 mm parts—large
   enough to provide sufficient layer cooling in the lab's ABS process.
2. One and two large end scallops identify the 6.26 and 6.46 mm deep-face
   widths respectively; identification does not depend on fine embossed text.
   Both begin at the same 11.75 mm bearing face.
3. Pull an ordinary M3 nut into each pocket with an M3 screw and washer, then
   leave the screw threaded one turn as a handle.
4. With a rail end still open, orient the solid face toward the slot mouth and
   the open nut pocket toward the extrusion center. Slide each sample along the
   pocket; never hammer or force it.
5. Select the widest pair that both travel freely along the real rail. Confirm
   that neither can pull outward through the slot mouth, then tighten one under
   a sacrificial washer by hand to verify clamping.
6. Before installing end connectors, load every required bar plus spares
   into the exact rail face where it will be used. A bar cannot move between
   the four independent slots after assembly.

The provisional production profile is 11.75 mm at the bearing face and
6.36 mm at the deep face until this bracketing physical coupon selects 6.26 or
6.46 mm. A production set contains 32 bars: 26 required plus six spares to
preload before rail ends are closed. Park spares loosely under a screw/washer
or an installed bracket so they do not rattle into inaccessible positions.
These parts are explicitly forbidden for outer-frame joints, stacking
registration, anti-lift retention, or other safety/structural loads.

The initial version keeps the hex pocket open and pressure-fits the nut because
that interface is already print-proven and a damaged nut remains replaceable.
A future pause-and-encapsulate variant is possible, but it needs a separately
calibrated, slightly wider nut cavity and a documented slicer pause layer; do
not insert metal into this open-pocket STL mid-print.

### Optical stack

The fixture's measured webcam center and the carrier's screen center both land
on `[X=200, Z=202]`. The camera is a Logitech C270 HD. Logitech currently lists
a 55° diagonal FOV for 16:9 capture, which the model conservatively resolves to
about 48.8° horizontal and 28.6° vertical. At the provisional 270.1 mm
lens-to-screen distance, that covers roughly 245 x 138 mm: about 28 mm of
margin on every side of the 188.35 x 79.77 mm DUT. The guard now requires a
full 20 mm margin on each edge, not 20 mm total.

The C270 fixture keep-out remains the physically measured 71 x 31.55 mm face
envelope. Logitech's published 72.91 x 31.91 x 66.64 mm dimensions include its
fixed mounting clip. Final acceptance is a simple unpowered framing check;
both payload planes remain independently adjustable through their gantry Y
parameters.

### Stacking registration—not load-bearing printed feet

The better term for the requested foot/receiver system is **stacking
registration guides**. Two flat tabs bolt to the exterior faces at each top
corner and extend 12 mm above the frame with a tapered lead-in. The next frame
drops between the eight tabs.

Each tab has two lower-frame slots positioned below the upper three-way corner
connector so it cannot pivot, plus an optional upper locking hole into the
bottom rail of the stacked frame. These holes use the supplied metal M5
drop-in T-nuts, M5 screws, and washers. The tabs prevent
lateral skating (and can prevent lift when locked); broad aluminum top/bottom
faces carry the vertical load directly. This keeps a cracked print from
becoming a stack collapse. Until a loaded physical test establishes a rated
stack count, use no more than two populated nodes on a stable surface and
positively restrain the stack against tipping.

### Front device identification

The front ID system is deliberately modular:

1. one flat, device-specific 166 × 38 mm raised-letter placard;
2. two reusable flat hanging straps that keep it completely beneath the top
   front rail;
3. two keyed spacers against the operator-facing side of the top-front 2020
   rail.

Each riser uses one M3 screw/washer and captured-nut carrier at the rail, plus
one M3 screw/nut at the placard. The default `TrimUI Smart Pro` lettering is
13.5 mm bold with 1.2 mm relief for the lab's 0.8 mm nozzle. Future devices
change only `DEVICE_LABEL` or add a tiny wrapper; the mounting geometry
remains shared. The sign is fixed to the outer frame and faces the operator
standing at the camera/front side, looking through the node toward the DUT. It
does not move when either payload gantry is repositioned.

## Build, preview, and validate

OpenSCAD 2021.01 or newer is sufficient:

```sh
make all       # printable STLs + generated cut list
make preview   # proxy, imported-plate, front-label, and print-group views
make validate  # repository lint, meshes, bounds, guards, and cut-list checks
make refresh-cut-list  # deliberately update checked-in CUT_LIST.md from CAD
openscad -D 'PART="presentation"' pocketforge-node-chassis.scad
openscad -D 'PART="presentation"' -D 'EXAMPLE_DEVICE_VARIANT="smart_pro_s"' pocketforge-node-chassis.scad
```

`make preview` first builds the production fixture, both production carrier
variants, and the exact six-hook installed layout in their own projects. It
then stages those meshes under `build/imports/` and imports them into the
chassis assembly. `PART="presentation"` shows the exact production boards,
all six accepted J-hooks, the device/camera proxies, and the analytical C270
field-of-view frustum together. The hook mesh is presentation-only and remains
separate from the printable carrier and hook-set STLs; it cannot accidentally
turn the serviceable cradle into one fused print. The cone likewise remains
independent so camera geometry can evolve without modifying either board.

`EXAMPLE_DEVICE_VARIANT="smart_pro"` is the default and keeps the imported
carrier title and front placard consistent. Select `smart_pro_s` to switch both
labels and the imported carrier together. The staged presentation assets are:

- `build/imports/dut-fixture.stl`;
- `build/imports/trimui-smart-pro-carrier.stl`;
- `build/imports/trimui-smart-pro-s-carrier.stl`;
- `build/imports/trimui-smart-pro-family-installed-hooks.stl`.

The normal `PART="assembly"` view intentionally defaults to lightweight plate
envelopes so repository-wide lint never depends on generated files. Run
`make preview` once before opening presentation mode. The staged imports are
also copied into the Desktop package, making that presentation self-contained.

Generated files live under `build/` and are not committed:

- `layout-assembly.png` — fast full-frame view;
- `layout-assembly-mesh.png` — exact production fixture/carrier meshes plus
  six installed hooks, device, and C270 field-of-view overlays;
- `layout-assembly-smart-pro-s.png` — the same complete assembly with the
  Smart Pro S carrier title and front placard selected together;
- `layout-front.png` — operator/front label and stack-registration view;
- `layout-stacked.png` — two-frame registration and metal load-path proof;
- `layout-gantry-joint-plate.png` — eight-part flat gantry interface set;
- `layout-gantry-splice.png` and `layout-gantry-splice-coupon.png` — one
  clamshell pair and the six-piece external-fit coupon;
- `layout-m3-slide-nut.png`, `layout-m3-slide-nut-end.png`, and
  `layout-m3-slide-nut-coupon.png` — enlarged perspective, end-profile, and
  two-piece bracketing-width nut-bar views;
- `layout-print-group-01.png` through `layout-print-group-07.png` — the seven
  ready-to-slice production batches;
- `cut-list.csv` and `cut-list.md` — geometry-derived pieces and 1 m stock plan;
- `device-id-placard.stl`;
- `placard-riser.stl` / `placard-riser-pair.stl`;
- `plate-spacer.stl` / `plate-spacer-set.stl`;
- `gantry-joint-plate.stl` / `gantry-joint-plate-set.stl`;
- `gantry-upright-splice-shell.stl` /
  `gantry-upright-splice-shell-pair.stl` /
  `gantry-upright-splice-shell-set.stl`;
- `gantry-upright-splice-fit-coupon.stl`;
- `placard-spacer.stl` / `placard-spacer-pair.stl`;
- `stacking-registration-tab.stl` / `stacking-registration-tab-set.stl`;
- `rail-fit-coupon.stl`;
- `m3-slide-nut-carrier.stl` / `m3-slide-nut-carrier-set.stl`;
- `m3-slide-nut-fit-coupon.stl`;
- `print-group-01-calibration.stl` through
  `print-group-07-gantry-splices.stl`.

`CUT_LIST.md` is the checked-in fabrication sheet. It is generated from the
same CAD parameters as `build/cut-list.md`, and `make validate` fails if the
two drift. This keeps the physical cutting plan reviewable in git while the
CSV remains a generated machine-readable artifact.

## Print groups and supports

The individual STLs above remain available for one-off replacement parts. For
a complete chassis, the numbered group STLs are already arranged in supported
quantities and in their intended bed orientation:

| Group | Contents | Why separate |
|---|---|---|
| 01 calibration | rail-key coupon + two 30 mm M3 nut bars bracketing dimension F | Print and physically select fits before production batches |
| 02 gantry hardware | 8 gantry joint plates | Flat keyed payload-gantry interfaces |
| 03 plate mounts | 8 plate spacers + 2 placard straps + 2 placard spacers | All keyed payload and label mounting interfaces |
| 04 stacking guides | 8 registration tabs | Separate safety/stacking hardware inspection |
| 05 device label | 1 `TrimUI Smart Pro` placard | Allows a different color or a slicer filament change for raised text |
| 06 M3 nut bars | 32 selected full-channel nut bars | 26 required light-duty fasteners plus six preloaded spares |
| 07 gantry splices | 8 identical clamshell halves | Forms four offcut-upright joints after the fit coupon is selected |

Every production group is support-free as exported and fits the conservative
247 × 207 mm Prusa printable envelope. Keep Group 05 separate for appearance,
not because it needs support. Print flat faces on the bed, use ABS and the
validated 0.8 mm-nozzle profile, and do not enable automatic reorientation.

## Provisional stock plan

At 400 mm outside dimensions and the three-way-end topology, one node requires
eight 1 m sticks:

- each stick: two 360 mm pieces plus one 180 mm gantry-upright half.

The sixteen 360 mm pieces supply the twelve outer rails and four continuous
crossbars; the eight 180 mm pieces supply the four split uprights. Total
finished extrusion remains 7200 mm. With a deliberately conservative 3.2 mm
allowance for each of 24 cuts, the plan retains about 723.2 mm across eight
sticks. This is the material minimum for the current topology: after reserving
six bars for twelve continuous outer-frame rails, the six resulting 273.6 mm
offcuts plus one additional 1 m bar contain only about 2641.6 mm before more
kerfs, less than the gantries' 2880 mm requirement. Seven bars therefore cannot
preserve both the continuous outer frame and two fully adjustable gantries.
The checked-in `CUT_LIST.md` is the fabrication artifact and the OpenSCAD
source remains the dimensional authority. `build/cut-list.md` is regenerated
on every build and validation checks it byte-for-byte against the committed
sheet.

## Initial printed/hardware BOM

- 1 front ID placard;
- 2 placard risers;
- 2 placard spacers;
- 8 plate spacers (four per plate);
- 8 flat keyed gantry indexing plates (four per gantry);
- 1 six-piece gantry-clamshell fit coupon, then 8 selected shell halves forming
  four upright splices;
- 8 stacking registration tabs for every chassis that will support another;
- 1 rail fit coupon before the other printed interfaces;
- 1 two-piece M3 nut-bar fit coupon, then 32 selected M3 nut bars (26
  required plus six preloaded spares);
- 8 B08C9Q2TGW zinc three-way corner connectors and their supplied M4 x 5 mm
  set screws;
- 8 B08D6T9CGN concealed zinc L-connectors and 16 supplied M5 x 6 mm set
  screws for the four gantry crossbars;
- 44 M3 machine screws, 44 ordinary M3 nuts, and wide washers: 16 gantry
  indexing-plate interfaces, 8 payload-plate mounts, 2 placard rail mounts,
  2 placard-to-strap joints, and 16 clamshell ear fasteners;
- 16 supplied metal M5 T-nuts, M5 screws, and washers for the lower stacking
  registration slots, plus up to 8 more in the upper chassis for optional
  positive locks;
- optional B09GX9P79F 60 x 60 x 4 mm aluminum T-plates with supplied M5 x 8 mm
  screws/drop-in nuts only if the dry frame needs additional anti-rack support.

One node consumes all eight three-way connectors from one B08C9Q2TGW kit and
eight concealed L-connectors. The on-hand 16 three-way connectors, 20 L
connectors, and 20 one-meter extrusions support exactly two complete nodes,
leaving four L-connectors and four full-length extrusions spare. A third
complete node would need four more stock extrusions, eight more three-way
connectors, and four more L-connectors.

## Measurements needed before cutting

1. Actual length of one nominal 1000 mm stick.
2. Actual saw-blade kerf, when convenient: the widest carbide-tooth width or
   the value printed on the blade, not feed speed. Until then CAD uses a
   conservative 3.2 mm solely for offcut accounting.
3. Dry-fit one three-way connector and confirm that a 360 mm rail plus two
   connector bodies produces 400 mm outside-to-outside.
4. Print the two-piece end-loaded nut-bar coupon and record the selected width;
   the separate rail key is already physically selected at 6.43 mm.
5. Print the six-piece gantry-clamshell coupon and record the selected external
   clearance before producing the eight full shell halves.
6. Perform one unpowered C270 framing check before the first populated stack.

After those are recorded, regenerate the cut plan, print the rail coupon, dry
assemble one empty frame, and obtain explicit owner approval before populating
or stacking it.
