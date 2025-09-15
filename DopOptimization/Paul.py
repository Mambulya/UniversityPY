"""
6 вариант
метод Пауэлла
f(x) = (x-3)^2, 0 <= x <= 10, X0 = 0
f(x) -> min
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_iterations(f, xs, a, b, err, б, h, iter):
    x_vals = np.linspace(a - 1, b + 1, 500)
    y_vals = f(x_vals)

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label="f(x)", color="#5fd2dc")
    plt.axhline(0, color="#536364", linestyle="--")
    plt.plot(xs, [f(x) for x in xs], 'o', label=f"{iter}  итераций", color="#667fd0")
    plt.title(f"метод Пауэлла при e = {err}, б={б}, h={h}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.xlim([a-1, b+1])
    plt.grid(True)
    # зазумить
    #plt.xlim([2.98, 3.001])
    #plt.ylim([2.99, 3.0000000000000030])
    plt.legend()
    plt.show()


def Paul_method(f, A, E, б, dx, plot=True):
    iteration = 0
    xs = [A]
    x1 = A
    Fmin = 0
    x_new = E + 1
    Xmin = E + 2 + б

    print("Промежуточные результаты:")

    while abs(Fmin - f(x_new)) > E or abs(Xmin - x_new) > б:
        x2 = x1 + dx
        if f(x1) > f(x2):
            x3 = x1 + 2*dx
        else:
            x3 = x1 - dx
            x1, x2, x3, = sorted([x1, x2, x3])

        f1, f2, f3 = f(x1), f(x2), f(x3)
        Fmin = min(f1, f2, f3)

        if Fmin == f1:
            Xmin = x1
        elif Fmin == f2:
            Xmin = x2
        else:
            Xmin = x3

        # квадратичная аппроксимация
        try:
            a1 = (f(x2) - f(x1)) / (x2 - x1)
            a2 = (1/(x3 - x2)) * (((f3 - f1) / (x3 - x1)) - ((f2 - f1) / (x2 - x1)))

            x_new = ((x2 + x1) / 2) - (a1 / (2*a2))
            xs.append(x_new)

        except ZeroDivisionError:
            x_new = xs[-1]
            break

        print(f"{iteration}) x1={x1} x2={x2} x3={x3} a1={a1} a2={a2} x*={x_new} f(x*)={f(x_new)} Fmin={Fmin} Xmin={Xmin}")
        print(f"  |Fmin - f(x*)| = {abs(Fmin - f(x_new))}, |Xmin - x*| = {abs(Xmin - x_new)}")
        x1 = Xmin
        iteration += 1


    if plot:
        plot_iterations(f=f, xs=xs, a=A, b=x_new + 0.1, err=E, б=б, h=dx, iter=iteration)
    return x_new, iteration, xs


if __name__ == "__main__":

    def func(x):   # искомая функция
        return (x-3)*(x-3)

    б = 0.1
    dif_x = 0.1    # шаг
    x, iter, xs = Paul_method(f=func, A=0, E=0.1, б=0.1, dx=dif_x)
    print("\nКорень: ", x)
    print("Итерации: ", iter)
    print("Промежуточные x: ", xs)
