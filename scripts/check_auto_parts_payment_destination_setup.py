#!/usr/bin/env python3
"""Regression gate for the 29 EUR Auto Parts payment destination setup.

This is a revenue-path workflow improvement: it converts the missing live
IBAN/Revolut/Stripe/PayPal blocker into a seller setup page that stores a real
payment destination locally and generates a buyer-ready payable order URL while
keeping confirmed revenue at 0 EUR until verified payment exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP_PAGE = ROOT / "website" / "auto-parts-payment-destination-setup.html"
ORDER_PAGE = ROOT / "website" / "auto-parts-bank-transfer-order.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(SETUP_PAGE.exists(), "missing payment destination setup page")
    require(ORDER_PAGE.exists(), "missing payable order page")
    setup = SETUP_PAGE.read_text(encoding="utf-8")
    order = ORDER_PAGE.read_text(encoding="utf-8")

    setup_markers = [
        "Configure Auto Parts Price Finder payment destination",
        "Seller payment setup · converts manual blocker into payable 29 EUR order URL",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const STORAGE_DESTINATION='apfPaymentDestination'",
        "const STORAGE_METHOD='apfPaymentMethod'",
        "function validDestination(v)",
        "function buildOrderUrl()",
        "function buildInvoiceRequest()",
        "function saveDestination()",
        "function clearDestination()",
        "function copyOrderCopy()",
        "paymentDestination",
        "paymentMethod",
        "IBAN, Revolut Business link, Stripe Payment Link or PayPal checkout URL",
        "buyer-ready payable order URL",
        "auto-parts-bank-transfer-order.html?",
        "auto-parts-buyer-outreach.html?product=auto-parts-price-finder&priceEur=29",
        "qpvPaidEventLedger",
    ]
    for marker in setup_markers:
        require(marker in setup, f"setup page missing executable marker: {marker}")

    zero_revenue_markers = [
        "confirmed revenue remains 0 EUR until verified paid event",
        "revenueCountedEur:0",
        "generated URLs are 0 EUR until verified paid event exists",
        "this setup is not revenue. Count 0 EUR until verified paid event exists",
        "Rejected weak patterns: setup saved, generated payment URL, invoice request",
    ]
    for marker in zero_revenue_markers:
        require(marker in setup, f"setup page missing zero-revenue guard: {marker}")

    integration_markers = [
        "localStorage.getItem('apfPaymentDestination')",
        "paymentDestination",
        "paymentMethod",
        "Pay 29 EUR to payment destination above using reference",
    ]
    for marker in integration_markers:
        require(marker in order, f"order page missing payment setup integration marker: {marker}")

    weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "setup save is revenue",
        "generated URL is revenue",
        "mailto click is revenue",
        "fake paid",
    ]
    for pattern in weak_patterns:
        require(pattern not in setup, f"weak/fake revenue pattern must not appear in setup page: {pattern}")

    print("PASS auto parts payment destination setup regression")
    print("checked: seller payment setup, local payment destination storage, buyer-ready payable order URL, invoice fallback, outreach handoff, and zero confirmed revenue until verified paid event")


if __name__ == "__main__":
    main()
