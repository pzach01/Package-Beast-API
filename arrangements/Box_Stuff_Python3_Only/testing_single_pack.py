

from . import testing_imports
from .testing_imports import *
# (not multibinpack= singlepack), this wierd name used to avoid confusing with single_pack.py, the 
# file used to render/pack items into a single container
def test_not_multibinpack():
    items=['4x4x4','4x4x4']
    containers=['4x4x4','4x4x4','10x5x5']
    containerList=box_stuff2.master_calculate_optimal_solution(containers,items,1000000,False)
    usedContainer=[container for container in containerList if (len(container.boxes)>0)][0]
    assert(usedContainer.volume==(10*5*5))
    

# tests for overfitting when we are packing items into a single container

def test_1():
    print("testing")
    container=ContainerPY3DBP('very-very-large-box', 8, 9, 10)


    items = [
        ItemPY3DBP('50g [powder 2]', 4, 4, 10),
        ItemPY3DBP('50g [powder 2]', 4, 4, 10),
        ItemPY3DBP('50g [powder 2]', 4, 4, 10),
        ItemPY3DBP('50g [powder 2]', 4, 4, 10),
        
        
    ]

    packer=single_pack.single_pack(container, items)
    test_for_double_fit(packer, 10000)
    assert(packer.unfit_items==[])


def test_2():
    container=ContainerPY3DBP('very-very-large-box', 5, 5, 10)
    items=[
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        
        
    ]

    packer=single_pack.single_pack(container, items)
    test_for_double_fit(packer, 10000)
    assert(packer.unfit_items==[])

def test_3():
    container=ContainerPY3DBP('very-very-large-box', 5, 5, 10)
    items=[
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),

        
    ]

    packer=single_pack.single_pack(container, items)
    # 'None' valid arrangment
    assert(packer==None)

# the test that broke pyshipping :)
#bin=p.Package('1800x1800x2400')
#box=p.Package('450x975x793') # 17 of these
def dz_test():
    container=ContainerPY3DBP('container', 1800,1800,2400)
    items=[]
    import time
    start=time.time()
    for i in range(0, 17):
        items.append(ItemPY3DBP(str(i),450,975,793))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=True)
    end=time.time()
    print(end-start)
    assert(not (packer==None))
    
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
            lowerWidth, upperWidth=item.position[0], item.position[0]+item.get_dimension()[0]
            lowerDepth, upperDepth=item.position[1], item.position[1]+item.get_dimension()[1]
            lowerHeight, upperHeight=item.position[2], item.position[2]+item.get_dimension()[2]
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
def test_doublefitting_raises_exception():
    item1=ItemPY3DBP('id=1', 10,10,10)
    item2=ItemPY3DBP('id=2',10,10,10)
    container=ContainerPY3DBP('id=Container',20,20,20)
    # had to do this to avoid a stupid import structure
    rotationType=[0,1,2,3,4,5,6,7]
    packer=Packer(rotationType)
    packer.bins=[container]
    item1.position=[0,0,0]
    item2.position=[0,0,0]
    packer.items=[item1,item2]
    exceptionRaised=False
    try:
        test_for_double_fit(packer,100000)
    except:
        exceptionRaised=True
    if not exceptionRaised:
        raise Exception('double fit didnt raise an exception')

#test_1()
#test_2()
#test_3()
#dz_test()
#test_doublefitting_raises_exception()
#test_not_multibinpack()
