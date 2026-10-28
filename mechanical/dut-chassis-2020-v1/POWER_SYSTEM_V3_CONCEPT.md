# PSU enclosure V3 — first unpowered print candidate

Owner-directed enclosure redesign, `tsp-bcx.21.45.3`. This iteration builds on
PR86's mechanical fit candidate and PR87's internal layout at `893948f`. The owner asked to complete design
work before any filament, and authorized conservative allowances for existing
assorted connectors/wires instead of requiring purchase identifiers. A gland
and dust seal are optional; preventing access to mains terminals remains the
purpose. No live mains work or production-pack change is included.

## Geometry and the reason for the taller case

The original 148 × 144 × 68 mm case allowed only 20.2 mm behind the C14's
measured 21.8 mm insertion body. This iteration reserves **35 mm beyond that
body**, including projecting terminals, insulated connectors and a wire turn.
That envelope reaches Y=87.2, overlapping the PSU's Y maximum of 91.5.
Moving the inlet upward clears the supply without thinning a wall or prescribing
right-angle connectors. The body footprint and three rail datums are unchanged;
the case is now **148 × 144 × 100 mm**. A removable 4 mm-thick cable-exit insert
projects from the left wall. These are deliberate exterior changes, not hidden
inside the previous envelope.

The enclosure uses a tray, flat lid, full rear panel, small rear-rail bridge and
small cable-exit insert with integral guard-retaining tabs. Main walls/floor/lid/panel frame remain 4 mm. The C14
cutout remains the physically accepted contour with 0.20 mm normal clearance in
a 1.2 mm seating island. The complete faceplate is surrounded by thick panel;
there is no thin region at a corner or edge. Print the panel face-down so the
island is three full 0.4 mm layers. The lid and rear panel retain overlapping
joints with 0.4 mm assembly clearance behind the seating faces.

Local +Y points rearward, +Z upward; installed origin is `[178,156,0]`.

| Item | Geometry / provenance |
| --- | --- |
| PSU | Owner-photographed ALT-1205T, **12 V / 5 A**, 77.5 × 110 × 36.86 mm |
| PSU transform | `translate([8,91.5,8]) rotate([0,0,-90])`, unchanged |
| PSU mounting centres | `(4.95,4.95), (25.3,30.9), (25.3,67), (53.3,67), (6.75,98.6)`, approved coupon corrections |
| C14 faceplate | 50.3 horizontal × 31 vertical; centre X63/Y144/Z68 |
| C14 panel margins | 12.5 top, 48.5 bottom, 37.85 left, 59.85 right |
| C14 connection allowance | 54 wide × 35 deep × 36 high, X36..90/Y87.2..122.2/Z50..86; assumed |
| PSU terminal allowance | X118..142/Y14..91.5/Z8..48; assumed |
| C13 plug corridor | 50 × 32 × 80 mm rearward; assumed, not the owner's measured cord |
| Right rail axes | World Y149.73 / 306, contact X326, Z10 |
| Rear rail axis | World X202/Y348, vertical into top slot |
| Bridge-to-tray axes | World X194 / 210, Y324; forward of the rear carrier plate |
| Slot keys | 6.2 wide × 2.4 projection; measured rail opening 6.73, depth 6.48 |
| Cable opening | 15.8 × 8.8 rounded slot, allowing one nominal 8 mm or two nominal 6 mm jackets |
| Nonprinted sheets | Nominal 1.6 mm insulating stock; see material boundary below |

"Allowance" is a design bound, not a claim that every generic connector fits.
The owner need not provide part numbers to continue CAD. Hardware outside these
bounds requires changing the parameters before manufacture. Wire gauge, ratings,
crimp compatibility and allowed bend radius cannot be inferred from outside
size. The shell is a secondary guard around the PSU metal case.

## Covered DC exit and retention

The DC outlet opens into a separate compartment behind the PSU. Front, rear and
right walls connect to the floor; a nonprinted sheet closes its roof. The sheet
drops in from above into open rebates, tucks under a short right-hand lip, and
is retained on the left by two tabs on the bolted outlet insert. This replaces
the former 24 mm bridge over a 2 mm-high loading slot, where support removal
would have been impractical. The right lip has a 45-degree underside.

The outer cable slot is centred at Z26. A solid baffle at X20..23.2 rises to Z32;
the second baffle at X36..39.2 has an open-top notch starting at Z34.
The nonprinted sheet supplies the notch roof at Z46.2; there is no printed bridge. A cable therefore has
to turn upward. The external slot has no axial straight path into the enclosure.
The compartment ends at a separate 14.8 mm DC transfer opening in the right wall,
centred Y107/Z36, well beyond the accessible baffles. Sleeve the DC conductors
at this transfer and retain them along the shown route. This is geometric
separation of the outlet from the mains bay, not a regulatory finger-probe or
reinforced-insulation claim.

Two integral tie bridges in the DC compartment and two ramped tie bridges in
the right-side AC bay provide independent retention locations. Retain each
outgoing cable separately; one loose tie around unequal cables is insufficient.
The printed bridges are mounting features, not tested pull-out ratings. The
small exit insert can be replaced for a different grommet/gland or cable size
without changing the tray. No dust or water rating is intended.

The blue 8 mm route and orange 8 mm route in the internal render are routing
allowances, not a wiring schematic. Actual DC leads begin at the PSU's +V/-V
terminals, AC/PE leads at their corresponding terminals. The exact terminal row
coordinates have not been measured, so no printed separator is forced between
terminal screws based on a photograph. Maintain insulation and independent
retention within that shared terminal area; assembly review must verify that
loose AC conductors cannot reach the DC circuit.

## Nonprinted guards, earth and cooling

Two source-owned SVG/DXF templates describe **nonprinted** 1.6 mm sheets:

- `dc_roof_template`: **110.6 × 23.6**, installed X4.2..114.8, Y95.8..119.4,
  Z46.2..47.8. Open rebates provide 0.2 mm nominal fit clearance; the short
  right lip and two insert tabs retain it. Do not reuse PR87's wider template.
- `terminal_shield_template`: an L-shaped sheet over the PSU terminal bay and
  C14 wiring, installed Z90..91.6. It attaches below the lid to three bosses,
  using M3 screws into captive nuts loaded from the exterior top of the lid.

The sheet thickness is an interface assumption. Use insulating sheet with
verified temperature, voltage and flammability suitability for the application;
an unmarked offcut is not qualified by this CAD. The templates are not STL
parts and must not be substituted with ordinary printed polymer. The existing
PSU terminal cover also remains installed.

Protective earth uses the PSU's designated metal PE terminal/bonding arrangement.
Neither printed mounts nor lid/rail screws form the PE path. The AC routing
allowance includes PE; continuity to the metal case still needs verification.
No new hole into the PSU is specified and no undocumented case screw is declared
an earth stud. The insulating sheets need no earth connection.

Front and roof vents retain offset baffles. The roof baffle now has 45-degree
corbels between its ribs instead of 8.8 mm horizontal ceilings. Inner vent cuts
extend through the corbels and stay offset 6 mm from the outer vents. The roof baffle is now 40.74 mm above
the PSU's measured upper surface, leaving the upper inlet wiring clear of it.
Cooling and material temperatures need physical validation. No IP, finger-probe,
thermal, flame or electrical certification follows from a successful CAD check.

## Assembly order and fasteners

Work unplugged. The design package does not instruct mains wiring or energization.

1. Seat the PSU in the tray. The approved mounting pattern is unchanged. Its
   underside fittings sit in 7 mm reliefs; screws pass through 3.6 mm bores with
   3.2 mm bearing webs and 7 mm × 2.4 mm head recesses. **Permitted screw
   penetration is not established.** Select length from the actual mounting
   specification/known hardware; do not probe into the PSU to discover it.
2. Load the exterior-accessible panel/lid/bridge nuts and fit the separate rear
   bridge. A rear top-slot M3 rail nut is required in addition to the side nuts.
3. Seat the C14 in its loose rear panel and check both locking tabs engage.
   Keep this panel off the tray while installing the DC sheet; fit inlet wiring
   after the sheet is seated. Preserve the shown connector and wire-turn space.
4. Lay DC cables through the open baffles and retain each independently at the
   internal bridges. Fit suitable edge protection/sleeving. With the lid, rear
   panel and outlet insert off, tilt the DC roof sheet about 14 degrees (left
   edge raised), lower it into the open compartment, slide its right edge
   under the retaining lip, and lower the left edge into the rebates. Then
   bolt the outlet insert on; both tabs must sit above the sheet. Its M3 nuts load from the isolated
   DC side into 5.6 AF pockets; the installed screws capture them.
5. Attach the L-shaped insulating shield beneath the lid. Three M3 nuts load
   from the exterior top; the screws enter from below the sheet. Check hardware
   does not protrude into the reserved terminal/wire envelope.
6. Fit rear panel and lid. Verify plug/fuse access, cover removal, all cable
   retention and no pinched insulation before the first physical fit is accepted.
7. Secure the two right-rail points and rear top-slot point. Verify clamping
   and cable-pull resistance with power disconnected.

Nominal screw starting points: M3×8 for the main lid/panel/bridge and shield;
M3×16 for the side insert. Confirm actual head, washer and nut stack; these do
not prescribe PSU screw length or electrical protection. Nut pockets are
pressure-fit allowances until the mating covers/screws retain them.

## Reproduction and evidence boundaries

From `mechanical/dut-chassis-2020-v1`:

```sh
python3 scripts/test_power_system_v3_collision_gate.py
xvfb-run -a make power-system-v3-concept
# Python with matplotlib and installed PrusaSlicer Flatpak:
python3 scripts/power_system_v3_slice_audit.py
# Same Python environment, also with trimesh, shapely and numpy:
python3 scripts/power_system_v3_printability.py
python3 scripts/test_power_system_v3_provenance.py
xvfb-run -a make validate
# Fast visual iteration without replacing the validation report:
xvfb-run -a python3 scripts/power_system_v3_concept.py --views-only --views internals dc-section shield
```

Outputs are in `build/power-system-v3-concept/`. The full target checks five
closed connected printable meshes, eight panel thickness probes, five PSU screw
bores/bearing webs, 45 actual-mesh outlet baffle rays, two sheet templates, and
part/component/service/chassis/plug/driver/wire-route interference (one 8 mm and two 6 mm DC routes). Collision
exports must be clean-empty: no output file, exit 1, exact empty diagnostic and
only expected cache/timing lines. Warnings, emitted meshes, other exits and
unknown output fail closed. Per-solid translated self-intersection uses 0.01 mm
per-axis inset; sub-0.02 mm features are outside this audit's qualification.
Real contact/gap and positive-penetration controls exercise the producer. The
result matrix covers eight selectors × twelve outcomes. A piecewise convex swept
volume (one-degree rotation chords, <0.005 mm deviation) also checks the DC sheet's lower/tuck/rotate installation path against
the tray and seated PSU, with the inlet wiring and outlet insert absent.

The slice audit uses 0.8 mm nozzle / 0.4 mm layers, four perimeters, 20% infill,
8 mm brim and supports off. It binds mesh/profile hashes, checks bed fit and
C14 island coverage, and produces layer sheets. This is geometry evidence, not
production G-code. Support-off slicing cannot prove real bridging performance.
Inspect the fixed views and actual layer sheets; successful export alone is not
visual review. Refer to the exact-head validation report/PR for checks actually
run; this document describes the intended checks and is not a substitute for
those results.

CAD, slice and printability reports carry source receipts. The CAD receipt
covers all six declared SCAD inputs, the CAD producer, topology helper and
receipt helper. Every OpenSCAD export emits its actual transitive dependency
list; an undeclared input fails the export. The slice receipt additionally
binds its producer and profile; the final audit binds its own producer. Consumers
verify receipts before work and again before publishing their result, as well
as checking the STL/G-code hashes. Missing legacy receipts and stale inputs
require regenerating CAD, slices and printability evidence in that order.
The provenance test runs both consumers against each mutated CAD input, each
slice input against the print audit, legacy receipts, integrity/end checks,
and declared/undeclared dependency lists. It never edits the real source tree.

The source chassis check includes its default plate proxies and rails. Actual
DUT cable bundles and unsurveyed board components are outside that model. The
owner's original private photos remain outside Git.

## Print setup and support removal

Use the STLs in their exported orientations; do not automatically stand the
panel or lid on edge. The audited process uses a **0.8 mm nozzle, 0.4 mm fixed
layers, four perimeters, 20% infill and 8 mm brim**, with the owner's ABS process.
Choose the printer's calibrated material/temperature profile; audit G-code is
not a machine release. The tray fits the audited 247 × 207 mm bed rotated
90 degrees with brim. The large ABS tray still needs normal warping control.

| STL | Bed face | Supports |
| --- | --- | --- |
| `tray.stl` | Outside floor down, open cavity up | Build-plate-only, 45-degree threshold, avoid supporting bridges; inspect locations below |
| `panel.stl` | Exterior face down; C14 island starts on bed | Off |
| `lid.stl` | Exterior roof down; skirt/baffle grow upward | Off |
| `bridge.stl` | Broad top face down; slot key upward | Off |
| `dc_insert.stl` | Exterior face down; retaining tabs upward | Off |

For the tray, permit supports **only under the two exposed rail keys and in the
five 7 mm-wide, 2.4 mm-deep PSU screw-head recesses on the underside**. The slicer
audit checks every generated support extrusion, including width, stays within
these removable regions. Peel the key supports sideways from the exposed edge;
pick the shallow recess supports out from below. No support is allowed inside
the vents, cable passages, nut pockets, guard rebates or AC/DC compartments.
Do not select supports everywhere. Check your final slicer preview against
`tray-support-map.png`; block any additional interior supports it proposes.

The lid corbels and DC nut-boss ramps grow at 45 degrees. The DC cable notch is
open at the top. Front intake slots, tie slots, horizontal screw bores and the
rear panel receivers retain short bridges. The independent printability audit
checks every layer for floating islands and clips actual extrusion segments
against prior-layer mesh sections expanded by 0.4 mm (45-degree growth). The
remaining unsupported straight segments must be at most 1.0 mm on the four
support-free parts and 8.8 mm on the tray outside its support zones. Curved or segmented paths still require the visual layer review; this gate
does not certify bridge anchoring or filament behaviour. These are geometric limits, not a measurement of the owner's printer's bridging quality.
The former lid ceilings exceed this gate; support-disabled slicing alone would
not have caught that regression.

Check the C14 island is continuous, vent passages are open, screw recesses are
clean and no tabs are cracked after printing. Stop assembly if the print is
warped, delaminated or has holes. All five parts are for a first **unpowered**
fit check; no separate disposable coupon is required by this iteration.

## Remaining physical and electrical gates

After the exact candidate passes the recorded CAD, slice, visual and independent
review checks, it is ready for the owner's first unpowered print. Owner visual approval, physical fit and
finger-access checks, confirmed PSU screw engagement, actual cable retention,
sheet/material suitability, PE continuity, fuse selection and full-load thermal
and electrical checks remain open. Generic dimensional allowances remove the
need for part numbers during CAD; they do not establish hardware ratings.
Physical fit and powered qualification follow the print; they are not further
CAD work prerequisites. Do not merge/close the bead, replace historical Downloads
artifacts or roll out to other DUTs from this document.

Implementation: owner-attended Codex GPT-6; exact deployed model ID unavailable.
PR86/87 approvals cover their previous heads. The printability changes require
their own exact-head independent review; see the package receipt and linked PR.
