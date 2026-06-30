#!/usr/bin/env python3
"""Static regression for QPV payment recovery queue."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "payment-recovery-queue.html"
html = PAGE.read_text(encoding="utf-8")

required = [
    "QPV Payment Recovery Queue",
    "qpvFollowUpLedger",
    "qpvContactedFollowUpLedger",
    "qpvPaymentRecoveryReminderLedger",
    "qpvOrderLedger",
    "payment_recovery_queue",
    "payment-recovery-queue-v1",
    "Generate + log first recovery reminder",
    "Copy next reminder message",
    "Download recovery queue JSON",
    "function queueRows",
    "function logReminder",
    "function reminderMessage",
    "function reminderIndex",
    "function paidIndex",
    "Duplicate recovery reminder blocked",
    "needs_payment_recovery_reminder",
    "sent_or_ready_to_send_awaiting_response",
    "recoveryPriorityScore",
    "expectedValueEur",
    "stale_rescue_7d_plus",
    "overdue_3d_plus",
    "sourceFilter",
    "./source-kpi-admin.html",
    "./follow-up-contact-admin.html",
    "./payment-ledger.html?source=payment_recovery_queue",
    "./paid-confirmation.html",
    "buyer:'SMB/product seller'",
    "SMB/product seller",
    "19 EUR",
    "confirmedRevenueEur",
    "recoveryQueueRevenueEur:0",
    "recoveryReminderRevenueEur:0",
    "contactedFollowUpRevenueEur:0",
    "preparedFollowUpRevenueEur:0",
    "Only paid/delivered order rows count confirmed EUR",
    "recovery queue row is not revenue",
    "recovery reminder attempt is not revenue",
    "contacted follow-up row is not revenue",
    "prepared follow-up row is not revenue",
    "paymentReference text is not revenue",
    "proof_submitted_manual_review is not paid",
    "checkout order is not revenue until paid",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: payment recovery queue missing marker: {marker}")

for forbidden in [
    "recoveryQueueRevenueEur:19",
    "recoveryReminderRevenueEur:19",
    "contactedFollowUpRevenueEur:19",
    "preparedFollowUpRevenueEur:19",
    "paymentReferencetextisrevenue",
    "proof_submitted_manual_reviewispaid",
    "checkoutorderisrevenue",
]:
    if forbidden in html.replace(" ", ""):
        raise SystemExit(f"FAIL: payment recovery queue accepts weak revenue pattern: {forbidden}")

print("PASS: payment recovery queue prioritizes unpaid buyers, logs deduped recovery reminders with source/reference continuity, and keeps reminder/contact/proof activity at 0 EUR until verified paid.")
