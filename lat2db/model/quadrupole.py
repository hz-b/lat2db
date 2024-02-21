from dataclasses import dataclass

from lat2db.model.classical_magnet import ClassicalMagnet

from typing import Optional

@dataclass
class Quadrupole:
    name: Optional[str] = None
    index: Optional[int] = None
    length: Optional[float] = None
    type: Optional[str] = None
    method: Optional[int] = None
    number_of_integration_steps: Optional[int] = None
    main_multipole_strength: Optional[float] = None
    main_multipole_index: Optional[int] = None

    energy: Optional[float] = None
    k: Optional[float] = None
    maxorder: Optional[str] = None
    passmethod: Optional[str] = None
    polynoma: Optional[str] = None
    polynomb: Optional[str] = None