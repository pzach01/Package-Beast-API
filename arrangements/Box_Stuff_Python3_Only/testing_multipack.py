from . import test_imports
from .test_imports import *

def render_off_api():
    pass


def test_3():
    items=['5x5x5','5x5x5','7x7x7']
    containers=['5x5x5','5x5x5','7x7x7']
    containerList=box_stuff2.master_calculate_optimal_solution(containers,items,timeout=30)    
    usedContainers=len([container for container in containerList if len(container.boxes)>0])
    assert(usedContainers==1)

def test_2():
    containers=['20x20x20','22x20x20']
    items=['2x2x2','3x2x1','4x5x2','3x7x2']
    containerList=box_stuff2.master_calculate_optimal_solution(containers,items,timeout=30)    
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==8000)
def test_1():
    print("Test 1 starting")
    bins=['10x10x10', '10x10x10']
    boxes=['5x5x5' for ele in range(0, 16)]
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,timeout=30)    
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==2000)

# test if adding the cost constraint behaves as 'sposed to
def cost_testing():


    bins=['10x10x10','8x8x8','8x8x8']
    boxes=['5x5x5','5x5x5']
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[100, 1,1])    
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==1024)
    
    
    

    bins=['10x10x10','8x8x8','8x8x8']
    boxes=['5x5x5','5x5x5']
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[1, 1,1])  
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==1000)  
    
    
    

    bins=['10x10x10','8x8x8','8x8x8','7x7x7']
    boxes=['5x5x5','5x5x5']
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[100, 1,1.50,1])    
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==855)
    
    
    


def weight_testing():    
    
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1']
    binWeights=[100,100]
    boxWeights=[20,20]
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==8**3)    
    
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1','1x1x1','1x1x1','1x1x1']
    binWeights=[120,100]
    boxWeights=[20,20,20,20,20]
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==10**3) 


    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1','1x1x1','1x1x1','1x1x1']
    binWeights=[151,100]
    boxWeights=[20,25,30,35,40]
    containerList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    usedVolume=sum([bin.volume for bin in containerList if len(bin.boxes) is not 0 ])
    assert(usedVolume==10**3) 
    
    
     
#weight_testing()

#cost_testing()
#test_2()
#test_1()
test_3()