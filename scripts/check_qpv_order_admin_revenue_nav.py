#!/usr/bin/env python3
"""Regression gate for QPV order-admin revenue-path navigation.

The order admin must expose the executable revenue workflow pages directly. A hidden
paid bridge, reminder workflow, or recovery workflow slows verified revenue collection
and causes operators to fall back to weak proof/recovery-as-revenue patterns.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "order-admin.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, 'href="./revenue-command-center.html"', "top-level command center navigation")
    require(text, 'href="./payment-reminder-workflow.html"', "top-level payment reminder navigation")
    require(text, 'href="./abandoned-checkout-recovery.html"', "top-level abandoned checkout recovery navigation")
    require(text, 'href="./order-paid-bridge.html"', "top-level paid bridge navigation")
    require(text, 'href="./paid-confirmation.html"', "top-level manual paid gate navigation")
    require(text, 'href="./lead-conversion-kpi.html"', "lead KPI navigation")
    require(text, 'href="./outreach-lead-pipeline.html"', "outreach pipeline navigation")
    require(text, "paidBridgeHref(orderId)", "per-order paid bridge URL builder")
    require(text, "reminderHref(orderId)", "per-order payment reminder URL builder")
    require(text, "recoveryHref(orderId)", "per-order abandoned recovery URL builder")
    require(text, '<a class="cta ghost" href="${reminder}">Payment reminders</a>', "per-order payment reminder action")
    require(text, '<a class="cta ghost" href="${recovery}">Recovery</a>', "per-order recovery action")
    require(text, '<a class="cta ghost" href="${bridge}">Paid bridge</a>', "per-order paid bridge action")
    require(text, "paymentReminderUrl", "selected order exposes reminder URL")
    require(text, "abandonedRecoveryUrl", "selected order exposes recovery URL")
    require(text, "admin navigation exposes payment-reminder-workflow.html", "QA rule for reminder navigation")
    require(text, "admin navigation exposes abandoned-checkout-recovery.html", "QA rule for recovery navigation")
    require(text, "each order exposes reminder and abandoned recovery links by orderId", "QA rule for orderId handoff")
    require(text, "Open Payment reminders for unpaid proof/order follow-up without counting revenue", "operator checklist reminder step")
    require(text, "Open Abandoned checkout recovery when checkout stalled before verified payment", "operator checklist recovery step")
    require(text, "Open Order → paid bridge to prefill the manual paid gate", "operator checklist bridge step")
    require(text, "Use Manual paid gate for idempotent paid confirmation", "operator checklist paid gate step")
    require(text, "proofSubmittedRevenueEur:0", "proof is still zero revenue")
    require(text, "reminderRevenueEur:0", "reminders are zero revenue")
    require(text, "recoveryRevenueEur:0", "recovery is zero revenue")

    forbid(text, "proof_submitted counts as revenue", "weak revenue claim")
    forbid(text, "reminder counts as revenue", "reminder-as-sale wording")
    forbid(text, "recovery counts as revenue", "recovery-as-sale wording")
    forbid(text, "revenueCountedEur:19", "hard-coded fake revenue")
    forbid(text, "payment proof is a sale", "proof-as-sale wording")

    print("PASS qpv order-admin revenue navigation regression")


if __name__ == "__main__":
    main()
