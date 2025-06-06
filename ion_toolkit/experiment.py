from typing import List
import numpy as np
from .ion import Ion
from .laser import Laser
from .energy_level import EnergyLevel
class Experiment:
    def __init__(self, ion: Ion, B_field: np.ndarray, lasers: List[Laser]):
        self.ion = ion
        self.B_field = B_field
        self.lasers = lasers
        self.levels: List[EnergyLevel] = []
    
    def add_levels(self, levels: List[EnergyLevel]):
        self.levels.extend(levels)
        
    

