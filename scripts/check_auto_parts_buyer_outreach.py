#!/usr/bin/env python3
"""Regression gate for Auto Parts Price Finder buyer outreach rows.

This is a revenue-path check, not a dashboard/audit check. It requires a usable
outreach workflow that creates concrete lead rows, mailto copy, CSV export, and
a direct 29 EUR order handoff while refusing to count outreach as revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PAGE = ROOT / "website" / "auto-parts-price-finder.html"
ORDER_PAGE = ROOT / "website" / "auto-parts-bank-transfer-order.html"
OUTREACH_PAGE = ROOT / "website" / "auto-parts-buyer-outreach.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PRODUCT_PAGE.exists(), "missing Auto Parts Price Finder product page")
    require(ORDER_PAGE.exists(), "missing bank-transfer order page")
    require(OUTREACH_PAGE.exists(), "missing buyer outreach page")

    product = PRODUCT_PAGE.read_text(encoding="utf-8")
    order = ORDER_PAGE.read_text(encoding="utf-8")
    outreach = OUTREACH_PAGE.read_text(encoding="utf-8")

    outreach_markers = [
        "Auto Parts Price Finder outreach generator",
        "Executable sales workflow · outreach-ready rows · 29 EUR offer",
        "const PRODUCT='auto-parts-price-finder'",
        "const PRICE_EUR=29",
        "const STORAGE_KEY='apfOutreachRows'",
        "function generateRows()",
        "function exportCsv()",
        "buildRow(i)",
        "mailto:?subject=",
        "auto-parts-bank-transfer-order.html",
        "source=auto-parts-outreach",
        "auto-parts-price-finder-outreach-rows.csv",
        "status:'outreach_ready_unpaid'",
        "revenueCountedEur:0",
        "pipeline value, not revenue",
        "Revenue rule: revenueCountedEur:",
    ]
    for marker in outreach_markers:
        require(marker in outreach, f"outreach page missing executable marker: {marker}")

    buyer_path_markers = [
        "Vehicle / niche",
        "Part / offer angle",
        "OEM / codes",
        "Target segment",
        "Rows to generate",
        "Generate outreach rows",
        "Export CSV",
        "Order page",
        "Product page",
    ]
    for marker in buyer_path_markers:
        require(marker in outreach, f"outreach page missing buyer path marker: {marker}")

    product_handoff_markers = [
        "auto-parts-buyer-outreach.html",
        "Buyer outreach rows",
    ]
    for marker in product_handoff_markers:
        require(marker in product, f"product page missing outreach handoff marker: {marker}")

    order_handoff_markers = [
        "auto-parts-buyer-outreach.html",
        "Outreach rows",
    ]
    for marker in order_handoff_markers:
        require(marker in order, f"order page missing outreach return marker: {marker}")

    rejected_weak_patterns = [
        "outreach row is revenue",
        "mailto click is revenue",
        "CSV export is revenue",
        "pipeline value is confirmed EUR",
        "revenueCountedEur:29",
        "confirmedRevenueEur:29",
        "fake paid event",
        "dashboard-only progress",
        "summary-only",
    ]
    for pattern in rejected_weak_patterns:
        require(pattern not in outreach, f"weak/fake revenue pattern must not appear in outreach page: {pattern}")

    print("PASS auto parts buyer outreach regression")
    print("checked: outreach rows, mailto text, CSV export, 29 EUR order handoff, product/order links, and zero confirmed revenue until verified payment")


if __name__ == "__main__":
    main()
