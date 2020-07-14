
from . import single_pack
from . import py3dbp_main
from .py3dbp_main import ContainerPY3DBP,ItemPY3DBP,Packer
import random
# makes test deterministic (reproducable)
seed=random.randint(0,10000)
seed=780
print('Seed:'+str(seed))
random.seed(seed)




import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from . import box_stuff2


from . import py3dbp_constants
from .py3dbp_constants import RotationType

from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import outside_container



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