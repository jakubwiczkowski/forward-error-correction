import time

import numpy as np

import model
from coder.bch.BCHCoder import BCHCoder
from coder.rs.ReedSolomonCoder import ReedSolomonCoder
from coder.triple.TripleCoder import TripleCoder
from model import BinarySymmetricChannel
from model import GilbertElliotModel

coders = [TripleCoder(), BCHCoder(mu=5, delta=7), ReedSolomonCoder(32), ReedSolomonCoder(128), ReedSolomonCoder(15), ReedSolomonCoder(200)]
models = [BinarySymmetricChannel(0.2),BinarySymmetricChannel(0.02),BinarySymmetricChannel(0.002),BinarySymmetricChannel(0.0002),BinarySymmetricChannel(0.00002), GilbertElliotModel(0.1, 0.8, 0.7, 0.01), GilbertElliotModel(0.01, 0.7, 0.7, 0.0001), GilbertElliotModel(0.05, 0.9, 0.9, 0.001)]

np.random.seed(int(time.time()))
x = list(np.random.randint(2, size=1024))
# print(f"Oryginalna tablica:     {x}")

for coder in coders:
    # print("===========================")
    # print(f"# Koder {coder.name()}")
    filepath = coder.name()+".txt"
    # print(filepath)
    file = open(filepath, "a")
    for channel in models:
        # print(f" > Kanał {channel.name()}")
        encoded = coder.encode(x)
        output = channel.accept(encoded)
        decoded = coder.decode(output)
        if(len(decoded)>len(x)):
            decoded = decoded[0:len(x)]
        ber = model.check_integrity(x, decoded)
        excess = len(encoded)/len(x) * 100
        # print(f"  - org: {x}")
        # print(f"  - enc: {encoded}")
        # print(f"  - out: {output}")
        # print(f"  - dec: {decoded}")
        # print(f"  - BER: {ber * 100}%")
        # print(f"  - exc: {excess}%")
        save = f"{coder.name()};{channel.name()}; {channel.parameters()} {ber * 100}; {excess}; {coder.parameters()}\n"
        file.writelines(save)
        # print(save)
    file.close()
        #do zapisu: [nazwa kodera; nazwa_kanalu; parametry kanalu; nazwa bit error rate; nadmiar bitowy; parametry kodera]
