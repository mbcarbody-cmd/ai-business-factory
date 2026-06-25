#!/usr/bin/env python3
"""Regression gate for the Daily Agent Improvement Engine.

The check enforces the daily learning contract:
- at least 10 accepted learning events,
- at least 3 normalized lessons,
- at least 3 evaluation cases,
- at least 3 champion/challenger comparisons,
- at least 1 promoted workflow improvement or harmful rule removal,
- at least 1 completed cross-agent sync,
- weak patterns must be explicitly rejected,
- confirmed EUR must remain 0 unless paid/delivered evidence exists.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "website" / "daily-agent-improvement-engine.html"
html = ENGINE.read_text(encoding="utf-8")

def count_objects(array_name: str) -> int:
    match = re.search(rf"const {array_name}=\[(.*?)\];", html, re.S)
    if not match:
        raise SystemExit(f"FAIL: missing {array_name}")
    return len(re.findall(r"\{id:'", match.group(1)))

requirements = {
    "learningEvents": 10,
    "normalizedLessons": 3,
    "evaluationCases": 3,
    "comparisons": 3,
    "promotedChanges": 1,
    "crossAgentSync": 1,
}

for array_name, minimum in requirements.items():
    actual = count_objects(array_name)
    if actual < minimum:
        raise SystemExit(f"FAIL: {array_name} has {actual}, expected at least {minimum}")

required_patterns = [
    "workflow_rule_v2",
    "summary_only_learning_allowed",
    "workflow_rule_v2_regression_checked_delta",
    "harmful_rule_removed",
    "RevenueAgent",
    "QARegressionAgent",
    "WorkflowOpsAgent",
    "REJECT_WEAK_PATTERN",
    "REJECT_FAKE_REVENUE",
    "ACCEPT_PROMOTION",
    "confirmedRevenueEur: 0",
    "paid/delivered only count EUR",
    "policy_file_without_regression",
]

for pattern in required_patterns:
    if pattern not in html:
        raise SystemExit(f"FAIL: Daily Agent Improvement Engine missing required proof pattern: {pattern}")

for forbidden in [
    "summary_only_learning_allowed',replacement:'summary_only_learning_allowed'",
    "revenueEurConfirmed:19",
    "payment proof equals revenue",
    "policy_file_without_regression','ACCEPT",
]:
    if forbidden in html.replace(" ", ""):
        raise SystemExit(f"FAIL: weak/harmful pattern present: {forbidden}")

print("PASS: Daily Agent Improvement Engine has enough events, lessons, evals, comparisons, promoted rule removal and cross-agent sync without fake revenue.")
