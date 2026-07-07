# AI Business Factory

Execution workspace for building autonomous internet businesses. The current priority is a small product that creates a real downloadable artifact before any sales activity.

## Current P0 product

**Quick Product Video**

A mobile browser app that creates a real vertical product video from uploaded photos:

- 1-8 local photos;
- product title, price, detail and contact text;
- 6, 10 or 15 second duration;
- animated zoom and photo transitions;
- 540x960 vertical canvas rendering;
- real WEBM video recording in the browser;
- playback and file download;
- Android installable PWA wrapper;
- no upload of user photos to a server.

## Live paths

```text
https://mbcarbody-cmd.github.io/ai-business-factory/website/video-maker.html
https://mbcarbody-cmd.github.io/ai-business-factory/website/android.html
https://mbcarbody-cmd.github.io/ai-business-factory/website/video-maker-android-qa.html
https://mbcarbody-cmd.github.io/ai-business-factory/website/quick-video-qa-proof-intake.html
https://mbcarbody-cmd.github.io/ai-business-factory/website/quick-video-paid-order.html
https://mbcarbody-cmd.github.io/ai-business-factory/website/quick-video-paid-event-verifier.html
```

## Rejected product

Content Hook Factory is rejected. It generated generic template text and video scripts, but no real video or sufficiently valuable finished artifact. It must not be sold or counted as delivery proof.

## Functional gate before revenue

Quick Product Video is not sell-ready until a real Android Chrome test proves all of the following:

1. photos load;
2. preview renders;
3. a non-empty WEBM file is generated;
4. the video plays;
5. the file downloads successfully.

The Android QA proof harness at `website/video-maker-android-qa.html` is the buyer/revenue-gate workflow for collecting that evidence. It creates a synthetic local WEBM, checks playback/download readiness, and stores proof JSON without counting revenue.

The QA proof intake at `website/quick-video-qa-proof-intake.html` is the first revenue-path handoff after that evidence. It accepts buyer details plus Android QA PASS proof JSON, rejects demo/fake/weak proof, unlocks payment and video-maker links only after the proof gate, and still records `0 EUR` until a separate verified paid event exists.

The paid order gate at `website/quick-video-paid-order.html` captures a 29 EUR buyer-ready order and production payment destination without counting revenue.

The paid event verifier at `website/quick-video-paid-event-verifier.html` counts revenue only after an exact real `+29 EUR` statement row matches a real QPV order and creates a duplicate-safe `verified_paid_event` ledger entry.

No outreach, payment request, domain purchase or paid-pilot claim is allowed before that evidence exists. No revenue may be counted from screenshots, checkout visits, promises to pay, manual claims, summaries, staffing plans, policies, idea lists, or audits.

## Repo structure

```text
website/video-maker.html                         Current functional P0
website/android.html                             Android PWA wrapper
website/video-maker-android-qa.html              Android Chrome WEBM proof harness
website/quick-video-qa-proof-intake.html         QA PASS intake before payment/outreach
website/quick-video-paid-order.html              29 EUR buyer-ready paid order gate
website/quick-video-paid-event-verifier.html     Exact +29 EUR paid event verifier
website/manifest.webmanifest                     Install metadata
website/sw.js                                    Offline app shell
OPS/product_gates/                               Product decisions and revenue gates
OPS/qa/                                          QA verdicts and proof
scripts/                                         OPS audit and validation tools
```
