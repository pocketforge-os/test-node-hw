# PSU enclosure V3 — mechanical fit candidate

A complete mechanical redesign for the owner's 2026-10-28 request, tracked under
`tsp-bcx.21.45.3`. This candidate is for **unpowered fit review**. It is not an
approved powered enclosure or a production pack change. PR85 remains historical;
this branch builds on the merged, physically corrected component/coupon source
at `0b1e3b7` without changing those measurements.

## What changed

Three large parts — tray, rear panel and lid — plus a small removable rear-rail
bridge. The main walls, floor, lid and rear panel frame are 4 mm. The C14 cutout
sits in a local 1.2 mm island surrounded by the full rear panel, well away from
edges and corners. The panel is a continuous solid; it does not depend on tiny
boolean joins or a separate cassette edge. It prints exterior-face-down so the
thin island is three full 0.4 mm layers, not an upright thin-wall extrusion.

Two spaced right-rail ears and the rear-rail bridge make a triangular mounting
pattern. The bridge prints separately, broad face down, eliminating the large
tray's rear flange overhang. Its two tray screws are forward of the rear carrier
plate so a straight driver can reach them. The third screw enters the top slot
of the rear extrusion. Positive keys fit within the measured rail openings.

The lid and rear panel have overlapping joints. The panel's U-shaped overlap
extends 10 mm inward; the lid skirt is 3.2 mm thick and 4 mm deep. Nominal exterior
seating faces meet; 0.4 mm clearance lies behind the overlap. These are assembly
joints, not an IP seal. The only intentional external openings are component,
fastener and ventilation openings. Rendered and sampled sliced geometry shows
no unintended open seams; this is not a global minimum-wall certificate.

Offset front intake slots and a ribbed, double-layer roof vent provide an air
path around the PSU shell. The roof baffle sits 8.74 mm above the measured PSU
keepout. Offset openings block a normal straight-through line; this does not
establish a finger-probe rating or replace the required terminal shield. Cooling
performance remains untested. The roof baffle prints with short bridges between
ribs; ABS bridging and shrink still require a physical print check.

## Dimensions and fit provenance

All values are millimetres. Local +Y is rearward and +Z is up. Installed origin
is `[178,156,0]` in the source chassis coordinates.

| Item | Current geometry |
| --- | --- |
| Main case including lid | 148 X × 144 Y × 68 Z |
| PSU | ALT-1205T, nameplate **12 V / 5 A**, 110 × 77.5 × 36.86 |
| PSU placement | `translate([8,91.5,8]) rotate([0,0,-90])` |
| C14 faceplate | 50.3 horizontal × 31 vertical |
| Insertion profile | Approved 27 × 46.86 contour, +0.20 normal clearance |
| C14 face datum | X=63, Y=144, Z=38, facing rearward |
| Flange margins | 10.5 above, 18.5 below, 37.85 left, 59.85 right |
| Right rail screws | World Y=149.73 and 306, X=326 contact plane, Z=10 axes |
| Rear rail screw | World X=202, Y=348, vertical axis into top slot |
| Bridge-to-tray screws | World X=194 / 210, Y=324, vertical axes |
| Rail keys | 6.2 wide × 2.4 deep; measured opening 6.73 / slot depth 6.48 |
| Tray print envelope | 150.4 × 198.27 × 64 |
| Rear panel print envelope | 148 × 60 × 10 |
| Lid print envelope | 148 × 144 × 14.4, roof down |
| Bridge print envelope | 24 × 34 × 6.4, top face down |

The C14 is slightly left of centre to clear the chassis rear carrier link and
bottom rail. The original centred layout intersected the provisional plug
corridor by 2660.597 mm³. The first split-bridge screw placement also intersected
the rear plate's driver corridor; moving those screws 10 mm forward clears it.
These are checked failures corrected in the final geometry, not just visual
assumptions.

PSU hole centres remain the owner-finalized underside coordinates:
`(4.95,4.95), (25.3,30.9), (25.3,67), (53.3,67), (6.75,98.6)`.
The photos show threaded fittings on the PSU underside. Screws now enter from
below through 3.6 mm clearance bores. Each pad has a 7 mm head recess 2.4 mm deep,
a 7 mm upper fitting relief 2.4 mm deep, and a 3.2 mm bearing web between them.
The fitting projection and permitted screw penetration are unmeasured. The pad
is therefore a fit allowance, not a verified screw-length prescription. The
owner accepted the last corner-hole correction without another coupon print.

Measured component contracts and all corrections remain in
`lib/alt-1205t-power-supply.md` and `lib/iec-c14-fused-switch.md`. Private source
photos were inspected without copying them into this package or repository.

## Assembly and hardware review

1. Check the tray against the two right-rail positions and rear rail. Insert
   suitable M3 rail nuts before access is obstructed. A rear top-slot nut is
   additional hardware; availability is not established by the old strip nuts.
2. With the tray off the chassis, seat the PSU on its pads. Fit screws upward
   through the underside recesses into the PSU's own fittings. Use heads that
   fit the 7 mm diameter / 2.4 mm depth recess. Verify engagement and internal
   penetration against the actual PSU before tightening; no invented length.
3. Load the two rear bridge M3 nuts into the top-open pockets. Fit the bridge
   and secure it to the tray. Load the four lid nuts and four rear-panel nuts
   into their accessible pockets before the covers are installed.
4. Seat the C14 in the panel while the panel is loose. Confirm both locking tabs
   engage the locally thin island. It must not be retained by friction alone.
5. Fit the rear panel and lid using their four screws each. M3 × 8 is a nominal
   starting length for these 4 mm panels and the bridge's tray screws; confirm
   actual nut/head fit and no bottoming. The 5.60 AF / 2.80 deep panel nut
   pockets are pressure-fit allowances; installed covers retain the nuts.
6. Attach the tray at both right-rail positions and the rear top slot. Check
   screw lengths against the real T-nuts. Confirm plug/fuse access, removal
   order, rail clamping and resistance to cable pull by hand, unpowered.

The fit package contains no mains wiring instructions. Disconnect and unplug
before opening it. No live device action is part of this CAD work.

## Reproduce the checks

From `mechanical/dut-chassis-2020-v1`:

```sh
xvfb-run -a make power-system-v3-concept
# Python environment with matplotlib; PrusaSlicer Flatpak installed:
python3 scripts/power_system_v3_slice_audit.py
xvfb-run -a make validate
```

Generated output: `build/power-system-v3-concept/`. The slice script uses
`scripts/prusaslicer-power-system-v3-audit.ini`: PrusaSlicer 2.9.6, 0.8 mm nozzle,
0.4 mm layers, four perimeters, 20% infill, 8 mm brim, supports disabled. The
tray rotates 90 degrees to fit the audit 247 × 207 bed with its brim. This is a
geometry-audit profile, **not a machine/material profile to print G-code from**.
Slice with the owner's actual printer profile for any eventual physical print.

The source exports four independently closed, connected meshes. The checker
measures eight panel thickness probes and five PSU screw bores/bearing webs,
then intersects parts, measured components, provisional service volumes,
source chassis, plug corridor and straight 8 mm driver corridors. Nominal
surface contacts are distinguished from positive-volume overlap.

The slice audit binds its results to the exact mesh and profile hashes, checks
all extrusion-path centres against the bed, rejects support toolpaths, and
checks four snap-island probe locations on each of the three 0.4 mm layers plus
the first layer above the island. Layer sheets show the actual extrusion paths
at selected critical heights. A clean support-off slice is not proof that a
printer will bridge perfectly. Inspect `*-layers.png`, the panel section, vent
section, six orthographic views, open/exploded views and chassis context.

The chassis collision check uses the source's default Smart Pro / legacy gantry
layout with accurate rails and plate proxies. Unknown board components, cable
bundles and unsurveyed live-DUT differences are outside that check. Internal
orange volumes and the 50 × 32 × 80 C13 plug corridor are provisional allowances.

## Open electrical and physical gates

This is a reviewed mechanical fit candidate, not completion of the parent
powered-enclosure bead. Before powered use, measure the C14 lug and insulated
connector projection, actual C13 plug/boot and bend, PSU terminal layout, cable
bundle and selected gland. The final nonprinted terminal shield, PE bonding
interface, continuous AC/DC separation, conductor retention and rated DC egress
are not implemented here; the case has no DC outlet hole yet. Those features
must be resolved together from actual hardware instead of cutting an arbitrary
exit hole now. Fuse selection, temperature/flammability suitability, thermal
performance, strain relief and electrical checks remain open.

Owner visual acceptance and physical fit/load checks are also open. This
candidate does not authorize fleet rollout, replacement of old Downloads files,
or closing `tsp-bcx.21.45.3`.

Implementation: owner-attended Codex GPT-6 session; exact deployed model identifier
unavailable. Independent review evidence and exact tested revision are recorded
on PR86; do not infer approval from this document alone.
