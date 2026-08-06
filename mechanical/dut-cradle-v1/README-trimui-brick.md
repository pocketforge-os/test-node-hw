# TrimUI Brick DUT cradle

This profile centers the portrait **TrimUI Brick (TG3040)** on a compact
180 × 205 mm carrier while preserving the fixture family's eight 4040-frame
zip-tie anchors. It deliberately uses the same physically accepted J-hook,
M3 captive-nut, and anti-rotation key mechanism as the Smart Pro family.
The added top margin carries the same centered outlined device-name box as the
Smart Pro carriers. Its 124 × 24 mm envelope stays fixed, while the device
name uses an 8.5 mm size proven to remain 2.4 mm inside every inner border
edge. The title and TOP/BOTTOM markings use regular-weight Liberation Sans
with only 0.35 mm of stroke expansion so their counters remain legible with
the 0.8 mm nozzle.

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

The five-contact design keeps the active retention simple while separating
weight support from edge capture:

- two rear-only bottom supports carry the device at 18 mm in from each edge;
  their short stems stop behind the bottom I/O insertion plane, so the TF,
  reset, USB-C, microphone, and audio openings remain accessible;
- two side hooks contact the straight portion of the thick side
  shell at 14 mm above the bottom, with 0.6 mm lateral play; the complete
  9 mm contact band stays above the 8.5 mm corner transition;
- one 6 mm-wide upper hook prevents escape, with 0.45 mm play.

The bottom supports reuse the same base, captive nut, key and rear shelf as
the side hooks but intentionally omit the continuous front stem and lip. The
side and upper hooks retain the shell with passive play; the supports carry
weight without occupying a port mouth. This avoids a new two-axis corner-cup
mechanism while making every fit surface independently inspectable.

All three parts retain a 10.4 mm-wide structural spine/base even though their
shell contacts remain 9 mm and 6 mm wide. That spine keeps one keyway datum and
puts a continuous broad face on the print bed. The anti-rotation key is 0.1 mm
above layer one rather than becoming a small support-requiring foot; the short
contact shelves bridge outward from the spine without support.

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
make build/trimui-brick-bottom-support.stl
make build/trimui-brick-side-hook.stl
make build/trimui-brick-upper-hook.stl
make build/trimui-brick-hook-set.stl
make build/trimui-brick-fit-coupon.stl
```

| File | Quantity / use |
|---|---|
| `trimui-brick-carrier.stl` | Print one |
| `trimui-brick-bottom-support.stl` | Print two |
| `trimui-brick-side-hook.stl` | Print two |
| `trimui-brick-upper-hook.stl` | Print one |
| `trimui-brick-hook-set.stl` | Optional arranged alternative containing two bottom supports, two side hooks, and one upper hook |
| `trimui-brick-fit-coupon.stl` | Print first: one of each contact part and one carrier mount coupon |

The source's `PART` selector accepts `assembly`, `plate`, `presentation_body`,
`presentation_labels`, audit-only `title_text`, `bottom_support`, `side_hook`,
`upper_hook`, `hook_set`, and `fit_coupon`. The two presentation parts exist
only to reproduce the material split in higher-level renders; print the fused
`plate` export.

## Hardware and assembly

- 5 × M3 × 12 mm pan-head screws;
- 5 × M3 nuts;
- 5 × M3 washers under the carrier;
- optional 0.5–1 mm felt or TPU contact pads;
- 8 heavy-duty zip ties for the 4040 anchors.

1. Print the fit coupon first. Confirm the 5.6 mm nut pocket, rear-only bottom
   support, side hook, and upper-hook passive shell fits.
2. Install the two bottom supports loosely and lower the Brick onto their rear
   shelves. Confirm their short stems remain behind the bottom connector plane.
   Do not use screw torque to squeeze the shell.
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
- Print the carrier body in white, then change to black at `plate_thickness`
  (3.2 mm), where the raised title, title-box border, and TOP/BOTTOM markings
  begin. The OpenSCAD assembly uses the same off-white/black material split.
- Hooks are exported on their broad strong spine; do not auto-orient upright.
  Their anti-rotation nub intentionally faces upward and begins 0.1 mm above
  the bed, so no support or slicer-generated raft should be needed.
- Start at 0.30–0.40 mm layers for the 0.8 mm nozzle, 4 perimeters, 5 top and
  bottom layers, and 20–30% gyroid infill.

```sh
make preview
make validate
```

Validation covers parser/evaluation lint, manifold meshes, Prusa bed bounds,
preview/export isolation, the 8 mm minimum rear-access rule, exact equality of
the upper/lower front contact datums, and a negative guard proving the bottom
supports cannot grow into the I/O insertion plane. A label-clearance guard
rejects an undersized plate, and a print-foot guard rejects any spine that
would let the anti-rotation key become the lowest feature. The registry-driven
title audit exports the locked 8.5 mm text mesh and checks its four inner-border
clearances. Final closure still
requires the owner's explicit physical fit and webcam-view confirmation.
