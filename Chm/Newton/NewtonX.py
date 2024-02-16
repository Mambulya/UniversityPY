from Taylor import a, b, arcsinh_approx, eps
import matplotlib.pyplot as plt
import numpy as np

"""
Aппроксимирует функцию ареасинуса arcsinh(x) = ln(x + sqrt(x^2 + 1)) 
с помощью полинома Ньютона на отрезке [a;b]. Узловые точки - значения полинома Тейлора 
из первой работы. Равностоящие узлы интерполяции.
Вычисляет погрешности интерполяции и рисует график прогрешностей при разных n.

Вариант 7
step = 0,05
[0; 0,8]
степени полинома Ньютона: n = 4,6,8,10,12,15,20
"""

class NewtonPolynom:
    def __init__(self, nArg, aArg=0, bArg=0.8, epsArg=0.000001):
        self.a = aArg
        self.b = bArg
        self.eps = epsArg
        self.n = nArg
        self.xi = None  # узлы
        self.yi = None
        self.ys = None  # значения полинома Лагранжа для точек кси
        self.ksis = None
        self.errors = None


    def get_knots(self):
        """
        Создаем сетку из узлов x и полученных полиномом Тейлора y
        вычисляет сетку n+1 узлов для полинома Лагранжа степени n
        :param n: степень полинома Лагранжа
        :return: сетка
        """
        step = (self.b-self.a) / self.n
        self.xi = [self.a + i * step for i in range(0, int((self.b - self.a) / step) + 1)]
        self.yi = [arcsinh_approx(x, self.eps) for x in self.xi]

    def f(self, list_of_x: list):
        """
        вычисляет разделенную разность для k порядка, то есть коэффициенты для будущего полинома Ньютона
        f(xi, xi+1, ..., xk) - принимает список из ИНДЕКСОВ иксов
        :return: f(xi, xi+1, ..., xk) - разделенная разность
        """
        if len(list_of_x) == 2:
            index_first_x = list_of_x[0]
            index_second_x = list_of_x[1]
            return (self.yi[index_second_x] - self.yi[index_first_x]) / (self.xi[index_second_x] - self.xi[index_first_x])
        return (self.f(list_of_x[1:]) - self.f(list_of_x[:-1]) ) / (self.xi[list_of_x[-1]] - self.xi[list_of_x[0]])

    def makeNewtonForX(self, x, start_i = 0):
        """
        :param x: точка в [a, b] НЕ УЗЛОВАЯ
        :param n: степень полинома
        :return: значение полинома лагранжа функуии arcsinh в точке x при степени n
        """

        if self.xi is None:
            self.get_knots()

        sum = self.yi[start_i]

        for i in range(self.n-1):

            product = 1

            for j in range(start_i, i+1):
                product *= (x - self.xi[j])

            sum += self.f([l for l in range(start_i, i+2)])*product

        return sum

    def makeNewtonPolynom(self):
        """
        вычисляет список не узловых точек кси и значения полинома Ньютона в тосках кси
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
            elif (ksi % ((self.b-self.a) / self.n) != 0):   # q на [a, b] и не узел
                self.ksis.append(ksi)

        #значения полинома Ньютона для точек кси
        self.ys = [self.makeNewtonForX(k) for k in self.ksis]


    def printError(self):
        # выведим погрешность для точек ksi

        if self.ys is None:
            self.makeNewtonPolynom(self)

        print("Погрешность в узловых точках:")
        for x in self.xi:
            print("|L({:.2f}) - F({:.2f}))| = {}".format(x, x, abs(self.makeNewtonForX(x) - arcsinh_approx(x, self.eps))))

        print("Погрешность в точках кси:")
        for k in self.ksis:
            print("|L({:.2f}) - F({:.2f}))| = {}".format(k, k, abs(self.makeNewtonForX(k) - arcsinh_approx(k, self.eps))))


    def calculateErrors(self):
        """
        Вычисляет погрешности вычисления для каждой точки кси
        :return:
        """
        self.errors = []

        if self.ys is None:
            self.makeNewtonPolynom()

        for k in self.ksis:
            ERROR = abs(self.makeNewtonForX(k) - arcsinh_approx(k, self.eps))
            self.errors.append(ERROR)



    def drawPolynom(self):
        """
        рисует график полинома Ньютона, Тейлора и функцию arsh(x) из numpy
        """

        # функция приближенная вручную через полином Ньютона

        if self.ys is None:
            self.makeNewtonPolynom()

        plt.plot(self.ksis, self.ys, label = "Newton arsh(x)")

        # check by numpy
        F = np.arcsinh(self.xi)
        plt.plot(self.xi, F, color= "red", label = "arsh(x)", linestyle = "--")

        # check by taylor
        plt.plot(self.xi, self.yi, label = "taylor arsh(x)", color = "green")

        plt.title("Полином Ньютона для Arsh(x)")
        plt.ylabel("y")
        plt.xlabel("x")
        plt.legend()
        plt.grid()

        plt.show()



N1 = NewtonPolynom(20, a, b, eps)
N1.drawPolynom()
N1.printError()


# нарисуем как изменяется погрешность при увеличении n
Ns = []
colors = [(0.92, 0.75, 0.83), (0.75, 0.92, 0.75), (0.98, 0.66, 0.66), (0.79, 0.75, 0.92),
          (0.75, 0.8, 0.92),  (0.55, 0.8, 0.94), (0.75, 0.92, 0.87)]

for n in range(4, 13, 2):
    N = NewtonPolynom(n, a, b, eps)
    N.get_knots()
    N.calculateErrors()
    Ns.append([N.ksis, N.errors])

for n in range(15, 21, 5):
    N = NewtonPolynom(n, a, b, eps)
    N.get_knots()
    N.calculateErrors()
    Ns.append([N.ksis, N.errors])

for i in range(len(Ns)):
    if i == 6 or i == 5:
        plt.plot(Ns[i][0], Ns[i][1], color=colors[i], label="n = " + str(15 + 5*(i % 2 == 0)))
    else:
        plt.plot(Ns[i][0], Ns[i][1], color=colors[i], label="n = " + str(4+2*i))



plt.title("Погрешность при n")
plt.ylabel("R")
plt.xlabel("x")
plt.legend()
plt.grid()
plt.show()
