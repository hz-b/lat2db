from typing import Optional, Sequence

import numpy as np
from pydantic import BaseModel

from .cavity import RFFieldHarmonic
from .magnetic_element import MagnetAssembly

nan = np.nan


class Sequencer(BaseModel):
    name: str
    index: int
    element_configuration: Optional[MagnetAssembly] = None
    cavity_configuration: Optional[RFFieldHarmonic] = None
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
