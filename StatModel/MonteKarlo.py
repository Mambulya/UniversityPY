"""
Метод Монте-Карло

Условие: бросают д20. Вигрыш при проске >16. Вычислить вероятность виграша. Бросков 10000
Теоретическая вероятность P = 0,25

"""
from random import randint
import matplotlib.pyplot as plt

def win():
    dice = randint(1, 20)
    return int(dice >= 16)

# experiment
throws = 1000
probability = 0
wins = 0

xs = []
ys = []
yprobability = [0.25]*throws

for throw in range(1, throws + 1):
    res = win()
    wins += res
    probability = wins / throw

    xs.append(throw)
    ys.append(probability)

plt.plot(xs, ys, color="red", label="экспериментальная P")
plt.plot(xs, yprobability, color = "green", linestyle="--", label="теоретическая P")
plt.title("Вероятность броска больше 15")
plt.ylabel("Вероятность P")
plt.xlabel("Бросок")
plt.grid()
plt.legend()
plt.ylim(0, 1)

plt.show()
