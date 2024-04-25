from linearSystem import create_system
from Progonka import calculate_errors
import matplotlib.pyplot as plt
from Yakobi import yakobi
"""
решения СЛАУ методом Зейделя
Так как в иходной матрице An x n преобладают диагональные элементы, то итерационный процесс сходится,
сходится лучше, чем метод Якоби
"""


def Seidel(A, f, tol = 0.000001, x0 = None, maxiter = None):
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

    if x0 == None:
        x0 = [0] * n    # начальное приближение

    r = []  # вектор норм невязок на итерациях, т. е. r(k) = ∥rk∥∞

    for iteration in range(maxiter):
        x_new = [0] * n
        for i in range(n):
            x_new[i] = (f[i] - sum(A[i][j] * x_new[j] for j in range(n)) - sum(A[i][j] * x0[j] for j in range(i + 1, n))) / A[i][i]
        r.append(max(abs(f[i] - sum(A[i][j] * x_new[j] for j in range(n))) for i in range(n)))  # отклонение на каждой итерации
        if max(abs(x_new[i] - x0[i]) for i in range(n)) < tol:  # норма соседних итераций
            return x_new, iteration, r
        x0 = x_new
    print("достигнуто максимальное число операций")
    return x0, iteration, r


# n = 5
# A, f, xs = create_system(5)
#
# result, niter, r = Seidel(A, f[1:-1])
# print(calculate_errors(xs[1:-1], result))

if __name__ == "__main__":
    colours = ["#edd1d1", "#edbebe", "#eda4a4", "#ed8787", "#ed6666", "#ed4c4c", "#ed2d2d", "#f00505"]
    coloursBLUE = ["#b8c7de", "#a0b9de", "#82a8e0", "#6596e0", "#4382e0",  "#2772e3", "#1267e5", "#0651c2"]
    n = [5, 10, 20, 50, 100]
    iterationsSeidel = []
    iterationsYakobi = []

    # график погрешностей и необходимых итераций
    for i in range(len(n)):
        A, f, xs = create_system(n[i])

        result, niter, r = Seidel(A, f[1:-1])
        iterationsSeidel.append(niter)

        result1, niter1, r1 = yakobi(A, f[1:-1])
        iterationsYakobi.append(niter1)

        print("погрешность при n = " + str(n[i]) + ": ", calculate_errors(xs[1:-1], result))

        plt.plot(range(niter + 1), r, color=colours[i], label="n = " + str(n[i]))

    plt.ylim(0, 0.050)
    plt.title("Погрешность при порядке n")
    plt.ylabel("погрешность на i итерации")
    plt.xlabel("итерация i")
    plt.legend()
    plt.grid()
    plt.show()

    # сравнение операций в методе Якоби и Зейделя
    for i in range(len(n)):

        plt.plot(n, iterationsSeidel, color=colours[i], label="n = " + str(n[i]))
        plt.plot(n, iterationsYakobi, color = coloursBLUE[i], label ="n = " + str(n[i]))

    plt.title("Количество итераций при порядке n")
    plt.ylabel("Количкство итераций")
    plt.xlabel("n")
    plt.legend(["Seidel", "Yakobi"])
    plt.grid()
    plt.show()
