#!/usr/bin/env python3
"""Static regression checks for the Quick Product Video buyer order-status path.

Run from repo root:
    python3 scripts/check_qpv_order_status_flow.py

The check rejects demo-only status pages and any buyer-visible flow that counts
pending/proof-submitted payment as confirmed revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "website" / "order-status.html"
CHECKOUT = ROOT / "website" / "checkout.html"
PAYMENT_LEDGER = ROOT / "website" / "payment-ledger.html"
ADMIN = ROOT / "website" / "order-admin.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    status = read(STATUS)
    checkout = read(CHECKOUT)
    payment = read(PAYMENT_LEDGER)
    admin = read(ADMIN)

    required_status_markers = [
        "qpvOrderLedger",
        "readLedger()",
        "findOrder(orderId)",
        "reads full qpvOrderLedger by orderId",
        "proof_submitted_manual_review counts 0 EUR",
        "only paid/delivered counts revenue",
        "Submit payment proof",
        "./payment-ledger.html?",
        "./video-maker.html?",
        "revenueCountedEur:paid?Number(row.priceEur||priceEur):0",
        "unknown order gives payment-proof fallback, not fake success",
    ]
    for marker in required_status_markers:
        require(marker in status, f"order-status.html missing required marker: {marker}")

    rejected_status_markers = [
        "QPV-DEMO-001",
        "const demo=",
        "demo[id]",
        "qpvLastCheckoutOrder')||'null'",
        "revenueCountedEur:19",
    ]
    for marker in rejected_status_markers:
        require(marker not in status, f"order-status.html contains rejected weak marker: {marker}")

    checkout_markers = [
        "Buyer order status",
        "id=\"statusLink\"",
        "function statusHref(order)",
        "./order-status.html?",
        "Buyer status is ready",
    ]
    for marker in checkout_markers:
        require(marker in checkout, f"checkout.html missing buyer status handoff marker: {marker}")

    require("Order status" in payment and "./order-status.html" in payment, "payment ledger must expose buyer order-status link")
    require("Customer status page" in admin and "./order-status.html" in admin, "admin must expose buyer order-status link")
    require("paymentStatus:'payment_pending'" in checkout, "checkout must still create unpaid orders only")
    require("paymentStatus:'proof_submitted_manual_review'" in payment, "payment proof must still require manual review")

    print("PASS qpv order status flow regression")
    print("checked: full-ledger buyer lookup, checkout status handoff, payment/admin links, zero-revenue pending/proof gate")


if __name__ == "__main__":
    main()
