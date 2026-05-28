"""mechatronics.py - mechatronics and motion-system calculations.

Mechatronics blends mechanical, electrical, and control engineering. These
helpers size the components of a motion system: ball screws (turning rotation
into linear travel), servo motors (torque, speed, and reflected inertia), and
the gearboxes between them.
"""

import math


class Mechatronics:
    """Motion-system sizing calculations: ball screws, servos, drives."""

    def ballscrew_linear_speed(self, *, motor_rpm, lead):
        """Linear speed of a ball-screw nut from motor speed.

        v = (rpm / 60) * lead.  Each revolution advances the nut by one lead.

        :param motor_rpm: screw rotational speed [rev/min]
        :param lead: screw lead - linear travel per revolution [mm]
        :returns: linear speed [mm/s]
        """
        revolutions_per_second = motor_rpm / 60.0
        return revolutions_per_second * lead

    def ballscrew_torque(self, *, thrust_force, lead, efficiency=0.9):
        """Motor torque needed to drive a thrust load through a ball screw.

        T = F * lead / (2*pi*eta).  The 2*pi converts linear lead to angular
        motion; efficiency accounts for friction in the screw.

        :param thrust_force: required axial thrust force [N]
        :param lead: screw lead [m] (note: metres here, not mm)
        :param efficiency: screw efficiency 0..1, defaults to 0.9
        :returns: required torque [N*m]
        """
        return thrust_force * lead / (2 * math.pi * efficiency)

    def motor_power(self, *, torque, speed_rpm):
        """Mechanical power from torque and rotational speed.

        P = T * omega, where omega = rpm * 2*pi / 60.

        :param torque: shaft torque [N*m]
        :param speed_rpm: shaft speed [rev/min]
        :returns: mechanical power [W]
        """
        angular_velocity = speed_rpm * 2 * math.pi / 60.0
        return torque * angular_velocity

    def reflected_inertia(self, *, load_inertia, gear_ratio):
        """Load inertia as the motor "sees" it through a gearbox.

        J_reflected = J_load / ratio^2.  A reduction dramatically shrinks the
        inertia the motor must accelerate - key to matching motor to load.

        :param load_inertia: inertia at the load [kg*m^2]
        :param gear_ratio: gear reduction ratio [-]
        :returns: reflected inertia at the motor shaft [kg*m^2]
        """
        return load_inertia / gear_ratio ** 2

    def acceleration_torque(self, *, inertia, angular_acceleration):
        """Torque to angularly accelerate an inertia: T = J * alpha.

        The rotational analogue of F = m*a.

        :param inertia: rotational inertia J [kg*m^2]
        :param angular_acceleration: angular acceleration alpha [rad/s^2]
        :returns: torque [N*m]
        """
        return inertia * angular_acceleration
