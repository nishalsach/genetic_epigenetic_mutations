#to get values of kink

import matplotlib.pyplot as plt
import numpy
import csv

total_gen = 100000

generations = list(range(1, (total_gen)+1))

y1 = numpy.loadtxt('avg_fitnesses.csv', delimiter = ',')
y1 = y1[8000:12000]

with open('avg_fitness_kink.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(y1)