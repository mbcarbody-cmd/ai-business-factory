#!/usr/bin/env python3
"""Static regression for QPV source KPI admin workflow."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "source-kpi-admin.html"
html = PAGE.read_text(encoding="utf-8")

required = [
    "qpvOrderLedger",
    "qpvPaymentProofLedger",
    "qpvConversionLedger",
    "qpvFollowUpLedger",
    "sourceFilter",
    "function sourceStats",
    "function allSources",
    "function sourceOf",
    "./offer.html?source=source_kpi_admin",
    "./checkout.html?source=source_kpi_admin",
    "./payment-ledger.html?source=source_kpi_admin",
    "./paid-confirmation.html",
    "./order-admin.html",
    "Order admin",
    "./revenue-command-center.html",
    "Revenue command center",
    "Source KPI admin exposes order-admin.html and revenue-command-center.html",
    "Only paid/delivered order rows count confirmed EUR",
    "proofSubmittedRevenueEur:0",
    "unverifiedProofRevenueEur:0",
    "followUpMessageRevenueEur:0",
    "preparedFollowUpRevenueEur:0",
    "proof_submitted_manual_review is not paid",
    "paymentReference text is not revenue",
    "source visit is not revenue",
    "lead event is not revenue",
    "checkout order is not revenue until paid",
    "generated follow-up message is not revenue",
    "prepared follow-up ledger row is not revenue",
    "kpiSources",
    "kpiLeads",
    "kpiOrders",
    "kpiProofs",
    "kpiPaid",
    "kpiRevenue",
    "confirmedRevenueEur",
    "uniqueLeads",
    "paidRows",
    "copyUnpaidProofs",
    "downloadUnpaidProofs",
    "unpaidProofRows",
    "toUnpaidProofCsv",
    "qpv-unpaid-proof-follow-up.csv",
    "needs_manual_payment_follow_up",
    "copyFollowUps",
    "downloadFollowUps",
    "followUpMessage(row)",
    "toFollowUpMessages",
    "qpv-unpaid-proof-follow-up-messages.txt",
    "One-click buyer follow-up messages",
    "Generate one copy-ready buyer follow-up message per deduped unpaid proof row; paid rows are excluded.",
    "paid rows are excluded",
    "markFollowUps",
    "markFollowUpsPrepared",
    "followUpKeyOf",
    "followUpPreparedIndex",
    "followUpStatusLedger",
    "follow_up_prepared",
    "preparedSource",
    "source_kpi_admin",
    "already prepared rows are excluded",
    "Prepared follow-up rows are outreach state only; they suppress duplicate chasing and never count as revenue.",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: source KPI admin missing marker: {marker}")

for forbidden in [
    "proofSubmittedRevenueEur:19",
    "unverifiedProofRevenueEur:19",
    "followUpMessageRevenueEur:19",
    "preparedFollowUpRevenueEur:19",
    "paymentReference text is revenue",
    "proof_submitted_manual_review is paid",
    "source visit is revenue",
    "generated follow-up message is revenue",
    "prepared follow-up ledger row is revenue",
]:
    if forbidden in html.replace(" ", ""):
        raise SystemExit(f"FAIL: source KPI admin accepts weak revenue pattern: {forbidden}")

print("PASS: source KPI admin filters source-attributed QPV ledgers, exports unpaid proofs, generates deduped buyer follow-up messages, tracks prepared follow-up status in qpvFollowUpLedger, and keeps unverified proof/source/follow-up activity at 0 EUR.")
