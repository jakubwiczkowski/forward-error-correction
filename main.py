import numpy as np
import komm

np.random.seed(1)

bsc = komm.BinarySymmetricChannel(0.1)

x = [0, 1, 1, 1, 0, 0, 0, 0, 0, 1]
y = bsc(x)

print(y)