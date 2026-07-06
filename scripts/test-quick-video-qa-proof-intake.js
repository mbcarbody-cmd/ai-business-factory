#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const pagePath = path.join(__dirname, '..', 'website', 'quick-video-qa-proof-intake.html');
const html = fs.readFileSync(pagePath, 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exit(1);
  }
}

function mustContain(text) {
  assert(html.includes(text), `missing required text: ${text}`);
}

mustContain('QA_PASS_REVENUE_GATE_UNLOCKED');
mustContain('VERIFIED_PAID_EVENT');
mustContain('revenueEur:0');
mustContain('quickProductVideoQaRevenueGate');
mustContain('quickProductVideoAndroidQaProof');
mustContain('quick-product-video-android-qa-v1');
mustContain('videoReadyState');
mustContain('downloadReady');
mustContain('Number(proof.bytes)>=90000');
mustContain('demo|test-only|example|fake|placeholder|lorem|localhost');
mustContain('Payment handoff unlocked, revenue remains 0 EUR');

assert(!/revenueEur\s*:\s*PRICE_EUR/.test(html), 'must not count price as revenue on QA pass');
assert(!/localStorage\.setItem\([^,]+,\s*String\(PRICE_EUR\)/.test(html), 'must not store fake revenue amount');
assert(!/PAID|paid event/i.test(html.replace(/VERIFIED_PAID_EVENT/g, '')), 'must not mark QA proof as paid');

console.log('PASS quick-video QA proof intake gate regression');
