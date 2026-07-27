# DUT holder profiles

This directory is the source-owned boundary between a device fixture contract
and reusable OpenSCAD holder mechanisms. It makes regeneration deterministic:
an agent may help author a new profile or mechanism, but rebuilding an accepted
holder uses only committed data, code and a pinned toolchain.

## The layers and their owners

| Layer | Owner | Committed? | Purpose |
|---|---|---:|---|
| Semantic device `.scad`, skins | `platform/device-models` | Yes | Visual/UI identity and simulator controls; never assumed to be tolerance geometry |
| `fixture-contract.json` | `platform/device-models/<slug>` | Yes | Evidence-backed envelope, contact regions, keep-outs, datums, uncertainty and qualification scope |
| Fixture lock | `profiles/fixture-locks/` | Yes | Exact platform Git revision, raw contract hashes and resolved interface payload used by this repo |
| Candidate lock + intake receipt | automation draft only | Yes, on the draft branch | Exact changed upstream payload plus an `awaiting_holder_design` work receipt; cannot drive production |
| Holder profile | `profiles/<family>.json` | Yes | Selected contact poses, exact device-to-carrier mapping, carrier/frame choices, retention/fastener parameters, artifact recipes and qualification link |
| Reusable mechanism | `lib/*.scad` plus the named template | Yes | Parametric carrier/hook implementation |
| Qualification manifest | `qualification/` | Yes | Normalized fingerprints and physical-acceptance provenance for fit-bearing meshes |
| STL, previews, print packs | build/CI/release output | **No source commit** | Generated distribution artifacts; raw SHA-256 belongs in a pack manifest/release |

The fixture lock is intentionally committed generated input, like a dependency
lockfile. It is not edited as a second source of device truth. Its source
revision/path/raw hashes are verified against the upstream platform repository,
and its resolved interface hash is recomputed locally.

## Current qualified profile

[`trimui-smart-pro-family.json`](trimui-smart-pro-family.json) is the first
declarative profile. It pins platform merge
`81c853928475fc4292d2744bedbb80f36cfb87fa` and fixture-interface SHA-256
`637aa67b32e284af2d5ad1b1655e630392e06fa80af1996f498f8d3cdecb20d5`.
The TG5050/Smart Pro S entry is a no-fit-delta alias of the canonical
TG5040/Smart Pro contract.

The profile selects the six accepted perimeter contacts inside the locked safe
intervals and supplies `perimeter_j_hook_v1` carrier, hook and fastener
parameters. The compiler derives the device envelope, local contact depth,
rear service opening, optical offset and 11 mm rear trigger/wiring clearance
from the lock. It then invokes OpenSCAD with an argument list—never a shell—and
passes every profile value as a `-D` override.

The decisive regression renders these four artifacts from the profile and
compares normalized geometry with the physically accepted manifest:

- unlabelled fit-bearing carrier body;
- one production J-hook;
- six-hook print set; and
- fit coupon.

Labels are presentation data and remain outside the carrier-body fingerprint.
Each `device_variants` entry still maps its slug to one exact wrapper and
display name, so pack generation cannot silently substitute the Smart Pro S
carrier label for a Smart Pro.

## Commands

From `mechanical/dut-cradle-v1`:

```bash
# Strict, render-free discovery validation.
python3 scripts/holder_profiles.py validate
python3 scripts/test_holder_profiles.py

# Verify both pinned platform files at the exact lock revision.
python3 scripts/holder_profiles.py verify-source \
  --profile profiles/trimui-smart-pro-family.json \
  --platform-root /path/to/platform

# Show the deterministic argument vector for review.
python3 scripts/holder_profiles.py print-command \
  --profile profiles/trimui-smart-pro-family.json \
  --artifact j_hook \
  --output /tmp/j-hook.stl

# Generate one caller-selected artifact.
python3 scripts/holder_profiles.py render \
  --profile profiles/trimui-smart-pro-family.json \
  --artifact j_hook \
  --output /tmp/j-hook.stl

# Rebuild every qualified artifact in a temporary directory and compare it.
python3 scripts/holder_profiles.py check-qualified \
  --profile profiles/trimui-smart-pro-family.json

# Prove a valid 11.3 -> 11.4 mm throat change is rejected by qualification.
python3 scripts/holder_profiles.py check-mutation \
  --profile profiles/trimui-smart-pro-family.json

# Emit the sorted matrices consumed by CI. These discover every profile.
python3 scripts/qualification_ci.py matrix --kind qualified-profiles
python3 scripts/qualification_ci.py matrix --kind qualified-devices

# Compare this checkout with an extracted PR-base cradle tree.
python3 scripts/qualification_ci.py plan \
  --base-root /tmp/pr-base/mechanical/dut-cradle-v1 \
  --output /tmp/qualification-plan.json

# Render one planned entry and write candidate STLs plus geometry-diff.json.
python3 scripts/qualification_ci.py check \
  --base-root /tmp/pr-base/mechanical/dut-cradle-v1 \
  --profile-id trimui-smart-pro-family \
  --output build/qualification-ci/trimui-smart-pro-family

# Prove a real 0.1 mm hook mutation is caught and emitted as diff evidence.
python3 scripts/qualification_ci.py check-mutation \
  --base-root /tmp/pr-base/mechanical/dut-cradle-v1 \
  --profile-id trimui-smart-pro-family \
  --output build/qualification-ci/trimui-smart-pro-family/mutation

# Inspect a verified platform dependency snapshot without writing source files.
python3 scripts/fixture_dependency_intake.py plan \
  --snapshot /tmp/platform-fixture-dependencies.json \
  --output /tmp/fixture-update-plan.json

# Validate every candidate lock/receipt discovered on an automation draft.
python3 scripts/fixture_dependency_intake.py validate-candidates
python3 scripts/fixture_dependency_intake.py matrix
```

Normal commands are read-only with respect to profiles, locks, qualification
records and OpenSCAD source. `render` writes only the explicit output path.
Qualification review commands refuse an existing output directory and, when
writing inside the repository, permit only the cradle's ignored `build/`
destinations. External temporary directories are also allowed.
Qualification CI discovers profile files rather than using a workflow-owned
allowlist. Adding a physically qualified profile therefore creates a required
matrix entry automatically; each qualified device variant also enters the
pushed-revision full-pack matrix. Every `profiles/*.json` file is owned registry
state, and one device slug may belong to exactly one profile.

## Add a device with an existing mechanism

1. Finish the platform semantic model and its separate fixture contract.
2. Obtain the in-hand measurements required by that contract. Leave unknown
   values unresolved; do not infer pressure-fit geometry from the visual mesh.
3. Add a versioned fixture lock in a reviewed change, pinning a full platform
   Git SHA and the raw hashes of the canonical contract plus any shared-chassis
   aliases. Never rewrite a lock retained by accepted qualification history.
4. Copy the nearest declarative holder profile. Select a supported reusable
   mechanism family, contact IDs and exact poses inside the locked contact
   intervals. Keep presentation choices separate from retention fields.
5. Run render-free validation and inspect the compiled OpenSCAD command.
6. Add one `device_variants` row per `device_slugs` entry. The production
   recipe must select `PART="plate"`, suppress preview DUT/hooks, and retain
   labels.
7. Generate the low-filament coupon first:

   ```sh
   python3 ../device-packs/build_device_pack.py build \
     --device <device-slug> --mode coupon
   ```

8. Print and physically check the coupon/contacts, then the carrier. Record
   explicit owner acceptance in a new qualification manifest before changing
   the profile status to `physically_qualified`.
9. Once qualified, generate `retrofit` or `full` through the pack builder.
   Never hand-select an old carrier, label, and hook set.
10. Every profile, shared-mechanism or toolchain PR must regenerate and
    compare that device's protected meshes.

This common path is data authoring plus physical validation, not an LLM
activity. Photos and calipers still require judgment, but regeneration does
not.

## A genuinely new retention mechanism

Some devices need a curved cup, stepped support, sliding rail or another shape
that `perimeter_j_hook_v1` cannot express. Use `implementation.kind =
"custom_openscad"` only as a temporary escape hatch. It requires:

- an existing source path;
- a concrete rationale;
- a follow-up reference for extracting a reusable mechanism family; and
- `qualification.status = "unqualified"`.

A custom profile cannot claim physical qualification. After its geometry works,
promote the reusable portions to a named declarative mechanism, migrate the
profile, run coupon/full physical acceptance, and only then qualify it. This is
where a repo-owned holder-design skill can accelerate first-pass CAD; the
merged result must still become deterministic source plus data.

## Intentional upstream or holder changes

A visual-only model/skin edit does not change the fixture-interface hash and
requires no holder update. If the platform fixture interface changes:

1. its interface revision/hash changes and prior platform qualification is
   invalidated or explicitly renewed;
2. a reviewed downstream PR refreshes this lock, sets the profile to
   `unqualified`, and adds an
   [`awaiting_physical_acceptance`](../qualification/changes/README.md) change
   record;
3. CI renders candidate meshes and publishes `geometry-diff.json` against the
   immutable prior manifest, while production pack generation remains blocked;
4. coupon/carrier prints receive explicit owner fit acceptance; and
5. a later PR adds a new manifest and completes the change record before
   restoring `physically_qualified`. CI rerenders the exact candidate from
   that PR's base and rejects any post-acceptance artifact-set or geometry
   drift.

Changing a holder profile or reusable mechanism follows the same rule: a golden
failure is evidence to inspect and print, never an instruction to refresh the
baseline. A profile that stays qualified must match the exact PR-base normalized
geometry even if its source was refactored. Editing an accepted manifest in
place, removing a qualified profile from discovery, or combining invalidation
and renewed qualification in one PR fails CI. Raw STL SHA-256 proves
distribution-file integrity; normalized mesh identity protects geometry;
neither replaces physical fit.

## Automatic upstream intake

The scheduled/manual
[`fixture-dependency-intake.yml`](../../../.github/workflows/fixture-dependency-intake.yml)
workflow runs only code checked out from protected `test-node-hw` `main`. It
clones exact current platform `main`, asks platform's own exporter to generate
and verify its canonical fixture snapshot, and plans every holder profile by
its subscribed device slugs.

The decision boundary is the resolved fixture-interface hash:

- visual-model, skin, render, label, and camera changes produce no snapshot
  change;
- raw contract/evidence or source-revision changes with the same resolved
  interface produce a deterministic `no_change`; and
- one changed resolved interface produces a new candidate lock under
  `profiles/fixture-locks/candidates/` plus an exact update receipt under
  `qualification/fixture-updates/`.

The candidate uses the separate
`pocketforge-fixture-candidate-lock-v1` schema. It preserves the complete
upstream payload without claiming that the current holder mechanism can
consume it. Its `pocketforge-fixture-update-receipt-v1` record pins the active
profile, devices, accepted lock/hash/interface, platform revision and raw
contracts, candidate interface revision/hash, candidate path/hash, and state
`awaiting_holder_design`.

Automation never changes `profiles/<family>.json`, an accepted lock,
OpenSCAD, a qualification record, or a print pack. It opens or refreshes one
draft PR on `automation/fixture-dependency-intake`; the same candidate is a
byte/tree no-op. A newer interface may replace that draft with
`--force-with-lease`, but unexpected paths, a non-draft PR, a concurrent
branch update, or either repository advancing after the plan fails closed.
Write credentials are read through `pf-secret` only after a real candidate is
staged.

OpenSCAD CI discovers every receipt rather than maintaining a workflow
allowlist. Each candidate gets an exact platform-revision verification job;
an unreferenced lock, missing device, alias divergence, stale raw hash,
malformed receipt, or changed candidate payload cannot hide on the draft.

The draft is an input to holder design, not a release. A holder designer must
review the new contact/keep-out contract, select or implement an appropriate
mechanism, create the normal versioned active lock and geometry-change record,
invalidate the old qualification, and print/accept the new geometry through
the existing two-PR lifecycle. No candidate receipt is physical acceptance.
