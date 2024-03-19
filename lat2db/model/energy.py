from pydantic.dataclasses import dataclass


@dataclass
class Energy:
    #: Todo:
    #:   remove engineering unit
    egu: str
    #: reconsider if that name should be here and not default to
    #: energy or particle_energy
    name: str
    #: specify the unit
    #: eV to be consitent with the beam energy
    #: deviates from SI, but that would be an acceptable compromise to
    #: the comumuity
    value: float