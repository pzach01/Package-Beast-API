from . import py3dbp_main
from .py3dbp_main import Packer, ContainerPY3DBP, ItemPY3DBP
from .py3dbp_constants import RotationType
import itertools
import random
import time
import math
random.seed(1)
# same as item permutations but randomly iterates and using this generator can yield the same permutation twice
class CustomItemPermutations():
    def next(self,itemList):
        returnItems=[]
        while(len(itemList)>0):
            toSelect=random.randint(0, len(itemList)-1)
            returnItems.append(itemList.pop(toSelect))
        return returnItems
# attempt to pack items into a single container

def single_pack_given_timing_and_rotations(container, itemList, volumeSafeGuard, printIteration, timeout, rotationType,randomSearch):

    endTime=None
    if timeout==None:
        endTime=math.inf
    else:
        endTime=time.time()+timeout  
    # container volume greater then sum of items we are trying to fit
    if volumeSafeGuard:
        if container.volume< sum([item.volume for item in itemList]):
            return None
    

    
    



    if not randomSearch:
        item_permutations=(itertools.permutations(itemList,len(itemList)))
        import copy
        count=0
        if len(itemList)==0:
            p= Packer(rotationType)
            p.items=[]
            p.unfit_items=[]
            p.set_container(container)
            return p
        for item_permutation in item_permutations:
            mixer=DimensionalMixupsGenerator(item_permutation)
            count+=1
            
            innerIteration=0
            while(True):
                try:
                    print("           innerIteration: "+str(innerIteration))
                    innerIteration+=1
                    render=False
                    itemsMixedUp=mixer.next()
                



                    packer =Packer(rotationType)
                    packer.set_container(copy.deepcopy(container))
                    for item in itemsMixedUp:
                        packer.add_item(item)
                    
                    res=packer.pack(render)
                    if res:
                        return packer
                    # timeout
                    if time.time()>endTime:
                        return None

                except StopIteration:

                    break
            if printIteration:
                print("     Iteration: "+str(count))


                #
        # if you couldn't find an arrangment
        return None    


    if randomSearch:
        count=0
        if len(itemList)==0:
            p= Packer(rotationType)
            p.items=[]
            p.unfit_items=[]
            p.set_container(container)
            return p
        # generates random permutations
        item_permutations_generator=CustomItemPermutations()
        import copy
        

        while(True):
            render=False


            item_permutation=item_permutations_generator.next(copy.deepcopy(itemList))
            
            mixer=DimensionalMixupsGenerator(item_permutation)
            mixer.count=random.randint(0, 6**(len(itemList))-1)
            itemsMixedUp=mixer.next()
        



            packer =Packer(rotationType)
            packer.set_container(copy.deepcopy(container))
            for item in itemsMixedUp:
                packer.add_item(item)
            
            res=packer.pack(render)
            if res:
                return packer
            if time.time()>endTime:
                return None

            if printIteration:
                print("     Iteration: "+str(count))
            count+=1


                #
        # if you couldn't find an arrangment; Never happens here (because we don't know which ones have been used)
        return None    

# wraps some of the higher level decisions up such as
# whether to search randomly or bruteforce
# whether to use the heuristic (and for how long)
# how long to search each of these things
def single_pack(container, itemList,volumeSafeGuard=True,printIteration=True,timeout=None):
    randomSearch=True
    if timeout==None:
        res= single_pack_given_timing_and_rotations(container, itemList, volumeSafeGuard, printIteration, 30,RotationType.HEURISTIC,randomSearch)
        if not(res==None):
            return res
        return single_pack_given_timing_and_rotations(container, itemList, volumeSafeGuard, printIteration, timeout,RotationType.ALL,randomSearch)
    else:
        res= single_pack_given_timing_and_rotations(container, itemList, volumeSafeGuard, printIteration, 30,RotationType.HEURISTIC,randomSearch)
        if not(res==None):
            return res
        return single_pack_given_timing_and_rotations(container, itemList, volumeSafeGuard, printIteration, timeout-30,RotationType.ALL,randomSearch)


# next() returns one of the possible ways to mixup the Length Width Height of an item for each item in the permutation; obviously not just 6 because it is for
# each item in the current ordering; 
# thus 6**n mixups
# ie. for each item
# L x W x H
# L x H x W
# H x L x W
# H x W x L
# W x H x L
# W x L x H
class DimensionalMixupsGenerator():
    def base_6_as_switches(self, number, n):
        # want to throw a bug right away if something dumb happens
        switches=[-1 for ele in range(0, n)]
        for index in reversed(range(0, n)):
            switches[index]=number%(6)
            number=number//(6)
        return switches

    def __init__(self, item_permutation):
        self.item_permutation=item_permutation
        self.count=0
        self.max=6**(len(item_permutation))
    def next(self):
        # have enumerated all permutations
        if self.count==self.max:
            raise StopIteration

        newItems=[]
        switches=self.base_6_as_switches(self.count, len(self.item_permutation))
        
        for index in range(0, len(self.item_permutation)):
            if switches[index]==0:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].xDim, self.item_permutation[index].yDim, self.item_permutation[index].zDim))
            if switches[index]==1:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].xDim, self.item_permutation[index].zDim, self.item_permutation[index].yDim))
            if switches[index]==2:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].yDim, self.item_permutation[index].xDim, self.item_permutation[index].zDim))
            if switches[index]==3:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].yDim, self.item_permutation[index].zDim, self.item_permutation[index].xDim))
            if switches[index]==4:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].zDim, self.item_permutation[index].xDim, self.item_permutation[index].yDim))
            if switches[index]==5:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].zDim, self.item_permutation[index].yDim, self.item_permutation[index].xDim))


        

        self.count+=1
        return newItems
