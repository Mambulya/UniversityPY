"""
Реализация кусочно-квадратичной аппроксимации
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.sin(x)

def quad_interp(x0, x1, x2, y0, y1, y2, x):
    """Интерполяция квадратным полиномом по трем точкам."""
    L0 = ((x - x1)*(x - x2)) / ((x0 - x1)*(x0 - x2))
    L1 = ((x - x0)*(x - x2)) / ((x1 - x0)*(x1 - x2))
    L2 = ((x - x0)*(x - x1)) / ((x2 - x0)*(x2 - x1))
    return y0*L0 + y1*L1 + y2*L2

def square_approximation(f, a, b, n):
    """
    Выполняет кусочно-квадратичную аппроксимацию функции f на отрезке [a, b]
    n — число отрезков
    """
    if n % 2 != 0:
        raise ValueError("Для кусочно-квадратичной аппроксимации n % 2 = 0")

    x_nodes = np.linspace(a, b, n + 1)
    y_nodes = f(x_nodes)
    x_plot = np.linspace(a, b, 100)
    y_true = f(x_plot)
    y_approx = np.zeros_like(x_plot)

    for i in range(0, n - 1, 2):  # каждые 3 узла (i, i+1, i+2)
        x0, x1, x2 = x_nodes[i:i+3]
        y0, y1, y2 = y_nodes[i:i+3]
        mask = (x_plot >= x0) & (x_plot <= x2)
        y_approx[mask] = quad_interp(x0, x1, x2, y0, y1, y2, x_plot[mask])

    return (x_plot, y_true, y_approx, x_nodes, y_nodes)

# Параметры аппроксимации
a = 0
b = 2 * np.pi
n = 6

# Выполняем аппроксимацию
x_plot, y_true, y_approx, x_nodes, y_nodes = square_approximation(f, a, b, n)
# [0.         1.04719755 2.0943951  3.14159265 4.1887902  5.23598776 6.28318531] x_nodes

print("Погрешность в точках не узловых:")
for i in range(1, len(x_plot)-1):
    print("|f({:.3f}) - ф({:.3f})| = {}".format(x_plot[i], x_plot[i], np.abs(y_approx[i] - y_true[i])))

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_true, label='f(x) = sin(x)', linewidth=2, color="#dad4ce")
plt.plot(x_plot, y_approx, '--', label='Кусочно-линейная аппроксимация', linewidth=2, color="#94af8c")
plt.plot(x_nodes, y_nodes, "o", label='Узлы аппроксимации', color="#ad1f2b")
plt.title('Кусочно-линейная аппроксимация функции')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.legend()
plt.show()