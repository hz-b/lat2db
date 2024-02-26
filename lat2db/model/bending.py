from dataclasses import dataclass, field

from typing import Optional
from .element import Element
from .magnetic_element import MagneticElement


@dataclass
class Bending(Element):
    element_properties: MagneticElement
    number_of_integration_steps: Optional[int] = None
    bending_angle: Optional[float] = 0.0
    entranceangle: Optional[float] = 0.0
    exitangle: Optional[float] = 0
    Energy: Optional[float] = None
    fringeint1: Optional[float] = None
    fullgap: Optional[float] = None