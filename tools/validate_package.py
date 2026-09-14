from pathlib import Path
import json, hashlib, sys

ROOT=Path(__file__).resolve().parents[1]
inv_path=ROOT/"FILE_INVENTORY.json"
if not inv_path.exists():
    print("FAIL: FILE_INVENTORY.json missing")
    sys.exit(2)
inv=json.loads(inv_path.read_text(encoding="utf-8"))
missing=[]
mismatch=[]
for rel, expected in inv["files"].items():
    p=ROOT/rel
    if not p.exists():
        missing.append(rel); continue
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual != expected:
        mismatch.append(rel)
if missing or mismatch:
    print("PACKAGE INTEGRITY: FAIL")
    if missing:
        print("Missing files:")
        for x in missing: print(" -",x)
    if mismatch:
        print("Hash mismatch:")
        for x in mismatch: print(" -",x)
    print("Do NOT silently fall back to an older Sticker Skill version.")
    sys.exit(1)
print(f"PACKAGE INTEGRITY: PASS ({len(inv['files'])} required files)")
