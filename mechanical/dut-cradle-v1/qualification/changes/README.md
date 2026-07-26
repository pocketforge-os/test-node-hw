# Holder geometry change records

Files in this directory are source-owned declarations for intentional
fit-bearing, fixture-interface, toolchain, or print-process changes. Candidate
STLs and geometry-diff reports are generated CI artifacts and do not belong in
Git.

The lifecycle is deliberately two PRs:

1. The change PR sets the holder profile to `unqualified`, clears its production
   qualification links, preserves the prior accepted manifest byte-for-byte,
   and adds an `awaiting_physical_acceptance` record. CI renders the candidate
   and publishes its diff against the accepted baseline.
2. After printing and explicit owner fit acceptance, a later PR adds a new
   immutable qualification manifest, restores `physically_qualified`, and
   changes the same record to `physically_accepted` with the new acceptance
   reference, date, manifest path, and manifest SHA-256.

An awaiting candidate may be refined across additional PRs. Its change ID,
accepted baseline, intent, and scopes stay fixed; its candidate fixture and
toolchain hashes advance with the reviewed candidate. Requalification binds to
the exact candidate state present at its PR base: CI rerenders that base
candidate and the proposed accepted candidate and requires their artifact sets
and normalized metrics to match. Awaiting and completed records are retained
permanently; deleting one is not a way to abandon or rewrite qualification
history.

An accepted manifest is never edited or reused for changed geometry. A profile
that remains physically qualified must reproduce its PR-base fingerprints and
topology exactly. Candidate reports cover the union of old and new artifact
names, so introducing a new clamp/hook type or removing an old part appears as
an explicit added/removed artifact rather than escaping the geometry diff.

Each `<change_id>.json` is strict
`pocketforge-holder-geometry-change-v1` data:

```json
{
  "schema": "pocketforge-holder-geometry-change-v1",
  "change_id": "example-holder-fit-v2",
  "profile_id": "example-holder",
  "base": {
    "profile_path": "profiles/example-holder.json",
    "geometry_manifest": "qualification/example-holder-v1.json",
    "manifest_sha256": "<64 lowercase hex>",
    "acceptance_ref": "tsp-example.1",
    "fixture_interface_sha256": "<64 lowercase hex>",
    "fixture_lock": "profiles/fixture-locks/example-holder-v1.json",
    "fixture_lock_sha256": "<64 lowercase hex>",
    "toolchain_lock": "qualification/cad-toolchain-v1.json",
    "toolchain_lock_sha256": "<64 lowercase hex>"
  },
  "intent": {
    "tracking_ref": "tsp-example.2",
    "reason": "Explain why accepted fit geometry must change.",
    "scopes": ["j_hook"]
  },
  "transition": {
    "state": "awaiting_physical_acceptance",
    "candidate_fixture_interface_sha256": "<64 lowercase hex>",
    "candidate_fixture_lock": "profiles/fixture-locks/example-holder-v2.json",
    "candidate_fixture_lock_sha256": "<64 lowercase hex>",
    "candidate_toolchain_lock": "qualification/cad-toolchain.json",
    "candidate_toolchain_sha256": "<64 lowercase hex>",
    "physical_acceptance": null
  }
}
```

For a brand-new, never-qualified profile, `base` is `null`. Scope values are a
sorted, duplicate-free subset of `carrier_body`, `fit_coupon`,
`fixture_interface`, `j_hook`, `j_hook_set`, `mechanism`, `print_process`, and
`toolchain`.

The candidate toolchain file is content-locked by SHA-256. A toolchain file
referenced by an accepted manifest is immutable; changing CAD tooling requires
a new lock path selected by an invalidated candidate and then by the new
qualification manifest. Accepted fixture locks are likewise immutable and
content-addressed by the change record, so a changed platform pin/interface
uses a new versioned fixture-lock path rather than rewriting accepted history.
