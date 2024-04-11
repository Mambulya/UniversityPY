"""

вычисляет матирицу А и вектор b у СЛАУ через метод конечных разностей

Вариант 3с стр 126

[a, b] = [0, pi]
"""

from math import sin, pi

# input
a = 0
b = pi


# шаг сетки x
n = 5
h = (b - a) / n
# внутренние точки сетки
xs = [a + i*h for i in range(1,n)]


A = [[0,]*(n-1) for i in range(n-1)]
f = [0] * (n-1)

# первое уравнение СЛАУ
A[0][0] = 2 + h*h*sin(xs[0])
A[0][1] = -1
f[0] = h*h*(9 + sin(xs[0]))*sin(3*xs[0])

# последнее уравнение СЛАУ
A[-1][-2] = -1
A[-1][-1] = 2 + h*h*sin(xs[-1])
f[-1] = h*h*(9+sin(xs[-1]))*sin(3*xs[-1])

# уравнения i = 2, ..., n-2
for i in range(2, n-1):
    A[i-1][i-2] = -1
    A[i-1][i-1] = 2 + h*h*sin(xs[i-1])
    A[i-1][i] = -1

    f[i-1] = h*h*(9+sin(xs[i-1]))*sin(3*xs[i-1])

for el in A:
    print(el)
print("--------------")
print(f)
