from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-verified-paid-router.html"

html = PAGE.read_text(encoding="utf-8")

required = [
    "apfPaidEventLedger",
    "apfVerifiedPaidRouterLedger",
    "auto-parts-price-finder",
    "PRICE_EUR=29",
    "verified paid event accepted",
    "receipt link ready",
    "fulfillment link ready",
    "auto-parts-paid-receipt.html",
    "auto-parts-fulfillment-delivery-desk.html",
    "revenueCountedEur:0",
    "router never increments revenue",
    "page visit",
    "copied next-action pack",
    "proof screenshot alone",
    "statement row without exact +29 EUR APF match",
    "fake/demo paid event",
    "BLOCKER: missing real paidEventId",
    "BLOCKER: paid event must be exact +29 EUR",
    "BLOCKER: status must be verified/paid/matched",
    "Fallback executed: open proof + statement match",
]

missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("Missing APF verified paid router regression markers: " + ", ".join(missing))

if html.count("revenueCountedEur:0") < 2:
    raise SystemExit("Router must repeat zero-revenue click/export rule in blocked and routed states")

if "localStorage.setItem(key,JSON.stringify(rows.slice(0,300)))" not in html:
    raise SystemExit("Router ledger must persist duplicate-safe local workflow rows")

if "rows.some(r=>r.paidEventId===action.paidEventId)" not in html:
    raise SystemExit("Router must dedupe by paidEventId")

print("APF verified paid router regression passed")
