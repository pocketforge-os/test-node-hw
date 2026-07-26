# PocketForge 2020 test-node chassis

Parametric OpenSCAD source for the reusable mechanical frame around one
PocketForge test node. The chassis carries:

- a movable electronics/webcam fixture on a two-upright gantry;
- a fixed device-specific DUT carrier on the shared optical axis;
- an operator-side power strip and replaceable device placard; and
- non-load-bearing stacking registration tabs and repositionable cable
  anchors.

The handheld is the **device under test (DUT)**. This surrounding assembly is
the **test-node chassis**.

The fleet-standard envelope is **346 W × 358 D × approximately 368 H mm**,
with **306 W × 318 D × 328 H mm** clear inside. One chassis uses six nominal
1 m sticks of 20 × 20 mm extrusion.

## Coordinate contract

Avoid “front” and “back”; those reverse with the observer.

- `Y=0`: operator-side outside plane.
- Increasing `Y`: toward the DUT and wall.
- `Y=358`: device-side outside plane.
- Left and right: viewed by an operator looking through the chassis toward the
  DUT.

The electronics fixture defaults to gantry centerline `Y=75`. The fixed DUT
carrier is on the device-side width rails. The power strip is inside the lower
operator-side width rail. The placard hangs below the upper operator-side width
rail.

## Accepted hardware and interfaces

The geometry is calibrated to the delivered hardware, not to a generic “2020”
assumption:

- SeekLiny B0DY7FKKMT 20-series extrusion, measured 20.00 mm face-to-face;
- measured slot mouth 6.73 mm, depth approximately 6.48 mm, widest pocket
  12.15 mm, lip depth 1.66 mm, and deep channel width 6.66 mm;
- BLCCLOY B08C9Q2TGW metal three-way end connectors;
- BLCCLOY B08D6T9CGN concealed metal L-connectors;
- ordinary metal M3 nuts measuring 5.36 mm across flats × 2.30 mm thick;
- face-loaded M5 drop-in T-nuts with low-profile M5 × 10 mm button-head
  screws and washers no larger than 10 mm OD for registration tabs and cable
  anchors; and
- Logitech C270 HD webcam, conservatively modeled from its 55° diagonal FOV.

The outer-frame and stacking load path is aluminum plus metal connectors.
Printed channel bars, gantry plates, carrier links, and registration tabs are
light-duty alignment/mounting parts. Never substitute a printed connector into
the outer-frame or vertical stacking load path.

## Aluminum cut list

| Part | Quantity | Finished length |
| --- | ---: | ---: |
| Outer vertical posts | 4 | 360 mm |
| Outer width rails | 4 | 306 mm |
| Outer depth rails | 4 | 318 mm |
| Fixture-gantry upright halves | 4 | 164 mm |
| Fixture-gantry crossbars | 2 | 306 mm |

The generated, connector-aware six-stick assignment is committed in
[`CUT_LIST.md`](CUT_LIST.md). Regenerate it with:

```sh
make refresh-cut-list
```

## Canonical print workflow

New chassis builds use these stable outputs:

| Batch | Output | Contents | Slicer exception |
| --- | --- | --- | --- |
| 00 | `production-batch-00-calibration.stl` | Rail key, channel-bar candidates, placard slide | Conditional after a process, material, printer, or extrusion change |
| 01 | `production-batch-01-ironed-interfaces.stl` | 28 short channel bars and four long splice bars | Iron topmost surfaces |
| 02 | `production-batch-02-splice-collars.stl` | Two full-wrap gantry collars | Print upright as exported |
| 03 | `production-batch-03-movable-mounts.stl` | Gantry plates, fixture spacers, carrier links | None |
| 04 | `production-batch-04-frame-hardware.stl` | Eight 18 × 92 × 4 mm registration tabs, placard mounts, power-strip blocks | None |
| 05 | `production-batch-05-placard-holder.stl` | Reusable placard holder | None |
| 06 | `production-batch-06-device-nameplate.stl` | Device-name plate only | Print white; change to black at 2.4 mm |
| 07 | `production-batch-07-wire-management.stl` | Eight rail-mounted zip-tie anchors | None |

All exported geometry is already in a support-free orientation and fits the
conservative 247 × 207 mm Prusa printable envelope. The accepted process is
ABS, 0.8 mm nozzle, 0.4 mm layers, at least three perimeters, at least four
top/bottom layers, 20–30% infill, supports disabled, and 100% scale. Do not
auto-orient or auto-arrange a production batch.

Build all production batches:

```sh
make batches
```

Build the optional calibration bed:

```sh
make calibration
```

Individual, stable replacement-part exports remain available through:

```sh
make replacements
```

## Captive M3 channel bars

The accepted short carrier is 18 mm long, 11.75 mm across the bearing face,
and 6.46 mm at the deep face. It captures an ordinary metal M3 nut in an open
5.60 × 2.80 mm hex pocket. Its broad solid face points toward the visible slot
mouth; the open nut pocket points toward the extrusion center. The compact
18 mm length stays inside the 20 mm fixture-upright landing envelope; the
superseded 30 mm handling-bar version can interfere at those joints.

The part is deliberately wider than the slot mouth. Load it through a cut rail
end before installing the end connector. Pull the nut squarely into the pocket
with an M3 screw and washer; do not glue or encapsulate it.

Batch 01 provides 28 short bars: 22 use-now mount positions and six parked
replacement bars. The authoritative rail/face preload map is in the handbook
assembly guide. Do not close a rail end until that map balances to 28.

## Stacking registration tabs

Batch 04 contains eight identical **18 × 92 × 4 mm** tabs, two for each upper
corner. The 18 mm width stays 1 mm inside each edge of a 20 mm rail face. Each
tab retains the established 60 mm lower-chassis engagement and screw-slot
centres at 12 and 28 mm, then projects 32 mm above the aluminum stack
interface. That projection spans the complete bottom rail of the chassis above
and continues 12 mm beside its corner post.

Install each tab to the lower chassis with two face-loaded M5 sets. After an
upper chassis is fully seated aluminum-to-aluminum, its third hole aligns with
the outward groove center of the upper chassis's bottom rail, 10 mm above the
interface. One additional face-loaded M5 set per tab then positively locks the
pair. The printed tabs provide lateral registration only; they never carry the
vertical stack load.

## Rail-mounted wire management

Batch 07 provides a starter set of eight identical anchors. Each
**32 × 18 × 8.8 mm** anchor bolts to any exposed 2020 rail face with one
face-loaded M5 T-nut, one low-profile M5 × 10 mm button-head screw, and one
flat washer no larger than 10 mm OD. Nothing is preloaded through a cut rail
end.

Two rounded **5.6 × 2.4 mm** transverse tunnels accept common zip ties up to
4.8 mm wide × 1.6 mm thick. Thread one tie through either tunnel, or use both
for a wider bundle. Print the broad rail-contact face on the bed with supports
disabled. Tighten the M5 screw only enough to stop the anchor from sliding,
and leave the tie loose enough that cables can move slightly under a fingertip.

These are routing aids, not strain relief, structural clamps, or stack
hardware. Their positions and final count follow each DUT harness. The
canonical eight-piece bed is intentionally separate so it can be repeated or
omitted without reprinting frame hardware; individual and eight-piece
replacement exports are also available.

## Fixture-upright splice

Each 328 mm gantry upright uses two 164 mm aluminum halves, one accepted
full-wrap collar, and two collar-specific double-nut bars:

- print the collar standing on its indexed open end;
- insert the unmarked 12.8 mm end of each long bar first;
- leave the one-scallop 16 mm end at the aluminum butt seam;
- butt both cuts fully;
- slide the collar 40 mm across the seam; and
- install four short M3 screws and wide washers only after all captive nuts
  align.

The collar and bars were physically fit-validated in the lab's ABS process.
They are for the light fixture gantry only.

## Source layout

- `pocketforge-node-chassis.scad`: assembly, production beds, replacement
  parts, guide scenes, semantic web-model layers, and assertions.
- `lib/pf-2020.scad`: self-contained measured extrusion visualization.
- `scripts/cutlist.py`: deterministic cut-list and stock assignment.
- `scripts/build_handbook_model.py`: semantic GLB assembly for the handbook.
- `scripts/build_handbook_batch_model.py`: canonical-bed STL conversion plus
  named multi-material layers for interactive handbook print previews.
- `scripts/handbook-model-requirements.txt`: pinned mesh-builder dependencies.
- `Makefile`: the supported export and validation interface.

The presentation imports the authoritative fixture/carrier STLs from their
sibling CAD projects. The TrimUI Smart Pro visual model is fetched from a
pinned platform commit and verified by SHA-256. Production STL exports never
contain presentation-only device geometry or camera-frustum overlays.
The installed Banana Pi BPI-M2 Zero V1.0 is carried through as five semantic
fixture layers, preserving its blue PCB, dark packages/header, metal ports and
shield, gold contacts, and pale silkscreen in both static renders and the
interactive handbook GLB.
The installed ACEIRMC ESP32-S3 SuperMini / HW-747 V0.0.2 is carried through as
six more semantic fixture layers: black PCB, dark ICs/buttons, metal USB-C and
switch frames, gold contacts, red ceramic antenna, and pale silkscreen. The
mesh retains the fixture's physical 18.50 × 23.67 mm envelope with USB-C
pointing down toward its service corridor.
The semantic model and static previews split the white placard insert from its
black raised device-name labels at `placard_insert_thickness`. The production
nameplate remains one fused STL on its own bed: print white through 2.4 mm,
then change to black for the raised text.

## Build and validate

```sh
make validate
```

That command:

- lints all repository OpenSCAD sources;
- exports and bounds-checks every production and replacement STL;
- renders the assembly and guide scenes;
- exercises routing, optical-FOV, gantry-travel, channel-bar, and cable-anchor
  negative guards;
- regenerates the cut list and compares it byte-for-byte with `CUT_LIST.md`;
  and
- verifies the pinned device model.

Generate the handbook's static scenes, eight interactive print beds, and
semantic full-chassis model:

```sh
python3 -m venv /tmp/pf-chassis-model-venv
/tmp/pf-chassis-model-venv/bin/pip install \
  -r scripts/handbook-model-requirements.txt
make PYTHON=/tmp/pf-chassis-model-venv/bin/python handbook-assets
```

Generated artifacts live under `build/` and are not committed. The public
handbook pins an immutable `test-node-hw` revision and regenerates them in CI,
preventing stale CAD visuals from being published. Every protected-`main`
change under `mechanical/**` also triggers `handbook-cad-refresh.yml`, which
advances the handbook's exact CAD gitlink through its own reviewed PR.

The static scene set includes one completed-state render for each major
assembly section plus focused panels for hidden splice hardware, concealed
gantry connectors, captive-nut preparation, exact per-rail preload counts,
the physical identity and lifecycle of parked replacement bars, rail
orientation, corner topology, assembly motion, positioning datums, carrier-link
selection, fixture spacing, optical orientation, final frame hardware, and the
face-loaded cable-anchor/tie path.
Keep those panels derived from the production modules rather than redrawing
their geometry independently.

## Assembly documentation

The novice-safe parts list, print settings, preload map, cutting order,
illustrated assembly, and unpowered verification gates live in the
[PocketForge handbook](https://pocketforge-os.github.io/handbook/hardware/test-node-chassis/).
Keep process instructions there rather than restoring development chronology
to this engineering README.

## Safety boundary

- Keep the DUT, programmable supply, USB power, battery emulator, and mains
  power disconnected during mechanical fabrication.
- Clamp extrusion, use an aluminum-rated blade, wear eye/hearing protection,
  and deburr every cut.
- Print ABS with a suitable enclosure and ventilation.
- Stack no more than two populated nodes until a load test establishes a rated
  count, and positively restrain the stack against tipping.
- Printed registration tabs locate stacked frames laterally; aluminum carries
  vertical load.
- Printed cable anchors organize a loose harness only. Do not use them as
  connector strain relief, overtighten a zip tie, or route a cable across a
  sharp rail end.
