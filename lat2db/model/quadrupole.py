from dataclasses import dataclass

from .element import Element
from .magnetic_element import MagnetAssembly
from typing import Sequence
from typing import Optional

@dataclass
class Quadrupole(Element):
    element_configuration:Optional[MagnetAssembly]=None
    
    def __init__(self, name, index, length, type, tags, element_configuration):
        self.name = name
        self.index = index
        self.length = length
        self.type = type
        self.tags = tags
        self.element_configuration = element_configuration

    def to_dict(self):
        return {
            "name": self.name,
            "index": self.index,
            "length": self.length,
            "type": self.type,
            "tags": self.tags,
            "element_configuration": self.element_configuration.to_dict()
        }