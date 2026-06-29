#!/usr/bin/env python3
"""Regression gate for QPV checkout -> payment ledger source attribution.

Payment proof is the last pre-revenue buyer action before manual verification.
It must preserve source attribution from checkout into proof rows, the shared
order ledger, paid-gate URLs and conversion events without counting revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYMENT_LEDGER = ROOT / "website" / "payment-ledger.html"
CHECKOUT = ROOT / "website" / "checkout.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    payment = read(PAYMENT_LEDGER)
    checkout = read(CHECKOUT)

    checkout_markers = [
        "function paymentHref(order)",
        "source:order.source",
        "./payment-ledger.html?",
        "Payment ledger page receives the same orderId, leadId, paymentReference and source.",
    ]
    for marker in checkout_markers:
        require(marker in checkout, f"checkout must send source into payment ledger: {marker}")

    required_payment_markers = [
        "SOURCE ATTRIBUTION",
        "id=\"source\"",
        "function sourceFrom()",
        "source:data.source||sourceFrom()",
        "source,attribution:'payment_ledger_proof_handoff'",
        "Source: ${proof.source}",
        "source:proof.source,attribution:proof.attribution",
        "version:'qpv-conversion-ledger-v3-payment-source-handoff'",
        "paid-confirmation.html?",
        "source:proof.source",
        "source ${lastProof.source}",
        "revenueCountedEur:0",
        "confirmedRevenue remains 0",
    ]
    for marker in required_payment_markers:
        require(marker in payment, f"payment ledger missing attribution/revenue marker: {marker}")

    rejected_code_patterns = [
        "source:'payment-ledger'",
        "source:'unknown'",
        "source:'checkout'",
        "revenueCountedEur:19",
        "confirmedRevenueEur:19",
        "paymentStatus:'paid'",
    ]
    for pattern in rejected_code_patterns:
        require(pattern not in payment, f"payment ledger must reject weak executable pattern: {pattern}")
        require(pattern not in checkout, f"checkout must reject weak executable pattern: {pattern}")

    required_rejection_copy = [
        "No fake paid state",
        "No proof that loses source attribution",
        "no confirmed EUR from manual-transfer text",
    ]
    for marker in required_rejection_copy:
        require(marker in payment, f"payment page must warn against weak pattern: {marker}")

    print("PASS qpv payment ledger source attribution regression")
    print("checked: checkout source reaches payment proof, proof/ledger/conversion/paid-gate rows keep source, revenue remains 0 EUR until manual paid verification")


if __name__ == "__main__":
    main()
