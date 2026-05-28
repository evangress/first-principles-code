"""Tests for the Gear, Electrical, and Mechatronics classes."""

import math

import pytest

from library.gear import Gear
from library.electrical import Electrical
from library.mechatronics import Mechatronics

gear = Gear()
electrical = Electrical()
mechatronics = Mechatronics()


# --- Gear ------------------------------------------------------------------

def test_gear_ratio_reduces_speed_and_multiplies_torque():
    ratio = gear.gear_ratio(driver_teeth=10, driven_teeth=40)
    assert ratio == pytest.approx(4.0)
    # A 4:1 reduction quarters the output speed...
    assert gear.output_speed(input_speed=1000.0, gear_ratio=ratio) == pytest.approx(250.0)
    # ...and (ideally) quadruples the torque.
    assert gear.output_torque(
        input_torque=10.0, gear_ratio=ratio,
    ) == pytest.approx(40.0)


def test_powertrain_ratio_is_the_product_of_stages():
    assert gear.powertrain_ratio(stage_ratios=[3.0, 2.0, 1.5]) == pytest.approx(9.0)


# --- Electrical ------------------------------------------------------------

def test_parallel_resistance_is_below_the_smallest_resistor():
    total = electrical.parallel_resistance(resistances=[100.0, 100.0])
    assert total == pytest.approx(50.0)
    assert total < 100.0


def test_series_resistance_adds():
    assert electrical.series_resistance(
        resistances=[100.0, 200.0, 300.0],
    ) == pytest.approx(600.0)


def test_rc_time_constant_and_power():
    assert electrical.rc_time_constant(
        resistance=1000.0, capacitance=1e-6,
    ) == pytest.approx(1e-3)
    assert electrical.power(voltage=10.0, current=2.0) == pytest.approx(20.0)


# --- Mechatronics ----------------------------------------------------------

def test_ballscrew_linear_speed():
    """600 rpm on a 5 mm lead -> 50 mm/s."""
    assert mechatronics.ballscrew_linear_speed(
        motor_rpm=600.0, lead=5.0,
    ) == pytest.approx(50.0)


def test_reflected_inertia_falls_with_square_of_ratio():
    """A 2:1 reduction makes the load look 1/4 as heavy to the motor."""
    assert mechatronics.reflected_inertia(
        load_inertia=0.04, gear_ratio=2.0,
    ) == pytest.approx(0.01)


def test_motor_power_from_torque_and_speed():
    """P = T*omega, with omega = rpm*2*pi/60."""
    expected = 2.0 * (3000.0 * 2 * math.pi / 60.0)
    assert mechatronics.motor_power(
        torque=2.0, speed_rpm=3000.0,
    ) == pytest.approx(expected)
