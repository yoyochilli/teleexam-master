#!/usr/bin/env python3
"""Audit visible self-check and conflict blocks in a generated Markdown result."""

from __future__ import annotations

import argparse
from pathlib import Path


AUDIT_FIELDS = ("可定位课程结论", "逻辑推导", "资料缺失", "资料冲突", "公式核验", "越界术语")
CONFLICT_FIELDS = ("来源 A", "来源 B", "影响", "待确认")


def audit(text: str) -> list[str]:
    errors: list[str] = []
    if "【交付前自省审计】" not in text:
        errors.append("缺少【交付前自省审计】")
    for field in AUDIT_FIELDS:
        if field not in text:
            errors.append(f"自省审计缺少字段：{field}")
    if "[资料冲突" in text:
        for field in CONFLICT_FIELDS:
            if field not in text:
                errors.append(f"资料冲突区块缺少字段：{field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="检查交付前自省审计与资料冲突区块")
    parser.add_argument("file", type=Path, help="待检查的 Markdown/TXT 文件")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8")
    errors = audit(text)
    if errors:
        print("FAIL")
        for item in errors:
            print(f"- {item}")
        return 1
    print("PASS: 自省审计与资料冲突结构完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
