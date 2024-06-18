import komm
import numpy as np

from coder.coder import Coder


class BCHCoder(Coder):
    def __init__(self, mu: int, delta: int):
        parameter = mu
        correcting_capability = delta
        self.bch_code = komm.BCHCode(parameter, correcting_capability)
        self.encoder = komm.BlockEncoder(self.bch_code)
        self.decoder = komm.BlockDecoder(self.bch_code)

    def prepare(self, data: list[int]) -> list[int]:
        if len(data) % self.bch_code.dimension == 0:
            return data

        additional_zeros = self.bch_code.dimension - (len(data) % self.bch_code.dimension)
        return np.append(data, [np.zeros(additional_zeros, dtype=np.uint8)]).tolist()

    def encode(self, data: list[int]) -> list[int]:
        return self.encoder(data).tolist()

    def decode(self, data: list[int]) -> list[int]:
        return self.decoder(data).tolist()

    def split_into_chunks(self, target: list[int], n: int):
        num_chunks = -(-len(target) // n)  # Equivalent to ceil(len(lst) / n)

        chunks = [target[i * n:(i + 1) * n] for i in range(num_chunks)]

        last_chunk_len = len(chunks[-1])
        if last_chunk_len < n:
            chunks[-1].extend([0] * (n - last_chunk_len))

        return chunks

    def name(self) -> str:
        return f"BCH"
        # return f"BCH - mu = {self.bch_code.mu} / delta = {self.bch_code.delta}"

    def parameters(self) -> str:
        return f"{self.bch_code.mu}; {self.bch_code.delta}"
