#!/usr/bin/env python3
"""Regression gate for QPV quote checkout.

The quote checkout is a buyer-ready step between outreach and checkout. It must
preserve lead attribution and never count quote/open/accept events as confirmed
revenue. Confirmed EUR remains owned by the manual paid gate.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "quote-checkout.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, "qpvQuoteLedger", "quote ledger persistence")
    require(text, "qpvConversionLedger", "conversion ledger persistence")
    require(text, "leadId is required", "leadId validation")
    require(text, "orderId is required", "orderId validation")
    require(text, "quote_created", "quote created conversion event")
    require(text, "quote_opened", "quote opened conversion event")
    require(text, "quote_accepted", "quote accepted conversion event")
    require(text, "quote_expired", "quote expired conversion event")
    require(text, "expired quote cannot continue to paid", "expired quote guardrail")
    require(text, "./checkout.html?", "checkout handoff URL")
    require(text, "./paid-confirmation.html", "manual paid gate navigation")
    require(text, "quoteAcceptedRevenueEur:0", "accepted quote is zero revenue")
    require(text, "confirmedRevenueEur:0", "confirmed revenue remains zero on quote page")
    require(text, "manual paid gate is the only confirmed revenue path", "paid gate revenue ownership")
    require(text, "all quote events preserve leadId and orderId", "attribution QA rule")

    forbid(text, "quote_accepted counts as paid", "quote acceptance as paid")
    forbid(text, "revenueEur:19", "hard-coded fake revenue")
    forbid(text, "confirmedRevenueEur:19", "fake confirmed revenue")
    forbid(text, "localStorage.setItem('qpvPaidEventLedger'", "quote page writing paid ledger")

    print("PASS qpv quote checkout regression")


if __name__ == "__main__":
    main()
