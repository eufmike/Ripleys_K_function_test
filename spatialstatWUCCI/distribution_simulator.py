# The Distribution Simulater is design to create pattern for culsttering
# analysis. 
# By Chien-cheng Shih (Mike)
# From Washington University Center for Cellular Imaging

# PoissonPP and ThomasPP are adpated from Connor Johnson's blog post
# (http://http://connor-johnson.com/2014/02/25/spatial-point-processes/)
# The ability for seed control is added for generating random numbers.  

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
    Returns a <Nx2> NumPy array.
    
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
    Returns a <Nx2> NumPy array.
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
    
    x = np.array([x]).T
    y = np.array([y]).T

    P = np.hstack((x, y))
    return P


def xyroi(xyarray, xmin, xmax, ymin, ymax):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates.
    xmin, xman: the range in x-axis
    ymin, ymax: the range in y-axis
    
    XYROI crop the dataset by given ranges in x and y axis ('xmin', 'xmax', 
    'ymin', 'max'), then return a <Nx2> NumPy array. 
    '''

    temp_xy = xyarray[(xyarray[:,0] > xmin) & (xyarray[:,0] < xmax) & (xyarray[:,1] > ymin) & (xyarray[:,1] < ymax)]
    return temp_xy

def xyroi_idx(xyarray, xmin, xmax, ymin, ymax):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates.
    xmin, xman: the range in x-axis
    ymin, ymax: the range in y-axis
    
    XYROI crop the dataset by given ranges in x and y axis ('xmin', 'xmax', 
    'ymin', 'max'), then return a <Nx3> NumPy array. 
    
    The last column is index. 

    '''

    idx = xyarray.shape[0]
    idxarray = np.array([range(idx)]).T
    xyarray = np.hstack((xyarray, idxarray))
    temp_xy = xyarray[(xyarray[:,0] > xmin) & (xyarray[:,0] < xmax) & (xyarray[:,1] > ymin) & (xyarray[:,1] < ymax)]
    return temp_xy

def xydensity(xyarray, Dx = None, Dy = None):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates.
    Dx, Dy: the dimension of 2D array (default = None). 

    XYDENSITY return the desity of given xy dataset. When x/y dimensions are specified, 
    density will be calculated according to the size of given area. Otherwise it returns
    the density based on the largest square area which covers all xy data point. 
    XYDENSITY returns density (count/area).
    '''
    
    x = (xyarray[:,0])
    y = (xyarray[:,1])
    if (Dy == None) & (Dx == None):
        area = (abs(max(x)-min(x))) * (abs(max(y)-min(y)))
        density = xyarray.shape[0] / area
    elif Dy == None:
        area = Dx * Dx
        density = xyarray.shape[0] / area
    else:
        area = Dx * Dy
        density = xyarray.shape[0] / area
    
    return density