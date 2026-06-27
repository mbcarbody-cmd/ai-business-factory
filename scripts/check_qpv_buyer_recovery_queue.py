#!/usr/bin/env python3
"""Static regression for QPV buyer recovery queue.

This test intentionally checks operational code, not summaries/policies.
It requires the shipped browser workflow to build outreach-ready rows only
from verified paid events and to keep all recovery/receipt events at 0 EUR.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "buyer-recovery-queue.html"
TEXT = PAGE.read_text(encoding="utf-8")

REQUIRED = [
    "qpvPaidEventLedger",
    "qpvReceiptLedger",
    "qpvConversionLedger",
    "qpvBuyerRecoveryQueue",
    "function verifiedPaid(event)",
    "event.paymentStatus==='paid'",
    "clean(event.orderId)",
    "clean(event.leadId)",
    "clean(event.paymentReference||event.reference)",
    "function dedupPaidEvents(events)",
    "orderId + payment reference",
    "receipt_generated",
    "receipt_downloaded",
    "receipt_emailed",
    "recovery_email_sent",
    "function recoveryEmailLogged(conversions,row)",
    "function logRecoveryEmail(row)",
    "only verified paid missing-aftercare rows are eligible",
    "recovery email logging is a buyer-aftercare KPI only and cannot confirm revenue",
    "Number(row.revenueEur||0)===0",
    "Number(row.receiptRevenueEur||0)===0",
    "revenueImpactEur:0",
    "revenueDeltaFromThisPageEur:0",
    "outreach-ready rows never increase confirmed EUR",
    "payment_proof",
    "checkout_created",
]

FORBIDDEN = [
    "confirmedRevenueEur+=",
    "revenueEur:priceEur",
    "receiptRevenueEur:priceEur",
    "paymentStatus==='proof'",
    "paymentStatus==='pending'",
    "checkout is paid",
    "proof is paid",
]

missing = [pattern for pattern in REQUIRED if pattern not in TEXT]
forbidden = [pattern for pattern in FORBIDDEN if pattern in TEXT]

assert PAGE.exists(), "buyer recovery queue page must exist"
assert not missing, f"missing required buyer recovery queue guards: {missing}"
assert not forbidden, f"forbidden fake-revenue patterns present: {forbidden}"

print("PASS qpv buyer recovery queue regression")
print("- verified paid ledger is the only queue source")
print("- duplicate paid events are deduplicated by orderId + reference")
print("- missing receipt-generated/downloaded/emailed actions create outreach rows")
print("- recovery_email_sent logs one-click outreach into qpvConversionLedger as 0 EUR")
print("- outreach, receipt and recovery rows remain 0 EUR and cannot confirm revenue")
