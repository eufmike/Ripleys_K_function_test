#%%
import pickle
import scipy.stats
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline

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
    x = scipy.stats.uniform.rvs()
    y = scipy.stats.uniform.rvs()
    P = np.hstack((x, y))
    return(P)
    
rate, Dx = 0.2, 20
P = PoissonPP(rate, Dx).T
plt.scatter(P[0], P[1], edgecolor = 'b', facecolor='none', alpha =0.5)
plt.show()

#%%
# Poisson test
import scipy.stats

rt = 0.2
Dx = 20
Dy = 20
N = 80
print(N)
# N = scipy.stats.poisson(rt*Dx*Dy).rvs()
# print(N)
print(((N, 1)))
x = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1))) 
# 0, Dx means range, ((N, 1)) means dimentional structure

y = scipy.stats.uniform.rvs(0, Dy, ((N, 1)))

print(len(x))
print('x = {}'.format(x))
# print(f"x = {x}")
# print(y)