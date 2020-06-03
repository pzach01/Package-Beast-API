from . import py3dbp_constants
from .py3dbp_constants import Axis


def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )


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

def intersect_lucas(item1,item2,containerX,containerY,containerZ):

    from . import new_is_valid_corner_point_code
    from .new_is_valid_corner_point_code import new_is_valid_corner_point as np
    # check within bounds
    if outside_container(item1, containerX,containerY,containerZ):
        return True
    if outside_container(item2, containerX,containerY,containerZ):
        return True
    # my old method
    item1C=[
        [item1.position[0],item1.position[1],item1.position[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1],item1.position[2]],
        [item1.position[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]],
        [item1.position[0],item1.position[1],item1.position[2]+item1.get_dimension()[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1],item1.position[2]+item1.get_dimension()[2]],
        [item1.position[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]+item1.get_dimension()[2]],
        [item1.position[0]+item1.get_dimension()[0],item1.position[1]+item1.get_dimension()[1],item1.position[2]+item1.get_dimension()[2]],


    ]

    item2C=[
        [item2.position[0],item2.position[1],item2.position[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1],item2.position[2]],
        [item2.position[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]],
        [item2.position[0],item2.position[1],item2.position[2]+item2.get_dimension()[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1],item2.position[2]+item2.get_dimension()[2]],
        [item2.position[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]+item2.get_dimension()[2]],
        [item2.position[0]+item2.get_dimension()[0],item2.position[1]+item2.get_dimension()[1],item2.position[2]+item2.get_dimension()[2]],


    ]




    return (not (np(item1C, item2C)))