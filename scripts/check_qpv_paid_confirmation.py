#!/usr/bin/env python3
"""Regression gate for QPV paid confirmation.

Paid confirmation may surface recovery conversion handoffs for manual verification,
but it must never count those handoffs as revenue until an idempotent verified
payment event is written by the paid gate.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "paid-confirmation.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, "QPV PAID CONFIRMATION", "paid gate identity")
    require(text, "qpvPaidEventLedger", "paid ledger")
    require(text, "qpvPaidDuplicateBlocks", "duplicate paid-event blocker")
    require(text, "paymentEventId(data.orderId,data.paymentReference)", "idempotent paid-event id")
    require(text, "Duplicate paid event blocked; revenue unchanged.", "duplicate block user message")
    require(text, "confirmedRevenue()", "confirmed revenue calculation")
    require(text, "qpvRecoveryConversionHandoffLedger", "recovery handoff ledger read")
    require(text, "Pending recovery conversion handoffs", "handoff status panel")
    require(text, "loadTopPendingHandoff", "one-click handoff loader")
    require(text, "readyRecoveryHandoffs", "ready handoff filter")
    require(text, "handoffPaidGateHref", "paid gate backlink params")
    require(text, "source-kpi-admin.html", "backlink to source KPI recovery ledger")
    require(text, "handoffRevenueEur:0", "zero revenue handoff panel contract")
    require(text, "pendingRecoveryHandoffRevenueEur:0", "zero revenue QA contract")
    require(text, "recovery_handoff_pending remain 0 EUR", "weak pattern rejection text")
    require(text, "manually verify bank/Revolut payment before marking paid", "manual verification guard")
    require(text, "Order ID, leadId, verified payment reference and admin verification note are required.", "paid gate required fields")

    forbid(text, "handoffRevenueEur:19", "fake handoff revenue")
    forbid(text, "pendingRecoveryHandoffRevenueEur:19", "fake QA handoff revenue")
    forbid(text, "recovery_handoff_pending counts as revenue", "weak revenue pattern")
    forbid(text, "reminder_sent counts as revenue", "weak reminder revenue pattern")

    print("PASS qpv paid confirmation recovery handoff regression")


if __name__ == "__main__":
    main()
