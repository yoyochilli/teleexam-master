#!/usr/bin/env python3
"""Extract visible text from PPTX slides while preserving slide numbers."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DRAWING_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
SLIDE_PATTERN = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
ZERO_WIDTH = re.compile("[\u200b-\u200f\u2028\u2029\u2060\ufeff\u00ad]")


def paragraphs(xml: bytes) -> list[str]:
    root = ET.fromstring(xml)
    result: list[str] = []
    for paragraph in root.iter(f"{DRAWING_NS}p"):
        text = "".join(node.text or "" for node in paragraph.iter(f"{DRAWING_NS}t")).strip()
        text = ZERO_WIDTH.sub("", text)
        if text and text != "AI生成" and not text.startswith(("生成时间:", "生成时间：")):
            result.append(text)
    return result


def extract(path: Path) -> list[dict[str, object]]:
    if path.suffix.lower() != ".pptx":
        raise ValueError("目前支持 .pptx；旧版 .ppt 请先另存为 .pptx。")
    with zipfile.ZipFile(path) as archive:
        members = sorted(
            ((int(match.group(1)), name) for name in archive.namelist() if (match := SLIDE_PATTERN.match(name))),
            key=lambda item: item[0],
        )
        slides = []
        for number, name in members:
            content = paragraphs(archive.read(name))
            slides.append({"number": number, "title": content[0] if content else f"第 {number} 页", "paragraphs": content[1:]})
        return slides


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="按页提取 PPTX 文本并保留证据位置")
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    slides = extract(args.input)
    if args.format == "json":
        print(json.dumps({"source": args.input.name, "slides": slides}, ensure_ascii=False, indent=2))
        return
    print(f"# PPTX 导入结果：{args.input.name}\n")
    for slide in slides:
        print(f"## 第 {slide['number']} 页：{slide['title']}")
        for line in slide["paragraphs"]:
            print(f"- {line}")
        print()


if __name__ == "__main__":
    main()
