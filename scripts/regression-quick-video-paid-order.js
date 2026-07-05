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
includes("revenueEur: 0", 'lead capture must not count revenue before payment verification');
includes("paymentStatus: 'pending_verification'", 'lead must be pending verification, not paid');
includes('isTrustedPaymentDestination', 'payment destination validator must exist');
includes('LT_IBAN_PATTERN', 'IBAN production payment path must be supported');
includes('TRUSTED_PAYMENT_HOSTS', 'trusted payment host allowlist must exist');
includes('buy.stripe.com', 'Stripe Checkout/payment links must be allowed');
includes('revolut.me', 'Revolut payment links must be allowed');
includes('paypal.com', 'PayPal payment links must be allowed');
includes('WEAK_PAYMENT_PATTERN', 'weak payment pattern denylist must exist');
['demo','test','example','fake','placeholder','localhost'].forEach(word => {
  includes(word, `weak pattern ${word} must be explicitly rejected`);
});
includes('./video-maker.html?', 'paid order must hand off to the real video maker');
includes('quickVideoPaidOrderLeads', 'buyer lead ledger must persist locally');
includes('mailto:', 'invoice/payment-request email path must exist');
includes('validEmail', 'buyer email validation must exist');

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

const validatorSource = html.match(/function isTrustedPaymentDestination\(value\)\{[\s\S]*?\n\}/);
assert(validatorSource, 'validator function source must be extractable');
const constantsSource = html.match(/const TRUSTED_PAYMENT_HOSTS[\s\S]*?const \$ =/);
assert(constantsSource, 'payment validation constants must be extractable');
const validator = new Function(`${constantsSource[0].replace('const $ =', 'var __stop =')}\n${validatorSource[0]}\nreturn isTrustedPaymentDestination;`)();
validDestinations.forEach(value => assert(validator(value), `expected valid payment destination: ${value}`));
invalidDestinations.forEach(value => assert(!validator(value), `expected invalid payment destination: ${value}`));

console.log('PASS quick-video-paid-order regression: 29 EUR lead capture, production payment validation, zero-revenue pending state, and video-maker handoff are enforced.');
