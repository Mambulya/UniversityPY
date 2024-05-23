import numpy as np
from math import e
import matplotlib.pyplot as plt

def runge_kutta(f:list, y0:list, a:int, b:int, h = 0.1, exact=False):
    """
    Метод Рунге-Кутты 4-го порядка для системы дифференциальных уравнений

    f: функция f(t, y) для dy/dt = f(t, y), где y - вектор
    y0: начальные значения y (вектор)
    a: начальное значение времени
    b: конечное значение времени
    h: шаг интегрирования
    """
    n = int((b - a) / h)
    t_values = np.linspace(a, b, n + 1)
    y_values = np.zeros((n + 1, len(y0)))

    y_values[0] = y0

    for i in range(n):
        t = t_values[i]
        y = y_values[i]

        k1 = f(t, y)
        k2 = f(t + h / 4, y + h / 4 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k1 - 2 * h * k2 + 2 * h * k3)

        y_values[i + 1] = y + h * (k1 + 4 * k3 + k4) / 6

    if exact:   # известно точное решение и можно подсчитать погрешность
        e1 = abs(abs(y_values[i, 0]) - e**(-t))
        e2 = abs(abs(y_values[i, 1]) - e**(-t))
        error = max(e1, e2)     # финальная погрешность

        return t_values, y_values, error

    return t_values, y_values


def system(t, y):
    alpha = 2
    beta = 3
    y1, y2 = y

    dy1_dt = -alpha * y1 - beta * y2 + (alpha + beta - 1) * np.exp(-t)
    dy2_dt = beta * y1 - alpha * y2 + (alpha + beta - 1) * np.exp(-t)

    return np.array([dy1_dt, dy2_dt])

if __name__ == "__main__":
    # Начальные условия
    y0 = [1, 1]
    a = 0
    b = 4

    # Решаем систему
    t_values, y_values, max_error = runge_kutta(system, y0, a, b, h=0.1, exact=True)

    y1_values = y_values[:, 0]
    y2_values = y_values[:, 1]

    # Точное решение
    exact_solution = np.exp(-t_values)


    # график решений
    plt.plot(t_values, y1_values, label='Численное решение y1(t)', color = "#ff5c77")
    plt.plot(t_values, y2_values, label='Численное решение y2(t)', color = "#ffbf00")
    plt.plot(t_values, exact_solution, label='Точное решение e^{-t}', linestyle='dashed', color = "#98c793")
    plt.xlabel('t')
    plt.ylabel('y')
    plt.legend()
    plt.title('Решения системы')
    plt.grid(True)
    plt.show()

    #   Проверка точности
    print("Решения при h = 0.1:")
    for t, y1, y2, exact in zip(t_values, y1_values, y2_values, exact_solution):
        print(f"t = {t:.2f}, y1 = {y1:.4f}, y2 = {y2:.4f}, точное решение = {exact:.4f}")
    print("--------- final error: {} ---------".format(max_error))



    # погрешности
    ERRORS = []
    hs = [0.01, 0.03, 0.07, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    for h in hs:
        _, _, ERROR = runge_kutta(system, y0, a, b, h=h, exact=True)
        ERRORS.append(ERROR)

    # график погрешности
    plt.plot(hs, ERRORS, label = "e = e(h)")
    plt.xlabel('h')
    plt.ylabel('e')
    plt.legend()
    plt.title('Зависимость погрешности от шага')
    plt.grid(True)
    plt.show()
