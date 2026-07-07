#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "auto-parts-statement-paid-event-matcher.html"
text = page.read_text(encoding="utf-8")

required = [
    "APF statement paid event matcher",
    "PRICE_EUR=29",
    "apfPaidEventLedger",
    "apfStatementPaidEventMatcherBlocks",
    "apfStatementPaidEventMatcherRuns",
    "exact +29 EUR",
    "verified_paid_event",
    "revenueCountedEur:0",
    "manual paid claim = 0 EUR",
    "payment-ready order rows",
    "real statement rows",
    "matchScore",
    "statementReference",
    "fulfillmentUrl",
    "receiptUrl",
    "auto-parts-paid-fulfillment.html",
    "auto-parts-paid-receipt.html",
    "auto-parts-buyer-batch-payment-runner.html",
    "not_exact_real_29_eur_statement_row",
    "no_real_order_match_for_exact_29_eur_statement_row",
    "summary, staffing plan, policy, idea list, audit",
    "checkout visit, promise to pay, proof screenshot, or manual paid claim = 0 EUR",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("APF statement paid event matcher regression failed; missing: " + ", ".join(missing))

for weak in ["demo", "test", "example", "fake", "placeholder", "buyer@example.com"]:
    if weak not in text.lower():
        raise SystemExit(f"APF statement paid event matcher must block weak pattern: {weak}")

for weak in ["summary", "staffing plan", "policy", "idea list", "audit"]:
    if weak not in text.lower():
        raise SystemExit(f"APF statement paid event matcher must explicitly reject weak pattern: {weak}")

if "stmt.amount===PRICE_EUR&&stmt.currency==='EUR'" not in text:
    raise SystemExit("APF statement paid event matcher must require exact 29 EUR statement rows")

if "ranked[0].score<50" not in text:
    raise SystemExit("APF statement paid event matcher must require a real order match score before revenue")

if "existing.has(paidEventId)" not in text:
    raise SystemExit("APF statement paid event matcher must be duplicate-safe")

if "revenueCountedEur:PRICE_EUR" not in text:
    raise SystemExit("APF statement paid event matcher must count revenue only inside verified paid events")

print("APF statement paid event matcher regression passed")
