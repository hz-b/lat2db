from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from lat2db.model.element import Element

@dataclass
class MagneticElement(Element):

    corrector: Optional[str] = None
    main_multipole_index: Optional[int] = None

    #: todo should be Optional[Sequence[float]] = None
    #: furthermore should be rather: PiggyBackMagnet (e.g. add on) or similar
    #: then stored as assembly consisting of
    #:  main and add ons
    kickangle: Optional[Sequence[float]] = None
    #: todo should be Optional[int] = None
    #: see if it should not be derived from polynoma and b
    maxorder: Optional[int] = None
    passmethod: Optional[str] = None
    #: todo, rename to normal_coefficients should be Optional[Sequence[float]] = None
    polynoma: Optional[Sequence[float]] = None
    #: todo rename to skew_coefficients, should be Optional[Sequence[float]] = None
    polynomb: Optional[Sequence[float]] = None


    @property
    def normal_coefficients(self):
        return self.polynomb

    @property
    def skew_coefficients(self):
        return self.polynoma

