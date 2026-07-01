from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "paid-fulfillment.html"
text = PAGE.read_text(encoding="utf-8")

required = [
    "qpvPaidEventLedger",
    "qpvCompletedOrderLedger",
    "paidEventId",
    "paymentStatus==='paid'",
    "function isVerifiedPaid",
    "function uniquePaidEvents",
    "function completeNext",
    "Complete next paid order",
    "Copy latest receipt",
    "Download latest receipt",
    "completedOrderRevenueEur",
    "fulfilledRevenueEur",
    "duplicateFulfillmentRevenueEur:0",
    "pendingFulfillmentRevenueEur:0",
    "receiptCopyRevenueEur:0",
    "receiptDownloadRevenueEur:0",
    "orphaned paidEventId",
    "duplicate paidEventId",
    "payment proof text",
    "pending fulfillment",
]

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"paid fulfillment regression failed; missing: {missing}")

if "writeArray(completedKey" not in text:
    raise SystemExit("paid fulfillment regression failed; no completed ledger write")

if "localStorage.setItem" not in text:
    raise SystemExit("paid fulfillment regression failed; localStorage persistence missing")

if "verified paid" not in text.lower():
    raise SystemExit("paid fulfillment regression failed; verified-paid language missing")

for forbidden in [
    "proofSubmittedRevenueEur:19",
    "receiptDownloadRevenueEur:19",
    "pendingFulfillmentRevenueEur:19",
    "duplicateFulfillmentRevenueEur:19",
]:
    if forbidden in text:
        raise SystemExit(f"paid fulfillment regression failed; forbidden fake revenue marker: {forbidden}")

print("QPV paid fulfillment regression passed")
