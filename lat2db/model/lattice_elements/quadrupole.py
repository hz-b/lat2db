from typing import Optional

from .element import Element
from .magnetic_element import MagnetAssembly
from ..integrator_configuration.integration_parameters import IntegrationParameters


class Quadrupole(Element):
    main_multipole_strength: float
    integration_parameters: IntegrationParameters
    element_configuration: Optional[MagnetAssembly] = None
