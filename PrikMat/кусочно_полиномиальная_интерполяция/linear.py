"""
Реализация кусочно-линейной интерполяции

"""
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.sin(x)
class LinearApproximation:
    def __init__(self, x_nodes, y_nodes):
        self.x_nodes = x_nodes
        self.y_nodes = y_nodes
        self.n = len(x_nodes)
        assert self.n == len(y_nodes)
        assert all(x_nodes[i] < x_nodes[i+1] for i in range(self.n - 1)), "x_nodes должны быть строго возрастающими"

    def approximate(self, x):
        """
        x: скаляр или список/массив значений
        возвращает аппроксимированное значение(я) в точках x
        """
        if isinstance(x, (int, float)):
            return self._approximate_point(x)
        else:
            return [self._approximate_point(xi) for xi in x]

    def _approximate_point(self, x):
        # Обработка выхода за границы
        if x <= self.x_nodes[0]:
            return self.y_nodes[0]
        if x >= self.x_nodes[-1]:
            return self.y_nodes[-1]

        # Найти интервал
        # Можно делать бинарный поиск, но для простоты — перебор
        for i in range(self.n - 1):
            if self.x_nodes[i] <= x <= self.x_nodes[i+1]:
                x0, x1 = self.x_nodes[i], self.x_nodes[i+1]
                y0, y1 = self.y_nodes[i], self.y_nodes[i+1]
                # Li
                y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                return y

        # На всякий случай (теоретически не должно случиться)
        return None


# Опорные узлы и значения функции sin(x)
x_nodes = np.linspace(0, 2 * np.pi, 12)
# [0.         0.57119866 1.14239733 1.71359599 2.28479466 2.85599332
#  3.42719199 3.99839065 4.56958931 5.14078798 5.71198664 6.28318531]
y_nodes = np.sin(x_nodes)

model = LinearApproximation(x_nodes.tolist(), y_nodes.tolist())

# Точки для построения графика
x_plot = np.linspace(0, 2 * np.pi, 100)
y_approx = model.approximate(x_plot.tolist())
y_true = np.sin(x_plot)

# тест на сходимость
print("C")
for i in range(len(x_plot)):
    print("|f({:.3f}) - ф({:.3f})| = {}".format(x_plot[i], x_plot[i], np.abs(y_approx[i] - y_true[i])))

plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_true, label='sin(x) — Истинная функция', color='#dad4ce')
plt.plot(x_plot, y_approx, '--', label='Кусочно-линейная аппроксимация', color='#94af8c')
plt.scatter(x_nodes, y_nodes, color='#ad1f2b', label='Узлы')
plt.title('Кусочно-линейная аппроксимация функции sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()
