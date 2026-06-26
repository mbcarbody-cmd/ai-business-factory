#!/usr/bin/env python3
"""Regression gate for QPV payment reminder workflow.

Payment reminders may move buyers toward checkout/verification, but they must remain
conversion events only. They cannot create paid events, count proof as revenue, or
duplicate reminder tasks for the same order interval.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "payment-reminder-workflow.html"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f"Forbidden {label}: {needle}")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    require(text, "qpvOrderLedger", "order ledger input")
    require(text, "qpvReminderTasks", "versioned reminder task ledger")
    require(text, "qpvConversionEvents", "conversion event ledger")
    require(text, "intervalHours=[24,72,168]", "24h/72h/7d reminder intervals")
    require(text, "validLead(order)", "leadId gate")
    require(text, "clean(order.orderId)", "orderId gate")
    require(text, "taskId(order,interval)", "dedupe key builder")
    require(text, "if(byId.has(id))return", "duplicate reminder guard")
    require(text, "recordConversionEvent(task,'payment_reminder_scheduled')", "scheduled conversion event")
    require(text, "recordConversionEvent(task,'payment_reminder_sent')", "sent conversion event")
    require(text, "revenueDeltaEur:0", "zero-revenue reminder event")
    require(text, "confirmedRevenueEur:revenue(orders)", "confirmed revenue remains paid/delivered only")
    require(text, "payment reminders never create paid events", "QA no-paid rule")
    require(text, 'href="./revenue-command-center.html"', "revenue command center navigation")
    require(text, 'href="./order-paid-bridge.html"', "paid bridge navigation")

    forbid(text, "paymentStatus='paid'", "reminder creates paid status")
    forbid(text, 'paymentStatus:"paid"', "reminder writes paid status")
    forbid(text, "revenueDeltaEur:19", "fake reminder revenue")
    forbid(text, "proof_submitted counts as revenue", "proof-as-sale claim")
    forbid(text, "payment proof is a sale", "proof-as-sale wording")

    print("PASS qpv payment reminder workflow regression")


if __name__ == "__main__":
    main()
