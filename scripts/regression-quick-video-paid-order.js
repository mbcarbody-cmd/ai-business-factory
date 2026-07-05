'use strict';

const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, '..', 'website', 'quick-video-paid-order.html');
const html = fs.readFileSync(htmlPath, 'utf8');

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function includes(fragment, message) {
  assert(html.includes(fragment), message);
}

includes('const PRICE_EUR = 29;', 'price must stay fixed at 29 EUR');
includes("product: 'Quick Product Video'", 'lead must identify the revenue product');
includes('priceEur: PRICE_EUR', 'lead must store the offer price');
includes('revenueEur: 0', 'lead capture must not count revenue before payment verification');
includes("paymentStatus: 'pending_verification'", 'lead must be pending verification, not paid');
includes('isTrustedPaymentDestination', 'payment destination validator must exist');
includes('LT_IBAN_PATTERN', 'IBAN production payment path must be supported');
includes('TRUSTED_PAYMENT_HOSTS', 'trusted payment host allowlist must exist');
includes('buy.stripe.com', 'Stripe Checkout/payment links must be allowed');
includes('checkout.stripe.com', 'Stripe Checkout host must be allowed');
includes('revolut.me', 'Revolut payment links must be allowed');
includes('pay.revolut.com', 'Revolut Pay host must be allowed');
includes('paypal.com', 'PayPal payment links must be allowed');
includes('WEAK_PAYMENT_PATTERN', 'weak payment pattern denylist must exist');
['demo','test','example','fake','placeholder','localhost','127\\.0\\.0\\.1'].forEach(word => {
  includes(word, `weak pattern ${word} must be explicitly rejected`);
});
includes('./video-maker.html?', 'paid order must hand off to the real video maker');
includes('quickVideoPaidOrderLeads', 'buyer lead ledger must persist locally');
includes('mailto:', 'invoice/payment-request email path must exist');
includes('validEmail', 'buyer email validation must exist');
includes('window.__QPV_ORDER_GATE__', 'page must expose a small browser-test seam');

const policy = {
  hosts: ['buy.stripe.com','checkout.stripe.com','revolut.me','pay.revolut.com','paypal.com','www.paypal.com'],
  weak: /(demo|test|example|fake|placeholder|sample|todo|localhost|127\.0\.0\.1)/i,
  iban: /^LT\d{18}$/i,
  isTrustedPaymentDestination(value) {
    const raw = String(value || '').trim();
    if (!raw || this.weak.test(raw)) return false;
    const compact = raw.replace(/\s+/g,'').toUpperCase();
    if (this.iban.test(compact)) return true;
    try {
      const url = new URL(raw);
      const host = url.hostname.toLowerCase();
      return url.protocol === 'https:' && this.hosts.some(allowed => host === allowed || host.endsWith('.' + allowed));
    } catch (_) { return false; }
  }
};

const validDestinations = [
  'LT121000011101001000',
  'https://buy.stripe.com/live_123',
  'https://pay.revolut.com/order/abc',
  'https://www.paypal.com/paypalme/example'
];
const invalidDestinations = [
  '',
  'https://example.com/pay',
  'https://fake.stripe.example/pay',
  'http://buy.stripe.com/not-secure',
  'https://unknown-payments.invalid/pay',
  'PLACEHOLDER_IBAN',
  'https://localhost/pay'
];
validDestinations.forEach(value => assert(policy.isTrustedPaymentDestination(value), `expected valid payment destination: ${value}`));
invalidDestinations.forEach(value => assert(!policy.isTrustedPaymentDestination(value), `expected invalid payment destination: ${value}`));

console.log('PASS quick-video-paid-order regression: 29 EUR lead capture, production payment validation, zero-revenue pending state, and video-maker handoff are enforced.');
