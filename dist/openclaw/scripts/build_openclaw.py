#!/usr/bin/env python3
"""
Build OpenClaw-compatible SKILL.md from Claude Code source.

Usage:
    python3 scripts/build_openclaw.py              # output to dist/openclaw/
    python3 scripts/build_openclaw.py -o /tmp/oc   # custom output dir
"""

import argparse
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories to copy alongside SKILL.md
COPY_DIRS = ["references", "scripts", "toolkit", "personas"]

# Files to copy alongside SKILL.md
COPY_FILES = [
    "requirements.txt",
    "config.example.yaml",
    "style.example.yaml",
    "writing-config.example.yaml",
    "VERSION",
]

# Frontmatter keys to strip (OpenClaw ignores allowed-tools)
STRIP_FRONTMATTER_KEYS = {"allowed-tools"}


def transform_frontmatter(frontmatter: str) -> str:
    """Remove Claude Code-specific frontmatter keys."""
    lines = frontmatter.split("\n")
    result = []
    skip_block = False
    for line in lines:
        # Check if this line starts a key we want to strip
        stripped = line.lstrip()
        if any(stripped.startswith(f"{key}:") for key in STRIP_FRONTMATTER_KEYS):
            skip_block = True
            continue
        # If we're in a skip block, skip indented continuation lines (list items)
        if skip_block:
            if stripped.startswith("- ") or stripped == "":
                continue
            skip_block = False
        result.append(line)
    return "\n".join(result)


def transform_body(body: str) -> str:
    """Apply all body transformations."""
    # 1. {skill_dir} → {baseDir}
    body = body.replace("{skill_dir}", "{baseDir}")

    # 2. WebSearch references in instructions (preserve in bash code blocks)
    #    "WebSearch:" as instruction prefix → "web_search:"
    #    "WebSearch " in prose → "web_search "
    body = re.sub(r'(?m)^WebSearch:', 'web_search:', body)
    body = re.sub(r'(?<![`/])WebSearch(?=[ "：，）])', 'web_search', body)
    #    WebSearch in parentheses/tables: "（WebSearch）"
    body = re.sub(r'(?<=（)WebSearch(?=）)', 'web_search', body)

    # 3. Path convention note
    body = body.replace(
        "本文档中 `{baseDir}` 指本 SKILL.md 所在的目录（即 WeWrite 的根目录）",
        "本文档中 `{baseDir}` 指本 SKILL.md 所在的目录（即 WeWrite 的根目录）",
    )

    return body


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split YAML frontmatter from body. Returns (frontmatter, body)."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    # +4 to skip the closing "---\n"
    fm = text[3:end].strip()
    body = text[end + 4:]  # skip "\n---"
    return fm, body


def build(output_dir: Path):
    skill_src = REPO_ROOT / "SKILL.md"
    text = skill_src.read_text(encoding="utf-8")

    fm, body = split_frontmatter(text)
    fm = transform_frontmatter(fm)
    body = transform_body(body)

    out_skill = output_dir / "SKILL.md"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_skill.write_text(f"---\n{fm}\n---{body}", encoding="utf-8")
    print(f"  SKILL.md → {out_skill}")

    # Copy supporting directories
    for d in COPY_DIRS:
        src = REPO_ROOT / d
        dst = output_dir / d
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", "*.pyo",
            ))
            print(f"  {d}/ → {dst}")

    # Copy supporting files
    for f in COPY_FILES:
        src = REPO_ROOT / f
        if src.is_file():
            shutil.copy2(src, output_dir / f)
            print(f"  {f} → {output_dir / f}")

    print(f"\nDone. OpenClaw skill at: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Build OpenClaw-compatible WeWrite skill")
    parser.add_argument(
        "-o", "--output",
        default=str(REPO_ROOT / "dist" / "openclaw"),
        help="Output directory (default: dist/openclaw/)",
    )
    args = parser.parse_args()
    build(Path(args.output))


if __name__ == "__main__":
    main()
