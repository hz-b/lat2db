from dataclasses import dataclass
import numpy as np

nan = np.nan


@dataclass
class Sequencer:
    name: str
    index: int
    strength: float = 0.0
    length: float = 0.0
    method: int = -1
    number_of_integration_steps: int = 4
    main_multipole_strength: float = 0.0
    main_multipole_index: int = -1
    type: str = "unknown"
    bending_angle: float = 0e0
    entry_angle: float = 0e0
    exit_angle: float | None = None
    frequency: float | None = None
    voltage: float | None = None
    phase: float | None = None
    harmonic_number: int = -1

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
