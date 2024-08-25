from typing import Optional
from .element import Element
from ..model.magnetic_element import MagnetAssembly


class Sextupole(Element):
    element_configuration: Optional[MagnetAssembly] = None
    # newly added
    K: Optional[float]
    N: Optional[float]