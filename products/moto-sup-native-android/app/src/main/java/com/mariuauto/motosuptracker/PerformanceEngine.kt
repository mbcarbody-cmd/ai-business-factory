package com.mariuauto.motosuptracker

import kotlin.math.abs
import kotlin.math.max

data class PerformanceResult(
    val type: String,
    val seconds: Double,
    val accuracyM: Double,
    val prefKey: String
)

/**
 * Pure Kotlin performance timing engine.
 *
 * It receives already filtered GPS samples and emits completed attempts.
 * Keeping this logic independent from Android makes it deterministic and unit-testable.
 */
class PerformanceEngine {
    private var previousSpeedKmh: Double? = null
    private var previousNs: Long? = null

    private var stoppedSinceNs = 0L
    private var accelerationArmed = false
    private var accelerationStartNs: Long? = null
    private var accelerationDistanceM = 0.0
    private var acceleration100Done = false
    private var quarterMileDone = false

    private var roll80StartNs: Long? = null
    private var rollCooldown = false

    private var brakingArmed = false
    private var brakingStartNs: Long? = null
    private var brakingPeakKmh = 0.0

    fun reset() {
        previousSpeedKmh = null
        previousNs = null
        stoppedSinceNs = 0L
        accelerationArmed = false
        accelerationStartNs = null
        accelerationDistanceM = 0.0
        acceleration100Done = false
        quarterMileDone = false
        roll80StartNs = null
        rollCooldown = false
        brakingArmed = false
        brakingStartNs = null
        brakingPeakKmh = 0.0
    }

    fun addSample(
        speedKmh: Double,
        elapsedRealtimeNs: Long,
        stepDistanceM: Double,
        accuracyM: Double
    ): List<PerformanceResult> {
        val safeSpeed = speedKmh.coerceAtLeast(0.0)
        val results = mutableListOf<PerformanceResult>()
        val prevSpeed = previousSpeedKmh
        val prevNs = previousNs

        if (prevSpeed == null || prevNs == null || elapsedRealtimeNs <= prevNs) {
            previousSpeedKmh = safeSpeed
            previousNs = elapsedRealtimeNs
            return results
        }

        updateStationaryArm(safeSpeed, elapsedRealtimeNs)
        processStandingStart(
            prevSpeed = prevSpeed,
            speed = safeSpeed,
            prevNs = prevNs,
            nowNs = elapsedRealtimeNs,
            stepDistanceM = stepDistanceM,
            accuracyM = accuracyM,
            results = results
        )
        processRollingAcceleration(prevSpeed, safeSpeed, prevNs, elapsedRealtimeNs, accuracyM, results)
        processBraking(prevSpeed, safeSpeed, prevNs, elapsedRealtimeNs, accuracyM, results)

        previousSpeedKmh = safeSpeed
        previousNs = elapsedRealtimeNs
        return results
    }

    private fun updateStationaryArm(speedKmh: Double, nowNs: Long) {
        if (speedKmh <= STATIONARY_MAX_KMH) {
            if (stoppedSinceNs == 0L) stoppedSinceNs = nowNs
            if (nowNs - stoppedSinceNs >= ARM_DELAY_NS) accelerationArmed = true
        } else {
            stoppedSinceNs = 0L
        }
    }

    private fun processStandingStart(
        prevSpeed: Double,
        speed: Double,
        prevNs: Long,
        nowNs: Long,
        stepDistanceM: Double,
        accuracyM: Double,
        results: MutableList<PerformanceResult>
    ) {
        if (
            accelerationArmed &&
            accelerationStartNs == null &&
            prevSpeed <= START_THRESHOLD_KMH &&
            speed > START_THRESHOLD_KMH
        ) {
            val startNs = crossingNs(prevSpeed, speed, START_THRESHOLD_KMH, prevNs, nowNs)
            accelerationStartNs = startNs
            val segmentFractionAfterStart = ((nowNs - startNs).toDouble() / (nowNs - prevNs).toDouble())
                .coerceIn(0.0, 1.0)
            accelerationDistanceM = stepDistanceM.coerceAtLeast(0.0) * segmentFractionAfterStart
            acceleration100Done = false
            quarterMileDone = false
            accelerationArmed = false
        } else if (accelerationStartNs != null) {
            accelerationDistanceM += stepDistanceM.coerceAtLeast(0.0)
        }

        val startNs = accelerationStartNs ?: return

        if (!acceleration100Done && prevSpeed < 100.0 && speed >= 100.0) {
            val finishNs = crossingNs(prevSpeed, speed, 100.0, prevNs, nowNs)
            val seconds = secondsBetween(startNs, finishNs)
            if (seconds in MIN_ACCEL_SECONDS..MAX_ATTEMPT_SECONDS) {
                results += PerformanceResult("0-100 km/h", seconds, accuracyM, "last_0_100_s")
            }
            acceleration100Done = true
        }

        if (!quarterMileDone && accelerationDistanceM >= QUARTER_MILE_M) {
            val segmentDistance = stepDistanceM.coerceAtLeast(0.0)
            val previousDistance = accelerationDistanceM - segmentDistance
            val fraction = if (segmentDistance > 0.01) {
                ((QUARTER_MILE_M - previousDistance) / segmentDistance).coerceIn(0.0, 1.0)
            } else {
                1.0
            }
            val finishNs = prevNs + ((nowNs - prevNs) * fraction).toLong()
            val seconds = secondsBetween(startNs, finishNs)
            if (seconds in MIN_QUARTER_SECONDS..MAX_QUARTER_SECONDS) {
                results += PerformanceResult("0-402 m", seconds, accuracyM, "last_402m_s")
            }
            quarterMileDone = true
        }

        if (speed <= STATIONARY_MAX_KMH && nowNs - startNs > CANCEL_AFTER_STOP_NS) {
            cancelStandingAttempt()
        } else if (acceleration100Done && quarterMileDone) {
            cancelStandingAttempt()
        } else if (nowNs - startNs > MAX_QUARTER_DURATION_NS) {
            cancelStandingAttempt()
        }
    }

    private fun processRollingAcceleration(
        prevSpeed: Double,
        speed: Double,
        prevNs: Long,
        nowNs: Long,
        accuracyM: Double,
        results: MutableList<PerformanceResult>
    ) {
        if (!rollCooldown && roll80StartNs == null && prevSpeed < 80.0 && speed >= 80.0) {
            roll80StartNs = crossingNs(prevSpeed, speed, 80.0, prevNs, nowNs)
        }

        val startNs = roll80StartNs
        if (startNs != null) {
            if (prevSpeed < 120.0 && speed >= 120.0) {
                val finishNs = crossingNs(prevSpeed, speed, 120.0, prevNs, nowNs)
                val seconds = secondsBetween(startNs, finishNs)
                if (seconds in MIN_ROLL_SECONDS..MAX_ATTEMPT_SECONDS) {
                    results += PerformanceResult("80-120 km/h", seconds, accuracyM, "last_80_120_s")
                }
                roll80StartNs = null
                rollCooldown = true
            } else if (speed < 70.0 || nowNs - startNs > MAX_ROLL_DURATION_NS) {
                roll80StartNs = null
            }
        }

        if (speed < 70.0) rollCooldown = false
    }

    private fun processBraking(
        prevSpeed: Double,
        speed: Double,
        prevNs: Long,
        nowNs: Long,
        accuracyM: Double,
        results: MutableList<PerformanceResult>
    ) {
        if (speed >= 100.0) {
            brakingArmed = true
            brakingPeakKmh = max(brakingPeakKmh, speed)
        }

        if (brakingArmed && brakingStartNs == null && prevSpeed >= 100.0 && speed < 100.0) {
            brakingStartNs = crossingNs(prevSpeed, speed, 100.0, prevNs, nowNs)
        }

        val startNs = brakingStartNs ?: return
        if (prevSpeed > BRAKE_FINISH_KMH && speed <= BRAKE_FINISH_KMH) {
            val finishNs = crossingNs(prevSpeed, speed, BRAKE_FINISH_KMH, prevNs, nowNs)
            val seconds = secondsBetween(startNs, finishNs)
            if (seconds in MIN_BRAKE_SECONDS..MAX_ATTEMPT_SECONDS) {
                results += PerformanceResult("100-0 km/h", seconds, accuracyM, "last_100_0_s")
            }
            resetBraking()
        } else if (speed > brakingPeakKmh + 5.0 || nowNs - startNs > MAX_BRAKE_DURATION_NS) {
            brakingStartNs = null
            brakingArmed = speed >= 100.0
            brakingPeakKmh = if (brakingArmed) speed else 0.0
        }
    }

    private fun cancelStandingAttempt() {
        accelerationStartNs = null
        accelerationDistanceM = 0.0
        acceleration100Done = false
        quarterMileDone = false
    }

    private fun resetBraking() {
        brakingStartNs = null
        brakingArmed = false
        brakingPeakKmh = 0.0
    }

    private fun crossingNs(
        prevSpeed: Double,
        speed: Double,
        threshold: Double,
        prevNs: Long,
        nowNs: Long
    ): Long {
        val delta = speed - prevSpeed
        if (abs(delta) < 0.0001) return nowNs
        val fraction = ((threshold - prevSpeed) / delta).coerceIn(0.0, 1.0)
        return prevNs + ((nowNs - prevNs) * fraction).toLong()
    }

    private fun secondsBetween(startNs: Long, finishNs: Long): Double =
        (finishNs - startNs) / 1_000_000_000.0

    companion object {
        private const val STATIONARY_MAX_KMH = 1.5
        private const val START_THRESHOLD_KMH = 1.0
        private const val BRAKE_FINISH_KMH = 3.0
        private const val QUARTER_MILE_M = 402.336

        private const val ARM_DELAY_NS = 1_000_000_000L
        private const val CANCEL_AFTER_STOP_NS = 2_000_000_000L
        private const val MAX_ROLL_DURATION_NS = 60_000_000_000L
        private const val MAX_BRAKE_DURATION_NS = 30_000_000_000L
        private const val MAX_QUARTER_DURATION_NS = 60_000_000_000L

        private const val MIN_ACCEL_SECONDS = 1.0
        private const val MIN_ROLL_SECONDS = 0.5
        private const val MIN_BRAKE_SECONDS = 0.5
        private const val MIN_QUARTER_SECONDS = 3.0
        private const val MAX_ATTEMPT_SECONDS = 30.0
        private const val MAX_QUARTER_SECONDS = 60.0
    }
}
