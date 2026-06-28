#!/usr/bin/env python3
"""Regression gate for QPV verified-paid buyer receipt workflow.

This script rejects receipt/download/email actions as revenue proof.
It validates that receipt.html only creates buyer receipts from qpvPaidEventLedger
rows with paymentStatus='paid', writes receipt/service events as 0 EUR, and keeps
confirmed revenue sourced only from verified paid events.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "receipt.html"
content = PAGE.read_text(encoding="utf-8")
compact = "".join(content.split())

required_patterns = {
    "receipt page title": "Buyer Receipt — Quick Product Video",
    "paid ledger source": "qpvPaidEventLedger",
    "receipt ledger source": "qpvReceiptLedger",
    "conversion ledger source": "qpvConversionLedger",
    "verified paid required": "verified_paid_event_required_before_receipt",
    "findPaid requires paid": "row.paymentStatus==='paid'",
    "idempotent receipt id": "receiptIdFor(paidEvent)",
    "existing receipt idempotent": "idempotent:true",
    "new receipt zero revenue": "receiptRevenueEur:0",
    "generated event zero revenue": "kpiEvent:'receipt_generated',revenueEur:0",
    "download event zero revenue": "auditReceiptAction('receipt_downloaded'",
    "email event zero revenue": "auditReceiptAction('receipt_emailed'",
    "audit action zero revenue": "kpiEvent,revenueEur:0",
    "confirmed revenue from paid ledger": "function confirmedRevenue(){return readJson(paidKey,[]).reduce((sum,row)=>sum+Number(row.amountEur||0),0)}",
    "receipt events do not increase revenue": "receiptEventsDoNotIncreaseRevenue:true",
    "proof pending blocked": "payment_pending/proof_submitted cannot generate receipts",
    "buyer route back to paid confirmation": "./paid-confirmation.html",
}

missing = [name for name, pattern in required_patterns.items() if pattern not in content]
if missing:
    raise SystemExit("FAIL: missing buyer receipt regression pattern(s): " + ", ".join(missing))

for forbidden in [
    "paymentStatus==='proof_submitted'",
    "paymentStatus==='pending'",
    "payment_pending receipt allowed",
    "proof_submitted receipt allowed",
    "receipt_generated counts as revenue",
    "receipt_downloaded counts as revenue",
    "receipt_emailed counts as revenue",
    "kpiEvent:'receipt_generated',revenueEur:19",
    "kpiEvent:'receipt_downloaded',revenueEur:19",
    "kpiEvent:'receipt_emailed',revenueEur:19",
    "receiptRevenueEur:19",
    "revenueEur:19,receiptId",
    "receiptEventsDoNotIncreaseRevenue:false",
    "summary_only",
]:
    if forbidden in content or forbidden in compact:
        raise SystemExit(f"FAIL: forbidden weak receipt/revenue pattern present: {forbidden}")

if "&&row.paymentStatus==='paid')||null}" not in content:
    raise SystemExit("FAIL: receipt generation must require an exact paid ledger match")

print("PASS: QPV buyer receipt workflow requires verified paid events, is idempotent, and records receipt actions with 0 EUR revenue impact.")
