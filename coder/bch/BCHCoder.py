import komm

from coder.coder import Coder


class BCHCoder(Coder):
    def __init__(self, mu: int, delta: int):
        self.bch_code = komm.BCHCode(mu, delta)
        self.encoder = komm.BlockEncoder(self.bch_code)
        self.decoder = komm.BlockDecoder(self.bch_code)

    def encode(self, data: list[int]) -> list[int]:
        split_data = self.split_into_chunks(data, self.bch_code.dimension)
        encoded_data = []
        for chunk in split_data:
            for bit in self.encoder(chunk):
                encoded_data.append(bit)
        return encoded_data

    def decode(self, data: list[int]) -> list[int]:
        split_data = self.split_into_chunks(data, self.bch_code.length)
        decoded_data = []
        for chunk in split_data:
            for bit in self.decoder(chunk):
                decoded_data.append(bit)
        return decoded_data

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
