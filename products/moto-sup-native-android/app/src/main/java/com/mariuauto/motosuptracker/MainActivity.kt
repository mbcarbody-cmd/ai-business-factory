package com.mariuauto.motosuptracker

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import java.io.File
import java.util.Locale
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

class MainActivity : Activity() {
    private lateinit var status: TextView
    private lateinit var speed: TextView
    private lateinit var gps: TextView
    private lateinit var trip: TextView
    private lateinit var attempt: TextView
    private lateinit var performance: TextView
    private lateinit var history: TextView
    private lateinit var modeGroup: RadioGroup
    private lateinit var motoButton: RadioButton
    private lateinit var supButton: RadioButton
    private lateinit var startButton: Button
    private lateinit var stopButton: Button
    private lateinit var exportButton: Button

    private val handler = Handler(Looper.getMainLooper())
    private val refreshTask = object : Runnable {
        override fun run() {
            refreshDashboard()
            handler.postDelayed(this, 750L)
        }
    }

    private var pendingExport: File? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        buildUi()
        requestNeededPermissions()
    }

    override fun onResume() {
        super.onResume()
        handler.removeCallbacks(refreshTask)
        handler.post(refreshTask)
    }

    override fun onPause() {
        handler.removeCallbacks(refreshTask)
        super.onPause()
    }

    private fun buildUi() {
        val scroll = ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(20), dp(18), dp(28))
            gravity = Gravity.CENTER_HORIZONTAL
            setBackgroundColor(Color.rgb(7, 17, 31))
        }

        root.addView(text("MARIŲ RIDE LAB", 27f, true))
        root.addView(text("Yamaha FJR1300A 2019 • v${appVersion()}", 14f, false).apply {
            setTextColor(Color.LTGRAY)
        })

        status = text("Neįrašinėjama", 16f, true)
        root.addView(status, fullWidth(top = 18))

        speed = text("0", 72f, true).apply { setTextColor(Color.WHITE) }
        root.addView(speed, fullWidth(top = 6))
        root.addView(text("km/h", 18f, false).apply { setTextColor(Color.LTGRAY) })

        gps = cardText("GPS: laukiama", 15f)
        trip = cardText("Kelionė: 0 m • 00:00 • max 0 km/h", 15f)
        attempt = cardText("Palauk gero GPS", 15f)
        performance = cardText(
            "0–100: —\n80–120: —\n100–0: —\n402 m: —",
            18f
        )

        root.addView(gps, fullWidth(top = 18))
        root.addView(trip, fullWidth(top = 10))
        root.addView(attempt, fullWidth(top = 10))
        root.addView(performance, fullWidth(top = 10))

        modeGroup = RadioGroup(this).apply {
            orientation = RadioGroup.HORIZONTAL
            gravity = Gravity.CENTER
        }
        motoButton = RadioButton(this).apply {
            text = "MOTO"
            isChecked = true
            setTextColor(Color.WHITE)
        }
        supButton = RadioButton(this).apply {
            text = "SUP"
            setTextColor(Color.WHITE)
        }
        modeGroup.addView(motoButton)
        modeGroup.addView(supButton)
        root.addView(modeGroup, fullWidth(top = 14))

        startButton = button("PRADĖTI ĮRAŠYMĄ") { startTracking() }
        stopButton = button("BAIGTI IR IŠSAUGOTI") { stopTracking() }
        exportButton = button("EKSPORTUOTI PASKUTINĘ KELIONĘ (.ZIP)") { exportLastSession() }
        root.addView(startButton, fullWidth(top = 8))
        root.addView(stopButton, fullWidth(top = 8))
        root.addView(exportButton, fullWidth(top = 8))
        root.addView(button("PROGRAMOS IR BATERIJOS NUSTATYMAI") { openAppSettings() }, fullWidth(top = 8))
        root.addView(button("ATIDARYTI GPS NUSTATYMUS") {
            startActivity(Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS))
        }, fullWidth(top = 8))

        root.addView(text("Paskutiniai rezultatai", 19f, true), fullWidth(top = 22))
        history = cardText("Rezultatų dar nėra", 14f)
        root.addView(history, fullWidth(top = 8))

        root.addView(text(
            "0–100 laikmatis aktyvuojamas tik bent 1 sekundę stovėjus ir esant tinkamam GPS. 100–0 pabaiga praktiškai fiksuojama ties 3 km/h, nes telefono GPS prie nulio triukšmauja. Bandymus atlik tik uždaroje trasoje.",
            12f,
            false
        ).apply { setTextColor(Color.GRAY) }, fullWidth(top = 18))

        scroll.addView(root)
        setContentView(scroll)
    }

    private fun requestNeededPermissions() {
        val permissions = mutableListOf(Manifest.permission.ACCESS_FINE_LOCATION)
        if (Build.VERSION.SDK_INT >= 33) permissions.add(Manifest.permission.POST_NOTIFICATIONS)
        val missing = permissions.filter { checkSelfPermission(it) != PackageManager.PERMISSION_GRANTED }
        if (missing.isNotEmpty()) requestPermissions(missing.toTypedArray(), REQUEST_PERMISSIONS)
    }

    private fun startTracking() {
        val prefs = getSharedPreferences(TrackingService.PREFS, MODE_PRIVATE)
        if (prefs.getBoolean("recording", false)) {
            Toast.makeText(this, "Įrašymas jau vyksta", Toast.LENGTH_SHORT).show()
            return
        }
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Reikia tikslios vietos leidimo", Toast.LENGTH_LONG).show()
            requestNeededPermissions()
            return
        }

        val mode = if (motoButton.isChecked) "MOTO" else "SUP"
        val intent = Intent(this, TrackingService::class.java).apply {
            action = TrackingService.ACTION_START
            putExtra(TrackingService.EXTRA_MODE, mode)
            putExtra(TrackingService.EXTRA_PROFILE, "Yamaha FJR1300A 2019")
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(intent) else startService(intent)
        Toast.makeText(this, "Įrašymas pradėtas: $mode", Toast.LENGTH_SHORT).show()
        handler.postDelayed({ refreshDashboard() }, 350L)
    }

    private fun stopTracking() {
        val prefs = getSharedPreferences(TrackingService.PREFS, MODE_PRIVATE)
        if (!prefs.getBoolean("recording", false)) {
            Toast.makeText(this, "Įrašymas nevyksta", Toast.LENGTH_SHORT).show()
            return
        }

        val intent = Intent(this, TrackingService::class.java).apply { action = TrackingService.ACTION_STOP }
        startService(intent)
        Toast.makeText(this, "Kelionė baigiama ir saugoma", Toast.LENGTH_SHORT).show()
        handler.postDelayed({ refreshDashboard() }, 700L)
    }

    private fun refreshDashboard() {
        val prefs = getSharedPreferences(TrackingService.PREFS, MODE_PRIVATE)
        val recording = prefs.getBoolean("recording", false)
        val mode = prefs.getString("mode", "MOTO") ?: "MOTO"
        val speedKmh = prefs.getFloat("speed_kmh", 0f)
        val accuracy = prefs.getFloat("accuracy_m", -1f)
        val speedAccuracy = prefs.getFloat("speed_accuracy_kmh", -1f)
        val sampleHz = prefs.getFloat("sample_hz", 0f)
        val points = prefs.getInt("point_count", 0)
        val distance = prefs.getFloat("distance_m", 0f)
        val duration = prefs.getLong("duration_ms", 0L)
        val maxSpeed = prefs.getFloat("max_speed_kmh", 0f)
        val quality = prefs.getString("gps_quality", "LAUKIAMA") ?: "LAUKIAMA"
        val attemptStatus = prefs.getString("attempt_status", "") ?: ""
        val lastUpdate = prefs.getLong("last_update_ms", 0L)
        val stale = recording && lastUpdate > 0L && System.currentTimeMillis() - lastUpdate > 5_000L

        status.text = when {
            stale -> "● GPS DUOMENYS SUSTOJO • $mode"
            recording -> "● ĮRAŠINĖJAMA • $mode • $points taškai"
            else -> "Neįrašinėjama"
        }
        status.setTextColor(
            when {
                stale -> Color.rgb(255, 120, 90)
                recording -> Color.rgb(80, 220, 140)
                else -> Color.LTGRAY
            }
        )
        speed.text = String.format(Locale.getDefault(), "%.0f", speedKmh)

        gps.text = buildString {
            append("GPS: $quality")
            if (accuracy >= 0f) append(" • ±${String.format(Locale.getDefault(), "%.0f", accuracy)} m")
            if (speedAccuracy >= 0f) append(" • greičio ±${String.format(Locale.getDefault(), "%.1f", speedAccuracy)} km/h")
            if (sampleHz > 0f) append(" • ${String.format(Locale.getDefault(), "%.1f", sampleHz)} Hz")
        }
        trip.text = "Kelionė: ${formatDistance(distance)} • ${formatDuration(duration)} • max ${String.format(Locale.getDefault(), "%.0f", maxSpeed)} km/h"
        attempt.text = if (stale) "Patikrink GPS ir baterijos ribojimus" else attemptStatus.ifBlank { "Palauk GPS" }

        performance.text = listOf(
            performanceLine("0–100", prefs, "last_0_100_s", "best_0_100_s"),
            performanceLine("80–120", prefs, "last_80_120_s", "best_80_120_s"),
            performanceLine("100–0", prefs, "last_100_0_s", "best_100_0_s"),
            performanceLine("402 m", prefs, "last_402m_s", "best_402m_s")
        ).joinToString("\n")

        history.text = loadHistory()
        modeGroup.isEnabled = !recording
        motoButton.isEnabled = !recording
        supButton.isEnabled = !recording
        startButton.isEnabled = !recording
        stopButton.isEnabled = recording
        exportButton.isEnabled = !recording && findLastSessionId() != null
    }

    private fun performanceLine(
        label: String,
        prefs: android.content.SharedPreferences,
        lastKey: String,
        bestKey: String
    ): String {
        val last = prefs.getFloat(lastKey, -1f)
        val best = prefs.getFloat(bestKey, -1f)
        return buildString {
            append("$label: ${formatResult(last)}")
            if (best > 0f) append(" • geriausias ${formatResult(best)}")
        }
    }

    private fun loadHistory(): String {
        val file = File(filesDir, TrackingService.RESULTS_FILE)
        if (!file.exists()) return "Rezultatų dar nėra"
        val rows = file.readLines().drop(1).takeLast(10).reversed()
        if (rows.isEmpty()) return "Rezultatų dar nėra"
        return rows.mapNotNull { row ->
            val p = row.split(',')
            if (p.size < 7) null else "${p[0].replace('T', ' ').take(19)} • ${p[3]}: ${p[4]} ${p[5]} • GPS ±${p[6]} m"
        }.joinToString("\n")
    }

    private fun exportLastSession() {
        val prefs = getSharedPreferences(TrackingService.PREFS, MODE_PRIVATE)
        if (prefs.getBoolean("recording", false)) {
            Toast.makeText(this, "Pirma baik įrašymą", Toast.LENGTH_LONG).show()
            return
        }
        val session = findLastSessionId()
        if (session == null) {
            Toast.makeText(this, "Išsaugotų kelionių dar nėra", Toast.LENGTH_LONG).show()
            return
        }

        val zip = File(cacheDir, "$session.zip")
        try {
            ZipOutputStream(zip.outputStream().buffered()).use { output ->
                addToZip(output, File(filesDir, "$session.gpx"))
                addToZip(output, File(filesDir, "$session.csv"))
                addToZip(output, File(filesDir, TrackingService.RESULTS_FILE))
            }
        } catch (e: Exception) {
            Toast.makeText(this, "Nepavyko paruošti eksporto: ${e.message}", Toast.LENGTH_LONG).show()
            return
        }

        pendingExport = zip
        val intent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "application/zip"
            putExtra(Intent.EXTRA_TITLE, "Mariu_Ride_$session.zip")
        }
        startActivityForResult(intent, REQUEST_EXPORT)
    }

    private fun addToZip(output: ZipOutputStream, file: File) {
        if (!file.exists()) return
        output.putNextEntry(ZipEntry(file.name))
        file.inputStream().buffered().use { it.copyTo(output) }
        output.closeEntry()
    }

    private fun findLastSessionId(): String? {
        val prefs = getSharedPreferences(TrackingService.PREFS, MODE_PRIVATE)
        val saved = prefs.getString("last_session_id", null)
        if (!saved.isNullOrBlank() && File(filesDir, "$saved.gpx").exists()) return saved
        return filesDir.listFiles { file -> file.extension.equals("gpx", true) }
            ?.maxByOrNull { it.lastModified() }
            ?.nameWithoutExtension
    }

    private fun openAppSettings() {
        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.parse("package:$packageName")
        }
        startActivity(intent)
    }

    @Deprecated("Legacy Activity result keeps this dependency-free")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != REQUEST_EXPORT || resultCode != RESULT_OK) return
        val source = pendingExport ?: return
        val uri: Uri = data?.data ?: return
        try {
            contentResolver.openOutputStream(uri)?.use { output ->
                source.inputStream().use { it.copyTo(output) }
            } ?: error("Nepavyko atidaryti pasirinkto failo")
            Toast.makeText(this, "Kelionė eksportuota", Toast.LENGTH_LONG).show()
        } catch (e: Exception) {
            Toast.makeText(this, "Eksporto klaida: ${e.message}", Toast.LENGTH_LONG).show()
        } finally {
            pendingExport = null
        }
    }

    private fun text(value: String, size: Float, bold: Boolean): TextView = TextView(this).apply {
        text = value
        textSize = size
        gravity = Gravity.CENTER
        setTextColor(Color.WHITE)
        if (bold) setTypeface(typeface, android.graphics.Typeface.BOLD)
    }

    private fun cardText(value: String, size: Float): TextView = text(value, size, false).apply {
        gravity = Gravity.START
        setPadding(dp(16), dp(14), dp(16), dp(14))
        setBackgroundColor(Color.rgb(17, 33, 52))
    }

    private fun button(label: String, click: () -> Unit): Button = Button(this).apply {
        text = label
        setOnClickListener { click() }
        minHeight = dp(52)
    }

    private fun fullWidth(top: Int = 0): LinearLayout.LayoutParams = LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT,
        ViewGroup.LayoutParams.WRAP_CONTENT
    ).apply { topMargin = dp(top) }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()

    private fun formatResult(seconds: Float): String = if (seconds > 0f) {
        String.format(Locale.getDefault(), "%.2f s", seconds)
    } else {
        "—"
    }

    private fun formatDistance(meters: Float): String = if (meters < 1000f) {
        String.format(Locale.getDefault(), "%.0f m", meters)
    } else {
        String.format(Locale.getDefault(), "%.2f km", meters / 1000f)
    }

    private fun formatDuration(ms: Long): String {
        val totalSeconds = ms / 1000L
        val hours = totalSeconds / 3600L
        val minutes = (totalSeconds % 3600L) / 60L
        val seconds = totalSeconds % 60L
        return if (hours > 0) {
            String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds)
        } else {
            String.format(Locale.US, "%02d:%02d", minutes, seconds)
        }
    }

    @Suppress("DEPRECATION")
    private fun appVersion(): String = runCatching {
        packageManager.getPackageInfo(packageName, 0).versionName ?: "?"
    }.getOrDefault("?")

    companion object {
        private const val REQUEST_PERMISSIONS = 10
        private const val REQUEST_EXPORT = 20
    }
}
