
# %%
import numpy as np

def edgecorrection(r, coor, dimlimit):
    circle_area = np.pi * np.square(r)
    print('circle_area')
    print(circle_area)

    print("coor")
    coor = np.array([coor])
    print(coor)
    
    print("dimlimit")
    print(dimlimit)
    
    distance = dimlimit - coor.T
    print("distance")
    print(distance)

    
    
    '''
    distance_clip = np.clip(distance/r, -1, 1)
    print("distance_clip")
    print(distance_clip)

    arccos = np.arccos(distance_clip)
    print('arccos')
    print(arccos)

    theta_in_radian = arccos/np.pi
    print('theta_in_radian')
    print(theta_in_radian)

    sector_percentage = theta_in_radian * 2/2
    sum_arc = np.sum(sector_percentage)
    print('sum_arc')
    print(sum_arc)
    
    total_proportion = 1 - sum_arc
    print('total_proportion')
    print(total_proportion)
    area_sector = total_proportion * circle_area
    print('area_sector')
    print(area_sector)

    
    # old method
    area_triangle_1 = np.sin(arccos) * np.square(r)/2
    print("area_triangle_1:")
    print(area_triangle_1)
    
    # new method
    # find edge and return a boolean
    edge_indicator = np.greater(arccos, np.array([[0]]))
    print('edge_indicator')
    print(edge_indicator)

    # get distance value
    distance_tangent = edge_indicator * distance
    
    # angel corner
    
    
    
    # get oneside of triangle area
    area_triangle_2_1 = np.sin(arccos) * distance_tangent * r/2
    area_triangle_2_2 = np.sin(arccos) * distance_tangent * r/2
    print("area_triangle_2_1:")
    print(area_triangle_2_1)
    print("area_triangle_2_2:")
    print(area_triangle_2_2)    
    

    area_cover = area_sector + np.sum(area_triangle_1)
    print(area_cover)
    area_factor = area_cover / circle_area
    print(area_factor)

    
    
    '''
    return r

dimlimit = np.array([[0, 50], [0, 50]])
coor = [10, 5]
r = 10
correction_factor = edgecorrection(r, coor, dimlimit)

# %%
import numpy as np
result = np.arccos([0.5])
print(result)
result = np.degrees(np.arccos([0.5]))
print(result)


result = np.arccos([1])
print(result)
# %%
angle = np.arccos(0.5)
print(angle)
result = np.sin(angle) * 1 * 1 / 2 
print(result)