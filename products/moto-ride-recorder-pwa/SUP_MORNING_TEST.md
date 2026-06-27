# SUP Morning Test — Moto Ride Recorder PWA

Goal: confirm the recorder works on Android Chrome before and during an irklente / SUP route.

## Open

Primary GitHub Pages URL, if Pages is enabled:

- `https://mbcarbody-cmd.github.io/ai-business-factory/`

Repo folder:

- `https://github.com/mbcarbody-cmd/ai-business-factory/tree/main/products/moto-ride-recorder-pwa`

## Before entering the water

1. Open the Pages URL in Android Chrome.
2. Wait for the app screen to load.
3. Tap `Install app` or Chrome menu -> `Add to Home screen`, if available.
4. Tap `Start ride` while still on shore.
5. Allow Location permission.
6. Wait until GPS shows at least 3 points or a GPS accuracy value.
7. Keep the phone screen on if possible.
8. Put the phone into a waterproof case / dry bag.

## During test

- Do not use the phone while paddling.
- If the map does not load, keep recording anyway. Route data still records without map tiles.
- GPS accuracy on water can jump. Judge the route shape and total distance after stopping.

## After return

1. Tap `Stop + save`.
2. Open the saved ride from history.
3. Export GPX first.
4. Export CSV second.
5. Export JSON if debugging is needed.

## What to report after test

- Did Location permission appear?
- Did the point counter increase?
- Did distance increase correctly?
- Did the map draw a line?
- Did Stop + save create a saved ride?
- Did GPX download work?
- Approx real route distance vs app distance.

## Known limits

- Real GPS requires HTTPS on Android Chrome.
- Browser recording is less reliable if the screen is locked or Android kills Chrome.
- For best first test, keep screen on and battery saver off.
