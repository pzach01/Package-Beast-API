from __future__ import division
import os
from . import box_stuff1

from . import py3dbp_main
from .py3dbp_main import ItemPY3DBP, ContainerPY3DBP

import random
import copy
import math
import itertools

def calculate_partion_list_size(binListSize, itemListSize):
    return math.factorial(binListSize+itemListSize-1)/(math.factorial(binListSize)*math.factorial(itemListSize-1))

def bruteforce(generator, binMasterList, boxMasterList,endTime,costList,binWeightCapacitys, boxWeights):
    import time
    timedOut=False
    minCost=float('inf')
    arrangment=None
    while(True):
        try:
            if(time.time()>endTime):
                timedOut=True
                break
            combination=generator.get_next_arrangment()        
            cost=calculate_cost(costList, combination)
            if(cost<minCost):        
                valid=True
                for binIndex in range(0, len(combination)):
                    bin=binMasterList[binIndex]
                    boxIndexes=[num for num in combination[binIndex]]
                    boxes=[]
                    for boxIndex in boxIndexes:
                        boxes.append((boxMasterList[boxIndex]))
                    ### uses one box with nothing leftover
                    if(len(boxes)!=0):
                        binpackResult=box_stuff1.binpack(boxes,bin)
                        if (binpackResult==None):
                            
                            valid=False
                            break
                        if(not weight_is_ok(binIndex,boxIndexes, binWeightCapacitys,boxWeights)):
                            valid=False
                            break
                ### arrangment is possible in this num bins
                if(valid):
                    minCost=cost
                    generator.updateMinCost(minCost)
                    arrangment=combination
        except StopIteration:
            break
    return arrangment, minCost,timedOut
                
# bin can hold boxes without going over weight limit
def weight_is_ok(binIndex, boxIndexes, binWeightCapacitys, boxWeights):
    if(binWeightCapacitys==None):
        return True
    
    maxWeight=binWeightCapacitys[binIndex]
    realWeight=0
    for index in boxIndexes:
        realWeight+=boxWeights[index]
    if(realWeight<maxWeight):
        return True
    else:
        return False

def calculate_cost(costList, arrangment):
    cost=0
    for setIndex in range(0, len(arrangment)):
        if len(arrangment[setIndex])!=0:
            cost+=costList[setIndex]
    return cost

# an arrangment of boxes and bins doesnt come with xyz coordinates in pyshipping, but arrangment seems to be implied by pyshipping (relatively untested)
def get_xyz_of_optimal_solution(minArrangment,bins1, boxs1,endTimeRendering):
    binList=[]
    packageList=[]    
    for index in range(0, len(minArrangment)):
        if(len(minArrangment[index])!=0):
            bin=bins1[index]
            boxesUsed=[]
            for setIndex in minArrangment[index]:
                boxesUsed.append(boxs1[setIndex])
            
            #print(boxesUsed)
            #print(bin)
            ### boxes used instead of leftover boxes are selected
            boxArrangment=box_stuff1.binpack(boxesUsed, bin, 2000000)
            #rendering failed the second time
            assert(boxArrangment is not None)
            #select the first box
            
            
            
            try:
                coordinateDict=box_stuff1.slot_bin_with_coordinates_py3dbp(boxArrangment, bin)
            ### couldnt figure out how to add with this particurlar bin arrangment 
            except ValueError:
                raise ValueError            
            
            # old code that falsely claimed to enumerate all the ways we can arrange the boxes (ignores rotations!)
            '''
            # get all the orders in which boxes can be placed into a single bin
            allArrangments=(itertools.permutations(boxArrangment,len(boxArrangment)))
            try:
                #get all permutations of the way boxes can fit in the bin: orientation doesnt matter (this is handled by slot_bin_with_coordinates) but order does
                while(True):
                    try:
                        # python3 specific
                        boxArrangment=next(allArrangments)
                        coordinateDict=box_stuff1.slot_bin_with_coordinates(boxArrangment, bin)
                        # if you find a single solution to pack the bin in; break
                        break
                    except ValueError:
                        pass
                        
            ### couldnt figure out how to add with this particurlar bin arrangment 
            except StopIteration:
                raise ValueError
            '''
            
            ### bins obviously dont have coordinates, also dictionary with bin as key could result in data overwrites if there are 2 of the same bin size
            ### as a result I use 2 lists
            binList.append(bin)
            packageList.append(coordinateDict)   
    return binList, packageList
# do 'numBins' simulations to minimize cost
# this is an exceedingly stupid way to do it, we make no assumptions about what an acceptable bin will look like and so (usually) produces suboptimal
# results unless you do a ton of simulations (maybe around 100k?, untested)
def hypothetical_binpack(numBins, boxs1, timeout=0, costList=None, binWeightCapacities=None, boxWeights=None):
    import random
    # do a bunch of random simulations to get a decent starting solution
    # this is an exceedingly large search space by using this parameter but we cant make any other assumptions without more work
    upperBound=sum([Package(box).heigth for box in boxs1])
    randomBins=[]
    for ele in range(0, numBins):
        x,y,z=random.randint(1, upperBound), random.randint(1, upperBound), random.randint(1,upperBound)
        binString=str(x)+'x'+str(y)+'x'+str(z)
        randomBins.append(binString)
    return fit_all(randomBins, boxs1, timeout, costList, binWeightCapacities, boxWeights)
            
    
    
    # then try to reduce dimensions by 1 (this gurantees that at least 1 dimension (x y or z) is tight against the boxes)
    
# attempt to fill all boxes in one of the bins
# Note to self: the backend code actually uses the API here 
def fit_all(bins1, boxs1, timeout=0, costList=None, binWeightCapacitys=None, boxWeights=None):
    import math
    minCost=math.inf
    minArrangment=None
    
    # this is exact replication of code in bruteforce, suboptimal but allows us to seperate api and backend
    internalBoxs1=[Package(box) for box in boxs1]
    internalBins1=[Package(bin) for bin in bins1] 
    assert((binWeightCapacitys==None and boxWeights==None) or (binWeightCapacitys!=None and binWeightCapacitys!=None))
    if(costList==None):
        internalCostList=[bin.volume for bin in internalBins1]    
    # end replication of bruteforce code
    
    for ele in range(0, len(bins1)):
        try:
            if(internalCostList[ele]<minCost):
                # cant subscript none so must use lambda
                miniCostList=None if costList==None else [costList[ele]]
                miniBinWeightCapacitys=None if binWeightCapacitys==None else [binWeightCapacitys[ele]]
                # call master_calculate_optimal_solution with just one bin
    
                apiFormat=master_calculate_optimal_solution([bins1[ele]], boxs1,timeout, miniCostList, miniBinWeightCapacitys, boxWeights)
                
                # no error, update to better solution
                minArrangment=apiFormat
                minCost=internalCostList[ele]
                
        # ran out of time
        except TimeoutError:
            pass
        # no solution, look for next bin
        except NotImplementedError:
            pass
    return apiFormat

# wrapper for the ItemPY3DBP class
def string_wrapper_for_item_class(itemString):
    l,w,h=float(itemString.split('x')[0]),float(itemString.split('x')[1]),float(itemString.split('x')[2])
    return ItemPY3DBP('',l,w,h,0)
def string_wrapper_for_container_class(itemString):
    l,w,h=float(itemString.split('x')[0]),float(itemString.split('x')[1]),float(itemString.split('x')[2])
    return ContainerPY3DBP('',l,w,h,0)
# bin weights must be in same order, same for box weights
def master_calculate_optimal_solution(bins1, boxs1,timeout=0,costList=None,binWeightCapacitys=None, boxWeights=None):
    # metaparameter, expose to API at some point
    renderingPercentageOfComputation=.5
    
    computationTimeout=timeout*(1-renderingPercentageOfComputation)
    renderingTimeout=timeout*(renderingPercentageOfComputation)
    
    assert(computationTimeout+renderingTimeout==timeout)
    import math
    import time
    
    partitionListSize=calculate_partion_list_size(len(bins1), len(boxs1))
    # half a billion
    maxMemorySize=500000000
    if(partitionListSize > maxMemorySize):
        raise TimeoutError("this is too big for the current algorithm, reduce number of bins or boxes")
    
    # if we reach this time trigger a timeout error
    endTimeComputation=math.inf if timeout==0 else time.time()+computationTimeout
    endTimeRendering=endTimeComputation+renderingTimeout
    
    # string intiliaztion
    boxs1=[string_wrapper_for_item_class(box) for box in boxs1]
    bins1=[string_wrapper_for_container_class(bin) for bin in bins1] 
    
    assert((binWeightCapacitys==None and boxWeights==None) or (binWeightCapacitys!=None and binWeightCapacitys!=None))

    
    # minimize volume if there is no cost list, otherwise use dollar
    if(costList==None):
        costList=[bin.volume for bin in bins1]
    
 
    # this cant timeout because its contribution to time should be minimal
    generator=box_stuff1.OptimizeBoxesGenerator(bins1,boxs1,costList)


    
    ## find the index arrangment of the cheapest combination (actual computation)
    minArrangment, minCost,timedOut=bruteforce(generator,bins1, boxs1,endTimeComputation,costList,binWeightCapacitys,boxWeights)
    if(minCost==float('inf')):
        raise NotImplementedError("no arrangment possible")

    
    
    ### min arrangment is merely indexes, still need the actual packages in there
    
    ### these should be equal in length

    binList, packageList=get_xyz_of_optimal_solution(minArrangment, bins1, boxs1,endTimeRendering)
    
    #return binList,packageList
    
    # new stuff, last two things are only for debugging if necessary
    apiFormat=convert_to_api_form(minArrangment, binList, packageList, bins1, boxs1, costList,binWeightCapacitys,boxWeights,timedOut)
    ### now that minimum arrangment indices have been found, actually find the coordinates of such bins

    return apiFormat


class BinAPI():
    def to_string(self):
        binAttributes="("+str(self.id)+","+str(self.height)+","+str(self.width)+","+str(self.length)+","+str(self.volume)+","+str(self.cost)+","+str(self.weightCapacity)+","+str(self.timedOut)
        boxAttributes=""
        for box in self.boxes:
            boxAttributes+=box.to_string()
        # end of the string
        boxAttributes+=")"
        return binAttributes+boxAttributes
    
    def to_dictionary(self):
        aDictionary={}
        aDictionary['id']=self.id
        aDictionary['height']=self.height
        aDictionary['width']=self.width
        aDictionary['length']=self.length
        aDictionary['volume']=self.volume
        aDictionary['cost']=self.cost
        aDictionary['weightCapacity']=self.weightCapacity
        # this is basically just a fancy for loop
        aDictionary['timedOut']=self.timedOut
        aDictionary['itemList']=[box.to_dictionary() for box in self.boxes]
        return aDictionary
    def __init__(self,id,height, width, length,cost, weightCapacity,timedOut):
        self.id=id
        
        self.height=float(height)
        self.width=float(width)     
        self.length=float(length)
        self.volume=float(length*width*height)
        
        
        self.cost=float(cost)
        self.weightCapacity=float(weightCapacity) if (weightCapacity is not None) else weightCapacity
        self.timedOut=timedOut
        self.boxes=[]
        self.id=0
    def set_id(self, id):
        self.id=id

    
    def add_box(self, box):
        self.boxes.append(box)
    # key value ordering is reversed
    # add the coordinate field to each box in the bin
    
    # such an oof
    def format_coordinates(self, coordinateDictionary):
        # dont reslot coordinates twice, we don't really care where a given box of the same dimensions goes
        slotted=[]
        for key in coordinateDictionary.keys():
            package=coordinateDictionary[key]
            height, width, depth=package.height, package.width, package.depth
            for boxIndex in range(0, len(self.boxes)):
                # boxes have the same coordinates
                
                # we have to do this because internally the HxLxD might get swapped around by the algorithm
                if (sorted([self.boxes[boxIndex].height,self.boxes[boxIndex].width,self.boxes[boxIndex].length])==sorted([height,width,depth])):
#                if((self.boxes[boxIndex].height==height and self.boxes[boxIndex].width==width)and self.boxes[boxIndex].length==depth):
                    self.boxes[boxIndex].set_center(key)
                    slotted.append(self.boxes.pop(boxIndex))
                    break
                
        self.boxes=slotted


class BoxAPI():
    def __init__(self,height, width, length,volume,weight):
        self.height=float(height)
        self.width=float(width)
        self.length=float(length)
        self.volume=float(volume)
        self.weight=float(weight) if weight is not None else weight
        
        self.x=None
        self.y=None
        self.z=None


    def to_dictionary(self):
        aDictionary={}
        aDictionary['height']=self.height
        aDictionary['width']=self.width
        aDictionary['length']=self.length
        aDictionary['volume']=self.volume
        aDictionary['weight']=self.weight
        aDictionary['xCenter']=self.x
        aDictionary['yCenter']=self.y
        aDictionary['zCenter']=self.z
        return aDictionary
    
    def set_center(self, center):
        self.x, self.y, self.z=float(center[0]), float(center[1]), float(center[2])
    def to_string(self):
        return "<"+str(self.height)+","+str(self.width)+","+str(self.length)+","+str(self.volume)+","+str(self.weight)+","+str(self.x)+","+str(self.y)+","+str(self.z)+">"
# this is mostly due to not recognizing design failure earlier. binList and packageList don't allow ordering so we have this big mess of a method to make
# things more clear

# NOTE TO SELF: this makes the implicity assumption that the binList and packageList returned have the same order as minArrangment (although often smaller in size); think this is true but
# good place to start if some bugs show up
def convert_to_api_form(minArrangment, binList, packageList, parameterBins, parameterBoxes, costList,binWeightCapacitys,boxWeights,timedOut):
    binObjects=[]
    # initialize bins

    # dummy initilizations for bin params
    if costList==None:
        costList=[None for ele in range(0, len(parameterBins))]
    if binWeightCapacitys==None:
        binWeightCapacitys=[None for ele in range(0, len(parameterBins))]
    
    
    for count in range(0, len(parameterBins)):
        ### implicit in bin is idea that it is ranked consistently height=longest side, width=second longest side, length=shortest side
        #def __init__(self,id,height, width, length,cost, weightCapacity)
        newBin=BinAPI(count+1, parameterBins[count].height, parameterBins[count].width, parameterBins[count].depth,costList[count],binWeightCapacitys[count],timedOut)
        binObjects.append(newBin)
    

    
    # dummy initilization for box params
    if boxWeights==None:
        boxWeights=[None for ele in range(0, len(parameterBoxes))]    
    
    
    boxObjects=[]
    # initialize the boxes
    for count in range(0,len(parameterBoxes)):
       #def __init__(self,height, width, length,volume,weight):
        boxObjects.append(BoxAPI(parameterBoxes[count].height, parameterBoxes[count].width, parameterBoxes[count].depth, parameterBoxes[count].volume,boxWeights[count]))
    
    # binList
    # packageList
    currentBin=0
    for arrangment in minArrangment:
        # do stuff
        if(len(arrangment) is not 0):
            for boxIndex in arrangment:
                # add the box, add the coordinates with it
                binObjects[currentBin].add_box(boxObjects[boxIndex])
                # there is a bug if this fails
            try:
                # put the coordinates into their corresponding location with the box                    
                binObjects[currentBin].format_coordinates(packageList.pop(0))
            except Exception:
                print("Bug, contact Lucas")
                break
        currentBin+=1
                

    
    return binObjects

        



