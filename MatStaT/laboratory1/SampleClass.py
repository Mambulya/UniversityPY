import matplotlib.pyplot as plt
import openpyxl
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
            Ex = {}
            б = {}
            Dx = б^2 = {}
            медиана = {}
            g1(коэффициент ассимметрии) = {}
            мода = {}
            Q1 = {}
            Q3 = {}
            интерквартильная широта = {}
            """.format(self.Ex, self.б,self.Dx, self.mediana, self.g1, self.fashion, self.Q1, self.Q3, self.interquartile_latitude))

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

        num_bins = int(self.volume / num)
        step = (max(self.data) - min(self.data)) / num_bins
        bins = [min(self.data) + step / 2]

        for i in range(num_bins):
            bins.append(bins[-1] + step)

        # вычисление частот каждого интервала
        frequencies = [0] * num_bins
        for d in self.data:
            for i in range(num_bins):
                if bins[i] <= d < bins[i + 1]:
                    frequencies[i] += 1
                    break

        # построение диаграммы
        fig, ax = plt.subplots(figsize=(13, 6))
        for i in range(num_bins):
            rect = plt.Rectangle((bins[i], 0), step, frequencies[i], color=rectangle_arg[0], ec=rectangle_arg[1])
            ax.add_patch(rect)
        ax.set_xlim([min(self.data) - 1, max(self.data) + 2])
        ax.set_ylim([0, max(frequencies) + 1])
        plt.xticks(bins)

        # отмечаем моменты
        fashion_line = ax.plot([self.fashion]*2, [0,max(frequencies) + 0.5], label="Мода", linestyle="dashdot", color="#DE3163", linewidth=2) # отмечаем моду
        mediana_line = ax.plot([self.mediana]*2, [0, max(frequencies) + 0.5], label="Медиана", linestyle="solid", color="#00FFFF", linewidth=2)
        Q1_line = ax.plot([self.Q1]*2, [0,max(frequencies) + 0.5], label="Q1", linestyle="dotted", color="#6495ED", linewidth=2)
        Q3_line = ax.plot([self.Q3] * 2, [0, max(frequencies) + 0.5], label="Q3", linestyle="dotted", color="#6495ED", linewidth=2)
        S_line = ax.plot([self.Ex, self.б + self.Ex], [max(frequencies) / 2]*2, label="б", linestyle="dashed", color="#badbdb", linewidth=2)


        # настройка диаграммы
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.title(diagram_name)
        plt.grid(linestyle=grid_arg[0], color=grid_arg[1])
        # создание легенды
        # hist_legend = ax.legend(legend_arg[0], loc=legend_arg[1], frameon=legend_arg[2])  # легенда гистограммы
        # ax.add_artist(hist_legend)

        # leg1 = ax.legend(loc='upper right')
        # leg2 = ax.legend([fashion_line, mediana_line, Q1_line, Q3_line, S_line], ['fashion', 'median', 'Q1', 'Q3', 'б'], loc='upper right')
        # ax.add_artist(leg1)

        fig.legend(loc='outside upper right')

        plt.show()

    def draw_possibility_histogram(self, Xlabel="Значения выборки", Ylabel="Вероятность", diagram_name="Вероятностная гистограмма",
                              rectangle_arg = ("pink", "red"), grid_arg=("--", "pink"), num = 7):
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

        num_bins = int(self.volume / num)
        step = (max(self.data) - min(self.data)) / num_bins
        bins = [min(self.data) + step / 2]

        for i in range(num_bins):
            bins.append(bins[-1] + step)

        # вычисление ОТНОСИТЕЛЬНЫХ частот каждого интервала
        frequencies = [0] * num_bins
        for d in self.data:
            for i in range(num_bins):
                if bins[i] <= d < bins[i + 1]:
                    frequencies[i] += 1
                    break
        Rfrequencies = [i / self.volume for i in frequencies]

        # построение диаграммы
        fig, ax = plt.subplots(figsize=(13, 6))
        for i in range(num_bins):
            rect = plt.Rectangle((bins[i], 0), step, Rfrequencies[i],  color=rectangle_arg[0], ec=rectangle_arg[1])
            ax.add_patch(rect)
        ax.set_xlim([min(self.data) - 1, max(self.data) + 2])
        ax.set_ylim([0, max(Rfrequencies) + 0.01])
        plt.xticks(bins)

        # настройка диаграммы
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.title(diagram_name)
        plt.grid(linestyle=grid_arg[0], color=grid_arg[1])

        # функция плотности
        rangeX = np.arange(bins[0], bins[-1], 0.5)
        std_dev = self.б
        mean = self.Ex
        pdf = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-np.power(rangeX - mean, 2) / (2 * np.power(std_dev, 2)))
        plt.plot(rangeX, pdf, 'r', linewidth=2, label='pdf')

        # создание легенды
        fig.legend(loc='upper right')
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
        plt.xlabel("Значения выборки")
        plt.ylabel("Частота")
        plt.show()

    def draw_empirical_fun(self):
        if self.data is None:
            self.create_data()

        ecdf = ECDF(self.data)

        plt.step(ecdf.x, ecdf.y, label="ecdf", color="red")
        plt.xlabel('Значения выборки')
        plt.ylabel("F(x)", fontsize=20)
        plt.legend(loc='upper left')
        plt.show()
