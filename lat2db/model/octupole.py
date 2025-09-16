from typing import Optional
from .element import Element
from ..model.magnetic_element import MagnetAssembly


class Octupole(Element):
    element_configuration: Optional[MagnetAssembly] = None