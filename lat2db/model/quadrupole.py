from dataclasses import dataclass

from .element import Element
from .magnetic_element import MagnetAssembly


@dataclass
class Quadrupole(Element):
    element_configuration: MagnetAssembly
