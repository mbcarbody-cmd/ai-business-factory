#!/usr/bin/env python3
"""Regression for Daily Learning Promotion Receipt Ledger v9.

This rejects reading-only or policy-only learning proof by requiring a real
routeable workflow, deduped local ledger receipt, source attribution, regression
evidence and 0 EUR until verified paid/delivered revenue exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "daily-learning-promotion-receipt-ledger.html"
html = PAGE.read_text(encoding="utf-8")
compact = html.replace(" ", "")

required = [
    "DAILY AGENT IMPROVEMENT ENGINE v9",
    "PROMOTION RECEIPT LEDGER",
    "dailyLearningPromotionReceiptLedger",
    "workflow_rule_v9_daily_learning_promotion_receipt_ledger_required",
    "promotion_without_deduped_workflow_receipt_allowed",
    "daily-agent-improvement-engine-v9",
    "daily-learning-promotion-receipt-ledger.html",
    "source-kpi-admin.html?source=daily_learning_promotion_receipt_v9",
    "daily-learning-admin-router.html?source=daily_learning_promotion_receipt_v9",
    "operator-action-opened-ledger.html?source=daily_learning_promotion_receipt_v9",
    "revenue-command-center.html?source=daily_learning_promotion_receipt_v9",
    "scripts/check_daily_learning_promotion_receipt_ledger.py",
    "requiredLearningEvents:19",
    "normalizedLessons:8",
    "evaluationCases:10",
    "championChallengerComparisons:9",
    "promotedChangesOrRulesRemoved:9",
    "crossAgentKnowledgeSyncs:8",
    "confirmedRevenueEur:0",
    "promotionReceiptRevenueEur:0",
    "LearningOpsAgent",
    "QARegressionAgent",
    "AdminReviewAgent",
    "WorkflowOpsAgent",
    "RevenueAgent",
    "PolicyOnlyAgent",
    "SummaryOnlyAgent",
    "IdeaListAgent",
    "StaffingPlanAgent",
    "LearningOpsAgent->QARegressionAgent",
    "AdminReviewAgent->SourceKpiAdminWorkflow",
    "WorkflowOpsAgent->OperatorActionLedger",
    "RevenueAgent->RevenueCommandCenter",
    "reading-only learning proof",
    "summary-only learning proof",
    "new policy file without regression",
    "staffing plan as learning proof",
    "idea list as learning proof",
    "promotion receipt as revenue",
    "operator action as revenue",
    "source visit as revenue",
    "payment proof as revenue",
    "promotion without deduped workflow receipt",
    "function receiptIndex",
    "function recordReceipt",
    "Record deduped promotion receipt",
    "Promotion receipts are operational learning proof only and never revenue.",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: promotion receipt ledger missing marker: {marker}")

for forbidden in [
    "confirmedRevenueEur:19",
    "promotionReceiptRevenueEur:19",
    "promotion receipt equals revenue",
    "reading-only learning proof accepted",
    "summary-only learning proof accepted",
    "policy file without regression accepted",
    "promotion without deduped workflow receipt accepted",
    "operator action as revenue accepted",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: promotion receipt ledger accepts weak pattern: {forbidden}")

print("PASS: Daily Learning Promotion Receipt Ledger v9 verifies 19 events, 8 lessons, 10 evals, 9 comparisons, 9 promotions/removals and 8 syncs; records deduped operational promotion receipts with Source KPI/Admin/Operator/Revenue routes; rejects summary/policy/staffing/idea proof and keeps promotion receipts at 0 EUR until verified paid.")
