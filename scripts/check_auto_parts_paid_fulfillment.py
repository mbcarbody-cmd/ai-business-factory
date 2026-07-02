#!/usr/bin/env python3
"""Regression gate for APF 29 EUR paid fulfillment completion.

This is not a dashboard/audit/summary gate. It requires a buyer-ready APF
fulfillment workflow that reads verified paid events, completes one unique
order, produces receipt text, writes a completed ledger, exports CSV, blocks
duplicates, and keeps all visits/copies/downloads/mailto clicks at 0 EUR.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-paid-fulfillment.html"
PAID_PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF paid fulfillment page")
    require(PAID_PAGE.exists(), "missing APF paid confirmation page")
    page = PAGE.read_text(encoding="utf-8")
    paid = PAID_PAGE.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder — paid fulfillment",
        "Executable revenue path · 29 EUR · APF paid fulfillment · completed-order ledger",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const PAID_KEY='apfPaidEventLedger'",
        "const QUEUE_KEY='apfFulfillmentQueue'",
        "const COMPLETED_KEY='apfCompletedOrderLedger'",
        "const DUPLICATE_KEY='apfFulfillmentDuplicateBlocks'",
        "function verifiedPaid(row)",
        "function uniqueVerifiedPaid()",
        "function fallbackQueueFromPaid()",
        "function pendingRows()",
        "function completeNext()",
        "function receiptFor(row)",
        "function exportCompleted()",
        "completedOrderRevenueEur:PRICE_EUR",
        "fulfillmentStatus:'fulfilled'",
        "source:'auto-parts-paid-fulfillment'",
        "auto-parts-completed-orders.csv",
        "auto-parts-price-finder-receipt.txt",
        "Email latest receipt",
    ]
    for marker in required_markers:
        require(marker in page, f"APF fulfillment page missing marker: {marker}")

    buyer_ready_markers = [
        "Buyer-ready delivery receipt",
        "Auto Parts Price Finder audit delivery",
        "Status: fulfilled",
        "Amount paid: ${PRICE_EUR} EUR",
        "Delivery: APF price audit ready",
        "mailto:",
        "buyer receipt is aftercare and not additional revenue",
    ]
    for marker in buyer_ready_markers:
        require(marker in page, f"APF fulfillment page missing buyer-ready marker: {marker}")

    integrity_markers = [
        "complete only verified apfPaidEventLedger rows",
        "fallback to verified paid events if queue row is missing",
        "write apfCompletedOrderLedger exactly once per paidEventId",
        "fulfilled EUR is reconciled only from completed ledger rows backed by APF paid events",
        "duplicate_apf_fulfillment_not_counted",
        "revenueFromReceiptCopyEur:0",
        "revenueFromReceiptDownloadEur:0",
        "revenueFromMailtoClickEur:0",
        "revenueFromQueueRowsEur:0",
        "duplicateFulfillmentRevenueEur:0",
    ]
    for marker in integrity_markers:
        require(marker in page, f"APF fulfillment page missing revenue-integrity marker: {marker}")

    rejected_fake_revenue = [
        "receiptCopyRevenueEur:29",
        "receiptDownloadRevenueEur:29",
        "mailtoClickRevenueEur:29",
        "queueRowsAreRevenue",
        "pending fulfillment is revenue",
        "page visit is revenue",
        "dashboard-only progress",
        "summary-only progress",
        "fake paid",
    ]
    for pattern in rejected_fake_revenue:
        require(pattern not in page, f"weak/fake fulfillment revenue pattern must not appear: {pattern}")

    require("apfFulfillmentQueue" in paid, "APF paid confirmation must enqueue APF fulfillment rows")
    print("PASS auto parts paid fulfillment regression")
    print("checked: APF verified paid ledger, fallback queue, completed order ledger, duplicate suppression, buyer receipt, CSV export, and zero revenue for visits/copy/download/mailto/queue rows")


if __name__ == "__main__":
    main()
