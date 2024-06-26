import glob
import os
import time
import re

import numpy as np
from matplotlib import pyplot as plt

import model
from coder.bch.BCHCoder import BCHCoder
from coder.rs.ReedSolomonCoder import ReedSolomonCoder
from coder.triple.TripleCoder import TripleCoder
from model import BinarySymmetricChannel
from model import GilbertElliotModel

binary_symmetric_channel_good_params = [0.0005]
binary_symmetric_channel_bad_params = [0.3]
gilbert_elliot_model_good_params = [0.1, 0.8, 0.9, 0.005]
gilbert_elliot_model_bad_params = [0.3, 0.6, 0.5, 0.02]

coders = [TripleCoder(), BCHCoder(mu=7, delta=5), BCHCoder(mu=15, delta=11), BCHCoder(mu=15, delta=5),
          ReedSolomonCoder(16, 1), ReedSolomonCoder(8, 2), ReedSolomonCoder(64, 2)]

models = [BinarySymmetricChannel(*binary_symmetric_channel_good_params),
          BinarySymmetricChannel(*binary_symmetric_channel_bad_params),
          GilbertElliotModel(*gilbert_elliot_model_good_params),
          GilbertElliotModel(*gilbert_elliot_model_bad_params)]

models.reverse()

np.random.seed(int(time.time()))

output_directory = "output_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for coder in coders:
    count = 4
    for channel in models:
        filepath = os.path.join(output_directory,
                                f"{coder.name()}_{coder.parameters().replace(' ', '').replace(';', '_')}_{count}.txt")
        with open(filepath, "a") as file:
            for i in range(1):
                x = list(np.random.randint(2, size=np.random.randint(2048)))
                prepared = coder.prepare(x)

                try:
                    encoded = coder.encode(prepared)
                except Exception as e:
                    print(f"Error: {e}")
                    continue

                output = channel.accept(encoded)
                decoded = coder.decode(output)

                if len(decoded) > len(prepared):
                    decoded = decoded[:len(prepared)]

                try:
                    ber = model.check_integrity(prepared, decoded)

                except Exception as e:
                    print(e)
                    continue

                excess = len(encoded) / len(x) * 100

                save = (f"{coder.name()};{channel.name()}; {ber * 100}; {excess}; {coder.parameters()}; "
                        f"{channel.parameters()}\n")
                file.writelines(save)
            count -= 1

# do zapisu: [nazwa kodera; nazwa_kanalu; nazwa bit error rate; nadmiar bitowy; parametry kanalu; parametry kodera]

results = []
file_list = glob.glob(os.path.join(output_directory, '*'))
count_state = 1

for file_path in file_list:
    with open(file_path, 'r') as file:
        ber = []
        exceed = []

        for x in file:
            tokens = x.split(';')
            ber.append(float(tokens[2]))
            exceed.append(float(tokens[3]))

        canal_name = tokens[1]
        state = 0 if count_state % 2 == 0 else 1
        coder_name = re.split(r'[/.]', file_path)[1][:-2]
        average_ber = sum(ber) / len(ber)
        average_exceed = sum(exceed) / len(exceed) -100 # jezeli jest wiecej w 2 razy to jest wiecej w 100 procent a nie 200

        count_state += 1

        result = {'coder name': coder_name,
                  'canal name': canal_name,
                  'average ber': average_ber,
                  'average exceed': average_exceed,
                  'state': state}
        results.append(result)

x_BSC_good = []
x_BSC_bad = []
x_Gilbert_good = []
x_Gilbert_bad = []
y_BSC_good = []
y_BSC_bad = []
y_Gilbert_good = []
y_Gilbert_bad = []
titles_BSC_good = []
titles_BSC_bad = []
titles_Gilbert_good = []
titles_Gilbert_bad = []

for result in results:
    match result.get('canal name'), result.get('state'):
        case ('BSC', 0):
            titles_BSC_good.append(result.get('coder name'))
            x_BSC_good.append(result.get('average ber'))
            y_BSC_good.append(result.get('average exceed'))
        case ('BSC', 1):
            titles_BSC_bad.append(result.get('coder name'))
            x_BSC_bad.append(result.get('average ber'))
            y_BSC_bad.append(result.get('average exceed'))
        case ('Gilbert-Elliot', 0):
            titles_Gilbert_good.append(result.get('coder name'))
            x_Gilbert_good.append(result.get('average ber'))
            y_Gilbert_good.append(result.get('average exceed'))
        case ('Gilbert-Elliot', 1):
            titles_Gilbert_bad.append((result.get('coder name')))
            x_Gilbert_bad.append(result.get('average ber'))
            y_Gilbert_bad.append(result.get('average exceed'))

# Plot BST Good State
plt.figure(figsize=(10, 8))
plt.scatter(x_BSC_good, y_BSC_good, color='green', label='BST Good State')
for i, txt in enumerate(titles_BSC_good):
    plt.annotate(txt.replace('_', ' '), (x_BSC_good[i], y_BSC_good[i]))
plt.xlabel('Average BER')
plt.ylabel('Average Exceed')
plt.title('BST Good State')
plt.legend()
plt.grid(True)
plt.show()

# Plot BST Bad State
plt.figure(figsize=(10, 8))
plt.scatter(x_BSC_bad, y_BSC_bad, color='red', label='BST Bad State')
for i, txt in enumerate(titles_BSC_bad):
    plt.annotate(txt.replace('_', ' '), (x_BSC_bad[i], y_BSC_bad[i]))
plt.xlabel('Average BER')
plt.ylabel('Average Exceed')
plt.title('BST Bad State')
plt.legend()
plt.grid(True)
plt.show()

# Plot Gilbert-Elliot Good State
plt.figure(figsize=(10, 8))
plt.scatter(x_Gilbert_good, y_Gilbert_good, color='blue', label='Gilbert-Elliot Good State')
for i, txt in enumerate(titles_Gilbert_good):
    plt.annotate(txt.replace('_', ' '), (x_Gilbert_good[i], y_Gilbert_good[i]))
plt.xlabel('Average BER')
plt.ylabel('Average Exceed')
plt.title('Gilbert-Elliot Good State')
plt.legend()
plt.grid(True)
plt.show()

# Plot Gilbert-Elliot Bad State
plt.figure(figsize=(10, 8))
plt.scatter(x_Gilbert_bad, y_Gilbert_bad, color='orange', label='Gilbert-Elliot Bad State')
for i, txt in enumerate(titles_Gilbert_bad):
    plt.annotate(txt.replace('_', ' '), (x_Gilbert_bad[i], y_Gilbert_bad[i]))
plt.xlabel('Average BER')
plt.ylabel('Average Excess')
plt.title('Gilbert-Elliot Bad State')
plt.legend()
plt.grid(True)
plt.show()

# for file_path in file_list:
#     os.remove(file_path)








