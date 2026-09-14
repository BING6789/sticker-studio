# T34 — Effective Visual Occupancy

240×240 canvas consistency is not enough. Check the alpha bounding box and perceived visual weight of meaningful visible content. Reduce meaningless transparent margins and normalize scale/repositioning relative to the pack median, without clipping text, white outlines, character features, gestures, props or necessary effects.

Do not force content to touch every edge or use one rigid occupancy percentage. Final QC combines alpha-bounding-box inspection with a same-size contact-sheet review.

P1 MUST FIX: avoidable transparent margins make a sticker materially smaller than the set, or normalization clips meaningful content.
P2 WARNING: perceived visual weight is noticeably inconsistent.


## V2.1 upgrade — Maximum Safe Occupancy
For WeChat production assets, the default objective is no longer merely “consistent occupancy.” It is:

> **maximize effective visual size within safe bounds.**

For main stickers, cover and icon:
- minimize meaningless transparent margins;
- scale the approved visual until the outermost required element approaches the safe edge;
- preserve all text, night-mode outline, facial features, gestures and required effects;
- do not shrink merely for aesthetic breathing room;
- compare perceived size against peer stickers/assets at realistic UI size.

A technically valid 240×240 or 100×100 file that looks materially smaller than comparable assets is a P1 failure.
