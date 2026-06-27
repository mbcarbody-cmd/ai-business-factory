#!/usr/bin/env python3
"""Regression gate for the QPV revenue command center.

The command center must create measurable product-state movement by exposing the
buyer acquisition -> quote/checkout -> proof follow-up -> paid gate -> verified
receipt -> buyer recovery -> recovery email logging workflow while preserving
revenue integrity. It is allowed to read ledgers and build action links; it must
not write fake paid events or count proof/checkout/receipt/recovery/email events
as paid revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "revenue-command-center.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    for needle, label in [
        ("QPV Revenue Command Center", "buyer-ready page title"),
        ("qpvOrderLedger", "order ledger read"),
        ("qpvOutreachLeadLedger", "outreach lead ledger read"),
        ("qpvPaidEventLedger", "paid event ledger read"),
        ("qpvReceiptLedger", "receipt ledger read"),
        ("qpvConversionLedger", "conversion ledger read"),
        ("qpvBuyerRecoveryQueue", "buyer recovery queue ledger read"),
        ("isProofReadyUnpaid", "proof-ready unpaid filter"),
        ("checkoutReadyLead", "checkout-ready lead filter"),
        ("dedupPaidEvents", "paid event idempotency"),
        ("receiptReadyPaidEvent", "receipt-ready verified-paid filter"),
        ("receiptExistsFor", "receipt idempotency guard"),
        ("legacyPaymentProofReference", "legacy proof reference normalizer"),
        ("paymentProof?.paymentNote", "legacy payment note fallback"),
        ("paymentProof?.note", "legacy proof note fallback"),
        ("function paidReference", "paid event reference normalizer"),
        ("event.paymentNote", "legacy paid event note fallback"),
        ("legacy paymentProof.paymentNote is normalized as paymentReference", "legacy reference QA rule"),
        ("buyerRecoveryMissingActions", "buyer recovery missing-action detector"),
        ("buyerRecoveryRows", "buyer recovery row builder"),
        ("buyerRecoveryCases", "buyer recovery KPI count"),
        ("buyerRecoveryRevenueEur:0", "buyer recovery zero revenue effect"),
        ("recoveryEmailSentFor", "recovery email verified-paid matcher"),
        ("recoveryEmailEvents", "recovery email KPI counter"),
        ("recoveryEmailLogged", "recovery email action-state detector"),
        ("Recovery emails", "recovery email KPI label"),
        ("recoveryEmailSentEvents", "recovery email QA KPI"),
        ("recoveryEmailRevenueEur:0", "recovery email zero revenue effect"),
        ("Log recovery email", "recovery email action CTA"),
        ("paymentReference:row.event.paymentReference||row.event.reference", "recovery email handoff payment reference"),
        ("row.event.paymentNote", "legacy payment note handoff"),
        ("recovery email KPI reads recovery_email_sent zero-EUR events matched to verified paid buyers", "recovery email KPI source guardrail"),
        ("recovery email action links preserve orderId leadId and paymentReference when present", "recovery email handoff guardrail"),
        ("recovery_email_sent is aftercare only and never paid revenue", "recovery email zero-revenue guardrail"),
        ("Buyer recovery queue", "buyer recovery KPI/nav label"),
        ("./buyer-recovery-queue.html", "buyer recovery queue link"),
        ("Open buyer recovery", "buyer recovery action CTA"),
        ("buyer recovery queue link is visible from command center", "buyer recovery nav guardrail"),
        ("buyer recovery KPI reads verified paid buyers missing receipt aftercare", "buyer recovery source guardrail"),
        ("buyer recovery action links preserve orderId and leadId when present", "buyer recovery handoff guardrail"),
        ("buyer recovery outreach is aftercare only and never paid revenue", "buyer recovery zero revenue guardrail"),
        ("./daily-revenue-action.html", "daily action link"),
        ("./order-followup-export.html", "proof-ready export link"),
        ("./order-paid-bridge.html", "paid bridge link"),
        ("./paid-confirmation.html", "manual paid gate link"),
        ("./receipt.html", "buyer receipt link"),
        ("Generate receipt", "receipt action queue CTA"),
        ("receiptReadyPaidEvents", "receipt KPI count"),
        ("missingReceipts", "missing receipt queue KPI"),
        ("receiptLedgerRows", "receipt ledger KPI"),
        ("receipt action links preserve orderId and leadId when present", "receipt handoff guardrail"),
        ("receipts are aftercare only and never paid revenue", "receipt zero-revenue guardrail"),
        ("./outreach-lead-pipeline.html", "outreach pipeline link"),
        ("./quote-checkout.html", "quote checkout link"),
        ("./lead-conversion-kpi.html", "lead KPI link"),
        ("Buyer</span> SMB/product seller", "buyer segment"),
        ("Price</span> 19 EUR", "buyer-ready price"),
        ("payment proof is not revenue", "proof revenue guardrail"),
        ("checkout is not paid", "checkout revenue guardrail"),
        ("quote accepted is not paid", "quote revenue guardrail"),
        ("revenueDeltaFromThisPageEur:0", "zero revenue side-effect"),
        ("receiptRevenueEur:0", "receipt zero revenue effect"),
        ("duplicate paid references are deduplicated by orderId + reference", "dedupe QA rule"),
    ]:
        require(text, needle, label)

    for needle, label in [
        ("localStorage.setItem(paidKey", "paid ledger write"),
        ("localStorage.setItem('qpvPaidEventLedger'", "paid ledger write literal"),
        ("paymentStatus='paid'", "fake paid mutation"),
        ('paymentStatus="paid"', "fake paid mutation"),
        ("proof_submitted counts as revenue", "proof-as-revenue claim"),
        ("checkout counts as paid", "checkout-as-revenue claim"),
        ("receipt counts as revenue", "receipt-as-revenue claim"),
        ("buyer recovery counts as revenue", "buyer-recovery-as-revenue claim"),
        ("recovery queue counts as paid", "recovery-queue-as-paid claim"),
        ("recovery_email_sent counts as revenue", "recovery-email-as-revenue claim"),
        ("recoveryEmailRevenueEur:19", "fake recovery email revenue"),
        ("buyerRecoveryRevenueEur:19", "fake buyer recovery revenue"),
        ("receiptRevenueEur:19", "fake receipt revenue"),
        ("revenueEur:19", "hard-coded revenue event"),
        ("confirmedRevenueEur:19", "fake confirmed revenue"),
    ]:
        forbid(text, needle, label)

    print("PASS qpv revenue command center regression with legacy payment proof references")


if __name__ == "__main__":
    main()
