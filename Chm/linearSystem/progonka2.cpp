from linearSystem import create_system
from math import sin
import matplotlib.pyplot as plt


def progonka(A, f):
    m = len(A)

    c = [0] * m     # верхняя диагональ
    b = [0] * m     # средняя диагональ
    a = [0] * m     # нижняя диагональ
    x = [0] * (m+2)     # alpha * x + beta

    alpha = [0]
    beta = [0]

    for i in range(m):
        b[i] = A[i][i]
        if i > 0:
            a[i] = A[i][i - 1]
        if i < m - 1:
            c[i] = A[i][i + 1]

    # a = [0, ..., 0]
    # b = [1, ..., 1]
    # c = [0, ..., 0]
    a = [0] + a + [0]
    b = [1] + b + [1]
    c = [0] + c + [0]

    # print("Верхняя диагональ: ", c)
    # print("Средняя диагональ: ", b)
    # print("Нижняя диагональ: ", a)

    alpha.append(-c[0] / b[0])
    beta.append(f[0] / b[0])

    n = m + 2

    for i in range(2, n):
        alpha.append(-c[i-1] / (a[i-1] * alpha[i - 1] + b[i-1]))
        beta.append((f[i-1] - a[i-1] * beta[i - 1]) / (a[i-1] * alpha[i - 1] + b[i-1]))

    # print("alpha: ", alpha)
    # print("beta: ", beta)

    x[n-1] = ((f[n-1] - a[n-1]*beta[n-1])/(b[n-1] + a[n-1]*alpha[n-1]))

    for i in range(n-2, -1, -1):
        x[i] = (alpha[i + 1] * x[i+1] + beta[i + 1])

    return x


def calculate_errors(x_act, x_pr):
    """

    :param x_act: x из равномерной сетки
    :param y_pr: y из прогонки
    :return:
    """
    # u = sin(3*x)
    max_error = -1

    for i in range(len(x_act)):
        u = sin(3*x_act[i])
        max_error = max(max_error, abs(abs(u) - abs(x_pr[i])))

    return max_error


# test #1 n = 5

# A, f, xs = create_system(1000)
#
# print("A: ")
# for i in range(len(A)):
#     print(A[i])
#
# print("f: ", f)
#
# x = progonka(A, f)
# print("равномерные узлы: ", xs)
# print("Решение: ", x)
#
# error = calculate_errors(xs, x)
# print("error: {:.20f}".format(error))

N = [5, 10, 20, 100, 200, 500, 1000]
colors = [(0.92, 0.75, 0.83), (0.75, 0.92, 0.75), (0.98, 0.66, 0.66), (0.79, 0.75, 0.92),
          (0.75, 0.8, 0.92),  (0.55, 0.8, 0.94), (0.75, 0.92, 0.87), (0.93, 0.74, 0.85)]

for n in N:
     A, f, xs = create_system(n)
     y = progonka(A, f)  # знаяения прогонки

     error = calculate_errors(xs, y)

     print("final error for n = {}: {:.20f} (h^2 = {:.20f})".format(n, error, (3.1415926535 / n)**2))

     u = [sin(3*i) for i in xs]
     plt.plot(xs, u, color=colors[N.index(n)], label="n = " + str(n))
     plt.plot(xs, y, color=colors[N.index(n)], linestyle = "--")

plt.title("Погрешность при порядке n (u -, y --)")
plt.ylabel("y, u")
plt.xlabel("x")
plt.legend()
plt.grid()
plt.show()
