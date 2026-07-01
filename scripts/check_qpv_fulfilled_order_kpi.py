#!/usr/bin/env python3
"""Static regression checks for fulfilled-order KPI dashboard.

The fulfilled-order KPI dashboard must expose buyer-ready fulfillment state
without turning page views, action links, duplicate completed rows, or orphan
completed rows into paid revenue.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "fulfilled-order-kpi.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    page = PAGE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    required_markers = [
        "QPV Fulfilled Order KPI",
        "qpvPaidEventLedger",
        "qpvCompletedOrderLedger",
        "function verifiedPaidEvents",
        "function verifiedCompletedOrders",
        "function duplicateCompletedOrders",
        "function orphanCompletedOrders",
        "function pendingPaidFulfillment",
        "function orderStatusHref",
        "function fulfillmentHref",
        "Fulfilled orders",
        "Pending fulfillment",
        "Fulfilled EUR",
        "Duplicate completed rows",
        "Orphan completed rows",
        "Receipt-ready status links",
        "./paid-fulfillment.html",
        "./paid-fulfillment-router.html",
        "./order-status.html",
        "./revenue-command-center.html",
        "Complete fulfillment",
        "Open buyer status",
        "fulfilled order KPI reads qpvPaidEventLedger and qpvCompletedOrderLedger only",
        "fulfilled order KPI matches completed rows to verified paid events by unique paidEventId",
        "fulfilled order KPI exposes pending verified paid events that still need paid-fulfillment.html",
        "fulfilled order KPI exposes order-status.html links for buyer-ready fulfilled orders",
        "fulfilled order KPI counts fulfilled EUR only from matching verified paid events",
        "fulfilled order KPI page views links status views and fulfillment actions never create revenue",
        "duplicate completed rows and orphan completed rows are blocked from fulfilled revenue",
        "payment proof checkout reminder recovery and receipt text are not fulfilled revenue",
        "revenueDeltaFromFulfilledOrderKpiPageViewsEur:0",
        "buyerStatusLinkRevenueEur:0",
        "fulfillmentActionLinkRevenueEur:0",
        "duplicateCompletedOrderRevenueEur:0",
        "orphanCompletedOrderRevenueEur:0",
    ]
    for marker in required_markers:
        require(marker in page, f"fulfilled-order-kpi.html missing marker: {marker}")

    forbidden_markers = [
        "localStorage.setItem(paidKey",
        "localStorage.setItem('qpvPaidEventLedger'",
        "paymentStatus='paid'",
        'paymentStatus="paid"',
        "proof counts as revenue",
        "checkout counts as paid",
        "receipt text counts as revenue",
        "duplicate completed row counts as revenue",
        "orphan completed row counts as revenue",
        "revenueDeltaFromFulfilledOrderKpiPageViewsEur:19",
        "buyerStatusLinkRevenueEur:19",
        "fulfillmentActionLinkRevenueEur:19",
        "duplicateCompletedOrderRevenueEur:19",
        "orphanCompletedOrderRevenueEur:19",
        "fulfilledRevenueEur:19",
        "QPV-DEMO-001",
        "const demo=",
    ]
    for marker in forbidden_markers:
        require(marker not in page, f"fulfilled-order-kpi.html contains rejected fake-revenue marker: {marker}")

    require("python3 scripts/check_qpv_fulfilled_order_kpi.py" in workflow, "CI workflow must run fulfilled-order KPI gate")

    print("PASS qpv fulfilled order KPI regression")
    print("checked: verified paidEventId matching, pending fulfillment, buyer status links, duplicate/orphan guards, zero-revenue page/action links")


if __name__ == "__main__":
    main()
