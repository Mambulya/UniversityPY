"""
метод Ньютона
c одной производной
f(x) = (x-3)^2, 0 <= x <= 10, X0 = 0
f(x) -> min
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_iterations(f, xs, a, b, err, iter):
    x_vals = np.linspace(a - 1, b + 1, 500)
    y_vals = f(x_vals)

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label="f(x)", color="#5fd2dc")
    plt.axhline(0, color="#536364", linestyle="--")
    plt.plot(xs, [f(x) for x in xs], 'o', label=f"{iter}  итераций", color="#667fd0")
    plt.title(f"метод Ньютона при e = {err}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.xlim([a-1, b+1])
    plt.grid(True)
    # зазумить
    # plt.xlim([-2.25, -0.75])
    # plt.ylim([-10, 2])
    plt.legend()
    plt.show()


def Newton_method(f, A, E, max_iter, df, plot=True):
    a = A  # x0
    e = E
    operations_limit = max_iter
    x = a
    dfx = df(f=f, x=x)      # первая производная
    iteration = 0
    xs = [x]

    print("Промежуточные результаты:")

    while abs(dfx) > e and iteration < operations_limit:
        try:
            if dfx == 0:
                return None
            x_new = x - f(x) / dfx
            print(f"X{iteration}={x}, X{iteration+1}={x_new}  dfx={dfx} f={f(x)}")
        except ZeroDivisionError:
            return None
        xs.append(x_new)
        if abs(x_new - x) < e:
            x = x_new
            break
        x = x_new
        dfx = df(f=f, x=x)
        iteration += 1

    if plot:
        plot_iterations(f, xs, a=A-1, b=x + 1, err=e, iter=iteration)

    return x, iteration

if __name__ == "__main__":

    def func(x):   # искомая функция
        return (x-3)*(x-3)

    def df_func(f, x, h=0.001): # производня функции
        return (f(x) - f(x-h)) / h

    print(Newton_method(f=func, A=0, E=0.1, df=df_func,max_iter=10, plot=True))