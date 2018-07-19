# coding: utf-8
# The Distribution Simulater is design to create pattern for culsttering
# analysis. 
# By Chien-cheng Shih (Mike)
# From Washington University Center for Cellular Imaging

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

def ripleyk(xyarray, xyarrayref, rstart, rend, density, rsize = None, rstep = 0.1, function = 'H_r'):
    '''
    xyarray: A <Nx2> NumPy array with xy coordinates

        equation
        
        K_r = 1/n * sum( (counts of target in area(r))/area(r) )
        L_r = sqrt( K_r / pi )
        H_r = L_r - r
        
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

    This function performs Ripley's functions on 2D dataset ('xyarray')
    with given rstep size ('rstep') or sample size rsize' inside given range 'rstart, rend'.
    
    ref: Kiskowski, M. A., Hancock, J. F., & Kenworthy, A. K. (2009). On the use of 
    Ripley's K-function and its derivatives to analyze domain size. Biophysical Journal, 
    97(4), 1095–1103. http://doi.org/10.1016/j.bpj.2009.05.039 

    '''
    
    if rsize == None:        
        RList = np.arange(rstart, rend + rstep, rstep)
    else:
        RList = np.linspace(rstart, rend, num = rsize + 1)  
    # create RList_array
    RList_array = np.array([RList])

    # get the length of xyarray
    pointcount = xyarray.shape[0]
    # create an zeros array
    countlist = np.zeros((pointcount, len(RList)))
    
    for i in range(pointcount):
    # for i in range(1):   
        # print('i = {}'.format(i))
        # assign ref point
        refxy = xyarray[i, :2]
        refidx = int(xyarray[i, 2])
        # print(refxy)
        # print(refidx)
        # print(xyarrayref) 
        # get distance from points to ref point
        xyarrayref_temp = np.delete(xyarrayref, refidx, 0)  
        # print(xyarrayref_temp)

        deltaxy2 = np.square(xyarrayref_temp - np.array(refxy))
        distance = np.sqrt(deltaxy2[:, 0] + deltaxy2[:, 1])
        
        # compare to RList_array
        distance = np.array([distance]).T
        # print(distance)

        delta = RList_array - distance

        # check if the distance bigger than given radius
        check = np.greater(delta, np.array([0]))
        count = np.sum(check, axis = 0)
        count = np.array([count])

        # add counts to countlist
        countlist[i] = count

    # perform clustering analysis 
    K_r = np.mean(countlist, axis = 0) / density
    # print(K_r)
  
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
        if function == 'K_r':
            # Ripley’s K-function
            result = K_r

        elif function == 'L_r':
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
    