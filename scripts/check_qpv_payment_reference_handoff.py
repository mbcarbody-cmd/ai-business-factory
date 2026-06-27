#!/usr/bin/env python3
"""Regression gate for QPV payment proof -> paid gate handoff.

Payment proof is not revenue, but it must carry a durable paymentReference
through the local proof ledger, order ledger, last-proof cache, conversion
ledger and paid-confirmation link so a verified buyer can be marked paid once
without losing attribution.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "payment-ledger.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    for needle, label in [
        ("PAYMENTREFERENCE TRACKED", "buyer-visible payment reference tracking"),
        ("paymentReferenceFrom", "canonical payment reference helper"),
        ("paymentReference=clean(data.paymentNote)", "proof reference extracted from buyer note"),
        ("paymentReference,reference:paymentReference", "proof stores canonical reference aliases"),
        ("paymentReference:paymentReferenceFrom(proof)", "order ledger stores canonical paymentReference"),
        ("reference:paymentReferenceFrom(proof)", "order ledger stores reference alias"),
        ("paymentProof:{...proof,leadId,paymentReference:paymentReferenceFrom(proof),reference:paymentReferenceFrom(proof)}", "existing order proof patch preserves reference"),
        ("writeJson(lastProofKey,{...proof,paymentReference:paymentReferenceFrom(proof),reference:paymentReferenceFrom(proof)})", "last proof cache preserves reference for paid gate"),
        ("paymentReference:paymentReferenceFrom(proof)", "conversion event includes paymentReference"),
        ("paidGateHref", "manual paid gate handoff"),
        ("./paid-confirmation.html?", "paid confirmation link"),
        ("paymentReference:paymentReferenceFrom(proof)", "paid gate URL includes payment reference"),
        ("Revenue remains 0 EUR until admin marks paid", "zero revenue proof message"),
        ("confirmedRevenueEur:confirmedRevenue", "export keeps confirmed revenue derived from ledger"),
    ]:
        require(text, needle, label)

    for needle, label in [
        ("paymentStatus:'paid'", "fake paid status from proof"),
        ("paymentStatus=\"paid\"", "fake paid mutation"),
        ("revenueEur:19", "hard-coded proof revenue"),
        ("revenueCountedEur:19", "hard-coded proof counted revenue"),
        ("confirmedRevenueEur:19", "fake confirmed revenue"),
        ("proof counts as revenue", "proof-as-revenue wording"),
        ("payment_proof_submitted_manual_review counts as revenue", "proof KPI as revenue"),
    ]:
        forbid(text, needle, label)

    print("PASS qpv payment reference handoff regression")


if __name__ == "__main__":
    main()
