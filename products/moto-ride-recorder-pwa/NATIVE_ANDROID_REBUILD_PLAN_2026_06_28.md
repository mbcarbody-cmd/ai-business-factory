# Native Android Rebuild Plan — Moto / SUP GPS Recorder

Status: required
Reason: PWA failed real SUP and motorcycle field tests.

## Decision

The recorder must move from browser PWA to native Android.

A browser GPS app is acceptable for demo UI only. It is not acceptable as the primary recorder for motorcycle or SUP use.

## Build target

Android-first app with:

- native location recording,
- visible recording notification,
- local append-only storage,
- recoverable sessions,
- GPX / CSV / JSON exports,
- separate sport profiles.

## Required Android capabilities

Manifest:

- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION
- FOREGROUND_SERVICE
- FOREGROUND_SERVICE_LOCATION
- POST_NOTIFICATIONS for Android 13+
- ACCESS_BACKGROUND_LOCATION only if locked-screen recording is required and user explicitly enables it

Service:

- foreground service type `location`
- persistent notification: `Recording GPS track`
- start service only from user action: Start button
- stop service only from user action: Stop button

Location:

- high accuracy provider
- 1 second target interval for motorcycle
- 2-3 second interval for SUP
- minimum distance filter:
  - SUP: 2-3 m
  - Moto: 5-10 m

Storage:

- write every accepted point immediately to local file or SQLite
- maintain current session id
- recover unfinished session on app open
- never wait until Stop to persist all data

Exports:

- GPX for maps / sharing
- CSV for analysis
- JSON for debugging

## Sport profiles

### SUP profile

Priority: clean distance and route shape.

- low-speed smoothing
- show km/h and knots
- ignore GPS jumps over water
- do not overreact to acceleration
- display elapsed time and distance clearly

### Motorcycle profile

Priority: speed, acceleration, braking events.

- higher speed ceiling
- acceleration / braking detection
- distance and max speed
- route color by speed

### Walking test profile

Priority: quick pre-test validation.

- show GPS point count
- simple distance check
- verifies permissions before real ride

## Acceptance tests

Before calling it working:

1. 5 minute walking test, screen on.
2. 10 minute walking test, screen locked.
3. 10 minute motorcycle / car test.
4. 10 minute SUP or slow water test.
5. Kill app mid-recording and reopen; track must recover.
6. GPX opens in Google Earth / OsmAnd / GPX viewer.
7. CSV contains timestamp, lat, lon, accuracy, speed, distance, profile.

## Fallback recommendation

For real routes before native app is ready, record with a proven Android GPS logger and use this repo app only as a reporting / post-analysis layer.
