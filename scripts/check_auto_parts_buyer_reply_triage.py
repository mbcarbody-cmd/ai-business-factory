#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / "website" / "auto-parts-buyer-reply-triage.html"
text = page.read_text(encoding="utf-8")

required = [
    "APF buyer reply triage",
    "PRICE_EUR=29",
    "apfBuyerReplyTriageLedger",
    "apfPaidEventLedger",
    "exact +29 EUR",
    "exactStatementMatchRequired:'+29 EUR'",
    "qualified_close_handoff_not_revenue",
    "unqualified_reply_not_revenue",
    "scoreReply",
    "QUALIFIED_INTENTS",
    "auto-parts-buyer-close-room.html",
    "auto-parts-first-paid-order-cockpit.html",
    "auto-parts-proof-statement-match.html",
    "buyer reply, copied close message, opened close room, CSV export, demo reply, or manual paid claim = 0 EUR",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("APF buyer reply triage regression failed; missing: " + ", ".join(missing))

for weak in ["summary", "staffing plan", "policy", "idea list", "audit", "CSV export", "manual paid claim"]:
    if weak not in text:
        raise SystemExit(f"weak pattern not explicitly rejected: {weak}")

if "revenueCountedEur:0" not in text:
    raise SystemExit("reply triage must keep revenue locked to 0 EUR until verified paid ledger match")

print("APF buyer reply triage regression passed")
