from dataclasses import dataclass

from lat2db.model.classical_magnet import ClassicalMagnet


@dataclass
class Sextupole(ClassicalMagnet):
    main_multipole_index: int = 3

