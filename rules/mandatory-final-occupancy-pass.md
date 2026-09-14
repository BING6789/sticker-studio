# T45 — Mandatory Final Occupancy Pass

## Core principle
T41 is not merely a prompt or QC preference. **Every final WeChat asset must pass a Pixel Safe occupancy finalization step after generation/editing and before delivery.**

Applies to:
- main stickers 240×240;
- cover 240×240;
- icon 100×100.

## Required order
1. approved art/text is complete;
2. T40 night-mode safety edge is applied where required;
3. compute final alpha/content bounds including text, subject, required props/effects and T40 edge;
4. detect avoidable transparent margins;
5. proportionally enlarge toward maximum safe occupancy;
6. reposition using visual center, not bounding-box center alone;
7. export at exact platform dimensions;
8. inspect at realistic WeChat UI size;
9. compare against representative peer-sized assets;
10. repair undersized/clipped assets only; do not regenerate approved art for occupancy correction.

## Completion gate
If there is still obvious safe transparent space that can be used to enlarge the meaningful visual without clipping or harming composition, the asset is **not final**.

## Main sticker rule
Character-first occupancy has priority over typography convenience. Do not shrink the character merely to reserve a large side text block. T43/T44 text must adapt around the maximized character.

## Icon rule — stricter
The 100×100 icon is a dedicated large-head asset, not a shrunken full-body sticker.
- head/face/signature expression dominate the canvas;
- minimize transparent margins aggressively but safely;
- preserve ears/hair/signature silhouette and T40 edge;
- no text/props/decorations;
- if approximately half the icon is avoidable transparent area, P1 FAIL.

## Cover rule
The single approved representative sticker should use the 240×240 cover area as fully as safely possible while retaining its approved content and T40 edge.

## Pixel Safe
Occupancy correction on approved art is engineering processing:
**NO REGENERATION, NO REDRAW, NO STYLE CHANGE.**
Only scale/reposition/pad/canvas operations required to satisfy the platform asset are allowed.

## Severity
P0 BLOCK:
- wrong final dimensions/format/transparency;
- required content or T40 edge clipped.

P1 MUST FIX:
- obvious avoidable transparent margin remains;
- sticker/cover/icon is materially smaller than peers at realistic UI size;
- icon occupies only a small central region;
- typography convenience caused character shrinkage;
- geometric centering produces poor visual centering.
