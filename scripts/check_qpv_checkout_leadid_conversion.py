#!/usr/bin/env python3
"""Regression gate for QPV leadId propagation through checkout.

This check rejects the weak pattern where a lead handoff opens checkout but
checkout creates an order with no leadId and no measurable conversion event.
It also rejects fake revenue from payment_pending checkout state.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / "website" / "checkout.html"
LEAD_SEND = ROOT / "website" / "lead-send.html"

checkout = CHECKOUT.read_text(encoding="utf-8")
lead_send = LEAD_SEND.read_text(encoding="utf-8")

required_checkout_patterns = [
    "conversionKey='qpvConversionLedger'",
    "function leadIdFrom(data)",
    "params().get('leadId')",
    "match=clean(data.notes).match(/Lead\\s+(LP-\\d{4}|MANUAL)/i)",
    "leadId,product:'Quick Product Video'",
    "kpiEvent:'payment_pending_order_created'",
    "stateFrom:'checkout_handoff'",
    "stateTo:'payment_pending'",
    "writeConversionEvent({leadId:order.leadId,orderId:order.orderId",
    "revenueEur:0",
    "Revenue remains 0 EUR until manual paid confirmation",
]

required_lead_patterns = [
    "Lead ${data.leadId} from Lead Send Helper",
    "checkout_url_created_not_paid",
    "revenueEur:0",
]

for pattern in required_checkout_patterns:
    if pattern not in checkout:
        raise SystemExit(f"FAIL: checkout.html missing leadId conversion tracking pattern: {pattern}")

for pattern in required_lead_patterns:
    if pattern not in lead_send:
        raise SystemExit(f"FAIL: lead-send.html missing source handoff pattern: {pattern}")

compact_checkout = checkout.replace(" ", "")
for forbidden in [
    "paymentStatus:'paid'",
    "kpiEvent:'paid'",
    "revenueEur:19",
    "revenueCountedEur:19",
    "stateTo:'paid'",
]:
    if forbidden in compact_checkout:
        raise SystemExit(f"FAIL: checkout is counting fake paid revenue or skipping payment proof: {forbidden}")

print("PASS: QPV checkout preserves leadId into orders and writes revenue-gated conversion events without counting payment_pending as revenue.")
