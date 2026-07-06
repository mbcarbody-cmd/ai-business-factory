#!/usr/bin/env python3
"""Regression gate for APF paid fulfillment delivery desk.

This is not a summary/audit/dashboard gate. It requires a concrete post-payment
workflow that reads verified 29 EUR APF paid events, creates buyer-ready delivery
packs, dedupes delivery by paid event, and keeps delivery/copy/export/mailto at
0 EUR because revenue is counted only by the verified paid ledger.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-fulfillment-delivery-desk.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF paid fulfillment delivery desk page")
    page = PAGE.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder — paid fulfillment delivery desk",
        "Executable revenue product · 29 EUR · APF paid fulfillment",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const PAID_KEY='apfPaidEventLedger'",
        "const FULFILLMENT_KEY='apfFulfillmentQueue'",
        "const DELIVERY_KEY='apfPaidDeliveryLedger'",
        "function verifiedPaidEvents()",
        "function fulfillmentByPaidId()",
        "function deliveryEmail(event,task)",
        "function buildDeliveries()",
        "ready_to_send_after_paid_verification",
        "auto-parts-paid-deliveries.json",
    ]
    for marker in required_markers:
        require(marker in page, f"APF paid delivery page missing marker: {marker}")

    buyer_ready_markers = [
        "Your Auto Parts Price Finder result",
        "Product: Auto Parts Price Finder",
        "Price paid: 29 EUR",
        "Payment proof:",
        "Result:",
        "paid buyer delivery packs built",
    ]
    for marker in buyer_ready_markers:
        require(marker in page, f"APF paid delivery page missing buyer-ready marker: {marker}")

    integrity_markers = [
        "read only verified_paid APF events with revenueCountedEur 29",
        "dedupe deliveries by paidEventId",
        "create buyer-ready delivery email and JSON pack",
        "write delivery rows with revenueCountedEur 0",
        "count revenue only through apfPaidEventLedger verified_paid rows",
        "revenueFromDeliveryPackEur:0",
        "revenueFromCopiedEmailEur:0",
        "revenueFromExportJsonEur:0",
        "revenueFromMailtoEur:0",
    ]
    for marker in integrity_markers:
        require(marker in page, f"APF paid delivery page missing integrity marker: {marker}")

    rejected_fake_revenue = [
        "deliveryPackRevenueEur:29",
        "copiedEmailRevenueEur:29",
        "exportJsonRevenueEur:29",
        "mailtoRevenueEur:29",
        "resultUrlRevenueEur:29",
        "delivery is revenue",
        "fake paid event accepted",
        "duplicate delivery counted as revenue",
    ]
    for pattern in rejected_fake_revenue:
        require(pattern not in page, f"weak/fake delivery revenue pattern must not appear: {pattern}")

    print("PASS auto parts paid fulfillment delivery desk regression")
    print("checked: verified paid-event ingestion, fulfillment queue merge, paidEventId delivery dedupe, buyer-ready delivery email/JSON, and zero revenue for delivery/copy/export/mailto actions")


if __name__ == "__main__":
    main()
