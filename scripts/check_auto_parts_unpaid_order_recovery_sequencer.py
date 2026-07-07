#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "auto-parts-unpaid-order-recovery-sequencer.html"
text = page.read_text(encoding="utf-8")

required = [
    "APF unpaid order recovery sequencer",
    "PRICE_EUR=29",
    "apfUnpaidOrderRecoveryLedger",
    "apfPaidEventLedger",
    "exact +29 EUR",
    "revenueCountedEur:0",
    "generated recovery is not revenue",
    "TRUSTED_PAYMENT_HOSTS",
    "stripe.com",
    "revolut.com",
    "paypal.com",
    "looksLikeIbanInstruction",
    "trustedPaymentDestination",
    "weakPattern",
    "recovery_sequence_ready",
    "mailtoLinks",
    "whatsappLinks",
    "auto-parts-paid-order-link-generator.html",
    "auto-parts-bank-statement-import.html",
    "recovery sequence, copied message, mailto click, WhatsApp click, checkout visit, promise to pay, screenshot, CSV export, or manual paid claim = 0 EUR",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("APF unpaid order recovery sequencer regression failed; missing: " + ", ".join(missing))

blocked_patterns = ["demo", "test", "example", "fake", "placeholder", "buyer@example.com"]
for pattern in blocked_patterns:
    if pattern not in text.lower():
        raise SystemExit(f"APF unpaid recovery does not block weak pattern: {pattern}")

for weak in ["summary", "staffing plan", "policy", "idea list", "audit"]:
    if weak not in text.lower():
        raise SystemExit(f"APF unpaid recovery must explicitly reject weak pattern: {weak}")

if "confirmedRevenue" not in text or "orderAlreadyPaid" not in text:
    raise SystemExit("APF unpaid recovery must read paid ledger and avoid duplicate revenue")

print("APF unpaid order recovery sequencer regression passed")
