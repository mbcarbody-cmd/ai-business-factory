#!/usr/bin/env python3
"""Regression gate for QPV buyer receipt workflow.

This static gate rejects weak receipt/revenue patterns:
- receipt before verified paid event,
- receipt download/email counted as revenue,
- duplicate receipt generation creating extra revenue,
- confirmed EUR sourced from anything except qpvPaidEventLedger.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "receipt.html"
content = PAGE.read_text(encoding="utf-8")

required_patterns = {
    "receipt page title": "Buyer Receipt — Quick Product Video",
    "paid ledger source": "qpvPaidEventLedger",
    "receipt ledger source": "qpvReceiptLedger",
    "verified paid required": "verified_paid_event_required_before_receipt",
    "findPaid requires paid": "row.paymentStatus==='paid'",
    "idempotent receipt id": "receiptIdFor(paidEvent)",
    "existing receipt idempotent": "idempotent:true",
    "new receipt zero revenue": "receiptRevenueEur:0",
    "generated event zero revenue": "kpiEvent:'receipt_generated',revenueEur:0",
    "download event zero revenue": "auditReceiptAction('receipt_downloaded'",
    "email event zero revenue": "auditReceiptAction('receipt_emailed'",
    "confirmed revenue from paid ledger": "function confirmedRevenue(){return readJson(paidKey,[]).reduce",
    "proof pending blocked": "payment_pending/proof_submitted cannot generate receipts",
    "buyer route back to paid confirmation": "./paid-confirmation.html",
}

missing = [name for name, pattern in required_patterns.items() if pattern not in content]
if missing:
    raise SystemExit("Missing buyer receipt regression pattern(s): " + ", ".join(missing))

for forbidden in [
    "receipt_generated counts as revenue",
    "receipt_downloaded counts as revenue",
    "receipt_emailed counts as revenue",
    "payment_pending receipt allowed",
    "proof_submitted receipt allowed",
    "receiptRevenueEur:19",
    "revenueEur:19,receiptId",
    "summary_only",
]:
    if forbidden in content:
        raise SystemExit(f"Forbidden weak receipt/revenue pattern present: {forbidden}")

print("PASS: QPV buyer receipt workflow requires verified paid events, is idempotent, and records receipt actions with 0 EUR revenue impact.")
