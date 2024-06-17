from reedsolo import RSCodec, ReedSolomonError

from coder.coder import Coder


class ReedSolomonCoder(Coder):
    def __init__(self,n, value: int):   #data length also has to be a multiple of 8
        self.value = value
        self.n = n                   #block size - must be a multiple of 8
        self.rsc = RSCodec(value)
        pass

    def encode(self, data: list[int]) -> list[int]:
        if len(data) % self.n != 0:
            data += [0] * (self.n - len(data) % self.n)
        string = [self.convert_segment(data[i:i + 8]) for i in range(0, len(data), 8)]
        blocks = [string[i:i + self.n // 8] for i in range(0, len(string), self.n // 8)]
        encoded_blocks = [self.rsc.encode(block) for block in blocks]
        output = list()
        for block in encoded_blocks:
            for byte in block:
                output.append(format(byte, '08b'))
        o = list()
        for byte_str in output:
            for bit in byte_str:
                o.append(int(bit))

        return o

    def convert_segment(self, segment):
        string = ''.join(str(bit) for bit in segment)
        return int(string, 2)

    def decode(self, data: list[int]) -> list[int]:
        string = [self.convert_segment(data[i:i + 8]) for i in range(0, len(data), 8)]

        block_size = self.n // 8 + self.value
        blocks = [string[i:i + block_size] for i in range(0, len(string), block_size)]
        decoded_blocks = []

        for block in blocks:
            i=0
            try:
                decoded_block, _, _ = self.rsc.decode(block)
                decoded_blocks.extend(decoded_block)
            except ReedSolomonError:
                decoded_blocks.extend(block[:self.n//8])
            i+=block_size
        output = list()
        for byte in decoded_blocks:
            output.append(format(byte, '08b'))

        o = list()
        for byte_str in output:
            for bit in byte_str:
                o.append(int(bit))

        return o

    def name(self) -> str:
        return "RS"

    def parameters(self) -> str:
        return f"{self.n}; {self.value}"        # liczba bajtów kontrolnych