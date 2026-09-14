# Intent Routing Rules — V1.1

Route before acting. Exactly one primary mode should control each user request.

## Priority cues
- “先讨论/先看看方案/先别生成” → discussion only; route to CREATE/COPY/STORYBOARD; generation forbidden.
- “正式生成/生成第N张/画一个” → GENERATE.
- “改动作/改表情/加删物体/换风格/改变角色行为” → EDIT.
- “改尺寸/透明PNG/转格式/居中/裁切/压缩” → PROCESS + Pixel Safe.
- “拆分/切成单张/从宫格提取” → SPLIT + Pixel Safe.
- “打包/ZIP/整理文件名” → PACKAGE.
- “检查/核对/有没有问题” → QC only.
- “头像/图标/横幅/平台上传图” → PLATFORM_ASSET unless the request is only technical resizing, in which case PROCESS is acceptable.

## Tool route
- PROCESS → `tools/cli.py inspect|resize|verify-alpha`
- SPLIT → `tools/cli.py split`
- QC → `tools/cli.py qc-image|qc-project`
- PLATFORM_ASSET → `tools/cli.py icon|banner` when an approved source already satisfies semantic requirements; otherwise semantic editing/generation requires explicit user intent.
- PACKAGE → `tools/cli.py package`, only after QC PASS.

## Minimum-change resolver
When ambiguity exists, choose the interpretation that changes the fewest pixels/fields while satisfying the request. Never infer permission to redesign.
