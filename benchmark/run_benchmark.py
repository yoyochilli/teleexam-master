#!/usr/bin/env python3
"""Run reproducible contract checks for evidence and Grill-Me outputs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evidence = load_module("evidence_auditor", ROOT / "skill" / "scripts" / "evidence_auditor.py")
grill = load_module("grill_turn_auditor", ROOT / "skill" / "scripts" / "grill_turn_auditor.py")


def grill_check(relative: str, phase: str) -> bool:
    text = (ROOT / relative).read_text(encoding="utf-8-sig")
    return bool(grill.audit(text, phase)["passed"])


cases = [
    {
        "id": "GOLD-EVIDENCE",
        "group": "golden",
        "passed": bool(evidence.check(ROOT / "examples" / "expected_output_excerpt.md")["passed"]),
        "expect": True,
    },
    {"id": "GOLD-ASK", "group": "golden", "passed": grill_check("examples/grill_turns/ask.txt", "ask"), "expect": True},
    {"id": "GOLD-CHALLENGE", "group": "golden", "passed": grill_check("examples/grill_turns/challenge.txt", "probe"), "expect": True},
    {"id": "GOLD-SCAFFOLD", "group": "golden", "passed": grill_check("examples/grill_turns/scaffold.txt", "scaffold"), "expect": True},
    {"id": "GOLD-AUDIT", "group": "golden", "passed": grill_check("examples/grill_turns/audit.md", "audit"), "expect": True},
    {
        "id": "BLOCK-UNTAGGED",
        "group": "violation",
        "passed": bool(evidence.check(FIXTURES / "bad_untagged_claim.md")["passed"]),
        "expect": False,
    },
    {
        "id": "BLOCK-NO-REMEDY",
        "group": "violation",
        "passed": bool(evidence.check(FIXTURES / "bad_missing_remedy.md")["passed"]),
        "expect": False,
    },
    {"id": "BLOCK-SPOILER", "group": "violation", "passed": grill_check("benchmark/fixtures/bad_spoiler_ask.txt", "ask"), "expect": False},
    {"id": "BLOCK-MULTI", "group": "violation", "passed": grill_check("benchmark/fixtures/bad_multi_question.txt", "ask"), "expect": False},
    {"id": "BLOCK-AUDIT", "group": "violation", "passed": grill_check("benchmark/fixtures/bad_incomplete_audit.md", "audit"), "expect": False},
]

for case in cases:
    case["matched_expectation"] = case["passed"] == case["expect"]

golden = [case for case in cases if case["group"] == "golden"]
violations = [case for case in cases if case["group"] == "violation"]
result = {
    "benchmark": "TeleExam Contract Benchmark v1",
    "scope": "规则与确定性审计器；不代表在线模型准确率",
    "total_cases": len(cases),
    "matched_expectation": sum(case["matched_expectation"] for case in cases),
    "golden_acceptance": {"passed": sum(case["passed"] for case in golden), "total": len(golden)},
    "violation_interception": {"passed": sum(not case["passed"] for case in violations), "total": len(violations)},
    "cases": cases,
}

print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["matched_expectation"] == result["total_cases"] else 1)
