# Install

BetterSeed is published as a curated release artifact, not a source dump. Use the latest GitHub release unless a specific build is called out separately.

## Accepted Build

- Build: `20260922T082155Z`
- App version: `2.22.0-bs.260922` (`1435393`)
- SHA-256: `40914e23e56a8452905dc74465caec0a2330c4d2f8bc361b81c5a24b9d3e80c7`
- Minimum Android: `11` (`API 30`)
- Architecture: `arm64-v8a`

## Upgrading from April 2026 releases

This release uses a new permanent signing key. Android cannot install it over
the April builds because the original private signing key is no longer available.
An installed APK contains only the public certificate, not that private key.

1. In the old BetterSeed, save every project you need to keep using **Save project**.
2. Copy the resulting `.snpsd` files from `Download/BetterSeed Projects` to a safe
   location, such as a computer. Back up `.bslook` styles and exported photos too.
   Confirm the files exist and, where possible, reopen the saved projects before
   uninstalling. Copy/Replace in View edits is not a project backup.
3. Only after checking your backups, uninstall the old **BetterSeed**. Uninstalling
   deletes its private app data, including unsaved edits and its clipboard/cache.
4. Install the new APK and use **Open project** to reopen your `.snpsd` files.

If a project cannot be saved, do not uninstall the old app until the work you need
has been recovered. There is no automatic transfer of private app data between
the two signing identities. Stock Snapseed is a different package and is unaffected.

Releases signed with the new permanent key can update this version normally.

## Recommended Flow

1. Download the release artifact from the GitHub release page.
2. Verify the SHA-256 checksum before installing.
3. Install the APK normally on Android.
4. Open BetterSeed and confirm the separate package identity and the `Open project` entry.

## Quick Verification

Linux/macOS:

```bash
sha256sum BetterSeed-20260922T082155Z.apk
```

The output must match:

```text
40914e23e56a8452905dc74465caec0a2330c4d2f8bc361b81c5a24b9d3e80c7
```

## Notes

The new release signing certificate SHA-256 is:

```text
d86ff8f2e497029e335685a1fa32927e4cd694efa732be622c27d8b9f17e2517
```

You can inspect it with `apksigner verify --print-certs BetterSeed-20260922T082155Z.apk`.

- BetterSeed is intended to live alongside stock Snapseed, not replace it.
- By default, projects live in `Download/BetterSeed Projects` and styles live in `Download/BetterSeed Styles`.
- Public releases stay conservative on purpose. The goal is a stable usable mod, not a dumping ground for every experiment.
- Everything needed for a normal install should be available from this repository and its release page.
