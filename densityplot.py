#%%
# libraries
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
 
# create data
x = np.random.normal(loc= 0, scale = 0.2, size=400)
y = x * 2 + np.random.normal(loc= 0, scale = 0.2, size=400)

plt.figure(figsize=(10,10))
plt.scatter(x, y, c = 'b', marker = '.')
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()

#%%
import time

#%%
# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents


nbins=1000
k = scipy.stats.gaussian_kde([x,y])
xi, yi = np.mgrid[-1:1:nbins*1j, -1:1:nbins*1j]
print(np.vstack([xi.flatten(), yi.flatten()]))
xi1 = xi.flatten()
yi1 = yi.flatten()

start = time.time()
zi = k(np.vstack([xi1, yi1]))
end = time.time()
print(zi)

print(end-start)
#%%
# Make the plot
plt.figure(figsize=(10,10))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.plasma)
plt.show()

#%%
space = 1000

xi = np.linspace(-1, 1, space+1)
yi = np.linspace(-1, 1, space+1)
Xi, Yi = np.meshgrid(xi, yi)
k = scipy.stats.gaussian_kde([x,y])
Zi = k(np.vstack([Xi.flatten(), Yi.flatten()]))
print(Zi)

plt.figure(figsize=(10,10))
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.pcolormesh(Xi, Yi, Zi.reshape(Xi.shape), cmap=plt.cm.plasma)
plt.show()

#%%
import seaborn as sns
plot = sns.kdeplot(x, y, shade=True)
plot.figure(figsize=(10,10))
plot.xlim(-1, 1)
plot.ylim(-1, 1)
plot.show()