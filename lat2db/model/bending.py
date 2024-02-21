from dataclasses import dataclass, field

from lat2db.model.classical_magnet import ClassicalMagnet
from typing import Optional


@dataclass
class Bending(ClassicalMagnet):
    bending_angle: Optional[float] = 0.0
    entranceangle: Optional[float] = 0.0
    exitangle: Optional[float] = 0
    Energy: Optional[float] = None
    fringeint1: Optional[float] = None
    fullgap: Optional[float] = None
    #k: Optional[float] = None
    maxorder: Optional[float] = None
    numintsteps: Optional[float] = None
    passmethod: Optional[str] = None
    polynoma: Optional[str] = None
    polynomb: Optional[str] = None