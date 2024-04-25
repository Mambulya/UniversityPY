from taylorApprox import arcsinh_approx, a, b
"""
Квадратурные формулы:
    правых прямоугольников
    левых прямоугольников
    трапеций
    симпсона
    гауса

"""
eps1 = 0.00001
eps2 = 0.0000001

def right_rectangle_rule(f, a, b, n):
    """
    Вычисляет приближенное значение определенного интеграла
    с использованием правых прямоугольников.

    f: функция, которую необходимо проинтегрировать
    a, b: пределы интегрирования
    n: количество прямоугольников
    """
    dx = (b - a) / n
    integral = 0
    for i in range(1, n + 1):
        integral += f(a + i * dx)
    integral *= dx
    return integral


def midpoint_rectangle_rule(f, a, b, n):
    """
    Вычисляет приближенное значение определенного интеграла
    с использованием формулы центральных прямоугольников.

    f: функция, которую необходимо проинтегрировать
    a, b: пределы интегрирования
    n: количество прямоугольников
    """
    dx = (b - a) / n
    integral = 0
    for i in range(n):
        x_midpoint = a + (i + 0.5) * dx
        integral += f(x_midpoint)
    integral *= dx
    return integral


def trapezoidal_rule(f, a, b, n):
    """
    Вычисляет приближенное значение определенного интеграла
    с использованием формулы трапеций.

    f: функция, которую необходимо проинтегрировать
    a, b: пределы интегрирования
    n: количество трапеций
    """
    dx = (b - a) / n
    integral = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        integral += f(a + i * dx)
    integral *= dx
    return integral


def simpsons_rule(f, a, b, n):
    """
    Вычисляет приближенное значение определенного интеграла
    с использованием формулы Симпсона.

    f: функция, которую необходимо проинтегрировать
    a, b: пределы интегрирования
    n: количество интервалов (должно быть четным числом)
    """
    if n % 2 != 0:
        raise ValueError("Число интервалов должно быть четным")

    dx = (b - a) / n
    integral = f(a) + f(b)

    for i in range(1, n, 2):
        integral += 4 * f(a + i * dx)
    for i in range(2, n - 1, 2):
        integral += 2 * f(a + i * dx)

    integral *= dx / 3
    return integral


def gauss_legendre_two_points(f, a, b, t = 0):
    """
    Вычисляет приближенное значение определенного интеграла
    с использованием квадратурной формулы Гаусса с двумя узлами.

    f: функция, которую необходимо проинтегрировать
    a, b: пределы интегрирования
    """
    x1 = -0.5773502691896257  # Первый узел
    x2 = 0.5773502691896257  # Второй узел

    # Веса для двух узлов
    w1 = w2 = 1

    # Преобразование интервала интегрирования от [-1, 1] к [a, b]
    integral = 0.5 * (b - a) * (w1 * f(0.5 * (b - a) * x1 + 0.5 * (a + b)) + w2 * f(0.5 * (b - a) * x2 + 0.5 * (a + b)))

    return integral


def Sn(n, kv_f):
    """

    :param n: степень разбиение
    :param f: квадратурная формула
    :return:
    """
    h = 1
    if kv_f == simpsons_rule:
        h = 2

    S = 0

    for i in range(1, n+1, h):
        S += kv_f(arcsinh_approx, a, b, i)

    return S

N = 1
ERROR = abs(Sn(N, right_rectangle_rule) - Sn(2*N, right_rectangle_rule))

for i in range(0, 10):
    print("S = " , right_rectangle_rule(arcsinh_approx, a, b, N), " n = ", N, " error = ", ERROR)
    N += 1
    ERROR = abs(Sn(N, right_rectangle_rule) - Sn(2 * N, right_rectangle_rule))
