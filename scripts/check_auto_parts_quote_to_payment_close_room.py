from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-quote-to-payment-close-room.html"

html = PAGE.read_text(encoding="utf-8")

required = [
    "apfQuoteToPaymentCloseLedger",
    "auto-parts-price-finder",
    "PRICE_EUR=29",
    "quote-to-payment close room",
    "outreach-ready row created",
    "29 EUR payment request ready",
    "proof + statement links ready",
    "auto-parts-bank-transfer-payment-request.html",
    "auto-parts-payment-proof-handoff.html",
    "auto-parts-proof-statement-match.html",
    "revenueCountedEur:0",
    "none until exact +29 EUR statement match creates apfPaidEventLedger",
    "quote/message/proof screenshot alone is not counted as paid",
    "BLOCKER: buyerEmail must be valid before outreach",
    "BLOCKER: vehicle and part/OEM scope are required before asking for 29 EUR",
    "Fallback executed: qualify one real buyer email",
    "summary",
    "staffing plan",
    "policy",
    "idea list",
    "audit",
    "page visit",
    "copied buyer message",
    "unpaid quote row",
    "manual paid claim",
    "fake/demo lead",
]

missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("Missing APF quote-to-payment close room regression markers: " + ", ".join(missing))

if html.count("revenueCountedEur:0") < 3:
    raise SystemExit("Close room must repeat zero-revenue rule in waiting, blocked and ready states")

if "rows.some(r=>r.leadId===action.leadId&&r.paymentReference===action.paymentReference)" not in html:
    raise SystemExit("Close room ledger must dedupe by leadId + paymentReference")

if "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$" not in html:
    raise SystemExit("Close room must validate buyer email before outreach")

print("APF quote-to-payment close room regression passed")
