#plotting from csv file

import matplotlib.pyplot as plt
import numpy 

total_gen = 100000

generations = list(range(1, (total_gen)+1))


y1 = numpy.loadtxt('avg_fitnesses2.csv', delimiter = ',')
y2 = numpy.loadtxt('gm_forward2.csv', delimiter = ',')
y3 = numpy.loadtxt('gm_backward2.csv', delimiter = ',')

print(len(y1), len(y2), len(y2))
plt.figure(figsize=(45, 20))
plt.plot(generations, y1, 'r', generations[:99001], y3, 'y', generations[999:], y2, 'b')
plt.show()
#plt.savefig('monomorphic, single peak, forwards+backwards.png', bbox_inches = 'tight')
