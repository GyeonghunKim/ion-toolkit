import os
import json
from typing import List
import numpy as np
from .energy_level import EnergyLevel, FineStructure, HyperfineStructure
from .units import Units, Constants
from .utils import L_str_to_int
class Ion:
    def __init__(self, species: str, mass_number: int):
        self.species = species
        self.mass_number = mass_number
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.library_name = os.path.join(current_dir, f"../ion_library/{self.species}_II/{self.species}-{self.mass_number}.json")
        self.library = json.load(open(self.library_name))
        self.energy_levels: List[EnergyLevel] = []

        self._load_energy_levels()
        
    def _load_energy_levels(self):
        for level in self.library["energy_levels"]:
            if level["order"] == "FineStructure":
                self.energy_levels.append(FineStructure(level["energy_Hz"] * Constants.h, level["n"], self.library["I"], L_str_to_int(level["L"]), level["J"], 2 * np.pi * level["line_width_2_pi_Hz"]))
            elif level["order"] == "HyperfineStructure":
                self.energy_levels.append(HyperfineStructure(level["energy_Hz"] * Constants.h, level["n"], self.library["I"], L_str_to_int(level["L"]), level["J"], level["F"], 2 * np.pi * level["line_width_2_pi_Hz"]))
                

if __name__ == "__main__":
    ion = Ion("Ba", 138)
    for energy_level in ion.energy_levels:
        print(energy_level)
        for zeeman_level in energy_level.zeeman_levels:
            print(zeeman_level)
    
