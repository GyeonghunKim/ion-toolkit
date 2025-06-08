from .units import Constants
import numpy as np


class Polarization:
    def __init__(self, k_hat: np.ndarray, epsilon_0: complex, epsilon_1: complex):
        """
        polarization_vector is a unit vector in the direction of the polarization of the laser.
        epsilon_0 is polarization component in same plane with B_field and k vector.
        epsilon_1 is polarization component in perpendicular to B_field and k vector plane. Since B field is set to z direction,
        this vector should on the xy plane
        """
        self.epsilon_0 = epsilon_0
        self.epsilon_1 = epsilon_1
       