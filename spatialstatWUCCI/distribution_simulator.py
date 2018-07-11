# The Distribution Simulater is design to create pattern for culsttering
# analysis. 
# By Chien-cheng Shih (Mike)
# From Washington University Center for Cellular Imaging

# PoissonPP and ThomasPP are adpated from Connor Johnson's blog post
# (http://http://connor-johnson.com/2014/02/25/spatial-point-processes/) 
# 

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

def PoissonPP(rt, Dx, Dy = None, seed = None):
    '''
    Determines the number of events 'N' for a rectangular region,
    given the rate 'rt' and the dimensions, 'Dx', 'Dy'.
    Returns a <2xN> NumPy array.
    '''
    if seed != None: 
        np.random.seed(seed=seed)
    
    if Dy == None:
        Dy = Dx

    N = scipy.stats.poisson(rt*Dx*Dy).rvs()
    x = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)))
    y = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)))
    P = np.hstack((x, y))
    return(P)

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