#!/usr/bin/env python3
"""Regression gate for the 29 EUR Auto Parts Price Finder payable order path.

This is a buyer/payment-path gate, not a dashboard or summary gate. It requires
an executable order form, a real payment destination gate, payment reference,
CSV export, APF-specific paid-confirmation and fulfillment handoff, plus a
fallback invoice request email when the payment provider destination is not
configured, while keeping confirmed revenue at 0 EUR until a verified paid event
exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PAGE = ROOT / "website" / "auto-parts-price-finder.html"
ORDER_PAGE = ROOT / "website" / "auto-parts-bank-transfer-order.html"
APF_PAID_PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PRODUCT_PAGE.exists(), "missing Auto Parts Price Finder product page")
    require(ORDER_PAGE.exists(), "missing bank-transfer order page")
    require(APF_PAID_PAGE.exists(), "missing APF paid confirmation page")
    product = PRODUCT_PAGE.read_text(encoding="utf-8")
    order = ORDER_PAGE.read_text(encoding="utf-8")
    paid = APF_PAID_PAGE.read_text(encoding="utf-8")

    product_markers = [
        "auto-parts-bank-transfer-order.html?product=auto-parts-price-finder&priceEur=29",
        "Paid confirmation",
        "bank-transfer order intent as revenue",
        "Payment path: auto-parts-bank-transfer-order.html?product=${PRODUCT}&priceEur=${PRICE_EUR}",
    ]
    for marker in product_markers:
        require(marker in product, f"product page missing bank-transfer handoff marker: {marker}")

    order_markers = [
        "Buy Auto Parts Price Finder audit — 29 €",
        "Executable revenue path · 29 EUR · payable order gate",
        "APF direct verified-paid handoff",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const SELLER='MB Marių auto'",
        "const CONTACT_EMAIL='automariu@gmail.com'",
        "const STORAGE_KEY='apfPayableOrders'",
        "const APF_PAID_CONFIRMATION_PAGE='./auto-parts-paid-confirmation.html'",
        "function createOrder()",
        "function exportOrders()",
        "function getPaymentDestination()",
        "function paymentDestinationIsConfigured()",
        "function buildApfPaidConfirmationUrl(order)",
        "paymentReference",
        "APF29-",
        "status:'awaiting_verified_payment'",
        "revenueCountedEur:0",
        "auto-parts-paid-confirmation.html?",
        "paid-fulfillment.html?",
        "auto-parts-payable-orders.csv",
        "apfPaidEventLedger",
    ]
    for marker in order_markers:
        require(marker in order, f"order page missing executable marker: {marker}")

    apf_confirmation_handoff_markers = [
        "Open APF paid confirmation",
        "buildApfPaidConfirmationUrl(order)",
        "buyerEmail:order.buyerEmail",
        "buyerName:order.buyerName",
        "vehicle:order.vehicle",
        "part:[order.part,order.oem].filter(Boolean).join(' / ')",
        "APF verified-paid handoff ready",
        "Open APF paid confirmation link and paste proof details",
        "generic paid-confirmation links",
    ]
    for marker in apf_confirmation_handoff_markers:
        require(marker in order, f"order page missing APF paid-confirmation handoff marker: {marker}")

    require(
        "./paid-confirmation.html?product=auto-parts-price-finder" not in order,
        "order page must not send APF buyers to the generic paid confirmation URL",
    )
    require(
        "auto-parts-paid-confirmation.html" in paid and "PAID_KEY='apfPaidEventLedger'" in paid,
        "APF paid confirmation page must own the APF paid ledger",
    )

    payment_gate_markers = [
        "Payment method",
        "Payment destination / URL",
        "IBAN, Revolut link, Stripe Payment Link or PayPal checkout URL",
        "payment destination required",
        "No order row is created and no revenue is counted until this is configured",
        "Pay 29 EUR to payment destination above using reference",
        "localStorage.setItem('apfPaymentDestination'",
        "paymentMethod",
        "paymentDestination",
    ]
    for marker in payment_gate_markers:
        require(marker in order, f"order page missing payable payment gate marker: {marker}")

    invoice_request_markers = [
        "Request payment invoice",
        "id=\"invoiceRequestLink\"",
        "function buildPaymentRequestMailto(order)",
        "function refreshInvoiceRequest()",
        "mailto:'+encodeURIComponent(CONTACT_EMAIL)",
        "APF 29 EUR payment request",
        "Please issue payment instructions for this 29 EUR Auto Parts Price Finder order",
        "Fallback executed: Request payment invoice now opens a prefilled email",
        "invoice request ready",
        "invoice request email",
        "this invoice request is not revenue",
    ]
    for marker in invoice_request_markers:
        require(marker in order, f"order page missing invoice-request fallback marker: {marker}")

    buyer_path_markers = [
        "Buyer email",
        "Buyer / company",
        "Vehicle",
        "Part",
        "OEM / codes",
        "Create payable 29 € order",
        "Email payment proof + order ID",
        "Fulfillment unlocks only after verified paid event",
    ]
    for marker in buyer_path_markers:
        require(marker in order, f"order page missing buyer path marker: {marker}")

    rejected_weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "order rows are revenue",
        "payment reference is revenue",
        "proof text is revenue",
        "dashboard-only progress",
        "summary-only",
        "fake paid",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in order, f"weak/fake revenue pattern must not appear in order page: {pattern}")

    print("PASS auto parts payable order regression")
    print("checked: 29 EUR buyer order form, required payment destination gate, payment reference, invoice-request fallback email, APF direct paid-confirmation handoff, proof instructions, fulfillment handoff, CSV export, and zero confirmed revenue until verified paid event")


if __name__ == "__main__":
    main()
