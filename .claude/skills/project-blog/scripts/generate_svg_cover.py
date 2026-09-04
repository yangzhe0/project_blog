#!/usr/bin/env python3
"""Generate a project_blog SVG cover from the maintained 1280x448 template."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path


PALETTES = {
    "violet-cyan": ("#A78BFA", "#7C5CFC", "#45E4E8"),
    "azure-blue": ("#7CA7FF", "#3977F6", "#54D6FF"),
    "emerald-blue": ("#79EDA6", "#20B974", "#55A5FF"),
    "coral-violet": ("#FF9A82", "#F06464", "#9B7BFF"),
    "amber-magenta": ("#FFD166", "#F08A3C", "#D77BFF"),
    "teal-lime": ("#66E7D8", "#13B8AE", "#C4EA72"),
    "rose-indigo": ("#FFA1C6", "#D65CAC", "#7E8CFF"),
}

TITLE_Y = {
    2: (145, 238),
    3: (112, 190, 268),
    4: (82, 143, 204, 265),
}

# The browser renders the full 1280x448 banner at roughly 40% size and the
# homepage card may crop it further. Keep 20% width reserve beyond the measured
# fit so font fallback and responsive rounding cannot clip title glyphs.
TITLE_SCALE = 0.72


def visual_units(text: str) -> float:
    units = 0.0
    for char in text:
        if char.isspace():
            units += 0.34
        elif ord(char) < 128:
            units += 0.60 if char.isalnum() else 0.42
        else:
            units += 1.0
    return max(units, 1.0)


def title_size(text: str, line_count: int) -> int:
    cap = {2: 76, 3: 68, 4: 56}[line_count]
    fitted = min(cap, int(540 / visual_units(text)))
    return max(32, round(fitted * TITLE_SCALE))


def subtitle_size(text: str) -> int:
    return max(13, min(18, int(560 / visual_units(text))))


def display_text(text: str) -> str:
    """Remove visible punctuation while preserving letters numbers and CJK."""
    without_punctuation = "".join(
        char for char in text if not unicodedata.category(char).startswith("P")
    )
    return re.sub(r"\s+", " ", without_punctuation).strip()


def comparable_content(text: str) -> str:
    return re.sub(r"\s+", "", display_text(text))


def choose_palette(name: str, seed: str) -> tuple[str, tuple[str, str, str]]:
    if name != "auto":
        return name, PALETTES[name]
    names = tuple(PALETTES)
    index = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16) % len(names)
    chosen = names[index]
    return chosen, PALETTES[chosen]


def replace_token(svg: str, token: str, value: str) -> str:
    return svg.replace("{{" + token + "}}", value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", required=True, help="Exact full article title")
    parser.add_argument("--line", action="append", required=True, dest="lines", help="Title line; repeat 2-4 times")
    parser.add_argument("--category", default="", help=argparse.SUPPRESS)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--tags", required=True, help="Compact cover keywords")
    parser.add_argument("--date", required=True, help="YYMMDD or display date")
    parser.add_argument("--palette", choices=("auto", *PALETTES), default="auto")
    parser.add_argument("--seed", help="Optional stable palette seed; defaults to title")
    parser.add_argument("--force", action="store_true", help="Allow replacing an existing output")
    args = parser.parse_args()

    if not 2 <= len(args.lines) <= 4:
        parser.error("provide 2 to 4 --line values")
    if comparable_content("".join(args.lines)) != comparable_content(args.title):
        parser.error("title lines must preserve all non-punctuation title content")
    if args.output.exists() and not args.force:
        parser.error(f"output exists: {args.output}; pass --force to replace it")

    skill_root = Path(__file__).resolve().parents[1]
    template_path = skill_root / "references" / "svg-cover-template.svg"
    svg = template_path.read_text(encoding="utf-8")

    palette_name, colors = choose_palette(args.palette, args.seed or args.title)
    ys = TITLE_Y[len(args.lines)]
    title_lines = []
    for line, y in zip(args.lines, ys):
        visible_line = display_text(line)
        size = title_size(visible_line, len(args.lines))
        title_lines.append(
            f'      <text x="640" y="{y}" font-size="{size}" letter-spacing="-1.2">{html.escape(visible_line)}</text>'
        )

    visible_subtitle = display_text(args.subtitle)
    visible_tags = display_text(args.tags)
    values = {
        "FULL_TITLE": html.escape(args.title),
        "COLOR_1": colors[0],
        "COLOR_2": colors[1],
        "COLOR_3": colors[2],
        "TITLE_LINES": "\n".join(title_lines),
        "SUBTITLE_SIZE": str(subtitle_size(visible_subtitle)),
        "SUBTITLE": html.escape(visible_subtitle),
        "TAGS": html.escape(visible_tags),
        "DATE": html.escape(args.date),
    }
    for token, value in values.items():
        svg = replace_token(svg, token, value)

    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", svg)))
    if unresolved:
        raise RuntimeError(f"unresolved template tokens: {', '.join(unresolved)}")
    ET.fromstring(svg)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8", newline="\n")
    print(f"wrote {args.output} (palette={palette_name}, 1280x448)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
