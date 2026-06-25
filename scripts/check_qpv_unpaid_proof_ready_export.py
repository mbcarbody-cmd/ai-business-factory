#!/usr/bin/env python3
"""Static regression gate for QPV unpaid proof-ready order export."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "order-followup-export.html"

text = PAGE.read_text(encoding="utf-8")

required = [
    "qpvOrderLedger",
    "qpvUnpaidProofReadyExportAudit",
    "function exportable(row)",
    "!isPaid(row)&&hasProof(row)&&clean(row.orderId)&&validLead(row)&&proofReference(row)",
    "revenueCountedEur:0",
    "confirmedRevenueDeltaEur:0",
    "missing leadId exported",
    "missing payment reference exported",
    "proof_submitted counted as revenue",
    "duplicate export creates revenue",
    "paid-confirmation.html",
    "order-status.html",
    "Download follow-up CSV",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("Missing unpaid proof-ready export safeguards: " + ", ".join(missing))

for forbidden in [
    "confirmedRevenueDeltaEur:19",
    "revenueCountedEur:19",
    "paymentStatus='paid'",
    "paymentStatus = 'paid'",
    "localStorage.setItem('qpvPaidEventLedger'",
    "qpvPaidEventLedger",
]:
    if forbidden in text:
        raise SystemExit(f"Forbidden fake-revenue/export side effect found: {forbidden}")

print("PASS qpv unpaid proof-ready export regression")
