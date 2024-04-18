from linearSystem import create_system
from matplotlib.pyplot import plot


# Вывод матрицы на экран
def print_arr(string, namevec, a):
    if (type(a) == int) or (type(a) == float):
        print(a)
    else:
        print(string)
        for k in range(len(a)):
            print("{}[{}] = {:8.4f}".format(namevec, k, a[k]))


# Процедура нахождения решения 3-х диагональной матрицы
def solution(a, b):
    # if (not isCorrectArray(a)):
    #     print('Ошибка в исходных данных')
    #     return -1

    n = len(a)
    x = [0]*n  # обнуление вектора решений
    print('Размерность матрицы: ', n, 'x', n)

    # Прямой ход
    p = [0 for k in range(0, n)]
    q = [0 for k in range(0, n)]
    # для первой 0-й строки
    p[0] = a[0][1] / (-a[0][0])
    q[0] = (- b[0]) / (-a[0][0])
    for i in range(1, n - 1):  # заполняем за исключением 1-й и (n-1)-й строк матрицы
        p[i] = a[i][i + 1] / (-a[i][i] - a[i][i - 1] * p[i - 1])
        q[i] = (a[i][i - 1] * q[i - 1] - b[i]) / (-a[i][i] - a[i][i - 1] * p[i - 1])
    # для последней (n-1)-й строки
    p[n - 1] = 0
    q[n - 1] = (a[n - 1][n - 2] * q[n - 2] - b[n - 1]) / (-a[n - 1][n - 1] - a[n - 1][n - 2] * p[n - 2])

    # print_arr('Прогоночные коэффициенты P: ', 'p', p)
    # print_arr('Прогоночные коэффициенты Q: ', 'q', q)

    # Обратный ход
    x[n - 1] = q[n - 1]
    for i in range(n - 1, 0, -1):
        x[i - 1] = p[i - 1] * x[i] + q[i - 1]

    return x

def progonka(A, f):
    n = len(f)

    c = [0] * n # верхняя диагональ
    b = [0] * n # средняя диагональ
    a = [0] * n # нижняя диагональ
    x = [0] * n # alpha * x + beta
    alpha = [0]
    beta = [0]

    for i in range(n):
        b[i] = A[i][i]
        if i > 0:
            a[i] = A[i][i - 1]
        if i < n - 1:
            c[i] = A[i][i + 1]

    # print("Верхняя диагональ: ", c)
    # print("Средняя диагональ: ", b)
    # print("Нижняя диагональ: ", a)

    alpha.append(-c[0] / b[0])
    beta.append(f[0] / b[0])

    for i in range(2, n):
        alpha.append(-c[i-1] / (a[i-1] * alpha[i - 1] + b[i-1]))
        beta.append((f[i-1] - a[i-1] * beta[i - 1]) / (a[i-1] * alpha[i - 1] + b[i-1]))

    # print("alpha: ", alpha)
    # print("beta: ", beta)

    x[n-1] = (f[n-1] - a[n-1]*beta[n-1])/(b[n-1] + a[n-1]*alpha[n-1])

    for i in range(n-2, -1, -1):
        x[i] = alpha[i + 1] * x[i+1] + beta[i + 1]

    return x


def calculate_errors(A_arg, f_arg, x_arg):
    errori = -1

    for i in range(len(A_arg)):
        answeri = 0

        for j in range(len(A_arg)):
            answeri += A_arg[i][j] * x_arg[j]

        errori = max(abs(abs(answeri) - abs(f_arg[i])), errori)

    return errori


# A, f = create_system(20)
#
# print("A: ")
# for i in range(4):
#     print(A[i])
#
# print("f: ", f)
#
# x = progonka(A, f)
# print("Решение: ", x)
#
# print("final error for n = {}: {:.20f}".format(len(A) + 1, calculate_errors(A, f, x)))

for n in [5, 10, 20, 50, 100, 200, 500, 1000]:
     A, f = create_system(n)
     x = progonka(A, f)  # корни уравнений
     #print_arr('Решение: ', 'x', x)

     print("final error for n = {}: {:.20f}".format(len(A) + 1, calculate_errors(A, f, x)))
