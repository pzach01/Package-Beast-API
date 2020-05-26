
from . import box_stuff2



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
    
    
     
weight_testing()

cost_testing()