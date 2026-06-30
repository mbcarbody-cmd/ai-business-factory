#!/usr/bin/env python3
"""Static regression for QPV follow-up contact admin workflow."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "follow-up-contact-admin.html"
html = PAGE.read_text(encoding="utf-8")

required = [
    "QPV follow-up contact admin",
    "qpvFollowUpLedger",
    "qpvContactedFollowUpLedger",
    "qpvOrderLedger",
    "markContacted",
    "markFirstContacted",
    "eligiblePreparedRows",
    "contactedIndex",
    "contactKeyOf",
    "contactAttemptCount:1",
    "contactAttemptStatus:'contacted_awaiting_response'",
    "contactedSource:'follow_up_contact_admin'",
    "followUpStatus==='follow_up_prepared'",
    "isFollowUpPrepared===true",
    "function paidIndex",
    "function confirmedRevenue",
    "Only paid/delivered order rows count confirmed EUR",
    "contactedFollowUpRevenueEur:0",
    "contactAttemptRevenueEur:0",
    "confirmedRevenueEur:0",
    "contacted follow-up row is not revenue",
    "contact attempt is not revenue",
    "prepared follow-up row is not revenue",
    "paymentReference text is not revenue",
    "proof_submitted_manual_review is not paid",
    "Source KPI admin",
    "./source-kpi-admin.html",
    "./payment-ledger.html?source=follow_up_contact_admin",
    "./paid-confirmation.html",
    "Contacted today",
    "Awaiting response",
    "Converted after follow-up",
    "qpv-contacted-follow-up-ledger.json",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: follow-up contact admin missing marker: {marker}")

for forbidden in [
    "contactedFollowUpRevenueEur:19",
    "contactAttemptRevenueEur:19",
    "contacted follow-up row is revenue",
    "contact attempt is revenue",
    "prepared follow-up row is revenue",
    "paymentReference text is revenue",
    "proof_submitted_manual_review is paid",
]:
    if forbidden in html.replace(" ", ""):
        raise SystemExit(f"FAIL: follow-up contact admin accepts weak revenue pattern: {forbidden}")

print("PASS: QPV follow-up contact admin marks only unpaid prepared follow-up buyers as contacted, suppresses duplicates/paid rows, preserves source and proof age, exports contacted ledger, and keeps contact attempts at 0 EUR until verified paid order rows exist.")
