from dataclasses import dataclass

from typing import Optional

@dataclass
class Sextupole:
    name: Optional[str] = None
    index: Optional[int] = None
    method: Optional[int] = None
    number_of_integration_steps: Optional[int] = None
    main_multipole_strength: Optional[float] = None
    main_multipole_index: Optional[int] = None

