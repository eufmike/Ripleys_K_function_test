# %%
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

filenames = []
version_list = []
time_list = []

# %%
# load file
subfolder = 'output'
subfolder_type = 'csv'
filename = 'P_ThomasPP_20'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_ThomasPP = pd.read_csv(inputpath)
P_ThomasPP = np.array(P_ThomasPP)

# %%
# ripleyk_v5
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v5 as ripleyk_v5
imp.reload(ripleyk_v5)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# ThomasPP test --------------------------------------
P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, 5, 15, 5, 15)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density, count, area = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 
print('Density: {}'.format(P_ThomasPP_density))
print('Count: {}'.format(count))
print('Area: {}'.format(area))

# %%
start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v5.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v5')
time_list.append(end - start)

# %%
plt.figure(figsize= (5, 10))
plot_1 = plt.subplot(311)
plot_1.plot(RList, K_r)
plot_1 = plt.subplot(312)
plot_1.plot(RList, L_r)
plot_1 = plt.subplot(313)
plot_1.plot(RList, H_r)
plt.show




#################################################################


# %%
# ----------------------------------
# localL_v1: multiple r
# ----------------------------------
import spatialstatWUCCI.localL_v1 as localL_v1
imp.reload(localL_v1)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

outputfolder = 'output'

# --------------------------------------
rmax = 5
Dx = 20
Dy = 20
imgsize = Dx * Dy
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
localK_r, localL_r, localH_r, RList, countlist= localL_v1.localL(xyarray_ref = P_ThomasPP_center, 
                    xyarray_all = P_ThomasPP, 
                    square_size = imgsize,
                    rstart = 0, rend = 5, rstep = 0.01)

end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v2')
time_list.append(end - start)


# %%
print(localK_r)
print(localL_r)

# %%
print(localK_r.shape[0])

# make plot
# %%
plt.figure(figsize= (5, 10))
plot_1 = plt.subplot(311)
for i in range(localK_r.shape[0]):
    plot_1.plot(RList, localK_r[i, :])
plot_1 = plt.subplot(312)
for i in range(localK_r.shape[0]):
    plot_1.plot(RList, localL_r[i, :])
plot_1 = plt.subplot(313)
for i in range(localK_r.shape[0]):
    plot_1.plot(RList, localH_r[i, :])
plt.show

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': filenames,
    })
display(results)