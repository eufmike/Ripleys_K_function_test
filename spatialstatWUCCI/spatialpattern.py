# coding: utf-8
# The Distribution Simulater is design to create pattern for culsttering
# analysis. 
# By Chien-cheng Shih (Mike)
# From Washington University Center for Cellular Imaging

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import time
import imp
import random
import spatialstatWUCCI.distribution_simulator as sswdistsim

# spest: general spatial pattern analysis
def spest(input_array_ref, input_array_all, rstart, rend, 
            density = None, rsize = None, rstep = 0.1, function = 'Hest', 
            downsize = True, pointsizelimit = 3000, 
            seed = 1947):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates. 
    
    function: 
        Three functions are built in: Kest, Lest, Hest 
        
        Kest: K(r) = N / area(A) * 1/(N-1) * sum (counts of target in area(r))
        Lest: L(r) = sqrt( K(r) / pi )
        Hest: H(r) = L(r) - r
        
        K_r = return a tuple (K_r, RList)
        L_r = return a tuple (L_r, RList)
        H_r = return a tuple (H_r, RList)
        all = return a tuple includes all three function (K_r, L_r, H_r, RList)
        (default = H_r)
    
    density: the average density of points (generally estimated as n/A, 
    where A is the area of the region containing all points)

    rstep: the step size of radius (r) in Ripley’s K-function
    rstart, rend: the start and end of r range
    rsize: the length of r list (default = None)
    rstep: the increment for r list (default = 0.1)
    downsize: the default size of downsizing

    This function performs Ripley's functions on 2D dataset ('xyarray')
    with given rstep size ('rstep') or sample size rsize' inside given range 'rstart, rend'.

    CAUTION: There is no edge correction implemented with this function. 
    
    ref: Kiskowski, M. A., Hancock, J. F., & Kenworthy, A. K. (2009). On the use of 
    Ripley's K-function and its derivatives to analyze domain size. Biophysical Journal, 
    97(4), 1095–1103. http://doi.org/10.1016/j.bpj.2009.05.039 

    '''
    countlist, RList, pointcountref, pointcountall = countlistgenerator(input_array_ref, input_array_all, 
                        rstart, rend, 
                        density, rsize, rstep, 
                        downsize, pointsizelimit,
                        seed)

    # perform clustering analysis 
    K_r = np.mean(countlist, axis = 0) / density
  
    print('--------------------------')
    print('Function: {}'.format(function))
    print('Range: {0} - {1}'.format(rstart, rend))
    if rsize == None: 
        print('Rstep: {}'.format(rstep))
    else: 
        print('Rsize: {}'.format(rsize))
    print('Pointcountref: {}'.format(pointcountref))
    print('Density: {}'.format(density))
    print('--------------------------')

    if function != 'all': 
        if function == 'Kest':
            # Ripley’s K-function
            result = K_r

        elif function == 'Lest':
            # Besag normalization Ripley’s K-function
            L_r = np.sqrt(K_r/np.pi)
            result = L_r

        else:
            # normalized by radius
            H_r = L_r - RList
            result = H_r
        
        # return the result with RList
        return (result, RList)
    else: 
        # return all results with RList
        L_r = np.sqrt(K_r/np.pi)
        H_r = L_r - RList
        print('Done')
        print('--------------------------')
        return (K_r, L_r, H_r, RList, countlist)
# ----------------------------------------------------------------------------
# localspest: local spatial pattern analysis
def localspest(input_array_ref, input_array_all, square_size, density = None,
            r = None, rstart = None, rend = None, rsize = None, rstep = 0.1, 
            function = 'localL', downsize = True, pointsizelimit = 3000, 
            seed = 1947):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates. 
    
    function: 
        Three functions are built in:
        
        localK: localK_r = N / area(A) * 1/(N-1) * sum (counts of target in area(r))
        localL: localL_r = sqrt( K(r) / pi )
        
        localK = return a tuple (localK_r, RList)
        localL = return a tuple (localL_r, RList)
        all = return a tuple includes all three function (localK_r, localL_r, RList)

    r = fix value of r
    rstep: the step size of radius (r) in Ripley’s K-function (default = 0.1)
    rstart, rend: the start and end of r range
    rsize: the length of r list (default = None)
    downsize: the default size of downsizing

    This function performs Ripley's functions on 2D dataset ('xyarray')
    with given rstep size ('rstep') or sample size rsize' inside given range 'rstart, rend', 
    but return a K or L value for each spot. Downsizing has been implemented.

    '''
    countlist, RList, pointcountref, pointcountall = countlistgenerator(input_array_ref, input_array_all, 
                        rstart, rend, 
                        density, rsize, rstep, 
                        downsize, pointsizelimit,
                        seed)    
    
    localK_r = countlist * square_size / (pointcountall - 1)
    localL_r = np.sqrt(localK_r / np.pi)
    localH_r = localL_r - RList

    print('--------------------------')
    print('Function: {}'.format(function))
    if rsize == None: 
        if len([r]) == 1:
            print('Single r value: {}'.format(r))
        else:
            print('Range: {0} - {1}'.format(rstart, rend))
            print('Rstep: {}'.format(rstep))
    else: 
        print('Range: {0} - {1}'.format(rstart, rend))
        print('Rsize: {}'.format(rsize))

    print('Pointcountref: {}'.format(pointcountref))
    print('--------------------------')

    return (localK_r, localL_r, localH_r, RList, countlist, input_array_ref)  



# ----------------------------------------------------------------------------    
# add index to array in the first column, not limited to 2D array
def arrayaddidx(array):
    idx = array.shape[0]
    idxarray = np.array([range(idx)]).T
    array = np.hstack((idxarray, array))
    return array


# ----------------------------------------------------------------------------
# create countlist
def countlistgenerator(input_array_ref, input_array_all, rstart, rend, 
                        density, rsize, rstep, 
                        downsize, pointsizelimit,
                        seed):
    # ----------------------------------------------------------------------------
    # create radius (RList_array)
    if rsize == None:        
        RList = np.arange(rstart, rend + rstep, rstep)
    else:
        RList = np.linspace(rstart, rend, num = rsize + 1)  
    RList_array = np.array([RList])

    # get counts from input_array_ref
    pointcountref = input_array_ref.shape[0]
    pointcountall = input_array_all.shape[0]
    
    # ----------------------------------------------------------------------------
    # examine if downsizing is required based on the input cut-off
    # If downsizng is required, the it overwrites input_array_ref
    # based on the random selection. 
    # Seed control is doable.  
    if pointcountref > pointsizelimit:
        if downsize == True:
            random.seed(seed)
            downsize_idx = random.sample(list(range(pointcountref)), pointsizelimit)
            input_array_ref = input_array_ref[downsize_idx]
            pointcountref = pointsizelimit
    
    # ----------------------------------------------------------------------------
    # memory preallocation
    # create an zeros array
    countlist = np.zeros((pointcountref, len(RList)))
    
    # ----------------------------------------------------------------------------
    # add index to the input array
    input_array_ref = arrayaddidx(input_array_ref) 

    for i in tqdm.trange(pointcountref):
        # assign ref point
        refxy = input_array_ref[i, :2]
        refidx = int(input_array_ref[i, 0])

        # get distance from points to ref point
        input_array_all_temp = np.delete(input_array_all, refidx, 0)
        
        xlimmin = refxy[0] - rend
        xlimmax = refxy[0] + rend
        ylimmin = refxy[1] - rend
        ylimmax = refxy[1] + rend

        input_array_all_temp = sswdistsim.xyroi(input_array_all_temp, xlimmin, xlimmax, ylimmin, ylimmax)
        
        deltaxy2 = np.square(input_array_all_temp - np.array(refxy))
        distance = np.sqrt(deltaxy2[:, 0] + deltaxy2[:, 1])
        
        # compare to RList_array
        distance = np.array([distance]).T
        delta = RList_array - distance
        # check if the distance bigger than given radius
        check = np.greater(delta, np.array([0]))
        count = np.sum(check, axis = 0)
        count = np.array([count])

        # add counts to countlist
        countlist[i] = count   
    
    return (countlist, RList, pointcountref, pointcountall)

