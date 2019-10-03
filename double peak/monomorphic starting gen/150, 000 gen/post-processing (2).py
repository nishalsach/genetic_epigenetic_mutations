#plotting from csv file

import matplotlib.pyplot as plt
import numpy, math

total_gen = 150000

generations = list(range(1, (total_gen)+1))

def truncate(f, n):
    return math.floor(f * 10**n)/ 10**n

y1 = numpy.loadtxt('avg_fitnesses2.csv', delimiter = ',')
y2 = numpy.loadtxt('gm_forward2.csv', delimiter = ',')
#y3 = numpy.loadtxt('gm_backward2.csv', delimiter = ',')

#GETTING GENERATION WHERE SUDDEN CHANGE IN GM AND AVG FITNESS OCCURS

w_diff = [0]
gm_diff = [0]

for i in range(len(y1)-1):
    w_diff += [y1[i+1] - y1[i]]

#for i in range(len(y2)-1):
#    gm_diff += [y2[i+1] - y2[i]]

maxwdiff_gen = w_diff.index(max(w_diff))
#maxgmdiff_gen = gm_diff.index(max(gm_diff)) + 1000
      
plt.figure(figsize=(45, 20))

#PLOTTING

plt.plot(generations, y1, 'r', generations[999:], y2, 'b') # #generations[:99001], y3, 'y',
plt.savefig('monomorphic, multi peak, forwards+backwards2.png', bbox_inches = 'tight')

 #getting satURATION POint

y2 = numpy.ndarray.tolist(y2)

#for i in range(len(y2)):
   # if y2[i] > 1.41:
     #   y2[i] = 1.41

for i in range(len(y2)):
    y2[i] = truncate(y2[i], 2)

saturation_gm = y2.index(max(y2)) + 1000
#print(y2.index(max(y2)))

f = open('post-proc2.txt', 'w+')
f.write("Index of generation w/greatest change in avg fitness: %d \n Generation with satn value of gm: %d" % (maxwdiff_gen, saturation_gm))
f.close
                            
