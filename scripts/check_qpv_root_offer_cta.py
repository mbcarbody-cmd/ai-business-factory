#!/usr/bin/env python3
"""Static regression check for root launcher -> QPV paid offer CTA.

The root page must not leave a ready buyer in a generator-only dead end. It must
expose a direct buyer-facing offer link with source attribution, a fixed 19 EUR
price, and the same zero-confirmed-revenue guardrail as the checkout/ledger path.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "website" / "index.html"
OFFER = ROOT / "website" / "offer.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    index = read(INDEX)
    offer = read(OFFER)

    required_index_markers = [
        'id="qpvRootOfferCta"',
        './offer.html?source=root-launcher&campaign=qpv-19eur&buyer=product-seller&priceEur=19',
        'Pirkti Quick Product Video — 19 €',
        'root launcher now sends buyers directly to the QPV paid offer with source attribution',
        'Confirmed revenue remains 0 EUR until payment is manually verified in the ledger',
    ]
    for marker in required_index_markers:
        require(marker in index, f"root launcher missing buyer CTA marker: {marker}")

    require("Quick Product Video" in offer, "QPV offer must exist")
    require("19 EUR" in offer, "QPV offer must expose fixed launch price")
    require("Generate checkout-ready lead" in offer, "QPV offer must keep executable lead capture")
    require("./payment-ledger.html" in offer, "QPV offer must keep ledger payment proof path")
    require("revenueCountedEur:0" in offer, "QPV offer must not count unpaid revenue")

    rejected_weak_patterns = [
        'href="./offer.html"',
        'href="./payment.html"',
        "confirmedRevenueEur:19",
        "revenueCountedEur:19",
        "fake paid",
        "summary-only",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in index, f"root launcher must reject weak pattern: {pattern}")

    print("PASS qpv root offer CTA regression")
    print("checked: root launcher has attributed QPV 19 EUR offer CTA, lead path stays ledger-gated, confirmed revenue remains 0 EUR until paid verification")


if __name__ == "__main__":
    main()
