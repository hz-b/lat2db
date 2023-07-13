from dataclasses import dataclass

from src.model.element import Element


@dataclass
class Marker(Element):
   """A virtual beam position monitor

   Used to get data at any point within the machine
   """
