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

'''
filename = 'P_PoissonPP_20'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_PoissonPP = pd.read_csv(inputpath)
P_PoissonPP = np.array(P_PoissonPP)
'''

outputfolder = 'output'
# %%
# ripleyk_v2
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v2 as ripleyk_v2
imp.reload(ripleyk_v2)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# 1. ThomasPP test --------------------------------------
P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, 5, 15, 5, 15)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v2.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v2')
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

# %%
# ripleyk_v3
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v3 as ripleyk_v3
imp.reload(ripleyk_v3)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# 1. ThomasPP test --------------------------------------
P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, 5, 15, 5, 15)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v3.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v3')
time_list.append(end - start)
# %%
# ripleyk_v4
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v4 as ripleyk_v4
imp.reload(ripleyk_v4)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# 1. ThomasPP test --------------------------------------
P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, 5, 15, 5, 15)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v4.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v4')
time_list.append(end - start)

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': 'P_ThomasPP_20',
    })
display(results)


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
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

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










# %%
## 256 size --------------------------------------
# load file
subfolder = 'output'
subfolder_type = 'csv'
filename = 'P_ThomasPP_256'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_ThomasPP = pd.read_csv(inputpath)
P_ThomasPP = np.array(P_ThomasPP)

import spatialstatWUCCI.ripleyk_v2 as ripleyk_v2
imp.reload(ripleyk_v2)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# %%
# ripleyk_v2
# ThomasPP test --------------------------------------
rmax = 5
Dx = 256
Dy = 256
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v2.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_256')
version_list.append('ripleyk_v2')
time_list.append(end - start)

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': 'P_ThomasPP_256',
    })
display(results)

# %%
'''
# ripleyk_v3
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v3 as ripleyk_v3
imp.reload(ripleyk_v3)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# ThomasPP test --------------------------------------
rmax = 5
Dx = 256
Dy = 256
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v3.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

version_list.append('ripleyk_v3')
time_list.append(end - start)

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': 'P_ThomasPP_20',
    })
display(results)
'''

# %%
# ripleyk_v4
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v4 as ripleyk_v4
imp.reload(ripleyk_v4)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# ThomasPP test --------------------------------------
rmax = 5
Dx = 256
Dy = 256
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v4.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_256')
version_list.append('ripleyk_v4')
time_list.append(end - start)

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': filenames,
    })
display(results)



##=====================================================












##=====================================================

# %%
# ripleyk_v5
# Ripley's K-function ----------------------------------
import spatialstatWUCCI.ripleyk_v5 as ripleyk_v5
imp.reload(ripleyk_v5)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

# ThomasPP test --------------------------------------
rmax = 5
Dx = 256
Dy = 256
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

# %%
P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v5.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01, 
                        downsize = True)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_256')
version_list.append('ripleyk_v5')
time_list.append(end - start)


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


# %%
P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
K_r, L_r, H_r, RList, densitylist = ripleyk_v5.ripleyk(xyarray_ref = P_ThomasPP_center, 
                        xyarray_all = P_ThomasPP,
                        function = 'all', 
                        density = P_ThomasPP_density, 
                        rstart = 0, rend = 5, rstep = 0.01, 
                        downsize = False)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_256')
version_list.append('ripleyk_v5')
time_list.append(end - start)

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

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': filenames,
    })
display(results)


##=====================================================



# localK and localL 















##=====================================================


# %% 
# reload package
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

## Test localL
##=====================================================
# %%
# load file
subfolder = 'output'
subfolder_type = 'csv'
filename = 'P_ThomasPP_20'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_ThomasPP = pd.read_csv(inputpath)
P_ThomasPP = np.array(P_ThomasPP)

# ----------------------------------
# localL_v1: single r
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
localK_r, localL_r, localH_r, RList, countlist, xyarray_ref= localL_v1.localL(xyarray_ref = P_ThomasPP_center, 
                    xyarray_all = P_ThomasPP, 
                    square_size =imgsize,
                    r = 1)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v2')
time_list.append(end - start)

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': filenames,
    })
display(results)

# %%
print(localK_r)
print(localL_r)
print(xyarray_ref)
# %%
# make plot
plt.figure(figsize= (5, 5))
plot_1 = plt.subplot(111)
plot_1.scatter(xyarray_ref[:, 0], xyarray_ref[:, 1], c = localL_r[:, 0])
plt.show


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
                    square_size =imgsize,
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




# %%
# load file
subfolder = 'output'
subfolder_type = 'csv'
filename = 'P_ThomasPP_256'
inputpath = os.path.join(path,subfolder, subfolder_type, filename + '.csv')
P_ThomasPP = pd.read_csv(inputpath)
P_ThomasPP = np.array(P_ThomasPP)

# ----------------------------------
# localL_v1: single r
# ----------------------------------
import spatialstatWUCCI.localL_v1 as localL_v1
imp.reload(localL_v1)

import spatialstatWUCCI.distribution_simulator as sswdistsim
imp.reload(sswdistsim)

outputfolder = 'output'

# --------------------------------------
rmax = 5
Dx = 256
Dy = 256
imgsize = Dx * Dy
xmin = 0 + rmax
xmax = Dx - rmax
ymin = 0 + rmax
ymax = Dx - rmax

P_ThomasPP_center = sswdistsim.xyroi_idx(P_ThomasPP, xmin, xmax, ymin, ymax)
# P_ThomasPP_center = sswdistsim.xyroi(P_ThomasPP, 0, 20, 0, 20)
P_ThomasPP_density = sswdistsim.xydensity(P_ThomasPP, Dx = 20) 

start = time.time()
localK_r, localL_r, localH_r, RList, countlist, xyarray_ref= localL_v1.localL(xyarray_ref = P_ThomasPP_center, 
                    xyarray_all = P_ThomasPP, 
                    square_size =imgsize,
                    r = 5)
end = time.time()
print('processing time: {}'.format(end - start))

filenames.append('P_ThomasPP_20')
version_list.append('ripleyk_v2')
time_list.append(end - start)

# %%
results = pd.DataFrame({
    'version': version_list,
    'time': time_list, 
    'file': filenames,
    })
display(results)

# %%
print(localK_r)
print(localL_r)
print(xyarray_ref)
# %%
# make plot
plt.figure(figsize= (5, 5))
plot_1 = plt.subplot(111)
plot_1.scatter(xyarray_ref[:, 0], xyarray_ref[:, 1], c = localL_r[:, 0], s = 9)
plt.show