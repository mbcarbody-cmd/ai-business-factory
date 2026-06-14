# Product Shipping Protocol

Date: 2026-06-14
Owner: CEO / Master Agent + Product Shipping Cell
Status: active

## Kodėl sukurtas

Sistema pradėjo per daug gaminti OPS/training dokumentų ir per mažai veikiančių produktų. Nuo šiol kiekvienas aktyvus product cell turi matuoti progresą ne pagal dokumentus, o pagal veikiantį artefaktą, demo, lead, revenue ar QA/deploy proof.

## Nauja taisyklė

Kiekvieną dieną turi atsirasti bent vienas iš šių rezultatų:

1. working product prototype,
2. public demo URL,
3. Android/PWA wrapper-ready build,
4. exact lead + offer + outreach draft,
5. paid pilot/proposal/invoice movement,
6. QA/deploy blocker closed with proof.

Docs alone do not count unless they directly unblock a shipped product.

## Product cells

### Cell A — Parts Seller OS

Priority: P0.
Output: seller workflow that handles part intake, category, location, pricing, listing readiness, order and dead-stock.

### Cell B — Micro Apps / Android PWA

Priority: P1 fast shipping.
Output: one useful mobile-first app prototype per sprint.

Current shipped examples:

- `products/date-spark-pwa/index.html`
- `products/market-pulse-pwa/index.html`

### Cell C — Revenue Tools

Priority: P0/P1.
Output: lead finder, offer generator, quote/invoice/payment flow, outreach packs.

### Cell D — AI Ads / Content Factory

Priority: P2 until revenue gate.
Output: tiny demo only: brief -> hooks -> variants -> QA -> CTA.

### Cell E — Opportunity Lab

Priority: research + tiny demo.
Output: validate new ideas, but cannot steal P0 capacity unless product gate passes.

## Dating app decision

A full dating network is not a two-day product because it requires accounts, real users, chat, moderation, abuse handling, report/block, privacy, growth loop and trust/safety.

But a useful dating-related product can ship fast:

- profile optimizer,
- icebreaker generator,
- match-readiness checker,
- local date ideas app,
- private community/waitlist MVP.

Therefore `Date Spark PWA` is a fast MVP, not a full dating network.

## Android app route

Fast route:

1. build mobile-first PWA,
2. host static demo,
3. test on Android browser,
4. wrap with Capacitor or Trusted Web Activity,
5. add app icon/splash,
6. only then consider Play Store.

Native Android first is slower and unnecessary for most validation MVPs.

## What does not count anymore

- another strategy document without product artifact,
- another agent layer without shipped output,
- another opportunity list without tiny demo,
- another market analysis without lead/revenue/product action,
- another design plan without actual page.

## Next 48h rules

1. Host shipped PWAs publicly.
2. Add CEO Cockpit shipped-products panel.
3. Move one PWA to Android-wrapper-ready checklist.
4. Create first landing/offer for one micro app.
5. Create exact lead list or user acquisition hypothesis for one shipped app.

## CEO verdict

The factory is not allowed to look smart while not shipping. Product artifacts must lead the system from now on.
