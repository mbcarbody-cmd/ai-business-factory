#!/usr/bin/env python3
"""Regression gate ensuring revenue/product checks actually run in CI.

This prevents weak progress where regression scripts exist but are never executed on
push/PR. It intentionally checks executable workflow wiring, not summaries or docs.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"

REQUIRED_CHECKS = [
    "scripts/check_daily_agent_improvement_engine.py",
    "scripts/check_daily_learning_operator_queue.py",
    "scripts/check_qpv_source_kpi_admin.py",
    "scripts/check_qpv_root_offer_cta.py",
    "scripts/check_qpv_offer_checkout_handoff.py",
    "scripts/check_qpv_offer_checkout_attribution.py",
    "scripts/check_qpv_payment_ledger_source_attribution.py",
    "scripts/check_qpv_checkout_flow.py",
    "scripts/check_qpv_order_status_flow.py",
    "scripts/check_qpv_revenue_command_center.py",
    "scripts/check_qpv_recovery_revenue_reconciliation.py",
    "scripts/check_qpv_order_admin_revenue_nav.py",
    "scripts/check_qpv_outreach_lead_pipeline.py",
    "scripts/check_revenue_regression_ci.py",
]

REJECTED_WEAK_PATTERNS = [
    "echo PASS",
    "continue-on-error: true",
    "|| true",
    "allow_failure",
    "policy-only",
    "summary-only",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(WORKFLOW.exists(), "Missing revenue regression GitHub Actions workflow")
    text = WORKFLOW.read_text(encoding="utf-8")

    require("on:" in text and "push:" in text and "pull_request:" in text, "CI must run on push and PR")
    require("workflow_dispatch:" in text, "CI must allow manual dispatch fallback")
    require("actions/checkout@v4" in text, "CI must checkout repository before running checks")
    require("actions/setup-python@v5" in text, "CI must set up Python")
    require("set -euo pipefail" in text, "CI shell must fail hard on regression errors")

    for check in REQUIRED_CHECKS:
        require(check in text, f"CI workflow does not execute required regression: {check}")
        require((ROOT / check).exists(), f"CI references missing regression script: {check}")

    for weak in REJECTED_WEAK_PATTERNS:
        require(weak not in text, f"CI workflow contains rejected weak pattern: {weak}")

    print("PASS revenue regression CI wiring")
    print("checked: push/PR workflow, manual fallback, hard-fail shell, daily learning gates, operator queue gate, recovery revenue reconciliation gate, and all QPV revenue regression scripts executed")


if __name__ == "__main__":
    main()
