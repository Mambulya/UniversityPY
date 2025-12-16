"""
РЕАЛИЗАЦИЯ МЕТОДА ПОТЕНЦИАЛОВ
ДЛЯ НАХОЖДЕНИЯ ОПТИМАЛЬНОГО ПЛАНА
ТРАНСПОРТНОЙ ЗАДАЧИ 3*3

опорный план был получен через метод северо-западного угла
реализация цикла с использованием идеи рекурсивного поиска
"""

import numpy as np
from north_west_angle import north_west_angle, C, A, B, X, n, m


def calculate_baise(X):
    """считает сколько базисных клеток"""
    baise = 0
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i][j] > 0:
                baise += 1
    return baise


def find_cycle_new(X, start_i, start_j, matrix_baise):
    """
    для поиска цикла на основе
    """

    # Временная матрица для поиска (1 - базисная клетка, -1 - стартовая клетка)
    temp_mat = matrix_baise.copy()
    temp_mat[start_i, start_j] = -1  # Помечаем стартовую клетку

    # Глобальная переменная для остановки поиска
    global FLAG_END
    FLAG_END = False

    # Вспомогательная функция для поиска цикла
    def dfs(pos, path, dir_row=True):
        """Рекурсивный поиск цикла
        pos - клетка
        dir_row - двигаться по строке (соседи)
        path - траектория цикла
        """
        global FLAG_END

        ii, jj = pos

        # Собираем соседей по строке или столбцу
        if dir_row:
            # Соседи по определенной строке
            neighbors = [(ii, k) for k in range(X.shape[1])
                         if k != jj and (temp_mat[ii, k] == 1 or (ii, k) == (start_i, start_j))]
        else:
            # Соседи по столбцу
            neighbors = [(k, jj) for k in range(X.shape[0])
                         if k != ii and (temp_mat[k, jj] == 1 or (k, jj) == (start_i, start_j))]

        # Если есть соседи
        if neighbors:
            # вернулись ли мы в стартовую клетку
            if (start_i, start_j) in neighbors and len(path) > 0:
                FLAG_END = True
                return path

            # Меняем направление и продолжаем поиск
            dir_row = not dir_row
            for neighbor in neighbors:

                if neighbor not in path:
                    path.append(neighbor)
                    result = dfs(neighbor, dir_row, path)

                    if FLAG_END:
                        return result
                    else:
                        # Удаляем клетку из пути, если не нашли цикл
                        path.pop()

        return path

    # Запускаем поиск
    cycle_cells = dfs((start_i, start_j), True, [(start_i, start_j)])

    # Если нашли цикл
    if FLAG_END and len(cycle_cells) > 1:
        # Добавляем знаки + и - (чередование)
        cycle_with_signs = []
        for k, (i, j) in enumerate(cycle_cells):
            sign = '+' if k % 2 == 0 else '-'
            cycle_with_signs.append((i, j, sign))

        return cycle_with_signs

    return None


def find_cycle_improved(X, start_i, start_j, matrix_baise):
    """
    Улучшенная версия поиска цикла с несколькими попытками
    """
    # Сначала пробуем найти прямоугольный цикл (для 3x3 обычно достаточно)
    # cycle = find_cycle_rectangular(X, start_i, start_j, matrix_baise)
    # if cycle:
    #     return cycle

    # Если не нашли, пробуем рекурсивный метод
    cycle = find_cycle_new(X, start_i, start_j, matrix_baise)
    if cycle:
        return cycle

    return None


def find_cycle_rectangular(X, start_i, start_j, matrix_baise):
    """
    Поиск простого прямоугольного цикла для матрицы 3x3
    """
    n_rows, n_cols = X.shape

    # Ищем клетки в той же строке, что и стартовая
    row_cells = []
    for j in range(n_cols):
        if j != start_j and matrix_baise[start_i, j] == 1:
            row_cells.append((start_i, j))

    # Ищем клетки в том же столбце, что и стартовая
    col_cells = []
    for i in range(n_rows):
        if i != start_i and matrix_baise[i, start_j] == 1:
            col_cells.append((i, start_j))

    # Пробуем найти прямоугольник
    for ri, rj in row_cells:
        for ci, cj in col_cells:
            # Проверяем, есть ли связь между (ci, rj) или (ri, cj)
            if matrix_baise[ci, rj] == 1:
                # Цикл через (ci, rj)
                return [
                    (start_i, start_j, '+'),
                    (start_i, rj, '-'),
                    (ci, rj, '+'),
                    (ci, start_j, '-')
                ]
            elif matrix_baise[ri, cj] == 1:
                # Цикл через (ri, cj)
                return [
                    (start_i, start_j, '+'),
                    (ci, start_j, '-'),
                    (ci, cj, '+'),
                    (start_i, cj, '-')
                ]

    return None


def potential(C, X):
    """
    Метод потенциалов для задачи 3x3 с новой функцией поиска цикла
    C - матрица стоимости
    X0 - опорный план
    """

    # для поиска цикла
    global FLAG_END

    X = X.copy()
    iteration = 0
    n_rows = X.shape[0]
    n_cols = X.shape[1]

    while iteration <= 100:
        iteration += 1
        print(f"                  ШАГ {iteration}")

        # Матрица базисных клеток
        matrix_baise = np.array([[0, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]], dtype=int)
        matrix_baise[X > 0] = 1

        print("Текущий план:")
        print(X)
        print("Базисные клетки:")
        print(matrix_baise)

        # Потенциалы u, v
        u = np.full(n_rows, np.nan)
        v = np.full(n_cols, np.nan)
        u[0] = 0  # первый потенциал

        # Если план вырожденный, добавляем фиктивные базисные клетки
        baise_count = calculate_baise(X)
        if baise_count < (n_rows + n_cols - 1):
            #print(f"Вырожденный план: {baise_count} базисных клеток, нужно {n_rows + n_cols - 1}")

            # фиктивные базисные клетки
            for i in range(n_rows):
                for j in range(n_cols):
                    if matrix_baise[i, j] == 0:
                        matrix_baise[i, j] = 1
                        baise_count += 1

                        if baise_count == n_rows + n_cols - 1:
                            break
                if baise_count == n_rows + n_cols - 1:
                    break

        # Вычисление потенциалов
        changed = True
        while changed:
            changed = False
            for i in range(n_rows):
                for j in range(n_cols):
                    if matrix_baise[i, j] == 1:  # Базисная клетка
                        if np.isnan(u[i]) and not np.isnan(v[j]):
                            u[i] = C[i, j] - v[j]
                            changed = True
                        elif not np.isnan(u[i]) and np.isnan(v[j]):
                            v[j] = C[i, j] - u[i]
                            changed = True

        if np.isnan(u).any() or np.isnan(v).any():
            # Потенциалы не определены полностью -> опт план найден
            return X

        print("Потенциалы поставщиков U:", u)
        print("Потенциалы потребителей V:", v)

        # Вычисление оценок Δ(i,j) = u[i] + v[j] - C[i,j]
        delta = (u.reshape(-1, 1) + v.reshape(1, -1)) - C
        delta[matrix_baise == 1] = np.nan  # Базисные клетки не рассматриваем для оценок

        print("Оценки Δ для небазисных клеток:")
        print(delta)

        # проверка оптимальности (Δ <= 0)
        max_delta = np.nanmax(delta)
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

        # построение цикла
        cycle = find_cycle_improved(X, i0, j0, matrix_baise)
        #print(cycle)
        if cycle is None:
            print("Не удалось найти цикл!")
            return X

        print(f"Цикл: (максимальная + оценка)")
        print(f"- начало в ({cycle[0][0] + 1, cycle[0][1] + 1})")
        for i in range(n_rows):
            for j in range(n_cols):
                cell_display = " 0 "
                for ci, cj, csign in cycle:
                    if ci == i and cj == j:
                        cell_display = f" {csign} "
                        break
                print(cell_display, end="")
            print()

        # выбираем min(x) с theta < 0
        # цикл это всегда + - + - ...
        # выбираем min(x) с theta < 0
        # цикл это всегда + - + - ...
        plus = []
        minus = []

        for k, cell in enumerate(cycle):
            if k % 2 == 0:
                plus.append(cell)
            else:
                minus.append(cell)

        theta = [X[i, j] for i, j, sign in minus if X[i, j] > 0]
        if not theta:
            print("Вырожденность — остановка")
            return X

        theta = min(theta)
        print(f"theta={theta} - минимальный x среди отрицательных оценок")

        # отнять theta у -
        # прибавиь theta у +
        for i, j, sign in plus:
            X[i, j] += theta
        for i, j, sign in minus:
            X[i, j] -= theta


        # Проверяем, сколько клеток стали нулевыми
        new_zero_cells = []
        for i, j, sign in cycle:
            if sign == '-' and X[i, j] == 0:
                new_zero_cells.append((i, j))

        # Если несколько клеток стали нулевыми, оставляем только одну как базисную
        if len(new_zero_cells) > 1:
            print(f"Несколько клеток стали нулевыми: {new_zero_cells}")
            print("Оставляем одну как базисную, остальные становятся свободными")

        print(f"Новый план:")
        print(X)
    return X


if __name__ == "__main__":
    X0 = north_west_angle(A, B, X)
    print("Опорный план с помощью СЗ угла:")
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
    print("====> на оптимальный план нужно", np.sum(X_opt * C))
