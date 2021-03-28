
'''
from . import single_pack

from . import py3dbp_main
from .py3dbp_main import ContainerPY3DBP,ItemPY3DBP,Packer
import random
# makes test deterministic (reproducable)
seed=random.randint(0,10000)
seed=327
print('Seed:'+str(seed))
random.seed(seed)




import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from . import box_stuff2
import time

from . import py3dbp_constants
from .py3dbp_constants import RotationType

from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import outside_container
from .box_stuff2 import master_calculate_optimal_solution

# iterationLimit (for each container)
def test_for_double_fit(packer, iterationLimit):
    sumCubesPoint=0
    #packer.bins[0].width
    #10
    #packer.bins[0].depth
    #10
    #packer.bins[0].height
    #10    
    # wouldnt be useful for debugging without
    if packer.container==None:
        raise Exception
    touchedCheck=False

    for index in range(0, iterationLimit):
        # generate a random point
        pointWidth=random.random()*packer.container.xDim
        pointDepth=random.random()*packer.container.yDim
        pointHeight=random.random()*packer.container.zDim      
        
        cubesPointIsIn=0
        for item in packer.items:
            # this is dumb; requiring us to reference the bins field by a different name then the items, why not just bin.depth?
            lowerWidth, upperWidth=min(item.position[0], item.position[0]+item.get_dimension()[0]),max(item.position[0], item.position[0]+item.get_dimension()[0])
            lowerDepth, upperDepth=min(item.position[1], item.position[1]+item.get_dimension()[1]),max(item.position[1], item.position[1]+item.get_dimension()[1])
            lowerHeight, upperHeight=min(item.position[2], item.position[2]+item.get_dimension()[2]),max(item.position[2], item.position[2]+item.get_dimension()[2])
            if(lowerWidth < pointWidth < upperWidth):
                if(lowerDepth < pointDepth < upperDepth):
                    if(lowerHeight < pointHeight <upperHeight):
                        cubesPointIsIn+=1
                        touchedCheck=True
        
        sumCubesPoint+=cubesPointIsIn
        
        # point should never be within two cubes interior at the same time 
        if(cubesPointIsIn>1):
            raise Exception
        # note: percentage of points that exist within exactly one box is almost equal to the volume occupied
    # can raise exception in low volume situtation where there are very few tests
    if not touchedCheck:
        pass
        #raise Exception('invalid inputs to test_for_double_fit')



def test_for_double_fit_api_version(apiObjects, iterationLimit):
    for container in apiObjects:
        sumCubesPoint=0

        touchedCheck=False

        for index in range(0, iterationLimit):
            # generate a random point
            pointWidth=random.random()*container.xDim
            pointDepth=random.random()*container.yDim
            pointHeight=random.random()*container.zDim      
            
            cubesPointIsIn=0
            for item in container.boxes:
                # this is dumb; requiring us to reference the bins field by a different name then the items, why not just bin.depth?
                lowerWidth, upperWidth=item.x-(item.xDim/2),item.x+(item.xDim/2)
                lowerDepth, upperDepth=item.y-(item.yDim/2),item.y+(item.yDim/2)
                lowerHeight, upperHeight=item.z-(item.zDim/2),item.z+(item.zDim/2)
                if(lowerWidth < pointWidth < upperWidth):
                    if(lowerDepth < pointDepth < upperDepth):
                        if(lowerHeight < pointHeight <upperHeight):
                            cubesPointIsIn+=1
                            touchedCheck=True
            
            sumCubesPoint+=cubesPointIsIn
            
            # point should never be within two cubes interior at the same time 
            if(cubesPointIsIn>1):
                raise Exception
            # note: percentage of points that exist within exactly one box is almost equal to the volume occupied
        # can raise exception in low volume situtation where there are very few tests
        if not touchedCheck:
            pass
            #raise Exception('invalid inputs to test_for_double_fit')


def test_for_outside_container_api(apiObjects):
    for container in apiObjects:
        for item in container.boxes:
            assert(0<=item.x-(item.xDim/2)<=item.x+(item.xDim/2)<=container.xDim)
            assert(0<=item.y-(item.yDim/2)<=item.y+(item.yDim/2)<=container.yDim)
            assert(0<=item.z-(item.zDim/2)<=item.z+(item.zDim/2)<=container.zDim)

'''