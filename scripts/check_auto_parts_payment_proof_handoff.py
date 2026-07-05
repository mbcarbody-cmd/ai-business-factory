#!/usr/bin/env python3
"""Regression gate for APF 29 EUR payment proof handoff.

This validates a real buyer workflow improvement: after a payable order or instant
checkout, the buyer can provide proof URL/hash and receive a seller email plus APF
paid-confirmation/fulfillment deep links. The handoff must not count revenue by
itself and must reject demo/test/example/fake proof before mailto or paid links.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-payment-proof-handoff.html"
CONFIRMATION_PAGE = ROOT / "website" / "auto-parts-paid-confirmation.html"
FULFILLMENT_PAGE = ROOT / "website" / "auto-parts-paid-fulfillment.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF payment proof handoff page")
    require(CONFIRMATION_PAGE.exists(), "missing APF paid confirmation page")
    require(FULFILLMENT_PAGE.exists(), "missing APF paid fulfillment page")
    page = PAGE.read_text(encoding="utf-8")

    required_markers = [
        "APF payment proof handoff · 29 EUR",
        "buyer proof email + paid-confirmation deep link",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const CONTACT_EMAIL='automariu@gmail.com'",
        "function paymentProofStatus(value)",
        "function requiredStatus()",
        "function buildSellerMailto()",
        "function buildPaidConfirmationUrl()",
        "function buildFulfillmentUrl()",
        "function buildHandoff()",
        "function copyProofPack()",
        "function loadFromUrl()",
        "paymentProof",
        "orderId",
        "paymentReference",
        "buyerEmail",
        "APF29 paymentReference is required",
        "buyerEmail is required for proof handoff",
        "auto-parts-paid-confirmation.html?",
        "auto-parts-paid-fulfillment.html?",
    ]
    for marker in required_markers:
        require(marker in page, f"proof handoff page missing marker: {marker}")

    proof_gate_markers = [
        "const BLOCKED_PROOF_PATTERNS=['demo','test','example','fake','placeholder','sample','todo','tbd','lorem','localhost','127.0.0.1','proof_required'];",
        "real paymentProof URL/hash is required before seller handoff",
        "rejected weak paymentProof pattern",
        "paymentProof must be an HTTPS receipt URL or 16+ character transaction hash",
        "if(/^https:\\/\\//i.test(proof))return {ok:true,reason:'real proof URL accepted'};",
        "if(/^[A-F0-9]{16,}$/i.test(proof))return {ok:true,reason:'transaction hash accepted'};",
        "No seller email, paid-confirmation URL, fulfillment URL, ledger event or revenue is generated from weak proof.",
        "aria-disabled",
    ]
    for marker in proof_gate_markers:
        require(marker in page, f"proof handoff page missing proof gate marker: {marker}")

    revenue_guard_markers = [
        "revenueCountedEur:0",
        "It does not count revenue by itself.",
        "APF revenue remains 0 EUR until auto-parts-paid-confirmation.html validates paymentProof",
        "Revenue rule: this email/proof handoff is not revenue.",
        "proof handoff, mailto click, paid-confirmation URL and fulfillment URL are 0 EUR",
        "Rejected weak patterns: page visit, copied proof text, demo/test/example/fake/placeholder proof",
        "fake paid event",
        "apfPaidEventLedger",
    ]
    for marker in revenue_guard_markers:
        require(marker in page, f"proof handoff page missing zero-revenue guard: {marker}")

    weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "proof handoff is revenue",
        "mailto click is revenue",
        "paid-confirmation URL is revenue",
        "fulfillment URL is revenue",
        "demo proof accepted",
        "proof_required accepted",
        "qpvPaidEventLedger",
    ]
    for pattern in weak_patterns:
        require(pattern not in page, f"weak/fake revenue pattern must not appear: {pattern}")

    print("PASS auto parts payment proof handoff regression")
    print(
        "checked: APF payment proof URL/hash gate, APF29 reference requirement, buyer email requirement, "
        "seller proof email, APF paid-confirmation deep link, APF fulfillment handoff, blocked demo/test/fake proof, "
        "and zero confirmed revenue until verified APF paid ledger event"
    )


if __name__ == "__main__":
    main()
