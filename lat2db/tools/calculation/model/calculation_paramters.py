"""to tools.calculation.model

"""
import enum
from pydantic.dataclasses import dataclass
from typing import Sequence


@dataclass
class ElementCalculationParameters:
    #: name of the element the parameters should be used for
    element_name: str
    #: number of integration steps to apply to the element
    integration_steps: int


class StateSpaceCoordinates(enum.Intenum):
    four = 4
    six = 6


@dataclass
class CalculationParametersRepository:
    per_element: Sequence[ElementCalculationParameters]
    state_space_coordinates: StateSpaceCoordinates
    with_radiation: bool
