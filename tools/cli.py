#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys
from sticker_tools import inspect_image, resize_and_pad, verify_alpha, split_sticker_sheet, create_cover_asset, create_icon_asset, create_banner_asset, qc_image, qc_project, write_json, package_project

ROOT = Path(__file__).resolve().parents[1]
WECHAT = ROOT / "platforms" / "wechat.yaml"

def dump(x): print(json.dumps(x, ensure_ascii=False, indent=2))

def main():
    p = argparse.ArgumentParser(prog="sticker-skill")
    sub = p.add_subparsers(dest="cmd", required=True)
    a=sub.add_parser("inspect"); a.add_argument("src")
    a=sub.add_parser("resize"); a.add_argument("src"); a.add_argument("dst"); a.add_argument("--width",type=int,required=True); a.add_argument("--height",type=int,required=True); a.add_argument("--background",default="transparent"); a.add_argument("--margin",type=int,default=0)
    a=sub.add_parser("verify-alpha"); a.add_argument("src")
    a=sub.add_parser("split"); a.add_argument("src"); a.add_argument("out_dir"); a.add_argument("--rows",type=int,required=True); a.add_argument("--cols",type=int,required=True); a.add_argument("--width",type=int,default=240); a.add_argument("--height",type=int,default=240); a.add_argument("--margin",type=int,default=20)
    a=sub.add_parser("cover"); a.add_argument("src"); a.add_argument("dst")
    a=sub.add_parser("icon"); a.add_argument("src"); a.add_argument("dst")
    a=sub.add_parser("banner"); a.add_argument("src"); a.add_argument("dst"); a.add_argument("--background",default="light")
    a=sub.add_parser("qc-image"); a.add_argument("src"); a.add_argument("--profile",choices=["main_sticker","cover","icon","banner"],required=True)
    a=sub.add_parser("qc-project"); a.add_argument("project_dir"); a.add_argument("--write",action="store_true")
    a=sub.add_parser("package"); a.add_argument("project_dir"); a.add_argument("zip_path")
    args=p.parse_args()
    if args.cmd=="inspect": dump(inspect_image(args.src))
    elif args.cmd=="resize": dump(resize_and_pad(args.src,args.dst,args.width,args.height,args.background,args.margin))
    elif args.cmd=="verify-alpha": dump(verify_alpha(args.src,True))
    elif args.cmd=="split": dump(split_sticker_sheet(args.src,args.out_dir,args.rows,args.cols,args.width,args.height,margin=args.margin))
    elif args.cmd=="cover": dump(create_cover_asset(args.src,args.dst))
    elif args.cmd=="icon": dump(create_icon_asset(args.src,args.dst))
    elif args.cmd=="banner": dump(create_banner_asset(args.src,args.dst,args.background))
    elif args.cmd=="qc-image":
        import yaml
        prof=yaml.safe_load(WECHAT.read_text(encoding="utf-8"))[args.profile]
        dump(qc_image(args.src,prof["width"],prof["height"],prof["format"],prof["transparency"]))
    elif args.cmd=="qc-project":
        q=qc_project(args.project_dir,str(WECHAT))
        if args.write: write_json(str(Path(args.project_dir)/"project"/"qc.json"),q)
        dump(q)
        if q["overall"]=="FAIL": sys.exit(2)
    elif args.cmd=="package": print(package_project(args.project_dir,args.zip_path,True))

if __name__=="__main__": main()
