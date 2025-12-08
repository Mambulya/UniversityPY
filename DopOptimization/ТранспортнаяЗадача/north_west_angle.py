"""
РЕАЛИЗАЦИЯ СОСТАВЛЕНИЯ ОПОРНОГО ПЛАНА ТРАНСПОРТНОЙ ЗАДАЧИ
С ПОМОЩЬЮ МЕТОДА СЕВЕРНО-ЗАПАДНОГО УГЛА

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

def north_west_angle(A, B, X):
    X_temp = np.array([[-1, -1, -1],
                        [-1, -1, -1],
                        [-1, -1, -1]])
    A_temp = A.copy()
    B_temp = B.copy()
    i, j =0, 0

    while i < m and j < n:
        if A_temp[i] == 0:
            i += 1
            continue
        if B_temp[j] == 0:
            j += 1
            continue

        x = min(A_temp[i], B_temp[j])

        X[i, j] = x

        A_temp[i] -= x
        B_temp[j] -= x

        if A_temp[i] == 0 and B_temp[j] == 0:
            # если это не последняя клетка переходим по диагонали
            if i < m - 1:
                i += 1
                j += 1
            else:
                i += 1
        elif A_temp[i] == 0:
            i += 1  # переходим к следующей строке
        else:
            j += 1  # переходим к следующему столбцу

    return X

if __name__=="__main__":
    X0 = north_west_angle(A, B, X)
    print("Опорный план с помощью СЗ угла:")
    print(X0)
    print("Суммарные затраты:")
    print(C*X0)
    print("Cуммарные затраты")
    print(np.sum(X*X0))
