# ALT-1205T semantic model provenance

The model uses the owner-approved 2026-09-07 measurement worksheet derived from private files `20250907_150533.jpg` through `20250907_150752.jpg`. Filenames identify the evidence set; no image bytes, crops, metadata, or location data are stored here.

The underside datum is the top-left corner of the 77.5 × 110 mm base, with +X right, +Y down, and +Z toward the 110 × 36.86 mm label side. The three internal M3 centres are the unequivocal minimal-coupon pattern. The lower-left leader values 5.75, 4, 10.4, 2.28, and 2.61 mm are retained by `alt1205t_lower_left_unresolved_leaders()` but their endpoints remain unresolved, so they do not create holes or safety-critical geometry. The small upper-right square is explicitly not a hole. Terminal and wire-bend projection is unknown and excluded from the measured keep-out; enclosure design must establish that clearance separately.
