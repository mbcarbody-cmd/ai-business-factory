#!/usr/bin/env python3
"""Regression gate for exposing APF paid checkout from the public root.

The root launcher must not hide the 29 EUR Auto Parts Price Finder behind deep
links or dashboards. It must expose a buyer-executable checkout path plus the
payment destination setup and APF paid confirmation handoff while still refusing
to count root clicks/page visits as revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CHECKOUT = ROOT / "website" / "auto-parts-instant-payment-link-checkout.html"
SETUP = ROOT / "website" / "auto-parts-payment-destination-setup.html"
PAID = ROOT / "website" / "auto-parts-paid-confirmation.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(INDEX.exists(), "missing public root index")
    require(CHECKOUT.exists(), "missing APF instant checkout page")
    require(SETUP.exists(), "missing APF payment destination setup page")
    require(PAID.exists(), "missing APF paid confirmation page")

    index = INDEX.read_text(encoding="utf-8")
    checkout = CHECKOUT.read_text(encoding="utf-8")
    setup = SETUP.read_text(encoding="utf-8")
    paid = PAID.read_text(encoding="utf-8")

    required_root_markers = [
        'id="auto-parts-price-finder-root-card"',
        "Auto Parts Price Finder — 29 € checkout",
        "./website/auto-parts-instant-payment-link-checkout.html?product=auto-parts-price-finder&priceEur=29&buyer=used-parts-seller&source=root-launcher",
        "Pirkti / siųsti 29 € checkout",
        "./website/auto-parts-payment-destination-setup.html?product=auto-parts-price-finder&priceEur=29&source=root-launcher",
        "Įvesti mokėjimo destination",
        "./website/auto-parts-paid-confirmation.html?product=auto-parts-price-finder&priceEur=29&buyer=used-parts-seller&source=root-launcher",
        "Paid confirmation",
        "apfPaidEventLedger",
        "APF revenue remains 0 EUR until verified paid event exists",
    ]
    for marker in required_root_markers:
        require(marker in index, f"root launcher missing APF buyer-path marker: {marker}")

    weak_patterns = [
        "root click is revenue",
        "page visit is revenue",
        "checkout click is revenue",
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "summary-only",
        "dashboard-only progress",
    ]
    for pattern in weak_patterns:
        require(pattern not in index, f"root launcher contains weak/fake revenue pattern: {pattern}")

    require("const LEDGER_KEY='apfInstantPaymentCheckoutLedger'" in checkout, "checkout must keep checkout-attempt ledger")
    require("const PAID_LEDGER_KEY='apfPaidEventLedger'" in checkout, "checkout must require APF paid ledger")
    require("function buildInstantCheckoutUrl()" in setup, "setup must generate instant checkout URL")
    require("PAID_KEY='apfPaidEventLedger'" in paid, "paid confirmation must write APF paid ledger")

    print("PASS APF root checkout launcher regression")
    print(
        "checked: public root exposes APF 29 EUR buyer checkout, payment destination setup, "
        "APF paid confirmation handoff, zero-revenue guard, and rejects root/page/checkout clicks as revenue"
    )


if __name__ == "__main__":
    main()
