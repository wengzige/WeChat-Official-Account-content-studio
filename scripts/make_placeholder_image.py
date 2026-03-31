#!/usr/bin/env python3
"""
Generate a simple local placeholder image for article layout slots.

Examples:
    python scripts/make_placeholder_image.py --output output/demo/cover-wide.jpg --label "COVER 2.35:1" --size cover
    python scripts/make_placeholder_image.py --output output/demo/cover-square.jpg --label "COVER 1:1" --size square
    python scripts/make_placeholder_image.py --output output/demo/img-01.jpg --label "IMG 01" --size article
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


SIZE_PRESETS = {
    "cover": (900, 383),
    "article": (1280, 720),
    "square": (1024, 1024),
}


def _load_font(size: int):
    candidates = [
        "arial.ttf",
        "segoeui.ttf",
        "calibri.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int):
    for size in range(84, 17, -4):
        font = _load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return _load_font(18)


def build_placeholder(width: int, height: int, label: str, subtitle: str) -> Image.Image:
    img = Image.new("RGB", (width, height), "#0b1733")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        r = int(11 + (24 - 11) * y / max(height, 1))
        g = int(23 + (63 - 23) * y / max(height, 1))
        b = int(51 + (112 - 51) * y / max(height, 1))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    margin = max(24, width // 28)
    draw.rounded_rectangle(
        (margin, margin, width - margin, height - margin),
        radius=max(18, width // 40),
        outline="#4cb6ff",
        width=max(2, width // 320),
    )

    panel_top = height * 0.23
    panel_bottom = height * 0.77
    draw.rounded_rectangle(
        (margin * 1.5, panel_top, width - margin * 1.5, panel_bottom),
        radius=max(16, width // 48),
        outline="#22d3c5",
        width=max(2, width // 360),
    )

    accent_y = int(height * 0.82)
    draw.rectangle(
        (margin * 1.5, accent_y, width - margin * 1.5, accent_y + max(8, height // 50)),
        fill="#f29a38",
    )

    label_font = _fit_text(draw, label, int(width * 0.55))
    subtitle_font = _load_font(max(18, width // 42))

    label_bbox = draw.textbbox((0, 0), label, font=label_font)
    label_w = label_bbox[2] - label_bbox[0]
    label_h = label_bbox[3] - label_bbox[1]
    label_x = (width - label_w) / 2
    label_y = height * 0.39 - label_h / 2
    draw.text((label_x, label_y), label, fill="#f2f7ff", font=label_font)

    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_w) / 2
    subtitle_y = label_y + label_h + max(14, height // 36)
    draw.text((subtitle_x, subtitle_y), subtitle, fill="#b9c7e6", font=subtitle_font)

    return img.filter(ImageFilter.SMOOTH)


def main():
    parser = argparse.ArgumentParser(description="Create a placeholder image for article layout slots")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--label", required=True, help="Main label, e.g. COVER or IMG 01")
    parser.add_argument(
        "--size",
        choices=sorted(SIZE_PRESETS.keys()),
        default="article",
        help="Image preset size",
    )
    parser.add_argument(
        "--subtitle",
        default="replace with final image",
        help="Small helper text rendered below the label",
    )
    args = parser.parse_args()

    width, height = SIZE_PRESETS[args.size]
    img = build_placeholder(width, height, args.label, args.subtitle)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output, quality=92)
    print(output)


if __name__ == "__main__":
    main()
