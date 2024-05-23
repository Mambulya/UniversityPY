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


def system(y, m):
    y1, y2 = y

    dy1_dt = (((1-y1) * y1**2) / (0.1 + y1)) / y1*y2
    dy2_dt = (y1 - m) * y2

    return np.array([dy1_dt, dy2_dt])

if __name__ == "__main__":
    # Начальные условия
    y0 = [0.3, 0.3]
    a = 0
    b = 0.4
    h = 0.03

    # Диапазон значений параметра m
    m_values = [0.1, 0.15, 0.25, 0.35]

    figure, axis = plt.subplots(1, 3)

    for m in m_values:
        t_values, y_values = runge_kutta(lambda t, y: system(y, m), y0, a, b, h)
        X_values = y_values[:, 0]
        Y_values = y_values[:, 1]

        axis[0].plot(t_values, X_values, label=f'X(t) при m={m:.2f}')
        axis[1].plot(t_values, Y_values, label=f'Y(t) при m={m:.2f}', linestyle='dashed')
        axis[2].plot(X_values, Y_values, label=f'X и Y при m={m:.2f}')

    axis[0].legend()
    axis[1].legend()
    axis[2].legend()
    axis[0].set_title('Численные решения Х(t) при m')
    axis[1].set_title('Численные решения Y(t) при m')
    axis[2].set_title('Численные решения (X, Y) при m')
    axis[0].grid()
    axis[1].grid()
    axis[2].grid()

    plt.show()


