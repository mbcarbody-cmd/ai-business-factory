#!/usr/bin/env python3
"""Regression gate for QPV lead -> checkout KPI handoff tracking.

This check rejects the weak pattern where lead-send.html merely creates a
checkout URL but does not persist the handoff into the measurable KPI ledger.
It also rejects fake revenue attribution from outreach or checkout-link events.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAD_SEND = ROOT / "website" / "lead-send.html"
LEAD_KPI = ROOT / "website" / "lead-kpi.html"

lead = LEAD_SEND.read_text(encoding="utf-8")
kpi = LEAD_KPI.read_text(encoding="utf-8")

required_lead_patterns = [
    "const handoffKey='qpvLeadHandoffLedger'",
    "function saveHandoff(proof)",
    "handoffStatus:'checkout_url_created_not_paid'",
    "kpiEvent:'checkout_handoff'",
    "rows.push(handoff)",
    "localStorage.setItem(handoffKey",
    "saveHandoff(result.proof)",
    "Revenue remains 0 EUR until verified paid",
]

required_kpi_patterns = [
    "handoffKey='qpvLeadHandoffLedger'",
    "checkout_handoff",
    "payment_pending",
    "proof_submitted_manual_review",
    "only paid/delivered counts confirmed EUR",
]

for pattern in required_lead_patterns:
    if pattern not in lead:
        raise SystemExit(f"FAIL: lead-send.html missing measurable handoff pattern: {pattern}")

for pattern in required_kpi_patterns:
    if pattern not in kpi:
        raise SystemExit(f"FAIL: lead-kpi.html missing revenue-gated KPI pattern: {pattern}")

for forbidden in [
    "checkout_handoff','paid'",
    "handoffStatus:'paid'",
    "kpiEvent:'paid'",
    "revenueEur:19,status:'send_ready_not_sent'",
    "revenueEur:19,storedAt",
]:
    if forbidden in lead.replace(" ", ""):
        raise SystemExit(f"FAIL: weak/fake revenue pattern present: {forbidden}")

print("PASS: QPV lead handoffs are persisted to KPI ledger without counting outreach or handoff links as revenue.")
