# Install

BetterSeed is published as a curated release artifact, not a source dump. Use the latest GitHub release unless a specific build is called out separately.

## Accepted Build

- Build: `20260410T142530Z`
- SHA-256: `fa204564f4dd7f1af3474f822f0e2b907f86d8f7b4ea53d931534e4bfa56409b`
- Minimum Android: `11` (`API 30`)

## Recommended Flow

1. Download the release artifact from the GitHub release page.
2. Verify the SHA-256 checksum before installing.
3. Install the APK normally on Android.
4. Open BetterSeed and confirm the separate package identity and the `Open project` entry.

## Quick Verification

Linux/macOS:

```bash
sha256sum BetterSeed-20260410T142530Z.apk
```

The output must match:

```text
fa204564f4dd7f1af3474f822f0e2b907f86d8f7b4ea53d931534e4bfa56409b
```

## Notes

- BetterSeed is intended to live alongside stock Snapseed, not replace it.
- By default, projects live in `Download/BetterSeed Projects` and styles live in `Download/BetterSeed Styles`.
- Public releases stay conservative on purpose. The goal is a stable usable mod, not a dumping ground for every experiment.
- Everything needed for a normal install should be available from this repository and its release page.
