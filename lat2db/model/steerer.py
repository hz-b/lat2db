from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly


class Steerer(Element):
    element_configuration: Optional[MagnetAssembly] = None
