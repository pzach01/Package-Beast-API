


from . import single_pack
from . import py3dbp_main
from .py3dbp_main import ContainerPY3DBP,ItemPY3DBP
import random
# makes test deterministic (reproducable)
random.seed(0)




# tests for overfitting when we are packing items into a single container

def test_1():
    print("testing")
    container=ContainerPY3DBP('very-very-large-box', 8, 9, 10, 100)


    items = [
        ItemPY3DBP('50g [powder 2]', 4, 4, 10, 2),
        ItemPY3DBP('50g [powder 2]', 4, 4, 10, 2),
        ItemPY3DBP('50g [powder 2]', 4, 4, 10, 2),
        ItemPY3DBP('50g [powder 2]', 4, 4, 10, 2),
        
        
    ]

    packer=single_pack.single_pack(container, items)
    test_for_double_fit(packer, 10000)
    assert(packer.unfit_items==[])





    
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
    for container in packer.bins:
        for index in range(0, iterationLimit):
            # generate a random point
            pointWidth=random.random()*container.width
            pointDepth=random.random()*container.height
            pointHeight=random.random()*container.depth      
            
            cubesPointIsIn=0
            for item in container.items:
                # this is dumb; requiring us to reference the bins field by a different name then the items, why not just bin.depth?
                lowerWidth, upperWidth=item.position[0], item.position[0]+item.width
                lowerDepth, upperDepth=item.position[1], item.position[1]+item.height
                lowerHeight, upperHeight=item.position[2], item.position[2]+item.depth
                if(lowerWidth < pointWidth < upperWidth):
                    if(lowerDepth < pointDepth < upperDepth):
                        if(lowerHeight < pointHeight <upperHeight):
                            cubesPointIsIn+=1
            
            sumCubesPoint+=cubesPointIsIn
            
            # point should never be within two cubes interior at the same time 
            if(cubesPointIsIn>1):
                break
        # note: percentage of points that exist within exactly one box is almost equal to the volume occupied
                
test_1()