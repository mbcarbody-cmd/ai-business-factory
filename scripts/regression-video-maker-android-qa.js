#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const qaPath = path.join(root, 'website', 'video-maker-android-qa.html');
const html = fs.readFileSync(qaPath, 'utf8');

const requiredSnippets = [
  'quick-product-video-android-qa-v1',
  'canvas.captureStream(30)',
  'new MediaRecorder',
  'minimumUsefulBytes',
  'waitVideoReady',
  'downloadReady',
  'quickProductVideoAndroidQaProof',
  'Revenue counter',
  '0 EUR until verified paid event',
  'PASS: WEBM sukurtas, playback ir download paruošti.'
];

const forbiddenWeakPatterns = [
  'fake paid event',
  'demo revenue',
  'count revenue',
  'localStorage.setItem(\'revenue',
  'localStorage.setItem("revenue',
  'status:\'PAID\'',
  'status:"PAID"'
];

const failures = [];
for (const snippet of requiredSnippets) {
  if (!html.includes(snippet)) failures.push(`missing required snippet: ${snippet}`);
}
for (const pattern of forbiddenWeakPatterns) {
  if (html.includes(pattern)) failures.push(`forbidden weak revenue pattern present: ${pattern}`);
}

const capturesWebm = /canvas\.captureStream\(30\)[\s\S]{0,260}new MediaRecorder/.test(html);
if (!capturesWebm) failures.push('MediaRecorder must be created from canvas capture stream path');

const gatesBlobSize = /blob\.size\s*<\s*min/.test(html) || /blob\.size\s*>=\s*min/.test(html);
if (!gatesBlobSize) failures.push('QA harness must gate PASS on blob.size minimum');

const exposesDownload = /download[^\n]+href\s*=\s*outputUrl/.test(html) || /\$\('download'\)\.href\s*=\s*outputUrl/.test(html);
if (!exposesDownload) failures.push('QA harness must expose generated WEBM as download href');

if (failures.length) {
  console.error('Android QA regression FAILED');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log('Android QA regression passed: real WEBM proof harness is present and does not count revenue.');
