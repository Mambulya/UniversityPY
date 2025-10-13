"""
Минимизация функции нескольких переменных с помощью метож Градиентого спуска

"""

import matplotlib.pyplot as plt
import numpy as np

def Gradient(f, X0, B, e, gradient, stop_rule, print_iter=False, plot=False):
    """
    Градиентныый спуск для минимизации (используется антиградиент)
    X0 : numpy array !
    """
    iter = 1
    X_curr = X0
    X_next = X_curr - B*gradient(X_curr[0], X_curr[1])

    xs = [X_curr, X_next]

    while stop_rule(f, e, x_curr=X_next, x_prev=X_curr) == False:
        if print_iter:
            print(f"Xk+1 = {X_next}   Xk = {X_curr}\n")
        X_curr = X_next
        X_next = X_curr - B*gradient(X_curr[0], X_curr[1])  # анти-градиент
        iter += 1
        xs.append(X_next)

    if plot:
        plot_gradient(f, xs)

    return (X_next, f(X_next), iter)  # (x*, f(x*), needed iterations)

def plot_gradient(f, xs):
    x1 = np.linspace(0, 6, 100)
    x2 = np.linspace(0, 5, 100)
    X1, X2 = np.meshgrid(x1, x2)
    Z = f([X1, X2])

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(X1, X2, Z, alpha=0.6, cmap='viridis')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x1,x2)')
    ax.set_title('f(x1, x2)')

    for i in range(len(xs)):
        x1 = xs[i][0]
        x2 = xs[i][1]
        z = f([x1, x2])
        if i == 0:
            c = "black"
            m = "o"
        elif i == len(xs) - 1:
            c = "red"
            m = "*"
        else:
            c = "blue"
            m = "o"

        ax.scatter(x1, x2, z, color=c, marker=m, label = f"k={i+1}")
        # градиент
        points_array = np.array(xs)
        ax.plot(points_array[:, 0], points_array[:, 1], f([points_array[:, 0], points_array[:, 1]]),
                color="#fad55c", linestyle="--", alpha=0.7)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    def func(x:list):
        x1 = x[0]
        x2 = x[1]
        """Исходная функция"""
        return 3*(x1-5)**2 + (x2-4)**2

    def df_func_x1(f, x:list, h=0.001): # первая производня функции по x1
        x1 = x[0]
        x2 = x[1]
        return (f(x) - f([x1 - h, x2])) / h

    def df_func_x2(f, x:list, h=0.001): # первая производня функции по x2
        x1 = x[0]
        x2 = x[1]
        return (f(x) - f([x1, x2 - h])) / h

    def gradient_func(x1, x2):
        """Градиент func"""
        derivative_x1 = df_func_x1(f=func, x=[x1, x2])   # первая производная func по x1
        derivative_x2 = df_func_x2(f=func, x=[x1, x2])  # первая производная func по x2
        return np.array([derivative_x1, derivative_x2])
        #return np.array([6*x1 - 30, 2*x2 - 8])

    def current_stop_rule(f, e, x_curr, x_prev):
        """Критерий остановки"""
         # для начальной итерации
        print(f"|f(Xk+1) - f(Xk)| = {abs(f(x_curr) - f(x_prev))}")
        return abs(f(x_curr) - f(x_prev)) <= e


    e = 0.1
    B = 0.1
    x0 = np.array([0,0])

    minimum = Gradient(f=func, X0 = x0, B=B, e=e, gradient = gradient_func,
             stop_rule=current_stop_rule, print_iter=True, plot=True)
    print(f"x* = {minimum[0]}   f(x*) = {minimum[1]}\nВсего итераций: {minimum[2]}")


