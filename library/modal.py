"""modal.py - classical vibration and modal analysis.

Vibration analysis predicts how structures and machines oscillate. These
helpers cover the single-degree-of-freedom (SDOF) spring-mass-damper - the
building block of all vibration theory - plus a multi-DOF eigenvalue solver
that finds natural frequencies and mode shapes using numpy's linear algebra.
"""

import math

import numpy as np


class Modal:
    """Vibration and modal-analysis calculations."""

    def natural_frequency(self, *, stiffness, mass):
        """Undamped natural frequency of an SDOF system.

        Returns both the angular frequency omega_n = sqrt(k/m) [rad/s] and the
        ordinary frequency f_n = omega_n / (2*pi) [Hz], because engineers quote
        both.

        :param stiffness: spring stiffness k [N/m]
        :param mass: mass m [kg]
        :returns: tuple (omega_n [rad/s], f_n [Hz])
        """
        omega_n = math.sqrt(stiffness / mass)
        f_n = omega_n / (2 * math.pi)
        return omega_n, f_n

    def damping_ratio(self, *, damping, mass, stiffness):
        """Dimensionless damping ratio zeta = c / (2*sqrt(k*m)).

        zeta < 1 underdamped (oscillates), = 1 critically damped, > 1 overdamped.

        :param damping: viscous damping coefficient c [N*s/m]
        :param mass: mass m [kg]
        :param stiffness: stiffness k [N/m]
        :returns: damping ratio zeta [-]
        """
        critical_damping = 2 * math.sqrt(stiffness * mass)
        return damping / critical_damping

    def damped_natural_frequency(self, *, stiffness, mass, damping):
        """Damped natural frequency omega_d = omega_n * sqrt(1 - zeta^2).

        This is the frequency a real (lightly damped) system actually rings at.

        :param stiffness: stiffness k [N/m]
        :param mass: mass m [kg]
        :param damping: damping coefficient c [N*s/m]
        :returns: damped angular frequency [rad/s]
        """
        omega_n, _ = self.natural_frequency(stiffness=stiffness, mass=mass)
        zeta = self.damping_ratio(damping=damping, mass=mass, stiffness=stiffness)
        return omega_n * math.sqrt(1 - zeta ** 2)

    def mode_shapes(self, *, mass_matrix, stiffness_matrix):
        """Natural frequencies and mode shapes of a multi-DOF system.

        Solves the generalized eigenvalue problem  K*phi = omega^2 * M*phi.
        Each eigenvalue is omega^2; each eigenvector is a mode shape describing
        the relative motion of every degree of freedom at that frequency.

        :param mass_matrix: mass matrix M, shape (n, n) [kg]
        :param stiffness_matrix: stiffness matrix K, shape (n, n) [N/m]
        :returns: tuple (natural_frequencies [Hz] sorted ascending,
                  mode_shapes as columns of an array)
        """
        # Convert inputs to numpy arrays so this works with plain Python lists.
        M = np.asarray(mass_matrix, dtype=float)
        K = np.asarray(stiffness_matrix, dtype=float)

        # M^-1 * K turns the generalized problem into a standard eigenproblem.
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.solve(M, K))

        # Eigenvalues are omega^2; take the root and convert rad/s -> Hz.
        omega = np.sqrt(np.abs(eigenvalues))
        frequencies_hz = omega / (2 * math.pi)

        # Sort modes from lowest to highest frequency for a tidy result.
        order = np.argsort(frequencies_hz)
        return frequencies_hz[order], eigenvectors[:, order]
