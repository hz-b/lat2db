from dataclasses import dataclass

from .element import Element
from ..model.magnetic_element import MagnetAssembly


@dataclass
class Sextupole(Element):
    element_configuration: MagnetAssembly
