from enum import Enum
from sympy import S
from sympy.core.numbers import Rational

class EnergyLevel:
    def __init__(self, n: int, L: int, J: Rational):
        self.n = n
        self.L = L
        self.J = J

class FineStructureZeemanLevel(EnergyLevel):
    def __init__(self, n: int, L: int, J: Rational, m_J: float, lande_g_factor: float):
        super().__init__(n, L, J)
        self.m_J = m_J
        self.lande_g_factor = lande_g_factor
    
    def zeeman_splitting(self, B_field: float):
        return self.lande_g_factor * self.m_J * B_field
class HyperfineStructureZeemanLevel(EnergyLevel):
    def __init__(self, n: int, L: int, J: Rational, F: Rational, m_F: float, lande_g_factor: float):
        super().__init__(n, L, J)
        self.F = F
        self.m_F = m_F
        self.lande_g_factor = lande_g_factor

class FineStructure(EnergyLevel):
    def __init__(self, n: int, L: int, J: Rational, lande_g_factor: float):
        super().__init__(n, L, J)
        self.lande_g_factor = lande_g_factor
        self.n_zeeman_levels = 2*J + 1
        self.zeeman_levels = [FineStructureZeemanLevel(self.n, self.L, self.J, m_J) for m_J in range(-J, J+1)]

class HyperfineStructure(EnergyLevel):
    def __init__(self, n: int, L: int, J: Rational, F: Rational, lande_g_factor: float):
        super().__init__(n, L, J)
        self.F = F
        self.lande_g_factor = lande_g_factor
        self.n_zeeman_levels = 2*F + 1
        self.zeeman_levels = [HyperfineStructureZeemanLevel(self.n, self.L, self.J, self.F, m_F) for m_F in range(-F, F+1)]

        

if __name__ == "__main__":
    fine_structure = FineStructure(n=6, L=0, J=1/2)
    print(fine_structure.lande_g_factor)

