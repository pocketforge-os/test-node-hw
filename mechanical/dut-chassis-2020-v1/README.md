# PocketForge stackable 2020 DUT chassis v1

This project is the mechanical **standard rack** around one PocketForge test
node. It holds one movable camera/electronics fixture and one fixed rear DUT
carrier on a shared optical axis inside a stackable 20 × 20 mm aluminum
extrusion chassis.

The fleet-standard frame is a compact **358 W × 346 D × 368 H mm external
rectangle**. Rectangular is intentional: the required plate margins and C270
optical distance differ by axis, while making every axis 400 mm wastes stock.
The usable payload face is 318 W × 328 H mm. It leaves at least 35 mm of
routing/service margin around both existing printed plates:

- electronics/webcam fixture: 200 × 247 mm;
- TrimUI Smart Pro carrier: 247 × 200 mm.

The delivered three-way fitting is not a 20 mm corner cube. It caps a vertical
post and sends two tongues into width/depth rails that butt against that post.
The owner's physical check found that a 360.00 mm post with a connector at each
end measures approximately 368 mm outside-to-outside. CAD therefore models the
actual cap-flush side-butt topology: the two horizontal rails terminate flush
against adjacent faces of the vertical post, not against or through each
other, and their top/bottom faces share the connector-cap planes with zero
inset. Finished cuts are 360 mm vertical, 306 mm depth, and 318 mm width; the
single fixture gantry reuses 318 mm crossbars and split 164 mm uprights. An
exact bounded cut optimizer fits one complete node into six
nominal 1 m sticks.

The exact packer avoids the tempting `360 + 318 + 306 mm` near-full-stick
pattern. Its fullest selected bars retain 36.4 mm after three conservative
3.2 mm kerfs. Measure every stick before cutting; if one is short, do not
silently shorten a finished rail—revise the cut plan.

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
- [HandsOn Technology 20-series three-way connector drawing](https://www.handsontec.com/dataspecs/alum-material/3W%20Corner%20Bracket.pdf):
  independent dimensional/application reference confirming the same
  vertical-post plus two side-butting horizontal-rail topology; used as a
  topology check only, not imported geometry;
- [BLCCLOY B08D6T9CGN](https://www.amazon.com/dp/B08D6T9CGN): twenty concealed
  26 x 26 x 9.5 mm zinc L-connectors for 6 mm slots, supplied with M5 x 6 mm
  set screws;
- [BLCCLOY B09GX9P79F](https://www.amazon.com/dp/B09GX9P79F): eight optional
  60 x 60 x 4 mm aluminum T-plates with M5 x 8 mm screws and M5 drop-in nuts;
- [Logitech C270 HD](https://www.logitech.com/en-ae/products/webcams/c270-hd-webcam.html):
  720p/30 fps, fixed focus, 55-degree diagonal widescreen FOV.
- [HandsOn Technology 20-series straight internal connector](https://handsontec.com/index.php/product/straight-internal-connector-for-2020-extrusion-profile/):
  conventional 100 × 10 × 5 mm steel bridge with four M5 set-screw points;
  used as an architecture reference only, not as imported geometry.

The delivered extrusion measures 20.00 mm face-to-face. The owner's labeled
end-section measurements are retained directly in CAD: 6.73 mm slot mouth
(A), approximately 6.48 mm slot depth (B), 12.15 mm widest internal pocket
(C), 1.66 mm lip depth (D), 1.20 mm diagonal web thickness (E), and 6.66 mm
narrow channel width at the extrusion web (F). This is a 20-series, nominal
slot-6 T/V-slot profile, but those measured interfaces—not another
manufacturer's “2020” drawing—control printed fit.

## Mechanical architecture

### Structural frame

The default `three_way_cap_flush_side_butt_B08C9Q2TGW_measured` topology uses:

| Piece | Qty | Finished length | Purpose |
|---|---:|---:|---|
| Vertical post | 4 | 360 mm | Connector stem; end caps make the outside height about 368 mm |
| Width rail | 4 | 318 mm | Butts between left/right post side faces |
| Depth rail | 4 | 306 mm | Butts between front/rear post side faces |
| Fixture-gantry upright half | 4 | 164 mm | Two reinforced halves form each 328 mm upright |
| Fixture-gantry crossbar | 2 | 318 mm | Two height-adjustable fixture bars |

Eight BLCCLOY B08C9Q2TGW zinc-alloy three-way connectors and their M4 set
screws close the perimeter corners. Four BLCCLOY B08D6T9CGN concealed zinc
L-connectors and their M5 set screws attach the two fixture crossbars to the
two gantry uprights.
Printed 90-degree/three-way outer-frame connectors are intentionally not part
of the production design: layer adhesion and polymer creep are poor tradeoffs
when complete DUT nodes may be stacked. The supplied metal corner fittings are
the outer-frame and stacking load path.

The 60 x 60 mm B09GX9P79F aluminum T-plates are retained as optional anti-rack
reinforcement after the first dry assembly. They are not required by the
baseline and should only be added where they do not obstruct a carrier plate,
cable, or service path.

### Movable fixture gantry and fixed rear carrier

Only the electronics/webcam fixture mounts to a complete 2020 gantry: two
vertical uprights bridge the outer top/bottom depth rails, and two horizontal
crossbars bridge those uprights. Each upright is two equal 164 mm halves joined
at its unloaded center; the crossbars remain continuous 318 mm aluminum. Four
broad, flat keyed ABS plates locate the gantry's upright ends. Every indexing plate
uses two M3 screws, wide washers, and printed end-loaded nut bars holding
ordinary metal M3 nuts—one fastener in the outer depth rail and one in the
upright. Perpendicular printed keys engage both slots to keep the joint square
while tightening. These parts position payload only; the outer aluminum frame
and metal corner connectors remain the stack load path.

The fixture adjusts in all three axes:

- loosen the eight gantry-end M3 fasteners to slide the gantry along
  the outer depth rails (Y / camera distance);
- loosen the four concealed zinc L-connectors to slide its two crossbars
  vertically along the uprights (Z);
- slide the four plate fasteners along the crossbars (X);
- the existing elongated plate slot absorbs print and assembly tolerance.

The default fixture-gantry center is Y=43.2 mm. The fixture board is mounted on
its front side, leaving 5 mm between the board and front outer rail. CAD rejects
an out-of-range gantry or a fixture/front-rail collision.

The DUT carrier does not need a second gantry. Its device-specific source
already places the screen center on the fleet optical datum, so four printed
vertical links fasten its existing corner slots directly to the rear outer
width rails. Two upper links carry the light plate; two lower links prevent
swing and racking. The rail end has a round M3 datum and the accepted 6.43 mm
slot key; the carrier end has a 10 mm adjustment capsule. Sliding the four rear
rail nut bars sets X, while device-specific top/bottom link lengths set Z. The
default links are 97.5 mm (top) and 114.5 mm (bottom), including 12 mm material
beyond each hole center. Their 5 mm thickness leaves the carrier rear face 25
mm ahead of the chassis back—approximately the requested inch of rear cable
service space.

Future smaller carriers keep this frame and regenerate only those parametric
link lengths. Once aligned, the carrier remains fixed; routine camera-distance
changes happen at the fixture gantry.

There is no 50 mm printed cantilever to measure perfectly or flex under the
plate. Zip ties remain an excellent emergency/service fallback, but are no
longer the primary mount.

Print `gantry-joint-plate.stl` with its broad 36 × 44 mm face on the bed and
the two perpendicular slot keys upward; it needs no support. The four-part
set fits comfortably on the Prusa bed. Start with M3 × 12 mm screws and wide
washers, then select the exact stocked length after the rail/carrier coupon is
dry-fitted. Install the horizontal-key end against the outer depth rail and the
vertical-key end against the gantry upright; rotate the same physical part
180° for a top joint. Tighten by hand only—the captured metal nut provides the
thread, while the ABS plate provides alignment and bearing area.

#### Reinforced offcut-upright splice

The center of each gantry upright uses a four-piece reinforced splice: two
identical external shells and two identical internal channel bars. Every part
prints on its broad face with no support; there is no tall sleeve whose strength
depends on Z-layer adhesion.

Each 80 mm external shell spans 40 mm onto both 164 mm rail halves. Its 6.43 mm
key enters the rail mouth and shallow wings wrap 8 mm around the extrusion.
The owner physically selected the one-notch coupon, corresponding to 0.20 mm
external clearance. Inside the same front/rear channels, an 80 mm
11.75-to-6.46 mm trapezoidal bar also spans the seam. It captures two ordinary
metal M3 nuts at ±24 mm, placing one fastener in each aluminum half. Two
opposed shell/bar pairs give four clamped points and reinforce both faces
without drilling the extrusion.

This follows the conventional straight internal-connector pattern—a long bar
bridging the joint with fasteners on both sides—but uses the delivered rail's
measured channel and the already accepted ABS taper. No marketplace mesh or
third-party geometry was imported. The reference commercial 20-series part is
100 × 10 × 5 mm steel with four M5 set screws; our light-duty version is
deliberately printable and uses replaceable metal M3 nuts.

The joint sits at each fixture upright midpoint, clear of both crossbars and
plate-mount hardware. It is acceptable here because the upright only positions
a light fixture plate; it is forbidden on any of the twelve outer-frame rails or any stacking
load path.

1. Print `gantry-upright-splice-reinforced-test-set.stl` exactly as exported.
   It contains two shells and two internal bars—one complete upright joint.
2. Pull four ordinary M3 nuts into the open hex pockets using an M3 screw and
   washer. Do not glue them and do not insert them mid-print.
3. With both 164 mm rail ends open, slide one internal bar 40 mm into the front
   channel and one 40 mm into the rear channel of the first half. Slide the
   second rail half over the exposed 40 mm of both bars until the cut ends butt.
4. Put an external shell over each reinforced face with its key spanning the
   seam. Install four M3 screws and wide washers into the captured nuts. Choose
   the shortest stocked screw that gives full nut engagement without bottoming
   against the extrusion web; tighten evenly by hand.
5. Confirm the assembled upright remains straight and resists gentle hand
   racking. Only after that physical gate should Groups 07 and 08 be printed.

The spacer keys use the measured 6.73 mm mouth with 0.30 mm nominal clearance.
The owner physically selected the resulting 6.43 mm key with the production
ABS/0.8 mm-nozzle process: it slides exactly as intended. The 6.63 mm coupon is
rejected as too large, while 6.23 mm remains a loose snap-in fallback. Reprint
the rail coupon only after changing material, nozzle, extrusion supplier, or
dimensional compensation.

### Captured M3 end-loaded nut bar—light duty only

The fixture gantry, fixture plate, rear-carrier links, and placard need 18 M3
slot fasteners per
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

The owner physically accepted both third-pass candidates on 2026-07-22. The
wider two-scallop candidate is therefore the production profile: 11.75 mm at
the bearing face and 6.46 mm at the deep face. It preserves the most material
while still travelling freely in the delivered rail. A production set
contains 24 bars: 18 required plus six spares to preload before rail ends are
closed. Park spares loosely under a screw/washer or an installed bracket so
they do not rattle into inaccessible positions.
These parts are explicitly forbidden for outer-frame joints, stacking
registration, anti-lift retention, or other safety/structural loads.

The initial version keeps the hex pocket open and pressure-fits the nut because
that interface is already print-proven and a damaged nut remains replaceable.
A future pause-and-encapsulate variant is possible, but it needs a separately
calibrated, slightly wider nut cavity and a documented slicer pause layer; do
not insert metal into this open-pocket STL mid-print.

### Optical stack

The fixture's measured webcam center and the carrier's screen center both land
on `[X=179, Z=192.5]`. The camera is a Logitech C270 HD. Logitech currently lists
a 55° diagonal FOV for 16:9 capture, which the model conservatively resolves to
about 48.8° horizontal and 28.6° vertical. At the default 256.1 mm
lens-to-screen distance, that covers roughly 232.4 × 130.7 mm: approximately
22.0 mm horizontal and 25.5 mm vertical margin on each edge of the
188.35 × 79.77 mm DUT. The guard requires a full 20 mm margin on every edge,
not 20 mm total.

The C270 fixture keep-out remains the physically measured 71 x 31.55 mm face
envelope. Logitech's published 72.91 x 31.91 x 66.64 mm dimensions include its
fixed mounting clip. Final acceptance is a simple unpowered framing check. The
carrier plane is fixed; the fixture gantry remains adjustable in Y.

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
does not move when the fixture gantry is repositioned.

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

`make preview` first builds the production fixture, the carriers'
presentation-only body/label splits, and the exact six-hook installed layout
in their own projects. It then stages the required meshes under
`build/imports/` and imports them into the chassis assembly.
`PART="presentation"` shows the exact production board geometry,
all six accepted J-hooks, the device/camera proxies, and the analytical C270
field-of-view frustum together. The hook mesh is presentation-only and remains
separate from the printable carrier and hook-set STLs; it cannot accidentally
turn the serviceable cradle into one fused print. The carrier body and labels
also remain separate presentation meshes so the white-to-black layer change is
visible without coincident-surface artifacts. The cone likewise remains
independent so camera geometry can evolve without modifying either board.

`EXAMPLE_DEVICE_VARIANT="smart_pro"` is the default and keeps the imported
carrier title and front placard consistent. Select `smart_pro_s` to switch both
labels and the imported carrier together. The staged presentation assets are:

- `build/imports/pocketforge-dut-fixture-v1.stl`;
- `build/imports/trimui-smart-pro-family-carrier-body.stl`;
- `build/imports/trimui-smart-pro-labels.stl`;
- `build/imports/trimui-smart-pro-s-labels.stl`;
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
- `layout-corner-joint.png` — isolated proof that both horizontal rails butt
  flush to adjacent vertical-post faces;
- `layout-gantry-joint-plate.png` — four-part flat fixture-gantry interface set;
- `layout-rear-carrier-links.png` — two top and two bottom fixed-carrier links;
- `layout-gantry-splice.png`, `layout-gantry-splice-installed.png`, and
  `layout-gantry-splice-coupon.png` — one complete reinforced test set, a
  translucent installed-joint/load-path view, and the historical six-piece
  external-fit coupon;
- `layout-m3-slide-nut.png`, `layout-m3-slide-nut-end.png`, and
  `layout-m3-slide-nut-coupon.png` — enlarged perspective, end-profile, and
  two-piece bracketing-width nut-bar views;
- `layout-print-group-01.png` through `layout-print-group-08.png` — the eight
  ready-to-slice production batches;
- `cut-list.csv` and `cut-list.md` — geometry-derived pieces and 1 m stock plan;
- `device-id-placard.stl`;
- `placard-riser.stl` / `placard-riser-pair.stl`;
- `plate-spacer.stl` / `plate-spacer-set.stl`;
- `rear-carrier-link-top.stl` / `rear-carrier-link-bottom.stl` /
  `rear-carrier-link-fit-pair.stl` / `rear-carrier-link-set.stl`;
- `gantry-joint-plate.stl` / `gantry-joint-plate-set.stl`;
- `gantry-upright-splice-shell.stl` /
  `gantry-upright-splice-shell-pair.stl` /
  `gantry-upright-splice-shell-set.stl`;
- `gantry-upright-splice-internal-bar.stl` /
  `gantry-upright-splice-internal-bar-set.stl` /
  `gantry-upright-splice-reinforced-test-set.stl`;
- `gantry-upright-splice-fit-coupon.stl`;
- `placard-spacer.stl` / `placard-spacer-pair.stl`;
- `stacking-registration-tab.stl` / `stacking-registration-tab-set.stl`;
- `rail-fit-coupon.stl`;
- `m3-slide-nut-carrier.stl` / `m3-slide-nut-carrier-set.stl`;
- `m3-slide-nut-fit-coupon.stl`;
- `print-group-01-calibration.stl` through
  `print-group-08-gantry-splice-internal-bars.stl`.

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
| 01 calibration | rail-key coupon + two 30 mm M3 nut bars bracketing dimension F | Physically accepted; retain for a material, nozzle, or extrusion change |
| 02 gantry hardware | 4 gantry joint plates | Flat keyed fixture-gantry interfaces |
| 03 plate mounts | 4 fixture spacers + 2 top/2 bottom rear-carrier links + 2 placard straps + 2 placard spacers | All keyed payload and label mounting interfaces |
| 04 stacking guides | 8 registration tabs | Separate safety/stacking hardware inspection |
| 05 device label | 1 `TrimUI Smart Pro` placard | Allows a different color or a slicer filament change for raised text |
| 06 M3 nut bars | 24 selected 11.75 / 6.46 mm full-channel nut bars | 18 required light-duty fasteners plus six preloaded spares |
| 07 gantry splice shells | 4 identical 0.20 mm-clearance external shells | Two outside bridges per fixture-upright joint |
| 08 gantry splice bars | 4 identical 80 mm double-nut internal bars | Two channel reinforcements per fixture-upright joint |

Every production group is support-free as exported and fits the conservative
247 × 207 mm Prusa printable envelope. Keep Group 05 separate for appearance,
not because it needs support. Print flat faces on the bed, use ABS and the
validated 0.8 mm-nozzle profile, and do not enable automatic reorientation.

## Six-stick stock plan

One node uses exactly six nominal 1 m sticks while retaining continuous
outer-frame rails and continuous fixture-gantry crossbars. The deterministic
exact packer proves this assignment:

- 2 sticks: `360 + 360 + 164 mm`, consuming 893.6 mm each including three
  conservative 3.2 mm kerfs;
- 2 sticks: `318 + 318 + 318 mm`, consuming 963.6 mm each;
- 1 stick: `306 + 306 + 306 mm`, consuming 927.6 mm;
- 1 stick: `306 + 164 + 164 mm`, consuming 643.6 mm.

The 18 finished pieces total 5228 mm. Kerf allowance is 57.6 mm and aggregate
remaining stock is 714.4 mm. Five sticks cannot contain 5285.6 mm of
kerf-inclusive material, so six is the volume lower bound as well as a proven
packing. `scripts/cutlist.py` searches from that lower bound upward with
symmetry pruning rather than relying on first-fit order.

The fullest 963.6 mm patterns retain 36.4 mm. Confirm every stick's actual
length and that the blade kerf does not exceed 3.2 mm before making those
cuts. The checked-in `CUT_LIST.md` is the fabrication
artifact and OpenSCAD remains the dimensional authority. `build/cut-list.md`
is regenerated on every build and validation checks it byte-for-byte against
the committed sheet.

## Initial printed/hardware BOM

- 1 front ID placard;
- 2 placard risers;
- 2 placard spacers;
- 4 fixture-plate spacers;
- 2 top and 2 bottom fixed rear-carrier links;
- 4 flat keyed fixture-gantry indexing plates;
- 1 four-piece reinforced gantry-splice test set; after physical acceptance,
  4 external shells plus 4 internal double-nut bars form two upright splices;
- 8 stacking registration tabs for every chassis that will support another;
- 1 rail fit coupon before the other printed interfaces;
- 1 two-piece M3 nut-bar fit coupon, then 24 selected M3 nut bars (18
  required plus six preloaded spares);
- 8 B08C9Q2TGW zinc three-way corner connectors and their supplied M4 x 5 mm
  set screws;
- 4 B08D6T9CGN concealed zinc L-connectors and 8 supplied M5 x 6 mm set
  screws for the two fixture crossbars;
- 38 M3 machine screws, 38 ordinary M3 nuts, and wide washers when all six
  spare slot bars are parked under hardware: 8 gantry indexing interfaces,
  4 fixture mounts, 4 carrier-to-rail mounts, 4 carrier-to-link joints,
  2 placard rail mounts, 2 placard-to-strap joints, 8 reinforced-splice
  fasteners, and 6 parked spares;
- 16 supplied metal M5 T-nuts, M5 screws, and washers for the lower stacking
  registration slots, plus up to 8 more in the upper chassis for optional
  positive locks;
- optional B09GX9P79F 60 x 60 x 4 mm aluminum T-plates with supplied M5 x 8 mm
  screws/drop-in nuts only if the dry frame needs additional anti-rack support.

One node consumes all eight three-way connectors from one B08C9Q2TGW kit,
four concealed L-connectors, and six one-meter extrusions. The on-hand 16
three-way connectors, 20 L-connectors, and 20 extrusions support two complete
nodes, leaving 12 L-connectors and eight full sticks. The stock alone supports
three six-stick nodes with two full bars spare, but the on-hand three-way
connectors cap immediate production at two nodes.

## Current fabrication order

1. Print `gantry-upright-splice-reinforced-test-set.stl` broad-face down,
   without supports. It is the complete four-piece test joint: two physically
   selected 0.20 mm-clearance shells and two channel-matched internal bars.
2. Assemble that test around two sacrificial/offcut rail pieces with four M3
   screws, four wide washers, and four ordinary metal nuts. Verify alignment,
   screw access, free internal-bar insertion, and gentle hand-racking resistance.
3. Groups 02, 04, 05, and 06 are independent. Group 03 now includes the fixed
   rear-carrier links; print `rear-carrier-link-fit-pair.stl` and dry-fit its
   one top/one bottom link before committing a full node. Print Groups 07 and 08 only after the reinforced
   joint passes the physical gate.
4. Before sawing a complete node, measure all six stock sticks and witness one
   cut to confirm the conservative 3.2 mm kerf allowance. The fullest selected
   pattern consumes 963.6 mm. Mark all finished dimensions and waste sides;
   kerf is removed by the blade, never subtracted from a requested finished
   length.
5. Follow `CUT_LIST.md` exactly. The already cut 360.00 mm verification piece
   is a vertical post; its connector-capped 368 mm measurement is accepted.

## Measurements needed before final assembly

1. Actual length of all six selected stock sticks.
2. Actual saw-blade kerf, when convenient: the widest carbide-tooth width or
   the value printed on the blade, not feed speed. Until then CAD uses a
   conservative 3.2 mm solely for offcut accounting.
3. Complete: a 360.00 mm post plus two delivered connector caps measured
   approximately 368 mm outside-to-outside.
4. Complete: the rail key and end-loaded nut bar are physically selected—6.43 mm key,
   11.75 mm bearing face, and 6.46 mm deep face.
5. Complete: the one-notch gantry shell was selected, giving 0.20 mm external
   clearance. Remaining gate: test the complete reinforced shell/internal-bar
   joint before producing the eight production splice parts.
6. Perform one unpowered C270 framing check before the first populated stack.
7. Dry-fit one top and one bottom rear-carrier link, including wide washers at
   the carrier slots, before printing the remaining pair.

After those are recorded, dry-assemble one empty frame and obtain explicit
owner approval before populating or stacking it.
