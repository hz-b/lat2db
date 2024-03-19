from pydantic.dataclasses import dataclass
from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly


@dataclass
class Quadrupole(Element):
    element_configuration: Optional[MagnetAssembly] = None
