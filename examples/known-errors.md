# Known Production Errors

## E001 — Split routed to Generate
Input: “拆成12张500×500透明PNG”
Expected: technical split and ZIP.
Actual: another 12-grid was generated.
Root cause: wrong intent routing.
Rule: SPLIT always enters Pixel Safe Mode.
Regression: T01.
Status: fixed in spec.

## E002 — Default ratio drift
Expected formal WeChat sticker but output changed ratio.
Rule: default formal WeChat single sticker = 500×500 transparent PNG.
Regression: T06/T07.
Status: fixed in spec.

## E003 — Remove text caused redraw
Input: remove text, everything else unchanged.
Expected: preserve all except text.
Actual: visual was regenerated.
Rule: PRESERVE_ALL + CHANGE_ONLY.
Regression: T03.
Status: fixed in spec.

## E004 — Fake transparency
Checkerboard appearance was treated as transparency.
Rule: inspect actual alpha channel.
Regression: T13.
Status: fixed in spec.

## E005 — Grid split artifacts
Blind slicing caused clipping/neighbor fragments.
Rule: detect actual content bounds and QC each extraction.
Regression: T14/T15.
Status: fixed in spec.

## E006 — Dark Mode Text Readability
Project: 细狗 / Thin Dog.
Problem: dark sticker text became hard to read in night mode.
Root cause: no dark-background QC preview.
Permanent correction: adaptive white text outline + light/dark/small-size QC.
Regression: T33.
