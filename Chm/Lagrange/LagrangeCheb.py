"""
Aппроксимирует функцию ареасинуса arcsinh(x) = ln(x + sqrt(x^2 + 1))
с помощью полинома Лагранжа на отрезке [a;b]. Узловые точки - значения полинома Тейлора
из первой работы. 
Используются Чебышевские узлы вместо равностоящих из LagrangeX.py!
"""

from Taylor import arcsinh_approx, a, b, eps
import matplotlib.pyplot as plt
import numpy as np
import math

"""
Aппроксимирует функцию ареасинуса arcsinh(x) = ln(x + sqrt(x^2 + 1)) 
с помощью полинома Лагранжа на отрезке [a;b]. Узловые точки - значения полинома Тейлора 
из первой работы.

Вариант 7
step = 0,05
[0; 0,8]
степени полинома Лагранжа: n = 4,6,8,10,12,15,20
"""


class LagrangePolynom:

    def __init__(self, nArg, aArg = 0, bArg = 0.8, epsArg = 0.000001):
        self.a = aArg
        self.b = bArg
        self.eps = epsArg
        self.n = nArg
        self.xi = None  # узлы
        self.yi = None
        self.xs = None
        self.ys = None
        self.ksis = None
        self.errors = None


    def get_knots(self, n= 70):
        """
        Создаем сетку из Чебышевских узлов x и полученных полиномом Тейлора y
        вычисляет сетку n+1 узлов для полинома Лагранжа степени n
        :param n: количество Чебышевских узлов на [-1;1] - тех, которые [a;b] будет меньше
        за n может быть взять 69б 70б 71, 72, так как при этих параметрах получается 21 Чебовских узлов
        на [0;0.8] - число 21 нужно, чтобы не адаптировать программу из-под равностаронних узлов из
        предыдущего скрипта
        :return: сетка
        """

        # вычисление Чебышевских узлов по формуле Xi = cos( (2*i*pi - pi) / (2*n))
        self.xi = sorted([math.cos(((2 * i - 1) * math.pi) / (2 * n)) for i in range(0, n) if 0 <= math.cos(((2 * i - 1) * math.pi) / (2 * n)) <= 0.8])
        self.yi = [arcsinh_approx(x, self.eps) for x in self.xi]


    def makeLagrangeForX(self, x):
        """
        :param x: точка в [a, b] НЕ УЗЛОВАЯ
        :param n: степень полинома
        :return: значение полинома лагранжа функуии arcsinh в точке x при степени n
        """

        if self.xi is None:
            self.get_knots()

        sum = 0

        for i in range(0, self.n+1):
            multiplier = 1

            for j in range(0, self.n+1):
                if (i != j):
                    multiplier *= ((x - self.xi[j]) / (self.xi[i] - self.xi[j]))

            sum += self.yi[i] * multiplier

        return sum


    def makeLagrangePolynom(self, stepArg = 0.01):
        """
        вычисляет список не узловых точек кси и знаяения полинома лагранжа в тосках кси
        :param step: через какое расстояние выберем новые точки кси
        :return:
        """

        # придумаем неузловые x - точки кси
        step = 0.01
        self.ksis = []
        for i in range(0, 1000):
            ksi = self.a + i*step
            if (ksi >= self.b):
                break
            elif (ksi % ((self.b-self.a) / self.n) != 0):   # q на [a, b] и не узел, где 0.05 - старый шаг
                self.ksis.append(ksi)

        #значения полинома Лагранжа для точек кси
        self.ys = [self.makeLagrangeForX(k) for k in self.ksis]


    def printError(self):
        # выведим погрешность для точек ksi

        if self.ys is None:
            self.makeLagrangePolynom(self)

        print("Погрешность в узловых точках:")
        for x in self.xi:
            print("|L({:.2f}) - F({:.2f}))| = {}".format(x, x, abs(self.makeLagrangeForX(x) - arcsinh_approx(x, self.eps))))

        print("Погрешность в точках кси:")
        for k in self.ksis:
            print("|L({:.2f}) - F({:.2f}))| = {}".format(k, k, abs(self.makeLagrangeForX(k) - arcsinh_approx(k, self.eps))))


    def calculateErrors(self):

        self.errors = []

        if self.ys is None:
            self.makeLagrangePolynom(self)

        for k in self.ksis:
            ERROR = abs(self.makeLagrangeForX(k) - arcsinh_approx(k, self.eps))
            self.errors.append(ERROR)



    def drawPolynom(self):
        """рисует график полинома Лагранжа, Тейлора и функцию arsh(x) из numpy"""
        # функция приближенная вручную через Лагранжа

        if self.ys is None:
            self.makeLagrangePolynom(self)

        plt.plot(self.ksis, self.ys, label = "lagrange arsh(x)")

        # check by numpy
        F = np.arcsinh(self.xi)
        plt.plot(self.xi, F, color= "red", label = "arsh(x)", linestyle = "--")

        # check by taylor
        plt.plot(self.xi, self.yi, label = "taylor arsh(x)", color = "green")

        plt.title("Ряд Лагранжа для Arsh(x)")
        plt.ylabel("y")
        plt.xlabel("x")
        plt.legend()
        plt.grid()

        plt.show()


L1 = LagrangePolynom(20, a, b, eps)
L1.drawPolynom()
L1.printError()


# нарисуем как изменяется погрешность при увеличении n
Ls = []
colors = [(0.92, 0.75, 0.83), (0.75, 0.92, 0.75), (0.98, 0.66, 0.66), (0.79, 0.75, 0.92),
          (0.75, 0.8, 0.92),  (0.55, 0.8, 0.94), (0.75, 0.92, 0.87)]
for n in range(4, 13, 2):
    L = LagrangePolynom(n, a, b, eps)
    L.get_knots()
    L.calculateErrors()
    Ls.append([L.ksis, L.errors])

for n in range(15, 21, 5):
    L = LagrangePolynom(n, a, b, eps)
    L.get_knots()
    L.calculateErrors()
    Ls.append([L.ksis, L.errors])

for i in range(len(Ls)):
    if i == 6 or i == 5:
        plt.plot(Ls[i][0], Ls[i][1], color=colors[i], label="n = " + str(15 + 5*(i % 2 == 0)))
    else:
        plt.plot(Ls[i][0], Ls[i][1], color=colors[i], label="n = " + str(4+2*i))



plt.title("Погрешность при n")
plt.ylabel("R")
plt.xlabel("x")
plt.legend()
plt.grid()
plt.show()
