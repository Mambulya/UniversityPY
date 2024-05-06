from linearSystem import create_system
from Progonka import calculate_errors
import matplotlib.pyplot as plt
import numpy as np

"""
МЕТОД НАИСКОРЕЙШЕГО СПУСКА
"""

def Spusk(A, f, tol = 0.000001, x0:list = None, maxiter = None):
    """

    :param A:   матрица СЛАУ
    :param f:   вектор b
    :param tol: критерий точности
    :param x0: начальное приближение к x
    :param maxiter: максимальное число итераций (итерации выполняются
    пока не выполнено условие ∥x**(k+1) − x**k∥∞ <= tol
    :return: X0 - корни
    """
    n = len(f)

    if maxiter == None:
        maxiter = 10 * n

    if x0 == None:
        x0 = [0] * n    # начальное приближение

    r = [0]*n

    # calculating r0
    for i in range(n):
        for j in range(n):
            r[i] += A[i][j] * x0[j]
        r[i] -= f[i]

    A = np.array(A)
    r = np.array(r)

    #calculationg T1
    T = np.dot(r, r) / np.dot(A @ r, r)


    for iteration in range(maxiter):
        r_new = [0] * n

        x_new = [0] * n
        for i in range(n):
            x_new[i] = x0[i] - T * r[i]

        if max(abs(x_new[i] - x0[i]) for i in range(n)) < tol:  # норма соседних итераций
            return x_new

        x0 = x_new

        # calculating rk
        for i in range(n):
            for j in range(n):
                r_new[i] += A[i][j] * x0[j]
            r_new[i] -= f[i]

        r = r_new
        T = np.dot(r, r) / np.dot(A @ r, r)

    return x0

# TEST n = 5
# A, f, xs = create_system(5)
# f = f[1:-1]
#
# print(Spusk(A, f))
errors = []

if __name__ == "__main__":
    N = [5, 10, 20, 100, 200]

    for n in N:
         A, f, xs = create_system(n)
         f = f[1:-1]
         y = Spusk(A, f)  # знаяения прогонки
         error = calculate_errors(xs[1:-1], y)
         errors.append(error)

         print("final error for n = {}: {:.20f}".format(n, error))

    plt.plot(N, errors, color="red", label = "ε")

    plt.title("Погрешность при различных n")
    plt.ylabel("e")
    plt.xlabel("n")
    plt.legend()
    plt.grid()
    plt.show()
