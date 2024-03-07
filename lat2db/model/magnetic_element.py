from dataclasses import dataclass
from typing import Optional, Sequence

from lat2db.model.element import Element


@dataclass
class MultipoleCoefficients:
    normal_coefficients: Optional[Sequence[float]] = None
    skew_coefficients: Optional[Sequence[float]] = None

    @property
    def maximum_order(self):
        return max(len(self.normal_coefficients), len(self.skew_coefficients))


@dataclass
class MagneticElement:
    """Info what field a particular magnet component provides
    """
    #: todoo or coefficients
    coeffs: MultipoleCoefficients
    main_multipole_index: Optional[int] = None
    main_multipole_strength: Optional[float] = None
    
    """   def to_dict(self):
        return {
            "coeffs": self.coeffs.__dict__,
            #"passmethod": self.passmethod,
            "main_multipole_index": self.main_multipole_index,
            "main_multipole_strength":self.main_multipole_strength
        } """


@dataclass
class AddonCorrector(Element):
    """
    or better:
         NebenMagnet Wie Nebenuhr?
         Piggypackmagnet I think is used at Brookhaven nationl lab


    Todo:
        * length: set it to None if it is identical with the
           Main magnet
    """
    #: corrector: add as metadata?
    # corrector: Optional[str] = None
    #: todo: review if one should not store MagneticElement
    # kickangle: Optional[Tuple[float]] = None
    """
    Kickangle: single angle
    Coefficients Angles with errors
    """
    element_properties: Optional[MagneticElement] = None


@dataclass
class KickAngles:
    """statisfy PyAT design flaws

    see if that could be part of the Element
    todo: revisit if implemetation as Corrector would
        be more consitent on the long run
    """
    #: maps to MagneticElement.skew_coefficient[0]
    x: Optional[float] = 0
    #: maps to MagneticElement.normal_coefficient[0]
    y: Optional[float] = 0


@dataclass
class MagnetAssembly:
    """does not need to be a single magnet, but can have extra magnets

    """
    magnetic_element: MagneticElement
    #: physisists often think of these corrector magnets
    kickangle: Optional[KickAngles]=None
    correctors: Optional[Sequence[AddonCorrector]]=None

    
