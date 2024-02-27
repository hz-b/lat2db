from dataclasses import dataclass, field

from typing import Optional
from .element import Element
from .magnetic_element import MagneticElement
from typing import Optional

@dataclass
class BendingGeometry:
    """Geometyr of the bending magnet

    Todo:
        Compare entrance angle exit angle to the names chosen in mad-ng
        entrance angle is beam use specific
        please not in "design" or generic models these magnets could be "mirrored", then
        exit becomes entrance and vice versa

        Alternative suggestions

        * down_stream
        * up_stream

        Side `A`: negative coordinate side
        Side `B`: positive coordinate side

        This idea above follows the naming convention of magnet connections at LHC.
        For humans its typically eassier to say:

           I put "side `A`" to the downstream side
           
    """
    bending_angle: Optional[float] = 0.0
    entrance_angle: Optional[float] = 0.0
    exit_angle: Optional[float] = 0
    #: full magnet height
    gap: Optional[float] = None

@dataclass
class Bending(Element):
    element_properties: Optional[MagneticElement]=None
    geometry : BendingGeometry
    #: property of the machine or lattice or a user defined parameter
    Energy: Optional[float] = None
    #: need to understand that value
    #: should be something like end model
    #: could be that it is very calculation engine specific
    fringeint1: Optional[float] = None
