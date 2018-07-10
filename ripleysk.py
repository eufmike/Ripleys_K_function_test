#%%
import pickle
import scipy.stats
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#%%
def PoissonPP(rt, Dx, Dy = None):
    '''
    Determines the number of events 'N' for a rectangular region,
    given the rate 'rt' and the dimensions, 'Dx', 'Dy'.
    Returns a <2xN> NumPy array.
    '''
    if Dy == None:
        Dy = Dx
    N = scipy.stats.poisson(rt*Dx*Dy).rvs()
    x = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)))
    y = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)))
    P = np.hstack((x, y))
    return(P)

rate, Dx = 0.05, 20
P = PoissonPP(rate, Dx).T
plt.figure(figsize=(10,10))
plt.scatter(P[0], P[1], edgecolor = 'b', facecolor='none', alpha =0.3)
plt.show()

#%%
def ThomasPP(kappa, sigma, mu, Dx):
    '''
    each forming a Poisson (mu) numbered cluster of points,
    having an isotropic Gaussian distribution with variance 'sigma'
    '''
    # Create a set of parent points form a Poisson(kappa)
    # distribution on the square region [0, Dx] * [0, Dx]
    parents = PoissonPP(kappa, Dx)
    # M is the number of parents
    M = parents.shape[0]
    # an empty list for the Thomas process points
    TP  = []
    # for each parent point
    for i in range(M):
        # determine a number of children accorfing to a Poisson(mu) distribution    
        N = scipy.stats.poisson(mu).rvs()
    # for each child point
        for j in range(N):
            # place a point centered on the location of the parent according 
            # to an isotropuc Gaussuan distribution with sigma variance
                pdf = scipy.stats.norm(loc = parents[i, :2], scale = (sigma, sigma))
                # add the child point to the list TP
                TP.append(list(pdf.rvs(2)))
    x, y = zip(*TP)
    pts = [x, y]
    return pts

aa = ThomasPP(kappa=0.05, sigma=0.2, mu=15, Dx=20)

plt.figure(figsize=(10,10))
plt.scatter(aa[0], aa[1], color='b', marker = '.', alpha = 0.2)
plt.show()

#%%
r_step = 0.1
RList = np.linspace(0.0, 10.0, num = 101)[1:]
print(RList)

#%%
count = len(aa[0])
biglist = np.empty((0, 100))
# print(biglist)

for i in range(count):
# for i in range(5):    
    deltax2 = (aa[0] - aa[0][i])**2
    deltay2 = (aa[1] - aa[1][i])**2
    # print(deltax2)
    # print(deltay2)
    distance = np.sqrt(deltax2 + deltay2)
    # print(distance)

    count_i = []
    for r in RList:        
        count = sum(distance < r)
        count_i.append(count / (np.pi * r**2))
    # print(count_i)
    
    biglist = np.append(biglist, np.array([count_i]), axis = 0)

print(biglist)

#%%
# K(r), L(r), H(r)
K_r = sum(biglist)/count
L_r = np.sqrt(K_r/np.pi)
H_r = L_r - RList

print(K_r)
print(L_r)
print(H_r)