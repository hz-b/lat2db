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
