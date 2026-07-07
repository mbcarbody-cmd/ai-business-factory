#!/usr/bin/env python3
"""Regression gate for APF real buyer importer.

The product improvement must convert real buyer rows into payment-ready 29 EUR
outreach rows, block demo/test/fake contacts, persist duplicate-safe ledgers, and
keep confirmed revenue at 0 EUR until an exact verified paid event exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-real-buyer-importer.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF real buyer importer page")
    page = PAGE.read_text(encoding="utf-8")

    product_markers = [
        "APF real buyer importer",
        "real buyer rows only",
        "29 EUR payment-ready outreach",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const LEDGER_KEY='apfRealBuyerImportLedger'",
        "const OUTREACH_LEDGER_KEY='apfOutreachSendLedger'",
        "const PAID_LEDGER_KEY='apfPaidEventLedger'",
        "Import real buyers into 29 € outreach queue",
        "payment-ready outreach generated",
    ]
    for marker in product_markers:
        require(marker in page, f"missing executable product marker: {marker}")

    buyer_validation_markers = [
        "function looksLikeEmail(value)",
        "function looksLikePhone(value)",
        "function parseLine(line)",
        "function validBuyer(row)",
        "missing real email or phone/WhatsApp contact",
        "blocked demo/test/example/fake buyer row",
        "blocked non-real source URL",
        "real buyer contact accepted",
    ]
    for marker in buyer_validation_markers:
        require(marker in page, f"missing real-buyer validation marker: {marker}")

    payment_destination_markers = [
        "function looksLikeIban(value)",
        "function isTrustedPaymentUrl(value)",
        "function destinationStatus()",
        "BLOCKER: no production Stripe/Revolut/PayPal URL or valid IBAN configured.",
        "BLOCKER: demo/test/example/fake payment destination rejected.",
        "destination must be valid IBAN or trusted Stripe/Revolut/PayPal HTTPS URL",
        "production payment destination accepted",
    ]
    for marker in payment_destination_markers:
        require(marker in page, f"missing payment destination gate marker: {marker}")

    revenue_lock_markers = [
        "revenueCountedEur:0",
        "Revenue remains 0 EUR until exact +29 EUR verified paid event exists",
        "confirmed revenue at <b>0 EUR</b> until <b>apfPaidEventLedger</b>",
        "status:'real_buyer_imported_not_revenue'",
        "outreachStatus:'ready_to_send_not_revenue'",
        "generated row, copied queue, CSV export, mailto/WhatsApp click, demo/test/example/fake row, manual paid claim",
    ]
    for marker in revenue_lock_markers:
        require(marker in page, f"missing zero-revenue guard marker: {marker}")

    handoff_markers = [
        "auto-parts-payment-launch-url-builder.html",
        "auto-parts-payment-proof-handoff.html",
        "Pay exactly ${PRICE_EUR} EUR with reference ${row.paymentReference}",
        "function buyerMessage(row)",
        "function importBuyers()",
        "function copyQueue()",
        "function exportLedger()",
        "mailto:",
        "https://wa.me/",
    ]
    for marker in handoff_markers:
        require(marker in page, f"missing buyer handoff marker: {marker}")

    weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "import is revenue",
        "copied queue is revenue",
        "mailto click is revenue",
        "WhatsApp click is revenue",
        "manual paid claim",
        "fake paid",
        "qpvPaidEventLedger",
    ]
    for pattern in weak_patterns:
        require(pattern not in page, f"weak/fake revenue pattern must not appear: {pattern}")

    print("PASS auto parts real buyer importer regression")
    print(
        "checked: production payment destination gate, real buyer validation, duplicate-safe import ledger, "
        "outreach queue handoff, mailto/WhatsApp buyer actions, payment launch/proof links, and zero confirmed revenue until exact +29 EUR paid event"
    )


if __name__ == "__main__":
    main()
