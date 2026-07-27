---
name: design-dut-holder
description: Design, derive, refine, validate, qualify, and release source-owned PocketForge DUT holders from versioned device fixture contracts. Use for a new handheld holder, an upstream fixture candidate, J-hook or contact placement, reusable retention-mechanism selection or creation, fit-coupon iteration, holder geometry drift or requalification, and coupon/retrofit/full print-pack readiness.
---

# Design DUT Holder

Turn a verified manufacturing fixture interface into reviewed parametric
OpenSCAD and strict holder-profile data. Allow judgment while designing a new
fit, then make every later build deterministic from committed source.

## Load the relevant guidance

- Read [references/workflow-contract.md](references/workflow-contract.md) for
  the ownership table, decision states, exact commands, and two-PR
  qualification lifecycle.
- Also read [references/mechanism-design.md](references/mechanism-design.md)
  before choosing or moving contacts, changing retention geometry, or creating
  a mechanism family.
- Run
  `scripts/validate_holder_workflow.py repository --profile profiles/<profile>.json`
  from this skill directory for a render-free source/profile preflight.

Use `$model-handheld-device` for semantic appearance, simulator controls, and
fixture-contract evidence. Keep DUT boards, pigtails, rail modules, wiring,
power/serial topology, labgrid bindings, and advanced setup in the separate
device integration profile keyed by the same device slug.

## Enter the repository workflow

Read `AGENTS.md`, inspect and claim the Bead, and create its required worktree
before editing. Identify:

- canonical device slug and hardware revision;
- platform fixture-contract revision and qualification state;
- candidate receipt or accepted fixture lock;
- existing holder profile and physical-qualification state, if any;
- available in-hand measurements and the exact physical review gate.

Do not edit an automation candidate branch in place. Continue its work on a
normal claimed branch, retain the candidate receipt as provenance, and verify
the exact platform source before designing.

## Classify the change before drawing

Choose exactly one route from the decision table:

1. **No fixture-interface drift** — make no fit-bearing holder change. A
   visual/model/skin-only platform update is a holder no-op. Regenerate from
   existing committed source only when an artifact is needed.
2. **Existing mechanism, new device** — author a strict unqualified
   declarative profile selecting safe named contacts and a supported mechanism.
   Generate the coupon first.
3. **Changed fit for a qualified profile** — preserve every accepted lock and
   manifest; add a new lock plus an append-only change record, invalidate the
   profile, and review generated geometry-diff evidence before printing.
4. **Genuinely novel retention** — prototype parameterized OpenSCAD only while
   unqualified. Extract the working shape into a named reusable mechanism with
   compiler validation and tests before physical qualification.

Reject malformed, stale, colliding, or unverified candidate state. Do not
guess through missing manufacturing evidence.

## Follow the holder workflow

### 1. Establish manufacturing truth

Use the fixture contract and in-hand measurements for fit. Never derive
tolerance geometry from the semantic render mesh or a photo-only estimate.
Confirm the envelope, local contact depths, safe contact intervals, keep-outs,
rear/service clearance, camera target, tolerances, provenance, and unresolved
measurements.

### 2. Verify immutable inputs

Validate candidate receipts and fetch their exact platform Git revision.
Verify every raw contract hash, shared-chassis alias, resolved interface hash,
and accepted lock link using the repository commands. Stop if current source
does not reproduce the pinned data.

### 3. Select contacts and a mechanism

Prefer a named declarative family that can satisfy all fixture constraints.
Choose contact coordinates only inside their locked safe intervals. Balance
retention, preserve insertion/removal and service access, and test the
worst-case tolerance rather than the nominal shell alone.

Use `custom_openscad` only as a temporary unqualified escape hatch. Do not make
it the qualified endpoint.

### 4. Author source, not meshes

Commit:

- versioned fixture dependency input;
- strict holder profile and device-variant mapping;
- parameterized reusable OpenSCAD mechanism/source;
- tests and append-only qualification intent/records; and
- toolchain or process locks when intentionally changed.

Do not commit routine STL, preview, geometry-diff, or print-pack output. Do not
rewrite an accepted lock, manifest, change record, or release asset.

### 5. Validate before printing

Run the render-free preflight, inspect the exact OpenSCAD argument vector, then
render the named artifacts. Compare every qualified profile, not only the new
device. Treat a normalized-geometry failure as evidence to investigate; never
refresh a golden merely to make CI green.

Build a `coupon` pack first. Dirty or unqualified overrides are prototype
provenance only and cannot produce a production pack.

### 6. Iterate through an exact candidate

Keep the profile unqualified while changing contact poses, play, hook throat,
clearances, mechanism source, or print process. Commit the candidate before
the acceptance print and record its exact revision. If fit-bearing source,
profile data, fixture input, or toolchain changes afterward, invalidate the
review and print again.

### 7. Preserve the two-PR physical gate

In the first PR, declare the intentional change, downgrade the profile, and
emit candidate meshes plus `geometry-diff.json`. Obtain explicit owner fit
acceptance outside Git automation.

In a later PR, bind that acceptance to the unchanged candidate, add a new
immutable qualification manifest, complete the retained change record, and
restore `physically_qualified`. Never infer acceptance from a passing render,
photo, or test.

### 8. Generate and hand off

After qualification, build and verify `retrofit` or `full` through the
device-pack builder. Let CI publish ephemeral review packs and let the
immutable release workflow archive a newly accepted qualification version.
Never overwrite an existing tag or asset.

Report the profile ID, device slugs, fixture/interface identity, normalized
geometry result, qualification manifest, pack/release identity, and remaining
electrical integration handoff.

## Ship only a reproducible result

Before merge:

1. run the skill validator and repository-specific unit/static suites;
2. prove accepted TrimUI geometry remains exact unless the Bead explicitly
   carries renewed physical acceptance;
3. inspect generated diff evidence for every intentional artifact change;
4. pass PR peer review and pushed-main checks;
5. merge through the required PR flow and remove the worktree.

An LLM may help design a new contact layout or mechanism. It must leave behind
reviewed parameters, source, tests, and provenance; rebuilding the accepted
holder must never require the LLM.
