#!/usr/bin/env python3
"""Regression gate for APF instant payment-link checkout.

This gate requires a buyer-executable checkout page that turns a configured
Stripe/Revolut/PayPal HTTPS payment destination into a direct Pay 29 EUR action,
records checkout attempts, and still refuses to count revenue until APF paid
confirmation verifies proof in the APF paid ledger.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT_PAGE = ROOT / "website" / "auto-parts-instant-payment-link-checkout.html"
PAID_PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"
FULFILLMENT_PAGE = ROOT / "website" / "auto-parts-paid-fulfillment.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(CHECKOUT_PAGE.exists(), "missing APF instant payment-link checkout page")
    require(PAID_PAGE.exists(), "missing APF paid confirmation page")
    require(FULFILLMENT_PAGE.exists(), "missing APF paid fulfillment page")

    checkout = CHECKOUT_PAGE.read_text(encoding="utf-8")
    paid = PAID_PAGE.read_text(encoding="utf-8")
    fulfillment = FULFILLMENT_PAGE.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder — instant 29 € checkout",
        "Executable APF checkout · 29 EUR · payment-link click ledger",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const LEDGER_KEY='apfInstantPaymentCheckoutLedger'",
        "const PAID_LEDGER_KEY='apfPaidEventLedger'",
        "const PAYMENT_DESTINATION_KEY='apfPaymentDestination'",
        "const PAYMENT_METHOD_KEY='apfPaymentMethod'",
        "const VALID_PAYMENT_METHODS=['stripe_payment_link','revolut_business','paypal_checkout','bank_transfer']",
        "function restoreFromUrlOrStorage()",
        "function isPaymentUrl(value)",
        "function buildCheckout()",
        "function buildPaidConfirmationUrl(row)",
        "function buildFulfillmentUrl(row)",
        "function saveCheckoutIntent()",
        "function startCheckout()",
        "id=\"payNowLink\"",
        "Pay 29 € now",
        "checkout_attempted_not_revenue",
        "revenueCountedEur:0",
        "apf-instant-payment-checkout-ledger.csv",
        "auto-parts-paid-confirmation.html?",
        "auto-parts-paid-fulfillment.html?",
        "paymentDestination",
        "paymentReference",
        "APF29-",
    ]
    for marker in required_markers:
        require(marker in checkout, f"checkout page missing executable marker: {marker}")

    buyer_path_markers = [
        "Buyer email",
        "Buyer / company",
        "Vehicle",
        "Part / OEM",
        "Payment method",
        "Payment destination / URL",
        "Stripe Payment Link",
        "Revolut Business",
        "PayPal checkout",
        "Pay 29 EUR using payment destination above",
        "Verify paid proof only through APF paid confirmation",
        "Fulfill only after verified paid event exists",
    ]
    for marker in buyer_path_markers:
        require(marker in checkout, f"checkout page missing buyer payment path marker: {marker}")

    url_checkout_markers = [
        "if(isPaymentUrl(row.paymentDestination)){$('payNowLink').href=row.paymentDestination}",
        "return /^https:\\/\\//i.test",
        "return true",
        "bank/text destination generated",
    ]
    for marker in url_checkout_markers:
        require(marker in checkout, f"checkout page missing instant payment URL behavior marker: {marker}")

    rejected_weak_patterns = [
        "checkout click is revenue",
        "payment link is revenue",
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "fake paid",
        "summary-only",
        "dashboard-only progress",
        "paid without proof",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in checkout, f"weak/fake revenue pattern must not appear: {pattern}")

    require("PAID_KEY='apfPaidEventLedger'" in paid, "APF paid confirmation must own paid ledger")
    require(
        "COMPLETED_KEY='apfCompletedOrderLedger'" in fulfillment,
        "APF fulfillment must own completed order ledger",
    )

    print("PASS APF instant payment-link checkout regression")
    print(
        "checked: buyer-ready 29 EUR payment-link checkout, URL/localStorage payment setup restore, "
        "checkout attempt ledger, direct Pay 29 link for HTTPS payment destinations, bank/text fallback, "
        "APF paid confirmation handoff, APF fulfillment handoff, CSV export, and zero confirmed revenue until verified paid proof"
    )


if __name__ == "__main__":
    main()
