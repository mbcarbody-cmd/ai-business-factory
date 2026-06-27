#!/usr/bin/env python3
"""Regression gate for the QPV revenue command center.

The command center must create measurable product-state movement by exposing the
buyer acquisition -> quote/checkout -> proof follow-up -> paid gate -> verified
receipt workflow while preserving revenue integrity. It is allowed to read
ledgers and build action links; it must not write fake paid events or count
proof/checkout/receipt as paid revenue.
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

    for needle, label in [
        ("QPV Revenue Command Center", "buyer-ready page title"),
        ("qpvOrderLedger", "order ledger read"),
        ("qpvOutreachLeadLedger", "outreach lead ledger read"),
        ("qpvPaidEventLedger", "paid event ledger read"),
        ("qpvReceiptLedger", "receipt ledger read"),
        ("isProofReadyUnpaid", "proof-ready unpaid filter"),
        ("checkoutReadyLead", "checkout-ready lead filter"),
        ("dedupPaidEvents", "paid event idempotency"),
        ("receiptReadyPaidEvent", "receipt-ready verified-paid filter"),
        ("receiptExistsFor", "receipt idempotency guard"),
        ("./daily-revenue-action.html", "daily action link"),
        ("./order-followup-export.html", "proof-ready export link"),
        ("./order-paid-bridge.html", "paid bridge link"),
        ("./paid-confirmation.html", "manual paid gate link"),
        ("./receipt.html", "buyer receipt link"),
        ("Generate receipt", "receipt action queue CTA"),
        ("receiptReadyPaidEvents", "receipt KPI count"),
        ("missingReceipts", "missing receipt queue KPI"),
        ("receiptLedgerRows", "receipt ledger KPI"),
        ("receipt action links preserve orderId and leadId when present", "receipt handoff guardrail"),
        ("receipts are aftercare only and never paid revenue", "receipt zero-revenue guardrail"),
        ("./outreach-lead-pipeline.html", "outreach pipeline link"),
        ("./quote-checkout.html", "quote checkout link"),
        ("./lead-conversion-kpi.html", "lead KPI link"),
        ("Buyer</span> SMB/product seller", "buyer segment"),
        ("Price</span> 19 EUR", "buyer-ready price"),
        ("payment proof is not revenue", "proof revenue guardrail"),
        ("checkout is not paid", "checkout revenue guardrail"),
        ("quote accepted is not paid", "quote revenue guardrail"),
        ("revenueDeltaFromThisPageEur:0", "zero revenue side-effect"),
        ("receiptRevenueEur:0", "receipt zero revenue effect"),
        ("duplicate paid references are deduplicated by orderId + reference", "dedupe QA rule"),
    ]:
        require(text, needle, label)

    for needle, label in [
        ("localStorage.setItem(paidKey", "paid ledger write"),
        ("localStorage.setItem('qpvPaidEventLedger'", "paid ledger write literal"),
        ("paymentStatus='paid'", "fake paid mutation"),
        ('paymentStatus="paid"', "fake paid mutation"),
        ("proof_submitted counts as revenue", "proof-as-revenue claim"),
        ("checkout counts as paid", "checkout-as-revenue claim"),
        ("receipt counts as revenue", "receipt-as-revenue claim"),
        ("receiptRevenueEur:19", "fake receipt revenue"),
        ("revenueEur:19", "hard-coded revenue event"),
        ("confirmedRevenueEur:19", "fake confirmed revenue"),
    ]:
        forbid(text, needle, label)

    print("PASS qpv revenue command center regression with receipt KPI")


if __name__ == "__main__":
    main()
