from __future__ import print_function, division
import numpy, time, csv
import matplotlib.pyplot as plt
import scipy.stats.mstats

#INITIALIZATIONS

start_time = time.time()
popn = 1000
locii = 10
total_gen = 100000
generations = list(range(1, (total_gen+1)))

ref_types = []

for i in range(2**locii): #populating  reference array of reference genotypes and epigenotypes
    binaryRepresentation = list(format(i, 'b'))
    finalRepresentation = [['0']*(locii-len(binaryRepresentation)) + binaryRepresentation]
    ref_types = ref_types + finalRepresentation

ref_types =[[int(j) for j in i] for i in ref_types] #converting the string to int in the refernce array

def partition(number, part):
    q1, r1 = divmod(number, part)
    indices = [q1 * i + min(i, r1) for i in xrange(part + 1)]
    lens = [indices[i + 1] - indices[i] for i in range(part)]
    return lens
	
def mutation(allele,freq): #defining mutation function
    temp = numpy.random.rand()
    if temp < freq:
        return(int(not(allele)))
    else:
        return(allele)

  
def individual_cycle(gef, offspring, locii, gfitnessref,efitnessref, ref_types):  
 
    gef_transient = [gef]*offspring #generating transient offspring of an indivdual

    for i1 in range(offspring): 
        for i2 in range(2): # (0 - genome, 1 - epigenome , 2 - fitness)
            for i3 in range(locii): #iterating through locii

                if i2 == 0: #mutation of genome
                    gef_transient[i1][i2][i3] = mutation(gef_transient[i1][i2][i3], 10**-6)

                if i2 == 1:#mutation of epigenome
                    gef_transient[i1][i2][i3] = mutation(gef_transient[i1][i2][i3], 10**-4)
			
        w_g = gfitnessref[ref_types.index(gef_transient[i1][0])] #to compare genotype of individual to reference genotypes and get the genetic fitness
        w_e = efitnessref[ref_types.index(gef_transient[i1][1])] #to compare epigenotype of individual to reference epigenotypes and get the epigenetic fitness
        gef_transient[i1][2] = max(w_g, w_e)
        
    return gef_transient #array of kids of the individual and their genome, epigenome, fitnesses

def iterations(num, gef_small, offspring_small,locii,gfitnessref,efitnessref, ref_types):
    return sum([individual_cycle(gef_small[indiv], offspring_small[indiv],locii,gfitnessref,efitnessref, ref_types) for indiv in range(num)],[])

# ******FOR PARALLEL PROCESSING ************************
import pp
ppservers = ()
ncpus = 8
job_server = pp.Server(ncpus, ppservers=ppservers)
cores = job_server.get_ncpus()  # number of cores/workers being used
inputs = partition(popn, cores)  # Job distribution to each cores

# --------------------------------------------------------
		

avg_w = []  # will have the average fitness of each geenration

#CREATING the fitness landscape for this replication
gfitnessref = [0.1 for i in range((2**locii)-1)] + [1.5]#populating reference arrays of FITNESSES of genotpes and epigenotypes by using binary scheme
efitnessref = [0.1 for i in range((2**locii)-1)] + [1.5]

#populating gef array of first generation of this replication with monomorphic genome, epigenome, and the correspong fitness (0.1, in this case)
gef = [[[0]*locii, [0]*locii, 0.1] for i in range(popn)]

for count in range(total_gen): #LOOP FOR A GENERATIONS WITHIN A SINGLE REPLICATION

    #SCALING THE FITNESSES AND GETTING ARRAY OF OFFSPRING NUMBER
    w_array = [gef[i][2] for i in range(popn)] #populating an array with only the fitnesses of the individuals
    fitness_sum = sum(w_array)
    avg_w += [fitness_sum/popn] #appending to an array of average fitnesses of each generation
    scaling_factor = 1 / fitness_sum  # calculating scaling factor for fitness
    w_scaled = list(map(lambda x: x*scaling_factor, w_array)) #multiplying each fitness by the scaling factor to update this population fitness array for this generation to use in multinomial function
    offspring = numpy.random.multinomial(popn, w_scaled) #generating number of offspring of every individual

    #gef_megatransient=iterations(popn,gef, offspring)
    #parallelisation code - to run individual_cycle on parts of the gef array, which are groups of individuals distributed to the cores
    job1 = [job_server.submit(iterations, (input, gef[sum(inputs[:ii]):sum(inputs[:ii])+input], offspring[sum(inputs[:ii]):sum(inputs[:ii])+input], locii, gfitnessref, efitnessref, ref_types,), (individual_cycle, mutation,), ("numpy",)) for ii, input in enumerate(inputs)]
    gef = sum([i() for i in job1], []) #summing up the offspring ka gef_transient arrays returned by individual_cycle

#POST PROCESSING OF CODE

gm_forward = []
gm_backward = []

for i in range(total_gen-999):

    gm_forward += [scipy.stats.mstats.gmean(avg_w[:(1000 + i)])]
    gm_backward += [scipy.stats.mstats.gmean(avg_w[(99000-i):])]

gm_backward = list(reversed(gm_backward))

with open('avg_fitnesses3.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(avg_w)

with open('gm_forward3.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(gm_forward)

with open('gm_backward3.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(gm_backward)

plt.figure(figsize=(45, 20))
plt.plot(generations, avg_w, 'r', generations[:99001], gm_backward, 'y', generations[999:], gm_forward)
plt.savefig('monomorphic, single peak, forwards+backwards3.png', bbox_inches = 'tight')


print("--- %s seconds ---" % (time.time() - start_time))



        

        

    
