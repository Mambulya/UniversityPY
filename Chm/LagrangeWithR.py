from taylorApprox import get_X_Y, arcsinh_approx
import matplotlib.pyplot as plt
import numpy as np

"""
Aппроксимирует функцию ареасинуса arcsinh(x) = ln(x + sqrt(x^2 + 1)) 
с помощью полинома Лагранжа на отрезке [a;b]. Узловые точки - значения полинома Тейлора 
из первой работы.

Вариант 7
step = 0,05
[0; 0,8]
степени полинома Лагранжа: n = 4,6,8,10,12,15,20
"""
a = 0
b = 0.8
eps = 0.000001

#Создаем сетку из узлов x и полученных полиномом Тейлора y
xi, yi = get_X_Y()


def makeLagrange(x, n):
    """
    :param x: точка в [a, b] НЕ УЗЛОВАЯ
    :param n: степень полинома
    :return: значение полинома лагранжа функуии arcsinh в точке x при степени n
    """
    sum = 0

    for i in range(0, n+1):
        multiplier = 1

        for j in range(0, n+1):
            if (i != j):
                multiplier *= ((x - xi[j]) / (xi[i] - xi[j]))

        sum += yi[i] * multiplier

    return sum

def drawLagrange(n):
    """
    рисует график полинома Лагранжа, Тейлора и функцию arsh(x) из numpy
    :param n: порядок полинома Лагранжа
    :return:
    """
    # придумаем неузловые x
    # пусть шаг будет 0.3
    step = 0.01
    ksis = []
    for i in range(0, 1000):
        ksi = a + i*step
        if (ksi >= b):
            break
        elif (ksi % 0.05 != 0):   # q на [a, b] и не узел, где 0.05 - старый шаг
            ksis.append(ksi)



    #значения полинома Лагранжа для новых x
    ys = [makeLagrange(X, n) for X in ksis]


    # выведим погрешность для точек ksi
    print("Погрешность в узловых точках:")
    for x in xi:
        print("|L({:.2f} - F({:.2f}))| = {}".format(x, x, abs(makeLagrange(x, n) - arcsinh_approx(x, eps))))

    print("Погрешность в точках кси:")
    for k in ksis:
        print("|L({:.2f} - F({:.2f}))| = {}".format(k, k, abs(makeLagrange(k, n) - arcsinh_approx(k, eps))))


    # функция приближенная вручную через Лагранжа
    plt.plot(ksis, ys, label = "lagrange arsh(x)")

    # check by numpy
    F = np.arcsinh(xi)
    plt.plot(xi, F, color= "red", label = "arsh(x)", linestyle = "--")

    # check by taylor
    plt.plot(xi, yi, label = "taylor arsh(x)", color = "green")

    plt.title("Ряд Лагранжа для Arsh(x)")
    plt.ylabel("y")
    plt.xlabel("x")
    plt.legend()
    plt.grid()

    plt.show()


drawLagrange(16)
