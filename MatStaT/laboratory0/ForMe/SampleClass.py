import matplotlib.pyplot as plt
import numpy as np
import openpyxl


class Sample:

    def __init__(self, path_arg):
        self.path = path_arg
        self.data = None
        self.volume = None
        self.Ex = None
        self.Dx = None
        self.б = None

    def create_data(self):
        """
        считывает выборгу с excel файла и заносит в массив
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
        определяет объём выборги
        """
        if self.data is None:
            self.create_data()
        self.volume = len(self.data)

    def create_moments(self):
        """
        вычисляет математическое ожидание Ех, дисперсию Dx и среднее квадратичесое б
        """
        if self.volume is None:
            self.create_volume()

        self.Ex = sum(self.data) / self.volume  # выборочное среднее - состоятельная и не смещенная оценка параметра
        self.Dx = np.var(self.data)  # дисперсия var() - смещенная
        self.б = self.Dx ** (1 / 2)  # среднее квадротическое

    def print_moments(self):
        """
        выписывает математическое ожидание, среднее квадратическое значение и дисперсию
        """
        if self.Ex is None:
            self.create_moments()
        print(
            """
            Ex ~ {}
            б ~ {}
            Dx = б^2 ~ {}
            """.format(np.round(self.Ex, 3),
                       np.round(self.б, 3), np.round(self.Dx, 3)))

    def frequency_histogram(self, Xlabel="Values", Ylabel="Amount", diagram_name="Frequency Histogram",
                            rectangle_arg = ("pink", "red"), legend_arg=(["Values"], 2, True), grid_arg=("--", "pink")):
        """
        рисует частотную гистограмму выборги
        :param Xlabel: название оси Х
        :param Ylabel: название оси У
        :param diagram_name: название гистограммы
        :param rectangle_arg: (цвет прямоугольников, цвет границ прямоугольников)
        :param legend_arg: (название легенды, расположение легенды, нарисовать легенду в рамке)
        :param grid_arg: (тип сетки, цвет сетки)
        """
        num_bins = int(self.volume / 7)
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

        # настройка диаграммы
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.title(diagram_name)
        plt.legend(legend_arg[0], loc=legend_arg[1], frameon=legend_arg[2])
        plt.grid(linestyle=grid_arg[0], color=grid_arg[1])

        plt.show()

    def possibility_histogram(self, Xlabel="Values", Ylabel="Posibility", diagram_name="Posibility Histogram",
                              rectangle_arg = ("pink", "red"), legend_arg=(["Values"], 2, True), grid_arg=("--", "pink")):
        """
        рисует вероятностную гистограмму выборги
        :param Xlabel: название оси Х
        :param Ylabel: название оси У
        :param diagram_name: название гистограммы
        :param rectangle_arg: (цвет прямоугольников, цвет границ прямоугольников)
        :param legend_arg: (название легенды, расположение легенды, нарисовать легенду в рамке)
        :param grid_arg: (тип сетки, цвет сетки)
        """
        num_bins = int(self.volume / 7)
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
        ax.set_ylim([0, 1])
        plt.xticks(bins)

        # настройка диаграммы
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.title(diagram_name)
        plt.legend(legend_arg[0], loc=legend_arg[1], frameon=legend_arg[2])
        plt.grid(linestyle=grid_arg[0], color=grid_arg[1])

        plt.show()
