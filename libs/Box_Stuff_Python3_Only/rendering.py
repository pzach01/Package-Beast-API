from __future__ import division

import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import



def render_bin(bin, boxes):
    import random
    # This import registers the 3D projection, but is otherwise unused.
    supportedColors=['red','blue','green','magenta','cyan','yellow']
    x, y, z = np.indices((bin.length,bin.xDim ,bin.heigth))   
    cubeList=[]
    for key in boxes.keys():
        upperZ=key[0]+(boxes[key].heigth/2)
        lowerZ=key[0]-(boxes[key].heigth/2) 
        upperY=key[1]+(boxes[key].xDim/2)
        lowerY=key[1]-(boxes[key].xDim/2)
        
        upperX=key[2]+(boxes[key].length/2)
        lowerX=key[2]-(boxes[key].length/2)


        cube = ((x>lowerX)&(x < upperX)) & (((y>lowerY)& (y<upperY)) & ((z>lowerZ)& (z<upperZ)))
        cubeList.append(cube)
    voxels=cubeList[0]
    for element in cubeList:
        voxels=voxels|element
        
    colors = np.empty(voxels.shape, dtype=object)
    for element in cubeList:
        colors[element]=supportedColors[random.randint(0,5)]
    
    # and plot everything
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(voxels, facecolors=colors, edgecolor='k')
    
    plt.show()    
