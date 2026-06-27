#!/usr/bin/env python3
"""Regression gate for QPV leadId propagation through checkout.

This check rejects the weak pattern where checkout creates a payment session
without a persistent leadId/orderId/paymentReference handoff. It also rejects
fake revenue from payment_pending checkout or lead handoff events.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / "website" / "checkout.html"
LEAD_SEND = ROOT / "website" / "lead-send.html"

checkout = CHECKOUT.read_text(encoding="utf-8")
lead_send = LEAD_SEND.read_text(encoding="utf-8")

required_checkout_patterns = [
    "conversionKey='qpvConversionLedger'",
    '<label for="leadId">Lead ID required before payment</label>',
    "function validLeadId(value)",
    "Valid leadId is required before checkout can create a payment session.",
    "function leadIdFrom(data)",
    "paymentReferenceFor(newOrderId,leadId)",
    "paymentReference",
    "handoffValidated:true",
    "kpiEvent:'lead_payment_handoff_validated'",
    "kpiEvent:'payment_pending_order_created'",
    "stateFrom:'lead_capture'",
    "stateFrom:'checkout_handoff'",
    "stateTo:'payment_pending'",
    "writeConversionEvent({leadId:order.leadId,orderId:order.orderId,paymentReference:order.paymentReference",
    "idempotencyKey:key",
    "function brokenHandoffRows(rows=readLedger())",
    "Broken handoffs",
    "repair leadId/orderId/paymentReference before payment follow-up",
    "revenueEur:0",
    "Revenue remains 0 EUR until manual paid confirmation",
    "no CHECKOUT_DIRECT fallback",
]

required_lead_patterns = [
    "Lead ${data.leadId} from Lead Send Helper",
    "checkout_url_created_not_paid",
    "revenueEur:0",
]

for pattern in required_checkout_patterns:
    if pattern not in checkout:
        raise SystemExit(f"FAIL: checkout.html missing lead/payment handoff validation pattern: {pattern}")

for pattern in required_lead_patterns:
    if pattern not in lead_send:
        raise SystemExit(f"FAIL: lead-send.html missing source handoff pattern: {pattern}")

compact_checkout = checkout.replace(" ", "")
for forbidden in [
    "CHECKOUT_DIRECT",
    "paymentStatus:'paid'",
    "kpiEvent:'paid'",
    "revenueEur:19",
    "revenueCountedEur:19",
    "stateTo:'paid'",
    "lead_payment_handoff_validated',stateFrom:'lead_capture',stateTo:'paid'",
]:
    if forbidden in compact_checkout:
        raise SystemExit(f"FAIL: checkout is counting fake revenue or allowing invalid handoff: {forbidden}")

print("PASS: QPV checkout requires leadId before payment handoff, preserves orderId/paymentReference, shows broken handoffs, and keeps handoff/payment_pending events at 0 EUR.")
