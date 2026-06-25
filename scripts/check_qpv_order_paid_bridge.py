#!/usr/bin/env python3
"""Regression gate for QPV order-paid bridge.

The bridge is allowed to create admin shortcuts only. It must not count revenue,
write paid events, or let missing leadId/reference shortcut into paid-confirmation.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "order-paid-bridge.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, "Order → Paid Bridge", "buyer-visible page title")
    require(text, "qpvOrderLedger", "source order ledger")
    require(text, "qpvPaidEventLedger", "paid ledger read for QA baseline")
    require(text, "leadId(row)", "leadId extraction")
    require(text, "proofRef(row)", "payment reference extraction")
    require(text, "ready_for_manual_verification", "manual verification state")
    require(text, "missing_leadId", "missing leadId blocker")
    require(text, "paid-confirmation.html", "prefilled paid gate link")
    require(text, "new URLSearchParams({orderId:clean(row.orderId),leadId:leadId(row),buyer:buyer(row),paymentReference:proofRef(row)})", "prefilled paid confirmation params")
    require(text, "revenueCountedByBridgeEur:0", "zero-revenue bridge contract")
    require(text, "bridge never writes qpvPaidEventLedger", "no paid write rule")
    require(text, "bridge never writes qpvConversionLedger", "no conversion write rule")
    require(text, "missing leadId blocks paid-gate shortcut", "leadId shortcut blocker rule")
    require(text, "Fix missing leadId/reference before paid gate.", "UI blocker text")

    forbid(text, "localStorage.setItem(paidKey", "paid ledger write")
    forbid(text, "writeJson(paidKey", "paid ledger writer")
    forbid(text, "writeJson(conversionKey", "conversion ledger writer")
    forbid(text, "revenueCountedByBridgeEur:19", "fake bridge revenue")
    forbid(text, "proof_submitted counts as revenue", "weak revenue pattern")

    print("PASS qpv order-paid bridge regression")


if __name__ == "__main__":
    main()
