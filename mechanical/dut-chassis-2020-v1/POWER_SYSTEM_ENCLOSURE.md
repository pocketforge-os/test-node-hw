# Single-supply enclosure candidate

This package is a **pre-DUT02 mechanical prototype**, not a certified mains
enclosure. It is a secondary mounting and finger guard around the PSU's metal
shell. Do not install or energize mains wiring until every pre-power gate below
is closed by a competent reviewer. Always unplug the IEC cord before removing
the hood or servicing the fuse drawer.

## Artifacts

`power-system-enclosure.scad` owns five stable selectors:

- `PART="base"`: floor-down base/tray, PSU mount pattern, exterior nut traps,
  barrier capture, conductor saddles, and the existing rail interface;
- `PART="hood"`: roof-down tool-removable hood, rear C14 island, structural
  walls, labyrinth joint, partition, and baffled front vents;
- `PART="barrier_template"`: 2D template for a separately fabricated inner
  shield (DXF and SVG outputs; this part is not printed);
- `PART="assembly"`: clean candidate assembly preview;
- `PART="installed_preview"`: evidence assembly with rail proxy and named
  service volumes.

The four evidence-only selectors (`evidence_top`, `evidence_rear`,
`evidence_section`, and `installed_preview`) may display colored service
keep-outs. No `text()` geometry occurs in either printable selector.

Validation also exports `partition_slice` and `dc_route_keepout` meshes. These
are measurement evidence only: the former isolates the complete printed
partition and its single intended bushing, while the latter isolates the
continuous provisional 12 V routing envelope. Neither is a printable part.

Build and validate with:

```sh
make power-system-enclosure
make validate-power-system-enclosure
```

## Coordinate and fit contract

The sealed case envelope is X=190..326, Y=160..300, Z=0..78 mm. The complete
installed rail-bearing envelope extends to Y=117.73..338 because the exposed
rail spine reaches beyond both sealed case walls. The provisional case audit
envelope began at X=191, but a 3.2 mm wall there would overlap the exact PSU
keep-out by 0.2 mm. The reviewed X=190 expansion preserves the exact PSU
transform while providing 0.8 mm nominal side clearance. It does not move a
chassis rail datum.

The base rail spine is X=322.8..326, Y=117.73..338, Z=0..20 mm. Its four M3
axes remain at `(Y,Z)=(125.73,10), (149.73,10), (306,10), (330,10)` and are
driven from the exterior, outside the sealed cavity.

The PSU calls the merged measured component library at exactly:

```scad
translate([194,257.5,4]) rotate([0,0,-90])
```

That produces the X=194..304, Y=180..257.5, Z=4..40.86 mm metal keep-out.
The final physical-fit M3 centers are inherited, not copied into negatives:
upper-left `(4.95,4.95)`, lower-left `(6.75,98.6)`, and internal centers
`(25.3,30.9)`, `(25.3,67)`, `(53.3,67)` in the PSU datum.

The inlet calls the merged measured library at exactly:

```scad
translate([308,300,49.15]) rotate([90,0,0])
```

Its cable face points toward world +Y (the DUT rear/wall). The nominal body is
27 × 46.86 mm with a true +0.20 mm contour clearance. Only the region entirely
under the 31 × 50.3 mm faceplate is thinned to the physically approved 1.2 mm
snap wall; surrounding rear structure remains 3.2 mm.

## Print and assembly assumptions

- Base: print floor-down, no supports; 220.27 × 136 × 20 mm.
- Hood: print roof-down, no supports; 136 × 140 × 74 mm.
- Initial process: 0.8 mm nozzle; 3.2 mm walls and 4.0 mm floor/roof are nozzle
  multiples. Material, layer height, temperatures, and flammability/temperature
  suitability remain unapproved.
- Hood: four short horizontal M3 screws. Each matching 5.75 mm-AF × 2.6 mm nut
  pocket is fed from a full-size exterior underside chute, then necks to a
  5.2 mm opening through a nominal 0.8 mm-high press-retaining lip before
  reopening into the seated pocket. The nut must be deliberately pressed past
  the throat and cannot slide or fall back through it under gravity before the
  screw is installed. The pocket remains isolated from the protected cavity.
  Screw length must be selected so it cannot enter that cavity.
- PSU: M3 hardware through the approved pattern into underside/exterior
  retained nuts. Verify the actual screw stack before installation.
- Joint: 0.8 mm nominal lateral gap and 6.4 mm overlap. The left tongue routes
  around the PSU, and both affected tongue runs clear the hood's internal
  partition crossings. The PSU metal side and the intersecting partition walls
  close those local portions of the labyrinth without part-to-part overlap.
- Vent slots are at most 1.6 mm. The inner bank is vertically staggered by half
  a pitch, has no direct line of sight, stays out of the terminal zone, and
  preserves a nominal 10 mm or greater PSU-side vent plenum.

## Barrier, wiring, and protective earth

Fabricate the exported continuous terminal shield from **1.0 mm G10/FR-4 or a
suitably rated polycarbonate**, only after the exact material and temperature/
flammability properties are approved. The template is a continuous 81.5 × 46 mm
plate covering the whole terminal edge instead of inventing individual
L/N/PE/DC screw positions. It has no cable hole. The barrier is captured at its
base and hood; it is not a decorative insert.

The printed X=304..307.2 partition is continuous from the PSU shell top at
Z=40.86 through the upper partition, closing the former Z=40.86..49.98 slit.
Its only intentional breach is the provisional 8.0 mm insulating-bushing hole
at world X=305.6, Y=191, Z=54, safely above the PSU. Below the PSU top the
terminal service envelope retains the full X=304..318 projection; above the
PSU it steps outward to X=307.2..314.5 to avoid the continuous wall and barrier
capture while preserving a real service corridor.

The partition deliberately shares the zero-thickness Z=40.86 boundary with
the PSU shell top so those surfaces close the vestibule together. The
interference proof checks the PSU keep-out interior with a 0.01 mm numerical
inset; it permits that boundary contact but still rejects any positive-volume
hood intrusion.

AC L/N/PE and inlet terminal volumes stay in the protected vestibule. Printed
saddles provide separate conductor retention before the terminal bends. The
yellow evidence route reserves a direct copper C14-PE-to-PSU-PE path, plus
ring- or fork-lug and anti-loosening hardware clearance. Printed parts and hood
screws are never part of protective-earth bonding. No PSU chassis bonding hole
is assumed or invented.

The front/operator wall contains a provisional flattened 12.5 mm opening for a
recognized M12/PG7-class gland around a named 6.0 mm, two-conductor 18-AWG
bundle. Those defaults are geometry placeholders, not a gland selection.
Insulated 12 V conductors cross from the terminal vestibule only through the
printed partition's rated bushing at X=305.6, Y=191, Z=54. The modeled connected
route then passes over the PSU with more than 10 mm nominal vertical clearance,
moves forward of the PSU, drops below the vent baffle, and reaches the existing
front gland center at X=270, Y=160, Z=31. It remains provisional and powered use
is blocked until the actual cable, insulating bushing, and gland are confirmed.

The 8.0 mm separation parameter is a conservative prototype geometry target,
not a declaration of creepage, clearance, regulatory category, or compliance.

## Hardware assumptions

- five M3 PSU screws/nuts as selected after real stack measurement;
- four short M3 hood screws and four standard M3 hex nuts;
- one separately fabricated terminal shield, provisionally 1.0 mm thick;
- one rated M12/PG7-class gland or bushing matching the measured cable;
- insulated, temperature-rated AC conductors and insulated terminals;
- dedicated green/yellow PE conductor with ring or fork lug and suitable
  anti-loosening metal hardware;
- cable ties/retainers appropriate for the provided saddles.

## Required pre-power gates

1. Confirm the exact PSU nameplate/datasheet, inlet approvals and ratings,
   conductor insulation/gauge, terminal style, load, and inrush.
2. Select the fuse type/value from that electrical evidence. **Fuse remains
   TBD; CAD does not select it.**
3. Confirm the exact cable and gland part, thread/retention envelope, pull-out
   rating, bend radius, and the 12 V bundle OD/count/gauge.
4. Confirm AC terminal, insulated-lug, IEC rear, wire-bend, and slack envelopes;
   edit the named assumptions if required and rerun validation.
5. Approve the barrier material, thickness, temperature/flammability rating,
   partition bushing, and final continuous cut template against the dressed
   real terminal strip.
6. Approve the printed polymer/process for temperature and flammability, then
   perform a full-load thermal/ventilation test with the hood installed.
7. Establish direct metal PE bonding with a competent wiring review; torque and
   retain the metal hardware, then perform and record a protective-earth
   continuity test. The print must not carry fault current.
8. Confirm tool-only hood access, screw lengths, nut retention, strain relief,
   seam engagement, baffle integrity, and absence of any touch/tool path to
   energized terminals.
9. Unplug before fuse service or hood removal. Never work live. Complete the
   separately authorized DUT02 integration/inspection procedure before any
   fleet rollout.

No certification or powered-use approval is claimed by these files.
