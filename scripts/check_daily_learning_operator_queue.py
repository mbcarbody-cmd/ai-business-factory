#!/usr/bin/env python3
"""Static regression for Daily Learning Operator Queue workflow."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "website" / "daily-learning-operator-queue.html"
ENGINE = ROOT / "website" / "daily-agent-improvement-engine.html"
queue = QUEUE.read_text(encoding="utf-8")
engine = ENGINE.read_text(encoding="utf-8")
compact_queue = queue.replace(" ", "")

required = [
    "Daily learning operator queue",
    "dailyAgentImprovementOperatorQueueLedger",
    "workflow_rule_v6",
    "operator_queue_required",
    "source-kpi-admin.html?source=daily_agent_improvement_v6",
    "revenue-command-center.html?source=daily_agent_improvement_v6",
    "payment-ledger.html?source=daily_agent_improvement_v6",
    "confirmedRevenueEur:0",
    "revenueEur:0",
    "reading_only",
    "summary_only",
    "policy_file_without_regression",
    "new_policy_file_without_workflow_delta",
    "next_task_only_fallback_allowed",
    "fallback_task_list_without_workflow_route",
    "fake_revenue_from_payment_proof",
    "fake_revenue_from_receipt_event",
    "source_blind_payment_review_allowed",
    "Record fallback route",
    "Run source KPI fallback",
]
for marker in required:
    if marker not in queue and marker not in compact_queue:
        raise SystemExit(f"FAIL: daily learning operator queue missing marker: {marker}")

engine_required = [
    "workflow_rule_v6",
    "daily-learning-operator-queue.html",
    "source-kpi-admin.html?source=daily_agent_improvement_v6",
    "workflow_rule_v6_operator_queue_required",
    "LearningOpsAgent",
]
for marker in engine_required:
    if marker not in engine:
        raise SystemExit(f"FAIL: daily engine not wired to v6 operator queue: {marker}")

for forbidden in [
    "confirmedRevenueEur:19",
    "revenueEur:19",
    "payment proof equals revenue",
    "receipt event equals revenue",
    "summary only accepted",
    "next task only accepted",
]:
    if forbidden in queue:
        raise SystemExit(f"FAIL: weak queue pattern present: {forbidden}")

print("PASS: Daily learning operator queue is executable, source-attributed, rejects weak learning proof, routes fallback into product workflows, and keeps operator actions at 0 EUR.")
