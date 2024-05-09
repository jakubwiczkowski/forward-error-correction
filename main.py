import os
import time

import numpy as np
from matplotlib import pyplot as plt

import model
from coder.bch.BCHCoder import BCHCoder
from coder.rs.ReedSolomonCoder import ReedSolomonCoder
from coder.triple.TripleCoder import TripleCoder
from model import BinarySymmetricChannel
from model import GilbertElliotModel

coders = [TripleCoder(), BCHCoder(mu=5, delta=7), BCHCoder(mu=3, delta=7), ReedSolomonCoder(32), ReedSolomonCoder(64), ReedSolomonCoder(128),
          ReedSolomonCoder(200)]
models = [BinarySymmetricChannel(0.5), BinarySymmetricChannel(0.2), BinarySymmetricChannel(0.02), BinarySymmetricChannel(0.002),
          BinarySymmetricChannel(0.0002), BinarySymmetricChannel(0.00002), GilbertElliotModel(0.1, 0.8, 0.7, 0.01),
          GilbertElliotModel(0.01, 0.7, 0.7, 0.0001), GilbertElliotModel(0.05, 0.9, 0.9, 0.001)]

models.reverse()

np.random.seed(int(time.time()))
x = list(np.random.randint(2, size=1024))
# print(f"Oryginalna tablica:     {x}")

for coder in coders:
    # print("===========================")
    # print(f"# Koder {coder.name()}")
    filepath = coder.name() + ".txt"
    # print(filepath)
    file = open(filepath, "a")
    for channel in models:
        # print(f" > Kanał {channel.name()}")
        encoded = coder.encode(x)
        output = channel.accept(encoded)
        decoded = coder.decode(output)
        if (len(decoded) > len(x)):
            decoded = decoded[0:len(x)]
        ber = model.check_integrity(x, decoded)
        excess = len(encoded) / len(x) * 100
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

plt.rcParams["figure.figsize"] = [6, 4]
plt.rcParams["figure.autolayout"] = True

data_list = ['BCH.txt', 'Potrojeniowy.txt', 'RS.txt']

root_dir = "plots"

for data in data_list:
    count = 0
    with open(data, "rt") as file:
        for x in file:
            tokens = x.split(';')

            if tokens[0] == 'BCH':
                coder_name = tokens[0]
                model_name = tokens[1]
                if tokens[1] == 'BSC':
                    model_params = [tokens[2]]
                    ber = tokens[3]
                    excess = tokens[4]
                    coder_params = [tokens[5], tokens[6]]
                else:
                    model_params = [tokens[2], tokens[3], tokens[4], tokens[5]]
                    ber = tokens[6]
                    excess = tokens[7]
                    coder_params = [tokens[8], tokens[9]]

            if tokens[0] == 'Potrojeniowy':
                coder_name = tokens[0]
                model_name = tokens[1]
                if tokens[1] == 'BSC':
                    model_params = [tokens[2]]
                    ber = tokens[3]
                    excess = tokens[4]
                    coder_params = []
                else:
                    model_params = [tokens[2], tokens[3], tokens[4], tokens[5]]
                    ber = tokens[6]
                    excess = tokens[7]
                    coder_params = []

            if tokens[0] == 'RS':
                coder_name = tokens[0]
                model_name = tokens[1]
                if tokens[1] == 'BSC':
                    model_params = [tokens[2]]
                    ber = tokens[3]
                    excess = tokens[4]
                    coder_params = [tokens[5]]
                else:
                    model_params = [tokens[2], tokens[3], tokens[4], tokens[5]]
                    ber = tokens[6]
                    excess = tokens[7]
                    coder_params = [tokens[8]]

            coder_params_str = ','.join(coder_params).replace('\n', '')
            model_params_str = ','.join(model_params).replace('\n', '')

            title = f"{coder_name}({coder_params_str})\n{model_name}({model_params_str})"

            plt.title(title, loc='center', wrap=False)
            plt.scatter(ber, excess)

            nested_dir = os.path.join(root_dir, tokens[0])
            os.makedirs(nested_dir, exist_ok=True)

            filename = os.path.join(nested_dir, f"{tokens[0]}{count}.png")
            count += 1

            plt.xlabel("Bit Error Rate")
            plt.ylabel("Excess")
            plt.savefig(filename)
            plt.close()
