#!/usr/bin/env python3
"""Audit evidence-tag syntax in generated Markdown outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TAG = re.compile(r"\[(?:确凿依据｜[^\]]+|逻辑推导｜依赖：[^\]]+|资料缺失：[^\]]+)\]")
LOGIC = re.compile(r"\[逻辑推导｜依赖：([^\]]+)\]")
MISSING = re.compile(r"\[资料缺失：([^\]]+)\]")
REMEDY = re.compile(r"建议|请补充|核对|上传|提供|重新")
TABLE_DIVIDER = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")


def check(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig")
    errors: list[dict[str, object]] = []
    tagged = 0
    in_code = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        tagged += len(TAG.findall(line))
        is_table_fact = stripped.startswith("|") and stripped.count("|") >= 3 and not TABLE_DIVIDER.match(stripped)
        is_named_fact = bool(re.match(r"^(?:[-*]\s*)?(?:结论|答案|评分点|公式|考点)\s*[：:]", stripped))
        is_header = is_table_fact and any(name in stripped for name in ("核心线索", "详细笔记", "置信度与证据", "题号", "命题依据"))
        if ((is_table_fact and not is_header) or is_named_fact) and not TAG.search(line):
            errors.append({"line": number, "code": "missing_confidence_tag", "text": stripped})
        logic = LOGIC.search(line)
        if logic and not logic.group(1).strip():
            errors.append({"line": number, "code": "empty_dependency", "text": stripped})
        missing = MISSING.search(line)
        if missing and not REMEDY.search(missing.group(1)):
            errors.append({"line": number, "code": "missing_remedy", "text": stripped})
    if text.count("\\(") != text.count("\\)"):
        errors.append({"line": 0, "code": "unbalanced_inline_math", "text": "\\( 与 \\) 数量不一致"})
    if text.count("\\[") != text.count("\\]"):
        errors.append({"line": 0, "code": "unbalanced_display_math", "text": "\\[ 与 \\] 数量不一致"})
    return {"file": path.name, "tagged_items": tagged, "passed": not errors, "errors": errors}


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="检查三级置信度标签、推导依赖、补救动作与公式定界符")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        report = check(args.input)
    except FileNotFoundError:
        parser.error(f"找不到输入文件：{args.input}")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
