# T45 Regression

PASS:
- 240×240 sticker is finalized after T40 using alpha/content bounds and visual-center correction;
- 240×240 cover uses the single approved sticker at maximum safe size;
- 100×100 icon is a large-head asset with minimal safe transparent margin;
- occupancy correction uses Pixel Safe scale/reposition only.

P1 FAIL:
- obvious safe transparent area remains unused;
- icon sits small in the center with roughly half the canvas empty;
- character was shrunk to make room for side text;
- realistic WeChat preview is visibly smaller than peer assets.

P0 FAIL:
- T40 edge, text, ears/hair, gesture or required content is clipped.
