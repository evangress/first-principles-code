"""Tests for library.dynamics.Dynamics.

These tests double as a pytest tutorial. Notice three ideas:

    * ``pytest.approx`` compares floating-point numbers with a tolerance, so
      9.999999 == approx(10) - essential when results come from real math.
    * ``@pytest.mark.parametrize`` runs the same test body over many inputs,
      turning a table of known answers into many individual test cases.
    * Each test name reads as a sentence describing the behaviour it checks.

Run just this file with:  uv run pytest tests/test_dynamics.py
"""

import pytest

from library.dynamics import Dynamics

# One shared instance is fine because the methods hold no state.
dyn = Dynamics()


def test_displacement_matches_kinematic_formula():
    """x = x0 + v0*t + 1/2*a*t^2 for the README's headline example."""
    result = dyn.displacement_constant_acceleration(
        initial_position=0.0, initial_velocity=5.0,
        acceleration=9.81, time=3.0,
    )
    assert result == pytest.approx(59.145)


def test_final_velocity_is_linear_in_time():
    """v = v0 + a*t: starting from rest at 9.81 m/s^2 for 2 s gives 19.62 m/s."""
    assert dyn.final_velocity(
        initial_velocity=0.0, acceleration=9.81, time=2.0,
    ) == pytest.approx(19.62)


def test_velocity_from_distance():
    """v^2 = v0^2 + 2*a*d, so from rest with a=2 over d=4 gives v=4 m/s."""
    assert dyn.velocity_from_distance(
        initial_velocity=0.0, acceleration=2.0, distance=4.0,
    ) == pytest.approx(4.0)


@pytest.mark.parametrize(
    "angle_deg, expected_range",
    [
        (45, 40.7886),   # 45 degrees gives the maximum range
        (30, 35.3240),
        (60, 35.3240),   # complementary angles share the same range
    ],
)
def test_projectile_range_over_angles(angle_deg, expected_range):
    """Range R = v^2 sin(2*theta)/g, checked at several launch angles."""
    result = dyn.projectile_range(speed=20.0, angle_deg=angle_deg)
    assert result == pytest.approx(expected_range, rel=1e-4)


def test_newtons_second_law_and_energy():
    """Spot-check the simple algebraic relations."""
    assert dyn.newtons_second_law(mass=2.0, acceleration=3.0) == pytest.approx(6.0)
    assert dyn.kinetic_energy(mass=2.0, velocity=3.0) == pytest.approx(9.0)
    assert dyn.momentum(mass=2.0, velocity=3.0) == pytest.approx(6.0)
    assert dyn.centripetal_acceleration(speed=10.0, radius=2.0) == pytest.approx(50.0)
