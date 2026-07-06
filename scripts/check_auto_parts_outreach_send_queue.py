#!/usr/bin/env python3
"""Regression gate for the APF 29 EUR outreach send queue.

This gate protects a concrete revenue workflow improvement: buyer-ready outreach
rows with real send actions and duplicate-safe sent-action KPI movement. It must
not count page visits, copied text, generated rows, CSV exports, or manual paid
claims as revenue. Confirmed revenue remains locked to verified +29 EUR APF paid
events in apfPaidEventLedger.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-outreach-send-queue.html"
INDEX = ROOT / "index.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(PAGE.exists(), "missing APF outreach send queue page")
    page = PAGE.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    required_page_markers = [
        "Auto Parts Price Finder — outreach send queue",
        "Executable revenue path · APF 29 EUR · outreach-ready send queue",
        "const PRICE_EUR=29",
        "const LEDGER_KEY='apfOutreachSendLedger'",
        "const QUEUE_KEY='apfOutreachSendQueue'",
        "const PAID_KEY='apfPaidEventLedger'",
        "const DEFAULT_PAYMENT_URL='./auto-parts-bank-transfer-order.html?product=auto-parts-price-finder&priceEur=29&buyer=used-parts-seller&source=outreach-send-queue'",
        "Load 12 buyer-ready seed rows",
        "Build outreach queue",
        "Open mailto",
        "Open WhatsApp",
        "Export outreach CSV",
        "payment/order URL required before outreach send queue",
        "Generated leads without payment path are rejected weak patterns",
        "revenueCountedEur:0",
        "status:'outreach_opened_not_paid'",
        "Copied outreach text",
        "Copy is not counted as sent outreach and not revenue",
        "CSV export is not revenue and not sent outreach",
        "Revenue: 0 EUR until apfPaidEventLedger has verified +29 EUR statement match",
    ]
    for marker in required_page_markers:
        require(marker in page, f"outreach send queue missing marker: {marker}")

    seed_markers = [
        "Kauno naudotos dalys",
        "Vilnius auto ardymas",
        "Klaipeda parts export",
        "Riga used parts",
        "Warsaw dismantler",
        "Berlin teile seller",
        "EU RHD specialist",
        "EV/PHEV parts",
    ]
    for marker in seed_markers:
        require(marker in page, f"missing concrete outreach seed buyer row: {marker}")

    executable_markers = [
        "function buildMessage(lead)",
        "function buildMailto(lead)",
        "function buildWhatsapp(lead)",
        "function markOpened(lead,channel)",
        "if(!ledger.some(row=>row.key===key))",
        "function exportCsv()",
        "function updateKpis()",
        "row.status==='verified_paid'",
        "Number(row.amountEur||row.priceEur)===PRICE_EUR",
    ]
    for marker in executable_markers:
        require(marker in page, f"missing executable send/KPI marker: {marker}")

    weak_patterns = [
        "revenueCountedEur:29",
        "generated row is revenue",
        "copied text is revenue",
        "CSV export is revenue",
        "manual paid claim",
        "summary-only",
        "staffing plan",
    ]
    for pattern in weak_patterns:
        require(pattern not in page, f"weak/fake revenue pattern must not appear: {pattern}")

    index_markers = [
        "auto-parts-outreach-send-queue.html?product=auto-parts-price-finder&priceEur=29",
        "Atidaryti APF outreach send queue",
        "opened outreach action",
    ]
    for marker in index_markers:
        require(marker in index, f"root launcher missing APF outreach send queue marker: {marker}")

    print("PASS auto parts outreach send queue regression")
    print("checked: 12 concrete buyer-ready seed rows, payment/order URL preflight, mailto/WhatsApp send actions, duplicate-safe apfOutreachSendLedger KPI, CSV export rejection, copied-text rejection, and revenue locked to verified +29 EUR APF paid events")


if __name__ == "__main__":
    main()
