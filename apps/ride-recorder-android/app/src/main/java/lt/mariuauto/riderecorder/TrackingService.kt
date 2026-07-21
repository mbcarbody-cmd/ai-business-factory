package lt.mariuauto.riderecorder

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.os.IBinder
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import com.google.android.gms.location.LocationCallback
import com.google.android.gms.location.LocationRequest
import com.google.android.gms.location.LocationResult
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import java.io.File
import java.time.Instant

class TrackingService : Service() {
    private val client by lazy { LocationServices.getFusedLocationProviderClient(this) }
    private val callback = object : LocationCallback() {
        override fun onLocationResult(result: LocationResult) {
            result.locations.forEach(::acceptLocation)
        }
    }

    override fun onCreate() {
        super.onCreate()
        createChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START -> startTracking()
            ACTION_STOP -> stopTrackingAndSave()
        }
        return START_NOT_STICKY
    }

    private fun startTracking() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            stopSelf()
            return
        }

        RideStore.resetForStart(System.currentTimeMillis())
        val openIntent = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_menu_mylocation)
            .setContentTitle("Ride Recorder")
            .setContentText("Kelionė įrašoma")
            .setOngoing(true)
            .setContentIntent(openIntent)
            .build()
        startForeground(NOTIFICATION_ID, notification)

        val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 1000L)
            .setMinUpdateDistanceMeters(2f)
            .build()
        client.requestLocationUpdates(request, callback, mainLooper)
    }

    private fun acceptLocation(location: Location) {
        if (location.accuracy > 40f) return
        val previous = RideStore.locations.lastOrNull()
        RideStore.locations.add(location)
        val added = if (previous != null) previous.distanceTo(location).toDouble() else 0.0
        val speed = if (location.hasSpeed()) location.speed * 3.6 else 0.0
        val old = RideStore.snapshot
        RideStore.publish(
            old.copy(
                speedKmh = speed,
                maxSpeedKmh = maxOf(old.maxSpeedKmh, speed),
                distanceMeters = old.distanceMeters + added,
                points = RideStore.locations.size
            )
        )
    }

    private fun stopTrackingAndSave() {
        client.removeLocationUpdates(callback)
        val file = writeGpx()
        val old = RideStore.snapshot
        RideStore.publish(old.copy(isRecording = false, speedKmh = 0.0, lastFile = file))
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun writeGpx(): File? {
        if (RideStore.locations.isEmpty()) return null
        val dir = File(filesDir, "rides").apply { mkdirs() }
        val file = File(dir, "ride-${System.currentTimeMillis()}.gpx")
        val body = buildString {
            append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            append("<gpx version=\"1.1\" creator=\"Ride Recorder\" xmlns=\"http://www.topografix.com/GPX/1/1\">\n<trk><name>Ride</name><trkseg>\n")
            RideStore.locations.forEach { l ->
                append("<trkpt lat=\"").append(l.latitude).append("\" lon=\"").append(l.longitude).append("\">")
                if (l.hasAltitude()) append("<ele>").append(l.altitude).append("</ele>")
                append("<time>").append(Instant.ofEpochMilli(l.time)).append("</time></trkpt>\n")
            }
            append("</trkseg></trk></gpx>\n")
        }
        file.writeText(body)
        return file
    }

    private fun createChannel() {
        val manager = getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(NotificationChannel(CHANNEL_ID, "Kelionės įrašymas", NotificationManager.IMPORTANCE_LOW))
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        const val ACTION_START = "ride.start"
        const val ACTION_STOP = "ride.stop"
        private const val CHANNEL_ID = "ride_tracking"
        private const val NOTIFICATION_ID = 1001
    }
}
