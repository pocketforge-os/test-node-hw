# Powkiddy X55 DUT cradle

This profile centers the landscape **Powkiddy X55** on a 247 × 175 mm carrier
with the PocketForge fleet's top title and eight 4040-frame zip-tie anchors.
It reuses the keyed M3 captive-nut hook mechanism while giving the X55 a traced
curved-shell proxy, three edge-specific hook profiles, and explicit safe bands
for the crowded top and bottom edges.

The owner trace, not the marketing box, governs retention. The front shell is
210 mm wide at its grips, 200 mm immediately below the shoulder keys, and
88.76 mm high. Powkiddy publishes a larger 212.5 × 94.5 × 19 mm overall
envelope. The preview carries both facts: the dark shell follows the traced
contact envelope, while its shoulder stacks reach toward the published outer
envelope. Production hooks never use the manufacturer XY box as a fit surface.

## Retention decision

Six passive contacts leave every port and control accessible:

- two 8 mm bottom supports flank the owner-annotated 58 mm dual-microSD
  exclusion. The left support is centered in the 28 mm clear region and the
  right support in the 20 mm clear region;
- two 8 mm top retainers occupy measured control-free gaps. The left gap is
  the 16.36 mm span between the 7.8 mm power key and the following 9 mm port.
  The right gap is the annotated 15 mm span inboard of the reset/control band;
- two loose lateral datums touch the shell at its 210 mm widest tangent. The
  owner confirmed both entire short ends are unobstructed.

Bottom shelves are 10 mm deep, side shelves 8 mm, and top shelves 7 mm. Their
front lips are respectively 3.0, 2.4, and 1.6 mm, keeping the top retainers
shallow around the display and shoulder controls. All three profiles share one
19.6 mm passive throat: Powkiddy's published 19 mm depth plus 0.6 mm play.
They also share a 10 mm carrier-to-shell rear gap. That depth is intentionally
provisional until owner calipers confirm the local top, bottom, side, and
maximum rear/trigger depths.

Green ghosts in the assembly show selected contact regions. Orange ghosts are
top buttons/connectors measured by the owner; red ghosts are shoulder and
dual-TF exclusions. Shell, screen, controls, shoulder keys, keep-outs, and
installed hooks are OpenSCAD background geometry and cannot enter an STL.

## Dimensional provenance

Owner sources:

- `/home/matt/Downloads/20260721_051032.jpg` — traced outline and caliper chain;
- `/home/matt/Downloads/20260721_051006.jpg` — physical DUT aligned to trace.

Manufacturer source:
<https://powkiddy.com/products/powkiddy-x55-5-5-inch-1280-720-ips-screen-rk3566-handheld-game-console-jelos-system-open-source-retro-console-childrens-gifts>.

No reusable X55 STEP/STL shell was located in the public model repositories
searched during design. The proxy therefore combines owner measurements with
official front, rear, top, bottom, and angled product imagery; it does not
pretend that a photograph-derived decorative surface is a metrology scan.

| Parameter | Value | Status |
|---|---:|---|
| Maximum traced shell width | 210 mm | Owner measurement; fit authority |
| Width immediately below triggers | 200 mm | Owner measurement |
| Traced shell height | 88.76 mm | Owner measurement; fit authority |
| Published overall envelope | 212.5 × 94.5 × 19 mm | Powkiddy reference only |
| Modeled local capture depth | 19 mm | Published proxy; owner caliper needed |
| Hook throat | 19.6 mm | Derived proxy: 19 + 0.6 mm passive play |
| Rear carrier gap | 10 mm | Fleet service datum; max-depth check needed |
| Bottom central exclusion | 58 mm | Owner measurement; dual TF cards |
| Bottom-left safe span | 28 mm | Owner measurement |
| Bottom-right safe span | 20 mm | Owner measurement |
| Top-left safe span | 16.36 mm | Owner measurement |
| Top-right safe span | 15 mm | Owner measurement / interpreted adjacency |
| Left power key | 7.8 mm | Owner measurement |
| Left following port | 9 mm | Owner measurement |
| Right reset/control band | 4.72 mm | Owner endpoints: 33.87–38.59 mm |
| Screen active proxy | 121.78 × 68.50 mm | Derived from published 5.5-inch 16:9 panel |
| Service aperture | 176 × 62 mm | Design choice; leaves perimeter structure |

The X55 source encodes these as named intervals with assertions. Correcting
one interpretation does not silently move the other supports.

## Printable parts

From `mechanical/dut-cradle-v1`:

```sh
make build/powkiddy-x55-carrier.stl
make build/powkiddy-x55-bottom-hook.stl
make build/powkiddy-x55-top-hook.stl
make build/powkiddy-x55-side-hook.stl
make build/powkiddy-x55-hook-set.stl
make build/powkiddy-x55-fit-coupon.stl
```

| File | Quantity / use |
|---|---|
| `powkiddy-x55-carrier.stl` | Print one after depth and coupon acceptance |
| `powkiddy-x55-bottom-hook.stl` | Print two |
| `powkiddy-x55-top-hook.stl` | Print two |
| `powkiddy-x55-side-hook.stl` | Print two |
| `powkiddy-x55-hook-set.stl` | Optional arranged set of all six hooks |
| `powkiddy-x55-fit-coupon.stl` | Print first; production bottom spacing and two hooks |

The source `PART` selector accepts `assembly`, `plate`, `bottom_hook`,
`top_hook`, `side_hook`, `hook_set`, and `fit_coupon`.

## Coupon, hardware, and assembly

Do not print the full carrier until the four local shell depths and maximum
rear protrusion are confirmed. Once those measurements are encoded, print the
coupon first. Its bottom mounts reproduce the production 82 mm separation.

- 6 × M3 machine screws, final length chosen after depth confirmation;
- 6 × M3 nuts;
- 6 × M3 washers beneath the carrier;
- optional 0.5–1 mm felt/TPU contact pads;
- 8 heavy-duty zip ties for the 4040 anchors.

Install both bottom hooks loosely and set the DUT onto their shelves. Add the
side datums with visible play, then install the two top retainers last. Screws
lock hook position; they never squeeze the shell. Confirm both microSD cards,
every top connector, all four shoulders, the display, speakers, buttons, and a
finger behind the DUT remain unobstructed before frame installation.

## Print and validation

- PETG preferred; no supports.
- Carrier flat with labels upward.
- Hooks are exported on the same broad structural spine validated for the
  earlier fleet profiles; do not auto-orient them upright.
- Start at 0.30–0.40 mm layers for the 0.8 mm nozzle, 4 perimeters, 5 top and
  bottom layers, and 20–30% gyroid infill.

```sh
make preview
make validate
```

Validation covers OpenSCAD syntax, manifold and bed bounds, exact preservation
of the owner's 210/200/88.76 mm datums, the minimum rear service gap, top safe
bands, the 58 mm dual-TF exclusion, support-free hook first layers, and proof
that the high-fidelity preview cannot leak into production STLs. Closure still
requires owner coupon and full-carrier fit confirmation.
