#!/usr/bin/env python3
"""Static regression gate for the QPV outreach lead pipeline.

This gate rejects fake product movement: an outreach page must create stable
leadId rows, dedupe imports, pass leadId into checkout, write conversion events,
and keep revenue at 0 until the existing verified paid flow confirms payment.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "outreach-lead-pipeline.html"

REQUIRED_SNIPPETS = [
    "qpvOutreachLeadLedger",
    "qpvConversionLedger",
    "stableLeadId",
    "leadFingerprint",
    "deduped/updated",
    "checkout.html?",
    "leadId",
    "outreach_contacted",
    "outreach_replied",
    "outreach_qualified",
    "outreach_checkout",
    "confirmedRevenueEur:0",
    "kpiRevenue').textContent='0'",
    "outreach page cannot write paid revenue",
    "duplicate import counted twice",
    "outreach status counted as paid",
]

FORBIDDEN_SNIPPETS = [
    "qpvPaidEventLedger.push",
    "paymentStatus='paid'",
    "paymentStatus = 'paid'",
    "confirmedRevenueEur:priceEur",
    "revenueEur:priceEur",
    "summary-only progress",
]


def main() -> int:
    if not PAGE.exists():
        raise SystemExit(f"Missing page: {PAGE}")
    text = PAGE.read_text(encoding="utf-8")
    missing = [snippet for snippet in REQUIRED_SNIPPETS if snippet not in text]
    forbidden = [snippet for snippet in FORBIDDEN_SNIPPETS if snippet in text]
    if missing or forbidden:
        raise SystemExit(
            "QPV outreach lead pipeline regression failed\n"
            f"Missing: {missing}\n"
            f"Forbidden: {forbidden}"
        )
    print("QPV outreach lead pipeline regression passed")
    print("leadId attribution: present")
    print("dedupe gate: present")
    print("checkout handoff: present")
    print("revenue gate: 0 EUR until verified paid event")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
