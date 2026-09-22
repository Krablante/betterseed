# Manual verification — history return fix

Status: manual checks completed for release `v2026.09.22-1`.

## Environment and method

One Android 16 / API 36 Google APIs x86_64 emulator with ARM64 translation,
2 virtual CPU cores and 3 GiB RAM. The real ARM64 library from the accepted APK
was used. No unit/integration/smoke-test files or generated test suites were used.
Checks used the real UI through ADB input, screenshots, package inspection and logs.

Base: `BetterSeed-20260410T193231Z.apk`, SHA-256
`cc67b58477e43769fa59b17ccb9078844837e9a7c0f81d1e851ddd59bd1c3bd7`.
Candidate: versionCode `1435393`, versionName `2.22.0-bs.260922`.
The initial checks used a development signing key. Final installation and
project-migration checks used `BetterSeed-20260922T082155Z.apk` with the new
permanent release key. The April signing identity cannot be updated in place;
the one-time reinstall is documented in [Install](install.md).

## Reproduction

The base APK was exercised with a 5152×3864 JPEG (5,922,346 bytes) and a
4200×6300 PNG overlay (48,868,758 bytes). Brush strokes were entered through the
real mask UI. The resulting masked layer was copied and inserted again to cross
the file-backed state threshold without needing further long drawing sessions.
The final stack had two masked Double Exposure steps and a 128,490-byte serialized
filter-state payload (128,494 bytes including the clipboard version header).

Toolbar Close crashed the base APK with:

```text
Failure delivering result ... request=102, result=-1
Caused by: java.lang.NullPointerException:
  Attempt to invoke interface method 'int java.util.List.size()' on a null object reference
  at bsh.c(PG:9)
  at ...MainActivity.onActivityResult(PG:103)
```

`BSHistory` showed two `filterstack_close` calls, then the first result listener's
`lafe_apply_view_edits`, followed by the crash in the second reader. This is an
observed Java state-transport failure, not an observed out-of-memory failure.

The captured filter payload was replayed in the candidate. Only the clipboard's
four-byte app-version header was adjusted for the existing version gate; no
filter or stroke bytes were changed. The old application's saved `.snpsd` was
also reopened to check the original photo/project path.

## Results

- Toolbar Close with the large state: editor returned, process stayed alive,
  one `filterstack_close_once`, no crash-buffer entries.
- System Back with the same large state in the reopened original project: passed.
- Replace through the history menu and its confirmation dialog: passed.
- Undo after Replace: restored the original one-step stack. Redo restored the
  two-step stack. Opening and closing unchanged history preserved Redo.
- Reopen the mask, add a stroke, rotate landscape and back, Discard changes:
  restored the original serialized payload byte-for-byte. Both payloads were
  128,490 bytes with SHA-256
  `2b8d52baeafd6f0817cee0ad009bc79f3fa9881b39692abff3a8c4dbcd8e5616`.
- Delete the top history step and return: one remaining step; Undo returned to
  the two-step state.
- Save project after the large-state edits: created a 54,922,104-byte `.snpsd`.
- Reopen that project after uninstalling the development build and installing
  the permanently signed release: both masked steps restored. Copying their
  state reproduced the exact 128,490-byte payload and SHA-256 above. Returning
  through the toolbar succeeded with one close record and an empty crash buffer.
- Full-resolution export completed: JPEG, 5152×3864, 4,960,163 bytes. Actual
  output pixels were inspected. This dense-mask export was slow under ARM64
  translation; no phone rendering-speed claim is made.
- APK ZIP payload comparison: only `classes.dex` and `AndroidManifest.xml`
  changed. All native libraries, assets, resources and `classes2.dex` match the base.
- The development-signed APK installed and ran; Android reports the new version.
- Final release signature and ZIP alignment verified. APK SHA-256:
  `40914e23e56a8452905dc74465caec0a2330c4d2f8bc361b81c5a24b9d3e80c7`.
  Its new signing certificate matches the separately verified signing-key backup.
- Reinstalling the release over itself with `adb install -r` succeeded, confirming
  same-key installation continuity. This does not bypass the April key mismatch.

## Limits

This reproduces and addresses the file-backed history-result crash. It does not
establish that every possible crash with very large images has the same cause.
The user's original images, physical phone and original crash log were not
available. ARM64 translation and software graphics make emulator timings
unsuitable for claims about phone rendering performance.

The original portable-project reader/writer and full-resolution render path are
unchanged. This patch does not add autosave, change export quality, reduce mask
point density, or promise unlimited image sizes.
