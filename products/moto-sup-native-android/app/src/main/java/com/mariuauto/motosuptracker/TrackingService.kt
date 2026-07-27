package com.mariuauto.motosuptracker

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Build
import android.os.Bundle
import android.os.IBinder
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.math.max

class TrackingService : Service(), LocationListener {
    private lateinit var locationManager: LocationManager
    private lateinit var prefs: android.content.SharedPreferences

    private var sessionId = ""
    private var mode = "MOTO"
    private var profile = "Yamaha FJR1300A 2019"
    private var startedAt = 0L
    private var lastLocation: Location? = null
    private var lastSpeedMps = 0.0
    private var totalDistanceMeters = 0.0
    private var pointCount = 0
    private var maxSpeedMps = 0.0

    private var previousPerfSpeedKmh: Double? = null
    private var previousPerfNs: Long? = null
    private var stoppedSinceNs = 0L
    private var accelArmed = false
    private var accelStartNs: Long? = null
    private var accelDistanceM = 0.0
    private var accel100Done = false
    private var quarterDone = false
    private var roll80StartNs: Long? = null
    private var rollCooldown = false
    private var brakingArmed = false
    private var brakingStartNs: Long? = null
    private var brakingPeakKmh = 0.0

    override fun onCreate() {
        super.onCreate()
        locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        prefs = getSharedPreferences(PREFS, MODE_PRIVATE)
        ensureChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            stopTracking()
            return START_NOT_STICKY
        }

        if (sessionId.isNotEmpty()) return START_STICKY

        val recovered = recoverSession()
        if (!recovered && intent?.action != ACTION_START) {
            stopSelf()
            return START_NOT_STICKY
        }
        if (!recovered) {
            mode = intent?.getStringExtra(EXTRA_MODE) ?: "MOTO"
            profile = intent?.getStringExtra(EXTRA_PROFILE) ?: "Yamaha FJR1300A 2019"
            startNewSession()
        }

        startForeground(NOTIFICATION_ID, buildNotification("Laukiama GPS"))
        startLocationUpdates()
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun startNewSession() {
        sessionId = newSessionId()
        startedAt = System.currentTimeMillis()
        totalDistanceMeters = 0.0
        pointCount = 0
        maxSpeedMps = 0.0
        resetPerformanceState()

        csvFile().writeText(
            "time_iso,session_id,mode,profile,lat,lon,accuracy_m,speed_accuracy_kmh,speed_mps,speed_kmh,accel_ms2,total_distance_m,altitude_m,bearing_deg\n"
        )
        gpxFile().writeText(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
                "<gpx version=\"1.1\" creator=\"Mariu Ride Lab\" xmlns=\"http://www.topografix.com/GPX/1/1\">\n" +
                "<metadata><name>$sessionId</name></metadata><trk><name>$profile</name><trkseg>\n"
        )
        currentSessionFile().writeText(listOf(sessionId, mode, profile, startedAt).joinToString("|"))
        prefs.edit()
            .putBoolean("recording", true)
            .putString("session_id", sessionId)
            .putString("mode", mode)
            .putString("profile", profile)
            .putFloat("speed_kmh", 0f)
            .putFloat("distance_m", 0f)
            .putFloat("max_speed_kmh", 0f)
            .putInt("point_count", 0)
            .putLong("duration_ms", 0L)
            .apply()
    }

    private fun recoverSession(): Boolean {
        val file = currentSessionFile()
        if (!file.exists()) return false
        val parts = runCatching { file.readText().split('|') }.getOrNull() ?: return false
        if (parts.size < 4) return false
        sessionId = parts[0]
        mode = parts[1]
        profile = parts[2]
        startedAt = parts[3].toLongOrNull() ?: System.currentTimeMillis()
        totalDistanceMeters = prefs.getFloat("distance_m", 0f).toDouble()
        pointCount = prefs.getInt("point_count", 0)
        maxSpeedMps = prefs.getFloat("max_speed_kmh", 0f).toDouble() / 3.6
        prefs.edit().putBoolean("recording", true).apply()
        return csvFile().exists() && gpxFile().exists()
    }

    private fun startLocationUpdates() {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            prefs.edit().putBoolean("recording", false).putString("gps_quality", "NĖRA LEIDIMO").apply()
            stopSelf()
            return
        }
        val minTimeMs = if (mode == "MOTO") 200L else 1000L
        try {
            locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                minTimeMs,
                0f,
                this
            )
        } catch (e: Exception) {
            prefs.edit().putBoolean("recording", false).putString("gps_quality", "GPS KLAIDA").apply()
            stopSelf()
        }
    }

    override fun onLocationChanged(location: Location) {
        val nowNs = location.elapsedRealtimeNanos
        val previous = lastLocation
        val step = if (previous != null) previous.distanceTo(location).toDouble() else 0.0
        val dtSec = if (previous != null) max(0.05, (nowNs - previous.elapsedRealtimeNanos) / 1_000_000_000.0) else 0.0
        val rawSpeedMps = if (location.hasSpeed()) location.speed.toDouble()
        else if (dtSec > 0.0) step / dtSec else 0.0
        val speedMps = rawSpeedMps.coerceIn(0.0, 110.0)
        val accel = if (previous != null && dtSec > 0.0) (speedMps - lastSpeedMps) / dtSec else 0.0
        val speedAccuracyKmh = if (location.hasSpeedAccuracy()) location.speedAccuracyMetersPerSecond * 3.6f else -1f
        val accepted = acceptRoutePoint(location, step, speedMps)

        if (accepted) {
            totalDistanceMeters += step
            pointCount += 1
            maxSpeedMps = max(maxSpeedMps, speedMps)
            appendCsv(location, speedMps, speedAccuracyKmh, accel)
            appendGpx(location)

            if (mode == "MOTO" && performancePointReliable(location, speedAccuracyKmh)) {
                processPerformance(speedMps * 3.6, nowNs, step, location.accuracy.toDouble())
            }

            lastLocation = location
            lastSpeedMps = speedMps
        }

        val quality = gpsQuality(location.accuracy, speedAccuracyKmh)
        saveLiveState(speedMps * 3.6, location.accuracy, speedAccuracyKmh, quality)
        updateNotification(speedMps * 3.6, quality)
    }

    private fun acceptRoutePoint(location: Location, step: Double, speedMps: Double): Boolean {
        if (location.accuracy > 60f) return false
        if (speedMps > 105.0) return false
        if (lastLocation != null && step > 350.0) return false
        if (mode == "SUP" && (speedMps > 15.0 || step > 100.0)) return false
        return true
    }

    private fun performancePointReliable(location: Location, speedAccuracyKmh: Float): Boolean {
        if (location.accuracy > 25f) return false
        if (speedAccuracyKmh >= 0f && speedAccuracyKmh > 9f) return false
        return true
    }

    private fun processPerformance(speedKmh: Double, nowNs: Long, stepM: Double, accuracyM: Double) {
        val prevSpeed = previousPerfSpeedKmh
        val prevNs = previousPerfNs
        if (prevSpeed == null || prevNs == null || nowNs <= prevNs) {
            previousPerfSpeedKmh = speedKmh
            previousPerfNs = nowNs
            return
        }

        if (speedKmh <= 2.0) {
            if (stoppedSinceNs == 0L) stoppedSinceNs = nowNs
            if (nowNs - stoppedSinceNs >= 1_000_000_000L) accelArmed = true
        } else {
            stoppedSinceNs = 0L
        }

        if (accelArmed && accelStartNs == null && prevSpeed <= 3.0 && speedKmh > 3.0) {
            accelStartNs = if (prevSpeed <= 1.0) prevNs else crossingNs(prevSpeed, speedKmh, 3.0, prevNs, nowNs)
            accelDistanceM = 0.0
            accel100Done = false
            quarterDone = false
            accelArmed = false
        }

        accelStartNs?.let { startNs ->
            val previousDistance = accelDistanceM
            accelDistanceM += stepM

            if (!accel100Done && prevSpeed < 100.0 && speedKmh >= 100.0) {
                val finishNs = crossingNs(prevSpeed, speedKmh, 100.0, prevNs, nowNs)
                val seconds = secondsBetween(startNs, finishNs)
                if (seconds in 1.0..30.0) recordResult("0-100 km/h", seconds, accuracyM, "last_0_100_s")
                accel100Done = true
            }

            if (!quarterDone && previousDistance < QUARTER_MILE_M && accelDistanceM >= QUARTER_MILE_M) {
                val fraction = ((QUARTER_MILE_M - previousDistance) / max(0.01, accelDistanceM - previousDistance)).coerceIn(0.0, 1.0)
                val finishNs = prevNs + ((nowNs - prevNs) * fraction).toLong()
                val seconds = secondsBetween(startNs, finishNs)
                if (seconds in 3.0..60.0) recordResult("0-402 m", seconds, accuracyM, "last_402m_s")
                quarterDone = true
            }

            if (speedKmh <= 2.0 && nowNs - startNs > 2_000_000_000L) {
                accelStartNs = null
                accelDistanceM = 0.0
            } else if (accel100Done && quarterDone) {
                accelStartNs = null
                accelDistanceM = 0.0
            }
        }

        if (!rollCooldown && roll80StartNs == null && prevSpeed < 80.0 && speedKmh >= 80.0) {
            roll80StartNs = crossingNs(prevSpeed, speedKmh, 80.0, prevNs, nowNs)
        }
        roll80StartNs?.let { startNs ->
            if (prevSpeed < 120.0 && speedKmh >= 120.0) {
                val finishNs = crossingNs(prevSpeed, speedKmh, 120.0, prevNs, nowNs)
                val seconds = secondsBetween(startNs, finishNs)
                if (seconds in 0.5..30.0) recordResult("80-120 km/h", seconds, accuracyM, "last_80_120_s")
                roll80StartNs = null
                rollCooldown = true
            } else if (speedKmh < 70.0 || nowNs - startNs > 60_000_000_000L) {
                roll80StartNs = null
            }
        }
        if (speedKmh < 70.0) rollCooldown = false

        if (speedKmh >= 100.0) {
            brakingArmed = true
            brakingPeakKmh = max(brakingPeakKmh, speedKmh)
        }
        if (brakingArmed && brakingStartNs == null && prevSpeed >= 100.0 && speedKmh < 100.0) {
            brakingStartNs = crossingNs(prevSpeed, speedKmh, 100.0, prevNs, nowNs)
        }
        brakingStartNs?.let { startNs ->
            if (speedKmh <= 3.0) {
                val seconds = secondsBetween(startNs, nowNs)
                if (seconds in 0.5..30.0) recordResult("100-0 km/h", seconds, accuracyM, "last_100_0_s")
                brakingStartNs = null
                brakingArmed = false
                brakingPeakKmh = 0.0
            } else if (speedKmh > brakingPeakKmh + 5.0 || nowNs - startNs > 30_000_000_000L) {
                brakingStartNs = null
                brakingArmed = speedKmh >= 100.0
            }
        }

        previousPerfSpeedKmh = speedKmh
        previousPerfNs = nowNs
    }

    private fun crossingNs(prevSpeed: Double, speed: Double, threshold: Double, prevNs: Long, nowNs: Long): Long {
        val delta = speed - prevSpeed
        if (kotlin.math.abs(delta) < 0.0001) return nowNs
        val fraction = ((threshold - prevSpeed) / delta).coerceIn(0.0, 1.0)
        return prevNs + ((nowNs - prevNs) * fraction).toLong()
    }

    private fun secondsBetween(startNs: Long, finishNs: Long): Double = (finishNs - startNs) / 1_000_000_000.0

    private fun recordResult(type: String, seconds: Double, accuracyM: Double, prefKey: String) {
        val file = File(filesDir, RESULTS_FILE)
        if (!file.exists()) file.writeText("time_iso,session_id,profile,type,value,unit,gps_accuracy_m\n")
        val value = String.format(Locale.US, "%.3f", seconds)
        val accuracy = String.format(Locale.US, "%.1f", accuracyM)
        file.appendText("${iso(System.currentTimeMillis())},$sessionId,$profile,$type,$value,s,$accuracy\n")
        prefs.edit().putFloat(prefKey, seconds.toFloat()).apply()
    }

    private fun appendCsv(location: Location, speedMps: Double, speedAccuracyKmh: Float, accel: Double) {
        val line = listOf(
            iso(location.time),
            sessionId,
            mode,
            profile,
            location.latitude.toString(),
            location.longitude.toString(),
            location.accuracy.toString(),
            if (speedAccuracyKmh >= 0f) String.format(Locale.US, "%.2f", speedAccuracyKmh) else "",
            String.format(Locale.US, "%.3f", speedMps),
            String.format(Locale.US, "%.1f", speedMps * 3.6),
            String.format(Locale.US, "%.3f", accel),
            String.format(Locale.US, "%.1f", totalDistanceMeters),
            if (location.hasAltitude()) location.altitude.toString() else "",
            if (location.hasBearing()) location.bearing.toString() else ""
        ).joinToString(",")
        csvFile().appendText(line + "\n")
    }

    private fun appendGpx(location: Location) {
        val elevation = if (location.hasAltitude()) "<ele>${String.format(Locale.US, "%.2f", location.altitude)}</ele>" else ""
        gpxFile().appendText(
            "<trkpt lat=\"${location.latitude}\" lon=\"${location.longitude}\">$elevation<time>${isoUtc(location.time)}</time></trkpt>\n"
        )
    }

    private fun saveLiveState(speedKmh: Double, accuracyM: Float, speedAccuracyKmh: Float, quality: String) {
        prefs.edit()
            .putBoolean("recording", true)
            .putString("mode", mode)
            .putFloat("speed_kmh", speedKmh.toFloat())
            .putFloat("accuracy_m", accuracyM)
            .putFloat("speed_accuracy_kmh", speedAccuracyKmh)
            .putString("gps_quality", quality)
            .putFloat("distance_m", totalDistanceMeters.toFloat())
            .putFloat("max_speed_kmh", (maxSpeedMps * 3.6).toFloat())
            .putInt("point_count", pointCount)
            .putLong("duration_ms", max(0L, System.currentTimeMillis() - startedAt))
            .apply()
    }

    private fun gpsQuality(accuracyM: Float, speedAccuracyKmh: Float): String {
        return when {
            accuracyM <= 10f && (speedAccuracyKmh < 0f || speedAccuracyKmh <= 5.5f) -> "GERAS"
            accuracyM <= 25f && (speedAccuracyKmh < 0f || speedAccuracyKmh <= 9f) -> "TINKAMAS"
            else -> "SILPNAS"
        }
    }

    private fun updateNotification(speedKmh: Double, quality: String) {
        val text = "$mode • ${String.format(Locale.US, "%.0f", speedKmh)} km/h • ${String.format(Locale.US, "%.2f", totalDistanceMeters / 1000.0)} km • GPS $quality"
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(NOTIFICATION_ID, buildNotification(text))
    }

    private fun buildNotification(text: String): Notification {
        val openIntent = Intent(this, MainActivity::class.java)
        val pending = PendingIntent.getActivity(
            this,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val builder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Notification.Builder(this, CHANNEL_ID)
        } else Notification.Builder(this)
        return builder
            .setContentTitle("Marių Ride Lab įrašinėja")
            .setContentText(text)
            .setSmallIcon(android.R.drawable.ic_menu_mylocation)
            .setContentIntent(pending)
            .setOngoing(true)
            .build()
    }

    private fun ensureChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(
                NotificationChannel(CHANNEL_ID, "GPS kelionės įrašymas", NotificationManager.IMPORTANCE_LOW)
            )
        }
    }

    private fun stopTracking() {
        try { locationManager.removeUpdates(this) } catch (_: Exception) {}
        if (sessionId.isNotEmpty()) closeGpx()
        currentSessionFile().delete()
        prefs.edit()
            .putBoolean("recording", false)
            .putFloat("speed_kmh", 0f)
            .apply()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
        sessionId = ""
    }

    private fun closeGpx() {
        val file = gpxFile()
        if (!file.exists()) return
        val tail = runCatching { file.readText().takeLast(32) }.getOrDefault("")
        if (!tail.contains("</gpx>")) file.appendText("</trkseg></trk></gpx>\n")
    }

    private fun resetPerformanceState() {
        previousPerfSpeedKmh = null
        previousPerfNs = null
        stoppedSinceNs = 0L
        accelArmed = false
        accelStartNs = null
        accelDistanceM = 0.0
        accel100Done = false
        quarterDone = false
        roll80StartNs = null
        rollCooldown = false
        brakingArmed = false
        brakingStartNs = null
        brakingPeakKmh = 0.0
    }

    override fun onDestroy() {
        try { locationManager.removeUpdates(this) } catch (_: Exception) {}
        super.onDestroy()
    }

    private fun csvFile(): File = File(filesDir, "$sessionId.csv")
    private fun gpxFile(): File = File(filesDir, "$sessionId.gpx")
    private fun currentSessionFile(): File = File(filesDir, "current_session.txt")
    private fun newSessionId(): String = "ride_" + SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
    private fun iso(timeMs: Long): String = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSZ", Locale.US).format(Date(timeMs))
    private fun isoUtc(timeMs: Long): String = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", Locale.US).apply {
        timeZone = java.util.TimeZone.getTimeZone("UTC")
    }.format(Date(timeMs))

    override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}
    override fun onProviderEnabled(provider: String) {}
    override fun onProviderDisabled(provider: String) {
        prefs.edit().putString("gps_quality", "GPS IŠJUNGTAS").apply()
    }

    companion object {
        const val ACTION_START = "com.mariuauto.motosuptracker.START"
        const val ACTION_STOP = "com.mariuauto.motosuptracker.STOP"
        const val EXTRA_MODE = "mode"
        const val EXTRA_PROFILE = "profile"
        const val PREFS = "ride_lab_state"
        const val RESULTS_FILE = "performance_results.csv"
        private const val CHANNEL_ID = "gps_recording"
        private const val NOTIFICATION_ID = 42
        private const val QUARTER_MILE_M = 402.336
    }
}
