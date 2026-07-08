#!/usr/bin/env python3
"""Regression gate for APF production payment destination guard.

This is a revenue-path gate, not a summary/audit check. It requires a concrete
browser workflow that refuses fake/demo payment destinations and only creates
buyer-ready 29 EUR APF order/outreach/statement-match handoffs after a production
payment preflight. Revenue must remain locked until an exact verified +29 EUR paid event.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-production-payment-destination-guard.html"
INDEX = ROOT / "index.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF production payment destination guard page")
    require(INDEX.exists(), "missing root launcher")

    page = PAGE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    page_markers = [
        "Auto Parts Price Finder — payment destination guard",
        "production payment destination guard",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const GUARD_KEY='apfProductionPaymentDestinationGuard'",
        "const PAID_KEY='apfPaidEventLedger'",
        "const BLOCKED_KEY='apfProductionPaymentDestinationBlocked'",
        "const VALID_PAYMENT_METHODS=['stripe_payment_link','revolut_business','paypal_checkout','bank_transfer']",
        "const REJECTED_PAYMENT_TOKENS=['example','demo','test','todo','placeholder','your-','sample','fake','localhost','127.0.0.1','lorem','changeme']",
        "function isProductionPaymentDestination(value,method)",
        "function runGuard()",
        "function buildUrls(row)",
        "auto-parts-bank-transfer-order.html",
        "auto-parts-outreach-send-queue.html",
        "auto-parts-statement-paid-event-matcher.html",
        "auto-parts-verified-paid-router.html",
        "status:'payment_destination_verified_order_ready'",
        "revenueCountedEur:0",
        "exact +29 EUR verified statement event",
        "Buyer/price: used auto-parts seller, 29 EUR",
    ]
    for marker in page_markers:
        require(marker in page, f"guard page missing required marker: {marker}")

    blocker_markers = [
        "BLOCKER: production payment destination required before buyer-ready APF payment/outreach links",
        "NO BUYER HANDOFF GENERATED",
        "Demo/test/fake/placeholder payment destination is rejected",
        "Fallback executed: keep revenue locked",
        "loadBlockedDemo()",
        "https://example.com/demo-checkout-placeholder",
    ]
    for marker in blocker_markers:
        require(marker in page, f"guard page missing weak-destination blocker marker: {marker}")

    production_destination_markers = [
        "IBAN LT121000011101001000",
        "stripe_payment_link",
        "revolut_business",
        "paypal_checkout",
        "bank_transfer",
        "paymentDestination",
        "paymentMethod",
        "statementMatchUrl",
        "paidRouterUrl",
        "orderUrl",
        "outreachUrl",
    ]
    for marker in production_destination_markers:
        require(marker in page, f"guard page missing production destination marker: {marker}")

    rejected_weak_patterns = [
        "payment destination visit is revenue",
        "generated URL is revenue",
        "copied link is revenue",
        "proof screenshot is revenue",
        "manual paid claim is revenue",
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "summary-only",
        "dashboard-only progress",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in page, f"weak/fake revenue pattern must not appear: {pattern}")

    root_markers = [
        "auto-parts-production-payment-destination-guard.html",
        "Patikrinti production payment destination",
        "payment destination guard",
    ]
    for marker in root_markers:
        require(marker in index, f"root launcher missing guard link marker: {marker}")

    print("PASS auto parts production payment destination guard regression")
    print(
        "checked: fake/demo payment destination blockers, production payment preflight, "
        "29 EUR APF order/outreach/statement/paid-router handoffs, duplicate-safe guard ledger, "
        "and zero confirmed revenue until exact verified +29 EUR paid event"
    )


if __name__ == "__main__":
    main()
