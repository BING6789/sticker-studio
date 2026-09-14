from __future__ import annotations
from PIL import Image, ImageChops
from pathlib import Path
import json, zipfile, math, os


def inspect_image(path: str) -> dict:
    p = Path(path)
    with Image.open(p) as im:
        rgba = im.convert("RGBA")
        alpha = rgba.getchannel("A")
        amin, amax = alpha.getextrema()
        return {
            "path": str(p),
            "width": im.width,
            "height": im.height,
            "format": im.format or p.suffix.lstrip('.').upper(),
            "mode": im.mode,
            "has_alpha_channel": "A" in rgba.getbands(),
            "alpha_min": int(amin),
            "alpha_max": int(amax),
            "has_transparent_pixels": amin < 255,
            "is_fully_opaque": amin == 255,
        }


def _parse_bg(background: str):
    if background == "transparent":
        return (0, 0, 0, 0)
    if background == "light":
        return (247, 244, 238, 255)
    if background.startswith("#") and len(background) in (7, 9):
        s = background[1:]
        vals = tuple(int(s[i:i+2], 16) for i in range(0, len(s), 2))
        return vals if len(vals) == 4 else vals + (255,)
    raise ValueError(f"Unsupported background: {background}")


def resize_and_pad(src: str, dst: str, width: int, height: int, background: str = "transparent", margin: int = 0) -> dict:
    im = Image.open(src).convert("RGBA")
    usable_w = max(1, width - 2 * margin)
    usable_h = max(1, height - 2 * margin)
    scale = min(usable_w / im.width, usable_h / im.height)
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    resized = im.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), _parse_bg(background))
    x = (width - resized.width) // 2
    y = (height - resized.height) // 2
    canvas.alpha_composite(resized, (x, y))
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, "PNG", optimize=True)
    return inspect_image(dst)


def verify_alpha(path: str, require_transparency: bool = True) -> dict:
    info = inspect_image(path)
    ok = info["has_transparent_pixels"] if require_transparency else True
    return {"ok": bool(ok), "require_transparency": require_transparency, "info": info}


def content_bbox(im: Image.Image, alpha_threshold: int = 8):
    alpha = im.convert("RGBA").getchannel("A")
    mask = alpha.point(lambda v: 255 if v > alpha_threshold else 0)
    return mask.getbbox()


def split_sticker_sheet(src: str, out_dir: str, rows: int, cols: int, width: int = 500, height: int = 500,
                        background: str = "transparent", boxes: list | None = None, trim: bool = True,
                        margin: int = 20) -> list[dict]:
    im = Image.open(src).convert("RGBA")
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    if boxes is None:
        cell_w, cell_h = im.width / cols, im.height / rows
        boxes = []
        for r in range(rows):
            for c in range(cols):
                x0 = round(c * cell_w); x1 = round((c + 1) * cell_w)
                y0 = round(r * cell_h); y1 = round((r + 1) * cell_h)
                boxes.append([x0, y0, x1, y1])
    if len(boxes) != rows * cols:
        raise ValueError("boxes length must equal rows*cols")
    results = []
    for i, box in enumerate(boxes, 1):
        crop = im.crop(tuple(box))
        if trim:
            bb = content_bbox(crop)
            if bb:
                crop = crop.crop(bb)
        tmp = out / f".{i:02d}_tmp.png"
        crop.save(tmp, "PNG")
        final = out / f"{i:02d}.png"
        resize_and_pad(str(tmp), str(final), width, height, background, margin=margin)
        tmp.unlink(missing_ok=True)
        results.append(inspect_image(str(final)))
    return results


def create_cover_asset(src: str, dst: str) -> dict:
    return resize_and_pad(src, dst, 240, 240, "transparent", margin=8)


def create_icon_asset(src: str, dst: str) -> dict:
    # Technical composition only. Semantic requirements (headshot/no text/no props) must be satisfied by the approved source.
    return resize_and_pad(src, dst, 50, 50, "transparent", margin=2)


def create_banner_asset(src: str, dst: str, background: str = "light") -> dict:
    return resize_and_pad(src, dst, 750, 400, background, margin=20)


def qc_image(path: str, width: int | None = None, height: int | None = None,
             fmt: str = "PNG", transparency: str = "optional") -> dict:
    info = inspect_image(path)
    failures = []
    if width is not None and info["width"] != width:
        failures.append({"severity": "P0", "code": "WIDTH", "expected": width, "actual": info["width"]})
    if height is not None and info["height"] != height:
        failures.append({"severity": "P0", "code": "HEIGHT", "expected": height, "actual": info["height"]})
    if fmt and info["format"].upper() != fmt.upper():
        failures.append({"severity": "P0", "code": "FORMAT", "expected": fmt, "actual": info["format"]})
    if transparency == "required" and not info["has_transparent_pixels"]:
        failures.append({"severity": "P0", "code": "TRANSPARENCY", "expected": "transparent pixels", "actual": "opaque"})
    return {"path": path, "overall": "PASS" if not failures else "FAIL", "failures": failures, "info": info}


def _load_yaml(path: str) -> dict:
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def qc_project(project_dir: str, platform_profile: str) -> dict:
    root = Path(project_dir)
    profile = _load_yaml(platform_profile)
    checks, failures, warnings = [], [], []
    main = profile["main_sticker"]
    sticker_dir = root / "stickers"
    sticker_files = sorted(sticker_dir.glob("*.png")) if sticker_dir.exists() else []
    if len(sticker_files) < 1 or len(sticker_files) > int(main.get("max_count", 24)):
        failures.append({"severity":"P0","code":"STICKER_COUNT","expected":"1-24","actual":len(sticker_files)})
    project_file = root / "project" / "project.json"
    if project_file.exists():
        pdata = json.loads(project_file.read_text(encoding="utf-8"))
        expected_count = pdata.get("sticker_count")
        if expected_count is not None and len(sticker_files) != expected_count:
            failures.append({"severity":"P0","code":"APPROVED_STICKER_COUNT_MISMATCH","expected":expected_count,"actual":len(sticker_files)})
        mc = pdata.get("master_character", {})
        if not mc.get("approved") or not mc.get("reference"):
            failures.append({"severity":"P0","code":"MASTER_CHARACTER_NOT_APPROVED"})
    else:
        failures.append({"severity":"P0","code":"MISSING_PROJECT_STATE"})
    for p in sticker_files:
        q = qc_image(str(p), main["width"], main["height"], main["format"], main["transparency"])
        checks.append(q)
        failures.extend(q["failures"])
    cover_path = root / "wechat" / "cover_240x240.png"
    icon_path = root / "wechat" / "icon_50x50.png"
    banner_path = root / "wechat" / "banner_750x400.png"
    if not cover_path.exists():
        failures.append({"severity":"P0","code":"MISSING_COVER"})
    else:
        c = profile["cover"]
        q = qc_image(str(cover_path), c["width"], c["height"], c["format"], c["transparency"])
        checks.append(q); failures.extend(q["failures"])
    if not icon_path.exists():
        failures.append({"severity":"P0","code":"MISSING_ICON"})
    else:
        i = profile["icon"]
        q = qc_image(str(icon_path), i["width"], i["height"], i["format"], i["transparency"])
        checks.append(q); failures.extend(q["failures"])
    if not banner_path.exists():
        failures.append({"severity":"P0","code":"MISSING_BANNER"})
    else:
        b = profile["banner"]
        q = qc_image(str(banner_path), b["width"], b["height"], b["format"], b["transparency"])
        checks.append(q); failures.extend(q["failures"])
    for req in profile["release"]["required_files"]:
        p = root / req
        if not p.exists():
            failures.append({"severity":"P0","code":"MISSING_REQUIRED_FILE","path":req})
    overall = "FAIL" if failures else ("WARNING" if warnings else "PASS")
    return {"overall": overall, "checks": checks, "failures": failures, "warnings": warnings,
            "platform_delivery": {"platform": profile["platform"], "sticker_count": len(sticker_files)}}


def write_json(path: str, data: dict):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def package_project(project_dir: str, zip_path: str, require_qc_pass: bool = True) -> str:
    root = Path(project_dir)
    qc_file = root / "project" / "qc.json"
    if require_qc_pass:
        if not qc_file.exists():
            raise RuntimeError("project/qc.json missing")
        qc = json.loads(qc_file.read_text(encoding="utf-8"))
        if qc.get("overall") != "PASS":
            raise RuntimeError(f"QC is not PASS: {qc.get('overall')}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                z.write(p, arcname=str(p.relative_to(root.parent)))
    return zip_path
