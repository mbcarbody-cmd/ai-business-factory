package com.mariuauto.motosuptracker

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
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
    private var sessionId: String = ""
    private var mode: String = "SUP"
    private var lastLocation: Location? = null
    private var totalDistanceMeters: Double = 0.0
    private var pointCount: Int = 0
    private var maxSpeedMps: Double = 0.0
    private var startedAt: Long = 0L

    override fun onCreate() {
        super.onCreate()
        locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        ensureChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            stopTracking()
            return START_NOT_STICKY
        }

        mode = intent?.getStringExtra(EXTRA_MODE) ?: "SUP"
        sessionId = newSessionId()
        startedAt = System.currentTimeMillis()
        writeHeader()
        startForeground(NOTIFICATION_ID, buildNotification("Waiting for GPS"))
        startLocationUpdates()
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun startLocationUpdates() {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            stopSelf()
            return
        }

        val minTimeMs = if (mode == "MOTO") 1000L else 2500L
        val minDistanceM = if (mode == "MOTO") 5f else 2f
        try {
            locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                minTimeMs,
                minDistanceM,
                this
            )
        } catch (_: Exception) {
            stopSelf()
        }
    }

    override fun onLocationChanged(location: Location) {
        val previous = lastLocation
        val step = if (previous != null) previous.distanceTo(location).toDouble() else 0.0
        val dtSec = if (previous != null) max(0.5, (location.time - previous.time) / 1000.0) else 0.0
        val speed = if (location.hasSpeed()) location.speed.toDouble() else if (dtSec > 0) step / dtSec else 0.0
        val accel = if (previous != null && dtSec > 0) (speed - previous.speed.toDouble()) / dtSec else 0.0

        val accepted = acceptPoint(location, step, speed)
        if (accepted) {
            totalDistanceMeters += step
            pointCount += 1
            maxSpeedMps = max(maxSpeedMps, speed)
            appendCsv(location, speed, accel)
            lastLocation = location
        }
        updateNotification(location, speed, accepted)
    }

    private fun acceptPoint(location: Location, step: Double, speed: Double): Boolean {
        if (location.accuracy > 80f) return false
        if (mode == "SUP") {
            if (speed > 12.0) return false
            if (step > 90.0) return false
        } else {
            if (speed > 110.0) return false
            if (step > 300.0) return false
        }
        return true
    }

    private fun writeHeader() {
        csvFile().writeText("time_iso,mode,lat,lon,accuracy_m,speed_mps,speed_kmh,accel_ms2,total_distance_m,altitude_m,bearing_deg\n")
        currentSessionFile().writeText(sessionId)
    }

    private fun appendCsv(location: Location, speed: Double, accel: Double) {
        val line = listOf(
            iso(location.time),
            mode,
            location.latitude.toString(),
            location.longitude.toString(),
            location.accuracy.toString(),
            String.format(Locale.US, "%.3f", speed),
            String.format(Locale.US, "%.1f", speed * 3.6),
            String.format(Locale.US, "%.3f", accel),
            String.format(Locale.US, "%.1f", totalDistanceMeters),
            if (location.hasAltitude()) location.altitude.toString() else "",
            if (location.hasBearing()) location.bearing.toString() else ""
        ).joinToString(",")
        csvFile().appendText(line + "\n")
    }

    private fun updateNotification(location: Location, speed: Double, accepted: Boolean) {
        val text = "${mode} ${pointCount} pts ${String.format(Locale.US, "%.2f", totalDistanceMeters / 1000.0)} km ${String.format(Locale.US, "%.0f", speed * 3.6)} km/h ${if (accepted) "OK" else "filtered"}"
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.notify(NOTIFICATION_ID, buildNotification(text))
    }

    private fun buildNotification(text: String): Notification {
        val builder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Notification.Builder(this, CHANNEL_ID)
        } else {
            Notification.Builder(this)
        }
        return builder
            .setContentTitle("Moto SUP Tracker recording")
            .setContentText(text)
            .setSmallIcon(android.R.drawable.ic_menu_mylocation)
            .setOngoing(true)
            .build()
    }

    private fun ensureChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            val channel = NotificationChannel(CHANNEL_ID, "GPS recording", NotificationManager.IMPORTANCE_LOW)
            manager.createNotificationChannel(channel)
        }
    }

    private fun stopTracking() {
        try { locationManager.removeUpdates(this) } catch (_: Exception) {}
        currentSessionFile().delete()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun csvFile(): File = File(filesDir, "$sessionId.csv")
    private fun currentSessionFile(): File = File(filesDir, "current_session.txt")
    private fun newSessionId(): String = "track_" + SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
    private fun iso(timeMs: Long): String = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSZ", Locale.US).format(Date(timeMs))

    override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}
    override fun onProviderEnabled(provider: String) {}
    override fun onProviderDisabled(provider: String) {}

    companion object {
        const val ACTION_STOP = "com.mariuauto.motosuptracker.STOP"
        const val EXTRA_MODE = "mode"
        private const val CHANNEL_ID = "gps_recording"
        private const val NOTIFICATION_ID = 42
    }
}
