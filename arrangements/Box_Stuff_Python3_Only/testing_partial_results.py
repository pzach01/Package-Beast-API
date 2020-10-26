from . import testing_imports
from .testing_imports import *



def test_partial_result_1():
    items=['4x4x4','4x4x4']
    containers=['4x4x4']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,60,False)
    assert(timedOut==True)
    assert(arrangmentPossible==True)
    usedContainer=containerList[0]
    
    assert(usedContainer.volume==(4*4*4))
def test_partial_result_2():
    items=['1x1x1','1x1x1']
    containers=['2x2x1','2x1x1']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,60,False)
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedContainer=None
    for container in containerList:
        if container.volume==2:
            usedContainer=container
    
    assert(len(usedContainer.boxes)==2)
    #usedContainer=containerList[0]
    
    #assert(usedContainer.volume==(4*4*4))
test_partial_result_1()
test_partial_result_2()