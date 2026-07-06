#!/usr/bin/env python3
"""Regression gate for APF buyer-ready paid receipt desk.

This is a product/workflow gate: a receipt may be generated only from an
existing duplicate-protected verified paid APF ledger row. Receipt actions must
not create revenue or pretend that page visits/copies/mailto/export are sales.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-paid-receipt.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF paid receipt page")
    require(WORKFLOW.exists(), "missing revenue regression workflow")
    page = PAGE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    executable_markers = [
        "Auto Parts Price Finder paid receipt desk — 29 €",
        "Executable revenue path · APF paid receipt · requires verified paid ledger row · 29 EUR",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const PAID_KEY='apfPaidEventLedger'",
        "const RECEIPT_KEY='apfPaidReceiptLedger'",
        "function findPaidEvent()",
        "function loadReceipt()",
        "function buildReceiptPayload(event)",
        "APF_BUYER_READY_PAID_RECEIPT",
        "auto-parts-paid-receipts.json",
    ]
    for marker in executable_markers:
        require(marker in page, f"paid receipt page missing executable marker: {marker}")

    verified_paid_gate_markers = [
        "verified paid ledger row not found",
        "fallback: open paid confirmation and verify 29 EUR payment first",
        "event.product!==PRODUCT",
        "Number(event.amountEur)!==PRICE_EUR",
        "Number(event.revenueCountedEur)!==PRICE_EUR",
        "!clean(event.paymentProof)",
        "event.status!=='verified_paid'",
        "requires product, exact 29 EUR, proof, verified_paid status",
        "buyer-ready receipt generated from verified paid ledger",
        "original APF revenue already counted once in paid ledger",
    ]
    for marker in verified_paid_gate_markers:
        require(marker in page, f"paid receipt page missing verified-paid gate marker: {marker}")

    zero_revenue_markers = [
        "revenueCountedEur:0",
        "0 EUR new revenue; receipt uses existing verified paid event only",
        "receipt revenueCountedEur:0",
        "COPIED_RECEIPT: buyer delivery action only; revenueCountedEur:0",
        "EXPORTED_RECEIPT_JSON: export action only; revenueCountedEur:0",
        "Receipt actions do not create revenue",
    ]
    for marker in zero_revenue_markers:
        require(marker in page, f"paid receipt page missing zero-revenue marker: {marker}")

    rejected_weak_patterns = [
        "receipt page visit",
        "copied receipt",
        "exported JSON",
        "opened mailto",
        "delivery link",
        "manual text",
        "fake/demo paidEventId",
        "missing paymentProof",
        "non-ledger order row",
    ]
    for marker in rejected_weak_patterns:
        require(marker in page, f"paid receipt page missing rejected weak pattern: {marker}")

    fake_revenue_patterns = [
        "receipt copied is revenue",
        "mailto opened is revenue",
        "delivery link is revenue",
        "receipt revenueCountedEur:29",
        "revenueCountedEur:PRICE_EUR,source:'auto-parts-paid-receipt'",
    ]
    for pattern in fake_revenue_patterns:
        require(pattern not in page, f"fake receipt revenue pattern must not appear: {pattern}")

    require(
        "python3 scripts/check_auto_parts_paid_receipt.py" in workflow,
        "CI workflow does not run APF paid receipt regression",
    )

    print("PASS auto parts paid receipt regression")
    print("checked: buyer-ready receipt from verified paid APF ledger only, proof/status/29 EUR gate, receipt ledger, copy/export/mailto zero revenue, and rejected weak patterns")


if __name__ == "__main__":
    main()
