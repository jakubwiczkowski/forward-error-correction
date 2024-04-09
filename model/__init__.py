from .gilbertelliott.channel import GilbertElliotModel
from .bsc.channel import BinarySymmetricChannel


def check_integrity(original: list[int], after_channel: list[int]) -> float:
    if len(original) != len(after_channel):
        return 0

    total_bits = len(original)
    faulty_bits = 0

    for idx, bit in enumerate(original):
        if after_channel[idx] == bit:
            continue
        faulty_bits += 1

    return (faulty_bits / total_bits)
