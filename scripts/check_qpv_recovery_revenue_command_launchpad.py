#!/usr/bin/env python3
"""Static regression for the QPV recovery revenue command launchpad."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "recovery-revenue-command-launchpad.html"
html = PAGE.read_text(encoding="utf-8")

required = [
    "Recovery Revenue Command Launchpad",
    "qpvRecoveryConversionHandoffLedger",
    "qpvPaidEventLedger",
    "sourceKpiAdminLink",
    './source-kpi-admin.html#recovered-revenue-dashboard',
    "revenueCommandCenterLink",
    './revenue-command-center.html#recovered-revenue-dashboard',
    "recoveredRevenueKpiLink",
    './recovered-revenue-kpi.html',
    "recoveryRevenueReconciliationLink",
    './recovery-revenue-reconciliation.html',
    "manualPaidGateLink",
    './paid-confirmation.html?source=recovery_revenue_command_launchpad',
    "function reconcile",
    "function paidEventIndex",
    "function isPaidConfirmedHandoff",
    "function isVerifiedPaidEvent",
    "conversionHandoffStatus)==='paid_confirmed'&&paidEventId(row)",
    "paymentStatus)==='paid'&&paidMatchKey(row)",
    "verifiedRecoveredOrders",
    "recoveredRevenueEur",
    "pendingHandoffs",
    "blockedRows",
    "launchpadRevenueEur:0",
    "dashboardLinkRevenueEur:0",
    "reconciliationRowRevenueEur:0",
    "pendingHandoffRevenueEur:0",
    "orphanedConfirmationRevenueEur:0",
    "duplicatePaidEventRevenueEur:0",
    "paymentReferenceRevenueEur:0",
    "proofSubmittedRevenueEur:0",
    "dashboard link is not revenue",
    "launchpad visit is not revenue",
    "pending handoff is not revenue",
    "orphaned confirmation is not revenue",
    "duplicate paidEventId is not revenue",
    "reconciliation row is not revenue",
    "Only a matching verified paid event can unlock recovered EUR",
]

for marker in required:
    if marker not in html:
        raise SystemExit(f"FAIL: recovery revenue command launchpad missing marker: {marker}")

for forbidden in [
    "localStorage.setItem(paidKey",
    "localStorage.setItem('qpvPaidEventLedger'",
    "paymentStatus='paid'",
    'paymentStatus="paid"',
    "launchpadRevenueEur:19",
    "dashboardLinkRevenueEur:19",
    "reconciliationRowRevenueEur:19",
    "pendingHandoffRevenueEur:19",
    "orphanedConfirmationRevenueEur:19",
    "duplicatePaidEventRevenueEur:19",
    "paymentReferenceRevenueEur:19",
    "proofSubmittedRevenueEur:19",
    "dashboard link counts as revenue",
    "launchpad visit counts as revenue",
    "pending handoff counts as revenue",
    "reconciliation row counts as revenue",
]:
    if forbidden in html.replace(" ", "") or forbidden in html:
        raise SystemExit(f"FAIL: recovery revenue command launchpad accepts weak revenue pattern: {forbidden}")

print("PASS: recovery revenue command launchpad links source/admin/reconciliation/paid-gate workflows, routes next handoff to paid confirmation, and keeps dashboard/link/pending/reconciliation/proof/payment-reference activity at 0 EUR until verified paid event match.")