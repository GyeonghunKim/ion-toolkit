from enum import Enum
from sympy import S
from sympy.core.numbers import Rational
from typing import Callable
import numpy as np
from .units import Units, Constants

class EnergyLevel:
    def __init__(self, energy: float, n: int, I: Rational, L: int, J: Rational, line_width: float):
        self.energy = energy
        self.n = n
        self.I = I
        self.L = L
        self.J = J
        self.line_width = line_width

class FineStructureZeemanLevel(EnergyLevel):
    def __init__(self, energy: float, n: int, I: Rational, L: int, J: Rational, m_J: float, line_width: float):
        super().__init__(energy, n, I, L, J, line_width)
        self.m_J = m_J
        self.lande_g_factor = 1 + (J*(J+1) - L*(L+1) + 0.5*(0.5+1))/(2*J*(J+1))
        self.zeeman_splitting_func: Callable[[float], float] = lambda B_field: self.lande_g_factor * self.m_J * Units.mu_B * B_field
    
    def __str__(self):
        return f"FineStructureZeemanLevel(energy={self.energy/Constants.h/Units.THz} THz, n={self.n}, I={self.I}, L={self.L}, J={self.J}, m_J={self.m_J})"
    
class HyperfineStructureZeemanLevel(EnergyLevel):
    def __init__(self, energy: float, n: int, I: Rational, L: int, J: Rational, F: Rational, m_F: float, line_width: float):
        super().__init__(energy, n, I, L, J, line_width)
        self.F = F
        self.m_F = m_F
        self.lande_g_factor = 1 + (F*(F+1) - J*(J+1) + I*(I+1))/(2*F*(F+1))
        self.zeeman_splitting_func: Callable[[float], float] = lambda B_field: self.lande_g_factor * self.m_F * Units.mu_B * B_field

    def __str__(self):
        return f"HyperfineStructureZeemanLevel(energy={self.energy/Constants.h/Units.THz} THz, n={self.n}, I={self.I}, L={self.L}, J={self.J}, F={self.F}, m_F={self.m_F})"   

class FineStructure(EnergyLevel):
    def __init__(self, energy: float, n: int, I: Rational, L: int, J: Rational, line_width: float):
        super().__init__(energy, n, I, L, J, line_width)
        self.n_zeeman_levels = 2*J + 1
        self.lande_g_factor = 1 + (J*(J+1) - L*(L+1) + 0.5*(0.5+1))/(2*J*(J+1)) 
        self.zeeman_levels = [FineStructureZeemanLevel(self.energy, self.n, self.I, self.L, self.J, m_J, self.line_width) for m_J in np.arange(-J, J+1)]

    def __str__(self):
        return f"FineStructure(energy={self.energy/Constants.h/Units.THz} THz, n={self.n}, I={self.I}, L={self.L}, J={self.J})"

class HyperfineStructure(EnergyLevel):
    def __init__(self, energy: float, n: int, I: Rational, L: int, J: Rational, F: Rational, line_width: float):
        super().__init__(energy, n, I, L, J, line_width)
        self.F = F
        self.n_zeeman_levels = 2*F + 1
        self.lande_g_factor = 1 + (F*(F+1) - J*(J+1) + I*(I+1))/(2*F*(F+1)) 
        self.zeeman_levels = [HyperfineStructureZeemanLevel(self.energy, self.n, self.I, self.L, self.J, self.F, m_F, self.line_width) for m_F in np.arange(-F, F+1)]

    def __str__(self):
        return f"HyperfineStructure(energy={self.energy/Constants.h/Units.THz} THz, n={self.n}, I={self.I}, L={self.L}, J={self.J}, F={self.F})"
