from dataclasses import dataclass

from .element import Element
from ..model.magnetic_element import MagneticElement
from typing import Optional

@dataclass
class Quadrupole(Element):
    element_properties: Optional[MagneticElement]=None
