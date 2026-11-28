package com.mariuauto.motosuptracker

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PerformanceEngineTest {
    @Test
    fun standingStartProducesInterpolatedZeroToHundred() {
        val engine = PerformanceEngine()
        engine.addSample(0.0, seconds(0.0), 0.0, 4.0)
        engine.addSample(0.0, seconds(1.1), 0.0, 4.0)
        engine.addSample(0.0, seconds(2.2), 0.0, 4.0)
        engine.addSample(50.0, seconds(3.2), 20.0, 4.0)
        val results = engine.addSample(100.0, seconds(4.2), 30.0, 4.0)

        val result = results.single { it.type == "0-100 km/h" }
        assertEquals(1.98, result.seconds, 0.02)
        assertEquals("last_0_100_s", result.prefKey)
    }

    @Test
    fun accelerationDoesNotStartWithoutStationaryArm() {
        val engine = PerformanceEngine()
        engine.addSample(20.0, seconds(0.0), 0.0, 5.0)
        engine.addSample(60.0, seconds(1.0), 20.0, 5.0)
        val results = engine.addSample(110.0, seconds(2.0), 30.0, 5.0)

        assertTrue(results.none { it.type == "0-100 km/h" })
    }

    @Test
    fun rollingEightyToOneTwentyIsInterpolated() {
        val engine = PerformanceEngine()
        engine.addSample(70.0, seconds(0.0), 0.0, 4.0)
        engine.addSample(90.0, seconds(1.0), 20.0, 4.0)
        val results = engine.addSample(130.0, seconds(2.0), 30.0, 4.0)

        val result = results.single { it.type == "80-120 km/h" }
        assertEquals(1.25, result.seconds, 0.01)
    }

    @Test
    fun brakingHundredToZeroUsesLowSpeedFinishThreshold() {
        val engine = PerformanceEngine()
        engine.addSample(110.0, seconds(0.0), 0.0, 5.0)
        engine.addSample(105.0, seconds(0.5), 15.0, 5.0)
        engine.addSample(90.0, seconds(1.0), 15.0, 5.0)
        val results = engine.addSample(0.0, seconds(2.0), 25.0, 5.0)

        val result = results.single { it.type == "100-0 km/h" }
        assertEquals(1.30, result.seconds, 0.02)
    }

    @Test
    fun standingQuarterMileUsesDistanceInterpolation() {
        val engine = PerformanceEngine()
        engine.addSample(0.0, seconds(0.0), 0.0, 4.0)
        engine.addSample(0.0, seconds(1.1), 0.0, 4.0)
        engine.addSample(0.0, seconds(2.2), 0.0, 4.0)
        engine.addSample(10.0, seconds(3.2), 1.0, 4.0)
        engine.addSample(50.0, seconds(8.2), 200.0, 4.0)
        val results = engine.addSample(100.0, seconds(13.2), 202.0, 4.0)

        val result = results.single { it.type == "0-402 m" }
        assertEquals(10.89, result.seconds, 0.03)
    }

    private fun seconds(value: Double): Long = (value * 1_000_000_000L).toLong()
}
