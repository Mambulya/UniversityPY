"""
метод Рунге-Кутты решения задачи Коши
* код для тестовой системы диф уравнений

x' = (x^2 * (1-x)) / (0.1 + x) - xy
y' = (x-m) * y
m из [0.1; 0.35]

"""
from math import e
import numpy as np
import matplotlib.pyplot as plt
from RKtest import runge_kutta


def system(t, y):
    y1, y2 = y

    dy1_dt = (((1-y1) * y1**2) / (0.1 + y1)) / y1*y2
    dy2_dt = (y1 - t) * y2

    return np.array([dy1_dt, dy2_dt])


# Начальные условия
y0 = [0.3, 0.3]
a = 0.1
b = 0.35
h = 0.01

# Решаем систему
m_values, y_values = runge_kutta(system, y0, a, b, h=h)

y1_values = y_values[:, 0]
y2_values = y_values[:, 1]

# Проверка точности
print(f"Решения при h = {h}:")
for t, y1, y2 in zip(m_values, y1_values, y2_values):
    print(f"m = {t:.2f}, X = {y1:.4f}, Y = {y2:.4f}")


# график решений
plt.plot(m_values, y1_values, color = "#1bf58b", label = "X")
plt.plot(m_values, y2_values, color = "#f56b1b", label = "Y")

plt.title("Численные решения X и Y при разных m")
plt.ylabel("X, Y")
plt.xlabel("m")
plt.grid()
plt.legend()
plt.show()
