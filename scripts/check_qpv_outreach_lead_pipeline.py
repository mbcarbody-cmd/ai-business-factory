#!/usr/bin/env python3
"""Static regression checks for the Quick Product Video outreach lead pipeline.

Run from repo root:
    python3 scripts/check_qpv_outreach_lead_pipeline.py

This rejects summary-only/acquisition-only claims unless the page ships executable
buyer rows, preserves checkout attribution, and keeps outreach revenue at 0 EUR.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "website" / "outreach-lead-pipeline.html"
COMMAND_CENTER = ROOT / "website" / "revenue-command-center.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    pipeline = read(PIPELINE)
    command_center = read(COMMAND_CENTER)

    required_pipeline_markers = [
        "seedBuyerPack",
        "Load 10 buyer-ready rows",
        "buyerReadyRows",
        "buyer_pack_2026_06_28",
        "buyerPackRows:buyerReadyRows.length",
        "buyer pack has 10 outreach-ready rows",
        "buyer pack counted as paid",
        "revenueEur:0",
        "$('kpiRevenue').textContent='0'",
        "confirmedRevenueEur:0",
        "checkoutUrl(row)",
        "leadId:row.leadId",
        "priceEur:String(row.priceEur)",
        "Revenue stays 0 EUR until verified paid event",
        "appendConversion(row,'lead_imported')",
        "outreach_${status}",
        "duplicate import counted twice",
        "missing leadId checkout handoff",
    ]
    for marker in required_pipeline_markers:
        require(marker in pipeline, f"outreach pipeline missing required marker: {marker}")

    buyer_row_count = len(re.findall(r"source:'buyer_pack_2026_06_28'", pipeline))
    require(buyer_row_count >= 10, f"buyer pack must contain at least 10 executable rows, found {buyer_row_count}")

    rejected_pipeline_patterns = [
        "kpiRevenue').textContent=priceEur",
        "kpiRevenue').textContent=rows.length",
        "confirmedRevenueEur:priceEur",
        "buyerPackRevenueEur",
        "paidByOutreach",
        "qpvPaidEventLedger.push",
        "paymentStatus='paid'",
        "paymentStatus = 'paid'",
    ]
    for pattern in rejected_pipeline_patterns:
        require(pattern not in pipeline, f"outreach pipeline must not count weak revenue pattern: {pattern}")

    require("./outreach-lead-pipeline.html" in command_center, "command center must link to outreach pipeline")
    require("Buyer</span> SMB/product seller" in command_center, "command center must expose buyer segment")
    require("Price</span> 19 EUR" in command_center, "command center must expose 19 EUR offer")

    print("PASS qpv outreach lead pipeline regression")
    print("checked: 10-row buyer pack, leadId checkout attribution, zero-EUR outreach guardrail, command center buyer/price link")


if __name__ == "__main__":
    main()
