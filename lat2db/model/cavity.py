from typing import Optional

from pydantic.dataclasses import dataclass

from lat2db.model.element import Element


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


class Cavity(Element):
    #: review : that's a property of the ring
    cavity_configuration: Optional[RFFieldHarmonic] = None
    harmonic_number: Optional[int] = None
