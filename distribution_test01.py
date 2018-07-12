#%%
import os, sys
import scipy.stats
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

dir = '/Users/michaelshih/Documents/code/personal_project/Ripleys_K_function_test/'
os.chdir(dir)

#%%
import imp
import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# ----------------------------------------------------------------------------
# make plot
import seaborn as sns
# sns.set_style("white")
# reset style 
sns.reset_orig()

# set seed for simulation
seed = 1219

# define the size of the canvas
plt.figure(figsize= (10, 10))
plotsize_x = 20.0
plotsize_y = 20.0

# plot 1
plot_1 = plt.subplot(221)
# create simulation
rate = 1/200
Dx = 20
P = sswdistsim.PoissonPP(rt = rate, Dx = Dx, seed = seed).T

plot_1.scatter(P[0], P[1], edgecolor = 'r', marker = '.', facecolor='none', alpha =0.7)
plot_1.set_xlim((0, 20))
plot_1.set_ylim((0, 20))

# plot 2
plot_2 = plt.subplot(222)
# create simulation
rate = 1/200
Dx = 20
sigma = 0.3
mu = 15
P = sswdistsim.ThomasPP(rt = rate, Dx = Dx, sigma = sigma, mu = mu, seed = seed)

Dy = Dx
N = scipy.stats.poisson(rate*Dx*Dy).rvs(random_state=seed)
print('Dx test = {}'.format(Dx))
print('Dy test = {}'.format(Dy))
print('N test = {}'.format(N))

plt.scatter(P[0], P[1], edgecolor = 'b', facecolor='none', alpha =0.7)
plot_2.set_xlim((0, 20))
plot_2.set_ylim((0, 20))

plt.show()

#%%
seed = 1219
mu = 15
sigma = 0.3
i = [0, 0]
pdf = scipy.stats.norm(loc = i, scale = (sigma, sigma))
N = scipy.stats.poisson(mu).rvs(random_state=seed)
XYP = list(pdf.rvs(2, random_state = seed))
print(XYP)