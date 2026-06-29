#!/usr/bin/env python3
"""Regression gate for QPV offer -> checkout source attribution.

This protects measurable KPI movement: traffic from the public offer must keep
source/attribution through checkout, local order proof, payment proof links and
conversion ledger events without counting unverified revenue.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OFFER = ROOT / "website" / "offer.html"
CHECKOUT = ROOT / "website" / "checkout.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    offer = read(OFFER)
    checkout = read(CHECKOUT)

    required_offer_markers = [
        "SOURCE ATTRIBUTION",
        "function attributionSource()",
        "source:data.source",
        "attribution:'qpv_offer_checkout_handoff'",
        "Source: ${data.source}",
        "Checkout-ready lead generated with source attribution",
        "checkout.html receives leadId/source and creates payment_pending order",
        "unattributed checkout traffic that cannot be measured",
        "revenueCountedEur:0",
    ]
    for marker in required_offer_markers:
        require(marker in offer, f"offer missing source attribution marker: {marker}")

    href_body = re.search(r"function checkoutHref\(data\)\{(.+?)\}\nfunction buildMailto", offer, re.S)
    require(href_body is not None, "offer must define executable checkoutHref(data)")
    for marker in ["leadId:data.leadId", "source:data.source", "attribution:'qpv_offer_checkout_handoff'", "./checkout.html?"]:
        require(marker in href_body.group(1), f"checkoutHref must propagate {marker}")

    required_checkout_markers = [
        "SOURCE ATTRIBUTION",
        "function sourceFrom()",
        "function attributionFrom()",
        "source:data.source||sourceFrom()",
        "attribution:data.attribution||attributionFrom()",
        "sourcePath:'offer_to_checkout_to_payment_proof'",
        "source:order.source,attribution:order.attribution",
        "version:'qpv-conversion-ledger-v2-source-attribution'",
        "source:order.source",
        "source ${order.source}",
        "revenueCountedEur:0",
    ]
    for marker in required_checkout_markers:
        require(marker in checkout, f"checkout missing source attribution marker: {marker}")

    rejected_weak_patterns = [
        "source:'checkout'",
        "source:'unknown'",
        "CHECKOUT_DIRECT fallback",
        "revenueCountedEur:19",
        "confirmedRevenueEur:19",
        "paymentStatus:'paid'",
        "fake checkout success",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in offer, f"offer must reject weak attribution/revenue pattern: {pattern}")
        require(pattern not in checkout, f"checkout must reject weak attribution/revenue pattern: {pattern}")

    print("PASS qpv offer checkout attribution regression")
    print("checked: offer carries source into checkout, checkout stores source/attribution in order proof, status/payment/builder links, and 0 EUR conversion events")


if __name__ == "__main__":
    main()
