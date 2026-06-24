from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'website' / 'lead-kpi.html'

text = PAGE.read_text(encoding='utf-8')

required = [
    'qpv-lead-checkout-kpi-v1',
    "orderKey='qpvOrderLedger'",
    "lastOutreachKey='qpvLastOutreachProof'",
    "handoffKey='qpvLeadHandoffLedger'",
    'checkoutOrdersFromLead',
    'leadToCheckoutConversionPct',
    'confirmedRevenueEur',
    'payment_pending counts 0 EUR',
    'proof_submitted_manual_review counts 0 EUR',
    'only paid/delivered counts confirmed EUR',
    'checkout_handoff',
    './lead-send.html',
    './checkout.html',
    './order-admin.html',
]
missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit(f'Missing required lead KPI dashboard markers: {missing}')

for forbidden in [
    'outreach counted as revenue',
    'proof counted as revenue',
    'revenueEur:19',
    'confirmedRevenueEur:19',
    'send_ready_not_sent counts revenue',
]:
    if forbidden in text:
        raise SystemExit(f'Forbidden weak revenue pattern found: {forbidden}')

if "function isPaid(row){return row.paymentStatus==='paid'||row.paymentStatus==='delivered'||row.fulfillmentStatus==='delivered'}" not in text:
    raise SystemExit('Paid gate must only allow paid/delivered orders.')

if "orders.filter(checkoutCreatedFromLead)" not in text:
    raise SystemExit('Dashboard must measure lead-originated checkout orders, not only static lead counts.')

print('PASS: QPV lead KPI dashboard regression markers present; fake revenue patterns rejected.')
