from .units import Constants

class Polarization:
    def __init__(self, sigma_plus: np.ndarray, sigma_minus: np.ndarray, pi: np.ndarray):
        self.sigma_plus = sigma_plus
        self.sigma_minus = sigma_minus
        self.pi = pi
        
class Laser:
    def __init__(self, wavelength: float, intensity: float, line_width: float, polarization: Polarization):
        self.wavelength = wavelength
        self.intensity = intensity
        self.line_width = line_width
        self.polarization = polarization
        
    def get_frequency(self):
        return Constants.c / self.wavelength
    



