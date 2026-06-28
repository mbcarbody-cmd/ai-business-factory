#!/usr/bin/env python3
"""Static regression checks for QPV offer -> checkout handoff.

This gate prevents a buyer-facing offer from producing a checkout URL that the
checkout page rejects. It only accepts executable product-state movement:
versioned leadId generation, checkout URL propagation, and zero-EUR revenue
until manual paid verification.
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
        "Generate checkout-ready lead",
        "Continue to checkout with leadId",
        "function leadId(){return `LP-${compactStamp()}",
        "leadId:data.leadId",
        "checkoutHref(data)",
        "Checkout link: ${checkoutHref(data)}",
        "checkout_handoff_ready",
        "revenueCountedEur:0",
        "confirmed revenue remains 0 EUR until manual paid verification",
        "checkout.html receives leadId and creates payment_pending order",
    ]
    for marker in required_offer_markers:
        require(marker in offer, f"offer checkout handoff missing marker: {marker}")

    require("validLeadId(data.leadId)" in checkout, "checkout must reject missing/invalid leadId")
    require("LP-\\d{4,}" in checkout, "checkout must accept LP leadId format from offer")
    require("paymentStatus:'payment_pending'" in checkout, "checkout must create payment-pending order only")
    require("revenueCountedEur:0" in checkout, "checkout must not count revenue at handoff")

    href_body = re.search(r"function checkoutHref\(data\)\{(.+?)\}\nfunction buildMailto", offer, re.S)
    require(href_body is not None, "offer must define executable checkoutHref(data)")
    require("leadId:data.leadId" in href_body.group(1), "checkoutHref must propagate leadId")
    require("./checkout.html?" in href_body.group(1), "checkoutHref must route to checkout page")

    rejected_weak_patterns = [
        "checkoutHref(data){const p=new URLSearchParams({brand:data.brand",
        "status:'paid'",
        "paymentStatus:'paid'",
        "revenueCountedEur:19",
        "confirmedRevenueEur:19",
        "fake checkout success",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in offer, f"offer must reject weak checkout pattern: {pattern}")

    print("PASS qpv offer checkout handoff regression")
    print("checked: offer creates leadId, checkout URL carries leadId, checkout remains payment-pending and 0 EUR until verified paid event")


if __name__ == "__main__":
    main()
