from __future__ import annotations
from pathlib import Path
import json
from jsonschema import validate


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def validate_file(instance_path, schema_path):
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    validate(instance=instance, schema=schema)
    return True


def resolve_sticker(assets_path, order_or_id):
    data = load_json(assets_path)
    for a in data.get("stickers", []):
        if str(a.get("id")) == str(order_or_id) or str(a.get("order")) == str(order_or_id):
            return a
    raise KeyError(f"Sticker not found: {order_or_id}")
