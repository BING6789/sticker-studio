from __future__ import annotations


def route_intent(text: str) -> dict:
    t = text.strip().lower()
    preserve_all = any(k in t for k in ["其他不变", "不要其他变化", "只改", "只去掉", "仅修改", "everything else unchanged", "only change"])
    discussion = any(k in t for k in ["先讨论", "先别生成", "先看看方案", "先沟通", "不要生成"])
    if discussion:
        if any(k in t for k in ["文案", "句子", "说法"]):
            return {"mode":"COPY","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
        if any(k in t for k in ["动作", "表演", "分镜", "怎么演"]):
            return {"mode":"STORYBOARD","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
        return {"mode":"CREATE","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
    # QC intent outranks operation keywords when user asks to inspect/check the result.
    if any(k in t for k in ["检查", "核对", "有没有问题", "qc"]):
        return {"mode":"QC","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
    if any(k in t for k in ["拆分", "切成单张", "切割", "从宫格提取", "提取单张"]):
        return {"mode":"SPLIT","generation_allowed":False,"pixel_safe":True,"preserve_all":preserve_all}
    if any(k in t for k in ["打包", "zip", "整理文件名"]):
        return {"mode":"PACKAGE","generation_allowed":False,"pixel_safe":True,"preserve_all":preserve_all}
    # Explicit platform asset without purely technical dimensions.
    if any(k in t for k in ["头像", "图标", "横幅", "上传图"]) and not any(k in t for k in ["500×500", "500*500", "200×200", "200*200", "750×400", "750*400", "改尺寸", "透明png", "透明格式", "转格式", "居中", "裁切", "压缩"]):
        return {"mode":"PLATFORM_ASSET","generation_allowed":False,"pixel_safe":True,"preserve_all":preserve_all}
    # Purely technical transformations must stay Pixel Safe.
    if any(k in t for k in ["500×500", "500*500", "200×200", "200*200", "750×400", "750*400", "改尺寸", "透明png", "透明格式", "转格式", "居中", "裁切", "压缩", "是不是真透明"]):
        return {"mode":"PROCESS","generation_allowed":False,"pixel_safe":True,"preserve_all":preserve_all}
    # Semantic edits to an existing image.
    if any(k in t for k in ["改动作", "改表情", "加一个", "删掉", "去掉文字", "字体小一点", "杯子文字", "换风格", "呲牙", "只修这一张"]):
        return {"mode":"EDIT","generation_allowed":True,"pixel_safe":False,"preserve_all":preserve_all}
    if any(k in t for k in ["正式生成", "生成第", "画一个", "生成图片", "重新生成"]):
        return {"mode":"GENERATE","generation_allowed":True,"pixel_safe":False,"preserve_all":preserve_all}
    if any(k in t for k in ["文案", "12个", "24个"]):
        return {"mode":"COPY","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
    if any(k in t for k in ["怎么表演", "分镜", "动作设计"]):
        return {"mode":"STORYBOARD","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
    return {"mode":"CREATE","generation_allowed":False,"pixel_safe":False,"preserve_all":preserve_all}
