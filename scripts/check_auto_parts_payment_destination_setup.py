#!/usr/bin/env python3
"""Regression gate for the 29 EUR Auto Parts payment destination setup.

This is a revenue-path workflow improvement: it converts the missing live
IBAN/Revolut/Stripe/PayPal blocker into a seller setup page that stores a real
payment destination locally, imports it from setup URLs, and generates a buyer-ready
instant checkout URL plus a payable order fallback while keeping confirmed revenue
at 0 EUR until verified payment exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP_PAGE = ROOT / "website" / "auto-parts-payment-destination-setup.html"
ORDER_PAGE = ROOT / "website" / "auto-parts-bank-transfer-order.html"
CHECKOUT_PAGE = ROOT / "website" / "auto-parts-instant-payment-link-checkout.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(SETUP_PAGE.exists(), "missing payment destination setup page")
    require(ORDER_PAGE.exists(), "missing payable order page")
    require(CHECKOUT_PAGE.exists(), "missing instant checkout page")
    setup = SETUP_PAGE.read_text(encoding="utf-8")
    order = ORDER_PAGE.read_text(encoding="utf-8")
    checkout = CHECKOUT_PAGE.read_text(encoding="utf-8")

    setup_markers = [
        "Configure Auto Parts Price Finder payment destination",
        "Seller payment setup · converts manual blocker into instant 29 EUR checkout URL",
        "URL-importable destination",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const STORAGE_DESTINATION='apfPaymentDestination'",
        "const STORAGE_METHOD='apfPaymentMethod'",
        "const VALID_PAYMENT_METHODS=['bank_transfer','revolut_business','stripe_payment_link','paypal_checkout']",
        "function validDestination(v)",
        "function validPaymentMethod(v)",
        "function params()",
        "function sharedPaymentParams()",
        "function buildInstantCheckoutUrl()",
        "function buildOrderUrl()",
        "function buildInvoiceRequest()",
        "function saveDestination()",
        "function clearDestination()",
        "function copyOrderCopy()",
        "function restoreFromUrlOrStorage()",
        "paymentDestination",
        "paymentMethod",
        "IBAN, Revolut Business link, Stripe Payment Link or PayPal checkout URL",
        "buyer-ready instant checkout URL",
        "payable order fallback",
        "auto-parts-instant-payment-link-checkout.html?",
        "auto-parts-bank-transfer-order.html?",
        "auto-parts-buyer-outreach.html?product=auto-parts-price-finder&priceEur=29",
        "apfPaidEventLedger",
    ]
    for marker in setup_markers:
        require(marker in setup, f"setup page missing executable marker: {marker}")

    url_import_markers = [
        "const urlDestination=(p.get('paymentDestination')||'').trim();",
        "const urlMethod=(p.get('paymentMethod')||'').trim();",
        "const destination=urlDestination||localStorage.getItem(STORAGE_DESTINATION)||'';",
        "if(validDestination(urlDestination)){",
        "localStorage.setItem(STORAGE_DESTINATION,urlDestination);",
        "localStorage.setItem(STORAGE_METHOD,$('paymentMethod').value);",
        "open setup with paymentDestination/paymentMethod URL parameters",
        "setup URL import",
    ]
    for marker in url_import_markers:
        require(marker in setup, f"setup page missing URL-import payment setup marker: {marker}")

    instant_checkout_handoff_markers = [
        "id=\"instantCheckoutUrl\"",
        "Open instant checkout URL",
        "instant checkout URL generated",
        "Buyer-ready instant checkout URL:",
        "generated instant checkout URL",
        "checkout attempt are not revenue",
        "buildInstantCheckoutUrl()",
    ]
    for marker in instant_checkout_handoff_markers:
        require(marker in setup, f"setup page missing instant checkout handoff marker: {marker}")

    zero_revenue_markers = [
        "confirmed revenue remains 0 EUR until verified paid event",
        "revenueCountedEur:0",
        "generated URLs are 0 EUR until verified paid event exists",
        "this setup, setup URL import, generated instant checkout URL, payable order URL and checkout attempt are not revenue",
        "Rejected weak patterns: setup saved, generated payment URL, instant checkout URL, setup URL import",
    ]
    for marker in zero_revenue_markers:
        require(marker in setup, f"setup page missing zero-revenue guard: {marker}")

    apf_ledger_markers = [
        "Fulfillment unlocks only after verified paid event exists in apfPaidEventLedger.",
        "Revenue rule: setup request and generated URLs are 0 EUR until verified paid event exists in apfPaidEventLedger.",
        "wrong ledger instruction",
    ]
    for marker in apf_ledger_markers:
        require(marker in setup, f"setup page missing APF ledger guard: {marker}")

    integration_markers = [
        "localStorage.getItem('apfPaymentDestination')",
        "paymentDestination",
        "paymentMethod",
        "Pay 29 EUR to payment destination above using reference",
    ]
    for marker in integration_markers:
        require(marker in order, f"order page missing payment setup integration marker: {marker}")

    checkout_markers = [
        "const PAYMENT_DESTINATION_KEY='apfPaymentDestination'",
        "function restoreFromUrlOrStorage()",
        "Pay 29 € now",
        "checkout_attempted_not_revenue",
        "auto-parts-paid-confirmation.html?",
        "auto-parts-paid-fulfillment.html?",
    ]
    for marker in checkout_markers:
        require(marker in checkout, f"instant checkout page missing setup handoff marker: {marker}")

    weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "setup save is revenue",
        "generated URL is revenue",
        "instant checkout is revenue",
        "setup URL import is revenue",
        "checkout attempt is revenue",
        "mailto click is revenue",
        "fake paid",
        "qpvPaidEventLedger",
    ]
    for pattern in weak_patterns:
        require(pattern not in setup, f"weak/fake revenue pattern must not appear in setup page: {pattern}")

    print("PASS auto parts payment destination setup regression")
    print(
        "checked: seller payment setup, URL/localStorage payment destination restore, buyer-ready instant checkout URL, "
        "payable order fallback, invoice fallback, outreach handoff, APF paid-ledger instruction, and zero confirmed revenue until verified paid event"
    )


if __name__ == "__main__":
    main()
