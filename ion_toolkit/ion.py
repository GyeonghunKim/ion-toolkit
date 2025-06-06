import os
import json
from typing import List
from .energy_level import EnergyLevel, FineStructure, HyperfineStructure
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
                self.energy_levels.append(FineStructure(level["n"], level["L"], level["J"]))
            elif level["order"] == "HyperfineStructure":
                self.energy_levels.append(HyperfineStructure(level["n"], level["L"], level["J"], level["F"]))
                

if __name__ == "__main__":
    ion = Ion("Ba", 138)
    print(ion.library)
