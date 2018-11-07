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

def localspest(xyarray_ref, xyarray_all, square_size,
            r = None, rstart = None, rend = None, rsize = None, rstep = 0.1, 
            function = 'localL', downsize = True, downsizesize = 3000):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates. 
    
    function: 
        Three functions are built in: Kest, Lest, Hest 
        
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
    


    