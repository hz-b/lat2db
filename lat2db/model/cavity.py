from dataclasses import dataclass
from typing import Optional
from lat2db.model.element import Element

@dataclass
class Cavity(Element):
    #: in Hertz
    frequency: float
    #: voltage of the cavity
    #: Todo:
    #:   review harmonic number
    #:     should only be voltage if magnets are stored in
    #:     in absolute field.
    #:     other wise it should be a transfer function
    #:
    voltage: float
    harmonic_number: Optional[int] = None
    #: in radians
    phase: Optional[float] = None
    energy: Optional[float] = None
    passmethod: Optional[str] = None
    timelag: Optional[float] = None

    