package lt.mariuauto.riderecorder

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import lt.mariuauto.riderecorder.databinding.ActivityMainBinding
import java.util.Locale
import kotlin.math.roundToInt

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private var pendingStart = false

    private val permissions = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { result ->
        val locationGranted = result[Manifest.permission.ACCESS_FINE_LOCATION] == true
        if (pendingStart && locationGranted) startRide()
        pendingStart = false
    }

    private val listener: (RideSnapshot) -> Unit = { snapshot ->
        runOnUiThread { render(snapshot) }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.startButton.setOnClickListener { ensurePermissionsAndStart() }
        binding.stopButton.setOnClickListener {
            ContextCompat.startForegroundService(
                this,
                Intent(this, TrackingService::class.java).setAction(TrackingService.ACTION_STOP)
            )
        }
        binding.shareButton.setOnClickListener { shareLastGpx() }
        render(RideStore.snapshot)
    }

    override fun onStart() {
        super.onStart()
        RideStore.listeners.add(listener)
    }

    override fun onStop() {
        RideStore.listeners.remove(listener)
        super.onStop()
    }

    private fun ensurePermissionsAndStart() {
        val fine = ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
        if (fine) {
            startRide()
        } else {
            pendingStart = true
            val requested = mutableListOf(Manifest.permission.ACCESS_FINE_LOCATION)
            if (android.os.Build.VERSION.SDK_INT >= 33) requested += Manifest.permission.POST_NOTIFICATIONS
            permissions.launch(requested.toTypedArray())
        }
    }

    private fun startRide() {
        ContextCompat.startForegroundService(
            this,
            Intent(this, TrackingService::class.java).setAction(TrackingService.ACTION_START)
        )
    }

    private fun render(s: RideSnapshot) {
        binding.statusText.text = if (s.isRecording) "Kelionė įrašoma" else "Pasiruošęs"
        binding.speedText.text = String.format(Locale.US, "%.0f km/h", s.speedKmh)
        binding.distanceText.text = String.format(Locale.US, "Atstumas: %.2f km", s.distanceMeters / 1000.0)
        binding.maxSpeedText.text = "Maks. greitis: ${s.maxSpeedKmh.roundToInt()} km/h"
        binding.pointsText.text = "GPS taškai: ${s.points}"
        binding.durationText.text = "Laikas: ${formatDuration(if (s.startedAt == 0L) 0L else System.currentTimeMillis() - s.startedAt)}"
        binding.startButton.isEnabled = !s.isRecording
        binding.stopButton.isEnabled = s.isRecording
        binding.shareButton.isEnabled = s.lastFile?.exists() == true
        binding.fileText.text = s.lastFile?.absolutePath ?: "GPX failas dar nesukurtas"
    }

    private fun formatDuration(ms: Long): String {
        val total = ms / 1000
        val h = total / 3600
        val m = (total % 3600) / 60
        val s = total % 60
        return String.format(Locale.US, "%02d:%02d:%02d", h, m, s)
    }

    private fun shareLastGpx() {
        val file = RideStore.snapshot.lastFile ?: return
        val uri = FileProvider.getUriForFile(this, "$packageName.files", file)
        startActivity(
            Intent.createChooser(
                Intent(Intent.ACTION_SEND).apply {
                    type = "application/gpx+xml"
                    putExtra(Intent.EXTRA_STREAM, uri)
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                },
                "Dalintis GPX"
            )
        )
    }
}
