

from . import test_imports
from .test_imports import *



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


def test_2():
    container=ContainerPY3DBP('very-very-large-box', 5, 5, 10, 100)
    items=[
        ItemPY3DBP('50g [powder 2]', 5, 5, 5, 2),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5, 2),
        
        
    ]

    packer=single_pack.single_pack(container, items)
    test_for_double_fit(packer, 10000)
    assert(packer.unfit_items==[])

def test_3():
    container=ContainerPY3DBP('very-very-large-box', 5, 5, 10, 100)
    items=[
        ItemPY3DBP('50g [powder 2]', 5, 5, 5, 2),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5, 2),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5, 2),

        
    ]

    packer=single_pack.single_pack(container, items)
    # 'None' valid arrangment
    assert(packer==None)

# the test that broke pyshipping :)
#bin=p.Package('1800x1800x2400')
#box=p.Package('450x975x793') # 17 of these
def dz_test():
    container=ContainerPY3DBP('container', 1800,1800,2400,100000)
    items=[]
    for i in range(0, 13):
        items.append(ItemPY3DBP(str(i),450,975,793,1))
    packer=single_pack.single_pack(container,items,iterationLimit=1000,volumeSafeGuard=True, printIteration=True)
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
    if len(packer.bins)==0:
        raise Exception
    touchedCheck=False
    for container in packer.bins:

        for index in range(0, iterationLimit):
            # generate a random point
            pointWidth=random.random()*container.width
            pointDepth=random.random()*container.height
            pointHeight=random.random()*container.depth      
            
            cubesPointIsIn=0
            for item in container.items:
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
    item1=ItemPY3DBP('id=1', 10,10,10,1)
    item2=ItemPY3DBP('id=2',10,10,10,1)
    container=ContainerPY3DBP('id=Container',20,20,20,4)
    packer=Packer()
    packer.bins=[container]
    item1.position=[0,0,0]
    item2.position=[0,0,0]
    container.items=[item1,item2]
    exceptionRaised=False
    try:
        test_for_double_fit(packer,100000)
    except:
        exceptionRaised=True
    if not exceptionRaised:
        raise Exception('double fit didnt raise an exception')
test_1()
test_2()
test_3()
#dz_test()
test_doublefitting_raises_exception()