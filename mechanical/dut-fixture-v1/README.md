# PocketForge DUT fixture plate v1

This is the parametric replacement for the original wood-mounted DUT harness: a **DUT fixture plate**
(also reasonably called an electronics mounting tray or tooling plate) sized for a Prusa i3 MK3S.
It carries the complete current harness while keeping every uncertain physical measurement editable near
the top of [`dut-fixture.scad`](dut-fixture.scad).

## Print this first

Do **not** spend a full plate's worth of filament before checking printer-specific fit:

```sh
make build/fit-coupon.stl
```

Print `build/fit-coupon.stl` flat, without supports. It contains:

- 1.6, 1.8, 2.0, 2.2, and 2.4 mm pilot bores in the production-size standoff;
- 6 × 2.0, 7 × 2.2, and 8 × 2.5 mm zip-tie slots;
- the production-size 12 × 5.5 mm 4040-frame tie slot;
- the initial webcam opening, 37.4 × 15.09 mm (the 37 × 14.69 mm measured rear housing plus 0.4 mm
  total clearance).

Choose the pilot that gives the desired thread-forming fit with the actual screw and filament. The
initial production choices are a 2.2 mm pilot for M2.5 screws and 1.7 mm for M2 screws. A printed
standoff is not a precision metal thread: for repeated servicing, drill/tap it after printing or change
the boss to suit a heat-set insert.

## Build and validate

OpenSCAD 2021.01 or newer is sufficient:

```sh
make preview       # angled + top-down component-envelope layout images
make lint          # fast parser/evaluation gate without a CGAL render
make validate      # production, coupon, split halves, joiner, and bed-bound checks
```

Pull requests touching `*.scad` run the repository-wide equivalent through the
`OpenSCAD lint` GitHub check, parsing and evaluating every OpenSCAD source before merge. The wrapper
explicitly rejects `ERROR:` diagnostics even when OpenSCAD incorrectly returns a zero process status.

Generated files live under `build/` and are intentionally not committed. The production STL is
`build/pocketforge-dut-fixture-v1.stl`.

No container is required for this: OpenSCAD is a single distro package, the source is portable, and
the stdlib-only bounds validator removes Python dependency drift. A container would add substantially
more machinery than determinism here.

## Layout and print settings

- Production plate: **200 × 247 × 3.2 mm** in the source. Rotate it 90° in the slicer; the resulting
  247 × 200 mm bed footprint retains 1.5 mm on each long-axis edge and 5 mm on each short-axis edge.
  The CAD and mesh checks treat that inset **247 × 207 mm** area—not the advertised 250 × 210 mm
  maximum—as the printable bed, following the first physical slicing attempt.
  Prefer the split build if the slicer or printer profile reserves additional end clearance.
- Exact CAD volume is about **160.7 cm³** before slicer compensation (roughly 199 g of PLA or 204 g
  of PETG if sliced effectively solid); the slicer's estimate remains authoritative.
- Print flat with standoffs upward; no support material.
- PLA is fine for layout verification. PETG is preferred for the final lab fixture because standoffs
  and cable-tie lands tolerate flex and heat better.
- Starting profile: 0.20 mm layers, 4 perimeters, 5 top/bottom layers, 15–20% gyroid infill. Use the
  split build for a brim or whenever the configured printable Y range is less than 247 mm.
- Eight 12 × 5.5 mm rounded slots mount the fixture to a 4040 frame: every corner has one horizontal
  and one vertical anchor, aimed toward its two adjacent rails. The 5.5 mm opening is intended for a
  common 4.8 mm heavy-duty cable tie; confirm the actual tie in the fit coupon before printing the
  plate. A 5 mm component keep-out remains around every frame slot for threading access.
- The webcam is centred left-to-right and kept near the plate centre. A machine-enforced 71 × 20 mm
  clear strip immediately below it is reserved for the owner's later secondary block.
- The upper powered USB/Ethernet hub has a 25 mm connector bay above it and an 18 × 12 mm cable
  corridor at its right end. Its lower and left sides reserve no unused cable space. Its two 7 × 2.7 mm
  tie-slot pairs include the extra 0.5 mm width requested after the first physical fit.
- The lower USB hub retains its physically proven bottom-edge placement. Its connector side opens
  beyond the plate, while centred 20 × 12 mm cable corridors reserve both narrow ends. The two hub
  bodies are separated only by the roughly 10 mm required for their independent zip-tie slots.
- The ESP32 is oriented with its 18.5 mm short edge toward the bottom of the plate. A centred 8.5 mm
  USB-C corridor reserves 20 mm below that edge. Four 3 × 3 mm tie slots sit 1.5 mm farther inward
  than the first print—two flanking USB-C and two mirrored on the opposite edge.
- The four-channel opto-isolated relay moves 10 mm left and sits on 26 mm-high, 9 mm-diameter
  standoffs, providing vertical clearance for the adjacent DP100 connections.

The plate can also be exported along the empty horizontal corridor as 200 × 150 mm lower and
200 × 97 mm upper sections. Both fit the MK3S without rotation:

```sh
make split
```

Print `plate-lower.stl`, `plate-upper.stl`, and three copies of `joiner.stl`. Join from below at the
three paired-hole locations using M3 × 10 screws, washers, and nuts. Those six joiner holes exist only
in the split exports; the one-piece plate remains solid across the seam. Split validation also requires
the upper part to retain the complete 29.2 mm fixture height so tall relay standoffs cannot be clipped.

## Measurement translation

The caliper notes measured mounting-hole spacing from the far outside edge of one hole to the far
outside edge of the other. The model converts those values with:

```text
centre spacing = far-edge spacing - hole diameter
```

| Item | Envelope / interface used | Status |
|---|---:|---|
| ALIENTEK DP100 | 94.6 × 62.2 mm | Owner-corrected physical measurement |
| DP100 tie positions | Two total: one on each short side, 21 / 25 mm down from top | Interpreted from sketch; parameterized |
| Webcam | 71 × 31.55 mm keep-out; 44.75 × 19.5 mm minimum aperture; 71 × 20 mm lower clear strip | Physically fit; printable opening gets 0.4 mm clearance |
| 4-channel relay | 51.85 × 72.70 mm; Ø3 holes; 45.03 × 66.93 mm centres; 26 mm standoffs | Measured; height owner-corrected after physical fit |
| BPI-M2-Zero | 29.90 × 65 mm; Ø2.6 holes; 23.00 × 58.36 mm centres | Converted from measured far edges |
| Boost converter | 43.16 × 21.23 mm; two Ø3 diagonal holes with 5 mm horizontal hole-edge-to-board-edge gaps (6.5 mm X centre insets), plus 1.1 mm top and 0.7 mm bottom gaps | Owner-corrected from physical fit and annotated measurement |
| MOSFET module | Ø2.2 holes, 13.38 mm centre spacing | Envelope and edge offset provisional |
| Antenna | 14.3 mm wide; mounted horizontally | Length/tie positions provisional |
| ESP32 | 23.67 × 18.5 mm; short-edge USB-C; four 3 × 3 mm short-edge tie slots | Envelope measured; slot fit owner-corrected after first print |
| Powered USB/Ethernet hub | 105.07 × 24 mm; ties 24 / 39 mm from ends; 25 mm top and 18 mm right service | Measured and physically fit |
| Unpowered USB hub | 105 × 24 mm; bottom connectors off-plate; 20 mm at both narrow ends | Estimated envelope; placement and service physically fit |
| 4040 frame anchors | Eight 12 × 5.5 mm rounded slots | Tunable; verify actual heavy-duty tie in coupon |

## Refinement workflow

1. Change only the named component parameters near the top of `dut-fixture.scad`.
2. Run `make preview validate`.
3. Reprint only the fit coupon when changing pilot, tie-slot, or webcam-aperture tolerances.
4. Print the plate only after the coupon and a paper/slicer layout review pass.

Preview component blocks are translucent interface envelopes, not cosmetic models. They are omitted
from every production STL and exist to expose inaccessible connectors and bad cable paths. The complete
preview subtree—including the component labels—uses OpenSCAD's `%` background modifier. Labels remain
visible in the editor but are intentionally absent from printable meshes because the lab printer uses
a 0.8 mm nozzle. Even a manual STL export from the default preview view contains only the printable
fixture. `make validate` proves that preview and production
exports have identical triangle geometry. Pairwise component spacing is also machine-enforced: every
render/export asserts at least 3 mm between envelopes; retention slots keep at least 1 mm from
components and one another; reserved webcam/hub service zones stay clear; and full M3 joiner screw-head
keep-outs may not intersect components, tie slots, or service zones. `make validate` includes an
intentional relay/antenna collision that must be rejected.
