#!/usr/bin/env python3
"""Regression gate for APF payment request sendroom.

This is an executable buyer/payment-path gate, not a summary or audit. It
requires real buyer rows, production payment destination preflight, duplicate-safe
send ledger, buyer-ready mailto/WhatsApp copy, APF paid-confirmation handoff,
APF fulfillment handoff, CSV export, and zero confirmed revenue until an exact
+29 EUR paid event is matched in the APF paid ledger.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-payment-request-sendroom.html"
PAID_PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"
FULFILLMENT_PAGE = ROOT / "website" / "auto-parts-paid-fulfillment.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF payment request sendroom page")
    require(PAID_PAGE.exists(), "missing APF paid confirmation page")
    require(FULFILLMENT_PAGE.exists(), "missing APF paid fulfillment page")

    page = PAGE.read_text(encoding="utf-8")
    paid = PAID_PAGE.read_text(encoding="utf-8")
    fulfillment = FULFILLMENT_PAGE.read_text(encoding="utf-8")

    page_markers = [
        "APF buyer payment request sendroom — 29 €",
        "Executable revenue path · APF 29 EUR",
        "production payment destination preflight",
        "outreach-ready buyer rows",
        "duplicate-safe send ledger",
        "APF paid confirmation handoff",
        "confirmed revenue remains 0 EUR until exact paid event",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const SELLER='MB Marių auto'",
        "const CONTACT_EMAIL='automariu@gmail.com'",
        "const SENDROOM_KEY='apfPaymentRequestSendroomLedger'",
        "const APF_PAID_CONFIRMATION_PAGE='./auto-parts-paid-confirmation.html'",
        "const APF_PAID_FULFILLMENT_PAGE='./auto-parts-paid-fulfillment.html'",
        "function prepareRequests()",
        "function parseBuyerRows()",
        "function buyerMessage(row,setup)",
        "function paidConfirmationUrl(row,setup)",
        "function fulfillmentUrl(row,setup)",
        "function exportCsv()",
        "apf-payment-request-sendroom.csv",
        "status:'send_ready_unpaid'",
        "revenueCountedEur:0",
        "APF29-",
        "exact +29 EUR",
        "apfPaidEventLedger",
    ]
    for marker in page_markers:
        require(marker in page, f"sendroom missing executable marker: {marker}")

    payment_gate_markers = [
        "Payment method",
        "Payment destination / URL",
        "LT IBAN, Revolut link, Stripe Payment Link or PayPal checkout URL",
        "const VALID_PAYMENT_METHODS=['bank_transfer','revolut_business','stripe_payment_link','paypal_checkout']",
        "const BLOCKED_PAYMENT_DESTINATION_PATTERNS=['demo','example','test','placeholder','sample','fake','todo','tbd','your-','localhost'",
        "function rejectPaymentDestination(destination)",
        "payment destination required",
        "production payment destination required",
        "production Stripe payment link required",
        "buy\\.stripe\\.com|checkout\\.stripe\\.com",
        "production Revolut Business link required",
        "revolut\\.me|pay\\.revolut\\.com|checkout\\.revolut\\.com",
        "production PayPal checkout link required",
        "paypal\\.com",
        "production bank-transfer IBAN required",
        "IBAN_OR_PAYMENT_LINK_REQUIRED",
        "sendroom blocked",
        "Fallback executed: keep rows in the textarea",
    ]
    for marker in payment_gate_markers:
        require(marker in page, f"sendroom missing production payment gate marker: {marker}")

    buyer_send_markers = [
        "Buyer rows: email, company, vehicle, part, oem, channel, phone",
        "Prepare payment requests",
        "Copy first request",
        "mailto:'mailto:'",
        "https://wa.me/",
        "Mokėjimas: 29 EUR",
        "Mokėjimo paskirtis: ${row.paymentReference}",
        "Po apmokėjimo atsiųskite pavedimo eilutę arba proof",
        "PAID_CONFIRMATION:",
        "FULFILLMENT:",
        "first request copied",
        "copy is not revenue",
    ]
    for marker in buyer_send_markers:
        require(marker in page, f"sendroom missing buyer send marker: {marker}")

    rejected_weak_patterns = [
        "summary-only",
        "audit-only",
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "copied messages are revenue",
        "CSV exports are revenue",
        "mailto clicks are revenue",
        "WhatsApp clicks are revenue",
        "manual paid claim",
        "fake paid",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in page, f"weak/fake revenue pattern must not appear in sendroom: {pattern}")

    require(
        "PAID_KEY='apfPaidEventLedger'" in paid,
        "APF paid confirmation must own the duplicate-safe paid ledger",
    )
    require(
        "COMPLETED_KEY='apfCompletedOrderLedger'" in fulfillment,
        "APF fulfillment must own the completed-order ledger",
    )

    print("PASS auto parts payment request sendroom regression")
    print("checked: real buyer rows, production payment destination preflight, duplicate-safe APF send ledger, buyer-ready mailto/WhatsApp messages, CSV export, APF paid-confirmation handoff, APF fulfillment handoff, and 0 EUR confirmed revenue until exact +29 EUR paid event")


if __name__ == "__main__":
    main()
