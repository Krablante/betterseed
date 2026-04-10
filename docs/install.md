# Install

BetterSeed is published as a curated release artifact, not a source dump. Use the latest GitHub release unless a specific build is called out separately.

## Accepted Build

- Build: `20260410T192447Z`
- SHA-256: `6540cf6ebbe3f5df25cb0b97583c8554ff205ebc0bfbb551537d8349de9e6aad`
- Minimum Android: `11` (`API 30`)

## Recommended Flow

1. Download the release artifact from the GitHub release page.
2. Verify the SHA-256 checksum before installing.
3. Install the APK normally on Android.
4. Open BetterSeed and confirm the separate package identity and the `Open project` entry.

## Quick Verification

Linux/macOS:

```bash
sha256sum BetterSeed-20260410T192447Z.apk
```

The output must match:

```text
6540cf6ebbe3f5df25cb0b97583c8554ff205ebc0bfbb551537d8349de9e6aad
```

## Notes

- BetterSeed is intended to live alongside stock Snapseed, not replace it.
- By default, projects live in `Download/BetterSeed Projects` and styles live in `Download/BetterSeed Styles`.
- Public releases stay conservative on purpose. The goal is a stable usable mod, not a dumping ground for every experiment.
- Everything needed for a normal install should be available from this repository and its release page.
