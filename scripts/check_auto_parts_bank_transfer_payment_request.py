from pathlib import Path

PAGE = Path('website/auto-parts-bank-transfer-payment-request.html')
text = PAGE.read_text(encoding='utf-8')

required = [
    'APF_BANK_TRANSFER_PAYMENT_REQUEST_CREATED',
    'apfBankTransferPaymentRequests',
    'apfPaidEventLedger',
    'auto-parts-bank-statement-import.html',
    'auto-parts-payment-proof-handoff.html',
    'revenueCountedEur:0',
    'payment request counted as sale',
    'copied message counted as revenue',
    'manual paid claim without statement row',
    'isProductionBankInstruction',
    'demo|test|example|fake|placeholder|sample',
    'PRICE_EUR=29',
]

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f'Missing APF bank transfer payment request guards: {missing}')

if 'confirmedRevenue(){return readJson(PAID_KEY).reduce' not in text:
    raise SystemExit('Revenue must be derived only from verified paid ledger, not request rows')

if 'writeJson(REQUEST_KEY,rows)' not in text:
    raise SystemExit('Payment request ledger write is missing')

if 'revenue is counted only later by a matching +29 EUR statement row' not in text.lower():
    raise SystemExit('Page must explicitly reject counting requests as revenue')

print('OK: APF bank transfer payment request desk blocks fake revenue and routes buyer to proof + statement import.')
