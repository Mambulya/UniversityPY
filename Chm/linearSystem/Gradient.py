from linearSystem import create_system
from Progonka import calculate_errors
import matplotlib.pyplot as plt
import numpy as np

"""
МЕТОД СОПРЯЖЕННЫХ ГРАДИЕНТОВ
"""

def Gradient(A, b, tol = 0.000001, it_max = None):
    n = len(b)

    if it_max == None:
        it_max = 10 * n

    it = 0
    x = 0
    r = np.copy(b)
    r_prev = np.copy(b)
    rho = np.dot(r, r)
    p = np.copy(r)
    
    while (np.sqrt(rho) > tol*np.sqrt(np.dot(b, b)) and it < it_max):
        it += 1
        if it == 1:
            p[:] = r[:]
        else:
            beta = np.dot(r, r)/np.dot(r_prev, r_prev)
            p = r + beta*p
            w = np.dot(A, p)
            alpha = np.dot(r, r)/np.dot(p, w)
            x = x + alpha*p
            r_prev[:] = r[:]
            r = r - alpha*w
            rho = np.dot(r, r)

    return x


# TEST n = 5
# A, f, xs = create_system(5)
# f = f[1:-1]
#
# print(Gradient(A, f))
errors = []

if __name__ == "__main__":
    N = [5, 10, 20, 100, 200]

    for n in N:
         A, f, xs = create_system(n)
         f = f[1:-1]
         y = Gradient(A, f)  # знаяения прогонки
         error = calculate_errors(xs[1:-1], y)
         errors.append(error)

         print("final error for n = {}: {:.20f}".format(n, error))

    plt.plot(N, errors, color="blue", label = "ε")

    plt.title("Погрешность при различных n")
    plt.ylabel("e")
    plt.xlabel("n")
    plt.legend()
    plt.grid()
    plt.show()
