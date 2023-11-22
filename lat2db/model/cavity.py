from dataclasses import dataclass

from lat2db.model.element import Element


@dataclass
class Cavity(Element):
    #: in Hertz
    frequency: float
    harmonic_number: int
    #: voltage of the cavity
    #: Todo:
    #:   review harmonic number
    #:     should only be voltage if magnets are stored in
    #:     in absolute field.
    #:     other wise it should be a transfer function
    #:
    voltage: float
    #: in radians
    phase: float = 0.0

