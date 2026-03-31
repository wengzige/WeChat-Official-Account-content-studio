# gzhskill

这个目录现在是一套可复用的公众号发稿工作流。

## 目录约定

- `.\.agents` / `.\.config` / `.\.local`：项目级 skill、配置和可执行文件
- `.\scripts`：通用脚本
- `.\templates`：新建文章时使用的模板
- `.\<文章标题>`：每一篇文章一个独立文件夹，文件夹名默认使用文章标题

## 推荐工作流

### 1. 新建文章目录

```powershell
cd E:\vscode\gzhskill
.\scripts\new-article.ps1 -Title "你的文章标题" -Author "阿绎 AYi" -SourceUrl "https://x.com/..."
```

脚本会自动创建：

- `article.md`
- `article-body.template.html`
- `draft-metadata.json`
- `assets\`
- `generated\`
- `generated\image-prompts.md`

如果标题里包含 Windows 不允许的字符，脚本会自动替换成 `-`，避免建目录失败。

### 2. 先跑一遍项目体检

```powershell
cd E:\vscode\gzhskill
.\scripts\project-doctor.ps1
.\scripts\project-doctor.ps1 -Fix
```

体检脚本会统一检查：

- 文章目录必需文件是否齐全
- 是否缺少 `generated\image-prompts.md`
- 是否还在使用旧占位符 `{{BODY_IMAGE_URL}}`
- 正文 HTML 里是否用了高风险的 `ul` / `ol` / `li`
- 是否还留着像 `article_work` 这类临时目录别名

加 `-Fix` 时，会自动补齐能安全自动修的内容。

### 3. 发布到公众号草稿箱

```powershell
cd E:\vscode\gzhskill
.\scripts\publish-article.ps1 -ArticleDir ".\你的文章标题"
```

默认约定：只要文章内容、配图和元数据已经准备完成，且你没有明确说“先别发”或“只生成不发布”，就默认继续推送到公众号草稿箱。

发布脚本现在会先做预检，并把结果写到该文章目录下的 `generated\preflight-report.json`。

如果正文里还有原生 `ul` / `ol` / `li`，发布会默认拦截；只有你明确确认这个列表在微信预览里没问题时，才允许使用：

```powershell
.\scripts\publish-article.ps1 -ArticleDir ".\你的文章标题" -AllowNativeLists
```

## 单篇文章目录说明

- `article.md`：原文、整理稿或我改写后的正文
- `article-body.template.html`：最终发到公众号的 HTML 模板
- `draft-metadata.json`：标题、作者、摘要、原文链接、封面路径、评论开关
- `assets\`：封面图和正文配图
- `generated\`：发布输出、提示词、预检报告等生成文件

## 图片占位符

在 `article-body.template.html` 里可以直接写本地图片占位符：

```html
{{IMAGE:assets/body-visual.png}}
```

发布脚本会自动：

1. 上传本地图片到微信素材库
2. 用微信图片地址替换占位符
3. 创建公众号草稿

兼容旧占位符：如果模板里还保留 `{{BODY_IMAGE_URL}}`，体检脚本可以帮你迁移到新的 `{{IMAGE:assets/body-visual.png}}` 形式，发布脚本也仍然兼容。

## 图片与提示词规则

如果本次工作流里包含“直接生图”，默认除了把图片落到 `assets\` 目录，也要把对应提示词一并保存到文章目录下的 `generated\image-prompts.md`，方便后续换图重生。

提示词要求：

- 必须详细，不能只写抽象风格词。
- 必须尽量写进文章里的核心数据、时间、人物、研究、结构和结论。
- 同时提供封面图提示词和正文图提示词。
- 图片主文案默认优先使用中文，不要偷换成英文占位。
- 图片里的中文必须清晰、可读、无乱码、无错字、无残缺笔画。
- 如果模型当前批次生成的中文不稳定，不能直接交付；要么继续重生直到中文正常，要么改为后期本地排字后再发布。
- 除非你明确同意，否则不能用“只放英文”“只放数字”来规避中文乱码问题。

## 正文排版兼容规则

- 在公众号正文的关键结构区块里，默认不要使用 `ul` / `ol` / `li` 来承载核心信息。
- 微信客户端对列表圆点和缩进的渲染不稳定，容易出现圆点错位、单独悬浮、段落不对齐等问题。
- 遇到“模块说明”“三点拆解”“步骤解释”“方法对比”这类内容，优先使用连续 `p` 标签，或使用带底色、边框、圆角的 `div` 卡片来排版。
- 只有在普通文本列表且已经实际预览验证正常时，才允许继续使用原生列表标签。