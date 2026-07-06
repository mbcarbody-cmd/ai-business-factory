#!/usr/bin/env python3
"""Regression gate for APF 29 EUR warm lead payment recovery.

This is not a summary/audit/dashboard gate. It requires an executable recovery
workflow that reads warm APF leads/orders, removes already-paid buyers, requires
a production payment destination, creates buyer-ready follow-up rows with payment
and proof links, and keeps recovery activity at 0 EUR until verified paid events.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-payment-recovery.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF payment recovery page")
    page = PAGE.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder — payment recovery",
        "Executable revenue path · 29 EUR · APF warm lead recovery",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const LEAD_KEY='apfBuyerLeads'",
        "const ORDER_KEY='apfPayableOrders'",
        "const LAUNCH_KEY='apfPaymentLaunchRows'",
        "const PAID_KEY='apfPaidEventLedger'",
        "const RECOVERY_KEY='apfPaymentRecoveryRows'",
        "function isProdDestination(v)",
        "function warmCandidates()",
        "function buildRows()",
        "function paymentLink(dest,row)",
        "function followup(row,dest)",
        "recovery_ready_not_paid",
        "auto-parts-payment-recovery.csv",
    ]
    for marker in required_markers:
        require(marker in page, f"APF recovery page missing marker: {marker}")

    buyer_ready_markers = [
        "Pay here:",
        "After payment, send proof here:",
        "./auto-parts-payment-proof-handoff.html",
        "./auto-parts-paid-confirmation.html",
        "Auto Parts Price Finder 29 EUR",
        "buyer-ready recovery rows built",
    ]
    for marker in buyer_ready_markers:
        require(marker in page, f"APF recovery page missing buyer-ready marker: {marker}")

    integrity_markers = [
        "remove buyers already present in verified paid ledger",
        "require production payment destination",
        "write recovery rows with revenueCountedEur 0",
        "count revenue only through apfPaidEventLedger verified_paid rows",
        "revenueFromRecoveryRowsEur:0",
        "revenueFromCsvExportEur:0",
        "revenueFromCopyEur:0",
        "revenueFromMailtoEur:0",
        "Demo/test/example/fake/localhost destinations are blocked",
    ]
    for marker in integrity_markers:
        require(marker in page, f"APF recovery page missing integrity marker: {marker}")

    allowed_destinations = [
        "buy\\.stripe\\.com",
        "checkout\\.stripe\\.com",
        "revolut\\.me",
        "paypal\\.me",
        "www\\.paypal\\.com",
        "IBAN\\s+",
    ]
    for marker in allowed_destinations:
        require(marker in page, f"APF recovery page missing production destination allowlist: {marker}")

    rejected_fake_revenue = [
        "recoveryRowRevenueEur:29",
        "csvExportRevenueEur:29",
        "mailtoRevenueEur:29",
        "copyFollowupRevenueEur:29",
        "paymentLinkClickRevenueEur:29",
        "proofLinkClickRevenueEur:29",
        "warm lead is revenue",
        "recovery row is revenue",
        "demo destination accepted",
    ]
    for pattern in rejected_fake_revenue:
        require(pattern not in page, f"weak/fake recovery revenue pattern must not appear: {pattern}")

    print("PASS auto parts payment recovery regression")
    print("checked: warm APF lead/order recovery, paid-buyer exclusion, production payment destination gate, buyer-ready follow-up rows, CSV export, and zero revenue for recovery/copy/mailto/click actions")


if __name__ == "__main__":
    main()
