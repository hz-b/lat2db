from dataclasses import dataclass
from typing import Optional

from .element import Element
from ..model.magnetic_element import MagneticElement
from typing import Optional

@dataclass
class Sextupole(Element):
    # main_multipole_strength: Optional[float] = None

    element_properties: Optional[MagneticElement]=None
    method: Optional[int] = None
    number_of_integration_steps: Optional[int] = None

    @property
    def main_multipole_strength(self):
        return self.normal_coefficients[2]
