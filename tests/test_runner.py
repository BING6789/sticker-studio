from pathlib import Path
from PIL import Image, ImageDraw
import json, shutil, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from router import route_intent
from sticker_tools import resize_and_pad, verify_alpha, split_sticker_sheet, create_cover_asset, create_icon_asset, create_banner_asset, qc_image, qc_project, write_json, package_project

RESULT=[]
def rec(name, ok, detail=""):
    RESULT.append({"test":name,"status":"PASS" if ok else "FAIL","detail":detail})

def make_rgba(path,size=(320,260),color=(180,120,80,255), transparent=True):
    bg=(0,0,0,0) if transparent else (255,255,255,255)
    im=Image.new("RGBA",size,bg); d=ImageDraw.Draw(im); d.ellipse((40,30,size[0]-40,size[1]-30),fill=color); im.save(path,"PNG")

def main():
    tmp=Path(tempfile.mkdtemp(prefix="sticker-skill-test-"))
    try:
        # behavioral regression
        cases=json.loads((ROOT/"tests/regression/cases.json").read_text(encoding="utf-8"))
        for c in cases:
            r=route_intent(c["input"])
            ok=(r["mode"]==c["expected_mode"] and r["generation_allowed"]==c["generation_allowed"])
            if "pixel_safe" in c: ok = ok and r.get("pixel_safe")==c["pixel_safe"]
            if "preserve_all" in c: ok = ok and r.get("preserve_all")==c["preserve_all"]
            rec(c["id"],ok,f"route={r}")
        # image ops
        src=tmp/"src.png"; make_rgba(src)
        out=tmp/"240.png"; resize_and_pad(str(src),str(out),240,240,"transparent",8)
        q=qc_image(str(out),240,240,"PNG","required")
        rec("IMG_RESIZE_240",q["overall"]=="PASS",str(q.get("failures")))
        rec("ALPHA_VERIFY",verify_alpha(str(out),True)["ok"])
        icon=tmp/"icon.png"; create_icon_asset(str(src),str(icon)); rec("ICON_50",qc_image(str(icon),50,50,"PNG","required")["overall"]=="PASS")
        banner=tmp/"banner.png"; create_banner_asset(str(src),str(banner)); rec("BANNER_750x400",qc_image(str(banner),750,400,"PNG","optional")["overall"]=="PASS")
        # uniform sheet split
        sheet=Image.new("RGBA",(800,600),(0,0,0,0)); d=ImageDraw.Draw(sheet)
        for r in range(3):
            for c in range(4):
                x=c*200+40; y=r*200+40; d.rectangle((x,y,x+120,y+120),fill=(80+20*c,100+20*r,160,255))
        sheetp=tmp/"sheet.png"; sheet.save(sheetp,"PNG")
        splitdir=tmp/"split"; res=split_sticker_sheet(str(sheetp),str(splitdir),3,4,240,240,margin=8)
        rec("SPLIT_COUNT",len(res)==12)
        rec("SPLIT_QC",all(qc_image(str(p),240,240,"PNG","required")["overall"]=="PASS" for p in splitdir.glob("*.png")))
        # mock WeChat project end-to-end
        proj=tmp/"demo"; (proj/"stickers").mkdir(parents=True); (proj/"wechat").mkdir(); (proj/"preview").mkdir(); (proj/"project").mkdir()
        for i in range(1,13): shutil.copy(out,proj/"stickers"/f"{i:02d}.png")
        cover=tmp/"cover.png"; create_cover_asset(str(src),str(cover)); shutil.copy(cover,proj/"wechat"/"cover_240x240.png"); shutil.copy(icon,proj/"wechat"/"icon_50x50.png"); shutil.copy(banner,proj/"wechat"/"banner_750x400.png"); shutil.copy(out,proj/"preview"/"overview.png")
        (proj/"project"/"project.json").write_text(json.dumps({"project_id":"demo","name":"demo","platform":"wechat","version":"1.2","status":"qc","sticker_count":12,"master_character":{"reference":"master.png","approved":True,"approved_at":"2026-09-11"},"output_defaults":{"width":240,"height":240,"format":"PNG","background":"transparent"}},indent=2),encoding="utf-8")
        (proj/"project"/"assets.json").write_text(json.dumps({"stickers":[],"icon":{},"banner":{}},indent=2),encoding="utf-8")
        (proj/"project"/"info.txt").write_text("demo",encoding="utf-8")
        # seed qc so required-file check sees it, then overwrite with real report
        (proj/"project"/"qc.json").write_text(json.dumps({"overall":"NOT_RUN","checks":[],"failures":[],"warnings":[]}),encoding="utf-8")
        qproj=qc_project(str(proj),str(ROOT/"platforms/wechat.yaml")); write_json(str(proj/"project/qc.json"),qproj)
        rec("WECHAT_PROJECT_QC",qproj["overall"]=="PASS",str(qproj.get("failures")))
        z=tmp/"demo.zip"; package_project(str(proj),str(z),True); rec("PACKAGE_AFTER_QC",z.exists() and z.stat().st_size>0)
    finally:
        outp=ROOT/"tests/results/latest.json"; outp.write_text(json.dumps({"summary":{"total":len(RESULT),"pass":sum(x["status"]=="PASS" for x in RESULT),"fail":sum(x["status"]=="FAIL" for x in RESULT)},"results":RESULT},ensure_ascii=False,indent=2),encoding="utf-8")
        shutil.rmtree(tmp,ignore_errors=True)
    data=json.loads((ROOT/"tests/results/latest.json").read_text(encoding="utf-8"))
    print(json.dumps(data["summary"],ensure_ascii=False))
    for x in data["results"]:
        if x["status"]=="FAIL": print("FAIL",x)
    return 0 if data["summary"]["fail"]==0 else 1

if __name__=="__main__": raise SystemExit(main())
