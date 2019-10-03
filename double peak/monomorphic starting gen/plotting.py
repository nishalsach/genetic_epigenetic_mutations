#plotting from csv file

import matplotlib.pyplot as plt
import numpy 

total_gen = 100000

generations = list(range(1, (total_gen)+1))
generations_toplot = generations[1000:]

x1 = generations
y1 = numpy.loadtxt('avg_fitnesses.csv', delimiter = ',')
x2 = generations_toplot
y2 = numpy.loadtxt('gm_forward.csv', delimiter = ',')
y3 = numpy.loadtxt('gm_backward.csv', delimiter = ',')

plt.figure(figsize=(45, 20))
plt.plot(generations, y1, 'r', generations[1000:], y2, 'b', generations[:99000], y3, 'y')
#plt.show()
plt.savefig('monomorphic, double peak, forwards+backwards.png', bbox_inches = 'tight')
