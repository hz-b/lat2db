from dataclasses import dataclass

from .element import Element
from .magnetic_element import MagnetAssembly
from typing import Sequence
from typing import Optional

@dataclass
class Quadrupole(Element):
    element_configuration:Optional[MagnetAssembly]=None
    md: Optional[object] = None
    tags: Optional[Sequence[str]] = None