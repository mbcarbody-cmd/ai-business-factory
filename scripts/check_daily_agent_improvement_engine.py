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
- confirmed EUR must remain 0 unless paid/delivered evidence exists,
- blocked learning runs must route to an executable revenue fallback workflow,
- post-paid buyer workflows must require verified paid events and keep receipt actions at 0 EUR,
- admin payment review must preserve source attribution and expose source KPI filtering.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "website" / "daily-agent-improvement-engine.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"
html = ENGINE.read_text(encoding="utf-8")
compact = html.replace(" ", "")
workflow = WORKFLOW.read_text(encoding="utf-8")


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
    "workflow_rule_v3",
    "workflow_rule_v4",
    "workflow_rule_v5",
    "summary_only_learning_allowed",
    "workflow_rule_v2_regression_checked_delta",
    "fallback_task_list_allowed",
    "workflow_rule_v3_executable_revenue_fallback_required",
    "fallback_executes_product_workflow",
    "revenue-command-center.html",
    "daily-revenue-action.html",
    "receipt.html",
    "receipt_action_can_infer_revenue",
    "workflow_rule_v4_verified_paid_only_receipt_zero_revenue",
    "verified_paid_only_receipts",
    "receipt_generated/downloaded/emailed are 0 EUR service KPIs",
    "fake_revenue_from_receipt_event",
    "check_qpv_buyer_receipt_workflow.py",
    "source_blind_payment_review_allowed",
    "workflow_rule_v5_admin_source_kpi_filter_required",
    "admin_source_kpi_filter",
    "source_attributed_payment_review",
    "payment-ledger.html?source=daily_agent_improvement_v5",
    "learning_gate_not_required_in_ci",
    "workflow_rule_v5_daily_learning_gate_ci_required",
    "check_daily_agent_improvement_engine.py",
    "harmful_rule_removed",
    "workflow_improvement_promoted",
    "RevenueAgent",
    "QARegressionAgent",
    "WorkflowOpsAgent",
    "OutreachAgent",
    "CustomerSuccessAgent",
    "AdminReviewAgent",
    "REJECT_WEAK_PATTERN",
    "REJECT_FAKE_REVENUE",
    "ACCEPT_PROMOTION",
    "confirmedRevenueEur: 0",
    "paid/delivered only count EUR",
    "policy_file_without_regression",
    "fallback_task_list_without_workflow_route",
]

for pattern in required_patterns:
    if pattern not in html:
        raise SystemExit(f"FAIL: Daily Agent Improvement Engine missing required proof pattern: {pattern}")

for forbidden in [
    "summary_only_learning_allowed',replacement:'summary_only_learning_allowed'",
    "fallback_task_list_allowed',replacement:'fallback_task_list_allowed'",
    "receipt_action_can_infer_revenue',replacement:'receipt_action_can_infer_revenue'",
    "source_blind_payment_review_allowed',replacement:'source_blind_payment_review_allowed'",
    "learning_gate_not_required_in_ci',replacement:'learning_gate_not_required_in_ci'",
    "revenueEurConfirmed:19",
    "payment proof equals revenue",
    "receipt event equals revenue",
    "policy_file_without_regression','ACCEPT",
    "next task list is accepted learning",
    "source-blind admin accepted",
]
    if forbidden in compact:
        raise SystemExit(f"FAIL: weak/harmful pattern present: {forbidden}")

if "workingUrl:'./revenue-command-center.html'" not in html:
    raise SystemExit("FAIL: promoted executable fallback does not point at revenue command center")

if "workingUrl:'./receipt.html'" not in html:
    raise SystemExit("FAIL: promoted post-paid buyer workflow does not point at receipt.html")

if "workingUrl:'./payment-ledger.html?source=daily_agent_improvement_v5'" not in html:
    raise SystemExit("FAIL: promoted admin source KPI workflow does not point at attributed payment ledger")

if "python3 scripts/check_daily_agent_improvement_engine.py" not in workflow:
    raise SystemExit("FAIL: Daily Agent Improvement Engine regression is not wired into revenue CI")

print("PASS: Daily Agent Improvement Engine v5 has enough events, lessons, evals, comparisons, promoted executable fallback, verified-paid receipt workflow, admin source KPI workflow, harmful-rule removals and cross-agent sync without fake revenue.")
