from linearSystem import create_system
from Progonka import calculate_errors
import matplotlib.pyplot as plt
import numpy as np
"""
решения СЛАУ методом релаксации
"""

def relaxation(A, f, w = 1, tol = 0.000001, x0:list = None, maxiter = None):
    """
    При ω = 1 метод переходит в метод Зейделя.
    :param A:   матрица СЛАУ
    :param f:   вектор b
    :param w:   релаксационный параметр
    :param tol: допускаемая погрешность
    :param x0:  начальное приближение
    :param maxiter: максимальное количство операций
    :return:
    """

    n = len(f)

    if x0 == None:
        x0 = np.zeros_like(f)

    if maxiter == None:
        maxiter = 10000

    for iteration in range(maxiter):
        x_old = x0.copy()

        for i in range(n):
            row_sum = np.dot(A[i, :i], x0[:i]) + np.dot(A[i, i+1:], x0[i+1:])
            x0[i] = (1 - w) * x_old[i] + w * (f[i] - row_sum) / A[i, i]

        if np.linalg.norm(x0 - x_old) < tol:
            return x0, iteration

    print("Достигнуто максимальное количество операций")
    return x0, iteration


if __name__ == "__main__":
    n = 20
    Ws = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    iters = []
    errors = []


    for omega in Ws:
        A, f, xs = create_system(n)

        A = np.array(A)
        f = np.array(f[1:-1])

        result, niter = relaxation(A, f, w=omega)
        ERRORi = calculate_errors(xs[1:-1], result)
        iters.append(niter)
        errors.append(ERRORi)

    # график скорости сходимости метода релаксации от параметра w
    plt.plot(Ws, iters, color = "red")
    plt.title("Сходимость SOR при Wi")
    plt.ylabel("Количкство итераций")
    plt.xlabel("Релаксацонный параметр w")
    plt.grid()
    plt.show()
    
    # график погрешности при разных омега
    plt.plot(Ws, errors, color = "blue")
    plt.title("Погрешность SOR при Wi")
    plt.ylabel("Погреншность")
    plt.xlabel("Релаксацонный параметр w")
    plt.grid()
    plt.show()
