#to generate random numbers and plot them

import numpy, time, csv
import matplotlib.pyplot as plt
import scipy.stats.mstats

random_nos = [numpy.random.uniform(0, 2) for i in range(100000)]

total_gen = 100000
generations = list(range(1, (total_gen)+1))

gm_forward = []
gm_backward = []

for i in range(total_gen-1000):

    gm_forward += [scipy.stats.mstats.gmean(random_nos[0:(999 + i)])]
    gm_backward += [scipy.stats.mstats.gmean(random_nos[(89999-i):])]

gm_backward = list(reversed(gm_backward))

plt.figure(figsize=(45, 20))
plt.plot(generations[:99000:10], gm_backward[::10], 'r', )
plt.savefig('uniform2.png', bbox_inches = 'tight')