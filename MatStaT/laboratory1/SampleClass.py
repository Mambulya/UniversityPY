import matplotlib.pyplot as plt
import openpyxl
import scipy.stats as stats
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF


class Sample:

    def __init__(self, path_arg):
        self.path = path_arg
        self.data = None
        self.volume = None
        self.Ex = None
        self.Dx = None
        self.Dx1 = None
        self.б = None
        self.б1 = None
        self.g1 = None
        self.mediana = None
        self.frequencies = None
        self.interquartile_latitude = None
        self.Q1 = None
        self.Q3 = None
        self.fashion = None

    def create_data(self):
        """
        считывает выборку с excel файла и заносит в массив
        """
        # считываем данные
        self.data = []
        book = openpyxl.open(self.path, read_only=True)
        sheet = book.active

        for row in range(1, 100000):
            try:
                self.data.append(float(sheet[row][0].value))
            except IndexError:
                break
            except ValueError:
                continue

    def create_volume(self):
        """
        определяет объём выборки
        """
        if self.data is None:
            self.create_data()
        self.volume = len(self.data)

    def get_assymetry(self):
        if self.Ex is None:
            self.create_moments()
        self.g1 = 0
        for i in range(self.volume):
            self.g1 += (self.data[i] - self.Ex) ** 3
        self.g1 *= (1 / (self.volume * (self.б ** 3)))

    def get_mediana(self):
        if self.data is None:
            self.create_data()
        if self.volume is None:
            self.create_volume()

        sorted_data = sorted(self.data)
        n = self.volume

        if n % 2:     #медиана - элемент посередине
            self.mediana = sorted_data[(n - 1) // 2]
        else:
            self.mediana = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    def create_moments(self):
        """
        вычисляет математическое ожидание Ех, дисперсию Dx и среднее квадратичесое б, моду fashion
        """
        if self.volume is None:
            self.create_volume()

        self.Ex = sum(self.data) / self.volume  # выборочное среднее - состоятельная и не смещенная оценка параметра
        self.Dx = sum([i**2 for i in self.data]) / self.volume - (self.Ex)**2
        self.Dx1 = self.volume*(self.Dx)**2 / (self.volume - 1)
        self.б = self.Dx ** (1 / 2)  # среднее квадротическое
        self.fashion = max(set(self.data), key = self.data.count)

    def print_moments(self):
        """
        выписывает математическое ожидание, среднее квадратическое значение и дисперсию
        """
        if self.Ex is None:
            self.create_moments()
        if self.mediana is None:
            self.get_mediana()
        if self.g1 is None:
            self.get_assymetry()
        if self.interquartile_latitude is None:
            self.get_interquartile_latitude()

        print(
            """
            n = {}
            Xn - X1 = {}
            Ex = {}
            б = {}
            Dx = б^2 = {}
            Dx1 = {}
            медиана = {}
            g1(коэффициент ассимметрии) = {}
            мода = {}
            Q1 = {}
            Q3 = {}
            интерквартильная широта = {}
            """.format(self.volume, max(self.data) - min(self.data), self.Ex, self.б,self.Dx, self.Dx1, self.mediana, self.g1, self.fashion, self.Q1, self.Q3, self.interquartile_latitude))

    def get_frequency(self):
        """
        ищет частоту уникальных элементов среди оригинальной выборки
        :return:
        """
        if self.data is None:
            self.create_data()
        # сопоставить частоту всем уникальным элементам
        data1 = list(set(self.data))
        self.frequencies = {i: self.data.count(i) for i in data1}

    def get_interquartile_latitude(self):
        if self.data is None:
            self.create_data()

        if self.volume is None:
            self.create_volume()

        if self.mediana is None:
            self.get_mediana()  # главная медиана
        sorted_data = sorted(self.data)

        index = (self.volume - 1) // 2

        # певая квартиль
        n = len(self.data[:index])
        if index % 2:     # в data нечет кол-во элементов
            self.Q1 = sorted_data[:index][(n - 1) // 2]
        else:             # data имеет чет кол-во элементов
            self.Q1 = sorted_data[:index + 1][n // 2]    # потому что длина теперь не n, а n + 1

        #третья квартиль
        n = len(self.data[index+1:])
        if index % 2:     # в data нечет кол-во элементов
            self.Q3 = sorted_data[index+1:][(n - 1) // 2]
        else:             # data имеет чет кол-во элементов
            self.Q3 = sorted_data[index+1:][(n - 1) // 2]

        self.interquartile_latitude = self.Q3 - self.Q1

    def draw_frequency_histogram(self, Xlabel="Значения выборки", Ylabel="Количество", diagram_name="Частотная гистограмма",
                            rectangle_arg = ("pink", "red"), legend_arg=(["Values"], 2, True), grid_arg=("--", "pink"), num=7):
        """
        * рисует частотную гистограмму выборки
        * отмечает
        - моду,
        - медиану,
        - квантили,
        - среднее квадратическое

        :param Xlabel: название оси Х
        :param Ylabel: название оси У
        :param diagram_name: название гистограммы
        :param rectangle_arg: (цвет прямоугольников, цвет границ прямоугольников)
        :param legend_arg: (название легенды, расположение легенды, нарисовать легенду в рамке)
        :param grid_arg: (тип сетки, цвет сетки)
        :param num: на сколько интервалов разбить ось Ох
        """
        if self.data is None:
            self.create_data()
        if self.volume is None:
            self.create_volume()
        if self.fashion is None:
            self.create_moments()
            self.get_frequency()
        if self.mediana is None:
            self.get_mediana()
        if self.interquartile_latitude is None:
            self.get_interquartile_latitude()
        if self.б is None:
            self.create_moments()

        num_bins = int(self.volume / num) # = 8

        # определение границ
        step = (max(self.data) - min(self.data)) / (num_bins-1)
        bins = [min(self.data) + step / 2]

        for i in range(num_bins-2):
            bins.append(bins[-1] + step)

        # вычисление частот каждого интервала
        # sum(np.logical_and(bins[i]>d, d<=bins[i+1]))

        frequencies = [0] * (num_bins)      # +2 места под -inf и +inf, -1 тк границ(bins) больше количсетва столбцов (frequencies) на 1
        frequencies[0] = sum(1 if i <= bins[0] else 0 for i in self.data)   # сколько чисел попало до 1 границы, т.е. -inf
        frequencies[-1] = sum(1 if i > bins[-1] else 0 for i in self.data)  # сколько чисел попало после последней границы, т.е. +inf

        for d in self.data:
            for i in range(0, len(bins)-1):
            # frequencies[i+1] = sum(np.logical_and(bins[i] >  self.data,  self.data <= bins[i + 1]))
                if bins[i] < d <= bins[i + 1]:
                    frequencies[i+1] += 1

        # print(max(self.data))
        # print(bins)
        # print(frequencies)
        # print(sum(frequencies))


        # построение диаграммы
        fig, ax = plt.subplots(figsize=(13, 6))
        rect = plt.Rectangle((bins[0]-step, 0), step, frequencies[0], color=rectangle_arg[0], ec=rectangle_arg[1])  # -Inf
        ax.add_patch(rect)

        for i in range(len(bins)):
            rect = plt.Rectangle((bins[i], 0), step, frequencies[i+1], color=rectangle_arg[0], ec=rectangle_arg[1]) # последняя итерация уже для -inf
            ax.add_patch(rect)

        ax.add_patch(rect)
        #ax.set_xlim([min(self.data) - 1, max(self.data) + 2])
        ax.set_ylim([0, max(frequencies) + 1])
        plt.xticks(bins)

        # отмечаем моменты
        fashion_line = ax.plot([self.fashion]*2, [0,max(frequencies) + 0.5], label="Мода", linestyle="dashdot", color="#DE3163", linewidth=2) # отмечаем моду
        mediana_line = ax.plot([self.mediana]*2, [0, max(frequencies) + 0.5], label="Медиана", linestyle="solid", color="#00FFFF", linewidth=2)
        Q1_line = ax.plot([self.Q1]*2, [0,max(frequencies) + 0.5], label="Q1", linestyle="dotted", color="#6495ED", linewidth=2)
        Q3_line = ax.plot([self.Q3] * 2, [0, max(frequencies) + 0.5], label="Q3", linestyle="dotted", color="#6495ED", linewidth=2)
        Ex_line = ax.plot([self.Ex, self.Ex], [0, max(frequencies) + 0.5], label="Мат. ожидание", linestyle="solid", color="#badbdb", linewidth=2)


        # настройка диаграммы
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.title(diagram_name)
        plt.grid(linestyle=grid_arg[0], color=grid_arg[1])

        fig.legend(loc='outside upper right')

        plt.show()

    def draw_possibility_histogram(self, Xlabel="Значения выборки", Ylabel="Вероятность", diagram_name="Вероятностная гистограмма",
                              rectangle_arg = ("pink", "red"), grid_arg=("--", "pink"), num = 10):
        """
        рисует вероятностную гистограмму выборки
        :param Xlabel: название оси Х
        :param Ylabel: название оси У
        :param diagram_name: название гистограммы
        :param rectangle_arg: (цвет прямоугольников, цвет границ прямоугольников)
        :param legend_arg: (название легенды, расположение легенды, нарисовать легенду в рамке)
        :param grid_arg: (тип сетки, цвет сетки)
        :param num: на сколько интервалов разбить ось Ох
        """
        if self.data is None:
            self.create_data()
        if self.volume is None:
            self.create_volume()
        if self.Ex is None:
            self.create_moments()

        num_bins = int(self.volume / num)  # = 8

        # определение границ
        step = (max(self.data) - min(self.data)) / (num_bins - 1)
        bins = [min(self.data) + step / 2]

        for i in range(num_bins - 2):
            bins.append(bins[-1] + step)

        # вычисление частот каждого интервала
        # sum(np.logical_and(bins[i]>d, d<=bins[i+1]))

        frequencies = [0] * (
            num_bins)  # +2 места под -inf и +inf, -1 тк границ(bins) больше количсетва столбцов (frequencies) на 1
        frequencies[0] = sum(
            1 if i <= bins[0] else 0 for i in self.data) / self.volume  # сколько чисел попало до 1 границы, т.е. -inf
        frequencies[-1] = sum(
            1 if i > bins[-1] else 0 for i in self.data) / self.volume  # сколько чисел попало после последней границы, т.е. +inf

        for d in self.data:
            for i in range(0, len(bins) - 1):
                # frequencies[i+1] = sum(np.logical_and(bins[i] >  self.data,  self.data <= bins[i + 1]))
                if bins[i] < d <= bins[i + 1]:
                    frequencies[i + 1] += 1/self.volume

        # построение диаграммы
        fig, ax = plt.subplots(figsize=(13, 6))
        rect = plt.Rectangle((bins[0] - step, 0), step, frequencies[0], color=rectangle_arg[0], ec=rectangle_arg[1])
        ax.add_patch(rect)
        for i in range(len(bins)):
            rect = plt.Rectangle((bins[i], 0), step, frequencies[i + 1], color=rectangle_arg[0], ec=rectangle_arg[1])
            ax.add_patch(rect)

        ax.add_patch(rect)

        ax.set_ylim([0, max(frequencies) + 0.01])
        plt.xticks(bins)

        # настройка диаграммы
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.title(diagram_name)
        plt.grid(linestyle=grid_arg[0], color=grid_arg[1])

        # функция плотности
        rangeX = np.arange(bins[0] - step, bins[-1] + step, 0.5)
        std_dev = self.б
        mean = self.Ex
        pdf = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-np.power(rangeX - mean, 2) / (2 * np.power(std_dev, 2)))
        plt.plot(rangeX, pdf, 'r', linewidth=2, label='f(x) норм. распределения')

        # проверка функции
        # x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)
        # plt.plot(x, stats.norm.pdf(x, mean, std_dev))

        # создание легенды
        fig.legend()
        plt.show()

    def draw_dot_graph(self):
        """
        без повторяющиеся данных
        """
        if self.data is None:
            self.create_data()

        if self.volume is None:
            self.create_volume()

        if self.frequencies is None:
            self.get_frequency()

        x = [i for i in self.frequencies.keys()]
        y = [i for i in self.frequencies.values()]
        plt.scatter(x, y)
        plt.title("Частотность значений")
        plt.xlabel("Значения выборки")
        plt.ylabel("Частота")
        plt.show()

    def draw_empirical_fun1(self):
        if self.data is None:
            self.create_data()
        if self.volume is None:
            self.create_volume()
        if self.Ex is None:
            self.create_moments()

        # истинная ЭФР
        ecdf = ECDF(sorted(self.data))
        plt.step(ecdf.x, ecdf.y, label="ЭФР F2", color="red")

        # теоретичкская ЭФР
        plt.plot(np.sort(self.data), np.linspace(0, 1, self.volume, endpoint=False), label="т.ЭФР F1", color="#40E0D0")

        plt.xlabel('Значения выборки')
        plt.ylabel("F(x)", fontsize=20)
        plt.legend(loc='upper left')

        plt.show()


    def draw_empirical_fun(self):
       if self.data is None:
           self.create_data()
       if self.volume is None:
           self.create_volume()
       if self.Ex is None:
           self.create_moments()

       X_sorted = sorted(self.data)

       # истинная ЭФР
       n = self.volume
       F = np.arange(1, n + 1) / n
       F_norm = F / np.max(F)
       plt.plot(X_sorted, F_norm, color='red', label="истинная ЭФР F2")

       # теоретичкская ЭФР
       plt.plot(np.sort(self.data), np.linspace(0, 1, self.volume, endpoint=False), label="т.ЭФР F1", color="#40E0D0")


       plt.title('Эмпирическая функция распределения')
       plt.xlabel('Значение случайной величины')
       plt.ylabel('F(x)')
       plt.legend()
       plt.show()
