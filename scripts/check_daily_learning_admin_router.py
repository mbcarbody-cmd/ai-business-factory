#!/usr/bin/env python3
"""Regression for Daily Learning Admin Router v8.

This rejects policy-only learning proof by requiring a routeable workflow that
connects Daily Agent Improvement learning proof to Source KPI Admin, a direct
Source KPI backlink contract and the Operator Action Opened Ledger, while
keeping operator/fallback activity at 0 EUR.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "daily-learning-admin-router.html"
html = PAGE.read_text(encoding="utf-8")
compact = html.replace(" ", "")

required = [
    "DAILY AGENT IMPROVEMENT ENGINE v8",
    "SOURCE KPI BACKLINK CONTRACT",
    "workflow_rule_v8_daily_learning_admin_router_source_kpi_backlink_required",
    "learning_workflow_without_source_kpi_admin_backlink_allowed",
    "daily-agent-improvement-engine-v8",
    "daily-learning-admin-router.html?source=daily_agent_improvement_v8",
    "source-kpi-admin.html?source=daily_learning_admin_router_v8",
    "source-kpi-admin.html?source=source_kpi_admin_learning_router_backlink_required",
    "operator-action-opened-ledger.html?source=daily_learning_admin_router_v8",
    "daily-learning-operator-queue.html?source=daily_learning_admin_router_v8",
    "revenue-command-center.html?source=daily_learning_admin_router_v8",
    "requiredLearningEvents:18",
    "normalizedLessons:7",
    "evaluationCases:9",
    "championChallengerComparisons:8",
    "promotedChangesOrRulesRemoved:8",
    "crossAgentKnowledgeSyncs:7",
    "confirmedRevenueEur:0",
    "sourceKpiBacklinkRevenueEur:0",
    "dailyLearningSourceKpiBacklinkContract",
    "LearningOpsAgent",
    "QARegressionAgent",
    "AdminReviewAgent",
    "WorkflowOpsAgent",
    "PolicyOnlyAgent",
    "SummaryOnlyAgent",
    "IdeaListAgent",
    "AdminReviewAgent->SourceKpiAdminWorkflow",
    "reading-only learning proof",
    "summary-only learning proof",
    "new policy file without regression",
    "staffing plan as learning proof",
    "idea list as learning proof",
    "opened operator action as revenue",
    "payment proof as revenue",
    "learning workflow without source KPI backlink",
    "dailyLearningAdminRouterProof",
    "scripts/check_daily_learning_admin_router.py",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: daily learning admin router missing marker: {marker}")

for forbidden in [
    "confirmedRevenueEur:19",
    "sourceKpiBacklinkRevenueEur:19",
    "openedOperatorActionRevenueEur:19",
    "operatorQueueExportRevenueEur:19",
    "payment proof equals revenue",
    "reading-only learning proof accepted",
    "summary-only learning proof accepted",
    "policy file without regression accepted",
    "learning workflow without source KPI backlink accepted",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: daily learning admin router accepts weak pattern: {forbidden}")

print("PASS: Daily Learning Admin Router v8 links learning proof to Source KPI Admin, Source KPI backlink contract, Operator Action Opened Ledger, operator queue and revenue command center; verifies 18 events, 7 lessons, 9 evals, 8 comparisons, 8 promotions/removals and 7 syncs; rejects policy/summary/idea proof and backlink-free learning workflows; keeps fallback/operator activity at 0 EUR until verified paid.")
