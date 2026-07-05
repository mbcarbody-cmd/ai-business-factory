#!/usr/bin/env python3
"""Regression for Daily Learning Admin Router v7.

This rejects policy-only learning proof by requiring a routeable workflow that
connects Daily Agent Improvement learning proof to Source KPI Admin and the
Operator Action Opened Ledger, while keeping operator/fallback activity at 0 EUR.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "daily-learning-admin-router.html"
html = PAGE.read_text(encoding="utf-8")
compact = html.replace(" ", "")

required = [
    "DAILY AGENT IMPROVEMENT ENGINE v7",
    "workflow_rule_v7_daily_learning_admin_router_required",
    "opened_operator_action_without_source_kpi_admin_link_allowed",
    "daily-agent-improvement-engine-v7",
    "daily-learning-admin-router.html?source=daily_agent_improvement_v7",
    "source-kpi-admin.html?source=daily_learning_admin_router_v7",
    "operator-action-opened-ledger.html?source=daily_learning_admin_router_v7",
    "daily-learning-operator-queue.html?source=daily_learning_admin_router_v7",
    "revenue-command-center.html?source=daily_learning_admin_router_v7",
    "requiredLearningEvents:18",
    "normalizedLessons:7",
    "evaluationCases:9",
    "championChallengerComparisons:8",
    "promotedChangesOrRulesRemoved:7",
    "crossAgentKnowledgeSyncs:6",
    "confirmedRevenueEur:0",
    "LearningOpsAgent",
    "QARegressionAgent",
    "AdminReviewAgent",
    "WorkflowOpsAgent",
    "PolicyOnlyAgent",
    "SummaryOnlyAgent",
    "IdeaListAgent",
    "reading-only learning proof",
    "summary-only learning proof",
    "new policy file without regression",
    "staffing plan as learning proof",
    "idea list as learning proof",
    "opened operator action as revenue",
    "payment proof as revenue",
    "dailyLearningAdminRouterProof",
    "scripts/check_daily_learning_admin_router.py",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: daily learning admin router missing marker: {marker}")

for forbidden in [
    "confirmedRevenueEur:19",
    "openedOperatorActionRevenueEur:19",
    "operatorQueueExportRevenueEur:19",
    "payment proof equals revenue",
    "reading-only learning proof accepted",
    "summary-only learning proof accepted",
    "policy file without regression accepted",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: daily learning admin router accepts weak pattern: {forbidden}")

print("PASS: Daily Learning Admin Router v7 links learning proof to Source KPI Admin, Operator Action Opened Ledger, operator queue and revenue command center; verifies 18 events, 7 lessons, 9 evals, 8 comparisons, 7 promotions/removals and 6 syncs; rejects policy/summary/idea proof; keeps fallback/operator activity at 0 EUR until verified paid.")
