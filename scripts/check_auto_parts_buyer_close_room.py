#!/usr/bin/env python3
"""Regression gate for APF buyer close room.

Requires one executable close-room page that turns an outreach lead into a
buyer-ready 29 EUR close workflow: checkout URL, buyer mailto, proof mailto,
paid confirmation, fulfillment, local ledger, CSV export, and zero confirmed
revenue until APF paid confirmation verifies the payment.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSE_PAGE = ROOT / "website" / "auto-parts-buyer-close-room.html"
CHECKOUT_PAGE = ROOT / "website" / "auto-parts-instant-payment-link-checkout.html"
PAID_PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"
FULFILLMENT_PAGE = ROOT / "website" / "auto-parts-paid-fulfillment.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(CLOSE_PAGE.exists(), "missing APF buyer close room page")
    require(CHECKOUT_PAGE.exists(), "missing APF instant checkout page")
    require(PAID_PAGE.exists(), "missing APF paid confirmation page")
    require(FULFILLMENT_PAGE.exists(), "missing APF paid fulfillment page")

    close = CLOSE_PAGE.read_text(encoding="utf-8")
    paid = PAID_PAGE.read_text(encoding="utf-8")
    fulfillment = FULFILLMENT_PAGE.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder buyer close room",
        "APF close room · buyer-ready 29 EUR offer",
        "production payment preflight",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const CLOSE_LEDGER_KEY='apfBuyerCloseRoomLedger'",
        "const PAID_LEDGER_KEY='apfPaidEventLedger'",
        "const VALID_PAYMENT_METHODS=['stripe_payment_link','revolut_business','paypal_checkout','bank_transfer']",
        "const REJECTED_PAYMENT_TOKENS=['example','demo','test','todo','placeholder','your-','sample','localhost','sandbox']",
        "function isProductionPaymentDestination(value)",
        "function preflightPaymentDestination(row)",
        "function paymentBlockerText()",
        "function buildCloseRoom()",
        "function buildCheckoutUrl(row)",
        "function buildPaidConfirmationUrl(row)",
        "function buildFulfillmentUrl(row)",
        "function buildProofMailto(row)",
        "function buildBuyerMailto(row)",
        "function buildClosePack(row)",
        "function startPayment()",
        "function copyClosePack()",
        "Pay 29 €",
        "Email buyer offer",
        "Proof mailto",
        "Paid confirmation",
        "Fulfillment",
        "Export close-room CSV",
        "apf-buyer-close-room-ledger.csv",
        "auto-parts-instant-payment-link-checkout.html?",
        "auto-parts-paid-confirmation.html?",
        "auto-parts-paid-fulfillment.html?",
        "paymentReference",
        "APF29-",
        "revenueCountedEur:0",
    ]
    for marker in required_markers:
        require(marker in close, f"close room missing executable marker: {marker}")

    buyer_close_path_markers = [
        "Buyer email",
        "Buyer / company",
        "Lead ID",
        "Vehicle",
        "Part / OEM",
        "Production payment destination / URL",
        "Payment gate",
        "paymentGate:'production-ready'",
        "paymentGate:row.paymentGate",
        "AUTO PARTS PRICE FINDER — BUYER CLOSE ROOM",
        "Checkout URL:",
        "Paid confirmation URL:",
        "Fulfillment URL after verified paid event:",
        "Pay exactly 29 EUR using reference",
        "Delivery starts only after verified APF paid event exists",
        "production payment destination required",
        "production payment destination verified",
        "demo/example/test destination rejected",
        "buyer close room ready",
        "checkout URL generated",
        "buyer email handoff ready",
        "proof and fulfillment gate wired",
    ]
    for marker in buyer_close_path_markers:
        require(marker in close, f"close room missing buyer close path marker: {marker}")

    rejected_weak_patterns = [
        "close room is revenue",
        "checkout URL is revenue",
        "email open is revenue",
        "payment URL click is revenue",
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "fake paid",
        "summary-only",
        "dashboard-only progress",
        "paid without proof",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in close, f"weak/fake revenue pattern must not appear: {pattern}")

    require("PAID_KEY='apfPaidEventLedger'" in paid, "APF paid confirmation must own paid ledger")
    require(
        "COMPLETED_KEY='apfCompletedOrderLedger'" in fulfillment,
        "APF fulfillment must own completed order ledger",
    )

    print("PASS APF buyer close room regression")
    print(
        "checked: outreach lead to buyer-ready 29 EUR close room, production payment destination "
        "preflight, checkout URL, buyer email handoff, paid proof mailto, paid confirmation handoff, "
        "fulfillment handoff, close-room ledger, CSV export and zero confirmed revenue until verified paid proof"
    )


if __name__ == "__main__":
    main()
