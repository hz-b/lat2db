"""to tools.calculation.model

"""
from dataclasses import dataclass


@dataclass
class CalculationParameeters:
    #: name of the element the parameters should be used for
    element_name: str
    #: number of integration steps to apply to the element
    integration_steps : int