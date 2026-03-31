# Humanizer: AI 写作去痕

去除文本中的 AI 生成痕迹，使文章听起来更自然、更像人类书写。

## 概述

Humanizer 是一个独立的文本处理模块，与写作风格系统并行工作：

| 特性 | 写作风格 (Style) | Humanizer |
|------|------------------|-----------|
| **作用** | 控制"怎么写" | 去除"AI 味" |
| **默认状态** | 启用 | 关闭（可选） |
| **独立性** | 可单独使用 | 可单独使用 |
| **组合使用** | - | 可与风格组合 |

## 处理能力

Humanizer 基于维基百科的"AI 写作特征"指南，检测并处理 **24 种 AI 痕迹模式**：

### 内容模式
- 过度强调意义、遗产和更广泛的趋势
- 过度强调知名度和媒体报道
- 以 -ing 结尾的肤浅分析
- 宣传和广告式语言
- 模糊归因和含糊措辞
- 公式化的"挑战与未来展望"部分

### 语言和语法模式
- 过度使用的"AI 词汇"（此外、至关重要、深入探讨、彰显等）
- 避免使用"是"（系动词回避）
- 否定式排比（不仅…而且…）
- 三段式法则过度使用
- 刻意换词（同义词循环）
- 虚假范围

### 风格模式
- 破折号过度使用
- 粗体过度使用
- 内联标题垂直列表
- 表情符号装饰

### 填充词和回避
- 填充短语（为了实现这一目标、在这个时间点等）
- 过度限定
- 通用积极结论

### 交流痕迹
- 协作交流痕迹（希望这对您有帮助、当然！等）
- 知识截止日期免责声明
- 谄媚/卑躬屈膝的语气

## CLI 使用

### 独立命令

```bash
# 基本用法
md2wechat humanize article.md

# 指定处理强度
md2wechat humanize article.md --intensity gentle
md2wechat humanize article.md --intensity aggressive

# 显示修改对比和质量评分
md2wechat humanize article.md --show-changes

# 输出到文件
md2wechat humanize article.md -o output.md
```

### 与写作风格组合

```bash
# 写作 + 去痕
md2wechat write --style dan-koe --humanize

# 指定去痕强度
md2wechat write --style dan-koe --humanize --humanize-intensity aggressive
```

## 处理强度

| 强度 | 描述 | 适用场景 |
|------|------|---------|
| `gentle` | 温和处理，只修改明显的问题 | 已经比较自然的文本 |
| `medium` | 平衡处理（默认） | 大多数场景 |
| `aggressive` | 激进处理，深度去除 AI 痕迹 | AI 味很重的文本 |

## 风格优先原则

当 Humanizer 与写作风格组合使用时，遵循**风格优先原则**：

```
用户: md2wechat write --style dan-koe --humanize

处理流程:
1. 用 Dan Koe 风格生成文章
2. 应用 Humanizer 去痕
3. 保留 Dan Koe 风格的核心特征（如破折号）
4. 只去除无意的 AI 痕迹
```

## 输出格式

Humanizer 处理后返回：

```json
{
  "success": true,
  "content": "处理后的文本...",
  "report": "修改说明...",
  "changes": [
    {
      "type": "filler_phrase",
      "original": "为了实现这一目标",
      "revised": "为了实现这一点",
      "reason": "删除填充短语"
    }
  ],
  "score": {
    "total": 42,
    "directness": 8,
    "rhythm": 9,
    "trust": 8,
    "authenticity": 9,
    "conciseness": 8,
    "rating": "良好 - 仍有改进空间"
  }
}
```

## 质量评分

Humanizer 使用 5 个维度评分（总分 50）：

| 维度 | 说明 | 评分标准 |
|------|------|---------|
| **直接性** | 直接陈述事实还是绕圈 | 10 分：直截了当；1 分：充满铺垫 |
| **节奏** | 句子长度是否变化 | 10 分：长短交错；1 分：机械重复 |
| **信任度** | 是否尊重读者智慧 | 10 分：简洁明了；1 分：过度解释 |
| **真实性** | 听起来像真人说话吗 | 10 分：自然流畅；1 分：机械生硬 |
| **精炼度** | 还有可删减的内容吗 | 10 分：无冗余；1 分：大量废话 |

**评级标准**：
- **45-50 分**：优秀，已去除 AI 痕迹
- **35-44 分**：良好，仍有改进空间
- **低于 35 分**：需要重新修订

## Claude Code 自然语言使用

```
"去除这篇文章的 AI 痕迹：article.md"
"把这篇文章重写得更像人写的"
"用温和强度处理这篇文章"
"用 Dan Koe 风格写一篇文章，并去除 AI 痕迹"
```

## 常见问题

### Q: Humanizer 会改变文章意思吗？

A: 不会。Humanizer 只修改表达方式，不改变核心信息。

### Q: 与写作风格冲突怎么办？

A: 风格优先。Humanizer 会识别并保留风格刻意为之的特征（如 Dan Koe 的破折号）。

### Q: 可以只处理特定类型的痕迹吗？

A: 可以。使用 `--focus` 参数指定聚焦模式（当前仅限 API 调用）。

### Q: 处理失败怎么办？

A: Humanizer 失败时会返回原始文章，不会丢失内容。
