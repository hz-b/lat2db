from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly

class Quadrupole(Element):
    element_configuration: Optional[MagnetAssembly] = None
    #newly added
    K: Optional[float]
    N: Optional[float]
