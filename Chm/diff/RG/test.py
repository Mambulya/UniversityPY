"""
метод Рунге-Кутты решения задачи Коши
* код для тестовой системы диф уравнений

y1' = -2y1 - 3y2 + 4e^-t
y2' = 3y1 - 2y2 + 4e^-t
y1(0) = 0, y2(0) = 0

[0, 4]
"""
from math import e

def f1Test(t, x1, x2):
    return -2 * x1 - 3*x2 + 4*e**(-t)

def f2Test(x1, x2, t):
    return 3* x1 - 2*x2 + 4*e**(-t)

def RGtest(h = 0.5):
    a = 0
    b = 4
    t = 0
    y0 = 0
    y1 = y0     # yi и y(i-1)
    y2 = y0

    for i in range(int((b-a) / h)):
        # вычисляем y1 на шаге i - при этом берем y2 при i
        k1 = f1Test(t, y1, y2)
        k2 = f1Test(t + h/4, y1 + h/4*k1, y2)
        k3 = f1Test(t + h/2, y1 + h/2*k2, y2)
        k4 = f1Test(t + h, y1 + h*k1 - 2*h*k2 + 2*h*k3, y2)
        y1New = y1 + (h/6) * (k1 + 4*k3 + k4)

        # вычисляем y2 на шаге i - при этом берем y1 при i+1 (новый)
        k1 = f1Test(t, y1New, y2)
        k2 = f1Test(t + h/4, y1New + h/4*k1, y2)
        k3 = f1Test(t + h/2, y1New + h/2*k2, y2)
        k4 = f1Test(t + h, y1New + h*k1 - 2*h*k2 + 2*h*k3, y2)
        y2 += (h/6) * (k1 + 4*k3 + k4)

        # обновляем данные
        y1 = y1New
        t += h

        if 3.0 <= t <= 3.1:
            print("i = {}: y1 = {}   y2 = {}".format(i, y1, y2))

RGtest(h = 0.03)
