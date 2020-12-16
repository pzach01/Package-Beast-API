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

    bestPacker=None
    endTime=time.time()+globalTimeout  

    

    if len(itemList)==0:
        p= Packer(rotationType,recursiveTimeout)
        p.items=[]
        p.unfit_items=[]
        p.set_container(container)
        p.isOptimal=True
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



                                    

                    itemsMixedUp=mixer.next()


                    packer =Packer(rotationType,recursiveTimeout)
                    
                    packer.set_container(copy.deepcopy(container))
                    for item in itemsMixedUp:
                        packer.add_item(item)
                    try:
                        packer.pack()
                    except TimeoutError:
                        pass
                    if packer.isOptimal:
                        return packer
                    # set new best packer
                    if bestPacker==None:
                        bestPacker=packer
                    if sum([item.volume for item in bestPacker.bestItems])<sum([item.volume for item in packer.bestItems]):
                        bestPacker=packer

                    # timeout
                    if time.time()>endTime:
                        return bestPacker

                except StopIteration:

                    break



                #
        # if you couldn't find an arrangment
        return bestPacker    


    if randomSearch:


        count=0

        # generates random permutations
        item_permutations_generator=CustomItemPermutations()
        

        while(True):
            if printIteration:
                print("     Iteration: "+str(count))


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
                packer.pack()
            except TimeoutError:
                pass
            if packer.isOptimal:
                return packer
            if bestPacker==None:
                bestPacker=packer
            if sum([item.volume for item in bestPacker.bestItems])<sum([item.volume for item in packer.bestItems]):
                bestPacker=packer

            if time.time()>endTime:
                return bestPacker


            count+=1


                #
        # if you couldn't find an arrangment; Never happens here (because we don't know which ones have been used)
        return bestPacker    
def get_best_packer(packerA,packerB):
    if packerA==None:
        return packerB
    if packerB==None:
        return packerA
    if sum([item.volume for item in packerA.bestItems])<sum([item.volume for item in packerB.bestItems]):
        return packerB
    else:
        return packerA
    
# wraps some of the higher level decisions up such as
# whether to search randomly or bruteforce
# whether to use the heuristic (and for how long)
# how long to search each of these things
def single_pack(container, itemList,volumeSafeGuard=True,printIteration=True,timeout=30,batchTime=30):
    # container volume greater then sum of items we are trying to fit
    bestPacker=None
    
    recursiveTimeout=max(.00005*((len(itemList)*(len(itemList)+1))/2),.01)
    batchMultiplier=1

    oneNinthBatchTime=batchTime/9
    # heuristic: 30 second batches that gradually get larger
    while(timeout>0):
        # 1 percent growth in timeouts
        batchMultiplier*=1.01
        recursiveTimeout=recursiveTimeout*batchMultiplier
        oneNinthBatchTime=oneNinthBatchTime*batchMultiplier

        randomSearch=False
        useBigSetsInDimensionalMixups=True
        start=time.time()
        # use the heuristic 7/9 of the time
        res= single_pack_given_timing_and_rotations(container, itemList, printIteration, min(timeout,oneNinthBatchTime*7),min(oneNinthBatchTime,min(timeout,recursiveTimeout)),RotationType.HEURISTIC,randomSearch,useBigSetsInDimensionalMixups)
        end=time.time()
        timeout-=end-start
        if res.isOptimal:
            return res
        bestPacker=get_best_packer(bestPacker,res)

                


        randomSearch=True
        useBigSetsInDimensionalMixups=False
        start=time.time()        
        res= single_pack_given_timing_and_rotations(container, itemList, printIteration, min(timeout,oneNinthBatchTime),min(oneNinthBatchTime,min(timeout,recursiveTimeout)),RotationType.HEURISTIC,randomSearch,useBigSetsInDimensionalMixups)
        end=time.time()
        timeout-=end-start
        if res.isOptimal:
            return res
        bestPacker=get_best_packer(bestPacker,res)

        start=time.time()
        res= single_pack_given_timing_and_rotations(container, itemList, printIteration, min(timeout,oneNinthBatchTime),min(oneNinthBatchTime,min(timeout,recursiveTimeout)),RotationType.ALL,randomSearch,useBigSetsInDimensionalMixups)
        end=time.time()
        timeout-=end-start
        if res.isOptimal:
            return res
        bestPacker=get_best_packer(bestPacker,res)


    return bestPacker



class DimensionalMixupBigSetsGeneratorWithExhaustiveEnds():
    def __init__(self, item_permutation,exhaustiveEndingLength):
        # constant
        self.exhaustiveEndingLength=min(exhaustiveEndingLength,len(item_permutation))

            

        # observe that these two lists make up the whole list
        self.useBigSetsGenerator=len(item_permutation[0:(len(item_permutation)-self.exhaustiveEndingLength)])>0
        self.bigSetsGenerator=DimensionalMixupBigSetsGenerator(item_permutation[0:(len(item_permutation)-self.exhaustiveEndingLength)])
        self.notBigSetsItems=item_permutation[(len(item_permutation)-self.exhaustiveEndingLength):]

        self.maxCount=6**self.exhaustiveEndingLength

        self.count=self.maxCount
        self.bigSetsItems=None



        # temporary, debugging
        self.expectedList=None
    def next(self):
        # check if need to reset; do so if need be (count gets set to 0 and get next bigSetsItems)
        if self.count==self.maxCount:
            self.count=0
            
            if self.useBigSetsGenerator:
                self.bigSetsItems=self.bigSetsGenerator.next()

                # debugging
                if self.useBigSetsGenerator:
                    zippyLoo=zip(self.bigSetsItems,self.expectedList)
                    allSame=True
                    while(True):
                        try:
                            a,b=next(zippyLoo)
                            if not (a.xDim==b.xDim):
                                allSame=False
                            if not (a.yDim==b.yDim):
                                allSame=False
                            if not (a.zDim==b.zDim):
                                allSame=False
                            if not (a.name==b.name):
                                allSame=False
                        except StopIteration:
                            break
                    if allSame:
                        1+1
            # only need one pass if this is false, then clockout next time we hit max count
            else:
                self.useBigSetsGenerator=True
                # use empty list since everyting is over the full permutations
                self.bigSetsItems=[]


        # get permutations from count, dont reset the order of permutations in the master list
        notBigSetsTemp=self.getPermutations(self.count)
        
        self.count+=1

        return self.bigSetsItems+notBigSetsTemp
    def getPermutations(self, count):
        permutation=[]

        for index in (range(0, len(self.notBigSetsItems))):
            thisFlip=count%6
            count=count//6


            if thisFlip==0:
                permutation.append(ItemPY3DBP(self.notBigSetsItems[index].name,self.notBigSetsItems[index].xDim, self.notBigSetsItems[index].yDim, self.notBigSetsItems[index].zDim))
            elif thisFlip==1:
                permutation.append(ItemPY3DBP(self.notBigSetsItems[index].name,self.notBigSetsItems[index].xDim, self.notBigSetsItems[index].zDim, self.notBigSetsItems[index].yDim))
            elif thisFlip==2:
                permutation.append(ItemPY3DBP(self.notBigSetsItems[index].name,self.notBigSetsItems[index].yDim, self.notBigSetsItems[index].xDim, self.notBigSetsItems[index].zDim))
            elif thisFlip==3:
                permutation.append(ItemPY3DBP(self.notBigSetsItems[index].name,self.notBigSetsItems[index].yDim, self.notBigSetsItems[index].zDim, self.notBigSetsItems[index].xDim))
            elif thisFlip==4:
                permutation.append(ItemPY3DBP(self.notBigSetsItems[index].name,self.notBigSetsItems[index].zDim, self.notBigSetsItems[index].xDim, self.notBigSetsItems[index].yDim))
            elif thisFlip==5:
                permutation.append(ItemPY3DBP(self.notBigSetsItems[index].name,self.notBigSetsItems[index].zDim, self.notBigSetsItems[index].yDim, self.notBigSetsItems[index].xDim))
            else:
                print(switches)
                raise Exception("bug in BigSetsWithExhaustiveEnds generator")
        return permutation

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
    def increment_partion_count_2(self):
        # reset
        if self.partitionArrangment[1]==len(self.item_permutation):
            self.allTwosVisited=True
            # gets incremented to 0 down the line
            self.count=-1
            self.partitionArrangment=(0,0,len(self.item_permutation))
        else:
            self.partitionArrangment=(0, self.partitionArrangment[1]+1, self.partitionArrangment[2]-1)

    # returns the switches (0-5) for each item (3 in total)
    def get_item_arrangment(self,count,n):
        return self.base_6_as_switches(count, n)
    # this is a special case of the general; but we chose 3 partitions because we don't have the speed 
    # to enumerate pase this for large n, and for small n it will be found by the random algorithm
    def get_switches_2_parition(self,count,length):
        if self.count==6**2:
            self.increment_partion_count_2()
            self.count=0
        switches=[-1 for ele in range(0, length)]

        currentIndex=0
        self.itemArrangment=self.get_item_arrangment(self.count,2)
        # note, we start on the RHS of the tuple and 'count' over to the left, hence index 0 is unused in the 2 case
        for index in range(0, self.partitionArrangment[1]):
            switches[currentIndex]=self.itemArrangment[0]
            currentIndex+=1
        for index in range(0, self.partitionArrangment[2]):
            switches[currentIndex]=self.itemArrangment[1]
            currentIndex+=1

        return switches
    def get_switches_3_partition(self,count,length):
        if self.count==6**3:
            self.increment_partion_count()
            self.count=0
        switches=[-1 for ele in range(0, length)]

        currentIndex=0
        self.itemArrangment=self.get_item_arrangment(self.count,3)
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
        self.allTwosVisited=False
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
        if self.allTwosVisited:
            switches=self.get_switches_3_partition(self.count,len(self.item_permutation))
        else:
            switches=self.get_switches_2_parition(self.count,len(self.item_permutation))

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
