from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "paid-fulfillment-router.html"
text = PAGE.read_text(encoding="utf-8")

required = [
    "qpv-paid-fulfillment-router-v1",
    "qpvPaidEventLedger",
    "qpvCompletedOrderLedger",
    "paid-fulfillment.html?source=paid_fulfillment_router",
    "paid-confirmation.html?source=paid_fulfillment_router",
    "revenue-command-center.html",
    "recovery-revenue-command-launchpad.html",
    "function isVerifiedPaid",
    "function uniquePaidEvents",
    "function verifiedCompletedRows",
    "function pendingPaidEvents",
    "function fulfillmentHref",
    "paymentStatus==='paid'",
    "pending fulfillment revenue 0 EUR",
    "routerRevenueEur:0",
    "routerLinkRevenueEur:0",
    "pendingFulfillmentRevenueEur:0",
    "receiptCopyRevenueEur:0",
    "receiptDownloadRevenueEur:0",
    "recoveryHandoffRevenueEur:0",
    "paymentProofRevenueEur:0",
    "duplicate paidEventId",
    "Fulfill this paid order",
    "Copy router QA JSON",
]

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"paid fulfillment router regression failed; missing: {missing}")

for forbidden in [
    "routerRevenueEur:19",
    "routerLinkRevenueEur:19",
    "pendingFulfillmentRevenueEur:19",
    "receiptCopyRevenueEur:19",
    "receiptDownloadRevenueEur:19",
    "recoveryHandoffRevenueEur:19",
    "paymentProofRevenueEur:19",
]:
    if forbidden in text:
        raise SystemExit(f"paid fulfillment router regression failed; forbidden fake revenue marker: {forbidden}")

if text.count("paid-fulfillment.html") < 3:
    raise SystemExit("paid fulfillment router regression failed; fulfillment route not prominent enough")

print("QPV paid fulfillment router regression passed")
