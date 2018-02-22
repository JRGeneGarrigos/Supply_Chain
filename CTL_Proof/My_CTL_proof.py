import numpy as np
import matplotlib.pyplot as plt

# 1- Create synthetic data with 6 different distributions
one = np.random.rand(1000000) # Uniform U(0,1), n = 1,000,000
two = np.random.chisquare(1, 1000000) # Chisquare (df=1), n = 1,000,000
three = np.random.gamma(2, 2, 1000000) # Gamma (2, 2), n = 1,000,000
four = np.random.laplace(1, 1, 1000000) # Laplace (1, 1), n = 1,000,000
five = np.random.negative_binomial(1, 0.1, 1000000) # Binomial (1, 0.1), n = 1,000,000)
six = np.random.poisson(5, 1000000) # Poisson (5), n=1,000,000)

population = np.zeros(6000000)
n = len(population)
i = 0
j = 0

# 2- Filling the population with the synthetic data of 6 distributions
while i < n:
    population[i] = one[j]
    i += 1
    population[i] = two[j]
    i += 1
    population[i] = three[j]
    i += 1
    population[i] = four[j]
    i += 1
    population[i] = five[j]
    i += 1
    population[i] = six[j]
    i += 1
    j += 1

# 3- Define the number of measures of each sample (sample_size),
#    and the number of samples (number_samples).
sample_size = 100 # should be higher that 30
number_samples = 100 # law of large numbers, as higher more accuracy

# 4- Defining the sample means array
# x is the sample means array, which has length 'number_samples'.
# Calculates the int mean of each sample. where each sample is filled randomly
# with 'sample_size' values of the population array defined previously. 
x = np.around([np.random.choice(population,size=sample_size,replace=False).mean()
                  for i in range(number_samples)], decimals=1)

# 5- plotting the results as a histogram.
# We get a Normal distribution.
# Incresing the 'number_samples' we obtein more accurary, but takes longer to 
# be computedl.
hist, bins = np.histogram(x, bins=20)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()

