import openpyxl
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f

class Sample:
    def __init__(self, path_arg):

        self.path = path_arg
        self.volume = None
        # все значения из выборки
        self.X = None
        self.Y = None
        # Элементы абсоютно меньше 3
        self.Xselected = None
        self.Yselected = None
        # математическое ожидание
        self.Xmean = None
        self.Ymean = None
        # среднеквадратическое отклонение
        self.Xstd = None
        self.Ystd = None
        # дисперсия (сумма моментов)
        self.Xvariance = None
        self.Yvariance = None
        # коэффиуиенты уравнения регрессии
        self.a = None
        self.b = None
        # линейный коэффиуиент корреляции между X и Y
        self.correlation = None
        # коэффициент детерминации
        self.determination = None
        #коэффициент множественной корреляции
        self.R = None

        self.__create_data()
        self.__create_volume()
        self.__create_moments()

    def __create_data(self):
        """
        считывает выборку с excel файла и заносит в массив X и Y
        функция create_data() заполняет список self.X значениями X из выборки, и self.Y - значениями Y
        """
        # считываем данные
        self.X = []
        self.Y = []
        book = openpyxl.open(self.path)
        sheet = book.active

        read_X = True

        for col in sheet.iter_cols(min_row=2, min_col=1, max_col=2):
            for cell in col:
                if read_X:
                    self.X.append(cell.value)
                else:
                    self.Y.append(cell.value)
            read_X = False

    def __create_volume(self):
        self.volume = len(self.X)

    def __create_moments(self):
        """вычисляет мат ожидание, дисперсию и среднеквадратическое"""
        self.Xmean = sum(self.X) / self.volume
        self.Ymean = sum(self.Y) / self.volume

        self.Xvariance = sum([i**2 for i in self.X]) / self.volume - (self.Xmean)**2
        self.Yvariance = sum([i ** 2 for i in self.Y]) / self.volume - (self.Ymean) ** 2

        self.Xstd = (self.Xvariance)**0.5
        self.Ystd = (self.Yvariance)**0.5

    def print_momenets(self):
        if self.Xmean is None:
            self.__create_moments()

        print("Для объясняющей переменной:")
        print("""
        мат ожидание = {}
        дисперсия = {}
        среднеквадратическое отклонение = {}
        """.format(self.Xmean, self.Xvariance, self.Xstd))

        print("Для переменной отклика:")
        print("""
        мат ожидание = {}
        дисперсия = {}
        среднеквадратическое отклонение = {}
        """.format(self.Ymean, self.Yvariance, self.Ystd))

    def __find_a_b(self):
        """
        находит коэффиуиенты a и b для уравнения линейной регрессии y = ax + b
        """
        meanXY = sum(self.X[i] * self.Y[i] for i in range(self.volume)) / self.volume
        meanXsqr = sum((x)**2 for x in self.X) / self.volume

        self.a = (meanXY - self.Xmean*self.Ymean) / (meanXsqr - (self.Xmean)**2)
        self.b = (self.Ymean * meanXsqr - self.Xmean * meanXY) / (meanXsqr - (self.Xmean)**2)

    def print_equation(self):
        if self.a is None:
            self.__find_a_b()
        print("уравнение регрессии имеет вид: y = {}x + ({})".format(np.round(self.a, 2), np.round(self.b, 2)))

    def __find_correlation(self):
        """
        находит линейный коэффиуиент кореляуии для объяснительной переменной и переменной отклика
        """

        # среднее x*y
        XYmean = sum(self.X[i] * self.Y[i] for i in range(self.volume)) / self.volume

        self.correlation = (XYmean - self.Xmean * self.Ymean) / (self.Xstd * self.Ystd)

    def print_correlation(self):
        if self.correlation is None:
            self.__find_correlation()

        print("коэффициент корреляции = {}".format(self.correlation))

    def regression(self, x):
        """
        вычисляет знаяение фкнкции регрессии от x, т.е. F(x) = ax + b, где
        a = self.a
        b = self.b
        :param x: аргумент функуии
        :return: значение уравнения регресси ax + b при определенном x
        """
        return self.a * x + self.b

    def __find_determonation(self):
        """
        высчитывает коэффиуиент детерминауии self.determination
        показвает насколько точно уравнение регресии отображает выборку
        """
        if self.a is None:
            self.__find_a_b()

        # сумма квадратных отклонений
        Ry = [self.regression(x) for x in self.X]
        Ey = sum(Ry) / self.volume

        Syy = sum((y -  self.Ymean)**2 for y in self.Y)
        SYY = sum((ry -  Ey)**2 for ry in Ry)
        SyY = sum((self.Y[i] - self.Ymean) * (Ry[i] - Ey) for i in range(self.volume))

        # коэффиуиент детерминации
        self.determination = (SyY ** 2) / (Syy * SYY)

        # коэффициент множественной корреляции
        self.R = self.determination ** 0.5

    def print_det(self):
        if self.determination is None:
            self.__find_determonation()
        print("коэффициент детерминации: {}".format(self.determination))

    def print_factf(self, p=95):
        """
        Расчитывает фактический и истинный критерий Фишера
        """
        SUM1 = sum((self.regression(x) - self.Ymean)**2 for x in self.X)
        SUM2 = sum((self.Y[i] - self.regression(self.X[i]))**2 for i in range(self.volume))

        F = SUM1/(SUM2/(self.volume - 2))
        print("Истинный критерий Фишера: {}".format(F))
        print("Табличный критерий Фишера (с вероятностью 0,95): {}".format(f.ppf(p / 100, dfn=1, dfd=self.volume - 2)))

    def __interval_inf(self, arg, p=95):
        """
        вычисляет ширину доаерительного интервала около регрессии в точке (x, regression(x))
        :param arg: аргусент в regression()
        :param p: доверительная вероятность/коэффициент доверия (%) 0 <= p <= 100
        :return: ширина половины интервала (слева и справа от линии регрессии) в точке (x, ax+b)
        """
        if self.a is None:
            self.__find_a_b()

        # значение F-распределения с вероятностью p
        F = f.ppf(p / 100, dfn=1, dfd=self.volume - 2)

        # сумма квадратов отклонений х
        Sxx = sum((x - self.Xmean)**2 for x in self.X)
        # сумма квадратов отелонений y от прогнозируемого y
        Se = sum((self.Y[i] - self.regression(self.X[i]))**2 for i in range(self.volume))
        # расстояние слева/спарва от регрессии
        st = F * (1 / self.volume + (arg - self.Xmean) ** 2 / Sxx) * (Se / (self.volume - 2))
        delta = st**0.5

        # значение ax + b
        y = self.a * arg + self.b
        up_y = y - delta
        down_y = y + delta

        return up_y, down_y

    def predictf(self, x, p):
        up, down = self.__interval_inf(x, p)

        print("При X = {} значение Y будет равняться от {} до {} с доверительной вероятностью {}%".format(x, np.round(up,1), np.round(down, 1), p))

    def draw_dot_graph(self, x_arg = None, y_arg = None, x_p=None):
        """
        рисует точечную диаграмму по элементам выборки X и Y
        :param x_arg: по умолчанию self.X, хотя можно поставить и для отобранных X
        :param y_arg:
        """
        if self.a is None:
            self.__find_a_b()

        if x_arg is None:
            x_arg = self.X
            y_arg = self.Y

        # точечная диаграмма
        plt.scatter(x_arg, y_arg, color="#6495ED")

        # линия регрессии
        plt.plot(self.X, [self.regression(x) for x in self.X], label="регрессия", color="#FF5733")

        plt.title("Точечная Диаграмма")
        plt.xlabel("Объясняющая переменная")
        plt.ylabel("Переменная отклика")
        plt.legend()
        plt.show()
