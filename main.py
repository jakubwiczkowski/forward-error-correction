import time

import komm
import numpy as np

import model
from coder.bch.BCHCoder import BCHCoder
from coder.triple.TripleCoder import TripleCoder
from model import BinarySymmetricChannel
from model import GilbertElliotModel

coders = [TripleCoder(), BCHCoder(mu=5, delta=7)]
models = [BinarySymmetricChannel(0.1), GilbertElliotModel(0.2, 0.8, 0.7, 0.01)]

np.random.seed(int(time.time()))
x = list(np.random.randint(2, size=16))
print(f"Oryginalna tablica:     {x}")

for coder in coders:
    print("===========================")
    print(f"# Koder {coder.name()}")
    for channel in models:
        print(f" > Kanał {channel.name()}")
        encoded = coder.encode(x)
        output = channel.accept(encoded)
        decoded = coder.decode(output)
        ber = model.check_integrity(x, decoded)

        print(f"  - enc: {encoded}")
        print(f"  - out: {output}")
        print(f"  - dec: {decoded}")
        print(f"  - BER: {ber * 100}%")


