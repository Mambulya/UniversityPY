"""
РЕАЛИЗАЦИЯ СОСТАВЛЕНИЯ ОПОРНОГО ПЛАНА ТРАНСПОРТНОЙ ЗАДАЧИ
С ПОМОЩЬЮ МЕТОДА ДВОЙНОГО ПРЕДПОЧТЕНИЯ

задача 3*3
"""

import numpy as np



C = np.array([[5189, 4603, 6760],
              [5787, 4842, 6712],
              [6628, 5668, 7911]])      # Cij - стоимость перевозки
A = np.array([700, 600, 500])           # aij - поставщики
B = np.array([1000, 200, 600])          # bij - потребители
X = np.array([[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]])               # распределение товара
n = 3                                   # потребители
m = 3                                   # поставщики

def cross_row(X, i, j):
    """зачеркивает небазисные клетки строки i
    кроме элемента ij
    """
    n = X.shape[1]
    for k in range(n):
        if k != j and not np.isnan(X[i][k]):
            X[i][k] = np.nan
    return X

def cross_column(X, j, i):
    """
    зачеркивает небазисные клетки столбца j
    кроме элемента ij
    """
    m = X.shape[0]
    for l in range(m):
        if l != i and not np.isnan(X[l][j]):
            X[l][j] = np.nan
    return X

def double_pref(C, A, B):
    X_flag = np.zeros((m, n), dtype=float)
    X_temp = np.zeros((m, n), dtype=float)
    X_filled = np.zeros((m, n), dtype=bool)  # Флаг заполненных клеток

    A_temp = A.copy()
    B_temp = B.copy()

    # выбор мин элемента в строке
    for i in range(m):
        minn = C[i][0]
        min_j = 0
        for j in range(n):
            if minn > C[i][j]:
                minn = C[i][j]
                min_j = j
        X_flag[i][min_j] += 1


    # выбор мин этемента по столбцам
    for j in range(n):
        minn = C[0][j]
        min_i = 0
        for i in range(m):
            if minn > C[i][j]:
                minn = C[i][j]
                min_i = i

        X_flag[min_i][j] += 1

    #print("Матрица предпочтений:")
    #print(X_flag)

    for i in range(m):
        for j in range(n):
            if X_flag[i][j] == 2 and not X_filled[i][j] and A_temp[i] > 0 and B_temp[j] > 0:
                if A_temp[i] <= B_temp[j]:  # зачеркиваем строку
                    X_flag = cross_row(X_flag, i, j)
                else:
                    X_flag = cross_column(X_flag, j, i)  # зачеркиваем столбец

                min_a_b = min(A_temp[i], B_temp[j])
                A_temp[i] -= min_a_b
                B_temp[j] -= min_a_b

                X_temp[i][j] = min_a_b

    for i in range(m):
        for j in range(n):
            if X_flag[i][j] == 1 and not X_filled[i][j] and A_temp[i] > 0 and B_temp[j] > 0:
                if A_temp[i] <= B_temp[j]:  # зачеркиваем строку
                    X_flag = cross_row(X_flag, i, j)
                else:
                    X_flag = cross_column(X_flag, j, i)  # зачеркиваем столбец

                min_a_b = min(A_temp[i], B_temp[j])
                A_temp[i] -= min_a_b
                B_temp[j] -= min_a_b

                X_temp[i][j] = min_a_b

    # заполняем оставшиеся клетки (если остались нераспределенные ресурсы)
    for i in range(m):
        for j in range(n):
            if not X_filled[i][j] and A_temp[i] > 0 and B_temp[j] > 0:
                min_a_b = min(A_temp[i], B_temp[j])
                X_temp[i][j] = min_a_b
                A_temp[i] -= min_a_b
                B_temp[j] -= min_a_b
                X_filled[i][j] = True

    return X_temp, X_flag

if __name__=="__main__":
    X0, X_flag = double_pref(C, A, B)
    print("Базисные клетки")
    print(X_flag)
    print("Опорный план с помощью метода двойного предпочтения:")
    print(X0)
    print("Суммарные затраты:")
    print(C*X0)
    print(np.sum(C*X0))