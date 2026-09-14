# Sticker Skill V2.1 Complete Acceptance Report

**Result: PASS**

## T41 — Maximum Safe Visual Occupancy
V2.1 now requires maximum safe use of the available canvas for:
- 240×240 main stickers;
- 240×240 cover;
- 100×100 icon.

Key rules:
- minimize meaningless transparent margins;
- bigger is preferred within safe bounds;
- T40 night-mode edge is included in the final content bounds;
- visual center is checked in addition to geometric center;
- realistic WeChat UI-size peer comparison is mandatory;
- visibly undersized sticker/icon/cover is P1;
- approved artwork may only be resized/repositioned, never regenerated for occupancy correction.

## Completeness
V2.1 is built from V2.0 Complete and retains all prior rules and package structure.
