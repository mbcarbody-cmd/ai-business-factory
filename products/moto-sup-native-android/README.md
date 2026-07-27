# Marių Ride Lab — Android GPS performance MVP

Status: **MVP implementation on `feature/mariu-ride-acceleration-mvp`**.

This is the native Android replacement for the browser PWA. It is designed first for the user's **Yamaha FJR1300A 2019**, while keeping a slower SUP recording mode.

## Implemented

- Android foreground GPS service that continues with the screen locked.
- Live speed, GPS accuracy, distance, duration and maximum speed.
- Automatic motorcycle measurements:
  - 0–100 km/h;
  - 80–120 km/h;
  - 100–0 km/h braking;
  - standing 402.336 m time.
- Linear interpolation between GPS samples at speed thresholds.
- GPS quality gate for performance attempts.
- Append-only CSV telemetry.
- GPX route file and Android document export.
- Persistent performance result history in `performance_results.csv`.
- Recovery of an unfinished recording after an Android process restart.
- Separate MOTO and SUP route filters.
- GitHub Actions debug APK build and downloadable artifact.

## Important accuracy limit

A phone commonly provides roughly 1 Hz GPS updates even when Android requests more frequent updates. Interpolation improves threshold timing, but a phone-only result remains approximate. The production path should support an external 10–25 Hz Bluetooth GNSS receiver and compare runs against a Dragy/RaceBox reference.

## Build

Open `products/moto-sup-native-android` in Android Studio, or run:

```bash
gradle :app:assembleDebug
```

GitHub Actions workflow: `.github/workflows/build-mariu-ride-android.yml`.

## Field test gate

Do not market this as accurate until all are completed:

1. Install debug APK on **UMIDIGI Bison GT2 Pro 5G**.
2. Record 10 minutes with the screen locked.
3. Export GPX and open it in a GPX viewer.
4. Perform several safe closed-course acceleration tests.
5. Compare 0–100 against video or a known GPS performance device.
6. Kill and reopen the app during a recording to verify recovery.
7. Confirm battery use and GPS stability during a one-hour ride.

## Next commercial milestones

- OpenStreetMap route screen and ride replay.
- Vehicle/profile manager and service history.
- External Bluetooth GNSS support.
- Video recording with telemetry overlay.
- TPMS integration where sensor protocols are accessible.
- Cloud account, leaderboards and shareable run cards.
