from dataclasses import dataclass
import numpy as np

nan = np.nan

from typing import Optional

@dataclass
class Sequencer:
    name: str
    index: int
    strength: Optional[float] = None
    length: Optional[float] = None
    method: Optional[int] = None
    number_of_integration_steps: Optional[int] = None
    main_multipole_strength: Optional[float] = None
    main_multipole_index: Optional[int] = None
    type: Optional[str] = None
    bending_angle: Optional[float] = None
    entry_angle: Optional[float] = None
    exit_angle: Optional[float] = None
    frequency: Optional[float] = None
    voltage: Optional[float] = None
    phase: Optional[float] = None
    harmonic_number: Optional[int] = None

    def set_properties(self, item):
        """

        :param sequence:
        :return:

        Todo:
            add check that default arguments are correctly set?
            Consistency checks?
        """
        # d = sequence.asdict()
        for key, val in item.items():
            setattr(self, key, val)

        pass
        # if (sequence.name):
        #     self.name = sequence.name
        # if (sequence.type):
        #     self.type = sequence.type
        # if (sequence.K):
        #     self.strength = sequence.K
        # if (sequence.N):
        #     self.strength = sequence.K
        # if (sequence.T):
        #     self.bending_angle = sequence.T
        # if (sequence.T1):
        #     self.entry_angle = sequence.T1
        # if (sequence.T2):
        #     self.exit_angle = sequence.T2
        # if (sequence.Voltage):
        #     self.phase = sequence.Voltage
        # if (sequence.HarmonicNumber):
        #     self.harmonic_number = sequence.HarmonicNumber
        # if (sequence.Frequency):
        #     self.frequency = sequence.Frequency
        # if (sequence.L):
        #     self.length = sequence.L
        # if (sequence.index):
        #     self.index = sequence.index
        # if (sequence.Method):
        #     self.method = sequence.Method
        # if (sequence.number_of_integration_steps):
        #     self.number_of_integration_steps = sequence.number_of_integration_steps
        # if (sequence.main_multipole_strength):
        #     self.main_multipole_strength = sequence.main_multipole_strength
        # if (sequence.main_multipole_index):
        #     self.main_multipole_index = sequence.main_multipole_index
