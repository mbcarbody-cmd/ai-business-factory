#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "quick-video-paid-event-verifier.html"
text = page.read_text(encoding="utf-8")

required = [
    "Quick Product Video paid event verifier",
    "PRICE_EUR=29",
    "quickVideoPaidOrderLeads",
    "quickVideoPaidEventLedger",
    "verified_paid_event",
    "exact +29 EUR",
    "Number(stmt.amount)===PRICE_EUR&&String(stmt.currency||'').toUpperCase()==='EUR'",
    "ranked[0]?.score>=70",
    "existing.has(event.paidEventId)",
    "revenueCountedEur:PRICE_EUR",
    "manual paid claim = 0 EUR",
    "checkout visit",
    "payment proof screenshot",
    "not_exact_real_29_eur_statement_row",
    "no_real_order_match",
    "receiptUrl",
    "fulfillmentUrl",
    "video-maker.html",
    "summary, staffing plan, policy, idea list, audit",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("QPV paid event verifier regression failed; missing: " + ", ".join(missing))

for weak in ["demo", "test", "example", "fake", "placeholder", "buyer@example.com"]:
    if weak not in text.lower():
        raise SystemExit(f"QPV paid event verifier must block weak pattern: {weak}")

for weak in ["summary", "staffing plan", "policy", "idea list", "audit"]:
    if weak not in text.lower():
        raise SystemExit(f"QPV paid event verifier must explicitly reject weak progress pattern: {weak}")

if "DUPLICATE_BLOCKED" not in text:
    raise SystemExit("QPV paid event verifier must reject duplicate paid events")

if "$('revenue').textContent=String(PRICE_EUR)" not in text:
    raise SystemExit("QPV paid event verifier must count revenue only after verified event")

print("QPV paid event verifier regression passed")
