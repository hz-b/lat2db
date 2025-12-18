from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly


class Bending(Element):
    """
    Todo:
        split up into different sub parts

        * angles as geometry

    """

    element_configuration: Optional[MagnetAssembly] = None
    # Todo: should it be treated as a corrector ?
    #       combined dipole / quads: are the quad strength ending up here
    gradient: Optional[float] = None
    number_of_integration_steps: Optional[int] = None
    bending_angle: Optional[float] = 0.0
    entranceangle: Optional[float] = 0.0
    exitangle: Optional[float] = 0
    fringeint1: Optional[float] = None
    fringeint2: Optional[float] = None
    fullgap: Optional[float] = None
