#!/usr/bin/env python3
"""Regression gate for the 29 EUR Auto Parts Price Finder bank-transfer order path.

This is a buyer/payment-path gate, not a dashboard or summary gate. It requires
an executable order form, payment reference, CSV export, paid-confirmation and
fulfillment handoff, while keeping confirmed revenue at 0 EUR until a verified
paid event exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PAGE = ROOT / "website" / "auto-parts-price-finder.html"
ORDER_PAGE = ROOT / "website" / "auto-parts-bank-transfer-order.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PRODUCT_PAGE.exists(), "missing Auto Parts Price Finder product page")
    require(ORDER_PAGE.exists(), "missing bank-transfer order page")
    product = PRODUCT_PAGE.read_text(encoding="utf-8")
    order = ORDER_PAGE.read_text(encoding="utf-8")

    product_markers = [
        "auto-parts-bank-transfer-order.html?product=auto-parts-price-finder&priceEur=29",
        "Paid confirmation",
        "bank-transfer order intent as revenue",
        "Payment path: auto-parts-bank-transfer-order.html?product=${PRODUCT}&priceEur=${PRICE_EUR}",
    ]
    for marker in product_markers:
        require(marker in product, f"product page missing bank-transfer handoff marker: {marker}")

    order_markers = [
        "Buy Auto Parts Price Finder audit — 29 €",
        "Executable revenue path · 29 EUR · bank-transfer order capture",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const SELLER='MB Marių auto'",
        "const CONTACT_EMAIL='automariu@gmail.com'",
        "const STORAGE_KEY='apfBankTransferOrders'",
        "function createOrder()",
        "function exportOrders()",
        "paymentReference",
        "APF29-",
        "status:'awaiting_verified_bank_transfer'",
        "revenueCountedEur:0",
        "paid-confirmation.html?",
        "paid-fulfillment.html?",
        "auto-parts-bank-transfer-orders.csv",
        "qpvPaidEventLedger",
    ]
    for marker in order_markers:
        require(marker in order, f"order page missing executable marker: {marker}")

    buyer_path_markers = [
        "Buyer email",
        "Buyer / company",
        "Vehicle",
        "Part",
        "OEM / codes",
        "Create 29 € order",
        "Pay 29 EUR by bank transfer using reference",
        "Email payment proof + order ID",
        "Fulfillment unlocks only after verified paid event",
    ]
    for marker in buyer_path_markers:
        require(marker in order, f"order page missing buyer path marker: {marker}")

    rejected_weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "order rows are revenue",
        "payment reference is revenue",
        "proof text is revenue",
        "dashboard-only progress",
        "summary-only",
        "fake paid",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in order, f"weak/fake revenue pattern must not appear in order page: {pattern}")

    print("PASS auto parts bank-transfer order regression")
    print("checked: 29 EUR buyer order form, payment reference, proof instructions, paid-confirmation/fulfillment handoff, CSV export, and zero confirmed revenue until verified paid event")


if __name__ == "__main__":
    main()
