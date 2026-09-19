#!/usr/bin/env python3
"""Validate one Grill-Me response against phase-specific anti-spoiler rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PRE_AUDIT_PHASES = {"ask", "probe", "scaffold"}
SPOILER = re.compile(r"参考答案|标准答案|正确答案|完整解析|评分标准|【采分点核验】|【课件直连】|【盲区入库】")
QUESTION_BLOCK = re.compile(r"(?:^|\n)\s*(?:第\s*)?\d+\s*[.、题]\s*")
AUDIT_SECTIONS = ("【采分点核验】", "【课件直连】", "【盲区入库】")


def audit(text: str, phase: str) -> dict[str, object]:
    stripped = text.rstrip()
    errors: list[str] = []
    if not stripped.endswith("？"):
        errors.append("reply_must_end_with_question_mark")
    if phase in PRE_AUDIT_PHASES:
        spoilers = sorted(set(SPOILER.findall(text)))
        if spoilers:
            errors.append("spoiler_content:" + ",".join(spoilers))
        count = len(QUESTION_BLOCK.findall(text))
        if count > 1:
            errors.append(f"multiple_questions:{count}")
        if phase == "scaffold" and re.search(r"(?:答案为|等于|结果是|所以)\s*[^？\n]+", text):
            errors.append("scaffold_may_reveal_result")
    if phase == "audit":
        for section in AUDIT_SECTIONS:
            if section not in text:
                errors.append("missing_section:" + section)
        if not stripped.endswith("是否继续下一题？"):
            errors.append("audit_must_end_with_continue_question")
    return {"phase": phase, "passed": not errors, "errors": errors}


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="检查 Grill-Me 单题、禁剧透和问句收尾规则")
    parser.add_argument("input", type=Path)
    parser.add_argument("--phase", required=True, choices=("ask", "probe", "scaffold", "audit"))
    args = parser.parse_args()
    try:
        text = args.input.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        parser.error(f"找不到输入文件：{args.input}")
    report = audit(text, args.phase)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
