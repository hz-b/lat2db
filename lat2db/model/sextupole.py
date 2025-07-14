from typing import Optional
from .element import Element
from ..model.magnetic_element import MagnetAssembly


class Sextupole(Element):
    element_configuration: Optional[MagnetAssembly] = None