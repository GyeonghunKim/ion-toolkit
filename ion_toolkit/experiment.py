from typing import List, Dict, Tuple
import numpy as np
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
        self.transition_linewidth = self.upper_level.line_width

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
        # coefficient = (
        #     self.get_transition_energy() / Constants.hbar * np.sqrt(3 * Constants.epsilon_0 * Constants.hbar * self.laser.wavelength**3 * self.)
        # )
        # return coefficient * self.laser.get_electric_field_amplitude()

        pass


class Experiment:
    def __init__(self, ion: Ion, magnetic_field: float):
        self.ion = ion
        self.magnetic_field = magnetic_field
        self.levels: List[EnergyLevel] = []
        self.transitions: List[Transition] = []
        self.ion.apply_magnetic_field(magnetic_field)
        self.lasers: List[Laser] = []

    def add_levels(self, levels: List[EnergyLevel]):
        self.levels.extend(levels)

    def add_laser(
        self, laser: Laser, transition_pair: List[Tuple[EnergyLevel, EnergyLevel]]
    ):
        self.lasers.append(laser)
        for level_1, level_2 in transition_pair:
            if isinstance(level_1, FineStructure) or isinstance(
                level_1, HyperfineStructure
            ):
                if isinstance(level_2, FineStructure) or isinstance(
                    level_2, HyperfineStructure
                ):
                    # level_1 is a FineStructure or HyperfineStructure and level_2 is a FineStructure or HyperfineStructure
                    for level_1_zeeman_level in level_1.zeeman_levels:
                        for level_2_zeeman_level in level_2.zeeman_levels:
                            self.transitions.append(
                                [
                                    Transition(
                                        level_1_zeeman_level,
                                        level_2_zeeman_level,
                                        laser,
                                        self.magnetic_field,
                                    )
                                ]
                            )
                else:
                    for zeeman_level in level_1.zeeman_levels:
                        self.transitions.append(
                            [
                                Transition(
                                    zeeman_level, level_2, laser, self.magnetic_field
                                )
                            ]
                        )
            else:
                if isinstance(level_2, FineStructure) or isinstance(
                    level_2, HyperfineStructure
                ):
                    # level_1 is a ZeemanLevel and level_2 is a FineStructure or HyperfineStructure
                    for zeeman_level in level_2.zeeman_levels:
                        self.transitions.append(
                            [
                                Transition(
                                    level_1, zeeman_level, laser, self.magnetic_field
                                )
                            ]
                        )
                else:  # level_1 is a ZeemanLevel and level_2 is ZeemanLevel
                    self.transitions.append(
                        [Transition(level_1, level_2, laser, self.magnetic_field)]
                    )
