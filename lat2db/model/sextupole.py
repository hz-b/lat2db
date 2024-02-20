from dataclasses import dataclass

from lat2db.model.classical_magnet import ClassicalMagnet


@dataclass
class Sextupole(ClassicalMagnet):
    main_multipole_index: int = 3
    name: str = ""
    index: int = 0
    length: float = 0.0
    type: str = "Sextupole"
    method: int = 0
    number_of_integration_steps: int = 0
    main_multipole_strength: float = 0.0

