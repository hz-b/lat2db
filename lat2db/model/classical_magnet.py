from dataclasses import dataclass

from lat2db.model.element import Element

# @dataclass
# class ComplexNumber:
#     re : float
#     im : float

@dataclass
class ClassicalMagnet(Element):
    """

    Todo:
        review to make it `design configuration` or `typical use case`
        as a configuration of mpole
    """
    method: int
    number_of_integration_steps: int
    # interpolation: Union[Multipoles | FieldInterpolation] I don't have a good reason to add this field

    #: strength of the dominant multipole
    #:
    #: Todo
    #:    change it to a complex number or complex data class
    #
    #     unit
    #:        :math:`T m^{n-1}`
    #:    or
    #:        :math:`T m^{n-1} / T m`
    #:
    #: one storing the field while the other is storing the field
    #: scaled by machine's energy
    main_multipole_strength: float
    main_multipole_index: int