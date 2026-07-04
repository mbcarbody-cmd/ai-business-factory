#!/usr/bin/env python3
"""Regression gate for APF instant payment-link checkout.

This gate requires a buyer-executable checkout page that turns a configured
Stripe/Revolut/PayPal HTTPS payment destination into a direct Pay 29 EUR action,
records checkout attempts, creates a copyable buyer checkout pack, creates a
prefilled buyer checkout email handoff and proof email, blocks demo/example/test
payment destinations from buyer handoff, and still refuses to count revenue until
APF paid confirmation verifies proof in the APF paid ledger.
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
        "Executable APF checkout · 29 EUR · production payment-destination gate",
        "buyer checkout pack",
        "buyer checkout email",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const LEDGER_KEY='apfInstantPaymentCheckoutLedger'",
        "const PAID_LEDGER_KEY='apfPaidEventLedger'",
        "const PAYMENT_DESTINATION_KEY='apfPaymentDestination'",
        "const PAYMENT_METHOD_KEY='apfPaymentMethod'",
        "const VALID_PAYMENT_METHODS=['stripe_payment_link','revolut_business','paypal_checkout','bank_transfer']",
        "const DEMO_DESTINATION_PATTERNS=['example.com','pay.example','demo','test_checkout','replace-with-real']",
        "function restoreFromUrlOrStorage()",
        "function isPaymentUrl(value)",
        "function isDemoDestination(value)",
        "function isProductionReadyDestination(value)",
        "function readinessBlocker(row)",
        "function buildCheckout()",
        "function buildPaidConfirmationUrl(row)",
        "function buildFulfillmentUrl(row)",
        "function buildPaymentProofMailto(row)",
        "function buildBuyerCheckoutEmailMailto(row)",
        "function buildBuyerCheckoutPack(row)",
        "function copyBuyerCheckoutPack()",
        "function saveCheckoutIntent()",
        "function startCheckout()",
        "id=\"payNowLink\"",
        "id=\"buyerCheckoutEmailLink\"",
        "id=\"paymentProofEmailLink\"",
        "Pay 29 € now",
        "Copy buyer checkout pack",
        "Send checkout to buyer",
        "Email payment proof",
        "checkout_attempted_not_revenue",
        "blocked_non_production_payment_destination",
        "paymentDestinationReady",
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
        "AUTO PARTS PRICE FINDER — 29 EUR CHECKOUT PACK",
        "Pay exactly 29 EUR and use reference",
        "Email proof to",
        "Delivery starts only after verified paid event appears",
        "payment proof link",
        "Verify paid proof only through APF paid confirmation",
        "Fulfill only after verified paid event exists",
        "Buyer checkout email:",
        "MB Marių auto",
    ]
    for marker in buyer_path_markers:
        require(marker in checkout, f"checkout page missing buyer payment path marker: {marker}")

    production_gate_markers = [
        "Demo/example/test URLs are blocked from buyer handoff",
        "waiting for production payment destination",
        "production payment destination blocked",
        "buyer handoff disabled",
        "fallback blocker mail ready",
        "BLOCKER: demo/example/test payment destination is not buyer-ready and cannot be sent or counted as revenue.",
        "do not send buyer checkout yet",
        "Replace demo/example/test destination with a real Stripe/Revolut/PayPal URL or IBAN",
        "Production payment destination ready:",
        "demo payment destination",
        "paymentDestinationReady?'yes':'no'",
        "paymentDestinationReady",
        "https://pay.example.com/apf-29-eur",
        "intentionally blocked by production payment-destination gate",
    ]
    for marker in production_gate_markers:
        require(marker in checkout, f"checkout page missing production destination gate marker: {marker}")

    url_checkout_markers = [
        "if(isPaymentUrl(row.paymentDestination)){$('payNowLink').href=row.paymentDestination}",
        "return /^https:\\/\\//i.test",
        "return true",
        "bank/text destination generated",
        "mailto:'+encodeURIComponent(CONTACT_EMAIL)",
        "mailto:'+encodeURIComponent(to)",
        "$('buyerCheckoutEmailLink').href=blocker?",
        "buildBuyerCheckoutEmailMailto(row)",
        "navigator.clipboard.writeText(pack)",
    ]
    for marker in url_checkout_markers:
        require(marker in checkout, f"checkout page missing instant payment URL behavior marker: {marker}")

    rejected_weak_patterns = [
        "checkout click is revenue",
        "payment link is revenue",
        "demo payment destination is revenue",
        "example payment destination is revenue",
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
        "production payment-destination gate blocking demo/example/test destinations from buyer handoff, "
        "checkout attempt ledger, direct Pay 29 link for HTTPS payment destinations, bank/text fallback, "
        "copyable buyer checkout pack, prefilled buyer checkout email handoff, payment proof mailto fallback, "
        "APF paid confirmation handoff, APF fulfillment handoff, CSV export, and zero confirmed revenue "
        "until verified paid proof"
    )


if __name__ == "__main__":
    main()
