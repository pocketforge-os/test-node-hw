# TrimUI Brick DUT cradle

This profile centers the portrait **TrimUI Brick (TG3040)** on a compact
180 × 205 mm carrier while preserving the fixture family's eight 4040-frame
zip-tie anchors. It deliberately uses the same physically accepted J-hook,
M3 captive-nut, and anti-rotation key mechanism as the Smart Pro family.
The added top margin carries the same centered outlined device-name box as the
Smart Pro carriers, using 14.4 mm bold lettering sized for the 0.8 mm nozzle.
The 124 mm-wide box leaves generous text padding without thinning the strokes.

The Brick is not uniformly thick. Its lower 20 mm region is 20 mm deep while
the upper body is 12 mm deep. A single shelf height would tilt the display or
load the rear shell, so the two printable hook profiles establish different
rear gaps but one shared front datum:

| Contact profile | Body depth | Rear gap above carrier | Passive throat | Front capture datum |
|---|---:|---:|---:|---:|
| Lower | 20.0 mm | 10.0 mm | 20.6 mm | 30.6 mm |
| Upper | 12.0 mm | 18.0 mm | 12.6 mm | 30.6 mm |

The shell front itself sits at 30.0 mm above the carrier. The additional
0.6 mm is passive hook clearance, not clamp pressure. The thick lower rear has
10 mm of finger space; the thin upper rear and shoulder-trigger region has
18 mm before trigger protrusion. A 56 × 86 mm service aperture keeps the back
reachable for manual trigger tests, wiring, and airflow.

## Retention decision

The first-print design uses five contacts rather than new mirrored corner cups:

- two lower hooks carry the device at 18 mm in from each bottom edge;
- two identical lower hooks contact the straight portion of the thick side
  shell at 14 mm above the bottom, with 0.6 mm lateral play; the complete
  9 mm contact band stays above the 8.5 mm corner transition;
- one 6 mm-wide upper hook prevents escape, with 0.45 mm play.

Four contacts therefore use the exact same `lower_hook` geometry. The single
`upper_hook` differs only where the stepped shell requires it: shelf height,
throat, width, support depth, and a shallow 1.2 mm front lip. This avoids a new
two-axis corner-cup mechanism during the first physical iteration and makes
every fit surface independently inspectable.

The upper hook is 17 mm from the device's left edge. Its 6 mm contact window is
well left of the centered 16 mm USB-host keep-out. Its 1.2 mm lip is below the
modeled 1.8 mm top bezel and must be confirmed against the physical glass before
printing the complete hook set.

## Measurements and visible assumptions

Owner source photo:
`/home/matt/Downloads/20260721_032150 (1).jpg`.

| Parameter | Value | Status |
|---|---:|---|
| Shell envelope | 72.8 × 110.75 mm | Owner drawing/caliper value |
| Thin upper depth | 12.0 mm | Owner drawing |
| Thick lower depth | 20.0 mm | Owner drawing |
| Thick lower region height | 20.0 mm | Owner drawing |
| Bottom corner transition | 8.5 mm | Owner drawing |
| Active screen proxy | 65.02 × 48.77 mm | 3.2-inch 4:3 calculation |
| Screen top margin | 1.8 mm | Photo-derived preview/contact assumption |
| Minimum rear access | 8.0 mm | Owner requirement; production uses 10 mm minimum |
| Upper USB keep-out | centered 16 mm window | Conservative port/cable proxy |

The default assembly renders the stepped shell, screen, selected top contact,
USB cable path, side/bottom connector areas, and rear triggers as transparent
background geometry. None of those preview/keep-out shapes can enter an STL.

## Printable parts

From `mechanical/dut-cradle-v1`:

```sh
make build/trimui-brick-carrier.stl
make build/trimui-brick-lower-hook.stl
make build/trimui-brick-upper-hook.stl
make build/trimui-brick-hook-set.stl
make build/trimui-brick-fit-coupon.stl
```

| File | Quantity / use |
|---|---|
| `trimui-brick-carrier.stl` | Print one |
| `trimui-brick-lower-hook.stl` | Print four |
| `trimui-brick-upper-hook.stl` | Print one |
| `trimui-brick-hook-set.stl` | Optional arranged alternative containing four lower hooks and one upper hook |
| `trimui-brick-fit-coupon.stl` | Print first: one lower hook, one upper hook, and one carrier mount coupon |

The source's `PART` selector accepts `assembly`, `plate`, `lower_hook`,
`upper_hook`, `hook_set`, and `fit_coupon`.

## Hardware and assembly

- 5 × M3 × 12 mm pan-head screws;
- 5 × M3 nuts;
- 5 × M3 washers under the carrier;
- optional 0.5–1 mm felt or TPU contact pads;
- 8 heavy-duty zip ties for the 4040 anchors.

1. Print the fit coupon or one lower and one upper hook first. Confirm the
   owner-validated 5.6 mm nut pocket and both passive shell fits.
2. Install the two bottom hooks loosely and lower the Brick onto their rear
   shelves. Do not use screw torque to squeeze the shell.
3. Bring the two lower side datums inward with visible play, then lock their
   screws. They locate the Brick but must not clamp it.
4. Install the narrow upper hook last. Confirm the front lip touches only bezel
   and remains clear of active pixels and the top USB-host path.
5. Confirm the screen is parallel to the plate, the rear triggers are free, a
   finger reaches through the service aperture, and every side/bottom port and
   control remains usable.

## Print and validation

- PETG preferred; no supports.
- Carrier flat with labels upward.
- Hooks are exported on their broad strong side; do not auto-orient upright.
- Start at 0.30–0.40 mm layers for the 0.8 mm nozzle, 4 perimeters, 5 top and
  bottom layers, and 20–30% gyroid infill.

```sh
make preview
make validate
```

Validation covers parser/evaluation lint, manifold meshes, Prusa bed bounds,
preview/export isolation, the 8 mm minimum rear-access rule, and exact equality
of the upper/lower front contact datums. A negative label-clearance guard also
proves that an undersized plate is rejected rather than allowing the centered
top title box to enter either 4040 attachment slot. Final closure still
requires the owner's explicit physical fit and webcam-view confirmation.
