#%%
import os, sys
import scipy.stats
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time
import imp
import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

path = '/Users/michaelshih/Documents/code/personal_project/Ripleys_K_function_test/'
os.chdir(path)

#%%
# load file
subfolder = 'output'
subfolder_type = 'csv'
filename = 'P_ThomasPP_256'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_ThomasPP = pd.read_csv(inputpath)
P_ThomasPP = np.array(P_ThomasPP)

filename = 'P_PoissonPP_256'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_PoissonPP = pd.read_csv(inputpath)
P_PoissonPP = np.array(P_PoissonPP)

#%%
# Ripley's K-function ----------------------------------
import imp
import spatialstatWUCCI.ripleyk_v3 as ripleyk_v3
imp.reload(ripleyk_v3)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)
#%%
# 1. ThomasPP ------------------------------------------
rmax = 5
Dx = 256
Dy = 256
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = Dx) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v3.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print(end - start)
'''
print(RList)
print(K_r)
print(L_r)
print(H_r)
print(densitylist)
'''
# %%
# plot
plt.figure(figsize= (10, 10))
plotsize_x = 20.0
plotsize_y = 20.0

plot_1 = plt.subplot(221)
plot_1.plot(RList, K_r)
plot_2 = plt.subplot(222)
plot_2.plot(RList, L_r)
plot_3 = plt.subplot(223)
plot_3.plot(RList, H_r)

