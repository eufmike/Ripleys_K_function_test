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

def PoissonPP(rt, N = None, ndimension = 2, rangelim = None, seed = None, seedmodifier = 1):
    '''
    rt = rate of Poisson distribution
    N = force to over write N (default = None)
    ndimension: the number of dimension (default = 2)
    rangelim: the limt for each dimension (default = None)
    seed = seed variable for random_state in .rvs arguments (default = None)
    seedmodifier = allow the seed value changes when iterating through dimensions (default = 1)

    PoissonPP determines the number of events 'N' for a rectangular region,
    given the rate 'rt', the dimensions. Returns a <N x ndimension > NumPy array. 
    Rangelim (NumPy array) defines the limit for each dimension. 
    
    Format needs to be: 
    [[x1_min, x1_max], 
     [x2_min, x2_max],
     [x3_min, x3_max], ...]]   
    
    Randomization can be controled by seed and seedmodifier. 
    
    Add-on:
    For rangelim, if the size of dimension is smaller than 1, which presumably return N as 0,  
    directly input N is allowed. 
    '''
    # check the value of rt
    if not (0 <= rt <= 1): 
        raise ValueError('error: var "rt" is a value between 0 and 1')
    
    # create a default ranage for each dimension if no limits are assigned.
    if rangelim is None:
        rangelim = np.zeros([ndimension, 2])
        rangelim[:, 1] = 20

    # return an error message when the input limits are inconsistent with the given n dimension
    if rangelim.shape[0] != ndimension:
        print('ndimension: {}'.format(ndimension))
        print('reangelim:')
        print(rangelim)
        raise ValueError('error: the dimension of array "rangelim" is not consistent with the var "ndimension"')
        return
    
    # create the size of range
    rangesize = rangelim[:,1] - rangelim[:,0]
    # create total space
    rangeprod = np.prod(rangesize, axis = 0)
    # calculate N based on the given dimension
    if N == None:
        if seed == None: 
            N = scipy.stats.poisson(rt*rangeprod).rvs()
        else:
            N = scipy.stats.poisson(rt*rangeprod).rvs(random_state=seed)
    
    # <array pre-allocation>
    # create zero matrix
    array = np.zeros([N, ndimension])
    # print(array.shape)
    seedtmp = seed
    # create random value for each dimension
    for i in range(ndimension):
        if seedtmp == None:
            tmp_rndvar = scipy.stats.uniform.rvs(loc = 0, scale = rangesize[i], size = N)
            
        else:
            tmp_rndvar = scipy.stats.uniform.rvs(loc = 0, scale = rangesize[i], size = N, random_state = seedtmp)
            seedtmp += seedmodifier

        tmp_rndvar_offset = rangelim[i][0] + tmp_rndvar
        
        # inject the array into pre-allocated array
        array[:, i] = tmp_rndvar_offset

    return(array)

def ThomasPP(rt, sigma, mu, N = None, ndimension = 2, rangelim = None, seed = None, seedmodifier = 1):
    '''
    rt = rate of Poisson distribution
    sigma = the standard deviation of Gaussian distribution surrounding parent points
    mu = generate the count for each Gaussian distribution following Poisson distribution
    N = force to over write N (default = None)
    ndimension: the number of dimension (default = 2)
    rangelim: the limt for each dimension (default = None)
    seed = seed variable for random_state in .rvs arguments (default = None)
    seedmodifier = allow the seed value changes when iterating through dimensions (default = 1)
    
    THOMASPP generates multiple Gaussian distribution surrounding given parents points, 
    which are created by PoissonPP(). The sample size of Gaussian distribution is determined by 
    Poisson distribution 'mu', where the variance is determined by 'Sigma'.
  
    '''

    # Create a set of parent points form a Poisson
    array_points_parents = PoissonPP(rt, N, ndimension, rangelim, seed, seedmodifier)
    
    # M is the number of parents
    M = array_points_parents.shape[0]
    # Create array for random count
    count_list = []
    
    # Create counts for each parent point
    seedtmp = seed
    for i in range(M):
        # print(seedtmp)
        if seedtmp == None:
            child_count = scipy.stats.poisson(mu).rvs()
        else: 
            child_count = scipy.stats.poisson(mu).rvs(random_state=seedtmp)
            seedtmp += seedmodifier
        count_list.append(child_count)
    # print(count_list)
    # return total number for the childern points
    total_count = sum(count_list)
    # create the index for start and end
    childern_idx_start = np.concatenate([np.array([0]), np.cumsum(count_list)[0: -1]])
    # print(childern_idx_start)
    childern_ide_end = np.cumsum(count_list)
    # print(childern_ide_end)
    
    # <array pre-allocation>
    array_points_childern = np.zeros([total_count, ndimension])
    
    seedtmp = seed    
    for i in range(M):
        # return the count for the given parent point
        childern_count = count_list[i]
        # return the coordinate for the given parent point
        parent = array_points_parents[i]
        # <array pre-allocation>
        array_temp = np.zeros([childern_count, ndimension])      
        for j in range(ndimension):
            parent_value = parent[j]
            if seedtmp == None:
                pdf = scipy.stats.norm(loc = parent_value, scale = sigma)
                array_temp[:, j] = list(pdf.rvs(childern_count))
            else:
                pdf = scipy.stats.norm(loc = parent_value, scale = sigma)  
                array_temp[:, j] = list(pdf.rvs(childern_count, random_state = seedtmp))
                seedtmp += seedmodifier
        # print(array_temp)
        array_points_childern[childern_idx_start[i]:childern_ide_end[i], :] = array_temp
    
    return(array_points_childern, array_points_parents)

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
    
    return (density, xyarray.shape[0], area) 