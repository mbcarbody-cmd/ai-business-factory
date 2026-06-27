#!/usr/bin/env python3
"""Regression gate for the QPV leadId conversion KPI workflow.

This rejects the weak pattern where a dashboard counts checkout/recovery/payment
proof/receipt as revenue, ignores qpvConversionLedger, or loses leadId attribution
between lead, checkout, abandoned checkout recovery, proof, paid, receipt and
delivered stages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KPI = ROOT / "website" / "lead-conversion-kpi.html"
PAYMENT_LEDGER = ROOT / "website" / "payment-ledger.html"
CHECKOUT = ROOT / "website" / "checkout.html"
RECOVERY = ROOT / "website" / "abandoned-checkout-recovery.html"
RECEIPT = ROOT / "website" / "receipt.html"

kpi = KPI.read_text(encoding="utf-8")
payment = PAYMENT_LEDGER.read_text(encoding="utf-8")
checkout = CHECKOUT.read_text(encoding="utf-8")
recovery = RECOVERY.read_text(encoding="utf-8")
receipt = RECEIPT.read_text(encoding="utf-8")

required_kpi_patterns = [
    "qpv-leadid-conversion-kpi-v4-receipt-events",
    "receiptKey='qpvReceiptLedger'",
    "function receiptRows()",
    "function receiptActionRows()",
    "leadIdReceiptOrders",
    "receiptZeroRevenueEvents",
    "receiptGeneratedEvents",
    "receiptDownloadedEvents",
    "receiptEmailedEvents",
    "paidToReceiptPct",
    "leadToReceiptPct",
    "receiptToDeliveredPct",
    "receipt_generated",
    "receipt_downloaded",
    "receipt_emailed",
    "receiptRule:'qpvReceiptLedger plus receipt_generated/receipt_downloaded/receipt_emailed conversion events are buyer-aftercare KPI only and require 0 EUR revenue.'",
    "Number(row.receiptRevenueEur||0)===0",
    "Number(row.revenueEur||0)===0",
    "qpv-leadid-conversion-kpi-v4-receipt-events",
    "recoveryKey='qpvAbandonedCheckoutRecoveries'",
    "function recoveryRows()",
    "leadIdAbandonedRecoveries",
    "checkoutToRecoveryPct",
    "recoveryToProofPct",
    "abandoned_checkout_recovery",
    "recoveryRule:'qpvAbandonedCheckoutRecoveries rows are conversion KPI only and require revenueCountedEur=0.'",
    "Number(row.revenueCountedEur||0)===0",
    "conversionKey='qpvConversionLedger'",
    "proofKey='qpvPaymentProofLedger'",
    "row.kpiEvent==='payment_proof_submitted_manual_review'",
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

required_recovery_patterns = [
    "recoveryKey='qpvAbandonedCheckoutRecoveries'",
    "eventType:'recovery_created'",
    "leadId:row.leadId",
    "orderId:row.orderId",
    "checkoutId:row.checkoutId",
    "revenueDeltaEur:0",
    "revenueCountedEur:0",
    "recoveryEventsAreRevenue:false",
    "confirmedRevenueSource:'verified paid events only'",
]

required_receipt_patterns = [
    "receiptKey='qpvReceiptLedger'",
    "conversionKey='qpvConversionLedger'",
    "kpiEvent:'receipt_generated'",
    "auditReceiptAction('receipt_downloaded',lastReceipt)",
    "auditReceiptAction('receipt_emailed',lastReceipt)",
    "receiptRevenueEur:0",
    "revenueEur:0",
    "receiptEventsDoNotIncreaseRevenue:true",
    "findPaid(orderId,leadId)",
    "verified_paid_event_required_before_receipt",
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

for pattern in required_recovery_patterns:
    if pattern not in recovery:
        raise SystemExit(f"FAIL: abandoned-checkout-recovery.html no longer preserves zero-revenue recovery attribution: {pattern}")

for pattern in required_receipt_patterns:
    if pattern not in receipt:
        raise SystemExit(f"FAIL: receipt.html no longer preserves zero-revenue paid-only receipt attribution: {pattern}")

compact = kpi.replace(" ", "")
for forbidden in [
    "payment_proof_submitted_manual_review')?19",
    "payment_pending_order_created')?19",
    "abandoned_checkout_recovery')?19",
    "recovery_created')?19",
    "recovery_completed')?19",
    "receipt_generated')?19",
    "receipt_downloaded')?19",
    "receipt_emailed')?19",
    "receiptRevenueEur:19",
    "receipt_generated:19",
    "receipt_downloaded:19",
    "receipt_emailed:19",
    "revenueEur:19",
    "revenueDeltaEur:19",
    "revenueCountedEur:19",
    "confirmedRevenueEur:19",
    "checkout_handoff:19",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: KPI appears to count a weak/fake revenue source: {forbidden}")

print("PASS: QPV leadId conversion KPI reads lead/checkout/recovery/proof/paid/receipt/delivered stages, preserves leadId attribution, tracks receipt aftercare as 0 EUR KPI, and counts EUR only from paid/delivered orders.")
