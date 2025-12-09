"""
РЕАЛИЗАЦИЯ МЕТОДА ПОТЕНЦИАЛОВ
ДЛЯ НАХОЖДЕНИЯ ОПТИМАЛЬНОГО ПЛАНА
ТРАНСПОРТНОЙ ЗАДАЧИ 3*3

"""

import numpy as np
from double_pref import double_pref, C, A, B, X, n, m

def potential(C, X):
    """
    Метод потенциалов для задачи 3x3
    C - матрица стоимости
    X0 - опроный план
    """

    X = X.copy()
    k = 0

    while True:
        k += 1
        print("             ШАГ  №", k)
        # потенциалы u, v
        u = np.full(n, np.nan)
        v = np.full(m, np.nan)
        u[0] = 0   # первый потенциал

        changed = True
        while changed:
            changed = False
            for i in range(n):
                for j in range(m):
                    if X[i, j] > 0:  # базисая клетка
                        if np.isnan(u[i]) and not np.isnan(v[j]):
                            u[i] = C[i, j] - v[j]
                            changed = True
                        elif not np.isnan(u[i]) and np.isnan(v[j]):
                            v[j] = C[i, j] - u[i]
                            changed = True

        # # если какие-то потенциалы не найдены
        # if np.any(np.isnan(u)) or np.any(np.isnan(v)):
        #     # добавляем маленький базис
        #     for i in range(n):
        #         for j in range(m):
        #             if X[i, j] == 0:
        #                 X[i, j] = 0.000000001
        #                 break
        #         else:
        #             continue
        #         break
        #     continue

        #  Δ(i,j) = (u+v) - C
        delta = (u.reshape(-1, 1) + v.reshape(1, -1)) - C

        # базисные клетки не рассматриваем
        delta[X > 0] = 0

        # проверка оптимальности (<= 0)
        max_delta = np.max(delta)
        if max_delta <= 0:
            print("Оптимальный план найден")
            return X

        # самая большая оценка
        max_val = -100000000000000
        i0 = j0 = 0

        for i in range(n):
            for j in range(m):
                if delta[i, j] > max_val:
                    max_val = delta[i, j]
                    i0, j0 = i, j

        # цикл (среди базисных клеток)
        # ищем вторую строку в столбце j0
        rows = [i for i in range(n) if X[i, j0] > 0 and i != i0]
        # ищем второй столбец в строке i0
        cols = [j for j in range(m) if X[i0, j] > 0 and j != j0]

        cycle = None
        for i1 in rows:
            for j1 in cols:
                if X[i1, j1] > 0:
                    cycle = [(i0, j0), (i1, j0), (i1, j1), (i0, j1)]
                    break
            if cycle:
                break

        if cycle is None:
            print("Не удалось построить цикл")
            return 0

        print(f"Цикл (1='+', 0='-'):")
        print(f"- начало в ({cycle[0][0]+1, cycle[0][1] + 1})")
        cycle_matrix = np.array([[np.nan, np.nan, np.nan],
                                [np.nan, np.nan, np.nan],
                                 [np.nan, np.nan, np.nan]])

        for k, (i, j) in enumerate(cycle):
            cycle_matrix[i][j] = delta[i][j] > 0
            #print(f"({i+1}, {j+1})", end="   ")
        print(cycle_matrix)

        # выбираем min(x) с theta < 0
        # цикл это всегда + - + - ...
        plus = []
        minus = []

        for k, cell in enumerate(cycle):
            if k % 2 == 0:
                plus.append(cell)
            else:
                minus.append(cell)

        # for k, (i, j) in enumerate(cycle):
        #     if delta[i][j] < 0:
        #         minus.append((i, j))
        #     elif delta[i][j] > 0:
        #         plus.append((i, j))

        theta = min([X[minus[m][0], minus[m][1]] for m in range(len(minus))])

        # отнять theta у -
        # прибавиь theta у +
        for i, j in plus:
            X[i, j] += theta
        for i, j in minus:
            X[i, j] -= theta

        # print_matrix("Новый план X", X)

        # # θ — минимальное из вычитаемых клеток
        # minus_nodes = [cycle[1], cycle[3]]
        # theta = min(X[i, j] for (i, j) in minus_nodes)
        #
        # # обнов план
        # for k, (i, j) in enumerate(cycle):
        #     if k % 2 == 0:   # +θ
        #         X[i, j] += theta
        #     else:           # -θ
        #         X[i, j] -= theta
        #
        # # удаляем нулевые
        # X[np.abs(X) < 1e-12] = 0
        #
        return X


if __name__=="__main__":
    X0, X_flag = double_pref(C, A, B)
    print("Опорный план с помощью метода двойного предпочтения:")
    print(X0)
    print("Суммарные затраты:")
    print(C*X0)
    print("==== на опорный план нужно", np.sum(C*X0), "д.ед. ==== ")


    print("\n\nМЕТОД ПОТЕНЦИАЛОВ (ОПТИМАЛЬНЫЙ ПЛАН)")
    X_opt = potential(C, X0)
    print("оптимальный план:")
    print(X_opt)
    print("Суммарные затраты:")
    print(X_opt * C)
    print("==== на оптимальный план нужно", np.sum(X_opt * C))
