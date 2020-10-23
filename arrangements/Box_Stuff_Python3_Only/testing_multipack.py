from . import testing_imports
from .testing_imports import *

def test_ids_only_pack_one_container():
    items=['4x4x4','5x5x5']
    containers=['4x4x4','4x4x4','10x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,180, False,[0,1])
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usableContainers=([container for container in containerList if len(container.boxes)>0])    
    assert(len(usableContainers)==1)
    if usableContainers[0].boxes[0].xDim==4:
        assert(usableContainers[0].boxes[0].id==0)
    else:
        assert(usableContainers[0].boxes[0].id==1)

    if usableContainers[0].boxes[1].xDim==4:
        assert(usableContainers[0].boxes[1].id==0)
    else:
        assert(usableContainers[0].boxes[1].id==1)


def test_only_pack_one_container():
    items=['4x4x4','4x4x4']
    containers=['4x4x4','4x4x4','10x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,60, False)    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedContainers=len([container for container in containerList if len(container.boxes)>0])
    assert(usedContainers==1)
    usedContainer=([container for container in containerList if len(container.boxes)>0])[0]
    assert(usedContainer.volume==(10*5*5))


def test_4():
    items=['4x4x4','4x4x4']
    containers=['4x4x4','4x4x4','10x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items)    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedContainers=len([container for container in containerList if len(container.boxes)>0])
    assert(usedContainers==2)

def test_3():
    items=['5x5x5','5x5x5','7x7x7']
    containers=['5x5x5','5x5x5','7x7x7']
    containerList,timedOut,arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items)    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedContainers=len([container for container in containerList if len(container.boxes)>0])
    assert(usedContainers==3)

def test_2():
    containers=['20x20x20','22x20x20']
    items=['2x2x2','3x2x1','4x5x2','3x7x2']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items)    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==8000)
def test_1():
    print("Test 1 starting")
    bins=['10x10x10', '10x10x10']
    boxes=['5x5x5' for ele in range(0, 16)]
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes)    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==2000)

# test if adding the cost constraint behaves as 'sposed to
def cost_testing():


    bins=['10x10x10','8x8x8','8x8x8']
    boxes=['5x5x5','5x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[100, 1,1])    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==1024)
    
    
    

    bins=['10x10x10','8x8x8','8x8x8']
    boxes=['5x5x5','5x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[1, 1,1])  
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==1000)  
    
    
    

    bins=['10x10x10','8x8x8','8x8x8','7x7x7']
    boxes=['5x5x5','5x5x5']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[100, 1,1.50,1])    
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==855)

# from DZ
def multibinpack_test_1():
    items=['8.938x5.563x4.75']
    container1=['18x18x24']
    container2=['21.688x15x6.125']
    containerList1,timedOut1, arrangmentPossible1=box_stuff2.master_calculate_optimal_solution(container1,items)
    assert(timedOut1==False)
    assert(arrangmentPossible1==True)
    usedVolume1=sum([bin.volume for bin in containerList1 if len(bin.boxes) is not 0 ])
    assert(usedVolume1==7776)
    containerList2,timedOut2,arrangmentPossible2=box_stuff2.master_calculate_optimal_solution(container2,items)
    assert(timedOut1==False)
    assert(arrangmentPossible1==True)
    usedVolume2=sum([bin.volume for bin in containerList2 if len(bin.boxes) is not 0 ])
    assert(1992 <usedVolume2<1993)

    bothContainers=['18x18x24','21.688x15x6.125']
    containerList3,timedOut3,arrangmentPossible3=box_stuff2.master_calculate_optimal_solution(container2,items)
    assert(timedOut1==False)
    assert(arrangmentPossible1==True)
    usedVolume3=sum([bin.volume for bin in containerList3 if len(bin.boxes) is not 0 ])
    assert(1992<usedVolume3<1993)


def weight_testing():    
    
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1']
    binWeights=[100,100]
    boxWeights=[20,20]
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==8**3)    
    
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1','1x1x1','1x1x1','1x1x1']
    binWeights=[120,100]
    boxWeights=[20,20,20,20,20]
    containerList,timedOut,arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==10**3) 


    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1','1x1x1','1x1x1','1x1x1']
    binWeights=[151,100]
    boxWeights=[20,25,30,35,40]
    containerList,timedOut,arrangmentPossible=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==10**3) 

multibinpack_test_1()
test_ids_only_pack_one_container()
test_only_pack_one_container()
weight_testing()
test_1()
test_2()
test_3()
test_4()
print('passed test 1-4')
cost_testing()
