from typing import List, Dict, Tuple
import numpy as np
from sympy import S
from sympy.physics.wigner import wigner_3j
from .ion import Ion
from .laser import Laser
from .energy_level import (
    EnergyLevel,
    FineStructureZeemanLevel,
    HyperfineStructureZeemanLevel,
    FineStructure,
    HyperfineStructure,
)
from enum import Enum
from .units import Constants, Units
from .utils import number_to_sympy, sympy_to_number


class TransitionOrder(Enum):
    dipole = 0
    quadrupole = 1


class Transition:
    def __init__(
        self,
        level_1: EnergyLevel,
        level_2: EnergyLevel,
        laser: Laser,
        magnetic_field: float,
    ):
        self.laser = laser
        self.magnetic_field = magnetic_field
        if level_1.energy > level_2.energy:
            self.lower_level = level_2
            self.upper_level = level_1
        else:
            self.lower_level = level_1
            self.upper_level = level_2
        self.transition_order = self.get_transition_order()
        self.transition_linewidth = (
            self.upper_level.line_width
            + self.lower_level.line_width
            + self.laser.line_width
        )
        self.transition_branching_ratio = self.get_transition_branching_ratio()
        self.rabi_frequency = self.get_rabi_frequency()

    def get_transition_branching_ratio(self):
        return self.upper_level.branching_ratios[self.lower_level.name]

    def get_transition_energy(self):
        return self.level1.energy - self.level2.energy

    def get_transition_order(self):
        if abs(self.lower_level.L - self.upper_level.L) == 1:
            return TransitionOrder.dipole
        elif abs(self.lower_level.L - self.upper_level.L) == 2:
            return TransitionOrder.quadrupole
        else:
            raise ValueError("Transition order not supported")

    def __str__(self):
        return f"Transition(level_1={self.lower_level}, level_2={self.upper_level})"

    def __repr__(self):
        return self.__str__()

    def get_rabi_frequency(self):
        if self.transition_order == TransitionOrder.dipole:
            coefficient = (
                self.laser.get_electric_field_amplitude()
                / Constants.h_bar
                * np.sqrt(
                    3
                    * Constants.epsilon_0
                    * Constants.h_bar
                    * self.laser.wavelength**3
                    * self.transition_branching_ratio
                    * self.transition_linewidth
                    / (8 * np.pi**2)
                )
            ) * np.sqrt(2 * self.upper_level.J + 1)
            sign = (-1) ** (
                self.lower_level.J
                + self.upper_level.J
                + max(self.lower_level.J, self.upper_level.J)
                - self.upper_level.m
            )
            polarization_effect = 0j
            for q, eps_q in zip(
                range(-1, 2), self.laser.polarization.epsilon_in_spherical_tensor
            ):
                polarization_effect += eps_q * sympy_to_number(
                    wigner_3j(
                        number_to_sympy(self.upper_level.J),
                        number_to_sympy(1),
                        number_to_sympy(self.lower_level.J),
                        -number_to_sympy(self.upper_level.m),
                        number_to_sympy(q),
                        number_to_sympy(self.lower_level.m),
                    )
                )
            return sign * coefficient * polarization_effect
        elif self.transition_order == TransitionOrder.quadrupole:
            raise NotImplementedError("Quadrupole transitions not implemented")
        else:
            raise ValueError("Transition order not supported")


class Experiment:
    def __init__(self, ion: Ion, magnetic_field: float):
        self.ion = ion
        self.magnetic_field = magnetic_field
        self.levels: List[EnergyLevel] = []
        self.transitions: List[Transition] = []
        self.ion.apply_magnetic_field(magnetic_field)
        self.lasers: List[Laser] = []

    