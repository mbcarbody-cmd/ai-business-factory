#!/usr/bin/env python3
"""Regression gate for QPV leadId propagation through payment proof.

This check rejects the weak pattern where checkout passes leadId to payment-ledger
but proof submission loses it, becomes orphaned from KPI attribution, or counts
manual proof as paid revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYMENT_LEDGER = ROOT / "website" / "payment-ledger.html"
CHECKOUT = ROOT / "website" / "checkout.html"

payment = PAYMENT_LEDGER.read_text(encoding="utf-8")
checkout = CHECKOUT.read_text(encoding="utf-8")

required_payment_patterns = [
    "LEADID TRACKED",
    "conversionKey='qpvConversionLedger'",
    "<label for=\"leadId\">Lead ID</label>",
    "if(p.get('leadId'))$('leadId').value=p.get('leadId')",
    "leadId:data.leadId||'PAYMENT_PROOF_DIRECT'",
    "kpiEvent:'payment_proof_submitted_manual_review'",
    "leadId:proof.leadId",
    "stateFrom:'payment_pending'",
    "stateTo:'proof_submitted_manual_review'",
    "source:'payment-ledger'",
    "revenueEur:0",
    "revenueCountedEur:0",
    "Proof saved for ${lastProof.orderId} with lead ${lastProof.leadId}",
    "conversions:readJson(conversionKey,[])",
]

required_checkout_patterns = [
    "paymentHref(order)",
    "leadId:order.leadId",
    "./payment-ledger.html?${p.toString()}",
]

for pattern in required_payment_patterns:
    if pattern not in payment:
        raise SystemExit(f"FAIL: payment-ledger.html missing leadId proof conversion pattern: {pattern}")

for pattern in required_checkout_patterns:
    if pattern not in checkout:
        raise SystemExit(f"FAIL: checkout.html no longer hands leadId into payment-ledger: {pattern}")

compact_payment = payment.replace(" ", "")
for forbidden in [
    "paymentStatus:'paid'",
    "kpiEvent:'paid'",
    "revenueEur:19",
    "revenueCountedEur:19",
    "stateTo:'paid'",
    "confirmedRevenueEur:19",
]:
    if forbidden in compact_payment:
        raise SystemExit(f"FAIL: payment proof is counting fake paid revenue or skipping manual verification: {forbidden}")

print("PASS: QPV payment proof preserves leadId, writes a revenue-gated conversion event, and keeps manual proof out of confirmed revenue.")
