from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly
from ..integrator_configuration.integration_parameters import IntegrationParameters


class Bending(Element):
    bending_angle: float
    integration_parameters: IntegrationParameters
    element_configuration: Optional[MagnetAssembly] = None
    entranceangle: Optional[float] = 0.0
    exitangle: Optional[float] = 0
    fringeint1: Optional[float] = None
    fringeint2: Optional[float] = None
    fullgap: Optional[float] = None
