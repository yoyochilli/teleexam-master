#!/usr/bin/env python3
"""Validate the visible evidence-graph snapshot required by study-map outputs."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_HEADINGS = ("资料体检", "复习准备度", "本次学习地图", "证据图谱快照")
REQUIRED_GRAPH_COLUMNS = ("来源节点", "考点/盲区节点", "用途节点", "状态")


def audit(text: str) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"缺少区块：{heading}")
    for column in REQUIRED_GRAPH_COLUMNS:
        if column not in text:
            errors.append(f"证据图谱缺少列：{column}")
    if "证据图谱快照" in text:
        tail = text.split("证据图谱快照", 1)[1]
        rows = [row for row in tail.splitlines() if row.strip().startswith("|")]
        data_rows = [row for row in rows if "---" not in row and "来源节点" not in row]
        if not data_rows:
            errors.append("证据图谱没有数据行")
        for row in data_rows:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) != 4 or any(not cell for cell in cells):
                errors.append("证据图谱存在孤立节点或空用途节点")
                break
            if cells[3] not in ("已闭合", "待确认", "资料冲突"):
                errors.append("证据图谱状态无效")
            if cells[3] == "已闭合" and any(word in cells[0] for word in ("缺失", "待补充", "未知", "待确认")):
                errors.append("缺失来源不得标记为已闭合")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="检查资料体检与证据图谱输出")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    errors = audit(args.file.read_text(encoding="utf-8"))
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: 资料体检与证据图谱结构完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
