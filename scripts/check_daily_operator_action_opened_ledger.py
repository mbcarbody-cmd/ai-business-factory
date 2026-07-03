#!/usr/bin/env python3
"""Static regression for Daily Learning operator action opened ledger workflow."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "operator-action-opened-ledger.html"
html = PAGE.read_text(encoding="utf-8")
compact = html.replace(" ", "")

required = [
    "dailyLearningOperatorQueue",
    "dailyLearningOperatorActionOpenedLedger",
    "operator-action-opened-ledger.html",
    "function openedKeyOf",
    "function topUnopenedAction",
    "function openTopAction",
    "openTopAction",
    "openedStatus:'operator_action_opened'",
    "openedSource:'operator_action_opened_ledger'",
    "operatorActionOpenedRevenueEur:0",
    "confirmedRevenueEur:0",
    "Opened operator action saved. Revenue remains 0 EUR until verified paid.",
    "No unopened operator action available, or duplicate blocked.",
    "opened operator action row is not revenue",
    "operator queue row is not revenue",
    "new policy file without regression is not learning proof",
    "reading is not learning proof",
    "summary is not learning proof",
    "payment proof is not paid revenue",
    "receipt is not paid revenue",
    "daily-learning-operator-action-opened-ledger.json",
    "./daily-learning-operator-queue.html?source=operator_action_opened_ledger",
    "./source-kpi-admin.html?source=operator_action_opened_ledger",
    "./revenue-command-center.html?source=operator_action_opened_ledger",
]

for pattern in required:
    if pattern not in html:
        raise SystemExit(f"FAIL: operator action opened ledger missing required pattern: {pattern}")

for forbidden in [
    "operatorActionOpenedRevenueEur:19",
    "confirmedRevenueEur:19",
    "opened operator action row is revenue",
    "operator queue row is revenue",
    "payment proof is paid revenue",
    "receipt is paid revenue",
    "policy file without regression is learning proof",
]:
    if forbidden in compact:
        raise SystemExit(f"FAIL: weak/harmful pattern present: {forbidden}")

print("PASS: operator action opened ledger dedupes fallback workflow events and keeps opened actions at 0 EUR until verified paid/delivered evidence.")
