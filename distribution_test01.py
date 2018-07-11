#%%
import os, sys
import scipy.stats
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

dir = '/Users/michaelshih/Documents/code/personal_project/Ripleys_K_function_test/'
os.chdir(dir)

import imp
import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)


#%%
# ----------------------------------------------------------------------------
# make plot
import seaborn as sns
# sns.set_style("white")
# reset style 
sns.reset_orig()

# define the size of the canvas
plt.figure(figsize= (10, 10))
plotsize_x = 20.0
plotsize_y = 20.0

plot_1 = plt.subplot(221)
# create simulation
rate = 1/400
Dx = 20
seed = 1000
P = sswdistsim.PoissonPP(rate, Dx).T
np.random.seed(seed=1223)

N = scipy.stats.poisson(rate*Dx*Dx).rvs()
print(N)

plot_1.scatter(P[0], P[1], edgecolor = 'r', marker = '.', facecolor='none', alpha =0.7)
plot_1.set_xlim((0, 20))
plot_1.set_ylim((0, 20))


plot_2 = plt.subplot(222)
rate = 0.2
Dx = 20
P = sswdistsim.PoissonPP(rate, Dx).T
plt.scatter(P[0], P[1], edgecolor = 'b', facecolor='none', alpha =0.7)
plot_2.set_xlim((0, 20))
plot_2.set_ylim((0, 20))


plt.show()