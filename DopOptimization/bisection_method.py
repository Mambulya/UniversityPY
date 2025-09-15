"""
Метод биссекции (дихотомии)

f(x) = (x-3)^2, 0 <= x <= 10, X0 = 0
"""
import numpy as np
import matplotlib.pyplot as plt


# def test_iterations(xs, method):
#     """
#     Тест на сходимость
#     """
#     # |Xk+1 - Xk-1|
#     if method == 3:  # метод Ньютона
#         p = 2
#     else:  # метод бисекции или секущих
#         p = 1
#
#     for k in range(1, len(xs) - 1):
#         E_prev = abs(xs[k] - xs[k - 1])
#         E_next = abs(xs[k + 1] - xs[k])
#
#         print(f"C = {E_next / (E_prev ** p)}")
#
#     # |Ek| ≈ CE(k-1)^p
#     # C ≈ Ek/E(k-1)^p


def plot_iterations(f, ys, zs, a, b, err, iter):
    x_vals = np.linspace(a - 1, b + 1, 500)
    y_vals = f(x_vals)

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label="f(x)", color="#5fd2dc")
    plt.axhline(0, color="#536364", linestyle="--")
    plt.plot(ys, [f(x) for x in ys], 'o', label=f"Yi", color="#667fd0")
    plt.plot(zs, [f(x) for x in zs], 'o', label=f"Zi", color="#e69138")
    plt.title(f"Метод дихотомии при e = {err}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.xlim([a - 1, b + 1])
    plt.grid(True)
    # зазумить
    # plt.xlim([-2.25, -0.75])
    # plt.ylim([-10, 2])
    plt.legend()
    plt.show()


def bisection_method(f, A, B, E, plot=False, test=False,):
    xs = []  # список итераций

    a = A  # start
    b = B  # end
    e = E  # error
    l = 2*e # погрешность L
    ys = [] # точки Yk
    zs = [] # точки Zk
    iteration = 0

    print("Промежуточные итерации:")

    while abs(b - a) > l:
        iteration += 1
        y = (a + b - e) / 2
        z = (a + b + e) / 2

        fy = f(y)
        fz = f(z)

        ys.append(y)
        zs.append(z)

        print(f"{iteration}) a={a} b={b} y{iteration}={y} z{iteration}={z} L={abs(b-a)}")

        if fy <= fz:
            b = z
            L = abs(b - a)
            if L <= l:
                x_root = (a + b) / 2
        else:
            a = y
    try:
        if plot:
            plot_iterations(f, ys, zs, a=A, b=B, err=e, iter=iteration)
        return x_root, iteration
    except Exception:
        return "метод не сошелся"

if __name__ == "__main__":

    def func(x):   # искомая функция
        return (x-3)*(x-3)

    print(bisection_method(f=func, A=0, B=10, E=0.1, plot=True))
