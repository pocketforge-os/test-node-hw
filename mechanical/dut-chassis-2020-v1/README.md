# PocketForge 2020 test-node chassis

Parametric OpenSCAD source for the reusable mechanical frame around one
PocketForge test node. The chassis carries:

- a movable electronics/webcam fixture on either the proven two-upright
  gantry or the material-reduced matched upper/lower bar pair;
- a fixed device-specific DUT carrier on the shared optical axis;
- an operator-side power strip and replaceable device placard; and
- non-load-bearing stacking registration tabs and repositionable cable
  anchors.

The handheld is the **device under test (DUT)**. This surrounding assembly is
the **test-node chassis**.

The fleet-standard envelope is **346 W × 358 D × approximately 368 H mm**,
with **306 W × 318 D × 328 H mm** clear inside. The proven gantry chassis uses
six nominal 1 m sticks of 20 × 20 mm extrusion. The qualified dual-bar chassis uses
five when starting from new stock, or four new sticks plus the retained
356.4 mm legacy offcut.

## Chassis topology selection

`CHASSIS_VARIANT="legacy_gantry"` remains the OpenSCAD default and its
production meshes are regression-frozen. Device-pack generation selects the
topology from `../device-packs/device-layouts.json`; do not choose it by hand.

| Device | Layout | Fixture support | Status |
| --- | --- | --- | --- |
| TrimUI Smart Pro | `chassis-core-v2` | Proven gantry + stack-clear carrier links | Physically qualified by `tsp-t1zd.2`; `chassis-core-v1` remains frozen |
| TrimUI Smart Pro S | `chassis-dualbar-v1` | Two movable 306 mm fixture bars + four printed joints + four printed links | Physically qualified by `tsp-t1zd.2` |
| TrimUI Brick / TG3040 | `chassis-dualbar-brick-v1` | Unchanged qualified dual-bar frame + Brick-specific 180 × 205 mm carrier links | Prototype candidate; owner holder/framing gate remains open |

Both layouts preserve the same outer frame, fixture plate, plate Y/Z datum,
camera optical relationship, DUT carrier, placard, power strip, stacking
interface, and wire anchors; each record locks its accepted stacking-tab
revision. In the dual-bar layout, a continuous bar
spans the lower depth rails and another spans the upper depth rails. Four identical
71.5 mm keyed links join those bars directly to the plate's existing upper and
lower slots.

## Coordinate contract

Avoid “front” and “back”; those reverse with the observer.

- `Y=0`: operator-side outside plane.
- Increasing `Y`: toward the DUT and wall.
- `Y=358`: device-side outside plane.
- Left and right: viewed by an operator looking through the chassis toward the
  DUT.

The electronics fixture support defaults to centerline `Y=75`. The fixed DUT
carrier is on the device-side width rails. The power strip runs front-to-back
inside the lower operator-right depth rail. The placard hangs below the upper
operator-side width rail.

## Accepted hardware and interfaces

The geometry is calibrated to the delivered hardware, not to a generic “2020”
assumption:

- SeekLiny B0DY7FKKMT 20-series extrusion, measured 20.00 mm face-to-face;
- measured slot mouth 6.73 mm, depth approximately 6.48 mm, widest pocket
  12.15 mm, lip depth 1.66 mm, and deep channel width 6.66 mm;
- BLCCLOY B08C9Q2TGW metal three-way end connectors;
- BLCCLOY B08D6T9CGN concealed metal L-connectors for the legacy gantry
  crossbars only;
- ordinary metal M3 nuts measuring 5.36 mm across flats × 2.30 mm thick;
- face-loaded M5 drop-in T-nuts with low-profile M5 × 10 mm button-head
  screws and washers no larger than 10 mm OD for registration tabs;
- face-loaded M5 or M3 drop-in T-nuts with matching low-profile screws and
  washers no larger than 10 mm OD (M5) or 7 mm OD (M3) for cable anchors;
- ELEGOO B09ZQS2JRD four-channel 5 V optocoupled relay board, physically
  fitted at 72.70 × 51.85 mm with Ø3 mm mounting holes; and
- Logitech C270 HD webcam, reconstructed from Logitech's official product
  views and 55° diagonal FOV around the physically fitted fixture interface;
- Eightwood B0CRDVS774 / EWUA0205 114 × 15 mm MHF4 antenna;
- VIENON B09MLRPTT2 / Usb-001 100 × 30 × 10 mm four-port USB hub; and
- Smays B00L32UUJK / microb-hub-8152 powered USB/Ethernet hub, using the
  owner-fit 105.07 × 24 × 15 mm installed envelope.

The outer-frame and stacking load path is aluminum plus metal connectors.
Printed channel bars, gantry plates, dual-bar fixture links, carrier links,
and registration tabs are light-duty alignment/mounting parts. Never
substitute a printed connector into the outer-frame or vertical stacking load
path.

## Aluminum cut list — proven gantry

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

The scrap-first dual-bar assignment is committed separately in
[`CUT_LIST_DUALBAR.md`](CUT_LIST_DUALBAR.md). It removes **656 mm** of finished
fixture-support extrusion (1268 → 612 mm), a 12.61% reduction across the
complete chassis and a 51.74% reduction in fixture-support extrusion.
Regenerate and check it with:

```sh
make dualbar-cutlist
make validate-dualbar-cut-list-sync
```

If no qualifying offcut exists, cut both fixture bars from the fifth fresh
stick and retain its 381.6 mm remainder. For batch work, three 306 mm bars fit
on one stick (927.6 mm including kerfs, 72.4 mm remainder). Two qualifying
offcuts eliminate the fifth fresh stick; one offcut alone does not.

## Canonical print workflow

The chassis source owns a device-independent core-bed set for each layout. The
table below is the proven gantry set. The device-pack builder combines the
registered layout with the one carrier variant selected by the device profile;
do not manually mix a chassis topology, carrier label, hook set, and device
slug.

| Batch | Output | Contents | Slicer exception |
| --- | --- | --- | --- |
| 00 | `production-batch-00-calibration.stl` | Rail key, channel-bar candidates, placard slide | Conditional after a process, material, printer, or extrusion change |
| 01 | `production-batch-01-ironed-interfaces.stl` | 28 short channel bars and four long splice bars | Iron topmost surfaces |
| 02 | `production-batch-02-splice-collars.stl` | Two full-wrap gantry collars | Print upright as exported |
| 03 | `production-batch-03-movable-mounts.stl` | Gantry plates and fixture spacers | None |
| 04 | `production-batch-04-frame-hardware.stl` | Eight 18 × 92 × 4 mm registration tabs, placard mounts, power-strip blocks | None |
| 05 | `production-batch-05-placard-holder.stl` | Reusable placard holder | None |

Carrier links, the labeled carrier, the profile-defined retention set, device
nameplate, and eight starter wire anchors are device-pack outputs. The chassis still exposes its
nameplate and anchor beds as development examples, but they are not canonical
inputs for a newly onboarded device.

All exported geometry is already in a support-free orientation and fits the
conservative 247 × 207 mm Prusa printable envelope. The accepted process is
ABS, 0.8 mm nozzle, 0.4 mm layers, at least three perimeters, at least four
top/bottom layers, 20–30% infill, supports disabled, and 100% scale. Do not
auto-orient or auto-arrange a production batch.

Build the five shared chassis-core batches:

```sh
make batches
```

Build the four Pro S candidate core beds without changing the legacy outputs:

```sh
make dualbar
make validate-dualbar-batches
```

Candidate Batches 01–02 contain 28 short channel bars, four identical keyed
fixture links, and four accepted printed crossbar-joint plates. Batch 04 keeps
the owner-corrected stacking tab and Batch 05 remains normalized-geometry
identical to the proven layout. `make dualbar` also
regenerates the cut list and six review views under `build/dualbar/`. Generate
the complete device-selected candidate through the pack builder, not by mixing
these files manually:

```sh
python3 mechanical/device-packs/build_device_pack.py build \
  --device trimui-smart-pro-s \
  --mode full \
  --allow-unqualified
```

Build a deterministic full pack from the repository root:

```sh
python3 mechanical/device-packs/build_device_pack.py build \
  --device trimui-smart-pro \
  --mode full
```

Build the optional calibration bed:

```sh
make calibration
```

## Printable 90-degree checker

`right-angle-checker.scad` is a standalone, support-free L-square for setting
and checking the unpowered extrusion frame. The default is **150 × 150 ×
5 mm** with **25 mm-wide arms**. A 25 mm arm spans the full 20 mm extrusion
face with a small handling margin on each side. At 150 mm, one degree of
angular error opens a gap of about 2.62 mm at the leg end; half a degree is
still about 1.31 mm, so the tool is sensitive without consuming most of the
print bed.

The concave reference corner has a 4 mm circular debris relief, and the convex
reference corner has a 2 mm 45-degree chamfer. These deliberately leave a
virtual intersection instead of letting a rail burr, connector fillet, or
speck of plastic create a false reading. The remaining straight inside
reference span is 121 mm; the straight outside span is 148 mm.

Build the default STL and preview with:

```sh
make right-angle-checker
make validate-right-angle-checker
```

Generated files are `build/right-angle-checker-150mm.stl` and
`build/right-angle-checker-150mm.png`. Change `leg_length`, `arm_width`,
`thickness`, `inside_corner_relief_radius`, or `outside_corner_chamfer` in the
OpenSCAD Customizer for another size. The recessed label derives its dimension
from `leg_length`; set `show_label=false` for a completely plain top face.
Assertions preserve useful reference spans and enforce the configured printer
envelope.

Print it flat, label side up, at 100% scale with supports disabled. Use the
same material/process as the chassis parts, but let the bed and part cool
before removal so the legs stay flat. Keep brims away from the reference faces
when practical; otherwise remove the brim and any elephant foot completely
without rounding or selectively reshaping those faces. The broad bottom and
the unrecessed area of the top face both remain planar, so either face can be
used during calibration.

Use the two concave inside faces around an outside extrusion corner. Use the
two long convex outside faces to compare an inside corner. Before trusting a
new print, perform a flip test against the same known-straight datum: take a
reading or draw a line, reverse the checker, and repeat from the same datum.
Agreement indicates that the printed tool is square enough for comparison. A
gap that changes sides, or two lines that diverge, includes twice the
checker's own angular error; inspect for warp or reprint before adjusting the
frame. This is an assembly comparator, not a certified metrology instrument.

Individual, stable replacement-part exports remain available through:

```sh
make replacements
```

See [`../device-packs/README.md`](../device-packs/README.md) for coupon,
retrofit, full-pack, qualification, and generated-artifact policy.

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

Dual-bar Batch 01 instead provides exactly 28: six active outer-width-rail
locations, four active power-strip locations on the lower operator-right depth
rail, four active fixture-bar link locations, eight active printed-joint
locations (four in the fixture bars and four in the depth rails), four parked
depth-rail spares, and two parked fixture-bar spares. It contains no long
splice bar.
Keep the two inventories separate.

Current device packs select `CARRIER_LINK_REVISION="stack_clear_v2"`. Its 9 mm
end margin keeps every installed link 1 mm inside the chassis's lower and upper
stack planes, eliminating the former 2 mm projection. The frozen
`chassis-core-v1` pack remains reproducible with `legacy_v1` and its original
12 mm end margin.

## Stacking registration tabs

Batch 04 contains eight identical **18 × 92 × 4 mm** tabs, two for each upper
corner. The 18 mm width stays 1 mm inside each edge of a 20 mm rail face. Each
tab retains the established 60 mm lower-chassis engagement and screw-slot
centres at 12 and 28 mm, then projects 32 mm above the aluminum stack
interface. That projection spans the complete bottom rail of the chassis above
and continues 12 mm beside its corner post.

Install each tab to the lower chassis with two face-loaded M5 sets. In the
current qualified dual-bar layout and handbook output, after an upper chassis is fully
seated aluminum-to-aluminum, the center of its third hole sits 17 mm above the
interface. This owner-corrected datum is 7 mm above the former position so the
hole clears the delivered metal corner intrusion. One additional face-loaded
M5 set per tab then positively locks the pair. The printed tabs provide lateral
registration only; they never carry the vertical stack load.

The physically qualified legacy `chassis-core-v1` print pack remains immutable
at its accepted geometry. Generate the revised tab from the current dual-bar
pack or the individual stacking-tab target; do not substitute a newly generated
legacy Batch 04 for that accepted pack.

## Rail-mounted wire management

Batch 07 provides a starter set of eight identical M5 anchors. Each
**32 × 18 × 8.8 mm** anchor bolts to any exposed 2020 rail face with one
face-loaded drop-in T-nut, a matching low-profile button-head screw, and one
flat washer. Use the default M5 hole with a washer no larger than 10 mm OD, or
export an individual M3 version with `CABLE_ANCHOR_FASTENER="M3"` and use a
washer no larger than 7 mm OD. Nothing is preloaded through a cut rail end.

Two rounded **5.6 × 2.4 mm** transverse tunnels accept common zip ties up to
4.8 mm wide × 1.6 mm thick. Thread one tie through either tunnel, or use both
for a wider bundle. Print the broad rail-contact face on the bed with supports
disabled. Tighten the screw only enough to stop the anchor from sliding,
and leave the tie loose enough that cables can move slightly under a fingertip.

These are routing aids, not strain relief, structural clamps, or stack
hardware. Their positions and final count follow each DUT harness. The
canonical eight-piece bed is intentionally separate so it can be repeated or
omitted without reprinting frame hardware; individual and eight-piece
replacement exports are also available.

## Qualified dual-bar fixture suspension

Join one continuous 306 mm bar between the two lower depth rails and a second
between the two upper depth rails. Use two accepted printed indexing plates
per bar and never splice either one. Before closing the bar ends, load two
active short M3 bars plus one blue-tagged spare into each operator-facing
groove for the fixture links. Load two more active bars into the clear inward
horizontal groove of each fixture bar for the printed end joints: upward on
the lower bar and downward on the upper bar. Load one active joint bar into
the matching inward horizontal groove of each outer depth rail and park one
spare in each depth rail's side groove.

At each fixture-bar end, orient the printed joint plate on the clear interior
face between the upper and lower rails. Seat its perpendicular keys in the
depth-rail and fixture-bar slots, then clamp both holes through their active
short bars. The lower plates sit above the lower rails; the upper plates sit
below the upper rails. These plates index the movable fixture support only and
never enter the outer-frame or vertical stacking load path.

At each fixture-plate side:

1. seat one link's 16 × 6.43 mm rail key in an active short bar and clamp its
   round hole to that bar;
2. clamp the link's plate-side round hole through the corresponding existing
   fixture-plate slot with an ordinary M3 fastener, wide washers, and a metal
   locknut;
3. install lower links above the plate's lower slots and upper links below the
   upper slots so every link pulls toward the plate rather than peeling away;
4. repeat at all four corners with the same printed part; and
5. confirm both aluminum bars, four links, and the fixture plate form one
   square, rack-free assembly without a printed member spanning the plate.

The source and normalized fingerprints are physically qualified by
`tsp-t1zd.2`. The accepted assembly passed printed fit, real loaded
sag/racking, camera alignment, service access, powered harness operation, and
explicit owner acceptance on 2026-08-03. Any geometry change must use a new
candidate layout ID and repeat that physical gate.

## Fixture-upright splice — proven gantry only

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
- `right-angle-checker.scad`: standalone parametric extrusion squaring tool.
- `lib/pf-2020.scad`: self-contained measured extrusion visualization.
- `scripts/check_right_angle_checker.py`: exact reference-face and 90-degree
  STL geometry check for the default and a non-default parameter set.
- `scripts/cutlist.py`: deterministic cut-list and stock assignment.
- `scripts/build_handbook_model.py`: semantic GLB assembly for the handbook.
- `scripts/build_handbook_batch_model.py`: canonical-bed STL conversion plus
  named multi-material layers for interactive handbook print previews.
- `scripts/handbook-model-requirements.txt`: pinned mesh-builder dependencies.
- `Makefile`: the supported export and validation interface.

The presentation imports the authoritative fixture/carrier STLs from their
sibling CAD projects. The accepted TrimUI Smart Pro S visual model is fetched
from a pinned platform commit and verified by SHA-256. Production STL exports
never contain presentation-only device geometry or camera-frustum overlays.
The installed ELEGOO B09ZQS2JRD relay board is carried through as six semantic
fixture layers: blue PCB, blue relay/terminal bodies, dark optocouplers and
drivers, metal screws/pins, red status LEDs, and pale markings. Its exact
51.85 × 72.70 mm installed envelope retains four relay channels, twelve screw
terminals, the measured mounting registration, and a +X terminal-bank
orientation.
The installed HiLetgo B07BNHR4HW / Flying-Fish XL6009 boost module is carried
through as five semantic fixture layers: blue PCB, dark
regulator/470-marked inductor/passives, blue W103 adjuster, metal
capacitors/pads/leads/screw, and pale markings. Its exact 43.16 × 21.23 ×
14.00 mm installed envelope retains the measured diagonal Ø3 mm mounting
registration, with IN on −X and OUT on +X.
The installed Ceksezx B0FMJH3DML / MTSD001 dual-MOSFET switch is carried
through as six semantic fixture layers: blue PCB, blue terminal bodies, dark
PD4184 MOSFETs/passives, metal screws/pads/leads, indicator LED, and pale
markings. Its exact 34 × 17 × 12 mm populated envelope remains centred in the
accepted 35 × 18 mm fixture envelope; the measured Ø2.2 mm mounting
registration is unchanged, and its four-position terminal bank faces −X.
The installed ALIENTEK B0CWRG6YFM / DP100 is carried through as seven semantic
fixture layers: dark enclosure, black panel/ports/seam/vents, gray controls,
IPS screen, red positive-output/status accents, metal banana/USB interfaces,
and pale markings. Its owner-measured 94.60 × 62.20 × 17.20 mm body remains
the fixture fit contract, while a 5.80 mm banana projection produces the
manual's 100.40 mm overall length. Outputs face −X, USB-C/USB-A face +X, and
the display/buttons/wheel face −Y.
The installed Banana Pi BPI-M2 Zero V1.0 is carried through as five semantic
fixture layers, preserving its blue PCB, dark packages/header, metal ports and
shield, gold contacts, and pale silkscreen in both static renders and the
interactive handbook GLB.
The installed ACEIRMC ESP32-S3 SuperMini / HW-747 V0.0.2 is carried through as
six more semantic fixture layers: black PCB, dark ICs/buttons, metal USB-C and
switch frames, gold contacts, red ceramic antenna, and pale silkscreen. The
mesh retains the fixture's physical 18.50 × 23.67 mm envelope with USB-C
pointing down toward its service corridor.
The installed Logitech C270 is carried through as five semantic layers:
dark-gray shell/articulated clip, black bezel/lens/cable, lens glass, lime
activity LED, and pale markings. The physically fitted body stays centered on
the fixture while its left-offset lens remains registered to the DUT optical
axis.
The final three component proxies are replaced with thirteen semantic layers.
The Eightwood EWUA0205 preserves its 114 × 15 mm paddle, routed coax, MHF4
connector, and markings. The VIENON Usb-001 preserves its 100 × 30 × 10 mm
black shell, four −Y USB-A ports, blue indicator, and +X fixed lead. The Smays
microb-hub-8152 preserves its 105.07 × 24 × 15 mm white shell, +Y USB bank,
−X RJ45, +X OTG lead, −Y DC input, and the installed DC plug/cable rising
through the six-millimetre inter-hub gap before crossing above the VIENON
lead. The black VIENON body sits 23.65 mm left of the white Smays body while
its presentation ties remain registered to the unchanged printable slots.
The old `fixture-components` layer now contains retention ties only.
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
- exports and verifies the default and a non-default right-angle checker;
- renders the assembly and guide scenes;
- exercises routing, optical-FOV, gantry-travel, channel-bar, and cable-anchor
  negative guards;
- regenerates the cut list and compares it byte-for-byte with `CUT_LIST.md`;
  and
- verifies the pinned device model.

Generate the handbook's source scenes, interactive print beds, and semantic
full-chassis model:

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

The canonical `pocketforge-test-node.glb` and `hero.png` are always generated
with `CHASSIS_VARIANT="dualbar_v1"` and
`EXAMPLE_DEVICE_VARIANT="smart_pro_s"`. The GLB retains separate semantic
layers for the actual handheld shell/controls/screen, carrier and hooks,
populated fixture components, webcam and field of view, frame and suspension,
power strip, placard, and registration hardware. Its provenance binds the
device slug, layout record, candidate acceptance reference, pinned device
model commit/hash, every layer hash, and the final model hash.

The source scene set also includes one completed-state render for each major
assembly section plus focused panels for hidden splice hardware, concealed
gantry connectors, captive-nut preparation, exact per-rail preload counts,
the physical identity and lifecycle of parked replacement bars, rail
orientation, corner topology, assembly motion, positioning datums, carrier-link
selection, fixture spacing, optical orientation, final frame hardware, and the
face-loaded cable-anchor/tie path.
Keep those panels derived from the production modules rather than redrawing
their geometry independently.

The novice handbook walkthrough has a separate ordered 17-image contract for
the Smart Pro S dual-bar chassis. Generate just that sequence with:

```sh
make guide-dualbar-assembly-steps
```

The stable outputs are `build/handbook/assembly-01-channel-bar.png` through
`assembly-17-final.png`. Every render target pins both `dualbar_v1` and
`smart_pro_s`; the target-contract test rejects a missing/reordered image or a
recipe that points back to a retired gantry assembly scene.

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
