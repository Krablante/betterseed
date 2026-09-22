# Development

This repository is intentionally compact and release-oriented.

It also contains a narrow, repeatable patch/build path for the accepted APK.
See [History return fix](history-fix.md) for the version-pinned input, architecture,
build/signing commands and manual verification checklist. The build changes the
existing BetterSeed mod rather than starting from another Snapseed version.

## Working Principles

- Keep the repository self-contained and public-facing.
- Prefer small, reviewable changes over noisy bulk drops.
- Do not commit secrets, operator notes, or generated local clutter.
- Update docs when the release contract changes.
- Keep signing keys and generated APKs outside the repository.
- Preserve the established signing certificate for in-place Android updates.

## Local Checks

- Confirm markdown renders cleanly.
- Confirm the banner SVG displays at the README header size.
- Verify the checksum block matches the current accepted release.
- Verify internal links still resolve.

## Scope

This repository is for release-facing material:

- README and public docs
- changelog and release notes
- checksums and integrity guidance
- public artwork and repository assets
- small version-pinned patch/build scripts (not a dump of decompiled Snapseed)
