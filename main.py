import time

import numpy as np

import model
from model import BinarySymmetricChannel
from model import GilbertElliotModel

np.random.seed(int(time.time()))

x = list(np.random.randint(2, size=1000))

print(f"Oryginalna tablica:     {x}")

bsc = BinarySymmetricChannel(0.1)
ge = GilbertElliotModel(0.2, 0.6, 0.7, 0.1)

after_bsc = bsc.accept(x)
after_ge = ge.accept(x)

print(f"Kanał Gilberta-Elliota: {after_ge}")
print(f"                   BER: {model.check_integrity(x, after_ge) * 100}%")
print(f"Kanał BSC:              {after_bsc}")
print(f"      BER:              {model.check_integrity(x, after_bsc) * 100}%")

