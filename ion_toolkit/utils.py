from sympy import S
import numpy as np
from .units import Constants
from .energy_level import EnergyLevel


def L_str_to_int(L_str: str) -> int:
    if L_str == "S":
        return 0
    elif L_str == "P":
        return 1
    elif L_str == "D":
        return 2
    eli