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
    # f_actual = []
    # f_pr = []
    max_error = -1

    for i in range(len(x_act)):
        f1 = sin(3*x_act[i])
        max_error = max(max_error, abs(abs(f1) - abs(x_pr[i])))

        # f_actual.append(f1)
        # f_pr.append(f2)

    return max_error#, f_actual, f_pr





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


# all_f_act = []
# all_f_pr = []
# xs_real = []
# x_app = []
N = [5, 10, 20, 50, 100, 200, 500, 1000]

for n in N:
     A, f, xs = create_system(n)
     x = progonka(A, f)  # корни прогонки

     #error, f_real, f_pr = calculate_errors(xs, x)
     error = calculate_errors(xs, x)

     # all_f_act.append(f_real)
     # all_f_pr.append(f_pr)


     print("final error for n = {}: {:.20f} (h^2 = {:.20f})".format(n, error, (3.1415926535 / n)**2))

     print("final error for n = {}: {:.20f}".format(len(A) + 1, calculate_errors(A, f, x)))
