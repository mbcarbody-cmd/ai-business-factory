#!/usr/bin/env python3
"""Regression checks for QPV admin buyer-status handoff.

This is intentionally static because the GitHub connector cannot execute a browser.
It rejects weak revenue-autopilot patterns that create UI text without connecting
orders to the actual buyer status/payment ledger flow.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMIN = ROOT / "website" / "order-admin.html"

html = ADMIN.read_text(encoding="utf-8")

required_patterns = {
    "ledger synced payment proof route": "href=\"./payment-ledger.html\"",
    "buyer status URL helper": "function statusHref(orderId)",
    "absolute buyer status URL": "function absoluteStatusHref(orderId)",
    "copy status button per order": "data-action=\"copyStatus\"",
    "open status link per order": "Open status",
    "status URL in selected JSON": "buyerStatusUrl",
    "copy status handler": "copyStatusLink(el.dataset.id)",
    "no fake proof revenue": "proofSubmittedRevenueEur:0",
    "confirmed revenue remains gated": "confirmedRevenueEur:revenue(rows)",
}

for name, needle in required_patterns.items():
    if needle not in html:
        raise SystemExit(f"FAIL missing {name}: {needle}")

rejected_patterns = {
    "legacy payment proof route": "href=\"./payment.html\"",
    "fake paid on proof": "paymentStatus='paid'",
    "fake 19 EUR proof revenue": "proofSubmittedRevenueEur:19",
    "status page without order id": "./order-status.html\" target",
}

for name, needle in rejected_patterns.items():
    if needle in html:
        raise SystemExit(f"FAIL rejected weak pattern present: {name}: {needle}")

if "order-status.html?" not in html or "new URLSearchParams({orderId})" not in html:
    raise SystemExit("FAIL buyer status link must include orderId query param")

if "navigator.clipboard.writeText(href)" not in html:
    raise SystemExit("FAIL copy button must copy the real absolute buyer status URL")

print("PASS qpv admin buyer-status handoff regression")
