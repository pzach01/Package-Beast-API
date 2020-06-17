from .intersection_methods import objects_intersect


def outside_container(item, containerX,containerY,containerZ):
    if (not(0<= item.position[0]<=containerX)):
        return True
    if (not(0<= item.position[1]<=containerY)):
        return True 
    if (not(0<= item.position[2]<=containerZ)):
        return True
    if (not(0<= item.position[0]+item.get_dimension()[0]<=containerX)):
        return True
    if (not(0<= item.position[1]+item.get_dimension()[1]<=containerY)):
        return True 
    if (not(0<= item.position[2]+item.get_dimension()[2]<=containerZ)):
        return True
    return False
# HIGHLY EXPERIMENTAL; THIS METHOD AS WELL AS ITS PLACMENT IN new_is_valid_corner_point
# if the items are strictly outside of each other, they don't intersect
# used as a speedup
def strictly_outside(item1Min, item1Max, item2Min, item2Max):
    if (item1Min[0]>item2Max[0]) or (item2Min[0]>item1Max[0]):
        return True
    if (item1Min[1]>item2Max[1]) or (item2Min[1]>item1Max[1]):
        return True
    if (item1Min[1]>item2Max[1]) or (item2Min[1]>item1Max[1]):
        return True

def intersect_lucas(item1,item2,containerX,containerY,containerZ):    
    item1C=item1.edgePoints
    item2C=item2.edgePoints
    # same shape
    if item1C==item2C:
        return True
    # consider experimental
    if strictly_outside(item1C[0], item1C[7], item2C[0], item2C[7]):
        return False
    return objects_intersect(item1C, item2C)