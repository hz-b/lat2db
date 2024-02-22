from dataclasses import dataclass
from typing import Optional
from ..model.magnetic_element import MagneticElement

@dataclass
class Sextupole(MagneticElement):
    method: Optional[int] = None
    number_of_integration_steps: Optional[int] = None
    # main_multipole_strength: Optional[float] = None


    @property
    def main_multipole_strength(self):
        return self.NormalCoefficients[2]
