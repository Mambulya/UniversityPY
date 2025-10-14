"""

Симплекс метод
"""
import numpy as np
import matplotlib.pyplot as plt

def simplex_method(f, x0, eps1, eps2, gamma, L, print_iter=False, plot=False):
    n = len(x0)
    iter = 1
    xs_plot = []
    Pn = (L*(n-1 + (n+1)**0.5)) / (2**0.5 * n)
    qn = (L*((n+1)**0.5) - 1) / (2**0.5 * n)

    Xij = np.zeros((n+1, n))
    Xij[0] = x0     # заполнение нулевой точки

    for j in range(1, n+1):
        for i in range(0, n):
            if j - i == 1:
                Xij[j][i] = Xij[0][i] + Pn
            else:
                Xij[j][i] = Xij[0][i] + qn

    F = [f(x) for x in Xij]

    # для отрисовки
    xs_plot.append(Xij.copy())

    while stop_rule(Xij, F, eps1, eps2) == False:

        iter += 1
        worst_x_index = F.index(max(F))
        Xp = Xij[worst_x_index]

        Xp_new = 0
        for x in Xij:
            Xp_new += x
        Xp_new -= Xp
        Xp_new *= (2/n)
        Xp_new -= Xp

        F_xp_new = f(Xp_new)

        if print_iter:
            print(f"====\nXij:\n{Xij}\nXp = {Xp} Xp_new = {Xp_new} f(Xp_new) = {F_xp_new}\nf = {F}\n====")

        if F_xp_new < max(F):
            print("Xp не оказалась худшей => заменим худшую вершину на нее")
            Xij[worst_x_index] = Xp_new
            F[worst_x_index] = f(Xp_new)
        else:
            # Xp_new окаазалась худшей точкой
            # возврат к исходному симплексу за счет сжатич отн лучшей вершины
            best_x_index = F.index(min(F))
            for j in range(n):
                if j != best_x_index:
                    Xij[j] = gamma*Xij[best_x_index] + (1-gamma)*Xij[best_x_index]
            F = [f(x) for x in Xij]

            print("Xp оказалась хуйдшей => возвращаем прошлый симплекс")

        xs_plot.append(Xij.copy())

    best_x_index = F.index(min(F))
    X_opt = Xij[best_x_index]

    if plot:
        plot_simplex(xs_plot)

    return X_opt, f(X_opt), iter

def plot_simplex(Xijs):
    plt.figure(figsize=(25, 8))
    iter = 0
    colors = ["#6bcb77", "#a78ee8", "#f7a072", "#72aee6", "#ad9dc5", "#cb3c83", "#d9023f", "#2a3877"]
    for X in Xijs:
        X_closed = np.vstack([X, X[0]])
        plt.scatter(X_closed[:, 0], X_closed[:, 1], alpha=0.3, color=colors[iter % len(colors)])
        # for vertex in X:
        #     if iter == len(Xijs) - 1:
        #         plt.scatter(vertex[0], vertex[1], marker="*", c="black")
        #     else:
        #         plt.scatter(vertex[0], vertex[1], c=colors[iter % len(colors)], alpha=0.3)

        plt.plot(X_closed[:, 0], X_closed[:, 1], linestyle="--", color=colors[iter % len(colors)], alpha=0.3)
        iter += 1
    plt.title("Симплексный метод для f(x1, x2) = 3 * (x1 - 5) ** 2 + (x2 - 4) ** 2")
    plt.show()

def func(x):
    x1 = x[0]
    x2 = x[1]
    """Исходная функция"""
    return 3 * (x1 - 5) ** 2 + (x2 - 4) ** 2

def norma(vector):
    """Евклидова норма"""
    norma = 0
    for x in vector:
        norma += x*x
    return norma**0.5

def stop_rule(xs:list, fs:list, eps1, eps2):
    """критерий остановки"""
    for i in range(len(xs) - 1):
        X_curr = xs[i]
        X_next = xs[i+1]

        F_curr = fs[i]
        F_next = fs[i]

        if norma(X_curr - X_next) > eps1:       # определить евклидову норму
            return False
        if abs(F_curr - F_next) > eps2:
            return False
        return True

if __name__ == "__main__":
    gamma = 0.5
    L = 1
    e1 = 0.01
    e2 = 0.01
    x0 = [0, 0]

    print(simplex_method(f=func, x0=x0, eps1 = e1, eps2=e2, gamma=gamma, L=L, print_iter=True, plot=True))
