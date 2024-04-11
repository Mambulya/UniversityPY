
# Пробные данные для уравнения A*X = B
from linearSystem import A, f

# Вывод матрицы на экран
def print_arr(string, namevec, a):
    if (type(a) == int) or (type(a) == float):
        print(a)
    else:
        print(string)
        for k in range(len(a)):
            print("{}[{}] = {:8.4f}".format(namevec, k, a[k]))


# Проверка 3х-диаг. матрицы коэффициентов на корректность
def isCorrectArray(a):
    n = len(a)

    for row in range(0, n):
        if (len(a[row]) != n):
            print('Не соответствует размерность')
            return False

    for row in range(1, n - 1):
        if (abs(a[row][row]) < abs(a[row][row - 1]) + abs(a[row][row + 1])):
            print('Не выполнены условия достаточности')
            return False

    if (abs(a[0][0]) < abs(a[0][1])) or (abs(a[n - 1][n - 1]) < abs(a[n - 1][n - 2])):
        print('Не выполнены условия достаточности')
        return False

    for row in range(0, len(a)):
        if (a[row][row] == 0):
            print('Нулевые элементы на главной диагонали')
            return False
    return True


# Процедура нахождения решения 3-х диагональной матрицы
def solution(a, b):
    if (not isCorrectArray(a)):
        print('Ошибка в исходных данных')
        return -1

    n = len(a)
    x = [0 for k in range(0, n)]  # обнуление вектора решений
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

    print_arr('Прогоночные коэффициенты P: ', 'p', p)
    print_arr('Прогоночные коэффициенты Q: ', 'q', q)

    # Обратный ход
    x[n - 1] = q[n - 1]
    for i in range(n - 1, 0, -1):
        x[i - 1] = p[i - 1] * x[i] + q[i - 1]

    return x


# MAIN - блок программмы
x = solution(A, f)  # Вызываем процедуру решение
print_arr('Решение: ', 'x', x)
