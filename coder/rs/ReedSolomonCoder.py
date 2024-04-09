from reedsolo import RSCodec, ReedSolomonError

from coder.coder import Coder


class ReedSolomonCoder(Coder):
    def __init__(self, value: int):
        self.rsc = RSCodec(value)
        pass

    def encode(self, data: list[int]) -> list[int]:
        return [int(i) for i in bin(int.from_bytes(self.rsc.encode(bytes(data)), byteorder="big")).lstrip('0b')]

    def decode(self, data: list[int]) -> list[int]:
        output = list()
        try:
            output = [int(i) for i in bin(int.from_bytes(self.rsc.decode(data)[1], byteorder="big")).lstrip('0b')]
        except ReedSolomonError:
            output = data
        return output

    def name(self) -> str:
        return "RS - nie wiem"