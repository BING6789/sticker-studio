# T42 Regression

PASS:
- OJBK / 真牛逼 match known R3 user-verified rejection cases.
- Warn + suggest alternatives; never silently replace.
- If user explicitly keeps original copy, preserve it and continue if otherwise allowed.
- Heuristics are not mislabeled as official banned words.

FAIL:
- platform risk becomes an unconditional production block;
- user-approved wording is silently sanitized;
- known rejection evidence is ignored.
