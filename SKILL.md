---
name: Sticker Studio
description: 一站式表情包设计与制作 Skill，支持角色/IP设计、文案、动作分镜、视觉生产、透明背景、图标封面、平台规格适配、审核风险提示和最终质检。
---

# Sticker Studio

## P0 Gate — Master Character First
For every CREATE project, the system MUST generate or establish a master character image before batch production. The user must explicitly approve that master character. Record `master_character.approved=true` and lock the approved asset as `master_reference`. **No user-approved master character = no batch sticker generation.** This gate cannot be silently bypassed.

If the user supplies an existing character, treat that asset as the candidate master reference, confirm the visual interpretation, obtain approval, then lock it.


## Mission
Turn an idea, copy list, or character reference into a consistent, sendable, platform-ready static sticker pack. The skill acts as IP planner, copy editor, storyboard director, visual-production controller, deterministic image-processing controller, QC system, and delivery packager.

Current public release prioritizes WeChat static sticker packs while keeping platform rules modular.

## Entry protocol
1. Read `manifest.yaml`.
2. Classify the user request using `rules/intent-routing.md`.
3. Load only the rule/workflow/platform files required by that route.
4. If a deterministic tool exists for the requested operation, use it instead of image generation.
5. Maintain project state using `schemas/project.schema.json`, `schemas/assets.schema.json`, and `schemas/qc.schema.json`.
6. Run QC before packaging and platform delivery.

## Route map
- `CREATE` → `rules/character-lock.md`, `rules/copywriting.md`, `workflows/create.yaml`
- `COPY` → `rules/copywriting.md`
- `STORYBOARD` → `rules/storyboard.md`
- `GENERATE` → `rules/generation.md`; image generation allowed
- `EDIT` → `rules/generation.md`; semantic image editing allowed, preserve unspecified content
- `PROCESS` → `rules/pixel-safe.md`, `workflows/process.yaml`, deterministic tools only
- `SPLIT` → `rules/pixel-safe.md`, `workflows/split.yaml`, `tools/cli.py split`
- `QC` → `rules/quality-control.md`, `tools/cli.py qc-image|qc-project`
- `PLATFORM_ASSET` → selected platform profile + `workflows/wechat-delivery.yaml`
- `PACKAGE` → platform profile + QC + `tools/cli.py package`

## Non-negotiable principles
1. **Understand before generate.** Route intent before choosing a production action.
2. **Preserve beats regenerate.** When a usable source image exists, prefer editing/processing it.
3. **Pixel Safe Mode.** Resize, crop, pad, alpha, background, format conversion, split, compress, rename and package must not redraw content.
4. **Locked means locked.** Do not drift locked character traits without explicit user approval.
5. **Failed-only repair.** Repair only failed assets; never regenerate a whole set because one item failed.
6. **Platform rules override defaults.** Platform profile > project defaults > generic defaults.
7. **Discussion means no generation.** “先讨论” and equivalents block image generation.
8. **No silent creative changes.** Do not improve unspecified elements.
9. **Minimum-change interpretation.** “其他不变/only change X” means preserve everything except X.
10. **One production error becomes one regression test.** Record root cause, rule update and test.

## Deterministic execution layer
The following operations MUST use deterministic tooling whenever a usable source file exists:
- inspect metadata
- resize/pad/canvas adaptation
- alpha/transparency verification
- sheet splitting
- file format conversion
- icon technical composition from an approved icon source
- banner technical composition from an approved sticker source
- file/set QC
- packaging

These operations MUST NOT invoke image generation.

## Project state
Maintain three machine-readable files in a project workspace:
- `project/project.json`: project identity, defaults, platform, status
- `project/assets.json`: canonical source/final asset mapping and per-asset status
- `project/qc.json`: QC checks, severity, failures, warnings and delivery status

Never infer “第17张” from filesystem order when `assets.json` exists. Resolve it by asset ID/order in project state.

## Character lock
Use `templates/character.json` and `rules/character-lock.md`.
- `locked`: identity-defining traits that cannot drift.
- `variable`: expression, pose, gesture, direction, props, emotional intensity, composition.
- `forbidden`: known drift modes and unwanted additions.
- `master_references`: canonical images/asset IDs when available.

## Copy engine
For a user-approved set of up to 24 stickers, seek balanced coverage across high-frequency replies, emotional reactions, social interaction, situations, IP-specific lines and positive/supportive reactions. Score candidates 1–5 on Sendability, Personality and Visuality. Detect semantic/emotional duplication, not only duplicate strings.

## Storyboard engine
Before generation, create a production card containing copy, emotion, face, body/action, props, visual contrast/joke, composition, text treatment and output spec. Prefer designs that remain understandable after removing text.

## Generation and editing
Use generation only for new visuals or semantic changes such as expression, pose, object, style or character action. For an existing target, preserve all locked traits and all unspecified content.

## “Other unchanged” protocol
When the user says “其他不变”, “everything else unchanged”, “only X”, or equivalent:
- set `PRESERVE_ALL=true`;
- define only requested fields under `CHANGE_ONLY`;
- preserve all other pixels/semantics to the maximum extent supported by the operation.

Technical changes stay in Pixel Safe Mode. Semantic edits use image editing but must preserve unspecified content.

## Platform profiles
Load machine-readable platform settings from `platforms/*.yaml`. For WeChat use `platforms/wechat.yaml`. The human-readable description remains in `platforms/wechat.md`.

If current official requirements conflict with the profile, verify the latest official requirement, update the profile, and add/update platform regression tests before delivery.

## QC pipeline
Run file, content, character, small-size and set-level QC according to `rules/quality-control.md`.
Severity:
- `P0 BLOCK`: wrong size/format/transparency/count or explicit instruction violation.
- `P1 MUST_FIX`: wrong text, clipping, neighboring artifacts, severe character drift, unintended elements.
- `P2 WARNING`: weak sendability, repetitive poses/emotions, low IP personality, weak small-size readability.

Do not package a formal release until all detectable P0/P1 technical failures are resolved or explicitly accepted by the user.

## Delivery
For WeChat, execute `workflows/wechat-delivery.yaml` and validate against `platforms/wechat.yaml`. Deliver a structured release pack with main stickers, icon, banner, preview, project metadata, QC report and release ZIP.

## Regression discipline
Every discovered production error must produce an error record with ERROR_ID, input, expected, actual, root cause, new rule, regression test and status. Re-run `python tests/test_runner.py` after changes.

## V1.1 boundaries
Static stickers only. GIF/video/animation are out of scope. A concept sheet is not a delivery asset. Final stickers are individual files. Image-generation consistency can be evaluated but cannot be guaranteed by deterministic tooling alone.

## V1.3–V1.7 Consolidated Production Rules

These rules extend the complete V1.2 executable base. They are additive and MUST NOT be satisfied by silently falling back to older rules.

- T26: Dynamic text–visual integration (`rules/text-composition.md`)
- T27: Single-approved-sticker 750×400 banner (`rules/banner-director.md`)
- T28–T30: Copy-driven variation, identity preservation, Minimal Sufficient Variation (`rules/character-variation.md`)
- T31: WeChat icon is 100×100 transparent approved-character headshot (`rules/icon-director.md`)
- T32: Small-canvas visual priority (`rules/small-canvas-composition.md`)
- T33: Dark-mode text readability with adaptive white outline (`rules/dark-mode-typography.md`)
- T34: Effective visual occupancy / alpha-bound visual-weight consistency (`rules/effective-visual-occupancy.md`)
- T35: Controlled contextual wardrobe variation (`rules/contextual-wardrobe-variation.md`)
- T36: Expressive typography + selective keyword emphasis (`rules/expressive-typography.md`)

### Typography execution order
IP typography identity → emotional rhythm → keyword emphasis (NONE/LIGHT/STRONG) → dynamic placement → white outline → light/dark/small-size QC.

### Character variation execution order
Expression → Action → Prop → Outfit.
Outfit changes are contextual, never random, and MASTER_REFERENCE identity remains locked.

### Final-size execution order
Small-canvas composition → dynamic typography → dark-mode outline → alpha-bounding-box occupancy check → same-size pack visual-weight review → 240×240 export.

## V1.8 Wardrobe Library & Selection Director
After MASTER_REFERENCE approval and before batch storyboarding, define/confirm a controlled 3–5 state wardrobe library when clothing can support scene communication. Use `rules/wardrobe-library-selection.md`, the wardrobe schema and template. Follow **Expression → Action → Prop → Outfit State → Outfit Change**. Base clothing is default, not mandatory. Never rotate outfits randomly; MASTER_REFERENCE identity overrides wardrobe variation.

## V1.9 Series Icon + Market Fit

### T38 — Series Icon Differentiation
For same-IP follow-up packs, read `rules/series-icon-differentiation.md` and maintain `series-icon-registry`. Same character identity must be preserved, but each series icon must have a clearly distinct signature expression/head state at 100×100 and chat-strip preview size.

### T39 — Sticker Market Fit Matrix
Before finalizing a new IP/series, score F/S/P/R/V/E/M/K using `rules/market-fit-matrix.md`. Use the result to determine whether the concept is primarily traffic-oriented, sendability-oriented, niche/vertical or long-term IP-oriented.

Market Fit is a decision aid, not a reason to override MASTER_REFERENCE, user-approved copy, platform specs or production gates.

## V2.0 Adaptive Night-Mode Outline

### T40 — Adaptive Night-Mode Outline
All final stickers default to a night-mode safety edge for both text and the main subject. Read `rules/adaptive-night-mode-outline.md`.

The edge is adaptive, outward-only and anti-aliased. It must be nearly imperceptible on white/light backgrounds while making the subject and text immediately distinguishable on dark/night backgrounds.

Do not use a fixed universal stroke width. Do not create jagged contours, fuzzy halos, dirty fringes or glow effects.

Required QC backgrounds: white, light gray, dark gray, near-black. Run both final 240×240 and realistic smaller chat-preview checks.

When applied to approved artwork, T40 is Pixel Safe technical processing: **NO REGENERATION**.

## V2.1 Maximum Safe Visual Occupancy

### T41 — Main sticker + cover + icon
All WeChat production assets default to maximum safe visual occupancy.

Apply T41 to:
- 240×240 main stickers;
- 240×240 cover;
- 100×100 icon.

Minimize meaningless transparent margins. Scale approved art until required content approaches the safe edge, while preserving text, character features, gestures and T40 night-mode outline.

Use visual centering, not merely bounding-box centering. Final QC must include realistic UI-size comparison against representative peer-sized assets.

For approved artwork, scale/reposition only: **NO REGENERATION**.

## V2.2 Platform Review Advisory Preflight
T42 adds advisory platform-review screening before copy lock and before packaging. Known rejection cases trigger warnings and safer alternatives, but the user retains the final creative decision. If the user explicitly keeps the original wording, preserve it and continue unless higher-level safety requirements independently prohibit the request. Consult `data/wechat-review-cases.json`; never present heuristics as an official blacklist.

## V2.3 Character-First Typography Composition

### T43 — Character first; typography performs with the character
Typography must not become a detached caption block that forces the IP character to shrink. Start from T41 maximum-safe character occupancy, then adapt text size, line breaks, path and controlled overlap around the pose.

For medium/long copy, reduce/adapt typography before reducing the character. Arc, semi-ring, staggered, directional and controlled-overlap layouts are explicitly allowed. Text may overlap low-information body/clothing areas but must protect eyes, mouth, identity anchors, core gestures and meaning-critical props.

Typography may perform emotion *within the sentence* through progressive size, spacing, baseline and direction. Standard positive case: `让我缓缓` may use progressively larger characters with looser spacing and a subtly descending baseline to reinforce fatigue.

T43 works with T26 + T36 + T41: text integrates with the visual, acts in the character's voice, and does not steal the canvas from the character.

## V2.4 Semantic Reading + Mandatory Occupancy

### T44 — Semantic Reading & Local Contrast Typography
Flexible typography must preserve one-glance reading. Keep one semantic sentence as one continuous visual unit by default. Split only when semantic structure/action binding makes the split clearer (e.g. `饼有了，钱呢？`, with `钱呢？` bound to the open palm). Use a Local Contrast Map and resolve collisions by placement → adaptive text color/value → local separation → subtle backing only as last resort.

### T45 — Mandatory Final Occupancy Pass
T41 is now enforced as a required Pixel Safe finalization step for every main sticker, cover and icon. After T40, compute final content bounds, enlarge toward maximum safe occupancy, correct visual center, and compare at realistic WeChat size. Obvious usable transparent margin means the asset is not final. Icon enforcement is stricter: dedicated large-head composition, minimal safe margin, never a small centered portrait.

### Rule precedence for final composition
Character identity/safety → semantic readability → character-first maximum occupancy → typography performance → decorative effects.
Typography convenience must never shrink the character or break reading continuity.
