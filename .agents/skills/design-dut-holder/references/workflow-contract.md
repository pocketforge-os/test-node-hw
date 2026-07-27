# Holder workflow contract

Use this reference for the source/generated boundary, state routing, and exact
repository commands. Run commands from the `test-node-hw` repository root
unless a section says otherwise.

## Ownership and artifact boundary

| Layer | Committed | Meaning |
| --- | --- | --- |
| Semantic model and skin | Yes, in `platform` | Appearance, controls, simulator rendering; not tolerance geometry |
| `fixture-contract.json` | Yes, in `platform` | Manufacturing envelope, safe contacts, keep-outs, datums, tolerances, evidence |
| Accepted fixture lock | Yes | Immutable exact upstream source/interface used by accepted holder history |
| Candidate lock and receipt | Yes, on dependency/design branch | Changed upstream input in `awaiting_holder_design`; cannot drive production |
| Holder profile | Yes | Contact choices, mechanism parameters, artifacts, device variants, qualification link |
| Mechanism OpenSCAD and compiler | Yes | Reusable deterministic geometry implementation |
| Change and qualification records | Yes | Append-only intent, exact physical acceptance, normalized geometry |
| STL, previews, geometry diff, local packs | No | Generated review/print output under ignored build or temporary paths |
| Qualified release ZIP/manifest/checksums | Release assets | Immutable distribution archive for one accepted qualification version |
| DUT PCB, pigtail, rail modules, wiring, labgrid | Separate integration profile | Electrical/deployment state keyed by the same device slug |

Raw STL SHA-256 protects distributed bytes. The normalized mesh fingerprint
protects fit geometry across harmless STL representation changes. Neither
proves physical fit.

## Decision table

| Observed state | Required route | Production effect |
| --- | --- | --- |
| Platform advanced but resolved fixture interface is unchanged | No holder edit; regeneration only from current committed profile | Existing qualification remains valid |
| New device uses an existing named mechanism | Add versioned lock plus strict declarative profile; start unqualified and print coupon | Coupon is non-production until accepted |
| Receipt state is `awaiting_holder_design` for a qualified profile | Verify source, preserve accepted lock/manifest, create a new candidate lock and invalidation change | Prior production release remains immutable; new production blocked |
| Profile/change state is `awaiting_physical_acceptance` | Refine source/data and generated diff under the same retained intent | Coupon only; no restored qualification |
| Exact committed candidate receives explicit owner acceptance | Later PR completes record as `physically_accepted`, adds a new manifest, restores profile `physically_qualified` | Retrofit/full and a new immutable release version become eligible |
| Existing families cannot express safe retention | Parameterized `custom_openscad` prototype while unqualified, then extract a named reusable mechanism and migrate | Never qualify the one-off escape hatch |
| Candidate/source is malformed, stale, colliding, or lacks required in-hand evidence | Fail closed and correct upstream/design input | No generated output may claim readiness |

For a brand-new profile, the append-only change record has no accepted base.
For an existing profile, its base names the old immutable lock and
qualification manifest. Do not delete a record to abandon or restart history.

## Render-free preflight

From the skill directory:

```bash
python3 scripts/validate_holder_workflow.py contract
python3 scripts/validate_holder_workflow.py repository \
  --profile profiles/<profile-id>.json
```

Add `--platform-root /path/to/platform` when the exact source checkout is
available. The validator delegates to repository entrypoints, inspects the
compiled coupon command, and proves those checks did not mutate fit-bearing
source.

## Verify a dependency candidate

```bash
python3 mechanical/dut-cradle-v1/scripts/fixture_dependency_intake.py \
  validate-candidates

python3 mechanical/dut-cradle-v1/scripts/fixture_dependency_intake.py \
  verify-source \
  --receipt qualification/fixture-updates/<receipt-id>.json \
  --platform-root /path/to/platform
```

The automation draft owns only candidate locks and receipts. Continue design
on a claimed normal branch. Never replace an accepted lock with candidate
bytes.

## Validate and inspect a holder profile

```bash
python3 mechanical/dut-cradle-v1/scripts/holder_profiles.py validate \
  --profile profiles/<profile-id>.json

python3 mechanical/dut-cradle-v1/scripts/holder_profiles.py verify-source \
  --profile profiles/<profile-id>.json \
  --platform-root /path/to/platform

python3 mechanical/dut-cradle-v1/scripts/holder_profiles.py print-command \
  --profile profiles/<profile-id>.json \
  --artifact fit_coupon \
  --output /tmp/<profile-id>-fit-coupon.stl
```

Inspect the argument vector before rendering. It must name only committed
profile data and source-owned OpenSCAD.

Render explicit review artifacts into ignored or temporary output:

```bash
python3 mechanical/dut-cradle-v1/scripts/holder_profiles.py render \
  --profile profiles/<profile-id>.json \
  --artifact fit_coupon \
  --output /tmp/<profile-id>-fit-coupon.stl
```

For a profile that remains qualified:

```bash
python3 mechanical/dut-cradle-v1/scripts/holder_profiles.py check-qualified \
  --profile profiles/<profile-id>.json
```

Do not run a baseline-recording command in response to failure. Diagnose the
profile, fixture input, source, or intentional-change state.

## Plan and review an intentional transition

CI compares the PR head to its exact base. For a local equivalent, extract the
base cradle tree and run:

```bash
python3 mechanical/dut-cradle-v1/scripts/qualification_ci.py plan \
  --base-root /path/to/pr-base/mechanical/dut-cradle-v1 \
  --output /tmp/holder-qualification-plan.json

python3 mechanical/dut-cradle-v1/scripts/qualification_ci.py check \
  --base-root /path/to/pr-base/mechanical/dut-cradle-v1 \
  --profile-id <profile-id> \
  --output mechanical/dut-cradle-v1/build/qualification-ci/<profile-id>
```

Review candidate STLs and `geometry-diff.json`. The report covers added,
removed, and changed artifacts; changing an artifact name does not escape
review.

The first PR:

1. keeps old locks/manifests/change history byte-identical;
2. sets the profile to `unqualified`;
3. clears production qualification links;
4. adds or advances an `awaiting_physical_acceptance` record; and
5. leaves rendered output uncommitted.

After an explicit owner gate on the exact committed candidate, the later PR:

1. rerenders the unchanged candidate;
2. adds a new versioned qualification manifest;
3. completes the retained record as `physically_accepted`; and
4. restores the profile to `physically_qualified`.

## Build deterministic print packs

Build the lowest-cost physical proof first:

```bash
python3 mechanical/device-packs/build_device_pack.py build \
  --device <device-slug> \
  --mode coupon

python3 mechanical/device-packs/build_device_pack.py verify \
  --pack mechanical/device-packs/build/<device-slug>/coupon
```

`--allow-dirty` and `--allow-unqualified` permanently mark prototype output
non-production. They are iteration escape hatches, not acceptance shortcuts.

After qualification:

```bash
python3 mechanical/device-packs/build_device_pack.py build \
  --device <device-slug> \
  --mode retrofit

python3 mechanical/device-packs/build_device_pack.py build \
  --device <device-slug> \
  --mode full
```

Do not hand-pick a carrier, hook set, nameplate, or chassis bed from an older
build directory.

## Verify release identity

```bash
python3 mechanical/device-packs/release_print_pack.py identity \
  --profile-id <profile-id>

python3 mechanical/device-packs/release_print_pack.py build \
  --profile-id <profile-id> \
  --output /tmp/<profile-id>-release

python3 mechanical/device-packs/release_print_pack.py verify \
  --bundle /tmp/<profile-id>-release
```

The build directory is generated. Publication belongs to the protected
immutable-release workflow. Never replace an existing tag, ZIP, manifest, or
checksum file.

The skill source path participates in pushed-main OpenSCAD artifact validation.
After those exact-source artifacts pass, the gated CAD dependency workflow may
advance the handbook gitlink. A skill edit therefore cannot make the handbook
document an untested test-node-hw revision.
