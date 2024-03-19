from pydantic.dataclasses import dataclass
from typing import Optional

from .element import Element
from ..model.magnetic_element import MagnetAssembly
from typing import Any
@dataclass
class Sextupole(Element):
    element_configuration: Optional[MagnetAssembly] = None