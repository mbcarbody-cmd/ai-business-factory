#!/usr/bin/env python3
"""Static regression checks for fulfilled buyer order-status continuity.

The status portal must expose completed paid orders to buyers without turning
page views, proof text, duplicate completions, or orphan completed rows into
revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "website" / "order-status.html"
FULFILLMENT = ROOT / "website" / "paid-fulfillment.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    status = read(STATUS)
    fulfillment = read(FULFILLMENT)
    workflow = read(WORKFLOW)

    required_status_markers = [
        "qpvPaidEventLedger",
        "qpvCompletedOrderLedger",
        "function verifiedPaidEvents",
        "function verifiedCompletedOrders",
        "function completedForOrder",
        "Fulfilled orders",
        "Fulfillment receipt",
        "Complete paid fulfillment",
        "fulfilled status requires unique completed order plus matching verified paidEventId",
        "revenueDeltaFromStatusPageViewsEur:0",
        "receiptViewRevenueEur:0",
        "duplicateCompletedOrderRevenueEur:0",
        "orphanCompletedOrderRevenueEur:0",
        "receipt view and order status page view are not revenue",
        "completed.receiptText",
        "paidEventId(completed)",
    ]
    for marker in required_status_markers:
        require(marker in status, f"order-status.html missing fulfilled-order marker: {marker}")

    legacy_order_status_markers = [
        "reads full qpvOrderLedger by orderId",
        "proof_submitted_manual_review counts 0 EUR",
        "only paid/delivered counts revenue",
        "Submit payment proof",
        "./payment-ledger.html?",
        "./video-maker.html?",
        "unknown order gives payment-proof fallback, not fake success",
    ]
    for marker in legacy_order_status_markers:
        require(marker in status, f"order-status.html lost legacy buyer-status marker: {marker}")

    rejected_status_markers = [
        "QPV-DEMO-001",
        "const demo=",
        "demo[id]",
        "qpvLastCheckoutOrder')||'null'",
        "revenueCountedEur:19",
        "receiptViewRevenueEur:19",
        "duplicateCompletedOrderRevenueEur:19",
        "orphanCompletedOrderRevenueEur:19",
    ]
    for marker in rejected_status_markers:
        require(marker not in status, f"order-status.html contains rejected fake-success marker: {marker}")

    require("qpvCompletedOrderLedger" in fulfillment, "paid fulfillment must still write/read completed order ledger")
    require("completed.receiptText" in status, "buyer status must expose completed order receipt text")
    require("python3 scripts/check_qpv_completed_order_status.py" in workflow, "CI workflow must run completed-order status gate")

    print("PASS qpv completed order status regression")
    print("checked: fulfilled buyer status, paidEventId reconciliation, receipt exposure, zero-revenue page-view guards")


if __name__ == "__main__":
    main()
