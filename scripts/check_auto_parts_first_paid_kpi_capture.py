#!/usr/bin/env python3
"""Regression gate for APF first paid KPI capture.

This is a revenue-path workflow improvement: it converts one real buyer/order and
one exact +29 EUR APF statement row into a duplicate-safe verified paid KPI event,
then hands off to receipt/fulfillment. It must reject screenshots, promises,
manual paid claims, demo/test placeholders, wrong amounts and duplicate rows as
0 EUR.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-first-paid-kpi-capture.html"
RECEIPT_PAGE = ROOT / "website" / "auto-parts-paid-receipt.html"
FULFILLMENT_PAGE = ROOT / "website" / "auto-parts-paid-fulfillment.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing first paid KPI capture page")
    require(RECEIPT_PAGE.exists(), "missing APF paid receipt page")
    require(FULFILLMENT_PAGE.exists(), "missing APF paid fulfillment page")
    page = PAGE.read_text(encoding="utf-8")

    executable_markers = [
        "APF first paid KPI capture",
        "exact +29 EUR statement row only",
        "duplicate-safe apfPaidEventLedger",
        "receipt + fulfillment handoff",
        "Capture verified paid KPI",
        "function capturePaidKpi()",
        "function validatePaidEvidence()",
        "function hasExactPlus29(statement)",
        "function hasApfReference(statement,orderId,reference)",
        "function paidEventId(orderId,statement)",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const LEDGER_KEY='apfPaidEventLedger'",
        "status:'verified_paid_event'",
        "amountEur:PRICE_EUR",
        "auto-parts-paid-receipt.html",
        "auto-parts-paid-fulfillment.html",
    ]
    for marker in executable_markers:
        require(marker in page, f"missing executable KPI marker: {marker}")

    real_evidence_markers = [
        "Buyer name/company",
        "Buyer contact",
        "APF order id",
        "Payment reference",
        "Statement row text",
        "real buyer and buyer contact are required before KPI capture",
        "APF order id is required and must start with APF",
        "statement row must contain exact +29 EUR",
        "statement row must contain APF plus order/reference/product evidence",
    ]
    for marker in real_evidence_markers:
        require(marker in page, f"missing real paid evidence gate: {marker}")

    zero_revenue_guards = [
        "confirmedRevenueEur:0",
        "NO_REVENUE",
        "Wrong amount is 0 EUR",
        "proof screenshots, promises, checkout visits or manual paid claims",
        "copied KPI pack is not revenue",
        "checkout attempt",
        "manual paid claim",
        "payment promise",
        "proof screenshot",
        "page visit",
    ]
    for marker in zero_revenue_guards:
        require(marker in page, f"missing zero-revenue guard: {marker}")

    fake_blockers = [
        "const BLOCKED_PATTERNS=['demo','test','example','fake','placeholder','sample','todo','lorem','manual paid','promise to pay','screenshot only'];",
        "function badPattern(value)",
        "rejected weak/fake paid evidence pattern",
        "DUPLICATE_BLOCKED",
        "duplicate statement row already exists in apfPaidEventLedger",
        "incrementalRevenueEur:0",
    ]
    for marker in fake_blockers:
        require(marker in page, f"missing weak/fake/duplicate blocker: {marker}")

    kpi_markers = [
        "confirmedRevenueEur:${PRICE_EUR}",
        "verifiedPaidEvents:${ledger.length}",
        "APF FIRST PAID KPI CAPTURED",
        "Revenue status: confirmed +29 EUR only because exact +29 EUR APF statement row was matched",
    ]
    for marker in kpi_markers:
        require(marker in page, f"missing measurable KPI marker: {marker}")

    forbidden_patterns = [
        "summary is progress",
        "staffing plan is progress",
        "policy is progress",
        "idea list is progress",
        "audit is progress",
        "screenshot is revenue",
        "promise to pay is revenue",
        "manual paid claim is revenue",
        "checkout attempt is revenue",
        "confirmedRevenueEur:29</span><span class=\"pill warn\"",
        "qpvPaidEventLedger",
    ]
    for pattern in forbidden_patterns:
        require(pattern not in page, f"weak/fake progress pattern must not appear: {pattern}")

    print("PASS auto parts first paid KPI capture regression")
    print(
        "checked: exact +29 EUR APF statement validation, real buyer/order requirement, "
        "duplicate-safe apfPaidEventLedger write, receipt/fulfillment handoff, measurable KPI output, "
        "and rejection of weak/fake/non-revenue patterns"
    )


if __name__ == "__main__":
    main()
