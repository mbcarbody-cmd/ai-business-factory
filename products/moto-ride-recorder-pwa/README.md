# Moto Ride Recorder PWA

Status: working MVP

Purpose: motorcycle ride recorder for Android/Chrome with GPS route, speed, acceleration, braking, map view, local ride history, and GPX/CSV/JSON export.

## What works

- Start / pause / resume / stop ride recording.
- GPS route recording with high accuracy mode.
- Current, average, and max speed.
- Distance and ride duration.
- Acceleration and braking from GPS speed delta.
- Optional device motion G readout when the phone/browser allows it.
- OpenStreetMap / Leaflet route map with route segments and accel/brake markers.
- LocalStorage ride history on the phone.
- Export current or saved ride as GPX, CSV, or JSON.
- PWA manifest + service worker so Android Chrome can install it to home screen.

## Run / deploy

Best Android test path:

1. Deploy this folder through GitHub Pages or another HTTPS static host.
2. Open the HTTPS URL in Android Chrome.
3. Tap menu → Add to Home screen / Install app.
4. Allow location permission.
5. Press `Start ride` before riding.

Important: mobile GPS APIs require a secure browser context on most phones. Use HTTPS, not a raw `file://` copy, for real ride recording.

## Folder

- `index.html` — full working app, no build step.
- `manifest.json` — PWA install metadata.
- `sw.js` — offline app shell cache.
- `icons/icon.svg` — app icon.

## Safety note

Do not interact with the app while riding. Start recording before moving, mount the phone safely, and review data only after stopping.
