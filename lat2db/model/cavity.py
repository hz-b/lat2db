from dataclasses import dataclass
from typing import Optional, Dict,Any
from lat2db.model.element import Element
from typing import Optional

from bson import ObjectId
from bson import BSON
from bson.codec_options import TypeRegistry, CodecOptions
from bson.raw_bson import RawBSONDocument
from dataclasses import asdict


@dataclass
class RFFieldHarmonic:
    #: voltage of the cavity
    #: Todo:
    #:   review voltage
    #:     should only be voltage if magnets are stored in
    #:     in absolute field.
    #:     other wise it should be a transfer function
    #:
    voltage: float
    #: in Hertz
    frequency: float
    #: in radians
    phase: Optional[str] = None
    #: todo: energy is a property of the machine not of the element
    energy: Optional[float] = None
    #: passmethod: Optional[str] = None
    #: need to review: is it a time lag or a phase slip
    #: phase slip per turn ?
    timelag: Optional[float] = None
    




@dataclass
class Cavity(Element):
    #: review : that's a property of the ring
    element_configuration :Optional[RFFieldHarmonic]=None
    harmonic_number: Optional[int] = None
    

