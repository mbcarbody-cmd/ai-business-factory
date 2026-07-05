#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-payment-launch-url-builder.html"

html = PAGE.read_text(encoding="utf-8")

required = [
    "APF 29 € payment launch URL builder",
    "const PRICE_EUR=29;",
    "const LEDGER_KEY='apfPaymentLaunchUrlLedger';",
    "const PAID_LEDGER_KEY='apfPaidEventLedger';",
    "const PRODUCT='auto-parts-price-finder';",
    "const BUYER='used-parts-seller';",
    "const CONTACT_EMAIL='automariu@gmail.com';",
    "function productionDestinationStatus(value)",
    "function isTrustedPaymentUrl(value)",
    "function looksLikeIban(value)",
    "function buildLaunchPack()",
    "function buildPack(row)",
    "function buildBuyerMailto(row)",
    "./auto-parts-instant-payment-link-checkout.html",
    "./auto-parts-buyer-lead-capture.html",
    "./auto-parts-payment-proof-handoff.html",
    "./auto-parts-paid-confirmation.html",
    "./auto-parts-paid-fulfillment.html",
    "paymentDestination:row.paymentDestination",
    "revenueCountedEur:0",
    "confirmed revenue remains 0 EUR",
    "verified paid event exists in ${PAID_LEDGER_KEY}",
]

missing = [needle for needle in required if needle not in html]
if missing:
    raise SystemExit(f"payment launch builder missing required revenue-flow markers: {missing}")

trusted_hosts = [
    "stripe.com",
    "buy.stripe.com",
    "pay.stripe.com",
    "checkout.stripe.com",
    "revolut.com",
    "revolut.me",
    "paypal.com",
    "www.paypal.com",
    "paypal.me",
]
for host in trusted_hosts:
    if host not in html:
        raise SystemExit(f"trusted production payment host missing: {host}")

weak_patterns = [
    "example.com",
    "pay.example",
    "demo",
    "test_checkout",
    "placeholder",
    "fake",
    "localhost",
    "127.0.0.1",
    "unknown HTTPS domain",
    "generated URL",
    "copied pack",
    "mailto click",
    "lead row",
    "checkout click",
    "invoice request",
    "proof text",
    "CSV export",
]
for pattern in weak_patterns:
    if pattern not in html:
        raise SystemExit(f"weak-pattern rejection missing: {pattern}")

# Guard against accidental revenue recognition before paid confirmation.
for forbidden in [
    "revenueCountedEur:PRICE_EUR",
    "revenueCountedEur=PRICE_EUR",
    "revenueCountedEur:29,status:'paid'",
    "status:'paid'",
    "confirmedRevenueEur:29",
]:
    if forbidden in html:
        raise SystemExit(f"payment launch builder must not count revenue directly: {forbidden}")

print("APF payment launch URL builder regression passed")
