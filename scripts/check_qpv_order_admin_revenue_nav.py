#!/usr/bin/env python3
"""Regression gate for QPV order-admin revenue-path navigation.

The order admin must expose the executable revenue workflow pages directly. A hidden
paid bridge or missing manual paid gate slows verified revenue collection and causes
operators to fall back to weak proof-as-revenue patterns.
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

    require(text, 'href="./order-paid-bridge.html"', "top-level paid bridge navigation")
    require(text, 'href="./paid-confirmation.html"', "top-level manual paid gate navigation")
    require(text, 'href="./lead-conversion-kpi.html"', "lead KPI navigation")
    require(text, 'href="./outreach-lead-pipeline.html"', "outreach pipeline navigation")
    require(text, "paidBridgeHref(orderId)", "per-order paid bridge URL builder")
    require(text, '<a class="cta ghost" href="${bridge}">Paid bridge</a>', "per-order paid bridge action")
    require(text, "admin navigation exposes order-paid-bridge.html", "QA rule for bridge navigation")
    require(text, "admin navigation exposes paid-confirmation.html", "QA rule for manual paid gate")
    require(text, "Open Order → paid bridge to prefill the manual paid gate", "operator checklist bridge step")
    require(text, "Use Manual paid gate for idempotent paid confirmation", "operator checklist paid gate step")
    require(text, "proofSubmittedRevenueEur:0", "proof is still zero revenue")

    forbid(text, "proof_submitted counts as revenue", "weak revenue claim")
    forbid(text, "revenueCountedEur:19", "hard-coded fake revenue")
    forbid(text, "payment proof is a sale", "proof-as-sale wording")

    print("PASS qpv order-admin revenue navigation regression")


if __name__ == "__main__":
    main()
