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
three-way end connectors occupy the eight 20 mm corner cubes. Keeping the four
gantry uprights in the same side planes as the outer depth rails makes every
perimeter rail, gantry upright, and gantry crossbar the same provisional
360 mm finished length.
Do not batch-cut extrusion until one physical connector is dry-fitted. Kerf
and actual stock length should be recorded for inventory accuracy, but neither
blocks two 360 mm pieces fitting comfortably within each nominal 1 m stick.

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
(C), 1.66 mm lip depth (D), and 1.20 mm diagonal web thickness (E). This is a
20-series, nominal slot-6 T/V-slot profile, but those measured interfaces—not
another manufacturer's “2020” drawing—control printed fit.

## Mechanical architecture

### Structural frame

The default `three_way_end_corners_B08C9Q2TGW` topology uses:

| Piece | Qty | Provisional length | Purpose |
|---|---:|---:|---|
| Vertical rail | 4 | 360 mm | Between lower/upper three-way connectors |
| Width rail | 4 | 360 mm | Between left/right three-way connectors |
| Depth rail | 4 | 360 mm | Between front/rear three-way connectors |
| Plate-gantry upright | 4 | 360 mm | Two per independently movable gantry |
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
those uprights. Four broad, flat keyed ABS plates locate each gantry's upright
ends. Every indexing plate uses two M3 screws, wide washers, and printed
twist-in carriers holding ordinary metal M3 nuts—one fastener in the outer
depth rail and one in the upright. Perpendicular printed keys engage both slots
to keep the joint square while tightening. These parts position payload only;
the outer aluminum cube and metal corner connectors remain the stack load path.

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

The spacer keys use the measured 6.73 mm mouth with 0.30 mm nominal clearance.
Print the rail coupon before the full spacer set because extrusion, ABS
shrinkage, and the 0.8 mm nozzle all affect the resulting fit.

### Captured M3 twist-in nut carrier—light duty only

The gantries, fixture, cradle, and placard need 26 M3 slot fasteners per
chassis. The printable carrier reuses the ordinary metal M3 nut already
validated in the
DUT-hook system: owner-measured 5.36 mm across flats by 2.30 mm thick, in the
proven 5.60 x 2.80 mm printed pocket. The metal nut carries the thread. The ABS
body locates it and spreads light plate/placard clamp load behind the rail
opening.

Installation:

1. Print `m3-twist-nut-fit-coupon.stl` flat, with the nut pockets upward.
2. Press an ordinary M3 nut into each pocket and pre-thread an M3 screw by one
   turn as a handle.
3. Turn it so the solid face points outward toward the plate and the open nut
   pocket points inward toward the center of the extrusion. This lets the
   metal nut pull against the carrier's four-layer floor when tightened.
4. Insert the carrier's narrow side through the rail opening with its long
   direction parallel to the rail.
5. Turn the screw clockwise until the carrier wedges; do not force it through
   the opening or use a powered driver.
6. Select the widest carrier that inserts and turns freely. One, two, and
   three edge notches identify 6.25, 6.45, and 6.60 mm bodies respectively.

The production default is the two-notch 6.45 mm body. A set STL contains 26
carriers: 16 for the eight gantry indexing plates, eight for the two payload
plates, and two for the placard rail mounts. These parts are explicitly
forbidden for outer-frame joints, stacking registration, anti-lift retention,
or other safety/structural loads.

A slicer pause could embed each metal nut and close a printed roof above it,
but that is intentionally not the v1 production route: a 26-part set would
require 26 correctly oriented insertions during one pause and would make a bad
nut difficult to replace. The open 5.60 mm pocket retains the already proven
bolt-and-washer pull-in fit. Any later embedded-nut variant should use its own
slightly wider coupon-calibrated pocket rather than weakening this known fit.

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

### Rear device identification

The rear ID system is deliberately modular:

1. one flat, device-specific 166 × 38 mm raised-letter placard;
2. two reusable flat hanging straps that keep it completely beneath the top
   rear rail;
3. two keyed spacers against the rear face of the top-rear 2020 rail.

Each riser uses one M3 screw/washer and captured-nut carrier at the rail, plus
one M3 screw/nut at the placard. The default `TrimUI Smart Pro` lettering is
13.5 mm bold with 1.2 mm relief for the lab's 0.8 mm nozzle. Future devices
change only `DEVICE_LABEL` or add a tiny wrapper; the mounting geometry
remains shared. The sign is rear-facing and fixed to the outer frame; it does
not move when either payload gantry is repositioned.

## Build, preview, and validate

OpenSCAD 2021.01 or newer is sufficient:

```sh
make all       # printable STLs + generated cut list
make preview   # proxy, imported-plate, and rear assembly views
make validate  # repository lint, meshes, bounds, guards, and cut-list checks
```

`make preview` first builds the production fixture/carrier meshes in their
own projects, then imports them into the chassis assembly. The chassis source
defaults to lightweight plate envelopes so repository-wide lint never depends
on generated files.

Generated files live under `build/` and are not committed:

- `layout-assembly.png` — fast full-frame view;
- `layout-assembly-mesh.png` — existing production plates imported in place;
- `layout-rear.png` — rear label/stack-registration view;
- `layout-stacked.png` — two-frame registration and metal load-path proof;
- `layout-gantry-joint-plate.png` — eight-part flat gantry interface set;
- `layout-m3-twist-nut.png` / `layout-m3-twist-nut-coupon.png` — enlarged
  carrier and three-fit coupon views;
- `cut-list.csv` and `cut-list.md` — geometry-derived pieces and 1 m stock plan;
- `rear-id-placard.stl`;
- `placard-riser.stl` / `placard-riser-pair.stl`;
- `plate-spacer.stl` / `plate-spacer-set.stl`;
- `gantry-joint-plate.stl` / `gantry-joint-plate-set.stl`;
- `placard-spacer.stl` / `placard-spacer-pair.stl`;
- `stacking-registration-tab.stl` / `stacking-registration-tab-set.stl`;
- `rail-fit-coupon.stl`;
- `m3-twist-nut-carrier.stl` / `m3-twist-nut-carrier-set.stl`;
- `m3-twist-nut-fit-coupon.stl`.

## Provisional stock plan

At 400 mm outside dimensions and the three-way-end topology, one node requires
ten 1 m sticks:

- ten sticks: two 360 mm pieces each.

All twenty finished rails are interchangeable 360 mm cuts. Total finished
extrusion is 7200 mm. With a deliberately conservative 3.2 mm allowance per
finished cut, the plan retains about 2736 mm in useful offcuts. The checked-in
source—not this prose table—is authoritative; `build/cut-list.md` is
regenerated on every build.

## Initial printed/hardware BOM

- 1 rear ID placard;
- 2 placard risers;
- 2 placard spacers;
- 8 plate spacers (four per plate);
- 8 flat keyed gantry indexing plates (four per gantry);
- 8 stacking registration tabs for every chassis that will support another;
- 1 rail fit coupon before the other printed interfaces;
- 1 M3 twist-nut fit coupon, then 26 selected M3 twist-nut carriers;
- 8 B08C9Q2TGW zinc three-way corner connectors and their supplied M4 x 5 mm
  set screws;
- 8 B08D6T9CGN concealed zinc L-connectors and 16 supplied M5 x 6 mm set
  screws for the four gantry crossbars;
- 28 M3 machine screws, 28 ordinary M3 nuts, and wide washers: 16 gantry
  indexing-plate interfaces, 8 payload-plate mounts, 2 placard rail mounts,
  and 2 placard-to-strap joints;
- 16 supplied metal M5 T-nuts, M5 screws, and washers for the lower stacking
  registration slots, plus up to 8 more in the upper chassis for optional
  positive locks;
- optional B09GX9P79F 60 x 60 x 4 mm aluminum T-plates with supplied M5 x 8 mm
  screws/drop-in nuts only if the dry frame needs additional anti-rack support.

One node consumes all eight three-way connectors from one B08C9Q2TGW kit and
eight concealed L-connectors. The on-hand 16 three-way connectors, 20 L
connectors, and 20 one-meter extrusions support exactly two complete nodes,
leaving four L-connectors spare and no unallocated full-length extrusion. A
third complete node would need ten more stock extrusions, eight more three-way
connectors, and four more L-connectors.

## Measurements needed before cutting

1. Actual length of one nominal 1000 mm stick.
2. Actual saw-blade kerf, when convenient: the widest carbide-tooth width or
   the value printed on the blade, not feed speed. Until then CAD uses a
   conservative 3.2 mm solely for offcut accounting.
3. Dry-fit one three-way connector and confirm that a 360 mm rail plus two
   connector bodies produces 400 mm outside-to-outside.
4. Print both rail-interface coupons and record the selected key/carrier.
5. Perform one unpowered C270 framing check before the first populated stack.

After those are recorded, regenerate the cut plan, print the rail coupon, dry
assemble one empty frame, and obtain explicit owner approval before populating
or stacking it.
