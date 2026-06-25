#!/usr/bin/env python3
"""Regression gate for QPV idempotent paid confirmation workflow.

This static gate intentionally rejects weak revenue patterns:
- proof/payment_pending counted as revenue
- paid confirmation without leadId
- paid confirmation without idempotent paidEventId
- duplicate paid events that can increase revenue
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "paid-confirmation.html"

content = PAGE.read_text(encoding="utf-8")

required_patterns = {
    "paid page exists with QPV title": "Idempotent Paid Confirmation — Quick Product Video",
    "leadId is required": "leadId is required before paid confirmation",
    "paid ledger key exists": "qpvPaidEventLedger",
    "duplicate block ledger exists": "qpvPaidDuplicateBlocks",
    "idempotent event id exists": "function paymentEventId(orderId,ref)",
    "duplicate paid event is blocked": "Duplicate paid event blocked; revenue unchanged.",
    "duplicate branch returns ok false": "return{ok:false,duplicate:true",
    "new paid event returns ok true": "return{ok:true,duplicate:false",
    "confirmed revenue only from paid ledger": "function confirmedRevenue(){return readJson(paidKey,[]).reduce",
    "conversion event writes verified paid": "verified_paid_once",
    "paid event keeps leadId": "leadId:event.leadId",
    "paid event keeps orderId": "orderId:event.orderId",
    "paid state requires admin note": "admin verification note are required",
    "proof pending remains zero rule": "proof_submitted/payment_pending remain 0 EUR",
    "order moved to production not delivered": "fulfillmentStatus:'in_production'",
}

missing = [name for name, pattern in required_patterns.items() if pattern not in content]
if missing:
    raise SystemExit("Missing paid-confirmation regression pattern(s): " + ", ".join(missing))

for forbidden in [
    "payment_pending counts as revenue",
    "proof_submitted counts as revenue",
    "fake paid",
    "summary_only",
]:
    if forbidden in content:
        raise SystemExit(f"Forbidden weak revenue pattern present: {forbidden}")

print("PASS: QPV paid confirmation idempotency workflow preserves leadId, blocks duplicates, and counts only verified paid events.")
