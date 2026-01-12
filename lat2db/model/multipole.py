from .element import Element
from ..model.magnetic_element import MagnetAssembly


class Multipole(Element):
    element_configuration: MagnetAssembly
