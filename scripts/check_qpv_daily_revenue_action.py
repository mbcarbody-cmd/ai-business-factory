#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "daily-revenue-action.html"
text = page.read_text(encoding="utf-8")

required = [
    "qpvOrderLedger",
    "qpvPaidEventLedger",
    "qpvOutreachLeadLedger",
    "isProofReadyUnpaid",
    "paymentReference(row)",
    "paidEventId(row)",
    "Download daily action CSV",
    "payment proof is not revenue",
    "revenueDeltaFromThisPageEur:0",
    "duplicate paid references are deduplicated by orderId + reference",
    "./paid-confirmation.html?",
    "./checkout.html?",
]
missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("daily revenue action cockpit missing required gates: " + ", ".join(missing))

for forbidden in [
    "localStorage.setItem(paidKey",
    "localStorage.setItem('qpvPaidEventLedger'",
    "paymentStatus='paid'",
    'paymentStatus="paid"',
    "revenueEur:19",
    "revenueEur: priceEur",
]:
    if forbidden in text:
        raise SystemExit("daily revenue action cockpit has forbidden fake-revenue side effect: " + forbidden)

if text.count("revenueEur:0") < 2:
    raise SystemExit("daily revenue action cockpit must keep exported action rows at 0 EUR revenue")

print("PASS: daily revenue action cockpit exposes proof-ready and outreach actions without writing fake paid revenue")
