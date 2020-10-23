from . import testing_imports
from .testing_imports import *



def test_partial_result_1():
    items=['4x4x4','4x4x4']
    containers=['4x4x4']
    containerList,timedOut, arrangmentPossible=box_stuff2.master_calculate_optimal_solution(containers,items,60,False)
    assert(timedOut==False)
    assert(arrangmentPossible==True)
    usedContainer=containerList[0]
    
    assert(usedContainer.volume==(4*4*4))

test_partial_result_1()