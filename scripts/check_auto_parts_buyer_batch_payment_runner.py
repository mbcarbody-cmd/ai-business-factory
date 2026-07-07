#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "auto-parts-buyer-batch-payment-runner.html"
text = page.read_text(encoding="utf-8")

required = [
    "APF buyer batch payment runner",
    "PRICE_EUR=29",
    "apfBuyerBatchPaymentRunLedger",
    "apfBuyerBatchPaymentRunBlocks",
    "apfPaidEventLedger",
    "exact +29 EUR",
    "revenueCountedEur:0",
    "outreach-ready rows are not revenue",
    "TRUSTED_PAYMENT_HOSTS",
    "stripe.com",
    "revolut.com",
    "paypal.com",
    "looksLikeIbanInstruction",
    "trustedPaymentDestination",
    "weakPattern",
    "payment_ready_outreach_row",
    "orderUrl",
    "statementMatchUrl",
    "mailtoLink",
    "whatsappLink",
    "auto-parts-paid-order-link-generator.html",
    "auto-parts-bank-statement-import.html",
    "generated row, copied message, mailto/WhatsApp click, CSV export, checkout visit, payment promise, screenshot, or manual paid claim = 0 EUR",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("APF buyer batch payment runner regression failed; missing: " + ", ".join(missing))

blocked_patterns = ["demo", "test", "example", "fake", "placeholder", "buyer@example.com"]
for pattern in blocked_patterns:
    if pattern not in text.lower():
        raise SystemExit(f"APF buyer batch runner does not block weak pattern: {pattern}")

for weak in ["summary", "staffing plan", "policy", "idea list", "audit"]:
    if weak not in text.lower():
        raise SystemExit(f"APF buyer batch runner must explicitly reject weak pattern: {weak}")

if "confirmedRevenue" not in text or "revenueCountedEur:0" not in text:
    raise SystemExit("APF buyer batch runner must keep generated outreach rows at 0 EUR")

if "slice(0,20)" not in text:
    raise SystemExit("APF buyer batch runner must cap one run to 20 actionable buyer rows")

print("APF buyer batch payment runner regression passed")
