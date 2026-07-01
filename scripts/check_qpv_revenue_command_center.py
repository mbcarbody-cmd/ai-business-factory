#!/usr/bin/env python3
"""Regression gate for the QPV revenue command center.

The command center must create measurable product-state movement by exposing the
buyer acquisition -> quote/checkout -> source KPI filter -> proof follow-up -> paid gate -> verified
fulfillment -> fulfilled-order KPI -> receipt -> buyer recovery -> recovery email logging -> payment
reference repair workflow while preserving revenue integrity. It is allowed to read ledgers and
build action links; it must not write fake paid events or count proof/checkout/
fulfillment/status/KPI/receipt/recovery/email/reference-repair events as paid revenue.
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
        ("qpvCompletedOrderLedger", "completed order ledger read"),
        ("qpvReceiptLedger", "receipt ledger read"),
        ("qpvConversionLedger", "conversion ledger read"),
        ("qpvBuyerRecoveryQueue", "buyer recovery queue ledger read"),
        ('href="./source-kpi-admin.html"', "top-level source KPI admin navigation"),
        ("Filter source KPI", "source KPI card CTA"),
        ("./source-kpi-admin.html", "source KPI action links"),
        ("source:row.source||row.paymentProof?.source||'unknown'", "order source KPI handoff"),
        ("source:row.source||'unknown'", "lead/paid source KPI handoff"),
        ("command center exposes source-kpi-admin.html for source attribution filtering", "source KPI QA rule"),
        ('href="./paid-fulfillment.html"', "top-level paid fulfillment navigation"),
        ('href="./paid-fulfillment-router.html"', "top-level fulfillment router navigation"),
        ('href="./fulfilled-order-kpi.html"', "top-level fulfilled-order KPI navigation"),
        ('href="./order-status.html"', "top-level buyer order status navigation"),
        ("Fulfill & reconcile", "fulfillment command card"),
        ("Complete fulfillment", "fulfillment CTA"),
        ("Route fulfillment", "router CTA"),
        ("Review fulfilled KPI", "fulfilled KPI CTA"),
        ("Open buyer status", "buyer status CTA"),
        ("Fulfilled orders", "fulfilled orders KPI tile"),
        ("Pending fulfillment", "pending fulfillment KPI tile"),
        ("Fulfillment rate", "fulfillment rate KPI tile"),
        ("function paidEventId", "paid event id normalizer"),
        ("function completedPaidEventId", "completed paid event id normalizer"),
        ("function verifiedCompletedOrders", "verified completed order matcher"),
        ("function pendingPaidFulfillment", "pending fulfillment detector"),
        ("function fulfillmentRate", "fulfillment rate calculator"),
        ("function fulfilledOrderStatusHref", "buyer status handoff builder"),
        ("function fulfilledKpiHref", "fulfilled KPI handoff builder"),
        ("verifiedFulfilledOrders", "fulfilled order QA KPI"),
        ("pendingPaidFulfillment", "pending fulfillment QA KPI"),
        ("fulfillmentRatePct", "fulfillment rate QA KPI"),
        ("completedOrderLedgerRows", "completed order ledger QA KPI"),
        ("paidFulfillmentLinkRevenueEur:0", "paid fulfillment link zero revenue effect"),
        ("fulfilledOrderKpiLinkRevenueEur:0", "fulfilled KPI link zero revenue effect"),
        ("fulfilledOrderKpiVisitRevenueEur:0", "fulfilled KPI visit zero revenue effect"),
        ("buyerStatusLinkRevenueEur:0", "buyer status link zero revenue effect"),
        ("command center exposes paid-fulfillment.html and paid-fulfillment-router.html for verified paid fulfillment", "fulfillment route QA rule"),
        ("command center exposes fulfilled-order-kpi.html for fulfilled revenue reconciliation", "fulfilled KPI QA rule"),
        ("command center exposes order-status.html for buyer-ready fulfilled order status", "buyer status QA rule"),
        ("command center fulfilled-order KPI counts only qpvCompletedOrderLedger rows matched to unique verified paidEventId", "verified fulfillment source guardrail"),
        ("command center pending fulfillment KPI reads verified paid events missing completed order rows", "pending fulfillment source guardrail"),
        ("paid fulfillment, fulfilled KPI and buyer status links are workflow actions only and never paid revenue", "fulfillment zero-revenue guardrail"),
        ('href="./payment-recovery-queue.html"', "top-level payment recovery queue navigation"),
        ("Run payment recovery", "payment recovery card CTA"),
        ("./payment-recovery-queue.html", "payment recovery action links"),
        ("paymentRecoveryQueueRevenueEur:0", "payment recovery zero revenue effect"),
        ("paymentRecoveryReminderRevenueEur:0", "payment recovery reminder zero revenue effect"),
        ("command center exposes payment-recovery-queue.html for unpaid buyer recovery reminders", "payment recovery QA rule"),
        ("payment recovery queue link is visible from command center", "payment recovery visibility guardrail"),
        ("payment recovery queue is follow-up only and never paid revenue", "payment recovery zero-revenue guardrail"),
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
        ("function aftercareReference", "aftercare reference normalizer"),
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
        ("Reference breaks", "payment reference continuity KPI label"),
        ("referenceBreaks", "payment reference continuity KPI id"),
        ("paymentReferenceBreakRows", "payment reference break detector"),
        ("looseAftercareRows", "aftercare continuity candidate detector"),
        ("paymentReferenceBreaks", "payment reference break QA KPI"),
        ("Repair reference continuity", "reference repair action CTA"),
        ("referenceContinuityRepairRevenueEur:0", "reference repair zero revenue effect"),
        ("paid aftercare continuity is checked by orderId leadId and paymentReference", "reference continuity QA rule"),
        ("reference break KPI reads receipt/recovery aftercare rows whose paymentReference does not match verified paid event", "reference break KPI source guardrail"),
        ("reference continuity repair is aftercare only and never paid revenue", "reference repair zero-revenue guardrail"),
        ("receipt action links preserve orderId leadId and paymentReference when present", "receipt reference handoff guardrail"),
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
        ("payment recovery counts as revenue", "payment-recovery-as-revenue claim"),
        ("payment recovery queue counts as paid", "payment-recovery-as-paid claim"),
        ("recovery queue counts as paid", "recovery-queue-as-paid claim"),
        ("fulfillment link counts as revenue", "fulfillment-link-as-revenue claim"),
        ("fulfilled KPI counts as revenue", "fulfilled-kpi-as-revenue claim"),
        ("buyer status counts as revenue", "buyer-status-as-revenue claim"),
        ("recovery_email_sent counts as revenue", "recovery-email-as-revenue claim"),
        ("reference continuity repair counts as revenue", "reference-repair-as-revenue claim"),
        ("recoveryEmailRevenueEur:19", "fake recovery email revenue"),
        ("buyerRecoveryRevenueEur:19", "fake buyer recovery revenue"),
        ("paymentRecoveryQueueRevenueEur:19", "fake payment recovery queue revenue"),
        ("paymentRecoveryReminderRevenueEur:19", "fake payment recovery reminder revenue"),
        ("paidFulfillmentLinkRevenueEur:19", "fake fulfillment link revenue"),
        ("fulfilledOrderKpiLinkRevenueEur:19", "fake fulfilled KPI link revenue"),
        ("fulfilledOrderKpiVisitRevenueEur:19", "fake fulfilled KPI visit revenue"),
        ("buyerStatusLinkRevenueEur:19", "fake buyer status link revenue"),
        ("referenceContinuityRepairRevenueEur:19", "fake reference repair revenue"),
        ("receiptRevenueEur:19", "fake receipt revenue"),
        ("revenueEur:19", "hard-coded revenue event"),
        ("confirmedRevenueEur:19", "fake confirmed revenue"),
    ]:
        forbid(text, needle, label)

    print("PASS qpv revenue command center regression with fulfilled-order KPI, fulfillment routing, source KPI navigation, payment recovery queue navigation, and payment reference continuity KPI")


if __name__ == "__main__":
    main()
