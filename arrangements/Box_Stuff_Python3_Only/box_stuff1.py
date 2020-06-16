
#!/usr/bin/env python
# encoding: utf-8
### DEPDENDECIES:
### python2.7
### pyshipping
### Microsoft Visual Studio (python extension), should show up 
### unsuccessful download via pip, only works via running python setup.py install upon pulling from git


### note to self: everything is all good because if a bin returns more then 1 bin, then we can't use it anyway
### this will result in repeat processing (ie. 2 of same type could be handled naively by algorithm, and maybe should later on)
### but from a permutations perspective there is nothing wholly suboptimal that can't be solved by additional computation


### as the permuation will delegate a set of packages to a bin and answer deterministically if they can fit in the package


### other optimization: if we achieve some benchmark (ie. min volume/cost of 100 cc or $100, we automatically disregard certain permutations such
### as an arragment of boxes that uses more then 100 cc or more then $100

### runtime discussion:
#https://www.careerbless.com/aptitude/qa/permutations_combinations_imp7.php
## k distinct balls into n boxes

#https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)
### gives the indexes of where the sticks should be placed in 

#Many elementary word problems in combinatorics are resolved by the 
#theorems above. For example, if one wishes to count the number of ways to distribute seven 
#indistinguishable one dollar coins among Amber, Ben, and Curtis so that each of them receives at least one dollar, 
#one may observe that distributions are essentially equivalent to tuples of three positive integers whose sum is 7.
#(Here the first entry in the tuple is the number of coins given to Amber, and so on.) Thus the stars and bars apply with n = 7 
#and k = 3, and there are (7-1 \choose 3-1)=15}ways to distribute the 
#coins. (by Theorem 2)

from __future__ import division
import itertools
import copy
import math
import time
#from . import new_is_valid_corner_point_code




### returns the number of items that belong in each bin
### because the boxes are sorted, this means we merely have to traverse through the bins and add the amount of boxes (from front of list)
### (or any nonambigous popping algorithm) and add this to the bin
def partitions(n, k):
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]
    

def convert_dimension_string_to_package_object(listOfBinsDimensions, listOfObjectsDimensions):
    return listOfBinsDimensions, listOfObjectsDimensions
    numObjects=len(listOfObjectsDimensions)
    numBins=len(listOfBinsDimensions)
    
    binList=[]
    objectList=[]
    for dim in listOfBinsDimensions:
        binList.append(Package(dim))
    for dim in listOfObjectsDimensions:
        objectList.append(Package(dim))
    return binList, objectList
# remove solutions that are more expensive then current cheapest
def remove_overly_expensive_solutions(partitions, costList, upperBound):
    newPartions=[]
    for partion in partitions:
        bound=0
        for index in range(0, len(partion)):
            ## if the bin is used (ie. contains an object)
            if(partion[index]!=0):
                bound+=costList[index]
        if(bound<=upperBound):
           
            newPartions.append(partion)


                
    return newPartions


            

    
    



            
def remove_duplicate(oldList):
    newSet=set()
    newList=[]
    for element in oldList:
        if(str(element) not in newSet):
            newSet.add(str(element))
            newList.append(element)
    return newList


        
def generate_an_arrangement(permutation,partition):
    anArrangementOfBoxesAndBins=[]            
    counter=0       
    tempPermutation=copy.deepcopy(permutation)
    tempPartition=copy.deepcopy(partition)
    
    while(len(tempPartition)!=0):
        ### get the number of boxes we can add
        numBoxesInThisBin=tempPartition.pop(0)
        oneBin=set()
        ### add num boxes to this bin
        for element in range(counter, numBoxesInThisBin+counter):
            counter+=1
            oneBin.add(tempPermutation.pop(0))
        anArrangementOfBoxesAndBins.append(oneBin)
        
    return anArrangementOfBoxesAndBins

"""
binpack.py

Created by Maximillian Dornseif on 2010-08-16.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

def slot_bin_with_coordinates_py3dbp(packageArrangment, bin):
    retDict={}
    for item in packageArrangment.items:


        xPos=float(item.position[0])
        yPos=float(item.position[1])
        zPos=float(item.position[2])

        xDim=int(item.get_dimension()[0])
        yDim=int(item.get_dimension()[1])
        zDim=int(item.get_dimension()[2])
        coordinate=(xPos+(xDim/2), yPos+(yDim/2), zPos+(zDim/2))
        from . import py3dbp_main
        from .py3dbp_main import ItemPY3DBP
        retDict[coordinate]=ItemPY3DBP('', xDim, yDim, zDim,item.weight)
        #retDict[coordinate]=Package(str(xDim)+"x"+str(yDim)+"x"+str(zDim), item.weight)
    return retDict


def get_min_max_tuple(extremePoints):
    minX,minY,minZ=extremePoints[0][0],extremePoints[0][1],extremePoints[0][2]
    maxX,maxY,maxZ=extremePoints[0][0],extremePoints[0][1],extremePoints[0][2]
    for extremePoint in extremePoints:
        if(extremePoint[0]<minX):
            minX=extremePoint[0]
        if(extremePoint[0]>maxX):
            maxX=extremePoint[0]
        if(extremePoint[1]<minY):
            minY=extremePoint[1]
        if(extremePoint[1]>maxY):
            maxY=extremePoint[1]
        if(extremePoint[2]<minZ):
            minZ=extremePoint[2]
        if(extremePoint[2]>maxZ):
            maxZ=extremePoint[2]
        
    return (minX,minY,minZ), (maxX,maxY,maxZ)
  

def sort_points_we_can_add_to(pointsWeCanAddTo):
    ### sort by min value of first index in tuple, min value of second index in tuple, min value of third index in tuple, in that order
    return sorted(pointsWeCanAddTo, key=lambda element: (element[0], element[1], element[2]))













def binpack(packages, bin=None,timeout=None):
   
    
    from . import single_pack as sp
    # convert to single pack format

    from . import py3dbp_main as m

    packer=sp.single_pack(bin, packages,True, False, timeout)



    #return bp.binpack(packages, bin, iterlimit)
    return packer


    ### check that permutations are producing the correct number of items for the (unique bin unique balls problem)


### This is actually just the tetris algorithm. Given that there is an ordered arrangment whose orientation cant be changed,
### thus, we just need a list of extreme points and update each time. 





def get_cost(numBins, numBoxes):
    print("K :"+str(numBins)+ ", N:"+str(numBoxes))
    print("lower: "+str(numBins**numBoxes))  

    partitionList=list(partitions(numBoxes,numBins))

    permutationsWithoutSticks=[list(element) for element in list(itertools.permutations(list(range(0,numBoxes)), numBoxes))]    
    upper=len(permutationsWithoutSticks)*len(partitionList)
    print("upper: "+str(upper))
    print("")    
    


class OptimizeBoxesGenerator:
    def __init__(self,listOfBinsDimensions, listOfObjectsDimensions,listOfCosts):        
        import time
        numBins=len(listOfBinsDimensions)
        numObjects=len(listOfObjectsDimensions)
        self.listOfCosts=listOfCosts
        self.binList, objectList=convert_dimension_string_to_package_object(listOfBinsDimensions,listOfObjectsDimensions)
            

        # get the cheapest possible cost (volume or $) that is obtainable theoretically
        self.cheapestPossible=self.get_cheapest_possible(self.binList, objectList,listOfCosts)
        self.minCost=float('inf')

        self.partitionList=list(partitions(numObjects,numBins))
        ### remove all possible bin arrangments that have a volume lower then the sum of the volumes of the objects (trivial lower bound)
        self.partitionList=self.disqualify_overly_cheap_solutions(self.partitionList,listOfCosts, self.cheapestPossible)
        self.permutationsWithoutSticks=itertools.permutations(list(range(0,numObjects)), numObjects)
        self.currentPermutation=None
        ## will have lots of duplicate sets
        self.partitionCount=len(self.partitionList)-1

        
        
        

        ## will have lots of duplicate sets

        
        
        ### remove all possible bin arrangments that have a volume lower then the sum of the volumes of the objects (trivial lower bound)
    
    # returns the cheapest possible solution: the smallest possible volume that is greater then the sum of the objects to be packed
    # this could be comp. intensive
    # knapsack problem (special case)
    # find smallest volume subset that is greater then lowerBoundOnCheapestPossibleVolume, often just a single bin    
    def get_cheapest_possible(self,binList, objectList,listOfCosts):
        # we cant have a set of bins that has volume lower then this in a valid solution
        lowerBoundOnCheapestPossibleVolume=sum([box.volume for box in objectList])
        
        volumeList=([bin.volume for bin in binList])
        
        # no solution possible
        if(sum(volumeList)<lowerBoundOnCheapestPossibleVolume):
            return float('inf')
        # try single element subsets
        return self.knapsack(volumeList, listOfCosts, 0, lowerBoundOnCheapestPossibleVolume)
    # always returns the cheapest item first so need to keep track of solution (list is sorted)
    def knapsack(self,volumeList, costList, currentVolume, minVolume):
        if currentVolume>=minVolume:
            return 0
        bestCost=math.inf
        for index in range(0,len(volumeList)):
            if volumeList[index]+currentVolume>=minVolume:
                currentCost=costList[index]
            else:
                currentCost=costList[index]+self.knapsack(volumeList[0:(index)]+volumeList[(index+1):], costList[0:(index)]+costList[(index+1):], currentVolume+volumeList[index], minVolume)
            if currentCost<bestCost:
                bestCost=currentCost
        return bestCost
         
            
    # reverse of other
    def disqualify_overly_cheap_solutions(self,partitions,listOfCosts, cheapestPossible):
        newPartions=[]
        for partion in partitions:
            bound=0
            for index in range(0, len(partion)):
                ## if the bin is used (ie. contains an object)
                if(partion[index]!=0):
                    bound+=listOfCosts[index]
            if(bound>=cheapestPossible):
               
                newPartions.append(partion)
        return newPartions
    # no solution that exceeds this exists (implies more bins)
    def update_partition():
        pass
    def updateMinCost(self, minCost):
        self.minCost=minCost
        self.partitionList=remove_overly_expensive_solutions(self.partitionList, self.listOfCosts, self.minCost)
        self.partitionCount=0
    def get_next_arrangment(self):  
        if(self.minCost==self.cheapestPossible):
            raise StopIteration
        if(len(self.partitionList)==0):
            raise StopIteration
        # generator implicitly allows checking of end of arrangments
        if (self.partitionCount==len(self.partitionList)-1):
            self.partitionCount=0
            self.currentPermutation=next(self.permutationsWithoutSticks)
        else:
            self.partitionCount+=1            
    
        returnValue= generate_an_arrangement(list(self.currentPermutation),self.partitionList[self.partitionCount])
        return returnValue
        
        # if the partition count is too high reset and get next permutation, else add 1

