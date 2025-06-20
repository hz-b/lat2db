from typing import Optional, Sequence, Hashable

import numpy as np
from pydantic import BaseModel

from .lattice_elements.cavity import RFFieldHarmonic
from .lattice_elements.magnetic_element import MagnetAssembly


class LatticeElement(BaseModel):
    id: Hashable
    length: float
    #: probably redundant information? should that not be given by
    # the basemodel
    type: str


class CavityParameters(BaseModel):
    frequency: float
    voltage: float
    phase: float
    harmonic_number: int


class BendingMagnet(BaseModel):
    bending_angle: Optional[float] = None
    entry_angle: Optional[float] = None
    exit_angle: Optional[float] = None


class Sequencer(BaseModel):
    """Todo: make me obsolete
    """
    name: str
    index: int
    element_configuration: Optional[MagnetAssembly] = None
    cavity_configuration: Optional[RFFieldHarmonic] = None
    strength: Optional[float] = None
    length: Optional[float] = None
    method: Optional[int] = None
    type: Optional[str] = None
    tags: Optional[Sequence[str]] = None
    passmethod: Optional[str] = None
    main_multipole_strength: Optional[float] = None
    def set_properties(self, item):
        """

        :param sequence:
        :return:
        """

        for key, val in item.items():
            setattr(self, key, val)

        pass
