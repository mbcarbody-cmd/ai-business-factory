#!/usr/bin/env python3
"""Regression gate for Revenue Command Center payment reminder navigation.

The command center must expose the payment reminder workflow as an executable
revenue follow-up action, while keeping reminders as conversion/follow-up events
only. It must never count proof, checkout, quote acceptance, or reminders as
confirmed EUR revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "revenue-command-center.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, 'href="./payment-reminder-workflow.html"', "top-level payment reminder navigation")
    require(text, 'Run reminders', "collect-revenue reminder CTA")
    require(text, "payment reminder workflow link is visible from command center", "QA reminder nav rule")
    require(text, "payment reminders are conversion/follow-up only and never paid revenue", "QA no-paid reminder rule")
    require(text, "payment-reminder-workflow.html',{orderId:row.orderId}", "orderId handoff to reminder workflow")
    require(text, "revenueDeltaFromThisPageEur:0", "zero revenue side-effect")
    require(text, "confirmedRevenueEur:confirmedRevenue(events)", "confirmed revenue from paid ledger only")
    require(text, "dedupPaidEvents(events)", "paid event dedupe gate")
    require(text, "payment proof is not revenue", "proof not revenue rule")
    require(text, "checkout is not paid", "checkout not paid rule")
    require(text, "quote accepted is not paid", "quote not paid rule")

    forbid(text, "revenueDeltaFromThisPageEur:19", "fake command-center revenue")
    forbid(text, "payment reminder is paid", "reminder-as-paid wording")
    forbid(text, "proof_submitted counts as revenue", "proof-as-sale wording")
    forbid(text, "checkout counts as paid", "checkout-as-sale wording")
    forbid(text, "quote accepted counts as paid", "quote-as-sale wording")

    print("PASS qpv revenue command center reminder navigation regression")


if __name__ == "__main__":
    main()
