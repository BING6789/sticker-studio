# Sticker Studio Skill V1.2

V1.2 turns the V1.0 specification into an executable, testable workflow.

## What changed from V1.0
- machine-readable `manifest.yaml`
- explicit intent-to-rule/tool routing
- deterministic `tools/` execution layer
- JSON schemas for project/assets/QC state
- machine-readable workflow files
- machine-readable regression cases
- executable test runner
- WeChat delivery verifier
- CLI for inspect/resize/split/icon/banner/qc/package

## Quick start

```bash
python tools/cli.py inspect path/to/image.png
python tools/cli.py resize input.png output.png --width 500 --height 500 --background transparent
python tools/cli.py split sheet.png out_dir --rows 3 --cols 4 --width 500 --height 500
python tools/cli.py qc-image sticker.png --profile main_sticker
python tools/cli.py qc-project project_dir
python tools/cli.py package project_dir release.zip
python tests/test_runner.py
```

## Design principle
Creative generation and semantic editing are model tasks. Technical image operations are deterministic tool tasks and must not regenerate artwork.


## V1.2 breaking workflow change
Batch generation is blocked until the user explicitly approves the master character image. WeChat delivery defaults are now: 1–24 main stickers at 240×240 transparent PNG, 240×240 transparent cover, 50×50 transparent icon, 750×400 light-background banner, name, description, and ZIP.

## V1.7 complete-package note
This release is intentionally rebuilt from the complete V1.2 executable repository, not from the smaller incremental V1.3–V1.6 folders. It contains tools, schemas, workflows, templates, platform files, regression tests and all later rule additions.

Before use in Codex, run:
`python3 tools/validate_package.py`

If validation fails, do not use an older-version file as a silent substitute; restore the complete V1.7 package first.
