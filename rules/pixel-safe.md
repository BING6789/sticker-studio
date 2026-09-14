# Pixel Safe Mode

## Trigger operations
resize, crop, pad, alpha/transparency processing, background replacement when it can be done technically, format conversion, split, compress, rename, package.

## Allowed
pixel manipulation, canvas resize, alpha manipulation, lossless extraction, proportional scaling, repositioning on canvas, file conversion, packaging.

## Forbidden
redrawing, restyling, character regeneration, prop invention, copy rewriting, composition reinterpretation.

## Split protocol
1. Use the approved source sheet only.
2. Detect actual content boundaries; do not assume a perfect equal grid if content crosses cells.
3. Preserve full text/action/effects.
4. Remove neighboring fragments only; do not redraw missing content.
5. Scale proportionally onto target canvas.
6. Validate every extracted asset before ZIP.
