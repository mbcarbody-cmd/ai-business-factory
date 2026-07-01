#!/usr/bin/env python3
"""Regression gate for QPV recovery revenue reconciliation.

The reconciliation dashboard must cross-check recovery handoff rows against
verified paid events, expose buyer/operator navigation, and forbid recovered
revenue from pending, orphaned, duplicate, proof, reminder, dashboard link, or
payment-reference-only states.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "recovery-revenue-reconciliation.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text.replace(" ", ""):
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    for needle, label in [
        ("Recovery Revenue Reconciliation", "page title"),
        ("qpvRecoveryConversionHandoffLedger", "recovery handoff ledger read"),
        ("qpvPaidEventLedger", "verified paid event ledger read"),
        ("function paidEventIndex", "paid event duplicate index"),
        ("function reconcile", "reconciliation engine"),
        ("isVerifiedPaidEvent", "verified paid event guard"),
        ("isPaidConfirmedHandoff", "paid-confirmed handoff guard"),
        ("orphaned_paid_confirmed_handoff_without_verified_paid_event", "orphaned confirmation block"),
        ("duplicate_paidEventId_or_handoff", "duplicate handoff block"),
        ("duplicate_paid_event", "duplicate paid event block"),
        ("verifiedRecoveredOrders", "verified recovered order KPI"),
        ("recoveredRevenueEur", "recovered EUR KPI"),
        ("pendingHandoffs", "pending handoff KPI"),
        ("orphanedConfirmations", "orphaned confirmation KPI"),
        ("duplicatePaidEventIds", "duplicate paid ID KPI"),
        ("reconciliationStatus", "reconciliation status KPI"),
        ("kpiVerified", "verified KPI DOM"),
        ("kpiRecovered", "recovered EUR DOM"),
        ("kpiPending", "pending KPI DOM"),
        ("kpiOrphans", "orphan KPI DOM"),
        ("kpiDuplicates", "duplicate KPI DOM"),
        ("kpiStatus", "status KPI DOM"),
        ("copyReconciliation", "copy action"),
        ("downloadReconciliation", "download action"),
        ("qpv-recovery-revenue-reconciliation.json", "download filename"),
        ('href="./source-kpi-admin.html#recovered-revenue-dashboard"', "source KPI backlink"),
        ('href="./revenue-command-center.html#recovered-revenue-dashboard"', "command center backlink"),
        ('href="./recovered-revenue-kpi.html"', "recovered KPI link"),
        ('href="./paid-confirmation.html?source=recovery_revenue_reconciliation"', "manual paid gate link"),
        ("revenueDeltaFromThisPageEur:0", "page zero revenue side-effect"),
        ("reconciliationRevenueEur:0", "reconciliation zero revenue"),
        ("pendingRevenueEur:0", "pending zero revenue"),
        ("orphanedConfirmationRevenueEur:0", "orphaned confirmation zero revenue"),
        ("duplicatePaidEventRevenueEur:0", "duplicate paid event zero revenue"),
        ("paymentReferenceRevenueEur:0", "payment reference zero revenue"),
        ("proofSubmittedRevenueEur:0", "proof zero revenue"),
        ("dashboardIntegrationRevenueEur:0", "dashboard link zero revenue"),
        ("pending handoff is not revenue", "pending weak-pattern rejection"),
        ("orphaned paid_confirmed handoff is not revenue", "orphaned weak-pattern rejection"),
        ("duplicate paidEventId is not revenue", "duplicate weak-pattern rejection"),
        ("payment reference is not revenue", "payment-reference weak-pattern rejection"),
        ("proof text is not revenue", "proof weak-pattern rejection"),
        ("recovery reminder is not revenue", "reminder weak-pattern rejection"),
        ("dashboard integration link is not revenue", "dashboard weak-pattern rejection"),
        ("reconciliation row is not revenue", "reconciliation weak-pattern rejection"),
    ]:
        require(text, needle, label)

    for needle, label in [
        ("pendingRevenueEur:19", "fake pending revenue"),
        ("orphanedConfirmationRevenueEur:19", "fake orphaned revenue"),
        ("duplicatePaidEventRevenueEur:19", "fake duplicate revenue"),
        ("paymentReferenceRevenueEur:19", "fake payment reference revenue"),
        ("proofSubmittedRevenueEur:19", "fake proof revenue"),
        ("dashboardIntegrationRevenueEur:19", "fake dashboard revenue"),
        ("reconciliationRevenueEur:19", "fake reconciliation revenue"),
        ("localStorage.setItem(paidKey", "paid ledger write"),
        ("localStorage.setItem('qpvPaidEventLedger'", "paid ledger write literal"),
        ("pending handoff counts as revenue", "pending-as-revenue claim"),
        ("orphaned handoff counts as revenue", "orphaned-as-revenue claim"),
        ("duplicate paidEventId counts as revenue", "duplicate-as-revenue claim"),
    ]:
        forbid(text, needle, label)

    print("PASS qpv recovery revenue reconciliation verifies paid handoffs against paid events and blocks pending/orphaned/duplicate fake revenue")


if __name__ == "__main__":
    main()
