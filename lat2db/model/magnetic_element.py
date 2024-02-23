from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from lat2db.model.element import Element

@dataclass
class MultipoleCoefficients:
    normal_coefficients: Optional[Sequence[float]] = None
    skew_coefficients: Optional[Sequence[float]] = None
   @property
    def maxorder(self):
        return max(len(self.normal_coefficients), len(self.skew_coefficients))


class AddonCorrector:
    """
    or better:
         NebenMagnet Wie Nebenuhr?
         Piggypackmagnet I think is used at Brookhaben nation lab

    Todo:
        should it have a separate id? e.g. to look up conversion factors
    """
    corrector: Optional[str] = None
    #: todo should be Optional[Sequence[float]] = None
    #: furthermore should be rather: PiggyBackMagnet (e.g. add on) or similar
    #: then stored as assembly consisting of
    #:  main and add ons
    kickangle: Optional[Sequence[float]] = None


@dataclass
class MagneticElement:
    """Info what field a particular magnet component provides
    """
    #: todoo or coefficients
    coeffs : MultipoleCoefficients
    #: todo: should that not be in describing the calculation
    #:       should it be here anyway? I think it is pyat specific
    passmethod: Optional[str] = None
    #: todo, rename to normal_coefficients should be Optional[Sequence[float]] = None
    main_multipole_index: Optional[int] = None


class MagnetAssembly:
    magnetic_element: MagneticElement
    corectors : Sequence[AddonCorrector]
class Magnet(Element):
    """
    Todo:
        * Magnet assembly
        * "Muttermagnet"
        * "Hauptmagnet"
        * "InstallableManet"
        * "selbständig nutzbares Gerät"
    """
    element_configuration =