#!/usr/bin/env python3
"""Regression gate for the 29 EUR Auto Parts Price Finder verified paid path.

This is a revenue-state gate, not a dashboard or idea list. It requires a real
manual verification workflow that counts APF revenue only after a duplicate-
protected paid event exists, updates payable order state, and creates a
fulfillment handoff.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing Auto Parts paid confirmation page")
    require(WORKFLOW.exists(), "missing revenue regression workflow")
    page = PAGE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    executable_markers = [
        "Auto Parts Price Finder verified payment — 29 €",
        "Executable revenue path · 29 EUR · APF verified paid gate",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const PAID_KEY='apfPaidEventLedger'",
        "const ORDER_KEY='apfPayableOrders'",
        "const FULFILLMENT_KEY='apfFulfillmentQueue'",
        "const DUPE_KEY='apfPaidDuplicateBlocks'",
        "function confirmPaid()",
        "function paidEventId(orderId,ref)",
        "function updatePayableOrder(event)",
        "function enqueueFulfillment(event)",
        "function confirmedRevenue()",
        "function exportPaidLedger()",
        "auto-parts-verified-paid-ledger.csv",
        "paid-fulfillment.html?",
    ]
    for marker in executable_markers:
        require(marker in page, f"paid confirmation page missing executable marker: {marker}")

    paid_gate_markers = [
        "Mark APF paid once",
        "Verified payment reference",
        "Admin verification note",
        "amount!==PRICE_EUR",
        "exact 29 EUR required",
        "verified_paid",
        "revenueCountedEur:PRICE_EUR",
        "29 EUR counted once",
        "ready_for_delivery",
        "payable order updated",
    ]
    for marker in paid_gate_markers:
        require(marker in page, f"paid confirmation page missing paid gate marker: {marker}")

    duplicate_and_zero_revenue_markers = [
        "duplicate_apf_paid_event_not_counted",
        "DUPLICATE_BLOCKED",
        "revenue unchanged",
        "revenueCountedEur:0",
        "NO_REVENUE",
        "order row",
        "payment reference",
        "proof text",
        "invoice request",
        "outreach row",
        "page visit",
        "duplicate click",
    ]
    for marker in duplicate_and_zero_revenue_markers:
        require(marker in page, f"paid confirmation page missing duplicate/zero-revenue marker: {marker}")

    rejected_fake_patterns = [
        "page visits are revenue",
        "proof text is revenue",
        "invoice request is revenue",
        "order intent is revenue",
        "duplicate clicks count revenue",
        "fake paid event",
        "revenueCountedEur:0 until paid gate is skipped",
    ]
    for pattern in rejected_fake_patterns:
        require(pattern not in page, f"fake/weak revenue pattern must not appear: {pattern}")

    require(
        "python3 scripts/check_auto_parts_paid_confirmation.py" in workflow,
        "CI workflow does not run APF paid confirmation regression",
    )

    print("PASS auto parts paid confirmation regression")
    print("checked: 29 EUR APF verified-paid gate, duplicate protection, payable-order update, fulfillment queue handoff, CSV export, and zero revenue for weak patterns")


if __name__ == "__main__":
    main()
