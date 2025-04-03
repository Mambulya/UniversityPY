
"""
метод биссекции
метод секущих (хорд)
метод Ньютона
"""

def black_box(f, method, **parametrs):
    """
    Метод биссекции
    Метод секущих
    Метод Ньютона
    для нахождения корня в нелинейном уравнении f(x)=0


    Метод Ньютона быстро сходится (имеет квадратичную сходимость)
    и допускает различные модификации, приспосоления для решения
    векторных задач и сеточных уравнений. Однако этот метод
    эффективен при весьма жестких ограничениях на характер функции f(x)
    """
    if method == "метод биссекции":
        a = parametrs["a"]
        b = parametrs["b"]
        e = parametrs["e"]    # погрешность x*

        fa = f(a)
        fb = f(b)
        c = (a+b) / 2
        fc = f(c)

        while (b-a) > e:
            if fa * fc < 0:
                b = c
            elif fb * fc < 0:
                a = c

            c = (a+b) / 2

        res = (a + b) / 2
        return res

    elif method == "метод секущих":
        a = parametrs["a"]
        b = parametrs["b"]
        e = parametrs["e"]    # погрешность x*
        operations_limit = parametrs["iter"]

        iteration = 0
        while abs(b - a) > e and iteration < operations_limit:
            c = b - f(b) * (b - a) / (f(b) - f(a))
            a = b
            b = c

            iteration += 1

        if abs(b - a) <= e:
            return b
        else:
            return None  # Метод не сошелся


    elif method == "метод Ньютона":
        a = parametrs["a"]
        df = parametrs["df"]
        e = parametrs["e"]
        operations_limit = parametrs["iter"]

        x = a
        iteration = 0
        while abs(f(x)) > e and iteration < operations_limit:
            try:
                x_new = x - f(x) / df(x)
            except ZeroDivisionError:
                print("Ошибка: Производная равна нулю. Метод Ньютона не может продолжиться")
                return None

            if abs(x_new - x) < e:
                return x_new

            x = x_new
            iteration += 1

        if abs(f(x)) <= e:
            return x
        else:
            print(f"Метод Ньютона не сошелся после {operations_limit} итераций")
            return None

    else:
        return "Неверный метод"

if __name__ == "__main__":

    def f(x):
        return x*x*x - x + 1


    def func(x):
        return x ** 2 - 2

    def df(x):
        return 2*x

    # тесты
    print("Метод биссекции:")
    print(black_box(f, method="метод биссекции", a=-2, b=-1, e= 0.0005))
    print(black_box(f, method="метод биссекции", b=-1, e=0.02, a=-2))
    print(black_box(f, method="метод биссекции", b=-1, a=-2, e=0.01, e2=0.0001))
    print("Метод секущих:")
    print(black_box(func, method="метод секущих", a=1, b=2, e=0.000001, iter=1000))
    print(black_box(f, method="метод секущих", b=-1, a=-2, e=0.01, e2=0.0001, iter=1000))
    print("Метод Ньютона")
    print(black_box(func, method="метод Ньютона", a=1, e=0.00001, iter=1000, df=df))
    print(black_box(func, method="метод Ньютона", a=1, e=0.01, iter=1000, df=df))
    print(black_box(func, method="метод Ньютона", a=-100, e=0.00001, iter=1000, df=df))
