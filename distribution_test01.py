# In distribution_test01, the script generates 
# 1: a <Nx2> array with Thomas Point Process by using ThomasPP
# 2: a <Nx2> array with Poisson Point Process by using PoissonPP
# 3: a <Nx2> array with Poisson-disc Sampling

# Random numbers can be controlled by seeding. 
# By Chien-cheng Shih (Mike)

#%%
import os, sys
import scipy.stats
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time

path = '/Users/michaelshih/Documents/code/personal_project/Ripleys_K_function_test/'
os.chdir(path)
outputfolder = 'output'
outputsubfolder_csv = 'csv'
outputsubfolder_figure = 'figure'

#%%
import imp
import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

#%% 
# Part 1: generating simulated data points ---------------------------------
# 1-1 generated a <Nx2> array by ThomasPP
# creating parent points
seed = 1219

rate = 0.1
Dx = 20
P_parent = sswdistsim.PoissonPP(rt = rate, Dx = Dx, seed = seed)

# creating children points
sigma = 0.3
mu = 50
P_children = sswdistsim.ThomasPP(rt = rate, Dx = Dx, 
                                sigma = sigma, mu = mu, seed = seed)
# reduce data to region of interest
xmin = 0 
xmax = Dx
ymin = 0
ymax = Dx

# crop data and calculate density
P_ThomasPP = sswdistsim.xyroi(P_children, xmin, xmax, ymin, ymax)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP) 

# print(P_ThomasPP.shape[0])
# print(P_ThomasPP_density)

# save to csv
filename = 'P_ThomasPP_20'
outputpath = os.path.join(path, outputfolder, outputsubfolder_csv, filename + '.csv')
df = pd.DataFrame(P_ThomasPP, columns = ['x', 'y']) 
df.to_csv(outputpath, index = False)

# save metadata
outputpath = os.path.join(path, outputfolder, outputsubfolder_csv, filename + '.txt')
with open(outputpath, 'w') as file: 
    file.write('Filename: {}.csv\n'.format(filename))
    file.write('Counts: {}\n'.format(P_ThomasPP.shape[0]))
    file.write('Density {:.2f} (counts/area)\n'.format(P_ThomasPP_density))
    file.write('Data range in x-axis: {0} - {1}\n'.format(xmin, xmax))
    file.write('Data range in y-axis: {0} - {1}\n'.format(ymin, ymax))
    file.close()

# 1-2 generated a <Nx2> array by PoissonPP
rate = 5
Dx = 20

# set data range
xmin = 0 
xmax = Dx
ymin = 0
ymax = Dx

P_PoissonPP = sswdistsim.PoissonPP(rt = rate, Dx = Dx, seed = seed)
# calculate density
P_PoissonPP_density = sswdistsim.xydensity(P_PoissonPP) 


# save to csv
filename = 'P_PoissonPP_20'
outputpath = os.path.join(path, outputfolder, outputsubfolder_csv, filename + '.csv')
df = pd.DataFrame(P_PoissonPP, columns = ['x', 'y']) 
df.to_csv(outputpath, index = False)

# save metadata
outputpath = os.path.join(path, outputfolder, outputsubfolder_csv, filename + '.txt')
with open(outputpath, 'w') as file: 
    file.write('Filename: {}.csv\n'.format(filename))
    file.write('Counts: {}\n'.format(P_PoissonPP.shape[0]))
    file.write('Density {:.2f} (counts/area)\n'.format(P_PoissonPP_density))
    file.write('Data range in x-axis: {0} - {1}\n'.format(xmin, xmax))
    file.write('Data range in y-axis: {0} - {1}\n'.format(ymin, ymax))
    file.close()

# 1-3 generated a <Nx2> array by ThomasPP (dispersed)



#%%
# Part 2: Ploting ------------------------------------------------------------
# set figure size
plt.figure(figsize= (10, 10))
plotsize_x = 20.0
plotsize_y = 20.0

# subplot 1
plot_1 = plt.subplot(221)
plot_1.scatter(P_children[:, 0], P_children[:, 1], 
                color = 'b', edgecolors = 'none', marker = '.', alpha =0.3)
plot_1.set_title('ThomasPP')

# subplot 2
plot_2 = plt.subplot(222)
plot_2.scatter(P_PoissonPP[:, 0], P_PoissonPP[:, 1], 
                color = 'b', edgecolors = 'none', marker = '.', alpha =0.3)
plot_2.set_title('PoissonPP')

# save figure
filename = 'Point_Process_20'
outputpath = os.path.join(path, outputfolder, outputsubfolder_figure, filename + '.png')
plt.savefig(outputpath)

plt.show()