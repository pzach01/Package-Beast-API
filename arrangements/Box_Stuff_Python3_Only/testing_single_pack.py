

from . import testing_imports
from .testing_imports import *
# (not multibinpack= singlepack), this wierd name used to avoid confusing with single_pack.py, the 
# file used to render/pack items into a single container
def test_not_multibinpack():
    items=['4x4x4','4x4x4']
    containers=['4x4x4','4x4x4','10x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,500,False)
    assert(timedOut==True)
    assert(arrangmentPossible==True)
    usedContainer=[container for container in containerList if (len(container.boxes)>0)][0]
    assert(usedContainer.volume==(10*5*5))
def test_overfitting_one_item_one_container():
    items=['10x10x10']
    containers=['5x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,35,False)
    assert(timedOut)    

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

    packer=single_pack.single_pack(container, items,True,False)
    test_for_double_fit(packer, 10000)
    assert(packer.unfit_items==[])
    assert(packer.isOptimal)


def test_2():
    container=ContainerPY3DBP('very-very-large-box', 5, 5, 10)
    items=[
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        
        
    ]

    packer=single_pack.single_pack(container, items,True,False)
    test_for_double_fit(packer, 10000)
    assert(packer.unfit_items==[])
    assert(packer.isOptimal)


def test_3():
    container=ContainerPY3DBP('very-very-large-box', 5, 5, 10)
    items=[
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),
        ItemPY3DBP('50g [powder 2]', 5, 5, 5),

        
    ]

    packer=single_pack.single_pack(container, items,True,False)
    # 'None' valid arrangment
    assert(not packer.isOptimal)


def dz_test_12_12_2020():
    container=ContainerPY3DBP('container', 18,18,24)
    items=[]
    import time
    start=time.time()
    for i in range(0, 21):
        items.append(ItemPY3DBP(str(i),9.75,4.438,7.875))
    timeout=120
    batchTime=120
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False,timeout=timeout,batchTime=batchTime)
    end=time.time()
    print(str(end-start)+" ,DZ test 12-12-2020, intersections checked: "+str(packer.intersectionsChecked))
    if timeout>30 or batchTime>30:
        print("still too slow^")
    assert(packer.isOptimal)
# the test that broke pyshipping :)
#bin=p.Package('1800x1800x2400')
#box=p.Package('450x975x793') # 17 of these


# Kleenex

def kleenex_test():
    container=ContainerPY3DBP('container', 21.6875,15,6.125)
    items=[]
    import time
    start=time.time()
    for i in range(0, 9):
        items.append(ItemPY3DBP(str(i),8.9375,3.5625,4.75))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False)
    end=time.time()
    print(str(end-start)+" ,Kleenex test, intersections checked: "+str(packer.intersectionsChecked))
    assert(packer.isOptimal)
def kleenex_test_overfitting():
    container=ContainerPY3DBP('container', 21.6875,15,6.125)
    items=[]
    import time
    start=time.time()
    for i in range(0, 10):
        items.append(ItemPY3DBP(str(i),8.9375,3.5625,4.75))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False)
    end=time.time()
    print(str(end-start)+" ,Kleenex overfitting")
    assert(not packer.isOptimal)


def dz_test_19():
    container=ContainerPY3DBP('container', 1800,1800,2400)
    items=[]
    import time
    start=time.time()
    for i in range(0, 19):
        items.append(ItemPY3DBP(str(i),450,975,793))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False,timeout=1000)
    assert( packer.isOptimal)


    end=time.time()
    print(str(end-start)+" ,19 test, intersections checked: "+str(packer.intersectionsChecked))
def dz_test_18():
    container=ContainerPY3DBP('container', 1800,1800,2400)
    items=[]
    import time
    start=time.time()
    for i in range(0, 18):
        items.append(ItemPY3DBP(str(i),450,975,793))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False,timeout=1000)
    test_for_double_fit(packer, 10000)

    end=time.time()
    print(str(end-start)+" ,18 test, intersections checked: "+str(packer.intersectionsChecked))
    assert( packer.isOptimal)

def test_doublefitting_raises_exception():
    item1=ItemPY3DBP('id=1', 10,10,10)
    item2=ItemPY3DBP('id=2',10,10,10)
    container=ContainerPY3DBP('id=Container',20,20,20)
    # had to do this to avoid a stupid import structure
    ALL=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]]
    packer=Packer(ALL,60)
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

'''
# ensure packer.timeout=math.inf
def timing_testing():
    container=ContainerPY3DBP('container', 5,5,250)
    import time
    for maxItems in range(1,900):
        items=[]

        start=time.time()

        for i in range(0, maxItems):
            items.append(ItemPY3DBP(str(i),5,1,1))
        packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=True,timeout=1000)
        assert(not(packer==None))
        end=time.time()
        print(str(maxItems)+':'+str(end-start))
'''

def dumbest_test_case_ever():
    container=ContainerPY3DBP('container', 20,20,20)
    items=[]
    import time
    start=time.time()
    for i in range(0, 1):
        items.append(ItemPY3DBP(str(i),2,2,2))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False,timeout=1000)
    test_for_double_fit(packer, 10000)

    end=time.time()
    print(end-start)
    assert( packer.isOptimal)
def timing_test_case():
    container=ContainerPY3DBP('container', 20,20,20)
    import time
    startFinal=time.time()
    for maxItems in range(1, 800):
        start=time.time()
        items=[]
        for i in range(0, maxItems):
            items.append(ItemPY3DBP(str(i),1,1,1))
        packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False,timeout=1000)
        end=time.time()
        assert(packer.isOptimal)
        print(str(i)+":"+str(end-start))
    endFinal=time.time()
    print("Final time: "+str(endFinal-startFinal))
def hard_test_case():
    container=ContainerPY3DBP('container', 23,29.25,12.75)
    items=[]
    import time
    start=time.time()
    for i in range(0, 21):
        items.append(ItemPY3DBP(str(i),4.438,9.75,7.875))
    packer=single_pack.single_pack(container,items,volumeSafeGuard=True, printIteration=False,timeout=1000)
    test_for_double_fit(packer, 10000)

    end=time.time()
    print('Hard test case:'+str(end-start))
    assert( packer.isOptimal)
print('testing_single_pack.py')
hard_test_case()
dz_test_12_12_2020()
test_overfitting_one_item_one_container()
timing_test_case()
dumbest_test_case_ever()
test_1()
test_2()
test_3()
kleenex_test()
dz_test_18()
dz_test_19()
kleenex_test_overfitting()
test_doublefitting_raises_exception()
test_not_multibinpack()
