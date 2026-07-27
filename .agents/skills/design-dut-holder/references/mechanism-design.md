# Contact and mechanism design

Read this reference whenever contact placement or retention geometry may
change. It guides design judgment; repository schemas and fixture contracts
remain authoritative.

## Start from evidence

Treat these inputs separately:

- the semantic model establishes appearance, simulator controls, and useful
  visual context;
- the fixture contract establishes manufacturing datums, measured envelope,
  local contact surfaces/depths, safe intervals, keep-outs, tolerance, and
  evidence confidence;
- calipers and in-hand trials resolve unknown or low-confidence fit values;
- the holder profile records deliberate contact/mechanism choices;
- physical qualification proves one exact printed candidate and process.

Do not turn photo-derived estimates into pressure-fit dimensions. Leave a
needed value unresolved and block qualification until it is measured.

## Select safe contacts

For every proposed contact:

1. use a named fixture contact and select its coordinate inside the locked safe
   interval;
2. bind depth and surface role to the contract rather than copying a shell
   thickness from the visual model;
3. remain clear of controls, ports, vents, speakers, triggers, seams, labels,
   cables, and the camera target;
4. distribute load so the device cannot translate, rotate, rock, or rack under
   normal operation;
5. preserve an intentional insertion/removal path without overstressing the
   shell or hook;
6. include designed play for device, printer, and process tolerance;
7. keep fasteners, nut captures, and adjustment travel accessible; and
8. verify the worst allowed envelope and local depth, not only the nominal
   unit.

Use opposing or redundant contacts only when each remains inside a safe
region. More hooks are not automatically safer; an extra contact can
overconstrain a tolerance stack or block service access.

## Reuse `perimeter_j_hook_v1` when it fits

Prefer the existing declarative family when:

- each retention point has a locally compatible perimeter surface and depth;
- a hook lip can engage without loading a control, seam, port, or curved
  transition;
- the rear service opening, trigger/wiring keep-out, and camera clearance
  remain valid;
- the required throat, play, support, and adjustment travel fit the supported
  parameter contract; and
- the carrier can remain support-free and serviceable.

Express the result as contact IDs, selected coordinates, designed play,
carrier parameters, retention parameters, artifacts, and device variants in a
strict profile. Do not fork a nearly identical OpenSCAD file merely to change
dimensions the profile already owns.

## Create a reusable mechanism when the shape is genuinely different

A curved cup, stepped support, sliding rail, compliant clip, or another
retention class may not fit `perimeter_j_hook_v1`.

Prototype the smallest parameterized source that proves the contact and
release motion. While prototyping:

- keep the profile `unqualified`;
- mark `implementation.kind` as `custom_openscad` with a concrete rationale
  and follow-up tracking reference;
- generate only non-production coupon/review output;
- isolate fit parameters from presentation and device labels; and
- add mutation tests that move a real fit-bearing parameter and prove the
  normalized fingerprint changes.

Before qualification:

1. extract the reusable geometry into a named mechanism family;
2. define and validate its declarative parameter/contact contract;
3. add it to the shared compiler/library instead of branching on one device
   name;
4. migrate the device profile away from `custom_openscad`;
5. validate every already qualified profile against the shared-library change;
   and
6. enter the normal coupon and two-PR physical gate.

The reusable family is the product. The one-off prototype is design evidence.

## Design the coupon around uncertainty

Use the lowest-filament artifact that can disprove the fit. Include the
tightest or least-certain contact geometry and, as relevant:

- hook throat, lip, support, and shell-depth relationship;
- nut pocket, keyway, screw clearance, and adjustment travel;
- curved or stepped contact patch;
- insertion and release motion;
- surface that controls rear/service clearance; and
- printer/material feature most sensitive to compensation.

If separate local coupons cannot expose interaction between contacts, print
the carrier before accepting. Never infer full retention from a fastener-only
coupon.

## Record an exact physical gate

Record:

- candidate Git revision and profile/fixture/toolchain hashes;
- device model/hardware revision and measured unit;
- printer, nozzle, material, layer height, compensation, and orientation;
- caliper results for the named fit criteria;
- insertion, retention, removal, control/port/vent/cable, rear, and camera
  checks;
- photos or evidence locations without committing private originals; and
- explicit owner acceptance reference and date.

Any later fit-bearing source, profile, fixture input, or toolchain change makes
that acceptance stale. Presentation-only labels may remain outside the
fit-bearing fingerprint only where the committed contract explicitly excludes
them.
