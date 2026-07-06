#!/usr/bin/env python3
"""Regression gate for APF first-buyer outreach launchpad.

This is a product-state check, not a summary/audit. It verifies that the page
creates concrete outreach-ready rows while blocking fake payment destinations and
refusing to count outreach/copy/export actions as revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-first-buyer-outreach-launchpad.html"
INDEX = ROOT / "index.html"

REQUIRED_PAGE_STRINGS = [
    "apfFirstBuyerOutreachLedger",
    "apfPaidEventLedger",
    "Generate 10 outreach-ready rows",
    "BUYER_SEGMENTS",
    "APF-OUTREACH-",
    "auto-parts-payment-launch-url-builder.html",
    "auto-parts-payment-proof-handoff.html",
    "revenueCountedEur:0",
    "revenueCountedEur:0",
    "productionDestinationStatus",
    "TRUSTED_PAYMENT_HOSTS",
    "looksLikeIban",
    "DEMO_DESTINATION_PATTERNS",
    "BLOCKER: demo/test/example/fake payment destination is not buyer-ready.",
    "outreach row, copied message, exported CSV, opened mailto, page visit and payment link click are not revenue",
]

REQUIRED_BUYER_SEGMENTS = [
    "Kaunas used parts seller",
    "RRR.lt dismantler",
    "eBay parts exporter",
    "Bodyshop buyer",
    "Hybrid/EV breaker",
    "Small scrapyard owner",
    "Facebook parts seller",
    "Insurance repair reseller",
    "Lithuania/Poland broker",
    "Premium SUV parts seller",
]

REJECTED_WEAK_PROGRESS = [
    "revenueCountedEur:29",
    "confirmed revenue 29",
    "outreach counted as revenue",
    "mailto counted as revenue",
    "CSV export counted as revenue",
    "demo destination accepted",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "Missing APF first buyer outreach launchpad page")
    page = PAGE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    for needle in REQUIRED_PAGE_STRINGS:
        require(needle in page, f"Launchpad missing required product-state string: {needle}")

    for segment in REQUIRED_BUYER_SEGMENTS:
        require(segment in page, f"Launchpad missing outreach-ready buyer segment: {segment}")

    for weak in REJECTED_WEAK_PROGRESS:
        require(weak not in page, f"Launchpad contains rejected weak revenue pattern: {weak}")

    require(page.count("['") >= 10, "Launchpad must embed at least 10 outreach-ready rows")
    require("auto-parts-first-buyer-outreach-launchpad.html" in index, "Root launcher must link APF outreach launchpad")
    require("outreach row" in index and "rejected weak patterns" in index.lower(), "Root must reject outreach rows as revenue")

    print("PASS APF first buyer outreach launchpad regression")
    print("checked: 10 buyer-ready rows, payment/proof deep links, production destination gate, fake/demo blocking, ledger storage, root link, and zero-revenue rule")


if __name__ == "__main__":
    main()
