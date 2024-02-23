from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from lat2db.model.element import Element

@dataclass
class MultipoleCoefficients:
    normal_coefficients: Optional[Sequence[float]] = None
    skew_coefficients: Optional[Sequence[float]] = None
    @property
    def maximum_order(self):
        return max(len(self.normal_coefficients), len(self.skew_coefficients))


class AddonCorrector:
    """
    or better:
         NebenMagnet Wie Nebenuhr?
         Piggypackmagnet I think is used at Brookhaven nationl lab

    Todo:
        should it have a separate id? e.g. to look up conversion factors
    """
    corrector: Optional[str] = None
    #: todo: review if one should not store MagneticElement
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
    """does not need to be a single magnet, but can have extra magnets

    """
    magnetic_element: MagneticElement
    #: physisists often think of these corrector magnets
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
    # todo: or distinquish at this place
    #: element_configuration: Union[MagnetAssembly, MagneticElement]
    element_configuration: MagnetAssembly