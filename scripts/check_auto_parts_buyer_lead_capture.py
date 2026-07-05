from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "auto-parts-buyer-lead-capture.html"
INDEX = ROOT / "index.html"

page = PAGE.read_text(encoding="utf-8")
index = INDEX.read_text(encoding="utf-8")

required_page_markers = [
    "APF fallback revenue path",
    "buyer lead capture",
    "invoice/payment-request email",
    "apfBuyerLeadLedger",
    "apfPaidEventLedger",
    "revenueCountedEur:0",
    "lead_captured_not_revenue",
    "BLOCKER: buyer email must be valid",
    "BLOCKER: buyer/company is required",
    "Duplicate APF lead found",
    "CSV export is not revenue",
    "Email seller payment request",
    "Open checkout with lead",
    "Configure payment destination",
    "Open proof handoff",
    "Rejected weak patterns",
    "invoice request email",
    "checkout deep link",
    "fake paid event",
]

missing = [marker for marker in required_page_markers if marker not in page]
if missing:
    raise SystemExit(f"buyer lead capture page missing markers: {missing}")

if "auto-parts-buyer-lead-capture.html" not in index:
    raise SystemExit("root launcher does not link APF buyer lead capture page")

if "Revenue counted now: ${row.revenueCountedEur} EUR" not in page:
    raise SystemExit("lead pack must explicitly keep revenue at 0 until paid event")

if "Count only verified paid event in ${PAID_LEDGER_KEY}" not in page:
    raise SystemExit("lead capture must not count leads as revenue")

print("APF buyer lead capture regression passed")
