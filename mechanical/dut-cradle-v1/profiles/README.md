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
| Holder profile | `profiles/<family>.json` | Yes | Selected contact poses, carrier/frame choices, retention/fastener parameters, artifact recipes and qualification link |
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
```

Normal commands are read-only with respect to profiles, locks, qualification
records and OpenSCAD source. `render` writes only the explicit output path.

## Add a device with an existing mechanism

1. Finish the platform semantic model and its separate fixture contract.
2. Obtain the in-hand measurements required by that contract. Leave unknown
   values unresolved; do not infer pressure-fit geometry from the visual mesh.
3. Update/add a fixture lock in a reviewed change, pinning a full platform Git
   SHA and the raw hashes of the canonical contract plus any shared-chassis
   aliases.
4. Copy the nearest declarative holder profile. Select a supported reusable
   mechanism family, contact IDs and exact poses inside the locked contact
   intervals. Keep presentation choices separate from retention fields.
5. Run render-free validation and inspect the compiled OpenSCAD command.
6. Generate the low-filament coupon first. A future device-pack command will
   automate `coupon`, `retrofit` and `full` batches; until then use `render`
   only for named artifacts.
7. Print and physically check the coupon/contacts, then the carrier. Record
   explicit owner acceptance in a new qualification manifest before changing
   the profile status to `physically_qualified`.
8. Once qualified, every profile, shared-mechanism or toolchain PR must
   regenerate and compare that device's protected meshes.

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
2. a reviewed downstream PR refreshes this lock and shows the profile impact;
3. holder geometry remains unqualified until coupon/full physical acceptance;
4. only accepted geometry receives a new golden manifest.

Changing a holder profile or reusable mechanism follows the same rule: a golden
failure is evidence to inspect and print, never an instruction to refresh the
baseline. Raw STL SHA-256 proves distribution-file integrity; normalized mesh
identity protects geometry; neither replaces physical fit.
