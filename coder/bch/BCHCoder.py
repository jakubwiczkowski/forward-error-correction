import komm

from coder.coder import Coder


class BCHCoder(Coder):
    def __init__(self, mu: int, delta: int):
        self.bch_code = komm.BCHCode(mu, delta)
        self.encoder = komm.BlockEncoder(self.bch_code)
        self.decoder = komm.BlockDecoder(self.bch_code)

    def encode(self, data: list[int]) -> list[int]:
        return list(self.encoder(data))

    def decode(self, data: list[int]) -> list[int]:
        return list(self.decoder(data))

    def name(self) -> str:
        return f"BCH"
        # return f"BCH - mu = {self.bch_code.mu} / delta = {self.bch_code.delta}"

    def parameters(self) -> str:
        return f"{self.bch_code.mu}; {self.bch_code.delta}"
