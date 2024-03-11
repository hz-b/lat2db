from dataclasses import dataclass

import numpy as np

from .cavity import RFFieldHarmonic
from .magnetic_element import MagneticElement, MagnetAssembly

nan = np.nan

from typing import Optional, Sequence


@dataclass
class Sequencer:
    name: str
    index: int
    element_configuration: Optional[MagnetAssembly] = None
    cavity_configuration :Optional[RFFieldHarmonic]=None
    strength: Optional[float] = None
    length: Optional[float] = None
    method: Optional[int] = None
    number_of_integration_steps: Optional[int] = None
    type: Optional[str] = None
    bending_angle: Optional[float] = None
    entry_angle: Optional[float] = None
    exit_angle: Optional[float] = None
    frequency: Optional[float] = None
    voltage: Optional[float] = None
    phase: Optional[float] = None
    harmonic_number: Optional[int] = None
    tags: Optional[Sequence[str]] = None

    def set_properties(self, item):
        """

        :param sequence:
        :return:
        """

        for key, val in item.items():
            setattr(self, key, val)

        pass
