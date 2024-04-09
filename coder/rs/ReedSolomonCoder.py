from reedsolo import RSCodec, ReedSolomonError

from coder.coder import Coder


class ReedSolomonCoder(Coder):
    def __init__(self, value: int):
        self.rsc = RSCodec(value)
        pass

    def encode(self, data: list[int]) -> list[int]:
        string = [self.convert_segment(data[i:i + 8]) for i in range(0, len(data), 8)]
        encoded = self.rsc.encode(string)
        output = list()
        for byte in encoded:
            output.append(format(byte, '08b'))
        o = list()
        for i in range(0, len(output)):
            for bit in output[i]:
                o.append(int(bit))
        return o

    def convert_segment(self, segment):
        string = ''.join(str(bit) for bit in segment)
        return int(string, 2)

    def decode(self, data: list[int]) -> list[int]:
        string = [self.convert_segment(data[i:i + 8]) for i in range(0, len(data), 8)]
        try:
            out, _, _ = self.rsc.decode(string)
        except:
            return "error"
        output = list()
        for byte in out:
            output.append(format(byte, '08b'))
        o = list()
        for i in range(0, len(output)):
            for bit in output[i]:
                o.append(int(bit))
        return o

    def name(self) -> str:
        return "RS - nie wiem"