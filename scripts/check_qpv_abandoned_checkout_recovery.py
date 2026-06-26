#!/usr/bin/env python3
"""Regression gate for the QPV abandoned checkout recovery workflow.

The workflow may create recovery links and conversion events, but must not count
abandoned checkout, recovery, proof, or quote acceptance as confirmed revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "abandoned-checkout-recovery.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, "abandonAfterMinutes=30", "30-minute abandonment gate")
    require(text, "leadId:clean(row.leadId)", "leadId preservation")
    require(text, "orderId:clean(row.orderId||row.id)", "orderId preservation")
    require(text, "checkoutId:clean(row.checkoutId||row.sessionId||row.orderId)", "checkout/session preservation")
    require(text, "recoveryId(row)", "deterministic recovery id")
    require(text, "existing.has(id)&&existing.get(id).status!=='expired'", "duplicate active recovery prevention")
    require(text, "recoveryHref(session)", "buyer-ready recovery link generation")
    require(text, "priceEur:String(row.priceEur||priceEur)", "original price preserved in recovery URL")
    require(text, "eventType:'recovery_created'", "conversion event recorded")
    require(text, "revenueDeltaEur:0", "recovery event zero-revenue guard")
    require(text, "revenueCountedEur:0", "recovery row zero-revenue guard")
    require(text, "confirmedRevenueSource:'verified paid events only'", "paid-ledger-only revenue rule")
    require(text, "checkout abandoned is not paid", "abandoned checkout rejected as sale")
    require(text, "recovery completed is not paid without verified paid event", "completed recovery rejected as paid")
    require(text, "payment proof is not revenue", "proof rejected as revenue")
    require(text, "quote accepted is not paid", "quote acceptance rejected as paid")
    require(text, "Export is not revenue", "CSV export no-revenue message")

    forbid(text, "revenueDeltaEur:19", "fake recovery revenue")
    forbid(text, "recovery_created is paid", "recovery-created-as-paid wording")
    forbid(text, "abandoned checkout counts as paid", "abandoned checkout as sale")
    forbid(text, "recovery completed counts as revenue", "completed recovery as revenue")
    forbid(text, "proof_submitted counts as revenue", "proof as sale")
    forbid(text, "quote accepted counts as paid", "quote as sale")

    print("PASS qpv abandoned checkout recovery regression")


if __name__ == "__main__":
    main()
