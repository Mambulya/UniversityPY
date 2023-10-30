import matplotlib.pyplot as plt
import numpy as np

"""
Aппроксимирует функцию ареасинуса arcsinh(x) = ln(x + sqrt(x^2 + 1)) 
с помощью полинома Тейлора до погрешности eps на отрезке [a;b].

Вариант 7
eps = 0,000001
step = 0,05
[0; 0,8]
"""
# input
eps = 0.000001
step = 0.05
a = 0
b = 0.8
n = 1


def arcsinh_approx(x, eps):
    """аппроксимирует саму функуию"""
    result = x
    q = x
    n = 0
    while abs(q) >= eps:
        q *= (-1) * (x**2) * (2*n + 1)**2 / ((2*n + 2) * (2*n + 3))
        result += q
        n += 1
    return result


def arcsinh_dev_approx(x, eps):
    """аппроусимипует производную"""
    result = 1
    q = 1
    n = 0
    while abs(q) >= eps:
        q *= (-2*n - 1) * (x**2) / (2*n + 2)
        result += q
        n += 1

    return result

# значения х, в которых нужно вычислить arsh(x) и Varcsinh(x)/Vx
def get_X_Y():
    xs = [a + i*step for i in range(0, int((b - a)/step)+1)]
    ys = [arcsinh_approx(x, eps) for x in xs]
    return xs, ys

xi, yi = get_X_Y()
dev_yi = [arcsinh_dev_approx(x, eps) for x in xi]   # аппрохимированная производная arcsinh(x)

if __name__ == "main":
    print("вывод значений аппроксимируемого arsh(x)")
    for i in range(len(xi)):
        print("F({:.2f}) = {}".format(xi[i], yi[i]))

    print("вывод значений аппроксимируемой производной arsh(x)")
    for i in range(len(xi)):
        print("F({:.2f}) = {}".format(xi[i], dev_yi[i]))

    # проверяем насколько совадает с arsh(x) в numpy
    F = np.arcsinh(xi)
    f = [1 / np.sqrt(1 + x**2) for x in xi]



    # функция в numpy
    plt.plot(xi, f, color = "red", label = "arsh'(x)")
    plt.plot(xi, F, color= "red", label = "arsh(x)", linestyle = "--")
    # функция приближенная вручную
    plt.plot(xi, yi, label = "approx arsh(x)")
    plt.plot(xi, dev_yi, label = "approx arsh'(x)", color="green")

    plt.title("Ряд Тейлора для Arsh(x)")
    plt.ylabel("y")
    plt.xlabel("x")
    plt.legend()
    plt.grid()

    plt.show()
