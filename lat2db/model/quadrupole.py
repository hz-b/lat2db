from dataclasses import dataclass

from typing import Optional

from ..model.magnetic_element import MagneticElement


@dataclass
class Quadrupole(Element):
    element_properties : MagneticElementProperties