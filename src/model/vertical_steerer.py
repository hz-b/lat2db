from dataclasses import dataclass

from src.model.classical_magnet import ClassicalMagnet


@dataclass
class VerticalSteerer(ClassicalMagnet):
    """a vertical corrector

    See todo of horizontal corrector for todo
    """
    main_multipole_index: int = 1
