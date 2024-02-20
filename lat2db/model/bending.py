from dataclasses import dataclass, field

from lat2db.model.classical_magnet import ClassicalMagnet


@dataclass
class Bending(ClassicalMagnet):
    name: str = ""
    index: int = 0
    length: float = 0.0
    type: str = "Bending"
    method: int = 0
    number_of_integration_steps: int = 0
    main_multipole_strength: int = 0
    main_multipole_index: int = 0
    bending_angle: float = 0.0
    entry_angle: float = 0.0
    exit_angle: int = 0
