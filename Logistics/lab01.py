"""
Лабораторная работа №1

Модель Леонтьева, заданная через коэффициенты прямых материальных затрат

"""
import numpy as np

A = np.array([[0.4, 0.1, 0.3],
              [0.2, 0.3, 0.3],
              [0.3, 0.2, 0.2]])     # aij
Y = np.array([[30],
              [30],
              [85]])          # конечный продукт
t = np.array([[1.5],
              [2],
              [3]])           # прямая трудоемкость
f = np.array([[4],
              [3.5],
              [2]])           # коэффициенты прямой фондоемкости
delta_Y_percentage = np.array([[20],
                               [10],
                               [-20]])    # изменение конечного продукта в %
E = np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]])           # единичная матрица

def get_det(A):
    """ Вычисляет определитель матрицы 3*3 с помощью правила треугильников"""
    det = (-(A[0, 2] * A[1, 1] * A[2, 0] + A[0, 0] * A[2, 1] * A[1, 2] + A[1, 0] * A[0, 1] * A[2, 2])
           + (A[0,0] * A[1,1] * A[2,2] + A[1, 0] * A[2, 1] * A[0, 2] + A[2, 0] * A[0, 1] * A[1, 2]))
    return det

def alg_dopolnenie(A):
    """
    Вычисляет матрицу алгебраических дополнений для квадратной матрицы A
    """
    n = A.shape[0]  # количество строк
    C = np.zeros_like(A, dtype=float)
    for i in range(n):
        for j in range(n):
            # минор
            minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
            # алгебраическое дополнение
            C[i, j] = ((-1) ** (i + j)) * np.linalg.det(minor)
    return C

def multiply_matrix_vector_no_plus(A, V):
    """Осуществляется формула Xij = Aij * xj -> вектор-столбец"""
    n = A.shape[0]
    C = np.zeros_like(A, dtype=float)
    for i in range(n):
        for j in range(n):
            C[i, j] = A[i, j] * V[j, 0]
    return C

def multiply_matrix_vector_plus(A, V):
    """матрица на столбец"""
    n = A.shape[0]
    m = A.shape[1]
    C = np.zeros((n, 1))

    for i in range(n):
        for j in range(m):
            C[i, 0] += A[i, j] * V[j, 0]
    return C



if __name__ == "__main__":
    # == I. Определить изменение валового выпуска ΔX и межотраслевые потоки ΔXij
    # X = (E - A)^-1 * Y
    print("I. Определить изменение валового выпуска ΔX и межотраслевые потоки ΔXij")
    E_A = E - A
    det = get_det(E_A)
    alg_dop = alg_dopolnenie(E_A)
    obrat_matrix = (1/det) * (alg_dop.T)

    # проверка
    # obrat_matrix = np.linalg.inv((E - A))   # = (E - A)^-1
    print(f"(E - A)^-1:\n {obrat_matrix}")
    print(f"=ПРОВЕРКА======\n(E - A) * (E - A)^-1 :\n {(E - A).dot(obrat_matrix)}\n===============")

    X = obrat_matrix.dot(Y)
    print(f"Валовый выпуск X:\n {X}")

    delta_Y = np.array([[(delta_Y_percentage[0, 0] * Y[0,0]) / 100],
                        [(delta_Y_percentage[1, 0] * Y[1,0]) / 100],
                        [(delta_Y_percentage[2, 0] * Y[2,0]) / 100]])
    print(f"ΔY:\n {delta_Y}")
    #delta_X = obrat_matrix.dot(delta_Y)
    delta_X = multiply_matrix_vector_plus(obrat_matrix, delta_Y)
    print(f"ΔX:\n {delta_X}")
    ΔXij = multiply_matrix_vector_no_plus(A, delta_X)
    print(f"Изменение межотрослевых потоков ΔXij:\n {ΔXij}\n")

    # ==== II Определить изменение потребности в трудовых ресурсах по отраслям
    # ΔXtj = tj(xj + Δxj)
    print("II Определить изменение потребности в трудовых ресурсах по отраслям ΔXtj")
    ΔXtj = t * (X + delta_X)
    print(ΔXtj)

    # ==== III Определить изменение потребности в ОПФ по отраслям ΔФj
    print("==== III Определить изменение потребности в ОПФ по отраслям ΔФj")
    ΔФj = f * delta_X
    print(ΔФj)

    # ==== IV определить промежуточный и валовый продукт Xij, Xi;
    # условно-чистый продукт Zj;
    # мат затраты в каждую отрасль Cij
    print("==== IV определить промежуточный и валовый продукт Xij, Xi")
    print(f"Валовый продукт Xi: \n {X}")
    Xij = multiply_matrix_vector_no_plus(A, X)

    print(f"Промежуточный продукт Xij: \n{Xij}")

    X_zatrat = np.array([[Xij[0, 0] + Xij[1, 0] + Xij[2, 0]],
                         [Xij[0, 1] + Xij[1, 1] + Xij[2, 1]],
                         [Xij[0, 2] + Xij[1, 2] + Xij[2, 2]]])
    print(f"Мат затраты в отраслях: \n{X_zatrat}")

    Zj = np.array(X - X_zatrat)
    print(f"Условно-чистый продукт отросли Zj: \n {Zj}")

    # ==== V Определить матрицы полных материальных затрат Cij и
    # коэффициенты косвенных материальных затрат первого порядка
    Cij = obrat_matrix - E
    print(f"==== V Полные материалььные затраты в каждой отрасли Cij: \n {Cij}")

    A1 = A.dot(A)
    print(f"коэффициенты косвенных материальных затрат первого порядка: \n {A1}")

    # ===== VI Определить совокупные затраты живого труда в каждой отрасли
    T = t * X
    # T = (t.T).dot(obrat_matrix)
    print(f"==== VI Совокупные затраты живого труда в каждой отрасли: \n {T}")

    # VII Определить совокупные затраты ОПФ в каждой отрасти
    F = f * X
    # F = f.dot(obrat_matrix)
    print(f"==== VII совокупные затраты ОПФ в каждой отрасти F: \n {F}")
