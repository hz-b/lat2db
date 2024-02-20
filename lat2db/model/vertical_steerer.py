from dataclasses import dataclass

__all__ = ["VerticalSteerer"]

from .classical_magnet import ClassicalMagnet
from .horizontal_steerer import HorizontalSteerer

@dataclass
class VerticalSteerer(ClassicalMagnet):
    """a vertical corrector

    Todo:
        see :class:`HorizontalSteerer`
    """
    main_multipole_index: int = 1
    name: str = ""
    index: int = 0
    length: float = 0.0
    type: str = "Verticalsteerer"
    method: int = 0
    number_of_integration_steps: int = 0
    main_multipole_strength: int = 0