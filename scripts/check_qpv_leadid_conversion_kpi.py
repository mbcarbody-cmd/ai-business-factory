#!/usr/bin/env python3
"""Regression gate for the QPV leadId conversion KPI workflow.

This rejects the weak pattern where a dashboard counts checkout/payment proof as
revenue, ignores qpvConversionLedger, or loses leadId attribution between lead,
checkout, proof, paid and delivered stages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KPI = ROOT / "website" / "lead-conversion-kpi.html"
PAYMENT_LEDGER = ROOT / "website" / "payment-ledger.html"
CHECKOUT = ROOT / "website" / "checkout.html"

kpi = KPI.read_text(encoding="utf-8")
payment = PAYMENT_LEDGER.read_text(encoding="utf-8")
checkout = CHECKOUT.read_text(encoding="utf-8")

required_kpi_patterns = [
    "qpv-leadid-conversion-kpi-v2",
    "conversionKey='qpvConversionLedger'",
    "proofKey='qpvPaymentProofLedger'",
    "row.kpiEvent==='payment_proof_submitted_manual_review'",
    "Number(row.revenueEur||0)===0",
    "leadIdQualifiedLeads",
    "leadIdCheckoutOrders",
    "leadIdPaymentProofs",
    "leadIdPaidOrders",
    "leadIdDeliveredOrders",
    "leadToCheckoutPct",
    "checkoutToProofPct",
    "leadToProofPct",
    "proofToPaidPct",
    "paidToDeliveredPct",
    "confirmedRevenueEur:confirmedRevenue(orders)",
    "Only qpvOrderLedger rows with paymentStatus paid/delivered or fulfillmentStatus delivered count confirmed EUR.",
    "payment_proof_submitted_manual_review",
    "manual_transfer_text",
]

required_payment_patterns = [
    "conversionKey='qpvConversionLedger'",
    "kpiEvent:'payment_proof_submitted_manual_review'",
    "stateTo:'proof_submitted_manual_review'",
    "revenueEur:0",
    "leadId:proof.leadId",
]

required_checkout_patterns = [
    "leadId:order.leadId",
    "paymentHref(order)",
    "payment_pending_order_created",
]

for pattern in required_kpi_patterns:
    if pattern not in kpi:
        raise SystemExit(f"FAIL: lead-conversion-kpi.html missing pattern: {pattern}")

for pattern in required_payment_patterns:
    if pattern not in payment:
        raise SystemExit(f"FAIL: payment-ledger.html no longer emits leadId proof conversion: {pattern}")

for pattern in required_checkout_patterns:
    if pattern not in checkout:
        raise SystemExit(f"FAIL: checkout.html no longer preserves leadId order conversion: {pattern}")

compact = kpi.replace(" ", "")
for forbidden in [
    "payment_proof_submitted_manual_review')?19",
    "payment_pending_order_created')?19",
    "revenueEur:19",
    "confirmedRevenueEur:19",
    "checkout_handoff:19",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: KPI appears to count a weak/fake revenue source: {forbidden}")

print("PASS: QPV leadId conversion KPI reads lead/checkout/proof/paid/delivered stages, preserves leadId attribution, and counts EUR only from paid/delivered orders.")
