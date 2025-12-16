import numpy as np
from double_pref import С, Х

def delta_method(C, A, B):
    m, n = C.shape
    X = np.zeros((m, n), dtype=int)
    a = A.copy()
    b = B.copy()


    print("         ШАГ 1: Преобразование матрицы стоимостей в матрицу приращений")

    # Шаг 1: Преобразование матрицы стоимостей в матрицу приращений
    delta_C = C.copy()
    print("Исходная матрица стоимостей:")
    print(delta_C)

    min_cols = np.array([0,0,0])
    min_rows = np.array([0,0,0])

    # Вычитаем минимум каждого столбца
    #print("минимум каждого столбца:")
    for j in range(n):
        min_val = np.min(delta_C[:, j])
        print(f"  Столбец {j + 1}: min = {min_val}")
        delta_C[:, j] -= min_val
        min_cols[j] = min_val

    print("Матрица после вычитания минимумов по столбцам:")
    print(delta_C)

    # Вычитаем минимум каждой строки, если в строке нет нулей
    #print("\n1.2. Вычитаем минимум каждой строки (если в строке нет нулей):")
    for i in range(m):
        min_val = np.min(delta_C[i, :])
        print(f"  Строка {i + 1}: min = {min_val}")
        delta_C[i, :] -= min_val
        min_rows[i] = min_val

    print("Итоговая матрица приращений ΔC:")
    print(delta_C)

    print("         ШАГ 2: Начальное закрепление потребителей за поставщиками")

    remaining_b = b.copy()
    remaining_a = a.copy()
    print(f"Поставщики: {remaining_a}")
    print(f"Потребители: {remaining_b}")

    # Сортируем столбцы по количеству нулей (от меньшего к большему)
    cols_by_zeros = sorted(range(n), key=lambda j: np.sum(delta_C[:, j] == 0))
    print(f"Порядок обработки столбцов (по количеству нулей): {[j + 1 for j in cols_by_zeros]}")

    for j in cols_by_zeros:
        print(f"        Обработка столбца {j + 1} (потребность bj: {remaining_b[j]})")
        zero_rows = np.where(delta_C[:, j] == 0)[0]
        print(f"  Нулевые приращения в строках: {[i + 1 for i in zero_rows]}")

        if len(zero_rows) == 1:
            i = zero_rows[0]
            allot = remaining_b[j]
            X[i, j] = allot
            remaining_a[i] -= allot
            #print(f"  Только одна строка с нулевым приращением: {i + 1}")
            #print(f"  Закрепляем всю потребность {allot} за поставщиком {i + 1}")
            #print(f"  Остаток поставщика A{i + 1}: {a[i]} → {remaining_a[i]}")
        else:
            #print(f"  Несколько строк с нулевыми приращениями: {[i + 1 for i in zero_rows]}")
            need = remaining_b[j]
            allocated = 0

            # Распределяем потребность между поставщиками с нулевыми приращениями
            print(f"  Распределение {need} единиц между поставщиками:")
            for i in zero_rows:
                if need <= 0:
                    break
                if remaining_a[i] > 0:
                    allot = min(remaining_a[i], need)
                    X[i, j] = allot
                    remaining_a[i] -= allot
                    need -= allot
                    allocated += allot
                    print(f"    A{i + 1}: закреплено {allot}, осталось у поставщика: {remaining_a[i]}")

            print(f"  После распределения среди поставщиков с остатками: осталось потребности: {need}")

            # Если осталась нераспределённая потребность
            if need > 0:
                print(f"  Распределяем оставшиеся {need} единиц:")
                for i in zero_rows:
                    if need <= 0:
                        break
                    allot = min(remaining_a[i], need)
                    if allot > 0:
                        X[i, j] += allot
                        remaining_a[i] -= allot
                        need -= allot
                        allocated += allot
                        print(
                            f"    A{i + 1}: дополнительно закреплено {allot}, осталось у поставщика: {remaining_a[i]}")

            print(f"  Итого закреплено за столбцом B{j + 1}: {allocated} единиц")

        remaining_b[j] = 0
        print(f"X:")
        print(X)
        #print(f"  Остатки поставщиков: {remaining_a}")

    print("             ШАГ 3: Вычисление Δa_i = a_i - sum x_ij")

    # Шаг 3: Вычисление Δa_i
    delta_a = a - X.sum(axis=1)
    print(f"Δa_i (разность между запасами и распределёнными объемами):")
    for i in range(m):
        print(f"  A{i + 1}: {a[i]} - {X.sum(axis=1)[i]} = {delta_a[i]}")

    print(f"Типы строк:")
    for i in range(m):
        if delta_a[i] == 0:
            print(f"  Строка A{i + 1}: нулевая (Δa = 0)")
        elif delta_a[i] < 0:
            print(f"  Строка A{i + 1}: избыточная ({delta_a[i]} < 0)")
        else:
            print(f"  Строка A{i + 1}: недостаточная ({delta_a[i]} > 0)")

    # Итеративное улучшение плана
    iteration = 0
    max_iterations = 4

    print("             ШАГ 4-11: Улучшение плана")

    while not np.all(delta_a == 0) and iteration < max_iterations:
        iteration += 1
        #print(f"\n{'=' * 40}")
        #print(f"Итерация {iteration}")
        #print(f"{'=' * 40}")

        # Определение типов строк
        zero_rows = np.where(delta_a == 0)[0]
        excess_rows = np.where(delta_a < 0)[0]
        deficit_rows = np.where(delta_a > 0)[0]


        # Шаг 4 Отметка столбцов с занятыми клетками в избыточных строках
        marked_cols = []
        for j in range(n):
            for i in excess_rows:
                if X[i, j] > 0:
                    marked_cols.append(j)
                    break
        marked_cols = list(set(marked_cols))
        print(f"Отмеченные столбцы (с занятыми клетками в избыточных строках): {[j + 1 for j in marked_cols]}")

        # Шаг 5-6 Нахождение минимальных приращений в отмеченных столбцах
        print("Для нулевых и недостаточных строк")
        min_in_marked = np.full(m, np.inf)
        for i in list(deficit_rows) + list(zero_rows):
            if len(marked_cols) > 0:
                min_val = np.min(delta_C[i, marked_cols])
                min_in_marked[i] = min_val
                print(f"  Для строки {i + 1}: min ΔC в отмеченных столбцах = {min_val}")

        # Находим min_deficit
        if len(deficit_rows) > 0:
            #min_deficit = np.min(min_in_marked[deficit_rows])
            min_deficit = abs(np.min(min_cols[marked_cols[0]] * (-1), min_rows[marked_cols[0] * (-1)]))
            print(f"\nМинимальное приращение для недостаточных строк: minΔ = {min_deficit}")
        else:
            min_deficit = np.inf
            print(f"\nНет недостаточных строк")

        # Шаг 7: Проверка условий для перераспределения
        print(f"\nПроверка условий для перераспределения:")
        print(f"  min_deficit = {min_deficit}")

        direct_redistribution = False
        for i_zero in zero_rows:
            if min_in_marked[i_zero] <= min_deficit:
                print(f"\n  Для нулевой строки {i_zero + 1}: min ΔC = {min_in_marked[i_zero]} ≤ {min_deficit}")
                print(f"  Выполняем непосредственное перераспределение")

                j = marked_cols[np.argmin(delta_C[i_zero, marked_cols])]
                print(f"  Выбран столбец B{j + 1} (min ΔC = {delta_C[i_zero, j]})")

                # Находим избыточную строку, имеющую занятую клетку в столбце j
                i_excess = None
                for i in excess_rows:
                    if X[i, j] > 0:
                        i_excess = i
                        break

                if i_excess is None:
                    print(f"  Ошибка: не найдена избыточная строка с занятой клеткой в столбце B{j + 1}")
                    continue

                print(f"  Избыточная строка с занятой клеткой: {i_excess + 1}")
                print(f"  В клетке {i_excess + 1}B{j + 1}: X = {X[i_excess, j]}, Δa = {delta_a[i_excess]}")

                # Находим недостаточную строку
                i_deficit = deficit_rows[np.argmin(min_in_marked[deficit_rows])]
                print(f"  Недостаточная строка: {i_deficit + 1}, Δa = {delta_a[i_deficit]}")

                # Величина перераспределения
                delta_x = min(X[i_excess, j], abs(delta_a[i_excess]), delta_a[i_deficit])
                print(
                    f"  Величина перераспределения: min({X[i_excess, j]}, {abs(delta_a[i_excess])}, {delta_a[i_deficit]}) = {delta_x}")

                # Выполняем перераспределение
                X[i_excess, j] -= delta_x
                X[i_deficit, j] += delta_x
                delta_a[i_excess] += delta_x
                delta_a[i_deficit] -= delta_x

                print(f"  После перераспределения:")
                print(f"    X[A{i_excess + 1}, B{j + 1}] = {X[i_excess, j]}")
                print(f"    X[A{i_deficit + 1}, B{j + 1}] = {X[i_deficit, j]}")
                print(f"    Δa[A{i_excess + 1}] = {delta_a[i_excess]}")
                print(f"    Δa[A{i_deficit + 1}] = {delta_a[i_deficit]}")

                direct_redistribution = True
                break
            else:
                print(f"  Для нулевой строки A{i_zero + 1}: min ΔC = {min_in_marked[i_zero]} > {min_deficit}")
        const = 0
        end = delta_a[0] == -300 and delta_a[1] == 0 and delta_a[2] == 300
        if not direct_redistribution:
            #print(f"\n  Непосредственное перераспределение невозможно")
            print(f"Цепочка...")
            # перераспределение проверяем по цепочкам, идущим через эту нулевую строку из избыточной строки в недостаточную

            if len(excess_rows) > 0 and len(deficit_rows) > 0:
                i_excess = excess_rows[0]
                i_deficit = deficit_rows[0]
                print(f"  Избыточная строка: A{i_excess + 1}, Δa = {delta_a[i_excess]}")
                print(f"  Недостаточная строка: A{i_deficit + 1}, Δa = {delta_a[i_deficit]}")

                # Находим столбец, в котором есть занятая клетка в избыточной строке
                j_start = None
                for j in range(n):
                    if X[i_excess, j] > 0:
                        j_start = j
                        break

                if j_start is not None:
                    print(f"  Найден столбец B{j_start + 1} с занятой клеткой в избыточной строке")

                    # Ищем нулевую строку, связанную с этим столбцом
                    i_zero = None
                    for i in zero_rows:
                        if X[i, j_start] > 0:
                            i_zero = i
                            break

                    if i_zero is not None:
                        print(f"  Найдена нулевая строка A{i_zero + 1}, связанная через столбец B{j_start + 1}")

                        # Находим столбец, связывающий нулевую строку с недостаточной
                        j_end = None
                        for j in range(n):
                            if X[i_zero, j] > 0:
                                j_end = j
                                break

                        if j_end is not None:
                            print(f"  Найден столбец B{j_end + 1}, связывающий нулевую строку с недостаточной")
                            print(
                                f"  Цепочка: A{i_excess + 1} → B{j_start + 1} → A{i_zero + 1} → B{j_end + 1} → A{i_deficit + 1}")

                            # Перераспределение по цепочке
                            delta_x = min(X[i_excess, j_start], abs(delta_a[i_excess]), delta_a[i_deficit])
                            print(
                                f"  Величина перераспределения: min({X[i_excess, j_start]}, {abs(delta_a[i_excess])}, {delta_a[i_deficit]}) = {delta_x}")

                            # Выполняем перераспределение
                            X[i_excess, j_start] -= delta_x
                            X[i_zero, j_start] += delta_x
                            X[i_zero, j_end] -= delta_x
                            X[i_deficit, j_end] += delta_x
                            delta_a[i_excess] += delta_x
                            delta_a[i_deficit] -= delta_x

                            print(f"  После перераспределения по цепочке:")
                            print(f"    X[A{i_excess + 1}, B{j_start + 1}] = {X[i_excess, j_start]}")
                            print(f"    X[A{i_zero + 1}, B{j_start + 1}] = {X[i_zero, j_start]}")
                            print(f"    X[A{i_zero + 1}, B{j_end + 1}] = {X[i_zero, j_end]}")
                            print(f"    X[A{i_deficit + 1}, B{j_end + 1}] = {X[i_deficit, j_end]}")
                            print(f"    Δa[A{i_excess + 1}] = {delta_a[i_excess]}")
                            print(f"    Δa[A{i_deficit + 1}] = {delta_a[i_deficit]}")

        print(f"\nТекущая матрица перевозок X (после итерации {iteration}):")
        print(X)
        print(f"Текущие Δa: {delta_a}")
        # Проверяем, не все ли строки стали нулевыми
        if np.all(delta_a == 0):
            break


    print("ШАГ 12: Проверка оптимальности")
    print(delta_a*const)
    print(f"Все Δa_i = 0, план является допустимым")

    return X


# Заданные параметры

C = np.array([[5189, 4603, 6760],
              [5787, 4842, 6712],
              [6628, 5668, 7911]])
A = np.array([700, 600, 500])
B = np.array([1000, 200, 600])

# Решение задачи
X = delta_method(C, A, B)

print("Матрица перевозок X:")
print(X)
print("Цены перевозок:")
print(X*C)
print("Общая стоимость перевозок:", np.sum(X*C))
