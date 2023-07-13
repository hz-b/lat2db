from dataclasses import dataclass

from src.model.element import Element

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
    #: Todo
    #:    change it to a complex number or complex data class
    main_multipole_strength: float
    main_multipole_index: int