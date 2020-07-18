from . import py3dbp_main
from .py3dbp_main import Packer, ContainerPY3DBP, ItemPY3DBP
from .py3dbp_constants import RotationType
import itertools
import random
import time
import math
import copy

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

def single_pack_given_timing_and_rotations(container, itemList, printIteration, globalTimeout,recursiveTimeout, rotationType,randomSearch,useBigSetsInDimensionalMixups):


    endTime=time.time()+globalTimeout  

    

    if len(itemList)==0:
        p= Packer(rotationType,recursiveTimeout)
        p.items=[]
        p.unfit_items=[]
        p.set_container(container)
        return p  



    if not randomSearch:
        # sort so that larger items are first
        itemList=list(reversed(sorted(itemList, key=lambda item: item.volume)))
        item_permutations=(itertools.permutations(itemList,len(itemList)))
        count=0

        for item_permutation in item_permutations:
            if printIteration:
                print("     Iteration: "+str(count))
            mixer=None
            if useBigSetsInDimensionalMixups:
                mixer=DimensionalMixupBigSetsGenerator(item_permutation)
            else:
                mixer=DimensionalMixupsGenerator(item_permutation)
            count+=1
            
            innerIteration=0

            while(True):
                try:
                    if printIteration:
                        print("           innerIteration: "+str(innerIteration))
                    innerIteration+=1
                    render=False
                    itemsMixedUp=mixer.next()
                



                    packer =Packer(rotationType,recursiveTimeout)
                    
                    packer.set_container(copy.deepcopy(container))
                    for item in itemsMixedUp:
                        packer.add_item(item)
                    try:
                        res=packer.pack(render)
                        if res:
                            return packer
                    except TimeoutError:
                        pass
                    # timeout
                    if time.time()>endTime:
                        return None

                except StopIteration:

                    break



                #
        # if you couldn't find an arrangment
        return None    


    if randomSearch:


        count=0

        # generates random permutations
        item_permutations_generator=CustomItemPermutations()
        

        while(True):
            if printIteration:
                print("     Iteration: "+str(count))
            render=False


            item_permutation=item_permutations_generator.next(copy.deepcopy(itemList))
            mixer=None
            if useBigSetsInDimensionalMixups:
                raise Exception("BigSets isn't supported for randomSearch")
            else:
                mixer=DimensionalMixupsGenerator(item_permutation)
            mixer.count=random.randint(0, 6**(len(itemList))-1)
            itemsMixedUp=mixer.next()
        



            packer =Packer(rotationType,recursiveTimeout)
            packer.set_container(copy.deepcopy(container))
            for item in itemsMixedUp:
                packer.add_item(item)
            try:
                res=packer.pack(render)
                if res:
                    return packer
            except TimeoutError:
                pass
            if time.time()>endTime:
                return None


            count+=1


                #
        # if you couldn't find an arrangment; Never happens here (because we don't know which ones have been used)
        return None    

# wraps some of the higher level decisions up such as
# whether to search randomly or bruteforce
# whether to use the heuristic (and for how long)
# how long to search each of these things
def single_pack(container, itemList,volumeSafeGuard=True,printIteration=True,timeout=30):
    # container volume greater then sum of items we are trying to fit
    if volumeSafeGuard:
        if container.volume< sum([item.volume for item in itemList]):
            return None
    
    recursiveTimeout=max(.00005*((len(itemList)*(len(itemList)+1))/2),.01)
    batchMultiplier=1
    timePerIterationType=10
    # heuristic: 30 second batches that gradually get larger
    while(timeout>0):
        # 1 percent growth in timeouts
        batchMultiplier*=1.01
        recursiveTimeout=recursiveTimeout*batchMultiplier
        timePerIterationType=timePerIterationType*batchMultiplier

        randomSearch=False
        useBigSetsInDimensionalMixups=True
        res= single_pack_given_timing_and_rotations(container, itemList, printIteration, min(timeout,timePerIterationType),min(timePerIterationType,min(timeout,recursiveTimeout)),RotationType.HEURISTIC,randomSearch,useBigSetsInDimensionalMixups)
        timeout-=timePerIterationType
        if not (res==None):
            return res
        


        randomSearch=True
        useBigSetsInDimensionalMixups=False
        
        res= single_pack_given_timing_and_rotations(container, itemList, printIteration, min(timeout,timePerIterationType),min(timePerIterationType,min(timeout,recursiveTimeout)),RotationType.HEURISTIC,randomSearch,useBigSetsInDimensionalMixups)
        timeout-=timePerIterationType  
        if not(res==None):
            return res

        res= single_pack_given_timing_and_rotations(container, itemList, printIteration, min(timeout,timePerIterationType),min(timePerIterationType,min(timeout,recursiveTimeout)),RotationType.ALL,randomSearch,useBigSetsInDimensionalMixups)
        timeout-=timePerIterationType
        if not(res==None):
            return res
        





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

class DimensionalMixupBigSetsGenerator():
    def base_6_as_switches(self, number, n):
        # want to throw a bug right away if something dumb happens
        switches=[-1 for ele in range(0, n)]
        for index in reversed(range(0, n)):
            switches[index]=number%(6)
            number=number//(6)
        return switches


    def increment_partion_count(self):
        if self.partitionArrangment[0]==len(self.item_permutation):
            raise StopIteration
        if self.partitionArrangment[1]==0:
            self.partitionArrangment=(0,self.partitionArrangment[0]+1,self.partitionArrangment[2]-1)
        else:
            self.partitionArrangment=(self.partitionArrangment[0]+1, self.partitionArrangment[1]-1, self.partitionArrangment[2])


    # returns the switches (0-5) for each item (3 in total)
    def get_item_arrangment(self,count):
        return self.base_6_as_switches(count, 3)
    # this is a special case of the general; but we chose 3 partitions because we don't have the speed 
    # to enumerate pase this for large n, and for small n it will be found by the random algorithm
    def get_switches_3_partition(self,count,n):
        if self.count==6**3:
            self.increment_partion_count()
            self.count=0
        switches=[-1 for ele in range(0, n)]

        currentIndex=0
        self.itemArrangment=self.get_item_arrangment(count)
        for index in range(0, self.partitionArrangment[0]):
            switches[currentIndex]=self.itemArrangment[0]
            currentIndex+=1
        for index in range(0, self.partitionArrangment[1]):
            switches[currentIndex]=self.itemArrangment[1]
            currentIndex+=1
        for index in range(0, self.partitionArrangment[2]):
            switches[currentIndex]=self.itemArrangment[2]
            currentIndex+=1

        return switches

    def __init__(self, item_permutation):
        self.item_permutation=item_permutation
        for item in item_permutation:
            # default to xDim>=yDim>=zDim
            item.xDim,item.yDim,item.zDim=list(reversed(sorted([item.xDim,item.yDim,item.zDim])))
        self.count=0
        self.max=6**3*(len(item_permutation)**3)
        self.partitionArrangment=(0,0,len(item_permutation))
    def next(self):
        # have enumerated all permutations
        if self.count==self.max:
            raise StopIteration

        newItems=[]
        switches=self.get_switches_3_partition(self.count,len(self.item_permutation))
        
        for index in range(0, len(self.item_permutation)):
            if switches[index]==0:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].xDim, self.item_permutation[index].yDim, self.item_permutation[index].zDim))
            elif switches[index]==1:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].xDim, self.item_permutation[index].zDim, self.item_permutation[index].yDim))
            elif switches[index]==2:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].yDim, self.item_permutation[index].xDim, self.item_permutation[index].zDim))
            elif switches[index]==3:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].yDim, self.item_permutation[index].zDim, self.item_permutation[index].xDim))
            elif switches[index]==4:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].zDim, self.item_permutation[index].xDim, self.item_permutation[index].yDim))
            elif switches[index]==5:
                newItems.append(ItemPY3DBP(self.item_permutation[index].name,self.item_permutation[index].zDim, self.item_permutation[index].yDim, self.item_permutation[index].xDim))
            else:
                print(switches)
                raise Exception("bug in BigSets generator")

        

        self.count+=1
        return newItems

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
