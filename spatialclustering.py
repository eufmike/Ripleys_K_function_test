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