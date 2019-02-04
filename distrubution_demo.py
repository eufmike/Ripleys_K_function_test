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

# %%
p = sswdistsim.PoissonPP(0.6, ndimension = 2)
print(p)

# %%
# plot 2D
rangelim = np.array([[0, 20], [10, 30]])
p = sswdistsim.PoissonPP(0.1, ndimension=2, rangelim = rangelim, seed = 100, seedmodifier = 2)
print(p)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(p[:, 0], p[:, 1],  alpha = 0.5)
plt.show()

# %% 
# plot 3D
rangelim = np.array([[0, 20], [10, 30], [20, 40]])
p = sswdistsim.PoissonPP(0.1, ndimension=3, rangelim = rangelim, seed = 100, seedmodifier = 2)
print(p)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(p[:, 0], p[:, 1], p[:, 2],  alpha = 0.5)
plt.show()
# %%
p = sswdistsim.PoissonPP(0.6, ndimension = 4)
print(p)
# %%
p = sswdistsim.PoissonPP(1, N = 10)
print(p)

# %%
p = sswdistsim.ThomasPP(0.3, 0.3, 30, ndimension = 2, seed = 1999)
print(p)
plt.figure(figsize = [5, 5])
plt.scatter(p[:,0], p[:,1], alpha = 0.3, s = 10)
plt.show

# %%
p = sswdistsim.ThomasPP(0.01, 0.5, 30, ndimension = 3, seed = 1999)
print(p)

# %%
print(p.shape)

# %%
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(p[:, 0], p[:, 1], p[:, 2],  alpha = 0.5)
plt.show()
