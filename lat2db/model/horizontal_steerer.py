from dataclasses import dataclass

from lat2db.model.classical_magnet import ClassicalMagnet


@dataclass
class HorizontalSteerer(ClassicalMagnet):
    """A small dipole allowing to apply correction in the horizontal plane

    Todo:
        at many light sources this magnet is a correction winding of a main magnet

        Use host component?
    """
    name: str = ""
    index: int = 12
    length: float = 0.0
    type: str = "Horizontalsteerer"
    method: int = 0
    number_of_integration_steps: int = 0
    main_multipole_strength: int = 0
    main_multipole_index: int = 1
