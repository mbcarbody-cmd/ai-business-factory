package com.mariuauto.motosuptracker

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.TextView
import android.widget.Toast
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : Activity() {
    private lateinit var status: TextView
    private lateinit var modeGroup: RadioGroup

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestNeededPermissions()
        buildUi()
        updateStatus()
    }

    private fun buildUi() {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 42, 32, 32)
            gravity = Gravity.CENTER_HORIZONTAL
        }

        val title = TextView(this).apply {
            text = "Moto SUP Tracker"
            textSize = 26f
            gravity = Gravity.CENTER
        }
        status = TextView(this).apply {
            textSize = 16f
            gravity = Gravity.CENTER
            text = "Ready"
        }

        modeGroup = RadioGroup(this).apply {
            orientation = RadioGroup.HORIZONTAL
            gravity = Gravity.CENTER
        }
        val sup = RadioButton(this).apply { text = "SUP"; isChecked = true }
        val moto = RadioButton(this).apply { text = "MOTO" }
        modeGroup.addView(sup)
        modeGroup.addView(moto)

        val start = Button(this).apply {
            text = "START RECORDING"
            setOnClickListener { startTracking() }
        }
        val stop = Button(this).apply {
            text = "STOP"
            setOnClickListener { stopTracking() }
        }
        val export = Button(this).apply {
            text = "SHOW LAST FILE"
            setOnClickListener { showLastFile() }
        }

        root.addView(title)
        root.addView(status)
        root.addView(modeGroup)
        root.addView(start)
        root.addView(stop)
        root.addView(export)
        setContentView(root)
    }

    private fun requestNeededPermissions() {
        val permissions = mutableListOf(Manifest.permission.ACCESS_FINE_LOCATION)
        if (Build.VERSION.SDK_INT >= 33) permissions.add(Manifest.permission.POST_NOTIFICATIONS)
        val missing = permissions.filter { checkSelfPermission(it) != PackageManager.PERMISSION_GRANTED }
        if (missing.isNotEmpty()) requestPermissions(missing.toTypedArray(), 10)
    }

    private fun startTracking() {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Location permission missing", Toast.LENGTH_LONG).show()
            requestNeededPermissions()
            return
        }
        val mode = if ((modeGroup.getChildAt(1) as RadioButton).isChecked) "MOTO" else "SUP"
        val intent = Intent(this, TrackingService::class.java).apply {
            putExtra(TrackingService.EXTRA_MODE, mode)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(intent) else startService(intent)
        Toast.makeText(this, "Recording started: $mode", Toast.LENGTH_SHORT).show()
        updateStatus()
    }

    private fun stopTracking() {
        val intent = Intent(this, TrackingService::class.java).apply { action = TrackingService.ACTION_STOP }
        startService(intent)
        Toast.makeText(this, "Recording stopped", Toast.LENGTH_SHORT).show()
        updateStatus()
    }

    private fun updateStatus() {
        val current = File(filesDir, "current_session.txt")
        status.text = if (current.exists()) {
            "Recording: ${current.readText()}"
        } else {
            "Not recording"
        }
    }

    private fun showLastFile() {
        val files = filesDir.listFiles { file -> file.extension == "csv" }?.sortedByDescending { it.lastModified() } ?: emptyList()
        if (files.isEmpty()) {
            Toast.makeText(this, "No track files yet", Toast.LENGTH_LONG).show()
            return
        }
        val f = files.first()
        val modified = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US).format(Date(f.lastModified()))
        Toast.makeText(this, "Last file: ${f.name} ${f.length()} bytes $modified", Toast.LENGTH_LONG).show()
    }
}
