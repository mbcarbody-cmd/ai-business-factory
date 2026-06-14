# Android Wrapper Checklist

Date: 2026-06-14
Owner: Product Shipping Cell + DevOps Commander
Status: active

## Goal

Turn one shipped mobile-first PWA into an Android-installable prototype.

Candidate PWAs:

1. `products/date-spark-pwa/index.html`
2. `products/market-pulse-pwa/index.html`
3. `products/auto-parts-title-generator-pwa/index.html`

## Fast route

### Option A — Trusted Web Activity

Use when public URL exists and the app is mostly web.

Needs:

- hosted HTTPS URL,
- manifest,
- service worker,
- icons,
- asset links,
- basic Android wrapper.

### Option B — Capacitor

Use when we want an APK before a final public URL.

Needs:

- npm project,
- static web build copied into app,
- Capacitor config,
- Android project generated,
- icon/splash,
- debug APK.

## First APK candidate

Recommended first: `Auto Parts Title Generator PWA`.

Reason:

- directly supports Parts Seller OS,
- lower legal/privacy risk than dating or finance,
- simple utility,
- good seller lead magnet,
- easiest to test on Android.

## Blockers

- no public URL yet,
- no service worker yet,
- no app icons yet,
- no local Android build proof yet.

## Next action

Create service worker + icons placeholders + Capacitor/TWA plan for Auto Parts Title Generator first.
