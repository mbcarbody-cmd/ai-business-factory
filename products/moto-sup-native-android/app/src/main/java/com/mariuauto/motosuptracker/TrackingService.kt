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
import android.os.PowerManager
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.math.max

class TrackingService : Service(), LocationListener {
    private lateinit var locationManager: LocationManager
    private lateinit var prefs: android.content.SharedPreferences
    private val performanceEngine = PerformanceEngine()

    private var wakeLock: PowerManager.WakeLock? = null
    private var sessionId = ""
    private var mode = "MOTO"
    private var profile = "Yamaha FJR1300A 2019"
    private var startedAt = 0L
    private var lastLocation: Location? = null
    private var lastSpeedMps = 0.0
    private var totalDistanceMeters = 0.0
    private var pointCount = 0
    private var maxSpeedMps = 0.0
    private var sampleRateHz = 0.0
    private var explicitStop = false

    override fun onCreate() {
        super.onCreate()
        locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        prefs = getSharedPreferences(PREFS, MODE_PRIVATE)
        ensureChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            if (sessionId.isEmpty()) recoverSession()
            explicitStop = true
            stopTracking()
            return START_NOT_STICKY
        }

        if (sessionId.isNotEmpty()) return START_STICKY

        val recovered = recoverSession()
        if (!recovered && intent?.action != ACTION_START) {
            prefs.edit().putBoolean("recording", false).apply()
            stopSelf()
            return START_NOT_STICKY
        }

        if (!recovered) {
            mode = intent?.getStringExtra(EXTRA_MODE) ?: "MOTO"
            profile = intent?.getStringExtra(EXTRA_PROFILE) ?: "Yamaha FJR1300A 2019"
            startNewSession()
        } else {
            performanceEngine.reset()
            prefs.edit().putString("attempt_status", "Įrašymas atkurtas; pradėtas bandymas nunulintas").apply()
        }

        startForeground(NOTIFICATION_ID, buildNotification("Laukiama GPS"))
        acquireWakeLock()
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
        sampleRateHz = 0.0
        lastLocation = null
        lastSpeedMps = 0.0
        performanceEngine.reset()

        csvFile().writeText(
            "time_iso,session_id,mode,profile,lat,lon,accuracy_m,speed_accuracy_kmh,sample_hz,speed_mps,speed_kmh,accel_ms2,total_distance_m,altitude_m,bearing_deg\n"
        )
        gpxFile().writeText(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
                "<gpx version=\"1.1\" creator=\"Mariu Ride Lab\" xmlns=\"http://www.topografix.com/GPX/1/1\">\n" +
                "<metadata><name>$sessionId</name></metadata><trk><name>${xmlEscape(profile)}</name><trkseg>\n"
        )
        currentSessionFile().writeText(listOf(sessionId, mode, profile, startedAt).joinToString("|"))

        prefs.edit()
            .putBoolean("recording", true)
            .putString("session_id", sessionId)
            .putString("mode", mode)
            .putString("profile", profile)
            .putString("attempt_status", "Palauk gero GPS ir visiškai sustok")
            .putString("gps_quality", "LAUKIAMA")
            .putFloat("speed_kmh", 0f)
            .putFloat("distance_m", 0f)
            .putFloat("max_speed_kmh", 0f)
            .putFloat("sample_hz", 0f)
            .putFloat("accuracy_m", -1f)
            .putFloat("speed_accuracy_kmh", -1f)
            .putInt("point_count", 0)
            .putLong("duration_ms", 0L)
            .putLong("last_update_ms", 0L)
            .remove("last_0_100_s")
            .remove("last_80_120_s")
            .remove("last_100_0_s")
            .remove("last_402m_s")
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
        sampleRateHz = prefs.getFloat("sample_hz", 0f).toDouble()

        val valid = sessionId.isNotBlank() && csvFile().exists() && gpxFile().exists()
        prefs.edit().putBoolean("recording", valid).apply()
        if (!valid) {
            currentSessionFile().delete()
            sessionId = ""
        }
        return valid
    }

    private fun startLocationUpdates() {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            prefs.edit()
                .putBoolean("recording", false)
                .putString("gps_quality", "NĖRA LEIDIMO")
                .putString("attempt_status", "Suteik tikslios vietos leidimą")
                .apply()
            stopSelf()
            return
        }

        val minTimeMs = if (mode == "MOTO") 100L else 1000L
        try {
            locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                minTimeMs,
                0f,
                this
            )
        } catch (e: Exception) {
            prefs.edit()
                .putBoolean("recording", false)
                .putString("gps_quality", "GPS KLAIDA")
                .putString("attempt_status", e.message ?: "Nepavyko paleisti GPS")
                .apply()
            stopSelf()
        }
    }

    override fun onLocationChanged(location: Location) {
        val nowNs = location.elapsedRealtimeNanos
        val previous = lastLocation
        val step = if (previous != null) previous.distanceTo(location).toDouble() else 0.0
        val dtSec = if (previous != null) {
            max(0.05, (nowNs - previous.elapsedRealtimeNanos) / 1_000_000_000.0)
        } else {
            0.0
        }

        if (dtSec > 0.0) {
            val instantHz = (1.0 / dtSec).coerceIn(0.0, 20.0)
            sampleRateHz = if (sampleRateHz <= 0.0) instantHz else sampleRateHz * 0.8 + instantHz * 0.2
        }

        val rawSpeedMps = if (location.hasSpeed()) {
            location.speed.toDouble()
        } else if (dtSec > 0.0) {
            step / dtSec
        } else {
            0.0
        }
        val speedMps = rawSpeedMps.coerceIn(0.0, 110.0)
        val accel = if (previous != null && dtSec > 0.0) (speedMps - lastSpeedMps) / dtSec else 0.0
        val speedAccuracyKmh = if (location.hasSpeedAccuracy()) {
            location.speedAccuracyMetersPerSecond * 3.6f
        } else {
            -1f
        }
        val accepted = acceptRoutePoint(location, step, speedMps)

        if (accepted) {
            totalDistanceMeters += step
            pointCount += 1
            maxSpeedMps = max(maxSpeedMps, speedMps)
            appendCsv(location, speedMps, speedAccuracyKmh, accel)
            appendGpx(location)

            if (mode == "MOTO") {
                if (performancePointReliable(location, speedAccuracyKmh)) {
                    val results = performanceEngine.addSample(
                        speedKmh = speedMps * 3.6,
                        elapsedRealtimeNs = nowNs,
                        stepDistanceM = step,
                        accuracyM = location.accuracy.toDouble()
                    )
                    results.forEach(::recordResult)
                    if (results.isEmpty()) updateAttemptStatus(speedMps * 3.6)
                } else {
                    performanceEngine.reset()
                    prefs.edit().putString("attempt_status", "GPS per silpnas tiksliam matavimui").apply()
                }
            }

            lastLocation = location
            lastSpeedMps = speedMps
        }

        val quality = gpsQuality(location.accuracy, speedAccuracyKmh, location.hasSpeed())
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
        if (!location.hasSpeed()) return false
        if (location.accuracy > 20f) return false
        if (speedAccuracyKmh >= 0f && speedAccuracyKmh > 7f) return false
        return true
    }

    private fun updateAttemptStatus(speedKmh: Double) {
        val status = when {
            speedKmh <= 1.5 -> "Stovi — laikmatis ruošiamas"
            speedKmh < 80.0 -> "Važiavimas įrašomas"
            speedKmh < 100.0 -> "Galimas 80–120 arba 0–100 bandymas"
            else -> "Greitis virš 100 km/h"
        }
        prefs.edit().putString("attempt_status", status).apply()
    }

    private fun recordResult(result: PerformanceResult) {
        val file = File(filesDir, RESULTS_FILE)
        if (!file.exists()) file.writeText("time_iso,session_id,profile,type,value,unit,gps_accuracy_m\n")
        val value = String.format(Locale.US, "%.3f", result.seconds)
        val accuracy = String.format(Locale.US, "%.1f", result.accuracyM)
        file.appendText("${iso(System.currentTimeMillis())},$sessionId,$profile,${result.type},$value,s,$accuracy\n")

        val bestKey = result.prefKey.replace("last_", "best_")
        val oldBest = prefs.getFloat(bestKey, -1f)
        val editor = prefs.edit()
            .putFloat(result.prefKey, result.seconds.toFloat())
            .putString("attempt_status", "Užfiksuota ${result.type}: ${String.format(Locale.US, "%.2f", result.seconds)} s")
        if (oldBest <= 0f || result.seconds < oldBest) editor.putFloat(bestKey, result.seconds.toFloat())
        editor.apply()
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
            String.format(Locale.US, "%.2f", sampleRateHz),
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
        val elevation = if (location.hasAltitude()) {
            "<ele>${String.format(Locale.US, "%.2f", location.altitude)}</ele>"
        } else {
            ""
        }
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
            .putFloat("sample_hz", sampleRateHz.toFloat())
            .putString("gps_quality", quality)
            .putFloat("distance_m", totalDistanceMeters.toFloat())
            .putFloat("max_speed_kmh", (maxSpeedMps * 3.6).toFloat())
            .putInt("point_count", pointCount)
            .putLong("duration_ms", max(0L, System.currentTimeMillis() - startedAt))
            .putLong("last_update_ms", System.currentTimeMillis())
            .apply()
    }

    private fun gpsQuality(accuracyM: Float, speedAccuracyKmh: Float, hasGpsSpeed: Boolean): String {
        return when {
            hasGpsSpeed && accuracyM <= 8f && (speedAccuracyKmh < 0f || speedAccuracyKmh <= 4f) -> "GERAS"
            hasGpsSpeed && accuracyM <= 20f && (speedAccuracyKmh < 0f || speedAccuracyKmh <= 7f) -> "TINKAMAS"
            else -> "SILPNAS"
        }
    }

    private fun updateNotification(speedKmh: Double, quality: String) {
        val text = "$mode • ${String.format(Locale.US, "%.0f", speedKmh)} km/h • " +
            "${String.format(Locale.US, "%.2f", totalDistanceMeters / 1000.0)} km • " +
            "${String.format(Locale.US, "%.1f", sampleRateHz)} Hz • GPS $quality"
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
        } else {
            Notification.Builder(this)
        }
        return builder
            .setContentTitle("Marių Ride Lab įrašinėja")
            .setContentText(text)
            .setSmallIcon(android.R.drawable.ic_menu_mylocation)
            .setContentIntent(pending)
            .setOngoing(true)
            .setOnlyAlertOnce(true)
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

    private fun acquireWakeLock() {
        if (wakeLock?.isHeld == true) return
        val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "$packageName:ride-tracking").apply {
            setReferenceCounted(false)
            acquire(MAX_WAKE_LOCK_MS)
        }
    }

    private fun releaseWakeLock() {
        val lock = wakeLock
        if (lock?.isHeld == true) runCatching { lock.release() }
        wakeLock = null
    }

    private fun stopTracking() {
        try {
            locationManager.removeUpdates(this)
        } catch (_: Exception) {
        }

        if (sessionId.isNotEmpty()) {
            closeGpx()
            prefs.edit().putString("last_session_id", sessionId).apply()
        }
        currentSessionFile().delete()
        prefs.edit()
            .putBoolean("recording", false)
            .putFloat("speed_kmh", 0f)
            .putString("attempt_status", "Kelionė išsaugota")
            .apply()
        releaseWakeLock()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
        sessionId = ""
    }

    private fun closeGpx() {
        val file = gpxFile()
        if (!file.exists()) return
        val tail = runCatching { file.readText().takeLast(64) }.getOrDefault("")
        if (!tail.contains("</gpx>")) file.appendText("</trkseg></trk></gpx>\n")
    }

    override fun onDestroy() {
        try {
            locationManager.removeUpdates(this)
        } catch (_: Exception) {
        }
        releaseWakeLock()
        if (!explicitStop && sessionId.isNotEmpty()) {
            prefs.edit().putString("attempt_status", "Android perkrovė GPS tarnybą").apply()
        }
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
    private fun xmlEscape(value: String): String = value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&apos;")

    override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}
    override fun onProviderEnabled(provider: String) {}
    override fun onProviderDisabled(provider: String) {
        performanceEngine.reset()
        prefs.edit()
            .putString("gps_quality", "GPS IŠJUNGTAS")
            .putString("attempt_status", "Įjunk GPS")
            .apply()
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
        private const val MAX_WAKE_LOCK_MS = 8 * 60 * 60 * 1000L
    }
}
