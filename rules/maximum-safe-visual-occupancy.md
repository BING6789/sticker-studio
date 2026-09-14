# T41 — Maximum Safe Visual Occupancy

## Principle
**Within platform-safe bounds, bigger is better.**

WeChat assets should use as much of the available visual area as possible while preserving clarity, identity, action, text and required safety edges.

This applies to:
- main stickers;
- cover;
- icon/avatar.

## Why
Equal canvas dimensions do not create equal perceived size. Excess transparent margins make an otherwise correct asset look smaller in the WeChat chat UI, store UI and pack selector.

## Processing order
For approved artwork:
1. finalize character / text;
2. apply T40 night-mode safety edge where applicable;
3. compute final alpha/content bounds;
4. enlarge proportionally toward maximum safe occupancy;
5. correct visual center, not only geometric center;
6. export to final platform dimensions;
7. inspect at realistic UI size against comparison assets.

## Main stickers — 240×240
Default objective:
- maximize character + text + required action/effect area;
- minimize unused transparent margins;
- prioritize face, expression and upper-body gesture unless full body is semantically necessary;
- do not add “breathing room” that weakens chat-window size.

## Cover — 240×240
The approved representative sticker should also be scaled for maximum safe occupancy:
- retain exactly one approved sticker;
- no extra title/name/slogan/decorations;
- minimize surrounding empty space;
- preserve all approved sticker text and T40 outline;
- do not redraw.

## Icon — 100×100
The main-character head portrait should fill the icon area as much as safely possible:
- head/face dominates;
- minimal transparent margin;
- no text, prop, decoration or extra character;
- preserve T38 series differentiation;
- do not shrink the headshot merely to create aesthetic whitespace.

At tiny pack-selector size, face and signature expression must remain instantly recognizable.

## Visual center
Do not rely only on alpha bounding-box centering.

Evaluate:
- face position;
- perceived mass;
- extended hand/gesture;
- long ears/hair/tie;
- asymmetric text;
- props/effects.

The asset should *look* centered and large, even when its mathematical bounding box is asymmetric.

## Comparison test
QC must include side-by-side comparison with representative peer-sized assets at realistic interface display size.

Fail if:
- the asset looks clearly smaller than comparable stickers/icons/covers;
- a large transparent margin remains without semantic need;
- face/expression becomes too small;
- size is reduced merely for composition “comfort.”

## Safety
Never enlarge until:
- text or white outline is clipped;
- hair/ears/fingers/gesture are clipped;
- anti-aliased T40 edge is cut;
- icon identity becomes awkwardly cropped;
- cover/sticker becomes visibly cramped.

## Severity
P1 MUST FIX:
- avoidable transparent margins cause materially smaller perceived size;
- main sticker, cover or icon is clearly undersized compared with peers;
- visual center is poor despite geometric centering;
- enlargement clips required content or T40 edge.

P2 WARNING:
- occupancy is acceptable but not yet near the best safe visual size.

## Pixel Safe
For already-approved artwork, resizing/repositioning to satisfy T41 is technical processing:
**NO REGENERATION.**
