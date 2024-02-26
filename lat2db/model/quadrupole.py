from dataclasses import dataclass

from .element import Element
from ..model.magnetic_element import MagneticElement


@dataclass
class Quadrupole(Element):
    element_properties: MagneticElement
