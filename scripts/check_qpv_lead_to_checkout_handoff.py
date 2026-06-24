#!/usr/bin/env python3
"""Static regression gate for QPV lead-send -> checkout handoff.

This prevents counting outreach summaries as product progress unless the lead helper
actually creates a prefilled checkout route that can become a payment_pending order.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lead = (ROOT / "website" / "lead-send.html").read_text(encoding="utf-8")
checkout = (ROOT / "website" / "checkout.html").read_text(encoding="utf-8")

required_lead_patterns = [
    "id=\"checkoutLead\"",
    "function checkoutHref(data)",
    "./checkout.html?",
    "brand:data.seller",
    "contact:data.buyerContact||data.channel",
    "product:data.productHint||'Quick Product Video item'",
    "status:'send_ready_not_sent'",
    "pipelineStatus:'Lead'",
    "revenueEur:0",
    "Open prefilled checkout",
]
missing = [pattern for pattern in required_lead_patterns if pattern not in lead]
if missing:
    raise SystemExit(f"lead-send checkout handoff regression failed; missing: {missing}")

if "fake" in lead.lower() and "NO FAKE SENDING" not in lead:
    raise SystemExit("fake pattern detected without explicit rejection copy")

if "revenueEur:19" in lead or "revenueEur: 19" in lead:
    raise SystemExit("outreach helper must not count 19 EUR revenue before verified payment")

required_checkout_patterns = [
    "function fillFromParams()",
    "brand:'brand'",
    "contact:'contact'",
    "product:'productName'",
    "paymentStatus:'payment_pending'",
    "revenueCountedEur:0",
]
missing_checkout = [pattern for pattern in required_checkout_patterns if pattern not in checkout]
if missing_checkout:
    raise SystemExit(f"checkout prefill/order gate regression failed; missing: {missing_checkout}")

print("PASS qpv lead-send -> prefilled checkout handoff keeps revenue at 0 until paid verification")
