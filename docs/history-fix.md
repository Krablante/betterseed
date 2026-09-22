# History return fix

This patch is based on BetterSeed `v2026.04.10-6`, not on a different Snapseed
release. It keeps the original native renderer, filter parameters, brush points,
resources and project format. It does not reduce image resolution or mask detail.

## Problem

The history toolbar's Close handler called `FilterStackActivity.I()` and then
`finish()`, which called `I()` again. System Back had the same duplicate entry.
Each `I()` applied the selected state, serialized the current state twice, and
pushed the current state into Undo when the history had changed.

Returning a serialized state is particularly unsafe here: both the `afe` result
listener and `MainActivity.onActivityResult` can read `EditSessionCurrentState`.
`dx.n()` puts filter lists larger than 102400 bytes in a temporary file;
`dx.m()` deletes that file after reading it. A second reader therefore cannot
restore the same file-backed state. Small inline states can hide this defect.
The request-102 switch path must be checked in smali: JADX's reconstructed Java
control flow can misleadingly appear to associate that path only with request 106.

Brush masks contain stroke subparameters and point buffers, so a lengthy mask can
cross this threshold independently of the compressed size of the source images.
Copy/paste restores the same parameters and does not remove this condition.

## Design

- `finish()` is the sole owner of history completion. Toolbar Close and system
  Back delegate without committing separately.
- The result carries the existing `EditSessionJobId` and viewport metadata, not
  serialized filter lists. Both activities already use the same registered `bsf`
  session. The result listener refreshes that session without cloning or
  reapplying its filter list.
- Changed history is committed once by the close path. Unchanged history does
  not create a new Undo entry or mark the session dirty during close.
- Undo records the entry snapshot `G`, not another clone of the exit state.
- Activity recreation preserves the entry snapshot separately from the current
  session. Discard and Undo retain their original meaning after recreation.
- `onSaveInstanceState` continues to serialize recovery state. Removing the
  unnecessary result transport does not remove Android lifecycle persistence.

No new renderer, background service, periodic autosave, cache format, or user
setting is introduced. The existing portable-project writer is not suitable for
frequent autosave because it materializes embedded source assets in memory.

## Build boundary

`tools/build.py` checks the accepted base APK SHA-256, decompiles its DEX with
Apktool, applies `tools/patch_history.py`, and assembles the first DEX with smali.
The ZIP is repacked from the original entries, replacing only `classes.dex` and
the manifest's `versionCode` (1435392 to 1435393) and `versionName`
(`2.22.0-bs.260922`, visible in Android app information). Old APK signatures are
removed. Native libraries, `classes2.dex`, resources and assets are unchanged.

The output is aligned but **unsigned**. Signing is deliberately separate: never
silently replace the established signing identity with a workstation debug key.
Android requires the existing signing identity for an in-place update.

```sh
python3 tools/build.py /path/to/BetterSeed-20260410T193231Z.apk /path/to/new-build.apk
apksigner sign --ks /private/path/to/release.keystore \
  --ks-pass env:BETTERSEED_STORE_PASSWORD --key-pass env:BETTERSEED_KEY_PASSWORD \
  --out /path/to/BetterSeed-signed.apk /path/to/new-build.apk
apksigner verify --verbose --print-certs /path/to/BetterSeed-signed.apk
zipalign -c -p 4 /path/to/BetterSeed-signed.apk
```

Build tools used for this patch: Python 3, Apktool 2.7.0 and smali 2.5.2,
plus Android `zipalign` and `apksigner`. Generated output belongs outside the
repository. No proprietary native source or signing material is stored here.

## Manual release checks

Use one Android device or emulator. Do not use generated test suites.

1. Confirm the base APK emits two `BSHistory: filterstack_close` records for one
   toolbar Close. Exercise a mask whose serialized state exceeds 102400 bytes.
2. Confirm the candidate emits one `filterstack_close_once` and returns to the
   editor with the same mask. Repeat using system Back.
3. Reopen and change the mask; check Copy/Replace, delete, Discard, Undo and Redo.
4. Recreate the history activity and check that Discard/Undo use its entry state.
5. Save and reopen an editable project, then export an image. Inspect actual pixels.
6. Inspect crash logs and the final APK's signature, version, alignment and
   unchanged resources/native payload. Verify the published checksum after upload.

Do not describe a matching user-device crash as reproduced without a crash log
or a directly observed reproduction. Emulator graphics/memory behavior is not a
substitute for a physical phone under the user's exact large-image workload.
