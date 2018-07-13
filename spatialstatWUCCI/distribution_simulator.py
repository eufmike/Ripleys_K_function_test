# The Distribution Simulater is design to create pattern for culsttering
# analysis. 
# By Chien-cheng Shih (Mike)
# From Washington University Center for Cellular Imaging

# PoissonPP and ThomasPP are adpated from Connor Johnson's blog post
# (http://http://connor-johnson.com/2014/02/25/spatial-point-processes/) 
# Seed argument for generating random numbers is added. 

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

def PoissonPP(rt, Dx, Dy = None, seed = None):
    '''
    rt = rate or Poisson distribution
    Dx, Dy = the dimension of 2D array. 
    seed = seed variable for random_state in .rvs arguments (default = None)
    
    POISSONPP determines the number of events 'N' for a rectangular region,
    given the rate 'rt', the dimensions, 'Dx', 'Dy', and seed variable.
    Returns a <2xN> NumPy array.
    
    '''
    
    if Dy == None:
        Dy = Dx
    if seed == None: 
        N = scipy.stats.poisson(rt*Dx*Dy).rvs()
        x = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)))
        y = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)))
    else:
        N = scipy.stats.poisson(rt*Dx*Dy).rvs(random_state=seed)
        x = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)), random_state=seed)
        y = scipy.stats.uniform.rvs(loc = 0, scale = Dx, size = ((N, 1)), random_state=seed + 1)
        '''
        print('Dx = {}'.format(Dx))
        print('Dy = {}'.format(Dy))
        print('N = {}'.format(N))
        '''
    P = np.hstack((x, y))
    return(P)

def ThomasPP(rt, Dx, sigma, mu, seed = None):
    '''
    rt = rate or Poisson distribution
    Dx, Dy = the dimension of 2D array
    sigma = the standard deviation of Gaussian distribution surrounding parent points
    mu = generate the count for each Gaussian distribution following Poisson distribution
    seed = seed variable for random_state in .rvs arguments (default = None)
    
    THOMASPP generates multiple Gaussian distribution surrounding given parents points, 
    which are created by PoissonPP(). The sample size of Gaussian distribution is determined by 
    Poisson distribution 'mu', where the variance is determined by 'Sigma'.
    '''

    # Create a set of parent points form a Poisson(kappa)
    # distribution on the square region [0, Dx] * [0, Dx]
    
    if seed == None:
        parents = PoissonPP(rt, Dx)
    else:    
        parents = PoissonPP(rt, Dx, seed = seed)
    # M is the number of parents
    M = parents.shape[0]
    # an empty list for the Thomas process points
    x = []
    y = []
    # for each parent point
    for i in range(M):
        # determine a number of children accorfing to a Poisson(mu) distribution
        parent_x = parents[i][0]
        parent_y = parents[i][1]
        pdf_x = scipy.stats.norm(loc = parent_x, scale = sigma)
        pdf_y = scipy.stats.norm(loc = parent_y, scale = sigma)
        
        # check if the seed arg exists.
        if seed == None:
            N = scipy.stats.poisson(mu).rvs()
            children_x = list(pdf_x.rvs(N))
            children_y = list(pdf_y.rvs(N))
        else:
            N = scipy.stats.poisson(mu).rvs(random_state =seed + i)
            children_x = list(pdf_x.rvs(N, random_state = (seed + i + 1)))
            children_y = list(pdf_y.rvs(N, random_state = (seed + i + 2)))
        
        # concate x y coordinates
        x = x + children_x
        y = y + children_y

    pts = [x, y]
    return pts