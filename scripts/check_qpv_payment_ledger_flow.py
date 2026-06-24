#!/usr/bin/env python3
"""Regression checks for the QPV payment proof ledger fallback page.

This is a static-code gate because the product is a GitHub Pages/browser-only flow.
It rejects fake payment success and verifies the proof page writes to the same
localStorage ledger used by checkout/admin while keeping confirmed revenue gated.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "payment-ledger.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def reject(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"forbidden {label}: {needle}")


def main() -> None:
    html = PAGE.read_text(encoding="utf-8")
    require(html, "PAYMENT PROOF LEDGER SYNC", "buyer-visible ledger sync heading")
    require(html, "ledgerKey='qpvOrderLedger'", "shared checkout/admin order ledger key")
    require(html, "proofKey='qpvPaymentProofLedger'", "dedicated payment proof ledger key")
    require(html, "function upsertProof(proof)", "proof upsert workflow")
    require(html, "paymentStatus:'proof_submitted_manual_review'", "manual review status")
    require(html, "revenueCountedEur:0", "zero revenue proof gate")
    require(html, "confirmedRevenue(rows)", "confirmed revenue reducer")
    require(html, "Verify real payment before changing paymentStatus to paid", "admin paid-gate instruction")
    require(html, "Download ledger", "admin/export handoff")
    require(html, "mailto:automariu@gmail.com", "buyer proof handoff")
    reject(html, "paymentStatus:'paid'", "fake paid assignment from proof page")
    reject(html, "revenueCountedEur:19", "fake revenue from proof page")
    print("PASS qpv payment ledger flow: proof is saved into qpvOrderLedger without counting revenue")


if __name__ == "__main__":
    main()
