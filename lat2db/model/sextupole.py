from dataclasses import dataclass

from .element import Element
from ..model.magnetic_element import MagnetAssembly

from typing import Sequence
from typing import Optional

@dataclass
class Sextupole(Element):
    element_configuration: Optional[ MagnetAssembly]=None
    md: Optional[object] = None
    tags: Optional[Sequence[str]] = None