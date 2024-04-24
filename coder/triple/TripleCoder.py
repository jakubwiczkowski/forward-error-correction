from coder.coder import Coder


class TripleCoder(Coder):
    def __init__(self):
        pass

    def encode(self, data: list[int]) -> list[int]:
        output = list()

        for bit in data:
            output += [bit] * 3

        return output

    def decode(self, data: list[int]) -> list[int]:
        output = list()

        count = 0
        ones = 0
        zeros = 0

        for bit in data:
            if bit == 1:
                ones += 1
            else:
                zeros += 1

            count += 1

            if count != 3:
                continue

            output.append(1 if ones > zeros else 0)

            count = 0
            ones = 0
            zeros = 0

        return output

    def name(self) -> str:
        return "Potrojeniowy"

    def parameters(self) -> str:
        return ""
