# Anbernic RG353V DUT cradle

This profile centers the portrait **Anbernic RG353V** on a 180 × 205 mm
carrier with the PocketForge fleet's standard top title and eight 4040-frame
zip-tie anchors. It reuses the parametric M3 captive-nut/keyed hook mechanism
while introducing grip-aware lower contacts and a curved-bottom fit coupon.

The carrier deliberately keeps the device front on one plane. Owner calipers
show an 18.77 mm hook-capture depth. Every hook leaves 10 mm between the shell
and carrier so the rear grips and triggers remain unloaded and a finger can
reach behind the DUT:

| Contact profile | Body depth | Rear gap | Passive throat | Front capture datum |
|---|---:|---:|---:|---:|
| Lower grip-aware | 18.77 mm | 10.00 mm | 19.37 mm | 29.37 mm |
| Upper screen-safe | 18.77 mm | 10.00 mm | 19.37 mm | 29.37 mm |

The shell itself reaches a 28.77 mm front plane; the remaining 0.60 mm is
passive hook clearance, never intended as clamp pressure.

## Retention decision

Four passive contacts avoid the variable-depth grips and every documented side
control:

- two long-shelf lower hooks carry the curved bottom at the owner-measured
  points 31 mm inward from each side (21 mm apart). Their 8 mm contact widths
  preserve an exact 13 mm center cable lane for the bottom USB-C port;
- two shallow top retainers share those same 31 mm edge insets. Their 8 mm
  contact bands sit between 24 mm outer shoulder-trigger exclusions and a
  13 mm center port lane.

No hook touches a side edge: owner calipers show roughly 19 mm depth near the
upper controls and as much as 29 mm at the grip ends. This also leaves the
volume rocker, power/reset buttons, and both microSD slots unobstructed. The
1.2 mm top lips stay within the annotated 8 mm safe bezel band and the
provisional 3 mm screen margin. The lower contacts use 12 mm rear shelves to
reach beneath the strongly curved grip shell; their 3 mm lip overlap remains
inside the straight central bottom segment.

Both hook profiles use a 10.4 mm structural spine/base to provide a continuous
broad-face first layer. The anti-rotation nub starts 0.1 mm above the bed rather
than becoming a tiny support-requiring foot. Both shell-contact profiles are
8 mm wide, so the printability fix does not enlarge device overlap.

## Measurements and assumptions

Owner source photo:
`/home/matt/Downloads/20260721_042527.jpg`.

Manufacturer source:
<https://win.anbernic.com/product/349.html>.

| Parameter | Value | Status |
|---|---:|---|
| Front envelope | 83 × 126 mm | Anbernic nominal; owner caliper confirmation required |
| Hook-capture shell depth | 18.77 mm | Owner caliper |
| Lower grip/control-region height | 70 mm | Owner drawing; placement aid only |
| Upper safe bezel band | 8 mm | Owner drawing |
| Variable side/grip depth | 19–29 mm | Owner caliper; explicit no-contact region |
| Top/bottom hook centers | 31 mm inward from each edge | Owner drawing / symmetric design |
| Bottom USB-C cable lane | 13 mm centered | Design keep-out from manufacturer imagery |
| Top center port lane | 13 mm centered | Conservative design keep-out |
| Top outer shoulder exclusions | 24 mm from each side | Manufacturer imagery |
| Screen proxy | 77 × 55 mm | Height owner-annotated; width preview-only |
| Bottom corner radius | 14 mm | Photo-derived preview only |
| Rear-trigger exclusion | 60–82 mm from bottom | Conservative photo-derived keep-out |
| Left volume exclusion | 82–106 mm from bottom | Manufacturer imagery |
| Right power/reset exclusions | 79–108 mm from bottom | Manufacturer imagery |
| Right TF exclusions | 25–67 mm from bottom | Manufacturer imagery |
| Minimum rear access | 10 mm | Design choice for airflow/hand/wire access |

Green assembly ghosts show selected contact bands. Red ghosts show rear
trigger exclusions; orange ghosts show port/control exclusions. These, the
shell, screen, and controls are background-only
and cannot leak into production STLs.

## Printable parts

From `mechanical/dut-cradle-v1`:

```sh
make build/anbernic-rg353v-carrier.stl
make build/anbernic-rg353v-lower-hook.stl
make build/anbernic-rg353v-upper-hook.stl
make build/anbernic-rg353v-hook-set.stl
make build/anbernic-rg353v-fit-coupon.stl
```

| File | Quantity / use |
|---|---|
| `anbernic-rg353v-carrier.stl` | Print one after coupon acceptance |
| `anbernic-rg353v-lower-hook.stl` | Print two |
| `anbernic-rg353v-upper-hook.stl` | Print two |
| `anbernic-rg353v-hook-set.stl` | Optional arranged set of all four hooks |
| `anbernic-rg353v-fit-coupon.stl` | Print first: exact 21 mm bottom-mount spacing plus two lower hooks |

The source `PART` selector accepts `assembly`, `plate`, `lower_hook`,
`upper_hook`, `hook_set`, and `fit_coupon`.

## Coupon, hardware, and assembly

Print the fit coupon before the carrier. Install its two lower hooks with M3
hardware, place only the device bottom into them, and verify that the 12 mm
shelves reach stable shell material without rocking or loading a control. This
test confirms the unmeasured curved profile at low filament cost.

- 4 × M3 × 12 mm pan-head screws;
- 4 × M3 nuts;
- 4 × M3 washers beneath the carrier;
- optional 0.5–1 mm felt/TPU contact pads;
- 8 heavy-duty zip ties for the 4040 anchors.

After coupon acceptance, install both bottom hooks loosely, lower the DUT onto
them, then install the two top retainers with visible play. Tighten screws only
to lock hook position—never to squeeze the
shell. Confirm the display is parallel to the plate, triggers move freely, the
rear service aperture admits a finger, and every port/control—including both
microSD slots and bottom USB-C—remains usable.

## Print and validation

- PETG preferred; no supports.
- Carrier flat with labels upward.
- Hooks are already exported on their broad structural spine; do not
  auto-orient them upright.
- Start at 0.30–0.40 mm layers for the 0.8 mm nozzle, 4 perimeters, 5 top and
  bottom layers, and 20–30% gyroid infill.

```sh
make preview
make validate
```

Validation covers OpenSCAD lint, manifold and bed bounds, preview/export
isolation, exact hook-family front-datum equality, trigger/control/top and
bottom-USB keep-outs, minimum curved-shelf reach, and the flat first-layer
spine. Final closure still
requires owner confirmation of the actual 83 × 126 mm envelope, coupon fit,
full-carrier stability, unobstructed controls, and webcam visibility.
