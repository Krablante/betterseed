# FAQ

## Is BetterSeed affiliated with Google?

No. BetterSeed is an independent Snapseed mod.

## Does it replace stock Snapseed?

No. The public canon is built around BetterSeed as a separate package.

## Why is this repository intentionally compact?

Because it is meant to stay easy to audit, easy to release, and easy to understand. It keeps the public release contract focused instead of turning into an unstructured dump.

## How do I trust a build?

Verify the accepted build checksum:

- Build: `20260922T082155Z`
- SHA-256: `40914e23e56a8452905dc74465caec0a2330c4d2f8bc361b81c5a24b9d3e80c7`

## Why does Android refuse to update my April build?

The September release uses a new permanent signing key. Android requires a
one-time reinstall when moving from the April signing identity. First save and
back up your `.snpsd` projects; uninstalling removes private app data and unsaved
work. Follow [the migration instructions](install.md#upgrading-from-april-2026-releases).

## Does the large-mask fix lower image or mask quality?

No. It removes duplicate history completion and serialized-state transport;
the native renderer, brush points and export quality are unchanged. The observed
crash was a missing temporary-state file read by a second result handler, not a
reason to downsample images. Other device memory limits still apply.

## Why keep the repo so small?

Because the public repo should be easy to audit, easy to release, and easy to maintain.

## Where do projects and styles go by default?

- Projects (`.snpsd`) live in `Download/BetterSeed Projects`
- Styles (`.bslook`) live in `Download/BetterSeed Styles`
- `Export as` lets you choose a different folder for flat photo exports

## Is BetterSeed a commercial product?

No. BetterSeed is published as a free hobby release. The author does not receive commercial compensation from this project and does not offer paid commercial licensing, support, or endorsement through this repository.
