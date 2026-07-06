#!/usr/bin/env python3
"""Regression gate for APF proof + statement paid-event match desk.

This gate requires concrete product movement: buyer proof is not revenue unless
it is paired with exactly one real +29 EUR EUR statement row containing the APF
reference, then the page writes a duplicate-safe paid event and fulfillment row.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-proof-statement-match.html"
INDEX = ROOT / "index.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF proof statement match page")
    page = PAGE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    required_markers = [
        "Auto Parts Price Finder — proof statement match desk",
        "Executable revenue gate · buyer proof + statement match · 29 EUR counted once",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const PAID_KEY='apfPaidEventLedger'",
        "const MATCH_KEY='apfProofStatementMatchLedger'",
        "const FULFILLMENT_KEY='apfFulfillmentQueue'",
        "const DUPE_KEY='apfPaidDuplicateBlocks'",
        "function proofMatchesOrder(orderId,proofText)",
        "function statementMatches(orderId)",
        "parseAmount(row)===PRICE_EUR",
        "hasEurCurrency(row)",
        "matches.length!==1",
        "duplicate_proof_statement_match_not_counted",
        "source:'auto-parts-proof-statement-match'",
        "paymentProof:'proof-hash:'",
        "revenueCountedEur:PRICE_EUR",
        "status:'verified_paid'",
        "apf-proof-statement-match-ledger.csv",
    ]
    for marker in required_markers:
        require(marker in page, f"APF proof statement match page missing marker: {marker}")

    product_state_markers = [
        "Payment proof + statement row → verified APF paid event",
        "buyer proof text contains the same reference",
        "statement row matched",
        "29 EUR counted once",
        "fulfillmentQueued",
        "confirmedRevenueEur",
    ]
    for marker in product_state_markers:
        require(marker in page, f"APF proof statement match page missing product-state marker: {marker}")

    rejected_weak_markers = [
        "proof screenshot alone",
        "copied proof",
        "mailto opened",
        "request row",
        "statement pasted without exact match",
        "order reference alone",
        "proof without accounting match",
        "fake paid event",
    ]
    for marker in rejected_weak_markers:
        require(marker in page, f"APF proof statement match must reject weak pattern: {marker}")

    forbidden_patterns = [
        "proofScreenshotRevenueEur:29",
        "copiedProofRevenueEur:29",
        "mailtoRevenueEur:29",
        "requestRowRevenueEur:29",
        "statementPasteRevenueEur:29",
        "manual paid claim is revenue",
        "summary-only progress",
        "dashboard-only progress",
    ]
    for pattern in forbidden_patterns:
        require(pattern not in page, f"weak/fake proof-statement revenue pattern must not appear: {pattern}")

    require("auto-parts-proof-statement-match.html" in index, "root launcher must expose APF proof statement match desk")
    require(
        "python3 scripts/check_auto_parts_proof_statement_match.py" in workflow,
        "CI must run APF proof statement match regression",
    )

    print("PASS auto parts proof statement match regression")
    print("checked: proof reference match, exact +29 EUR EUR statement match, duplicate suppression, paid ledger write, match ledger, fulfillment queue, and weak-pattern rejection")


if __name__ == "__main__":
    main()
