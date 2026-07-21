package lt.mariuauto.riderecorder

import android.location.Location
import java.io.File
import java.util.concurrent.CopyOnWriteArrayList

data class RideSnapshot(
    val isRecording: Boolean = false,
    val startedAt: Long = 0L,
    val speedKmh: Double = 0.0,
    val maxSpeedKmh: Double = 0.0,
    val distanceMeters: Double = 0.0,
    val points: Int = 0,
    val lastFile: File? = null
)

object RideStore {
    val locations = CopyOnWriteArrayList<Location>()
    @Volatile var snapshot = RideSnapshot()
    val listeners = CopyOnWriteArrayList<(RideSnapshot) -> Unit>()

    fun publish(value: RideSnapshot) {
        snapshot = value
        listeners.forEach { it(value) }
    }

    fun resetForStart(now: Long) {
        locations.clear()
        publish(RideSnapshot(isRecording = true, startedAt = now))
    }
}
