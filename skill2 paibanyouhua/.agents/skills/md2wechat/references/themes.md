# 微信公众号主题风格指南

> 本文档用于提供视觉风格示例和提示词参考。
>
> 不要把这里的主题数量、名称清单或参数表当成运行时真相源。对 Agent 和自动化脚本，始终先执行：
>
> ```bash
> md2wechat themes list --json
> md2wechat themes show <name> --json
> ```
>
> 当前项目的能力发现主路径见仓库文档 `docs/DISCOVERY.md`。

## 主题概览

本项目支持多种主题风格，涵盖 AI 生成模式和 API 模式。下面内容主要用于帮助理解视觉方向，不负责声明运行时完整能力面。

### AI 模式主题（推荐）

| 主题 | 命令参数 | 风格描述 | 适合内容 |
|------|----------|----------|----------|
| 🟠 **秋日暖光** | `--theme autumn-warm` | 温暖治愈，橙色调，文艺美学 | 情感故事、生活随笔 |
| 🟢 **春日清新** | `--theme spring-fresh` | 清新自然，绿色调，生机盎然 | 旅行日记、自然主题 |
| 🔵 **深海静谧** | `--theme ocean-calm` | 深邃冷静，蓝色调，理性专业 | 技术文章、商业分析 |
| ⚪ **自定义** | `--theme custom` | 使用自定义提示词 | 特殊需求 |

### API 模式主题

以下 API 主题分组和示例主要用于帮助理解命名风格与设计语言。

#### 主题预览
📚 **完整主题预览**: [https://md2wechat.app/theme-gallery](https://md2wechat.app/theme-gallery)

#### 基础主题（6 个）- v1.0 内置

| 主题 | 命令参数 | 风格描述 | 适合内容 |
|------|----------|----------|----------|
| **default** | `--mode api` 或默认 | 微信经典，温暖舒适 | 通用内容 |
| **bytedance** | `--theme bytedance` | 科技现代，简洁利落 | 科技资讯 |
| **apple** | `--theme apple` | 视觉渐变，精致优雅 | 产品评测 |
| **sports** | `--theme sports` | 活力动感，充满能量 | 体育健康 |
| **chinese** | `--theme chinese` | 古典雅致，书卷气息 | 文化文章 |
| **cyber** | `--theme cyber` | 未来科技，霓虹光影 | 前沿科技 |

#### 主题系列示例

**Minimal 系列** - 干净克制，纯色文字无装饰

| 颜色 | 主题 | 命令 | 风格 |
|------|------|------|------|
| 🟡 | minimal-gold | `--theme minimal-gold` | 金色系 |
| 🟢 | minimal-green | `--theme minimal-green` | 绿色系 |
| 🔵 | minimal-blue | `--theme minimal-blue` | 蓝色系 |
| 🟠 | minimal-orange | `--theme minimal-orange` | 橙色系 |
| 🔴 | minimal-red | `--theme minimal-red` | 红色系 |
| 🎓 | minimal-navy | `--theme minimal-navy` | 藏青色系 |
| ⚫ | minimal-gray | `--theme minimal-gray` | 灰色系 |
| 🌤 | minimal-sky | `--theme minimal-sky` | 天蓝色系 |

**Focus 系列** - 居中对称，标题上下双横线

| 颜色 | 主题 | 命令 | 风格 |
|------|------|------|------|
| 🟡 | focus-gold | `--theme focus-gold` | 金色系 |
| 🟢 | focus-green | `--theme focus-green` | 绿色系 |
| 🔵 | focus-blue | `--theme focus-blue` | 蓝色系 |
| 🟠 | focus-orange | `--theme focus-orange` | 橙色系 |
| 🔴 | focus-red | `--theme focus-red` | 红色系 |
| 🎓 | focus-navy | `--theme focus-navy` | 藏青色系 |
| ⚫ | focus-gray | `--theme focus-gray` | 灰色系 |
| 🌤 | focus-sky | `--theme focus-sky` | 天蓝色系 |

**Elegant 系列** - 层次丰富，左边框递减 + 渐变背景

| 颜色 | 主题 | 命令 | 风格 |
|------|------|------|------|
| 🟡 | elegant-gold | `--theme elegant-gold` | 金色系 |
| 🟢 | elegant-green | `--theme elegant-green` | 绿色系 |
| 🔵 | elegant-blue | `--theme elegant-blue` | 蓝色系 |
| 🟠 | elegant-orange | `--theme elegant-orange` | 橙色系 |
| 🔴 | elegant-red | `--theme elegant-red` | 红色系 |
| 🎓 | elegant-navy | `--theme elegant-navy` | 藏青色系 |
| ⚫ | elegant-gray | `--theme elegant-gray` | 灰色系 |
| 🌤 | elegant-sky | `--theme elegant-sky` | 天蓝色系 |

**Bold 系列** - 视觉冲击，标题满底色 + 圆角投影

| 颜色 | 主题 | 命令 | 风格 |
|------|------|------|------|
| 🟡 | bold-gold | `--theme bold-gold` | 金色系 |
| 🟢 | bold-green | `--theme bold-green` | 绿色系 |
| 🔵 | bold-blue | `--theme bold-blue` | 蓝色系 |
| 🟠 | bold-orange | `--theme bold-orange` | 橙色系 |
| 🔴 | bold-red | `--theme bold-red` | 红色系 |
| 🎓 | bold-navy | `--theme bold-navy` | 藏青色系 |
| ⚫ | bold-gray | `--theme bold-gray` | 灰色系 |
| 🌤 | bold-sky | `--theme bold-sky` | 天蓝色系 |

#### 主题命名规则

```
<系列>-<颜色>

系列:
  minimal  - 干净克制，纯色文字
  focus    - 居中对称，双横线
  elegant  - 左边框递减，渐变背景
  bold     - 标题满底色，圆角投影

颜色: gold, green, blue, orange, red, navy, gray, sky
```

#### 使用方法
```bash
# 基础主题（默认）
md2wechat convert article.md

# v2.0 新主题
md2wechat convert article.md --theme elegant-gold --preview
md2wechat convert article.md --theme minimal-blue --draft --cover cover.jpg
```

> 💡 **提示**: 某些 API 主题或主题能力可能依赖特定 API 域名与服务能力，先检查当前配置与 `themes list --json` 的实际输出。

### 背景类型选择 🆕

除了主题，你还可以自定义背景样式：

| 背景类型 | 命令 | 效果 | 适合场景 |
|----------|------|------|----------|
| `default` | `--background-type default` | 默认背景（纯色或渐变） | 通用内容 |
| `grid` | `--background-type grid` | 网格纹理背景 | 技术文档、笔记类 |
| `none` | `--background-type none` | 无背景（透明） | 嵌入式内容 |

**使用示例：**

```bash
# 使用网格背景
md2wechat convert article.md --theme elegant-gold --background-type grid

# 使用无背景
md2wechat convert article.md --theme minimal-blue --background-type none

# 组合使用
md2wechat convert article.md --theme focus-green --background-type grid --draft --cover cover.jpg
```

默认值是 `none`。只有在需要显式背景时才传 `--background-type default` 或 `--background-type grid`。

**配置文件设置：**

```yaml
# ~/.config/md2wechat/config.yaml
api:
  background_type: none  # default/grid/none
```

---

## AI 主题详情

### 主题 1: autumn-warm（秋日暖光）

#### 整体感觉
温暖治愈、橙色调、文艺美学，适合情感表达和生活方式内容。

#### 配色方案
```css
主背景: #faf9f5 (暖白)
文字色: #4a413d (深褐灰)
主强调色: #d97758 (秋日暖橙)
副强调色: #c06b4d (橙红)
引用背景: #fef4e7 (淡橙)
```

#### 设计特点
- 卡片式布局，米白方格纹理
- 圆角 18px，柔和阴影
- 标题使用 ▶ 符号 + 暖橙文字
- 引用块带内阴影和暖橙左边框

#### 提示词关键词
```
温暖治愈、秋日暖光、橙色调、文艺美学、卡片布局、柔和光效
```

#### 生成指令示例
```
使用秋日暖光主题生成微信公众号 HTML：
- 暖白背景 #faf9f5，深褐灰文字 #4a413d
- 主强调色 #d97758（秋日暖橙）
- 卡片式布局，圆角 18px
- 标题使用 ▶ 符号
- 所有 CSS 必须内联（style 属性）
- 图片使用占位符 <!-- IMG:index -->
```

---

### 主题 2: spring-fresh（春日清新）

#### 整体感觉
清新自然、绿色调、生机盎然，适合户外和自然主题。

#### 配色方案
```css
主背景: #f5f8f5 (淡绿)
文字色: #3d4a3d (深绿灰)
主强调色: #6b9b7a (春日嫩绿)
副强调色: #4a8058 (草地翠绿)
引用背景: #e8f0e8 (淡绿)
```

#### 设计特点
- 清新点状纹理背景
- 圆角 16px，清新阴影
- 标题使用 ❀ 符号 + 绿色文字
- 引用块带清新绿色调

#### 提示词关键词
```
清新自然、春日花园、绿色调、生机盎然、点状纹理、清新阴影
```

#### 生成指令示例
```
使用春日清新主题生成微信公众号 HTML：
- 淡绿背景 #f5f8f5，深绿灰文字 #3d4a3d
- 主强调色 #6b9b7a（春日嫩绿）
- 清新点状纹理背景
- 标题使用 ❀ 符号
- 所有 CSS 必须内联
- 图片使用占位符 <!-- IMG:index -->
```

---

### 主题 3: ocean-calm（深海静谧）

#### 整体感觉
深邃冷静、蓝色调、理性专业，适合技术和商业内容。

#### 配色方案
```css
主背景: #f0f4f8 (淡蓝)
文字色: #3a4150 (深蓝灰)
主强调色: #4a7c9b (深海蔚蓝)
副强调色: #3d6a8a (静谧石蓝)
引用背景: #e8f0f8 (淡蓝)
```

#### 设计特点
- 淡蓝网格纹理背景
- 圆角 14px，深邃阴影
- 标题使用 ◆ 符号 + 蓝色文字
- 引用块带静谧蓝色调

#### 提示词关键词
```
深海静谧、理性专业、蓝色调、网格纹理、深邃蓝调、清晰层次
```

#### 生成指令示例
```
使用深海静谧主题生成微信公众号 HTML：
- 淡蓝背景 #f0f4f8，深蓝灰文字 #3a4150
- 主强调色 #4a7c9b（深海蔚蓝）
- 淡蓝网格纹理背景
- 标题使用 ◆ 符号
- 所有 CSS 必须内联
- 图片使用占位符 <!-- IMG:index -->
```

---

### 主题 4: custom（自定义）

#### 用途
允许用户提供自定义提示词，实现完全个性化的排版风格。

#### 使用方法
```bash
md2wechat convert article.md --mode ai --custom-prompt "你的自定义提示词"
```

#### 自定义提示词模板
```
请将以下 Markdown 转换为微信公众号 HTML：

配色要求：
- 主色：#your_color
- 副色：#your_color
- 背景：#your_color

字体要求：
- 字号：16px
- 行高：1.8
- 字体：系统默认无衬线

技术要求：
1. 所有 CSS 必须内联（style 属性）
2. 使用安全的 HTML 标签
3. 图片使用占位符 <!-- IMG:index -->
4. 不使用外部样式表

请转换以下 Markdown内容：
```

---

## API 模式主题

### 主题: default（默认）

#### 说明
调用 [md2wechat.cn](https://md2wechat.cn) API 进行快速转换。

#### 特点
- 响应速度快（秒级）
- 样式稳定规范
- 无需 AI 调用

#### 使用方法
```bash
# 默认就是 API 模式
md2wechat convert article.md

# 或显式指定
md2wechat convert article.md --mode api
```

---

## 通用技术规范（所有 AI 主题）

### 容器结构（关键）
```html
<!-- 必须在 body 后立即创建主容器 -->
<div style="background-color: #xxx; padding: 40px 10px; letter-spacing: 0.5px;">
  <!-- 所有内容放在这里 -->
</div>
```

### 卡片结构
```html
<section style="max-width: 800px; padding: 25px; background: #fff; border-radius: 16px;">
  <!-- 内容 -->
</section>
```

### 安全 HTML 标签
```html
section, p, span, strong, em, u, a, h1-h6, ul, ol, li,
blockquote, pre, code, table, thead, tbody, tr, th, td,
img, br, hr
```

### 图片占位符格式
```html
<!-- IMG:0 -->
<!-- IMG:1 -->
<!-- IMG:2 -->
```

---

## 主题选择建议

| 内容类型 | 推荐主题 | 理由 |
|----------|----------|------|
| 情感故事、生活随笔 | autumn-warm | 温暖色调营造情感氛围 |
| 旅行日记、自然主题 | spring-fresh | 清新绿色契合自然主题 |
| 技术文章、商业分析 | ocean-calm | 专业蓝色调传达可信感 |
| 快速发布 | API 模式 | 秒级响应，稳定可靠 |
| 品牌定制内容 | custom | 完全自定义风格 |

---

## 在 Claude Code 中使用

### 方法 1: 通过 md2wechat 命令
```bash
# 在 Claude Code 中直接调用
md2wechat convert article.md --mode ai --theme autumn-warm --preview
```

### 方法 2: 通过 Skill
在 Claude Code 中直接说：
```
请用秋日暖光主题将 article.md 转换为微信公众号格式
```

---

## 主题文件位置

主题配置文件位于项目 `themes/` 目录：

**AI 主题：**
- `themes/autumn-warm.yaml` - 秋日暖光
- `themes/spring-fresh.yaml` - 春日清新
- `themes/ocean-calm.yaml` - 深海静谧
- `themes/custom.yaml` - 自定义

**API 主题：**

**v1.0 基础主题（6 个）：**
- `themes/default.yaml` - 默认主题
- `themes/bytedance.yaml` - 字节跳动风格
- `themes/apple.yaml` - Apple 极简风格
- `themes/sports.yaml` - 运动活力风格
- `themes/chinese.yaml` - 中国传统文化风格
- `themes/cyber.yaml` - 赛博朋克风格

**v2.0 新增主题（32 个）：**
- `themes/api.yaml` - 完整主题列表
- `themes/elegant-gold.yaml` - Elegant 金色示例
- `themes/minimal-blue.yaml` - Minimal 蓝色示例
- `themes/focus-green.yaml` - Focus 绿色示例
- `themes/bold-red.yaml` - Bold 红色示例

每个主题文件包含完整的 AI 提示词模板，确保生成效果一致。

---

## 完整主题切换示例

### 秋日暖光（情感故事）
```markdown
# 那些年，我们一起追过的梦

还记得青春年少时...

![怀旧照片](./photos/old-days.jpg)
```

```bash
md2wechat convert story.md --mode ai --theme autumn-warm --preview
```

### 春日清新（旅行日记）
```markdown
# 春日游园记

三月的公园，花开正盛...

![公园美景](./photos/spring-park.jpg)
```

```bash
md2wechat travel.md --mode ai --theme spring-fresh --preview
```

### 深海静谧（技术文章）
```markdown
# 微服务架构最佳实践

在现代应用开发中...

![架构图](./diagrams/architecture.png)
```

```bash
md2wechat tech-post.md --mode ai --theme ocean-calm --preview
```
