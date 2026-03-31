#!/usr/bin/env python3
"""
Fixed humanness scoring pipeline for WeWrite optimization loops and article QA.

Two-layer scoring:
1. Objective checklist (deterministic yes/no checks)
2. Reader-feel judge (currently a stub unless a real judge is wired in)

Composite score is inverted:
- 0 = very human
- 100 = obviously AI-ish
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BANNED_WORDS = [
    "首先",
    "其次",
    "最后",
    "总之",
    "综上所述",
    "总而言之",
    "此外",
    "另外",
    "与此同时",
    "不仅如此",
    "更重要的是",
    "在此基础上",
    "作为一个",
    "让我们",
    "值得注意的是",
    "需要指出的是",
    "不可否认",
    "众所周知",
    "事实上",
    "显而易见",
    "可以说",
    "从某种意义上说",
    "非常重要",
    "至关重要",
    "具有重要意义",
    "发挥着重要作用",
    "意义深远",
    "影响深远",
    "引发了广泛关注",
    "引起了热烈讨论",
    "综合来看",
    "由此可见",
    "不难发现",
    "通过以上分析",
    "正如我们所看到的",
]

REAL_SOURCE_PATTERNS = [
    r"[A-Z][a-z]+\s+[A-Z][a-z]+",
    r"[\u4e00-\u9fff]{2,4}(?:表示|指出|认为|写道|提到|说过|称)",
    r"(?:据|根据|来自)\s*[\u4e00-\u9fffA-Za-z0-9《》“”]+(?:报告|数据|研究|调查|统计)",
    r"20[12]\d(?:年|\b)",
    r"\d+(?:\.\d+)?%",
    r"\d+(?:\.\d+)?\s*(?:亿|万)?\s*(?:美元|元|人民币|人)",
]

BROKEN_SENTENCE_PATTERNS = [
    r"—[^。！？!?]*$",
    r"……|\.{3,}",
    r"不对[，,。]",
    r"算了[，,。]?",
    r"等等[，,。]?",
]

WORD_TEMPERATURE_BUCKETS = {
    "cold": ["认知负荷", "信息不对称", "路径依赖", "商业模式", "生态位", "增量"],
    "warm": ["说白了", "其实", "讲真", "说实话", "坦白讲", "懂的都懂", "怎么说呢"],
    "hot": ["DNA动了", "格局打开", "遥遥领先", "内卷", "炸了", "杀疯了", "吃灰"],
    "wild": ["整挺好", "不靠谱", "瞎折腾", "搁这儿", "糊弄", "扯", "怼"],
}


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    return text.strip()


def check_no_banned_words(text: str) -> tuple[bool, str]:
    found = [word for word in BANNED_WORDS if word in text]
    if found:
        return False, f"命中 {len(found)} 个套话：{', '.join(found[:5])}"
    return True, "未命中常见 AI 套话"


def check_real_sources(text: str) -> tuple[bool, str]:
    count = sum(len(re.findall(pattern, text)) for pattern in REAL_SOURCE_PATTERNS)
    if count >= 3:
        return True, f"检测到 {count} 个真实素材信号"
    return False, f"真实素材信号只有 {count} 个，建议至少 3 个"


def check_broken_sentences(text: str) -> tuple[bool, str]:
    count = 0
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        for pattern in BROKEN_SENTENCE_PATTERNS:
            count += len(re.findall(pattern, line))
        if 1 <= len(line) <= 10 and not line.startswith("#"):
            count += 1
    if count >= 3:
        return True, f"检测到 {count} 处破句/停顿/短句"
    return False, f"破句和短句只有 {count} 处，建议至少 3 处"


def check_sentence_length_variance(text: str) -> tuple[bool, str]:
    sentences = re.split(r"[。！？!?\n]", text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 1]
    if len(sentences) < 5:
        return False, "句子数量太少，暂时无法判断句长波动"

    lengths = [len(sentence) for sentence in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((length - mean) ** 2 for length in lengths) / len(lengths)
    stddev = variance ** 0.5
    if stddev > 15:
        return True, f"句长标准差 {stddev:.1f}，波动自然"
    return False, f"句长标准差 {stddev:.1f}，偏整齐"


def check_paragraph_length_variance(text: str) -> tuple[bool, str]:
    paragraphs = [para.strip() for para in re.split(r"\n\s*\n", text) if para.strip()]
    paragraphs = [para for para in paragraphs if not para.startswith("#")]
    if len(paragraphs) < 3:
        return True, "段落太少，不强制检查"

    consecutive_similar = 0
    for current, nxt in zip(paragraphs, paragraphs[1:]):
        if abs(len(current) - len(nxt)) <= 20:
            consecutive_similar += 1

    if consecutive_similar <= 1:
        return True, f"相近长度连续段落 {consecutive_similar} 组"
    return False, f"相近长度连续段落 {consecutive_similar} 组，节奏偏平"


def check_word_temperature_mix(text: str) -> tuple[bool, str]:
    found = sum(1 for words in WORD_TEMPERATURE_BUCKETS.values() if any(word in text for word in words))
    if found >= 3:
        return True, f"命中 {found}/4 组词汇温度"
    return False, f"词汇温度只有 {found}/4 组，建议至少 3 组"


def run_layer1(text: str) -> dict:
    checks = [
        ("no_banned_words", check_no_banned_words),
        ("real_sources", check_real_sources),
        ("broken_sentences", check_broken_sentences),
        ("sentence_length_variance", check_sentence_length_variance),
        ("paragraph_length_variance", check_paragraph_length_variance),
        ("word_temperature_mix", check_word_temperature_mix),
    ]

    results: dict[str, dict] = {}
    passed = 0
    failed_checks: list[str] = []

    for name, func in checks:
        ok, detail = func(text)
        results[name] = {"passed": ok, "detail": detail}
        if ok:
            passed += 1
        else:
            failed_checks.append(name)

    results["_summary"] = {
        "passed": passed,
        "total": len(checks),
        "pass_rate": round(passed / len(checks), 4),
        "failed_checks": failed_checks,
    }
    return results


JUDGE_PROMPT = """你是一个经验丰富的公众号编辑读者。你对 AI 生成的内容非常敏感。

现在请你阅读下面这篇文章，然后回答一个问题：

这篇文章读起来像人写的吗？

评分标准（1-10）：
- 1-3：明显是 AI 写的，语言规整得过头，没有人的犹豫和棱角。
- 4-5：有明显 AI 痕迹，信息没问题，但缺乏个人色彩和情绪起伏。
- 6-7：大部分像人写的，偶尔有几句过于顺滑或工整。
- 8-9：很像人写的，有个人判断、停顿、情绪波动和不完美感。
- 10：完全像真人编辑写的，如果不提醒，不会怀疑 AI 参与。

请只输出一个 JSON：{"score": 数字, "reason": "一句话理由"}

文章内容：
{article}
"""


def run_layer2_stub(_: str) -> dict:
    return {
        "score": 5.0,
        "reason": "LLM 判官尚未接入，当前使用默认中性分",
        "is_stub": True,
        "judge_mode": "stub",
    }


def compute_composite(layer1: dict, layer2: dict) -> float:
    layer1_pass_rate = layer1["_summary"]["pass_rate"]
    layer2_score = float(layer2["score"]) / 10.0
    humanness = layer1_pass_rate * 0.6 + layer2_score * 0.4
    return round((1 - humanness) * 100, 2)


def score_article(text: str) -> dict:
    clean = strip_markdown(text)
    layer1 = run_layer1(clean)
    layer2 = run_layer2_stub(clean)
    composite = compute_composite(layer1, layer2)
    result = {
        "composite_score": composite,
        "layer1": layer1,
        "layer2": layer2,
        "char_count": len(clean),
        "summary": {
            "layer1_passed": layer1["_summary"]["passed"],
            "layer1_total": layer1["_summary"]["total"],
            "failed_checks": layer1["_summary"]["failed_checks"],
            "layer2_is_stub": bool(layer2.get("is_stub")),
        },
    }
    return result


def print_verbose(result: dict) -> None:
    layer1 = result["layer1"]
    layer2 = result["layer2"]
    print("=" * 60)
    print(f"HUMANNESS SCORE: {result['composite_score']:.1f}/100 (越低越像人)")
    print("=" * 60)
    print(f"\nLayer 1 - Objective Checklist ({layer1['_summary']['passed']}/{layer1['_summary']['total']})")
    for name, data in layer1.items():
        if name.startswith("_"):
            continue
        status = "PASS" if data["passed"] else "FAIL"
        print(f"  {status} {name}: {data['detail']}")
    print(f"\nLayer 2 - Reader Feel: {layer2['score']}/10")
    print(f"  {layer2['reason']}")
    print(f"\nComposite: {result['composite_score']:.1f} (0=更像人, 100=更像 AI)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score article humanness")
    parser.add_argument("input", help="Markdown article file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detailed output")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    result = score_article(text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.verbose:
        print_verbose(result)
        return

    print(f"{result['composite_score']:.1f}")


if __name__ == "__main__":
    main()
