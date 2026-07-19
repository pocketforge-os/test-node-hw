# PocketForge parametric DUT cradle v1

This is the camera-facing half of a PocketForge test harness: a reusable
**device carrier / DUT cradle** that fixes a handheld at a repeatable optical
datum without loading its controls, triggers, display, or exposed rear wiring.
The first profile is the **TrimUI Smart Pro S**.

The carrier is deliberately not a tight six-point vise. Two lower hooks carry
the device, the removable upper pair captures it, and the two lateral hooks are
loose datums. Every hook has a rear shelf, so the six perimeter contacts—not
the open PCB and not the shoulder triggers—establish a 6 mm carrier gap.

## Why separate parts

OpenSCAD modules are the template mechanism:

- [`lib/dut-cradle-library.scad`](lib/dut-cradle-library.scad) contains the
  reusable carrier fastener and J-hook geometry.
- [`trimui-smart-pro-s-cradle.scad`](trimui-smart-pro-s-cradle.scad) is the
  device profile and presentation/export wrapper: shell dimensions, optical
  offset, contact windows, hook poses, labels, and common 4040 datum.

A future handheld gets a new wrapper/profile while reusing the library. The
carrier envelope and eight corner frame anchors remain standardized; the
device outline, service aperture, safe contacts, and optical center may change.

`PART` selects independent printable objects:

| `PART` | Result |
|---|---|
| `assembly` | Default presentation; exports only the carrier because DUT, safe windows, and installed hooks are background geometry |
| `plate` | Carrier plate |
| `hook` | One J-hook, already laid on its strong printing side |
| `hook_set` | Six production J-hooks arranged for one print |
| `fit_coupon` | Three throat/nut variants plus the production screw-slot/keyway coupon |

## Print the coupon first

```sh
make build/fit-coupon.stl
```

The three hooks are ordered left-to-right:

1. 12.2 mm throat, 5.8 mm M3 nut pocket;
2. 12.6 mm throat, 6.0 mm M3 nut pocket (production default);
3. 13.0 mm throat, 6.0 mm M3 nut pocket.

The detached coupon plate contains the production 3.5 mm M3 adjustment slot
and shallow anti-rotation keyway. Check the actual device edge at all proposed
contact regions: the photographed DUT is open and wired, and the 12 mm value is
a local measurement rather than a guaranteed uniform shell thickness. A thin
0.5–1 mm felt or TPU contact pad is recommended for the final hooks.

## Build and validate

```sh
make preview
make validate
```

Generated STLs and PNGs live under `build/`, remain uncommitted, and are
published as a GitHub Actions artifact on relevant pushes. The main outputs are
`trimui-smart-pro-s-carrier.stl`, `j-hook.stl`, and `j-hook-set.stl`.

Validation parses every repository OpenSCAD source, renders all meshes, proves
the 247 × 200 mm plate fits the conservative 247 × 207 mm Prusa envelope,
rejects an undersized hook throat, and proves preview-only geometry cannot leak
into a carrier export.

## Hardware and assembly

- 6 printed J-hooks (PETG preferred);
- 6 × M3 nuts (coupon tests 5.8 and 6.0 mm across-flat pockets);
- 6 × M3 × 12 mm pan-head machine screws;
- 6 × M3 washers under the plate;
- optional thin felt/TPU pads at shell contacts;
- 8 heavy-duty cable ties for the 4040-frame anchors.

Assembly order:

1. Insert each nut from the top of its hook base.
2. Loosely install the two bottom hooks from the rear of the carrier. Their
   rectangular keys must enter the shallow guide channels.
3. Lower the DUT onto the two rear shelves. The screws lock hook position; do
   **not** tighten the hooks inward to squeeze the shell.
4. Set the side hooks with roughly 0.6 mm play and tighten them.
5. Install the top hooks last with roughly 0.45 mm play. These are the only
   hooks normally removed when servicing the DUT.
6. Confirm every trigger, button, connector, speaker/vent, wire, and the full
   display remains free before mounting the carrier to the 4040 frame.

M3 × 12 is the calculated starting length for a 3.2 mm carrier, 4.4 mm hook
base, washer, and 2.4 mm-class nut. Verify it on the coupon. The screw and nut
sit 8 mm outside the shell edge, so excess length cannot point into the DUT.

## Profile measurements and assumptions

| Parameter | Initial value | Status |
|---|---:|---|
| Shell envelope | 188.35 × 79.77 mm | Owner measurement |
| Local edge capture depth | 12.0 mm | Owner measurement; coupon required |
| Production hook throat | 12.6 mm | 0.6 mm passive clearance |
| Rear carrier gap | 6.0 mm | Design choice |
| Front lip overlap | 2.8 mm | Design choice; below screen margin |
| Rear service aperture | 158 × 52 mm | Design choice; leaves perimeter structure |
| Top-left safe window | 35.41–50 mm from left | Interpreted from nested sketch dimensions |
| Top-right safe window | 34–50 mm from right | Interpreted from nested sketch dimensions |
| Bottom safe windows | 24–35 mm from each end | Interpreted from nested sketch dimensions |
| Active screen proxy | 110.8 × 62.3 mm | Preview-only provisional estimate |
| Screen optical offset | [0, 0] | Independent, awaiting camera registration |

The paper sketch appears to mark each mountable region between the two nested
dimension endpoints; clamp centers use those interval midpoints. Green bars in
the assembly preview make this assumption visible. Adjust the four named safe
windows if that reading is wrong—nothing in the reusable hook changes.

## Print settings

- Carrier: flat, labels upward, no support; PETG preferred.
- Hooks: the STL already lays each hook on its broad side so layers run through
  the J profile; no support.
- Start at 0.30–0.40 mm layers for the 0.8 mm nozzle, 4 perimeters, 5 top/bottom
  layers, and 20–30% gyroid. Use the slicer's preview to verify the 1.2 mm-deep
  anti-rotation channels and 0.8 mm raised labels survive the selected layer
  height.
- The large central aperture is intentional: it saves material, improves
  airflow, keeps the open PCB/wiring untouched, and permits rear service.
