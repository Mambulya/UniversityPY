from SampleClass import Sample
import numpy as np
import statistics
from collections import Counter

Sample1 = Sample("./data.xlsx")
Sample1.print_moments()
Sample1.get_frequency()


print("TEST:")
print("Q1 = {}".format(np.quantile(Sample1.data, 0.25)))
print("Q3 = {}".format(np.quantile(Sample1.data, 0.75)))
print("M = {}".format(np.mean(Sample1.data)))
print("Dx = {}".format(np.var(Sample1.data)))
print("б = {}".format(np.std(Sample1.data)))
print("мода = {}".format(statistics.mode(Sample1.data)))
print("interquile latitude = {}".format(np.percentile(Sample1.data, 75, interpolation='higher') - np.percentile(Sample1.data, 25, interpolation='lower')))

# проверка единственности моды
print("\nСамые частые знвчения")
k = Counter(Sample1.frequencies)
high = k.most_common(3)
print(high)
