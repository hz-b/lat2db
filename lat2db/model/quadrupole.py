from dataclasses import dataclass

from .element import Element
from ..model.magnetic_element import MagneticElement
from typing import Optional
from .magnetic_element import Magnet
@dataclass
class Quadrupole(Magnet):
    pass
