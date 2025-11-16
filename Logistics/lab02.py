"""
Лабораторная работа № 2

МЕТОД ЦЕНТРА ТЯЖЕСТИ

"""

import numpy as np
import matplotlib.pyplot as plt


# data = {"A":[1600, 4, 18, 42],         # Vi, ti, xi, yi
#         "B": [1700, 6, 26, 7],
#         "C": [500, 2, 94, 8],
#         "D": [1100, 3, 68, 73],
#         "E": [1300, 4, 41, 80]}

data = {"A":[1600, 4, 20, 15],         # Vi, ti, xi, yi
        "B": [70, 5, 20, 8],
        "C": [1200, 3, 65, 75],
        "D": [900, 7, 4, 60],
        "E": [100, 2,5, 40]}

# data = {"A":[1500, 2, 90, 65],         # Vi, ti, xi, yi
#         "B": [1600, 3, 7, 50],
#         "C": [500, 1, 6, 20],
#         "D": [1200, 4, 10, 55],
#         "E": [100, 5,60, 20]}

def print_table(d:dict):
    for key in d.keys():
        print(key, d[key])

def calculate_Xo_Yo(places:dict):
    Xo = sum([places[key][0] for key in places.keys()]) / sum([places[key][2] for key in places.keys()])
    Yo = sum([places[key][1] for key in places.keys()]) / sum([places[key][2] for key in places.keys()])
    return round(Xo, 6), round(Yo, 6)

def print_distance(data, O):
    for key in data.keys():
        print(f"{key}: Xi = {data[key][2]}  Yi = {data[key][3]}")
    print(f"Склад: Xi = {O[0]}   Yi = {O[1]}")

def norma(O_prev, O):
    norma = 0
    for i in range(len(O)):
        norma += (O[i] - O_prev[i])**2
    return norma**0.5

O = [0, 0]      # координаты склада
O_prev = [0,0]
O_X_history = []    # для второго графика
O_Y_history = []
TC = 0
TC_prev = 10000
e = 0.01
iter = 0
iterations = []

# xi*(Vi*ti), yi*(Vi*ti), Vi*ti для каждого пункта  - промежуточные вычисления
X_Y = {}
ro = {}

for key in data.keys():
    xi = data[key][2]
    yi = data[key][3]
    Vi = data[key][0]
    ti = data[key][1]

    X_Y[key] = [xi*(Vi*ti), yi*(Vi*ti), Vi*ti, 0]   # 0 под ТС

# шаг 0

# Xo = sum([X_Y[key][0] for key in X_Y.keys()]) / sum([X_Y[key][2] for key in X_Y.keys()])
# Yo = sum([X_Y[key][1] for key in X_Y.keys()]) / sum([X_Y[key][2] for key in X_Y.keys()])
Xo, Yo = calculate_Xo_Yo(X_Y)
O[0] = Xo
O[1] = Yo
O_X_history.append(Xo)
O_Y_history.append(Yo)

# рисунок 1 -  начального располодения
for key in data.keys():
    plt.plot([data[key][2], O[0]], [data[key][3], O[1]], label=key)

plt.grid(True)
plt.legend()
plt.title("Начальное  расположение")
plt.ylabel("Y")
plt.xlabel("X")
plt.show()

# таблица наачального расположения
print("ТАБЛИЦА НАЧАЛЬНОГО РАСПОЛОЖЕНИЯ ОБЪЕКТОВ")
print_distance(data, O)
# print(X_Y)

# шаг 1
print("\nТАБЛИЦА ПРОМЕЖУТОЧНЫХ ИТЕРАЦИЙ")
while abs(TC_prev - TC) > e and (norma(O_prev, O) > e):
    TC_curr = 0
    print(f"Итерация: {iter+1}")
    # для выводя промежуточных итераций
    column_sum_2 = 0
    column_sum_3 = 0
    column_sum_4 = 0
    column_sum_5 = 0

    for key in data.keys():
        xi = data[key][2]
        yi = data[key][3]
        Vi = data[key][0]
        ti = data[key][1]

        r = ((xi - Xo)*(xi - Xo) + (yi-Yo)*(yi-Yo))**0.5
        ro[key] = r
        X_Y[key][3] = Vi*ti/r

        TC_curr += Vi*ti*r

        print(f"{key}: r0i={round(r, 6)}  vi*ti*r0i={round(Vi*ti*r, 6)}  xi*vi*ti/r0i={round(xi*Vi*ti/r, 6)}  yi*vi*ti/r0i={round(yi*Vi*ti/r, 6)}  vi*ti/r0i={round(Vi*ti/r, 6)}")
        column_sum_2 += round(Vi*ti*r, 6)
        column_sum_3 += round(xi*Vi*ti/r, 6)
        column_sum_4 += round(yi*Vi*ti/r, 6)
        column_sum_5 += round(Vi*ti/r, 6)

    Xo = sum(data[key][2] * X_Y[key][3] for key in X_Y.keys()) / sum(X_Y[key][3] for key in X_Y.keys())
    Yo = sum(data[key][3] * X_Y[key][3] for key in X_Y.keys()) / sum(X_Y[key][3] for key in X_Y.keys())

    O_prev[0] = O[0]
    O_prev[1] = O[1]
    O[0] = round(Xo, 6)
    O[1] = round(Yo, 6)
    O_X_history.append(Xo)
    O_Y_history.append(Yo)

    TC_prev = TC
    TC = TC_curr
    iter += 1

    print(f"Сумма:            {column_sum_2}  {column_sum_3}  {column_sum_4}  {column_sum_5}")
    print(f"Xo={O[0]}  Yo={O[1]}\n")


    # таблица итераций
    iterations.append([iter, O, TC, TC_prev])
    #print(f"{iter}) X0 = {O[0]}     Y0 = {O[1]}      TC = {TC}     TC(k)-TC(k+1) = {TC_prev - TC}")


print("\nТАБЛИЦА ИТЕРАЦИЙ")
for i in iterations:
    print(f"{i[0]}) X0 = {i[1][0]}     Y0 = {i[1][1]}      TC = {i[2]}     TC(k)-TC(k+1) = {i[3] - i[2]}")

# 2 график - изменение координат склада
plt.plot(O_X_history, O_Y_history)
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.title("Изменение координат склада по итерациям")
plt.show()

# график 3 - опт расположение склада
for key in data.keys():
    plt.plot([data[key][2], O[0]], [data[key][3], O[1]], label=key)

plt.grid(True)
plt.legend()
plt.title("Оптимальное расположение")
plt.ylabel("Y")
plt.xlabel("X")
plt.show()

print("\nТАБЛИЦА ОПТИМАЛЬНОГО РАСПОЛОЖЕНИЯ ОБЪЕКТОВ")
print_distance(data, O)