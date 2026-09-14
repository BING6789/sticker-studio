# Changelog

## 1.2.0 — 2026-09-11

### P0 workflow change
- Added **Master Character Approval Gate**: no batch sticker generation before explicit user approval of the master character image.
- Approved master image is stored as `master_reference` in project state.

### WeChat delivery contract changed
- Main stickers: user-approved count, maximum 24; 240×240 transparent PNG.
- Cover: 240×240 transparent PNG.
- Avatar icon: 50×50 transparent PNG.
- Banner: 750×400 PNG, light background.
- Required text: name and introduction/description.
- Final artifact: ZIP after QC PASS.

### Execution/QC
- Updated deterministic resize/split defaults to 240×240.
- Added cover asset processing.
- Updated icon processing to 50×50.
- QC now validates approved sticker count and master-character approval state.
- Packaging remains blocked unless QC is PASS.

## V1.7
- Rebuilt as a **complete package** on top of the full V1.2 executable base, then merged V1.3–V1.6 rules forward.
- Added T36 Expressive Typography Director.
- Added selective keyword emphasis modes: NONE / LIGHT / STRONG.
- Added package integrity inventory and validator to prevent missing-file fallback.
- Codex/agents MUST report package-integrity failure instead of silently substituting older-version files.

## V1.8
- Added T37 Wardrobe Library & Selection Director.
- Added controlled 3–5 state wardrobe library for suitable IPs.
- Added Outfit State before full Outfit Change.
- Added wardrobe schema/template and regression coverage.

## V1.9
- Added T38 Series Icon Differentiation.
- Added persistent Series Icon Registry schema/template.
- Added T39 Sticker Market Fit Matrix.
- Added F/S/P/R/V/E/M/K scoring and evidence-level labeling.
- Added pre-series market-fit checkpoint and same-IP icon side-by-side QC.

## V2.0
- Added T40 Adaptive Night-Mode Outline.
- Night-mode protection now covers both text and character/subject silhouette.
- Added adaptive outward-only anti-aliased edge rules.
- Added explicit anti-jagged, anti-fuzzy-halo and anti-dirty-fringe QC.
- Added four-background preview QC and realistic small-chat one-glance recognition test.
- Applying night-mode protection to approved art is Pixel Safe and forbids regeneration.

## V2.1
- Upgraded T34 from occupancy consistency toward maximum safe occupancy.
- Added T41 Maximum Safe Visual Occupancy.
- T41 applies to main stickers, cover and 100×100 icon.
- Added visual-center correction and realistic UI peer-comparison QC.
- Added explicit rule that avoidable transparent margins and materially undersized assets are P1 failures.
- T40 night-mode outline is now included in the final occupancy bounds.
- Occupancy corrections on approved artwork are Pixel Safe and must not trigger regeneration.

## V2.2
- Added T42 advisory platform-review preflight.
- Added R0–R3 review-risk labels.
- Added WeChat real-case registry with OJBK and 真牛逼 as user-verified rejection cases.
- Added safer-copy suggestions.
- Review warnings do not force replacement; user retains final creative decision.
- Added copy-stage and final text+visual review passes.

## V2.3
- Added T43 Character-First Typography Composition.
- Explicitly prevents rigid detached text blocks from shrinking the IP character.
- Added adaptive copy-length strategies: smaller type, segmented, arc/semi-ring, staggered, directional and controlled-overlap layouts.
- Added intra-sentence typography acting: progressive size, spacing and baseline movement.
- Added `让我缓缓` as a positive regression case: progressively larger/slower typography can reinforce fatigue.
- Integrated T43 with T26 expressive placement, T36 typography performance and T41 maximum safe visual occupancy.

## V2.4
- Added T44 Semantic Reading & Local Contrast Typography.
- Added Semantic Split Gate and Reading Path Test.
- Added Local Contrast Map and contrast-resolution order; transparent backing is last resort.
- Added T45 Mandatory Final Occupancy Pass.
- Converted maximum occupancy from prompt/QC preference into a required Pixel Safe delivery-stage operation.
- Strengthened 100×100 icon occupancy: dedicated large-head asset; small centered icon with large empty margins is P1.
- Added explicit precedence so typography cannot shrink the character or break semantic reading.
- Added regression cases for `饼有了，钱呢？`, `让我缓缓`, same-color tie/text collision, and undersized icon.
