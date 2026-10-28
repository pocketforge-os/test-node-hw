# PSU enclosure V3 — layout study

This is the first layout for the owner's 2026-10-28 redesign request, tracked
under `tsp-bcx.21.45.3`. It is a review artifact, not an approved print or
electrical enclosure. PR85's earlier enclosure remains historical evidence.
The component and coupon foundation is merged at `0b1e3b7`; no production pack
or existing component measurement changes in this study.

## Architecture

Three printed structural pieces: an open tray, a flat top lid, and a full rear
panel. The rear panel prints exterior-face-down. Its small C14 snap island is
surrounded on all sides by substantial panel material; it is never a bridge
to a nearby corner or a separate thin strip attached to a lid edge.

The tray has 4 mm walls/floor and a 4 mm lid. The rear panel has a 4 mm frame
with a local 1.2 mm snap island under the inlet flange. Its continuous U-shaped
inner overlap reaches 10 mm behind the exterior face. The lid has a 3.2 mm
thick, 4 mm deep overlap that steps around the front fastener pillars.
Nominal seating surfaces meet; 0.4 mm running clearance is behind the overlaps.
These are assembly joints, not an IP seal or a demonstrated electrical barrier.

The panel and lid each use four M3 axes. Visible top/rear loading pockets reuse
the previously qualified 5.60 mm across-flats / 2.80 mm deep nut geometry.
The installed cover captures the nuts. Screw lengths, entry chamfers, loading
sequence and actual hardware fit still need physical qualification. PSU pockets
reuse the corrected five-hole pattern, with 2.6 mm pocket depth in 12 mm pads.

## Fit and coordinates

All values are millimetres. Local +Y points toward the DUT/wall; +Z is up.
Installed origin is `[178,156,0]` in the existing chassis coordinates.

| Item | Geometry / evidence |
| --- | --- |
| Main case including lid | 148 X × 144 Y × 68 Z |
| PSU | 110 × 77.5 × 36.86; exact existing component keepout |
| PSU placement | `translate([8,91.5,6.4]) rotate([0,0,-90])` |
| C14 faceplate | 50.3 horizontal × 31 vertical, rotated from the approved model |
| C14 nominal insertion profile | Approved 27 × 46.86 contour, +0.20 normal clearance |
| C14 face datum | Local X=63, Y=144, Z=38; faces rearward |
| Flange margin to nearest panel edge | 10.5 above, 18.5 below, 37.85 left, 59.85 right |
| Right rail screws | Retained world Y=149.73 and 306; X=326 contact plane, Z=10 axes |
| Rear rail screw | World X=202, Y=348, vertical axis through the rail's top slot |
| Rail keys | 6.2 wide × 2.4 deep, based on measured 6.73 opening / 6.48 slot depth |
| Tray export including mounts | 150.4 × 214.27 × 64 |
| Panel export | 148 × 60 × 10, lying exterior-face-down |
| Lid export | 148 × 144 × 8, lying exterior-roof-down |

Two spaced right-rail ears and a rear-rail brace form a triangular support
pattern. The rear screw is accessed from above: a horizontal screw would trap
the driver between the panel and the rear rail. Both rail key shapes and the
rear top pad are checked against the source-owned extrusion geometry.
Availability and relocation of a suitable rear-rail T-nut remain physical
installation questions; the old four right-rail nuts do not establish this.

The original centered inlet at X=74/Z=34 produced **2660.597 mm³** of interference
between a provisional 50 × 32 × 80 plug-access corridor and the rear chassis
structures. Moving it 11 mm left and 4 mm up clears that corridor while keeping
the thin region well inside the panel. This is why the final inlet is slightly
off the panel's exact centre. The corridor is a design allowance, not a measured
C13 plug or cable-bend model.

## Reproduce and inspect

From this directory, with OpenSCAD and Python available:

```sh
xvfb-run -a make power-system-v3-concept
xvfb-run -a make validate-power-system-v3-concept
```

Outputs are under `build/power-system-v3-concept/`: meshes, fixed-camera PNGs,
per-export logs and `report.json` with mesh hashes, bounds and checks. The model
entrypoint is `power-system-v3-concept.scad`. Open its `PART="assembly"` selector
for the assembled view. Other useful selectors are `open`, `exploded`, `frame`,
`chassis`, `plug_access`, `panel`, and `panel_section`.

Checks use the exported meshes, not just source text:

- Each structural piece must be one closed connected edge-manifold mesh.
- Four Z-ray probes measure the panel island at 1.2 mm; four measure the
  surrounding frame at 4 mm.
- Solid intersections check parts, PSU/inlet, provisional internal service
  volumes, existing lower rails/plate proxies/carrier links, the plug corridor,
  and 8 mm straight screwdriver corridors.
- Nominal mating surface contact can produce CGAL zero-volume sheets. The
  report distinguishes these from empty intersections and rejects positive
  overlap above 0.0001 mm³. This is a layout interference check, not a general
  tolerance, strength or minimum-wall certificate.

The chassis check uses the existing source's default Smart Pro / legacy-gantry
layout and accurate slot extrusions, with plate proxies. It does not include
unmodeled cables, every component mounted to the boards, or a surveyed live DUT.
The simplified two-rail render is only a readable mounting illustration; the
`chassis` and collision selectors use the repository's chassis modules.

## Remaining work before a print candidate

1. Review this arrangement with the owner, especially the three-piece assembly,
   larger working space, rear rail pad and inlet location.
2. Measure the actual C13 plug/boot, inlet lug projection, insulated terminals,
   wire bends, cable bundle/gland and PSU terminal layout. Orange blocks in the
   open render reserve space; their dimensions are provisional. Final AC/DC
   separation, a nonprinted terminal shield, PE connection access, strain relief
   and fuse data are not implemented in this concept.
3. Add cooling and the DC exit after those paths are fixed. The current solid
   case is intentionally incomplete in those respects and is not suitable for
   energization.
4. Resolve print orientation and support details with a slicer. The rear top
   rail pad has an exposed external overhang that needs local removable support
   or a revised brace. No support-free claim is made. Check horizontal nut
   pockets, elephant foot, 0.8 mm nozzle treatment of the accepted 1.2 mm island,
   ABS shrink/creep and available bed/brim space. The panel and lid print flat.
5. Exercise actual nut loading, all driver paths, screw lengths, rail clamping,
   plug pull loads, and joint retention. Investigate all unintended slits in
   actual sliced layers, not only the nominal solids.
6. Run the full repository/print regression, independent review and the owner's
   visual/physical gates before a print release. Existing Downloads files are
   not replaced by this layout study. The bead remains in progress.

## Measurement provenance

The unchanged `lib/alt-1205t-power-supply.md` and
`lib/iec-c14-fused-switch.md` preserve the owner measurements and physical-fit
corrections. The final PSU upper-left hole correction was accepted without
another coupon print; it must not be described as separately printed proof.
No private photograph or screenshot is copied into this source package.

Design/implementation: owner-attended Codex GPT-6 session; exact deployed model
identifier unavailable. No independent reviewer has approved this V3 layout.
