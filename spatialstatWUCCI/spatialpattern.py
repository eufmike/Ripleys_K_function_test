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
def spest(xyarray_ref, xyarray_all, rstart, rend, density, rsize = None, rstep = 0.1, function = 'Hest', downsize = True, downsizesize = 3000):
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

    # create radius (RList_array)
    if rsize == None:        
        RList = np.arange(rstart, rend + rstep, rstep)
    else:
        RList = np.linspace(rstart, rend, num = rsize + 1)  
    RList_array = np.array([RList])

    # get count of points
    pointcount = xyarray_ref.shape[0]

    print(pointcount)
    print(downsizesize)
    print(downsize)
    # downsize
    if pointcount > downsizesize:
        if downsize == True:
            random.seed(10)
            downsize_idx = random.sample(list(range(pointcount)), downsizesize)
            xyarray_ref = xyarray_ref[downsize_idx]
            pointcount = downsizesize


    # memory preallocation ------------------------------------------
    # create an zeros array
    countlist = np.zeros((pointcount, len(RList)))

    # calculate counts ----------------------------------------------
    for i in tqdm.trange(pointcount):
        # assign ref point
        refxy = xyarray_ref[i, :2]
        refidx = int(xyarray_ref[i, 2])

        # get distance from points to ref point
        xyarray_all_temp = np.delete(xyarray_all, refidx, 0)
        
        xlimmin = refxy[0] - rend
        xlimmax = refxy[0] + rend
        ylimmin = refxy[1] - rend
        ylimmax = refxy[1] + rend

        xyarray_all_temp = sswdistsim.xyroi(xyarray_all_temp, xlimmin, xlimmax, ylimmin, ylimmax)

        deltaxy2 = np.square(xyarray_all_temp - np.array(refxy))
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
        

    # perform clustering analysis 
    print(countlist)
    K_r = np.mean(countlist, axis = 0) / density
  
    print('--------------------------')
    print('Function: {}'.format(function))
    print('Range: {0} - {1}'.format(rstart, rend))
    if rsize == None: 
        print('Rstep: {}'.format(rstep))
    else: 
        print('Rsize: {}'.format(rsize))
    print('Pointcount: {}'.format(pointcount))
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


# localspest: local spatial pattern analysis
def localspest(xyarray_ref, xyarray_all, square_size,
            r = None, rstart = None, rend = None, rsize = None, rstep = 0.1, 
            function = 'localL', downsize = True, downsizesize = 3000):
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

    # create radius (RList_array)
    if r == None: 
        if rsize == None:        
            RList = np.arange(rstart, rend + rstep, rstep)
        else:
            RList = np.linspace(rstart, rend, num = rsize + 1)  
    else:
        RList = np.array([r])
    RList_array = np.array([RList])

    # print(RList_array)
    
    # get count of points
    pointcount = xyarray_ref.shape[0]
    pointcount_all = xyarray_all.shape[0]

    print('pointcount: {}'.format(pointcount))
    # print(downsizesize)
    # print(downsize)
    # downsize
    if pointcount > downsizesize:
        if downsize == True:
            random.seed(10)
            downsize_idx = random.sample(list(range(pointcount)), downsizesize)
            xyarray_ref = xyarray_ref[downsize_idx]
            pointcount = downsizesize
            print('The point count is over {} and the sample will be downsized.'.format(downsizesize))
 
    
    # memory preallocation ------------------------------------------
    # create an zeros array
    countlist = np.zeros((pointcount, len(RList)))
    # print(countlist)
    
    if rend == None:        
        rend = r

    # calculate counts ----------------------------------------------
    for i in tqdm.trange(pointcount):
        # assign ref point
        refxy = xyarray_ref[i, :2]
        refidx = int(xyarray_ref[i, 2])

        # get distance from points to ref point
        xyarray_all_temp = np.delete(xyarray_all, refidx, 0)
        
        xlimmin = refxy[0] - rend
        xlimmax = refxy[0] + rend
        ylimmin = refxy[1] - rend
        ylimmax = refxy[1] + rend

        xyarray_all_temp = sswdistsim.xyroi(xyarray_all_temp, xlimmin, xlimmax, ylimmin, ylimmax)

        deltaxy2 = np.square(xyarray_all_temp - np.array(refxy))
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
        
        
    print(countlist)
    
    localK_r = countlist * square_size / (pointcount_all - 1)
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

    print('Pointcount: {}'.format(pointcount))
    print('--------------------------')

    return (localK_r, localL_r, localH_r, RList, countlist, xyarray_ref)    
    