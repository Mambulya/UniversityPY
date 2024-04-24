from linearSystem import create_system
from Progonka import calculate_errors
import matplotlib.pyplot as plt

"""
Решение системы методом Якоби
"""


def yakobi(A, f, tol = 0.000001, x0 = 0, maxiter = None):
    """

    :param A:   матрица СЛАУ
    :param f:   вектор b
    :param tol: критерий точности
    :param x0: начальное приближение к x
    :param maxiter: максимальное число итераций (итерации выполняются
    пока не выполнено условие ∥x**(k+1) − x**k∥∞ <= tol
    :return: X0 - корни, iteration - сколько итераций потребовалось, r -  вектор норм невязок на итерациях
    """
    n = len(f)

    if maxiter == None:
        maxiter = 10 * n

    X0 = [x0] * n   # начальное приближение
    r = []  # вектор норм невязок на итерациях, т. е. r(k) = ∥rk∥∞

    for iteration in range(maxiter):
        x_new = [0] * n
        for i in range(n):
            x_new[i] = (f[i] - sum(A[i][j] * X0[j] for j in range(n) if j != i)) / A[i][i]
        r.append(max(abs(f[i] - sum(A[i][j] * x_new[j] for j in range(n))) for i in range(n)))  # отклонение на каждой итерации
        if max(abs(x_new[i] - X0[i]) for i in range(n)) < tol:  # норма соседних итераций
            return x_new, iteration, r
        X0 = x_new

    return X0, iteration, r


# TEST
# n = 5
# A, f, xs = create_system(5)
#
# result, niter, r = yakobi(A, f[1:-1])
# print(calculate_errors(xs[1:-1], result))
# draw_error_n(range(niter+1), r)

if __name__ == "__main__":
    colours = ["#edd1d1", "#edbebe", "#eda4a4", "#ed8787", "#ed6666", "#ed4c4c", "#ed2d2d", "#f00505"]
    n = [5, 10, 20, 50, 100, 200]

    # график погрешностей и необходимых итераций
    for i in range(len(n)):
        A, f, xs = create_system(n[i])

        result, niter, r = yakobi(A, f[1:-1])
        print("погрешность при n = " + str(n[i]) + ": ", calculate_errors(xs[1:-1], result))

        plt.plot(range(niter+1), r, color=colours[i], label = "n = " + str(n[i]))

    plt.ylim(0, 0.2)
    plt.title("Погрешность при порядке n")
    plt.ylabel("погрешность на i итерации")
    plt.xlabel("итерация i")
    plt.legend()
    plt.grid()
    plt.show()
    
# погрешности при
# n = 5:    0.32537025465931224
# n = 10:   0.0722228001628562
# n = 20:   0.017928882788322387
# n = 50:   0.005980879605362643
# n = 100:  0.013008721989205885
# n = 200:  0.09984828772332521
# n = 500:  0.3930047945530395
