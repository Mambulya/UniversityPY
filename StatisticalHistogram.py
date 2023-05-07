import matplotlib.pyplot as plt
import openpyxl

# считываем данные
path = "./data.xlsx"
book = openpyxl.open(path, read_only=True)
sheet = book.active
data = []

# исходные данные
for row in range(1, 100000):
    try:
        data.append(float(sheet[row][0].value))
    except IndexError:
        break
    except ValueError:
        continue

volume = len(data)
num_bins = int(volume / 7)

# вычисление границ интервалов
step = (max(data) - min(data)) / num_bins
bins = [min(data) + step / 2]

for i in range(num_bins):
    bins.append(bins[-1] + step)

# вычисление частот каждого интервала
frequencies = [0] * num_bins
for d in data:
    for i in range(num_bins):
        if bins[i] <= d < bins[i + 1]:
            frequencies[i] += 1
            break

# построение диаграммы
fig, ax = plt.subplots(figsize=(13, 6))
for i in range(num_bins):
    rect = plt.Rectangle((bins[i], 0), step, frequencies[i], color='pink', ec='red')
    ax.add_patch(rect)
ax.set_xlim([min(data) - 1, max(data) + 2])
ax.set_ylim([0, max(frequencies) + 1])
plt.xticks(bins)

# настройка диаграммы
plt.xlabel("Values")
plt.ylabel("Amount")
plt.title("Statistical Histogram")
plt.legend(["Values"], loc=2, frameon=True)
plt.grid(linestyle='--', color='pink')

plt.show()
