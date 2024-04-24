from enum import Enum

import komm

from model.model import Model
import numpy as np


class State(Enum):
    GOOD = 1
    BAD = 2


class GilbertElliotModel(Model):
    def __init__(self, b: float, g: float, p_b: float, p_g: float):
        self.state = State.GOOD
        self.b = b          # prawdopodobienstwo zmiany na zly stan
        self.g = g          # prawdopodobienstwo zmiany na dobry stan
        self.p_b = p_b      # prawdopodobienstwo przeklamania bitu w stanie zlym
        self.p_g = p_g      # prawdopodobienstwo przeklamania bitu w stanie dobrym

        self.good_channel = komm.BinarySymmetricChannel(p_g)
        self.bad_channel = komm.BinarySymmetricChannel(p_b)

    def accept(self, data: list[int]) -> list[int]:
        output = list(data)

        for idx, bit in enumerate(data):
            p = np.random.uniform(low=0.0, high=1.0)

            if self.state == State.GOOD:
                y = self.good_channel(bit)
                if p < self.b:
                    self.state = State.BAD
            else:
                y = self.bad_channel(bit)
                if p < self.g:
                    self.state = State.GOOD

            output[idx] = y[0]
        return output

    def name(self) -> str:
        return f"Gilbert-Elliot"
        # return f"Gilbert-Elliot - b = {self.b} / g = {self.g} / p_b = {self.p_b} / p_g = {self.p_g}"

    def parameters(self) -> str:
        return f"{self.b}; {self.g}; {self.p_b}; {self.p_g};"
