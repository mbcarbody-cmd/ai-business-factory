# Moto SUP Native Android Tracker

Status: skeleton_started
Reason: browser PWA failed real SUP and motorcycle tests.

This folder is the Android-native replacement for `products/moto-ride-recorder-pwa`.

## Goal

A real Android GPS recorder with:

- user-started foreground location service,
- persistent recording notification,
- local append-only track file while recording,
- GPX / CSV export,
- separate SUP and motorcycle modes,
- recovery after app restart.

## Why native

The PWA used browser geolocation. That is not reliable enough for locked-screen or long route recording on Android. The correct Android implementation needs a foreground service of type `location`, runtime location permission, and immediate persistent storage of track points.

## Current contents

- Minimal Gradle Android project skeleton.
- Kotlin `MainActivity` with Start / Stop / Export buttons.
- Kotlin `TrackingService` using Android `LocationManager` GPS updates.
- Manifest with location + foreground service permissions.

## Build expectation

Open this folder in Android Studio as a Gradle Android project and build the debug APK.

## Field gate

Do not call this product working until:

1. 10 minute walking test with screen locked succeeds.
2. 10 minute moto / car test succeeds.
3. SUP or slow route test succeeds.
4. GPX export opens in a GPX viewer.
5. Unfinished recording is recoverable after app restart.
