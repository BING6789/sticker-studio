# T40 — Adaptive Night-Mode Outline

## Goal
Every sticker must remain instantly recognizable in light and dark/night interfaces without looking like it has an obvious white sticker border on a white background.

**Target:** almost invisible on white/light backgrounds; immediately separating character + text from dark backgrounds.

## Scope
Default ON for all final stickers:
1. text contrast edge;
2. character / subject silhouette edge;
3. necessary props/effects when their loss would harm meaning.

## Adaptive, not fixed
Never apply one fixed stroke width/opacity to every sticker.

Determine edge treatment from:
- local luminance/contrast of the subject edge;
- final 240×240 size;
- line-art weight;
- subject darkness;
- text size/weight;
- perceived visual occupancy.

Dark edges/subjects may need a stronger near-white separation edge.
Light subjects should receive a weaker/minimal edge so the white-background view does not look heavy.

## Rendering model
Prefer a clean outward-only alpha-derived safety edge:
1. derive an anti-aliased outer silhouette from the approved alpha;
2. expand outward only;
3. use near-white/white separation treatment;
4. preserve smooth anti-aliased contour;
5. optionally use a very subtle low-opacity outer transition only when needed;
6. composite subject above the safety edge.

Do NOT erode, blur or repaint the approved subject.

## Hard quality constraints
- no jagged contour;
- no fuzzy halo;
- no dirty gray/black fringe;
- no clipped outline;
- no doubled/ghosted edge;
- no obvious glow effect;
- no materially enlarged “die-cut sticker” appearance on white background.

## Text
T33 remains active. Text uses adaptive white/near-white outline as required for dark-mode readability. T40 extends the same night-mode safety concept to the full subject silhouette.

## Required preview backgrounds
QC at final size and small chat preview on:
- white;
- light gray;
- dark gray;
- near-black / night mode.

## One-glance test
At realistic chat-preview size, a viewer should identify:
- character silhouette;
- face/expression;
- core gesture/action;
- text;
in the first glance, without needing to inspect the sticker.

## QC severity
P0 BLOCK:
- final PNG loses true transparency or required content is clipped.

P1 MUST FIX:
- dark subject merges into dark background;
- text is not immediately readable;
- jagged, fuzzy, dirty, doubled or halo-like outline;
- outline visibly damages approved art;
- white-background border is conspicuously heavy.

P2 WARNING:
- outline is technically functional but inconsistent with pack visual weight;
- light-background edge is more visible than necessary.

## Pixel Safe rule
When T40 is applied to already-approved artwork, it is technical processing:
**NO REGENERATION.**
Do not redraw the character merely to improve night-mode contrast.
