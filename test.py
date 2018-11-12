
# %%
import numpy as np

def PolyArea(x,y):
       return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def TriangleArea(v1, v2, v3):
    area_list = []
    for i in range(v1.shape[0]):
        v_array_temp = np.concatenate((v1[None, i, :], v2[None, i, :]), axis = 0)
        v_array = np.concatenate((v_array_temp, v3[None, i, :]), axis = 0)
        area_temp = PolyArea(v_array[:, 0], v_array[:, 1])
        area_list.append(area_temp)
    return(area_list)


def edgecorrection(r, coor, dimlimit):
    circle_area = np.pi * np.square(r)
    print('circle_area')
    print(circle_area)
    
    coor_array = np.array([coor]).T
    # print(coor_array)
    
    dimlimit_recenter = dimlimit - coor_array
    dimlimit_array = np.array([dimlimit_recenter.flatten()]).T
    
    # build corners
    print("new xy limits")
    print(dimlimit_recenter.T)
    corner_x = dimlimit_recenter.T[:, 0].repeat(2)
    corner_x = np.array([corner_x]).T
    corner_y = np.roll(dimlimit_recenter.T[:, 1].repeat(2), -1, axis = 0)
    corner_y = np.array([corner_y]).T
    print(corner_x)
    print(corner_y)
    corner_coor = np.concatenate((corner_x, corner_y), axis = 1) 
    print("recentered corner")
    print(corner_coor)

    # temporary solution
    point_on_edge = np.array([
                            [dimlimit_recenter.T[0, 0], 0], 
                            [0, dimlimit_recenter.T[1, 1]],
                            [dimlimit_recenter.T[1, 0], 0],
                            [0, dimlimit_recenter.T[0, 1]]
                            ])
    print("point on edge")
    print(point_on_edge)

    # create list for vertices
    v1 = point_on_edge.repeat(2, axis = 0)
    v2 = np.roll(corner_coor.repeat(2, axis = 0), -1, axis = 0)
    v3 = np.array([[0, 0]]).repeat(v1.shape[0], axis = 0)    

    triangle_area = TriangleArea(v1, v2, v3)
    print(triangle_area)

    def intersection(r, edge_point):
        print(edge_point)
        print(r)
        theta = np.arccos(edge_point/np.array([[r]]))/np.pi
        
        
        print(theta)
        
        coor1 = []
        coor2 = []
        return (coor1, coor2)
    # create intersection coordinate
    
    for i in range(point_on_edge.shape[0]):
        print(point_on_edge[i])
        coor1, coor2 = intersection(r, point_on_edge[i])




        # print(coor1)
        # print(coor2)
    
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

# %%
# point projection test
p = np.array([2, 6])
k = 2
wk = np.array([1, k])
wk = np.array([wk/np.sqrt(np.sum(np.square(wk)))])
wd_temp = np.dot(p, wk.T)
wd = np.dot(wd_temp, wk)

print(wd)













'''
# distance to the corner
corner_distance = np.sqrt(np.sum(np.square(corner_coor), axis =1))
print("corner distance")
print(corner_distance)
'''
'''
# calculate the shortest distance to the edge
coe_x = np.array([1, 0]).repeat(2)
coe_x = np.reshape(coe_x, (4, 1))
coe_y = np.array([0, 1]).repeat(2)
coe_y = np.reshape(coe_y, (4, 1))

line_array = np.concatenate((coe_x, coe_y), axis = 1)
line_array = np.concatenate((line_array, dimlimit_array), axis = 1)
# print(line_array)
'''
'''
coor_array_new = np.array([[0, 0, 1]]).T
# print(coor_array_new)


# point to the shortest distance
numerator = np.abs(np.dot(line_array, coor_array_new))
denominator = np.sqrt(np.square(coe_x) + np.square(coe_y))
shortest_dis = numerator/denominator
print(shortest_dis)
'''
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