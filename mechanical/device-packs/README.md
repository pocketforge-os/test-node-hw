# Device print packs

Device print packs turn one reviewed holder profile into the exact STL set for
fit testing, retrofitting an existing node, or building a complete new node.
The selection is data-driven: a device slug must map to one labeled production
carrier in its holder profile before a pack can be built.

## Source and generated artifacts

Commit the inputs:

- semantic device and fixture contracts;
- holder profiles, qualification records, and OpenSCAD sources;
- the chassis-core layout;
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
| `full` | Build a complete test node | Retrofit pack, optional process-calibration bed, and shared chassis beds 01–05 |

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

A coupon may be generated before physical qualification; it is always marked
non-production while the profile is unqualified. `retrofit` and `full` refuse
an unqualified profile unless `--allow-unqualified` is explicitly supplied,
and that override is permanently recorded as non-production provenance.

A dirty source tree is refused for every mode unless `--allow-dirty` is
supplied. A dirty pack is always non-production. These escape hatches support
iteration; they cannot produce a production-eligible manifest.

Physical qualification is deliberately not automated. Print the coupon and
holder, check the named fit and access criteria, obtain the owner's explicit
acceptance, and then update the holder qualification record in a reviewed
change. Ordinary builds re-render and compare every fit-bearing qualified mesh
before emitting a pack.

## Adding a device

1. Finish the semantic device model and fixture interface.
2. Add or update a strict holder profile. Map every supported device slug to
   exactly one `production_carrier` source and display name.
3. Reuse the declarative perimeter-hook mechanism when its contact and
   clearance constraints fit. If the device needs a new retention mechanism,
   add source and tests first; that engineering step can still be agent-assisted
   but must end in the same data contract.
4. Generate and physically test the `coupon` pack.
5. Record explicit owner acceptance and lock the fit-bearing normalized
   geometry.
6. Generate `retrofit` or `full`; do not hand-select STLs from old build
   directories.

A device-model or holder change changes an input hash. Fit-bearing drift also
fails the accepted normalized-geometry checks. Chassis link geometry has its
own exact regression lock. CI builds a real coupon on pull requests and a
complete ephemeral pack for every dynamically discovered qualified device on
each relevant pushed revision, so stale generated output cannot make a source
change look complete.

The static normalized hashes in `layouts/chassis-core-v1.json` characterize
the established chassis beds and make any later edit explicit in review. They
are regression baselines, not a claim of new physical qualification. The
holder qualification manifest remains the authoritative physical-fit record;
changing either kind of lock requires understanding the geometry change, not
blindly recording a new digest.

## Immutable production releases

One release represents exactly one versioned physical-qualification manifest,
not a moving snapshot of a device name. The qualification file
`qualification/<profile-id>-vN.json` deterministically owns the tag
`print-pack-<profile-id>-vN`. Every device variant named by that profile is
included as its own `device-pack-<device-slug>.zip`. A source-only refactor
does not replace or republish an accepted release. Geometry that needs renewed
physical acceptance gets a new `vN` qualification manifest and therefore a new
release tag.

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
workflow. Before creating a release, it requires repository release
immutability to already be enabled. It creates a draft, uploads the complete
asset set, verifies GitHub's reported SHA-256 and size for every asset, and only
then publishes. It finally requires `immutable=true`, resolves the protected
tag to the exact manifest commit, downloads and hashes every asset, and confirms
the release was not selected as the moving latest release. An exact rerun is a
no-op; any conflicting draft, tag, target, or asset fails closed. Published
assets are never overwritten or deleted by this tooling.

To consume a release, name the qualification tag explicitly:

```sh
tag=print-pack-trimui-smart-pro-family-v1
gh release download "$tag" \
  --repo pocketforge-os/test-node-hw --dir "$tag"
(cd "$tag" && sha256sum --check SHA256SUMS)
```

For full source-aware validation, check out the commit recorded in
`release-manifest.json` and run `release_print_pack.py verify` against the
download directory. Do not script against GitHub's “latest” release.
