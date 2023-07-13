from dataclasses import dataclass

from src.model.classical_magnet import ClassicalMagnet


@dataclass
class Sextupole(ClassicalMagnet):
    main_multipole_index: int = 3

