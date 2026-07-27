# Marių Ride Lab — Android GPS performance RC1

Status: **0.3.0-rc1 — ready for first real-device field testing**.

Native Android GPS recorder designed first for **Yamaha FJR1300A 2019** and **UMIDIGI Bison GT2 Pro 5G**, with a separate slower SUP recording mode.

## Included in RC1

- Foreground GPS service with persistent notification.
- Partial wake lock to reduce locked-screen recording interruptions.
- Explicit Android GPS hardware requirement and foreground-location permissions.
- Live speed, route distance, duration, maximum speed, GPS accuracy and actual sample rate.
- Stale-GPS warning when location updates stop for more than five seconds.
- Automatic motorcycle measurements:
  - 0–100 km/h after at least one second stationary;
  - 80–120 km/h;
  - 100–0 km/h braking;
  - standing 402.336 m time.
- Linear interpolation between GPS samples at thresholds.
- Performance attempts rejected when GPS speed or accuracy is inadequate.
- Latest and best result storage.
- Append-only CSV telemetry and GPX route recording.
- One-file ZIP export containing the last ride GPX, CSV and result history.
- Recovery of an unfinished recording after Android restarts the service.
- Safe Start / Stop controls that do not start a stop-only foreground service.
- Automatic unit tests for acceleration, rolling acceleration, braking and quarter mile.
- GitHub Actions test gate followed by APK compilation.

## Measurement limits

This RC uses the phone's built-in GPS. Many phones deliver about 1 Hz location updates, although the app requests faster updates and displays the rate actually received. Threshold interpolation improves consistency but cannot turn 1 Hz GPS into Dragy-level measurement.

For commercial-grade timing, add an external 10–25 Hz Bluetooth GNSS receiver and validate against Dragy or RaceBox. The app deliberately shows GPS quality and rejects clearly weak samples rather than silently presenting every number as accurate.

The 100–0 finish is detected at 3 km/h because phone GPS tends to fluctuate around zero.

## Build and test

```bash
gradle :app:testDebugUnitTest :app:assembleDebug
```

GitHub Actions workflow: `.github/workflows/build-mariu-ride-android.yml`.

## Field test gate

Do not call the measurement accurate until these pass:

1. Install RC1 on **UMIDIGI Bison GT2 Pro 5G**.
2. Grant precise location and notification permissions.
3. Set the app battery mode to unrestricted in Android settings.
4. Record at least 10 minutes with the screen locked.
5. Confirm the persistent notification remains and sample rate continues updating.
6. Stop and export the ZIP; verify GPX and CSV open correctly.
7. Perform at least five safe closed-course 0–100 attempts.
8. Compare with synchronized video or a known GPS performance device.
9. Kill/reopen the UI during recording and verify the service continues.
10. Complete a one-hour ride to measure battery use and OEM process-killing behaviour.

## After field validation

- External Bluetooth GNSS support.
- OpenStreetMap route and ride replay.
- Video recording with telemetry overlay.
- Vehicle and service-history profiles.
- Shareable result cards and optional cloud backup.
- TPMS integration where sensor protocols are legally and technically accessible.
