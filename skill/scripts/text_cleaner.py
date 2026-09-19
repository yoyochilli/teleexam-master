#!/usr/bin/env python3
"""Normalize study text and split it into evidence-ready units."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ZERO_WIDTH = re.compile("[\u200b-\u200f\u2028\u2029\u2060\ufeff\u00ad]")
QUESTION = re.compile(r"^(?:第?\s*\d+\s*[题、.．]|[(（]\s*\d+\s*[）)]|\d+\s*[、.．])\s*(.*)$")
HEADING = re.compile(r"^(?:#{1,6}\s+|第[一二三四五六七八九十\d]+[章节]|[一二三四五六七八九十]+[、.])\s*(.+)$")


def normalize(text: str) -> list[str]:
    text = ZERO_WIDTH.sub("", text)
    table = str.maketrans({"：": ":", "；": ";", "，": ",", "（": "(", "）": ")", "　": " "})
    lines = []
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = re.sub(r"[ \t]+", " ", raw.translate(table)).strip()
        if line and line != "AI生成":
            lines.append(line)
    return lines


def build_units(lines: list[str]) -> list[dict[str, object]]:
    units: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in lines:
        heading = HEADING.match(line)
        if heading:
            current = {"title": heading.group(1).strip(), "items": []}
            units.append(current)
            continue
        if current is None:
            current = {"title": "未归类材料", "items": []}
            units.append(current)
        question = QUESTION.match(line)
        kind = "question" if question else "bullet" if line.startswith(("-", "*", "•")) else "note"
        content = question.group(1).strip() if question else line.lstrip("-*• ").strip()
        current["items"].append({"type": kind, "text": content})
    return units


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="清洗课程笔记和题目文本")
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="json")
    args = parser.parse_args()
    units = build_units(normalize(args.input.read_text(encoding="utf-8-sig")))
    payload = {"source": args.input.name, "unit_count": len(units), "units": units}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# 清洗结果：{args.input.name}\n")
        for index, unit in enumerate(units, 1):
            print(f"## {index}. {unit['title']}")
            for item in unit["items"]:
                print(f"- {item['type']}: {item['text']}")
            print()


if __name__ == "__main__":
    main()
