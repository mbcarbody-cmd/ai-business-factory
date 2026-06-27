#!/usr/bin/env python3
"""Regression gate for the QPV leadId conversion KPI workflow.

This rejects the weak pattern where a dashboard counts checkout/recovery/payment
proof/receipt/recovery-email as revenue, ignores qpvConversionLedger, or loses
leadId attribution between lead, checkout, abandoned checkout recovery, proof,
paid, receipt, recovery email and delivered stages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KPI = ROOT / "website" / "lead-conversion-kpi.html"
PAYMENT_LEDGER = ROOT / "website" / "payment-ledger.html"
CHECKOUT = ROOT / "website" / "checkout.html"
RECOVERY = ROOT / "website" / "abandoned-checkout-recovery.html"
RECEIPT = ROOT / "website" / "receipt.html"
BUYER_RECOVERY = ROOT / "website" / "buyer-recovery-queue.html"

kpi = KPI.read_text(encoding="utf-8")
payment = PAYMENT_LEDGER.read_text(encoding="utf-8")
checkout = CHECKOUT.read_text(encoding="utf-8")
recovery = RECOVERY.read_text(encoding="utf-8")
receipt = RECEIPT.read_text(encoding="utf-8")
buyer_recovery = BUYER_RECOVERY.read_text(encoding="utf-8")

required_kpi_patterns = [
    "qpv-leadid-conversion-kpi-v5-recovery-email-events",
    "href=\"./buyer-recovery-queue.html\"",
    "<b id=\"kRecoveryEmails\">0</b>",
    "function recoveryEmailRows()",
    "row.kpiEvent==='recovery_email_sent'",
    "Number(row.revenueEur||0)===0",
    "Number(row.revenueImpactEur||0)===0",
    "recoveryEmailSentEvents",
    "receiptToRecoveryEmailPct",
    "recoveryEmailRule:'recovery_email_sent events are buyer-aftercare KPI only, require revenueEur=0 and revenueImpactEur=0, and cannot confirm revenue.'",
    "rejectedRevenueSources:['outreach_message','checkout_handoff','abandoned_checkout_recovery','payment_pending_order_created','payment_proof_submitted_manual_review','receipt_generated','receipt_downloaded','receipt_emailed','recovery_email_sent','buyer_recovery_email','manual_transfer_text']",
    "Open buyer-recovery-queue.html and log one recovery email for missing aftercare without revenue impact.",
    "reads qpvConversionLedger recovery_email_sent with revenueEur 0 and revenueImpactEur 0",
    "requires recovery email events to be buyer-aftercare KPI only",
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

required_buyer_recovery_patterns = [
    "kpiEvent:'recovery_email_sent'",
    "revenueEur:0",
    "revenueImpactEur:0",
    "recovery email logging is a buyer-aftercare KPI only and cannot confirm revenue",
    "reads only verified qpvPaidEventLedger paymentStatus=paid events",
    "recovery_email_sent is idempotent by leadId orderId payment reference",
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

for pattern in required_buyer_recovery_patterns:
    if pattern not in buyer_recovery:
        raise SystemExit(f"FAIL: buyer-recovery-queue.html no longer emits zero-revenue recovery email logging: {pattern}")

compact = kpi.replace(" ", "")
for forbidden in [
    "payment_proof_submitted_manual_review')?19",
    "payment_pending_order_created')?19",
    "abandoned_checkout_recovery')?19",
    "recovery_created')?19",
    "recovery_completed')?19",
    "recovery_email_sent')?19",
    "buyer_recovery_email')?19",
    "receipt_generated')?19",
    "receipt_downloaded')?19",
    "receipt_emailed')?19",
    "receiptRevenueEur:19",
    "receipt_generated:19",
    "receipt_downloaded:19",
    "receipt_emailed:19",
    "recovery_email_sent:19",
    "buyer_recovery_email:19",
    "revenueEur:19",
    "revenueImpactEur:19",
    "revenueDeltaEur:19",
    "revenueCountedEur:19",
    "confirmedRevenueEur:19",
    "checkout_handoff:19",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: KPI appears to count a weak/fake revenue source: {forbidden}")

print("PASS: QPV leadId conversion KPI reads lead/checkout/recovery/proof/paid/receipt/recovery-email/delivered stages, preserves leadId attribution, tracks receipt and recovery email aftercare as 0 EUR KPI, and counts EUR only from paid/delivered orders.")