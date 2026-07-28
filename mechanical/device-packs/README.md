# Device print packs

Device print packs turn one reviewed holder profile into the exact STL set for
fit testing, retrofitting an existing node, or building a complete new node.
The selection is data-driven in two independent dimensions: a device slug must
map to one labeled production carrier in its holder profile and to one chassis
layout in `device-layouts.json` before a pack can be built. The builder rejects
a caller-supplied layout that disagrees with that registry.

## Source and generated artifacts

Commit the inputs:

- semantic device and fixture contracts;
- holder profiles, qualification records, and OpenSCAD sources;
- the device-to-layout registry and qualified/candidate chassis layouts;
- generator and regression tests; and
- documentation.

Do not commit routine STL exports. A pack is generated from an immutable Git
revision, verified, and carried by CI or a release artifact. Pull-request and
pushed-commit artifacts are temporary review evidence; an immutable GitHub
release is the archive of record for physically accepted production packs. Its
`manifest.json` records every source-file SHA-256, every exact OpenSCAD
definition, raw STL hashes, representation-independent mesh fingerprints,
bounds, volume, triangle count, and topology. `SHA256SUMS` covers every STL.
Neither file contains timestamps or absolute build paths.

The handbook's browser generator follows the same rule. It publishes a
source-only browser bundle—not rendered STLs—made directly from the canonical
holder-profile and device-layout registries:

```sh
python3 mechanical/device-packs/export_browser_bundle.py build
python3 mechanical/device-packs/export_browser_bundle.py verify
```

`catalog.json` contains every registered device, all three pack modes, the
exact resolved artifact plan and OpenSCAD definitions, qualification state,
print contract, and accepted normalized fingerprint where one exists. The
bundle also contains the complete hashed `.scad` include closure and
`SHA256SUMS`. It contains no STL. A browser can therefore render one selected
part or a complete pack locally without maintaining a second device list.
Adding a device to a valid holder profile and `device-layouts.json`
automatically adds it to the next catalog export.

OpenSCAD facet ordering is not byte-stable across otherwise identical runs.
The builder therefore rewrites each render as a canonical ASCII STL with exact
renderer coordinates, deterministic facet ordering/start vertices, and
preserved winding. The raw hashes identify those distributed canonical files;
the independent normalized fingerprints still answer whether their geometry
matches an accepted or regression-locked mesh.

## Pack modes

| Mode | Purpose | Contents |
| --- | --- | --- |
| `coupon` | Validate a new or changed physical fit cheaply | Qualified holder fit coupon |
| `retrofit` | Change the DUT on an existing chassis | Coupon, selected labeled carrier, six-hook set, four carrier links, device nameplate, eight wire anchors |
| `full` | Build a complete test node | Retrofit pack, optional process-calibration bed, and every core bed owned by the selected chassis layout |

The calibration bed is included in a full export so the pack is complete, but
it only needs printing after the printer, material, process, or extrusion
changes.

Holder coupon/carrier/hook records specify PETG, matching the qualified cradle
guidance. Chassis-core, link, placard, and routing records specify ABS. Every
record fixes 100% scale, support-free exported orientation, and any
artifact-specific ironing or filament-change exception.

## Build and verify

Run from the repository root:

```sh
python3 mechanical/device-packs/build_device_pack.py build \
  --device trimui-smart-pro \
  --mode coupon
```

After the coupon and holder have passed the physical qualification gate:

```sh
python3 mechanical/device-packs/build_device_pack.py build \
  --device trimui-smart-pro \
  --mode retrofit

python3 mechanical/device-packs/build_device_pack.py build \
  --device trimui-smart-pro \
  --mode full
```

The TrimUI Smart Pro remains mapped to the physically proven two-upright
gantry. The TrimUI Smart Pro S is mapped to the material-reduced dual-bar
candidate. Generate that candidate explicitly for printing and review with:

```sh
python3 mechanical/device-packs/build_device_pack.py build \
  --device trimui-smart-pro-s \
  --mode full \
  --allow-unqualified
```

Its clean-source manifest must report `production_eligible=false`,
`nonproduction_reasons=["layout_unqualified"]`, and
`layout.qualification.acceptance_ref="tsp-t1zd.2"`. There is no flag that maps
the Pro S back to the legacy layout or maps the base model onto the candidate.

Outputs default to
`mechanical/device-packs/build/<device>/<mode>/`. Existing output is never
overwritten implicitly. Use `--replace` only to atomically replace a directory
that already contains a recognized generated pack.

Verify an existing pack against both its files and the current source
checkout:

```sh
python3 mechanical/device-packs/build_device_pack.py verify \
  --pack mechanical/device-packs/build/trimui-smart-pro/full
```

The qualified toolchain is OpenSCAD 2021.01 as pinned in
`../dut-cradle-v1/qualification/cad-toolchain.json`.

## Qualification and prototype gates

A coupon may be generated before holder qualification; it is always marked
non-production. `retrofit` and `full` refuse unqualified holder geometry unless
`--allow-unqualified` is explicitly supplied. A `full` pack additionally
requires a physically qualified chassis layout. Candidate layouts also require
`--allow-unqualified` and record `layout_unqualified` permanently. A retrofit
that contains no candidate chassis-core bed may still be production-eligible
when its holder and every emitted artifact remain qualified.

A dirty source tree is refused for every mode unless `--allow-dirty` is
supplied. A dirty pack is always non-production. These escape hatches support
iteration; they cannot produce a production-eligible manifest.

Physical qualification is deliberately not automated. Print the coupon and
holder, check the named fit and access criteria, obtain the owner's explicit
acceptance, and then update the holder qualification record in a reviewed
change. Ordinary builds re-render and compare every fit-bearing qualified mesh
before emitting a pack.

Qualified chassis layouts are immutable by layout ID. CI compares every
qualified layout file and its registered device mappings with the pull
request's base revision; change geometry under a new candidate layout ID
instead of editing a proven version. Promotion is staged: candidate geometry
must land first, be printed and accepted, and a later change may update only
its `qualification` record. CI also renders every production full pack on the
pull request, so changing shared OpenSCAD source without reproducing every
accepted normalized fingerprint fails before merge.

## Adding a device

1. Finish the semantic device model and fixture interface.
2. Add or update a strict holder profile. Map every supported device slug to
   exactly one `production_carrier` source and display name.
3. Add exactly one entry to `device-layouts.json`. Reuse a physically
   qualified layout only when its recorded device scope actually covers the
   new slug; otherwise add a candidate source-owned layout with a tracked
   physical acceptance reference.
4. Reuse the declarative perimeter-hook mechanism when its contact and
   clearance constraints fit. If the device needs a new retention mechanism,
   add source and tests first; that engineering step can still be agent-assisted
   but must end in the same data contract.
5. Generate and physically test the `coupon` pack.
6. Record explicit owner acceptance and lock the fit-bearing normalized
   geometry.
7. Generate a non-production `full` candidate, physically qualify any new
   chassis topology, and promote only its accepted normalized fingerprints.
8. Generate `retrofit` or `full`; do not hand-select STLs from old build
   directories.

A device-model or holder change changes an input hash. Fit-bearing drift also
fails the accepted normalized-geometry checks. Chassis link geometry has its
own exact regression lock. CI builds a real coupon plus complete ephemeral
packs for every registered qualified or candidate layout on pull requests and
repeats those packs on each relevant pushed revision, so stale generated
output cannot make a source change look complete.

The static normalized hashes in `layouts/chassis-core-v1.json` freeze the
working base chassis. `layouts/chassis-dualbar-v1.json` separately freezes the
Pro S candidate beds. Shared Batch 04, Batch 05, carrier-link, calibration, and
wire-anchor hashes are identical across both layouts; only dual-bar Batches
01–02 are new. These are regression baselines, not automatic physical
qualification. Changing a lock requires understanding the geometry change,
not blindly recording a new digest.

## Immutable production releases

One release represents exactly one versioned physical-qualification manifest,
not a moving snapshot of a device name. The qualification file
`qualification/<profile-id>-vN.json` deterministically owns the tag
`print-pack-<profile-id>-vN`. Every device variant named by that profile is
included as its own `device-pack-<device-slug>.zip`. A source-only refactor
does not replace or republish an accepted release. Geometry that needs renewed
physical acceptance gets a new `vN` qualification manifest and therefore a new
release tag.

Release generation resolves the same per-device registry and refuses if any
selected layout is still a candidate. It also refuses to force mixed layouts
through the original single-layout release schema. The tracked Pro S physical
gate owns the later versioned mixed-layout release lane; the immutable
`print-pack-trimui-smart-pro-family-v1` release remains untouched.

Each canonical, uncompressed ZIP has fixed metadata, sorted safe paths, and one
`device-pack-<device-slug>/` root. The release also carries:

- `release-manifest.json`, which binds every archive to the holder profile,
  qualification manifest, accepted geometry/source revision and acceptance
  reference, fixture lock and upstream platform revision/contracts, chassis
  layout, test-node-hw commit, release generator, and CAD toolchain; and
- release-level `SHA256SUMS`, which covers every ZIP and the release manifest.

Build and verify the complete release candidate from a clean commit:

```sh
python3 mechanical/device-packs/release_print_pack.py build \
  --profile-id trimui-smart-pro-family

python3 mechanical/device-packs/release_print_pack.py verify \
  --bundle mechanical/device-packs/build/releases/\
print-pack-trimui-smart-pro-family-v1
```

The builder refuses dirty source, unqualified profiles, prototype overrides,
unsafe archive paths, and unversioned qualification names. Repeated builds from
the same clean commit are byte-identical. Generated release directories remain
under the ignored `mechanical/device-packs/build/` tree; neither ZIPs nor
release metadata are committed.

Publication runs only through the main-only `Publish qualified print pack`
workflow. GitHub deliberately withholds the repository immutability setting
from the workflow's ordinary contents token. An administrator therefore runs a
separate authorization immediately before dispatch:

```sh
PF_RELEASE_ADMIN_TOKEN="$(gh auth token)" \
  python3 mechanical/device-packs/publish_print_pack.py authorize \
    --profile-id trimui-smart-pro-family

gh workflow run publish-print-pack.yml \
  --repo pocketforge-os/test-node-hw \
  --ref main -f profile_id=trimui-smart-pro-family
```

`authorize` requires a clean checkout at the current remote `main`, reads the
live immutable-release setting with administration access, and writes a
non-secret Actions-variable proof bound to the exact repository, tag, and
commit. The proof expires after one hour. The release workflow receives no
administration credential and has no permission to mint or refresh that proof.

After validating the authorization, the workflow creates a draft, uploads the
complete asset set, verifies GitHub's reported SHA-256 and size for every asset,
and only then publishes. It finally requires `immutable=true`, resolves the
protected tag to the exact manifest commit, downloads and hashes every asset,
and verifies the release attestation when the runner's GitHub CLI supports it.
Both release mutations send `make_latest=false`, so a print pack never replaces
an existing latest release by request. GitHub nevertheless designates the
repository's only published full release as latest; that moving repository
pointer is neither release identity nor a publication postcondition. An exact
rerun is a no-op even in that sole-release case. Any expired/mismatched
authorization or conflicting draft, tag, target, or asset fails closed.
Published assets are never overwritten or deleted by this tooling.

To consume a release, name the qualification tag explicitly:

```sh
tag=print-pack-trimui-smart-pro-family-v1
gh release download "$tag" \
  --repo pocketforge-os/test-node-hw --dir "$tag"
(cd "$tag" && sha256sum --check SHA256SUMS)
```

For full source-aware validation, check out the commit recorded in
`release-manifest.json` and run `release_print_pack.py verify` against the
download directory. Always name the versioned qualification tag; do not script
against GitHub's “latest” release or its UI badge.
