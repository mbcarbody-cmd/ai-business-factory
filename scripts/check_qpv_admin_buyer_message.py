#!/usr/bin/env python3
"""Regression checks for QPV admin buyer delivery message handoff.

Static gate because connector runtime cannot launch a browser. It rejects summary-only
work and weak revenue patterns: buyer messages must be generated from the real local
ledger, include a buyer status URL, preserve the payment-ledger route, and keep
proof-submitted revenue at 0 EUR until manual paid/delivered confirmation.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMIN = ROOT / "website" / "order-admin.html"
html = ADMIN.read_text(encoding="utf-8")

required_patterns = {
    "buyer delivery message panel": "Buyer delivery message",
    "message DOM target": "id=\"deliveryMessage\"",
    "copy buyer message button": "id=\"copyDeliveryMessage\"",
    "per-order copy buyer message action": "data-action=\"copyDelivery\"",
    "delivery message function": "function deliveryMessage(row)",
    "payment line function": "function paymentLine(row)",
    "fulfillment line function": "function fulfillmentLine(row)",
    "message contains order id": "Order ID: ${row.orderId}",
    "message contains status URL": "Track status here: ${absoluteStatusHref(row.orderId)}",
    "message contains price": "Price: ${Number(row.priceEur||priceEur)} EUR",
    "message keeps unpaid revenue zero": "Confirmed revenue counted now: ${isPaid(row)?Number(row.priceEur||priceEur):0} EUR",
    "selected JSON exports message": "buyerDeliveryMessage:deliveryMessage(focus)",
    "copy handler writes message": "navigator.clipboard.writeText(text)",
    "payment proof path remains ledger synced": "./payment-ledger.html",
    "proof revenue remains zero": "proofSubmittedRevenueEur:0",
}

for name, needle in required_patterns.items():
    if needle not in html:
        raise SystemExit(f"FAIL missing {name}: {needle}")

rejected_patterns = {
    "summary-only placeholder": "TODO buyer message",
    "fake paid on proof": "proof_submitted counts 19 EUR",
    "fake proof revenue": "proofSubmittedRevenueEur:19",
    "legacy proof page route": "href=\"./payment.html\"",
    "message without order status link": "Track status here: ./order-status.html\n",
}

for name, needle in rejected_patterns.items():
    if needle in html:
        raise SystemExit(f"FAIL rejected weak pattern present: {name}: {needle}")

if "deliveryMessage(focus)" not in html or "deliveryMessage(row)" not in html:
    raise SystemExit("FAIL buyer message must be generated from selected ledger row")

if "payment_pending counts 0 EUR" not in html or "proof_submitted counts 0 EUR" not in html:
    raise SystemExit("FAIL revenue gate rules must remain visible in admin QA")

print("PASS qpv admin buyer delivery message regression")
