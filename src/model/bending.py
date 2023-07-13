from dataclasses import dataclass, field

from src.model.classical_magnet import ClassicalMagnet


@dataclass
class Bending(ClassicalMagnet):
    #: typical lattice file name this value "T"
    bending_angle: float = 0.0
    #: typical lattice file name this value "T1"
    entry_angle: float = 0.0
    #: typical lattice file name this value "T2"
    exit_angle: float = 0.0
    main_multipole_index: int = 1
