from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly


class Bending(Element):
    element_configuration: Optional[MagnetAssembly] = None
    number_of_integration_steps: Optional[int] = None
    bending_angle: Optional[float] = 0.0
    entranceangle: Optional[float] = 0.0
    exitangle: Optional[float] = 0
    fringeint1: Optional[float] = None
    fringeint2: Optional[float] = None
    fullgap: Optional[float] = None

    #newly added

    L: Optional[float]
    T: Optional[float]
    T1: Optional[float]
    T2: Optional[float]
    K: Optional[float]
    N: Optional[float]

