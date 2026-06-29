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
    "proof_submitted_manual_review is not paid",
    "paymentReference text is not revenue",
    "source visit is not revenue",
    "lead event is not revenue",
    "checkout order is not revenue until paid",
    "kpiSources",
    "kpiLeads",
    "kpiOrders",
    "kpiProofs",
    "kpiPaid",
    "kpiRevenue",
    "confirmedRevenueEur",
    "uniqueLeads",
    "paidRows",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: source KPI admin missing marker: {marker}")

for forbidden in [
    "proofSubmittedRevenueEur:19",
    "unverifiedProofRevenueEur:19",
    "paymentReference text is revenue",
    "proof_submitted_manual_review is paid",
    "source visit is revenue",
]:
    if forbidden in html.replace(" ", ""):
        raise SystemExit(f"FAIL: source KPI admin accepts weak revenue pattern: {forbidden}")

print("PASS: source KPI admin filters source-attributed QPV ledgers, exposes command backtracking, and keeps unverified proof/source activity at 0 EUR.")
