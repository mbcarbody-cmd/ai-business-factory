#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "auto-parts-paid-order-link-generator.html"
text = page.read_text(encoding="utf-8")

required = [
    "APF paid order link generator",
    "PRICE_EUR=29",
    "apfPaidOrderLinkLedger",
    "apfPaidEventLedger",
    "exact +29 EUR",
    "exactStatementMatchRequired:'+29 EUR'",
    "revenueCountedEur:0",
    "order_link_generated_not_revenue",
    "duplicate_order_link_not_revenue",
    "TRUSTED_PAYMENT_HOSTS",
    "stripe.com",
    "revolut.com",
    "paypal.com",
    "looksLikeIban",
    "buyerStatus",
    "productionDestinationStatus",
    "auto-parts-bank-transfer-order.html",
    "auto-parts-instant-payment-link-checkout.html",
    "auto-parts-payment-proof-handoff.html",
    "auto-parts-proof-statement-match.html",
    "auto-parts-verified-paid-router.html",
    "generated order link, copied message, email, WhatsApp, page visit, checkout attempt, proof screenshot or manual paid claim = 0 EUR",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("APF paid order link generator regression failed; missing: " + ", ".join(missing))

blocked_patterns = ["demo", "test", "example", "fake", "placeholder", "buyer@example.com"]
for pattern in blocked_patterns:
    if pattern not in text.lower():
        raise SystemExit(f"APF paid order link generator does not block weak pattern: {pattern}")

for weak in ["summary", "staffing plan", "policy", "idea list", "audit"]:
    if weak in text.lower() and "Rejected weak patterns" not in text:
        raise SystemExit(f"weak pattern is not explicitly rejected: {weak}")

print("APF paid order link generator regression passed")
