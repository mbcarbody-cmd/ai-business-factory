#!/usr/bin/env python3
"""Regression gate for the buyer-ready Auto Parts Price Finder product.

This must stay a real product/workflow improvement, not another dashboard. It
requires a callable pricing app, fixed paid offer, lead/order row export, payment
handoff, and zero confirmed revenue until a verified paid event exists.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-price-finder.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing Auto Parts Price Finder product page")
    html = PAGE.read_text(encoding="utf-8")

    required_product_markers = [
        "AI Auto Parts Price Finder",
        "Pirkti kainos auditą — 29 €",
        "product=auto-parts-price-finder&priceEur=29&buyer=used-parts-seller",
        "Manual paid gate",
        "payment-ledger.html?product=auto-parts-price-finder&priceEur=29",
        "Lead email / klientas",
        "saveLead()",
        "exportCsv()",
        "auto-parts-price-finder-leads.csv",
        "revenueCountedEur:0",
        "confirmed revenue = 0 EUR until verified paid event",
        "used-parts seller, 29 EUR",
    ]
    for marker in required_product_markers:
        require(marker in html, f"missing product marker: {marker}")

    required_workflow_markers = [
        "function scorePart()",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "low:Math.round(low)",
        "ask:Math.round(ask)",
        "high:Math.round(high)",
        "status:'lead_created_unpaid'",
        "localStorage.setItem('apfLeadRows'",
        "paid-confirmation.html?product=${PRODUCT}&priceEur=${PRICE_EUR}",
    ]
    for marker in required_workflow_markers:
        require(marker in html, f"missing executable workflow marker: {marker}")

    rejected_weak_patterns = [
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "fake paid",
        "dashboard-only progress",
        "checkout click as revenue counted",
        "summary-only",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in html, f"weak/fake revenue pattern must not appear: {pattern}")

    print("PASS auto parts price finder product regression")
    print("checked: 29 EUR buyer-facing pricing product, lead CSV, paid handoff, manual ledger gate, zero revenue until verified paid event")


if __name__ == "__main__":
    main()
