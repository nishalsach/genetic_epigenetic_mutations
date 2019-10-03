#plotting from csv file

import matplotlib.pyplot as plt
import numpy, math, scipy.stats

total_gen = 150000

generations = list(range(1, (total_gen)+1))

y1 = numpy.loadtxt('gm_lastthousand.csv', delimiter = ',')
y2 = numpy.loadtxt('maxwdiff_gen.csv', delimiter = ',')

amofgms = numpy.mean(y1)
seomofgms = scipy.stats.sem(y1)

      
plt.figure(figsize=(45, 20))

#PLOTTING

plt.plot(generations, y1, 'r', generations[999:], y2, 'b') # #generations[:99001], y3, 'y',
plt.savefig('monomorphic, single peak, forwards+backwards.png', bbox_inches = 'tight')

 #getting satURATION POint

y2 = numpy.ndarray.tolist(y2)

#for i in range(len(y2)):
   # if y2[i] > 1.41:
     #   y2[i] = 1.41

for i in range(len(y2)):
    y2[i] = truncate(y2[i], 2)

saturation_gm = y2.index(max(y2)) + 1000
#print(y2.index(max(y2)))

f = open('post-proc.txt', 'w+')
f.write("Index of generation w/greatest change in avg fitness: %d \n Generation with satn value of gm: %d" % (maxwdiff_gen, saturation_gm))
f.close
                            
