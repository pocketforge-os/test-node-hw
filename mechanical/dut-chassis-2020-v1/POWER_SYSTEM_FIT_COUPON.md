# Power-system fit coupon

This disposable planar coupon checks the owner-approved ALT-1205T underside
datums, the rigid 27 × 46.86 mm IEC C14 insertion profile in a 3.0 mm test panel,
and a separate M3 nut-trap/process sample. It prints at the source orientation:
broad face flat on the bed, Z upward, with no supports. It is **not an electrical
part** and must never be used as a mains enclosure or powered-wire guard.

Build and validate it with:

```sh
make power-system-fit-coupon
make validate-power-system-fit-coupon
```

The PSU region checks all five M3 features, including the reinterpreted upper-left
centre and derived lower-left centre, plus the unchanged upper-right 3.3 × 4.7 mm
slot and the new 2.61 × 4.0 mm bottom-open slot. The IEC opening applies a true
uniform 0.20 mm contour offset per side. The nut sampler is connected for printing
but is explicitly process-only geometry, not part of the PSU pattern.

The validation output's `pocketforge-normalized-stl-v1` fingerprint is the
reproducible acceptance identity for the coupon mesh. A raw STL SHA-256 checks
only one exported file's transport integrity: OpenSCAD may emit equivalent
facets in a different order, so every raw hash must be labeled
**build-instance-specific** and must not be used as the acceptance identity.

The defaults are 0.20 mm IEC clearance per side, 0.40 mm added to the nominal
M3 screw-hole diameter, 0.25 mm added across the nominal 5.5 mm nut flats, and
a 3.0 mm wall. Each is independently overridable with the matching OpenSCAD
define without changing component-library constants.

After the corrected coupon was printed with a 0.8 mm nozzle, the owner found
the physical lettering unreadable and mostly unable to fit on the sparse part.
The printable selector is therefore intentionally label-free: it contains no
raised, recessed, embossed, engraved, coordinate, warning, or process text.
Annotations exist only in the separately selected PNG evidence scene and are
never part of the default STL export.

## Physical acceptance gate

Print the exact committed candidate and report every correction numerically.
The owner must explicitly confirm that:

- all five PSU M3 checks and the upper-right slot align with the real PSU without
  forcing after placing its underside on the coupon and sliding the PSU left and
  up until its outer left edge seats against the crisp `X=0` shoulder and its
  outer top edge seats against the crisp `Y=0` shoulder;
- the 2.61 × 4.0 mm bottom slot aligns at X=2.28 and remains genuinely open at
  the bottom edge;
- the IEC rigid body and both 5 mm locking tongues insert through the 3.0 mm
  panel, the tongues spring outward after insertion, and they retain behind the
  wall;
- the provisional, unmeasured 0.6 mm resting tongue projection is adequate, or
  the required correction is reported numerically;
- the 31 × 50.3 mm IEC faceplate fully covers the clearanced opening; and
- a real M3 screw passes and a real nominal 5.5 mm-across-flats, 2.4 mm-thick
  nut fits and remains captured in the separate sampler.

The first printed coupon was evaluated in private physical-fit photos
`1-Photo-1.jpg`, `2-Photo-2.jpg`, and `3-Photo-3.jpg`. These provenance identifiers
are basenames only; the private files are not copied into Git.

Physical acceptance applies only to the exact candidate revision and stated
printer, nozzle, material, layer height, compensation, and orientation. It does
not qualify a final enclosure or authorize wiring or powered use.
