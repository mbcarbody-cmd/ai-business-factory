#!/usr/bin/env python3
"""Regression gate for QPV Revenue Command Center abandoned-checkout recovery navigation.

The command center is the operator's highest-value revenue screen. It must expose
checkout recovery directly and pass orderId into the recovery workflow without
counting recovery, proof, reminder, quote, or checkout activity as paid revenue.
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

    require(text, 'href="./abandoned-checkout-recovery.html"', "top-level abandoned checkout recovery navigation")
    require(text, "Run checkout recovery", "collect-revenue recovery action")
    require(text, "isRecoverableUnpaid(row)", "recoverable unpaid order detector")
    require(text, "recoverableUnpaidOrders", "recoverable-order KPI state")
    require(text, "link('./abandoned-checkout-recovery.html',{orderId:row.orderId})", "per-order recovery URL with orderId")
    require(text, "Checkout recovery", "per-order recovery action label")
    require(text, "recovery action links preserve orderId when present", "QA rule for orderId handoff")
    require(text, "abandoned checkout recovery link is visible from command center", "QA rule for visible recovery navigation")
    require(text, "abandoned checkout recovery is conversion/follow-up only and never paid revenue", "QA rule for zero-revenue recovery")
    require(text, "revenueDeltaFromThisPageEur:0", "command center zero revenue side-effect")
    require(text, "paid revenue comes only from deduplicated qpvPaidEventLedger events", "paid-ledger-only revenue rule")

    forbid(text, "recovery counts as revenue", "recovery-as-sale wording")
    forbid(text, "abandoned checkout is paid", "abandoned-checkout-as-paid wording")
    forbid(text, "checkout is paid", "checkout-as-sale wording")
    forbid(text, "quote accepted is paid", "quote-as-sale wording")
    forbid(text, "proof is paid", "proof-as-sale wording")
    forbid(text, "revenueCountedEur:19", "hard-coded fake revenue")

    print("PASS qpv revenue command center recovery navigation regression")


if __name__ == "__main__":
    main()
