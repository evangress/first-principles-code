"""dynamics.py - kinematics and rigid-body dynamics calculations.

Dynamics is the study of motion and the forces that cause it. This class
collects the everyday formulas an engineer reaches for: kinematic equations,
projectile motion, Newton's second law, and momentum/energy relations.

Every method takes keyword-only arguments (note the leading ``*``) so that
calls are self-documenting, and every method returns a plain number or tuple so
results compose easily with numpy and scipy.
"""

import math


class Dynamics:
    """Kinematics and rigid-body dynamics helpers.

    The methods are stateless, so one shared instance is fine::

        dyn = Dynamics()
        v = dyn.final_velocity(initial_velocity=0.0, acceleration=9.81, time=2.0)
    """

    # Standard gravity near Earth's surface [m/s^2]. Exposed as a class
    # attribute so callers can reuse it: ``Dynamics.GRAVITY``.
    GRAVITY = 9.80665

    def displacement_constant_acceleration(
        self, *, initial_position, initial_velocity, acceleration, time
    ):
        """Displacement under constant acceleration: x = x0 + v0*t + 1/2*a*t^2.

        :param initial_position: starting position x0 [m]
        :param initial_velocity: starting velocity v0 [m/s]
        :param acceleration: constant acceleration a [m/s^2]
        :param time: elapsed time t [s]
        :returns: position x at time t [m]
        """
        return (
            initial_position
            + initial_velocity * time
            + 0.5 * acceleration * time ** 2
        )

    def final_velocity(self, *, initial_velocity, acceleration, time):
        """Velocity after constant acceleration: v = v0 + a*t.

        :param initial_velocity: starting velocity v0 [m/s]
        :param acceleration: constant acceleration a [m/s^2]
        :param time: elapsed time t [s]
        :returns: velocity v at time t [m/s]
        """
        return initial_velocity + acceleration * time

    def velocity_from_distance(self, *, initial_velocity, acceleration, distance):
        """Velocity after travelling a distance: v^2 = v0^2 + 2*a*d.

        Useful when you know how far something moved but not how long it took.

        :param initial_velocity: starting velocity v0 [m/s]
        :param acceleration: constant acceleration a [m/s^2]
        :param distance: distance travelled d [m]
        :returns: final speed v [m/s] (always non-negative)
        """
        # max(..., 0.0) guards against tiny negative values from rounding.
        return math.sqrt(max(initial_velocity ** 2 + 2 * acceleration * distance, 0.0))

    def projectile_range(self, *, speed, angle_deg, gravity=GRAVITY):
        """Horizontal range of a projectile launched over flat ground.

        R = v^2 * sin(2*theta) / g.

        :param speed: launch speed [m/s]
        :param angle_deg: launch angle above horizontal [degrees]
        :param gravity: gravitational acceleration [m/s^2], defaults to Earth
        :returns: horizontal range [m]
        """
        # Trig functions in ``math`` expect radians, so convert first.
        angle_rad = math.radians(angle_deg)
        return speed ** 2 * math.sin(2 * angle_rad) / gravity

    def projectile_time_of_flight(self, *, speed, angle_deg, gravity=GRAVITY):
        """Time a projectile spends in the air over flat ground.

        t = 2 * v * sin(theta) / g.

        :param speed: launch speed [m/s]
        :param angle_deg: launch angle above horizontal [degrees]
        :param gravity: gravitational acceleration [m/s^2]
        :returns: time of flight [s]
        """
        angle_rad = math.radians(angle_deg)
        return 2 * speed * math.sin(angle_rad) / gravity

    def newtons_second_law(self, *, mass, acceleration):
        """Net force from Newton's second law: F = m*a.

        :param mass: mass [kg]
        :param acceleration: acceleration [m/s^2]
        :returns: force [N]
        """
        return mass * acceleration

    def kinetic_energy(self, *, mass, velocity):
        """Translational kinetic energy: KE = 1/2 * m * v^2.

        :param mass: mass [kg]
        :param velocity: speed [m/s]
        :returns: kinetic energy [J]
        """
        return 0.5 * mass * velocity ** 2

    def momentum(self, *, mass, velocity):
        """Linear momentum: p = m*v.

        :param mass: mass [kg]
        :param velocity: velocity [m/s]
        :returns: momentum [kg*m/s]
        """
        return mass * velocity

    def centripetal_acceleration(self, *, speed, radius):
        """Centripetal acceleration for circular motion: a = v^2 / r.

        :param speed: tangential speed [m/s]
        :param radius: radius of the circular path [m]
        :returns: centripetal acceleration [m/s^2]
        """
        return speed ** 2 / radius
