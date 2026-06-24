#!/usr/bin/env python3
"""Static regression checks for the Quick Product Video checkout revenue path.

Run from repo root:
    python3 scripts/check_qpv_checkout_flow.py

This intentionally avoids browser automation so it can run in the current static
GitHub Pages repo without npm, Playwright, or external services.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / "website" / "checkout.html"
PAYMENT = ROOT / "website" / "payment.html"
ADMIN = ROOT / "website" / "order-admin.html"
BUILDER = ROOT / "website" / "video-maker.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    checkout = read(CHECKOUT)
    payment = read(PAYMENT)
    admin = read(ADMIN)
    builder = read(BUILDER)

    required_checkout_markers = [
        "Create payment-pending order",
        "qpvOrderLedger",
        "qpvLastCheckoutOrder",
        "paymentStatus:'payment_pending'",
        "fulfillmentStatus:'lead'",
        "revenueCountedEur:0",
        "confirmedRevenue(rows)",
        "./payment.html?",
        "./video-maker.html?",
        "Download order JSON",
        "Revenue gate:",
    ]
    for marker in required_checkout_markers:
        require(marker in checkout, f"checkout.html missing required marker: {marker}")

    required_ids = [
        "checkoutForm",
        "brand",
        "contact",
        "productName",
        "ctaText",
        "photoCount",
        "paymentLink",
        "builderLink",
        "proof",
    ]
    for element_id in required_ids:
        require(f'id="{element_id}"' in checkout, f"checkout UI missing id={element_id}")

    require("priceEur=19" in checkout, "checkout price must stay at 19 EUR")
    require("photoCount") and require("min=\"1\"" in checkout and "max=\"12\"" in checkout, "photo count must be constrained to 1-12")
    require("payment_pending" in admin and "proof_submitted" in admin and "paid" in admin, "admin must support payment status gate")
    require("confirmedRevenueEur" in admin, "admin must expose confirmed revenue evidence")
    require("revenueCountedEur:0" in payment, "payment proof must not count revenue before manual verification")
    require("__QPV_ORDER_PREFILL__" in builder and "orderId" in builder, "builder must support checkout order handoff prefill")

    order_id_pattern = re.search(r"QPV-\$\{stamp\}-\$\{Math\.random\(\)\.toString\(36\)\.slice\(2,6\)\.toUpperCase\(\)\}", checkout)
    require(order_id_pattern is not None, "checkout must create QPV order IDs with timestamp and random suffix")

    print("PASS qpv checkout flow regression")
    print("checked: checkout UI, local ledger, payment proof gate, admin revenue gate, builder prefill")


if __name__ == "__main__":
    main()
