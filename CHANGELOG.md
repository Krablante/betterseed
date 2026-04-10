# Changelog

All notable changes to BetterSeed will be documented here.

## v2026.04.10-3 - 2026-04-10

### Fixed

- `Retrolux Brightness` and `Retrolux Contrast` now stay on stock `[-100, +100]` even when the BetterSeed global boundary is set above `100`
- The rest of `Retrolux` keeps the expanded BetterSeed boundary, so the fix stays narrow instead of weakening the whole tool

### Current Public Canon

- Public canon refreshed to build `20260410T142530Z`
- Release artifact checksum refreshed for the accepted baseline

## v2026.04.10-2 - 2026-04-10

### Added

- Initial public BetterSeed skeleton
- Release-oriented README, docs, banner, and license
- Standalone project notice covering GPL scope and free hobby release posture

### Changed

- Removed workspace-specific references from the public repository
- Switched the repository license from MIT to GPL-3.0
- Tightened the public docs so the repo reads as a standalone release home
- Rewrote the initial public history into one clean root commit
- Refreshed the public canon to build `20260410T123202Z`
- Updated install and integrity docs for the current release artifact

### Fixed

- `Export as -> SAVE` stays in the editor and writes a normal JPEG
- `View edits` delete/edit roundtrip remains stable
- `Lens Blur` can be reopened from `View edits -> Edit filter` without the crash that blocked re-editing

### Curated Baseline

- Separate BetterSeed package identity
- Restored stock photo picker for normal open
- Separate Open project entry in Home and editor toolbar
- Editable `.snpsd` save/open
- Save project stays in editor
- Reopened projects remain editable while regular export still works
- Embedded source kept and `edits_cache` removed
- `.bslook` import/export
- Preview fidelity improvements
- Curves 99 support
- Global range expansion and boundary controls
- No-resize full-res export fix
- `Export as -> SAVE` fix
- View edits delete/edit roundtrip fixes
- Lens Blur re-edit stability fix
- Shared numeric controls with exact value and hold-repeat
- BetterSeed-only custom UI language behavior
- Author channel link
