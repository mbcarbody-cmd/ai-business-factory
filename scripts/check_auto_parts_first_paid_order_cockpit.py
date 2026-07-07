#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "auto-parts-first-paid-order-cockpit.html"
text = page.read_text(encoding="utf-8")

required = [
    "APF first paid order cockpit",
    "PRICE_EUR=29",
    "apfCloseAndFulfillCockpitLedger",
    "apfPaidEventLedger",
    "exact +29 EUR",
    "exactStatementMatchRequired:'+29 EUR'",
    "revenueCountedEur:0",
    "payment_request_ready_not_revenue",
    "blocked_payment_destination",
    "TRUSTED_PAYMENT_HOSTS",
    "stripe.com",
    "revolut.com",
    "paypal.com",
    "looksLikeIban",
    "auto-parts-proof-statement-match.html",
    "auto-parts-verified-paid-router.html",
    "copied request, sent email, page visit, CSV export, proof screenshot, or manual paid claim = 0 EUR",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("APF first paid order cockpit regression failed; missing: " + ", ".join(missing))

for weak in ["summary", "staffing plan", "policy", "idea list", "audit"]:
    if weak in text.lower() and "0 EUR" not in text:
        raise SystemExit(f"weak pattern is not explicitly revenue-blocked: {weak}")

print("APF first paid order cockpit regression passed")
