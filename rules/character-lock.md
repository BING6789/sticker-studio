# Character Lock

Before batch production, define and freeze character identity.

## Locked examples
species, age impression, body ratio, face shape, hair/ear shape, primary palette, signature clothing, signature accessories, base art style, personality cues.

## Variable examples
expression, pose, gesture, direction, prop, emotion intensity, composition.

## Forbidden examples
random accessories, costume drift, body-shape drift, age drift, unrequested cuteness/realism, random text, random badges.

If a generated asset violates a locked trait, mark P1 and repair that asset only.


## Master Character Approval Gate (P0)
For CREATE projects, generate a clean master character image before bulk sticker production. The user must explicitly approve this master image. Store the approval in project state and set it as `master_reference`. Until approval is recorded, `batch_generate` is forbidden. Revisions before approval must modify only the master-character stage.

For an existing user-supplied character, analyze it, confirm the interpretation with the user, and then lock the supplied/approved asset as the master reference. Do not redesign it unless requested.
