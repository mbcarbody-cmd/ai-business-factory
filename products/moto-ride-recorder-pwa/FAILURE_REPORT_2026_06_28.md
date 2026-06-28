# Field Failure Report — Moto / SUP Recorder

Date: 2026-06-28
Status: failed_field_test

## User result

The browser PWA did not work well enough in real SUP and motorcycle use.

## Root cause

The first implementation was a browser PWA. That is not reliable enough for motorcycle / SUP track recording because:

1. Android Chrome may pause or throttle location updates when the screen is locked, battery saver is enabled, or the browser tab loses focus.
2. The app has no Android foreground service with a persistent notification.
3. The app has no guaranteed background location permission flow.
4. The app has no crash-proof autosave / recover loop.
5. SUP speeds are low, so GPS noise creates bad speed / acceleration values.
6. Motorcycle speeds need a different filtering profile than SUP.
7. The app relies on external Leaflet / OSM assets; if those fail, user trust drops even if GPS recording still partially works.

## Current code problems

- PWA uses `navigator.geolocation.watchPosition`, which is only acceptable for foreground testing.
- It is not a real Android GPS logger.
- It has no native background recording.
- It stores only after Stop + save, so failed sessions can lose data.
- It does not separate modes: SUP / motorcycle / walking test.
- It has only one acceleration threshold.

## Correct product direction

Stop treating this as a web app.

Next version must be a native Android tracker:

- Kotlin or React Native / Expo dev build.
- FusedLocationProviderClient or native location provider.
- Foreground service type: location.
- Persistent notification while recording.
- Runtime fine location permission.
- Background location permission only if needed for locked-screen recording.
- Local append-only track file while recording.
- Recover unfinished recording on app restart.
- Separate mode profiles:
  - SUP: low speed, GPS smoothing, knots, distance priority.
  - Moto: high speed, acceleration / braking events, higher sample rate.
- Export GPX / CSV / JSON.

## Immediate fallback for real rides

Until native app is built, use a proven GPS logger app for real recording, and use this repo app only for UI / reporting experiments.

## Product gate

No more claims of working field recorder until:

1. 10 minute walking test with screen locked succeeds.
2. 10 minute car / motorcycle test succeeds.
3. SUP or slow-water test succeeds.
4. GPX export matches expected route shape and distance.
5. App restart recovers unfinished recording.
