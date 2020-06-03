from . import py3dbp_main
from .py3dbp_main import Packer, ContainerPY3DBP, ItemPY3DBP
import itertools



def single_pack(container, itemList,iterationLimit=1000):
    # container volume greater then sum of items we are trying to fit
    if container.volume< sum([item.volume for item in itemList]):
        return None

    import math

    bin_weight_capacity = math.inf
    

    
    
    # Option 1 Just trys to place the items in the order defined. This may or may not find a solution since order matters
    #item_permutations = [items]
    
    # Option 2 All permutations of the items
    # This takes forever to generate the permutations
    item_permutations=(itertools.permutations(itemList,len(itemList)))
    #item_sets=set(itertools.permutations(itemList))
    #print(type(item_permutations))
    #print(type(item_sets))


    # Option 3 Shuffle items n times to form n different orders to try to place items
    
    #item_permutations = []
    #for i in range(iterationLimit):
    #    item_permutations.append(random.sample(itemList, len(itemList)))
    
    #
    import copy
    count=0

    for item_permutation in item_permutations:
        render=False
        
        count+=1
        
        packer =Packer()
        packer.add_bin(copy.deepcopy(container))
        for item in item_permutation:
            packer.add_item(item)
    
        packer.pack(render)
        if packer.bins[0].unfitted_items:
            pass
            #print("doesn't fit, yo")
        if not packer.bins[0].unfitted_items:
            #print("fits, yo!")
    
    

    
            x_vals = []
            y_vals = []
            z_vals = []
            widths = []
            heights = []
            depths = []
    
            for b in packer.bins:
    
                for item in b.items:
                    x_vals.append(float(item.position[0]))
                    y_vals.append(float(item.position[1]))
                    z_vals.append(float(item.position[2]))
    
                    # print("width:", float(item.width), "height:", float(item.height), "depth:", float(item.depth))
                    # print("dim_0:", item.get_dimension()[0], "dim_1:", item.get_dimension()[1], "dim_2:", item.get_dimension()[2])
                    widths.append(float(item.get_dimension()[0]))
                    heights.append(float(item.get_dimension()[1]))
                    depths.append(float(item.get_dimension()[2]))
    
                    #print(item.rotation_type)
    
                for item in b.unfitted_items:
                    pass
    
    
    
            return packer
            #
            
    
