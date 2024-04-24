import komm

from model.model import Model


class BinarySymmetricChannel(Model):
    def __init__(self, p: float):
        self.p = p
        self.channel = komm.BinarySymmetricChannel(p)

    def accept(self, data: list[int]) -> list[int]:
        return list(self.channel(data))

    def name(self) -> str:
        return f"BSC"
        # return f"BSC - p = {self.p}"

    def parameters(self) -> str:
        return f"{self.p};"
