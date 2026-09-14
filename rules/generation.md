# Generation & Editing

Generate only when new semantic pixels are required. Editing an existing image must preserve all unspecified content and character locks.

A review sheet is not a final export. Do not regenerate a sheet when the user asks to split/export it.

When one item fails, regenerate/edit only that item unless the user explicitly requests a full redesign.


## P0 Precondition
`batch_generate` MUST verify `master_character.approved == true` and a non-empty `master_reference`. If either condition is false, stop and request user approval of the master character.
