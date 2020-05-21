
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
from . import package
from .package import Package
import time
from . import new_is_valid_corner_point_code




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

        # print("width:", float(item.width), "height:", float(item.height), "depth:", float(item.depth))
        # print("dim_0:", item.get_dimension()[0], "dim_1:", item.get_dimension()[1], "dim_2:", item.get_dimension()[2])
        xDim=int(item.get_dimension()[0])
        yDim=int(item.get_dimension()[1])
        zDim=int(item.get_dimension()[2])
        coordinate=(xPos+(xDim/2), yPos+(yDim/2), zPos+(zDim/2))
        retDict[coordinate]=Package(str(xDim)+"x"+str(yDim)+"x"+str(zDim), item.weight)
    return retDict


### returns aDictionary with keys corresponding to unique coordinate, value corresponding to non unique bin
def slot_bin_with_coordinates(packageArrangment, bin):
    ### implicit in bin is idea that it is ranked consistently height=longest side, width=second longest side, length=shortest side
    
    #### thus a package arrangment corresponds to a specific arrangment (height, width, length aren't just longest sides ordered but reflect proper stack)
    retDict={}
    orgin=(0,0,0)
    midPointOfBin=generate_midpoint(orgin, bin.heigth, bin.width, bin.length)
    bounds=generate_extreme_points(midPointOfBin, bin.heigth, bin.width, bin.length)
    existingShapes=[]
    ### bounds obviously cant be in existing shapes, as a protocol checks that all new shapes are strictly outside existing shapes, which is impossible to add
    ### new shapes to the bin if this is so (logical contradiction)
    #existingShapes.append(bounds)
    # we cant ever add to an interior point (as we have already added to it) so we keep it on a banned point list
    interiorPoints=[]
    for package in packageArrangment:

        ### try to slot, if you can't add throw exception        
        ### the control structure past 'generate_extreme_points' is screwed up
        ### We should break out of trying to addThePackage once we can add it (thus updating retDict and other sideeffects), and also break when
        ## we discover we can't add from a corner point (only takes one extreme point out of bounds to disqualify the cornerPoint for a given shape)
        ### flatten the structured list of 'existingShapes' into just a list of points
        flattenedPoints=[]
        for list in existingShapes:
            for point in list:
                if ((point not in flattenedPoints) and (point not in interiorPoints)):
                    flattenedPoints.append(point)
        ### bounds isn't in existing shapes but should still be considered a place we can add point to
        for point in bounds:
            flattenedPoints.append(point)
        ### sort the points by the values you need to
        pointsWeCanAddTo=sort_points_we_can_add_to(flattenedPoints)
        ### 

        addedShape=False
        ### current failures: not adding to earlier succesful point
        ### not catching failure outside box
        for cornerPoint in pointsWeCanAddTo:
            midPoint=generate_midpoint(cornerPoint, package.heigth, package.width, package.length)            
            newShape=generate_extreme_points(midPoint, package.heigth, package.width, package.length)
            ### the shape exists within the bounds of the bin 
            if new_is_valid_corner_point_code.new_is_valid_corner_point(bounds,existingShapes,newShape):            
            #if is_valid_corner_point(bounds, existingShapes,newShape):
                ### add new shape to 'existingShapes'
                existingShapes.append(newShape)
                ### add the new coordinate and package to 'retDict'
                retDict[(midPoint)]=package
                addedShape=True
                interiorPoints.append(cornerPoint)
                break
                       
        if(not addedShape):
            raise ValueError("didnt add a shape")



        ### create some sort of fail condition if you cant add a shape to the box (throw Exception)
        
        
    
    return retDict

def is_valid_corner_point(bounds, existingShapes, newShape):
    if strictly_within(bounds, newShape):
        
        for oldShape in existingShapes:
            ### keep checking the list if this newShape is strictly outside oldShape
            sameShape=True
            for element in oldShape:
                if element in newShape:
                    pass
                else:
                    sameShape=False
            if(sameShape):
                return False
            if stictly_outside(oldShape, newShape):
                pass
            else:
                ### we cant add the newShape at corner point as it has bounds inside an old shape
                return False
            if stictly_outside(newShape, oldShape):
                pass
            else:
                return False
            
        ### add the point
        ### this wont actually work (out of scope but idea is correct below, add this shape to squares, midpoint to retDict)
        return True
    else:
        return False
'''
## returns if a shape is strictly outside dimensions of 'oldShape', ie. dont share space
def stictly_outside(oldShape, newShape):
    min, max=get_min_max_tuple(oldShape)
    ### < instead of <= because extreme points can have the same coordinate (2 extreme points at one coordinate)
    for extremePoint in newShape:
        if((min[0] <extremePoint[0]<max[0])):
            if((min[1] <extremePoint[1]<max[1])):
                if((min[2] <extremePoint[2]<max[2])):
                    return False
    return True
'''
def stictly_outside(oldShape, newShape):
    min, max=get_min_max_tuple(oldShape)
    ### < instead of <= because extreme points can have the same coordinate (2 extreme points at one coordinate)
    for extremePoint in newShape:
        if extremePoint in oldShape:
            pass
        else:
            if((min[0] <=extremePoint[0]<=max[0])):
                if((min[1] <=extremePoint[1]<=max[1])):
                    if((min[2] <=extremePoint[2]<=max[2])):
                        return False
    return True
def strictly_within(bounds, newShape):
    ## all extreme points are within bounds
    min, max=get_min_max_tuple(bounds)
    for extremePoint in newShape:
        if(not (extremePoint[0]>=min[0] and extremePoint[0]<=max[0])):
            return False
        if(not (extremePoint[1]>=min[1] and extremePoint[1]<=max[1])):
            return False
        if(not (extremePoint[2]>=min[2] and extremePoint[2]<=max[2])):
            return False
    
    
    return True

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
            

### assumes we are slotting to the top right of the corner point (ie. midpoint has a height, width, and length greater then the corner point)
def generate_midpoint(cornerPoint, height, width, length):
    return (cornerPoint[0]+(height/2), cornerPoint[1]+(width/2), cornerPoint[2]+(length/2))

### returns the 8 extreme points that define the bound of the 
def generate_extreme_points(midPoint, height, width, length):

    lowerHeight, upperHeight=midPoint[0]-(height/2), midPoint[0]+(height/2)
    lowerWidth, upperWidth= midPoint[1]-(width/2), midPoint[1]+(width/2)
    lowerLength, upperLength=midPoint[2]-(length/2), midPoint[2]+(length/2)
    
    p1=(lowerHeight,lowerWidth, lowerLength)
    p2=(lowerHeight,lowerWidth, upperLength)
    p3=(lowerHeight, upperWidth, lowerLength)
    p4=(lowerHeight, upperWidth, upperLength)
    p5=(upperHeight,lowerWidth, lowerLength)
    p6=(upperHeight,lowerWidth, upperLength)
    p7=(upperHeight, upperWidth, lowerLength)
    p8=(upperHeight, upperWidth, upperLength)    
    return [p1,p2,p3,p4,p5,p6,p7,p8]

def sort_points_we_can_add_to(pointsWeCanAddTo):
    ### sort by min value of first index in tuple, min value of second index in tuple, min value of third index in tuple, in that order
    return sorted(pointsWeCanAddTo, key=lambda element: (element[0], element[1], element[2]))













def binpack(packages, bin=None, iterlimit=1000000):
   
    from . import binpack_simple as bp 
    
    from . import single_pack as sp
    # convert to single pack format

    from . import py3dbp_main as m
    container=m.Bin('the_bin', bin.width, bin.heigth, bin.length, bin.weight)
    items = [m.Item('an_item', package.width, package.heigth, package.length, package.weight) for package in packages]
    packer=sp.single_pack(container, items)



    #return bp.binpack(packages, bin, iterlimit)
    return packer


    ### check that permutations are producing the correct number of items for the (unique bin unique balls problem)


### This is actually just the tetris algorithm. Given that there is an ordered arrangment whose orientation cant be changed,
### thus, we just need a list of extreme points and update each time. 
#The values describe the width, height and depth of the knapsack in that order.





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
        
        volumeList=sorted([bin.volume for bin in binList])
        costList=sorted(listOfCosts)
        
        # no solution possible
        if(sum(volumeList)<lowerBoundOnCheapestPossibleVolume):
            return float('inf')
        # try single element subsets
        for index in range(0, len(volumeList)):
            
            cheapestPossible=self.knapsack(volumeList,costList, 0,0, lowerBoundOnCheapestPossibleVolume, index)
            if(cheapestPossible!=None):
                return cheapestPossible
        # no solution
        return float('inf')
    # always returns the cheapest item first so need to keep track of solution (list is sorted)
    def knapsack(self,volumeList,costList, currentVolume, currentCost,lowerBoundOnCheapestPossibleVolume, depthLimit):
        for index in range(0, len(volumeList)):
            if(depthLimit==0):
                if(volumeList[index]+currentVolume>= lowerBoundOnCheapestPossibleVolume):
                    return costList[index]+currentCost
            else:
                # return the value obtained by using this element with further depth
                return self.knapsack(volumeList[0:index]+volumeList[index+1::],costList[0:index]+costList[index+1::], currentVolume+volumeList[index],currentCost+costList[index], lowerBoundOnCheapestPossibleVolume, depthLimit-1)
        # no solution
        return None
            
            
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

