#!/usr/bin/env python3
"""Static regression checks for fulfilled-order KPI dashboard.

The fulfilled-order KPI dashboard must expose buyer-ready fulfillment state
without turning page views, action links, duplicate completed rows, or orphan
completed rows into paid revenue. Fulfillment entry points must also route the
operator back into this KPI so completed-order revenue can be reconciled quickly.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "fulfilled-order-kpi.html"
FULFILLMENT = ROOT / "website" / "paid-fulfillment.html"
ROUTER = ROOT / "website" / "paid-fulfillment-router.html"
WORKFLOW = ROOT / ".github" / "workflows" / "revenue-regression.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_markers(text: str, markers: list[str], filename: str) -> None:
    for marker in markers:
        require(marker in text, f"{filename} missing marker: {marker}")


def forbid_markers(text: str, markers: list[str], filename: str) -> None:
    for marker in markers:
        require(marker not in text, f"{filename} contains rejected fake-revenue marker: {marker}")


def main() -> None:
    page = PAGE.read_text(encoding="utf-8")
    fulfillment = FULFILLMENT.read_text(encoding="utf-8")
    router = ROUTER.read_text(encoding="utf-8")
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
    require_markers(page, required_markers, "fulfilled-order-kpi.html")

    fulfillment_handoff_markers = [
        "./fulfilled-order-kpi.html?source=paid_fulfillment",
        "id=\"fulfilledKpiTopLink\"",
        "id=\"fulfilledKpiLink\"",
        "function fulfilledKpiHref",
        "fulfilledOrderKpiUrl",
        "Fulfilled KPI:",
        "fulfilledOrderKpiLinkRevenueEur:0",
        "fulfilledOrderKpiVisitRevenueEur:0",
        "fulfilled order KPI link",
        "fulfilled order KPI visit",
        "store fulfilledOrderKpiUrl so operator can reconcile completed orders immediately",
    ]
    require_markers(fulfillment, fulfillment_handoff_markers, "paid-fulfillment.html")

    router_handoff_markers = [
        "./fulfilled-order-kpi.html?source=paid_fulfillment_router",
        "id=\"fulfilledKpiLink\"",
        "function fulfilledKpiHref",
        "Review fulfilled KPI",
        "fulfilledOrderKpi:'./fulfilled-order-kpi.html?source=paid_fulfillment_router'",
        "fulfilledOrderKpiLinkRevenueEur:0",
        "fulfilledOrderKpiVisitRevenueEur:0",
        "nextFulfilledKpiUrl",
        "fulfilledKpiUrl",
        "fulfilled order KPI link",
        "fulfilled order KPI visit",
    ]
    require_markers(router, router_handoff_markers, "paid-fulfillment-router.html")

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
        "fulfilledOrderKpiLinkRevenueEur:19",
        "fulfilledOrderKpiVisitRevenueEur:19",
        "duplicateCompletedOrderRevenueEur:19",
        "orphanCompletedOrderRevenueEur:19",
        "fulfilledRevenueEur:19",
        "QPV-DEMO-001",
        "const demo=",
    ]
    forbid_markers(page, forbidden_markers, "fulfilled-order-kpi.html")
    forbid_markers(fulfillment, forbidden_markers, "paid-fulfillment.html")
    forbid_markers(router, forbidden_markers, "paid-fulfillment-router.html")

    require("python3 scripts/check_qpv_fulfilled_order_kpi.py" in workflow, "CI workflow must run fulfilled-order KPI gate")

    print("PASS qpv fulfilled order KPI regression")
    print("checked: verified paidEventId matching, pending fulfillment, buyer status links, fulfillment handoff links, duplicate/orphan guards, zero-revenue page/action links")


if __name__ == "__main__":
    main()
