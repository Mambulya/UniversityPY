import numpy as np
import matplotlib.pyplot as plt
import openpyxl


# считываем данные
path = "./data.xlsx"
book = openpyxl.open(path, read_only=True)
sheet = book.active
data = []

for row in range(1, 100000):
    try:
        data.append(float(sheet[row][0].value))
    except IndexError:
        break
    except ValueError:
        continue


# находим характеристики распределения
volume = len(data)
MAX = max(data)
MIN = min(data)
diff = MAX - MIN
Ex = sum(data) / volume                             # выборочное среднее - состоятельная и не смещенная оценка параметра
Dx = np.var(data)                                   # дисперсия var() - смещенная
б = Dx**(1/2)                                       # среднее квадротическое

# Гисторграммы - частотная/вероятностная
k = int(volume/5)                                   # количество интервалов
step = (MAX - MIN) / (k-1)                          # шаг между интервалами
interval1 = MIN + step/2
intervalK = MAX - step/2                            # последняя метка
intervals = [interval1]

# формируем метки интеравалов
for i in range(1, k-1):
    intervals.append(intervals[i-1] + step)
intervals.append(intervalK)


# рисуем гистограмму распределения
fig, diagram = plt.subplots(figsize =(13, 6))      # размер картинки

plt.hist(data,intervals, color="pink", ec="red")
plt.xticks(intervals)
plt.xlabel("Values")
plt.ylabel("Amount")
plt.title("Statistics Histogram")
plt.legend("Values", loc=2, frameon=False)
plt.grid(linestyle='--', color='pink')
plt.show()


# OUTPUT
print(
"""
MAX = {}
MIN = {}
количество интервалов (k) = {}
step = {}
interval 1 = {}
interval K = {}
Ex = {}
б = {}
Dx = б**2 = {}
""".format( MAX, MIN, k, step, interval1, intervalK, np.round(Ex, 3), б, Dx))
