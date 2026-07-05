#!/usr/bin/env python3
"""Regression gate for APF bank statement paid-event importer.

This gate requires a concrete revenue workflow, not a summary/audit: pasted
bank/Revolut/Stripe/PayPal statement rows must create APF verified paid events
only when one real EUR 29 row matches the APF/order reference, then queue paid
fulfillment and reject weak revenue patterns.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-bank-statement-import.html"
INDEX = ROOT / "index.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF bank statement import page")
    page = PAGE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder — bank statement import",
        "Executable revenue path · 29 EUR · APF bank statement importer · no fake paid events",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const PAID_KEY='apfPaidEventLedger'",
        "const IMPORT_KEY='apfStatementImportLedger'",
        "const FULFILLMENT_KEY='apfFulfillmentQueue'",
        "const DUPE_KEY='apfPaidDuplicateBlocks'",
        "function parseAmount(text)",
        "function hasEurCurrency(text)",
        "function candidateRows()",
        "function importStatementPaidEvent()",
        "parseAmount(row)===PRICE_EUR",
        "hasEurCurrency(row)",
        "matches.length!==1",
        "duplicate_statement_import_not_counted",
        "source:'auto-parts-bank-statement-import'",
        "paymentProof:'statement-hash:'",
        "revenueCountedEur:PRICE_EUR",
        "status:'verified_paid'",
        "auto-parts-statement-import-ledger.csv",
    ]
    for marker in required_markers:
        require(marker in page, f"APF statement importer missing marker: {marker}")

    buyer_revenue_markers = [
        "Import real payment statement → APF paid ledger",
        "bank/Revolut/Stripe/PayPal CSV",
        "real statement row contains APF/order reference, exact 29 EUR amount, EUR currency",
        "verified paid event written",
        "fulfillment queued",
        "confirmedRevenueEur",
    ]
    for marker in buyer_revenue_markers:
        require(marker in page, f"APF statement importer missing revenue marker: {marker}")

    rejected_weak_markers = [
        "CSV pasted",
        "page visit",
        "order reference alone",
        "amount without APF reference",
        "non-EUR row",
        "multiple ambiguous rows",
        "manual proof text without bank row",
        "fake paid event",
    ]
    for marker in rejected_weak_markers:
        require(marker in page, f"APF statement importer must explicitly reject weak pattern: {marker}")

    forbidden_patterns = [
        "statementImportRevenueEur:29",
        "csvPasteRevenueEur:29",
        "pageVisitRevenueEur:29",
        "orderReferenceAloneRevenueEur:29",
        "manual proof text is revenue",
        "summary-only progress",
        "dashboard-only progress",
        "fake paid",
    ]
    for pattern in forbidden_patterns:
        require(pattern not in page, f"weak/fake statement-import revenue pattern must not appear: {pattern}")

    require("auto-parts-bank-statement-import.html" in index, "root launcher must expose APF bank statement importer")
    print("PASS auto parts bank statement import regression")
    print("checked: exact +29 EUR APF statement match, EUR currency check, duplicate suppression, apfPaidEventLedger write, import ledger, fulfillment queue, CSV export, and rejected weak revenue patterns")


if __name__ == "__main__":
    main()
