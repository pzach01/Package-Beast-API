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
    '''
    # dont think we need to do this because it is checked upon adding to bin
    # check within bounds
    if outside_container(item1, containerX,containerY,containerZ):
        return True
    if outside_container(item2, containerX,containerY,containerZ):
        return True
    '''
    # we don't need to do this dynamically (could be stored)
    # my old method
    item1C=sorted([
        [item1.position[0],item1.position[1],item1.position[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1],item1.position[2]],
        [item1.position[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]],
        [item1.position[0],item1.position[1],item1.position[2]+item1.get_dimension()[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1],item1.position[2]+item1.get_dimension()[2]],
        [item1.position[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]+item1.get_dimension()[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]+item1.get_dimension()[2]],


    ])

    item2C=sorted([
        [item2.position[0],item2.position[1],item2.position[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1],item2.position[2]],
        [item2.position[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]],
        [item2.position[0],item2.position[1],item2.position[2]+item2.get_dimension()[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1],item2.position[2]+item2.get_dimension()[2]],
        [item2.position[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]+item2.get_dimension()[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]+item2.get_dimension()[2]],


    ])
    # same shape
    if item1C==item2C:
        return True
    # consider experimental
    if strictly_outside(item1C[0], item1C[7], item2C[0], item2C[7]):
        return False

    return (not (objects_intersect(item1C, item2C)))