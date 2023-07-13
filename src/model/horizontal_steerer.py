from dataclasses import dataclass

from src.model.classical_magnet import ClassicalMagnet


@dataclass
class HorizontalSteerer(ClassicalMagnet):
    """A small dipole allowing to apply correction in the horizontal plane

    Todo:
        at many light sources this magnet is a correction winding of a main magnet

        Use host component?
    """
    main_multipole_index: int = 1
