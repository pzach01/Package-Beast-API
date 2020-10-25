from __future__ import division
import os
from . import box_stuff1

from . import py3dbp_main
from .py3dbp_main import ItemPY3DBP, ContainerPY3DBP

import random
import copy
import math
import itertools
import time

def calculate_partion_list_size(binListSize, itemListSize):
    return math.factorial(binListSize+itemListSize-1)/(math.factorial(binListSize)*math.factorial(itemListSize-1))

def bruteforce_multibinpack(generator, binMasterList, boxMasterList,endTime,costList,binWeightCapacitys, boxWeights):
    import time
    timedOut=False
    minCost=float('inf')
    arrangment=None
    # list of packers that correspond to each container
    bestRenderingList=[None for ele in range(0, len(binMasterList))]
    while(True):
        try:
            if(time.time()>endTime):
                timedOut=True
                break
            combination=generator.get_next_arrangment()     
            tempRenderingList=[]
   
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
                        rendering=box_stuff1.binpack(boxes,bin,endTime-time.time())
                        tempRenderingList.append(rendering)
                        if (rendering==None):
                            
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
                    bestRenderingList=tempRenderingList
        except StopIteration:
            break
    return arrangment, minCost,timedOut,bestRenderingList
def bruteforce_singlepack(generator, binMasterList, boxMasterList,endTime,costList,binWeightCapacitys, boxWeights):
    import time
    import math
    assert(len(binMasterList)==1)
    assert(len(costList)==1)
    bin=binMasterList[0]
    rendering=box_stuff1.binpack(boxMasterList,bin,endTime-time.time(),saveNonOptimal=True)
    return None, costList[0] if len(rendering.bestItems)>0 else math.inf,len(rendering.bestItems)>0,[rendering]
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
    arrangments=[]
    for index in range(0, len(minArrangment)):
        bin=bins1[index]
        boxesUsed=[]
        for setIndex in minArrangment[index]:
            boxesUsed.append(boxs1[setIndex])
        
        boxArrangment=box_stuff1.binpack(boxesUsed, bin)
        arrangments.append(boxArrangment)  
        
    return arrangments
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
def fit_all(bins1, boxs1, timeout, itemIds=[], costList=None, binWeightCapacitys=None, boxWeights=None):
    import math
    minCost=math.inf
    minArrangment=None
    

    assert((binWeightCapacitys==None and boxWeights==None) or (binWeightCapacitys!=None and binWeightCapacitys!=None))
    volumeList=[]
    for ele in bins1:
        x,y,z=float(ele.split('x')[0]),float(ele.split('x')[1]),float(ele.split('x')[2])
        volume=x*y*z
        volumeList.append(volume)
    if(costList==None):
        costList=volumeList
        # use volume

    # end replication of bruteforce code
    indexUsed=None
    anyArrangmentPossible=False
    bestScore=0
    optimalScore=sum([item for item in volumeList])
    for ele in range(0, len(bins1)):
        try:
            if(costList[ele]<minCost or(not bestScore ==optimalScore)):
                # cant subscript none so must use lambda
                miniCostList=None if costList==None else [costList[ele]]
                miniBinWeightCapacitys=None if binWeightCapacitys==None else [binWeightCapacitys[ele]]
                # call master_calculate_optimal_solution with just one bin
                numRemaining=(len(bins1))-ele
                start=time.time()
                apiFormat,timedOut,arrangmentPossible=master_calculate_optimal_solution([bins1[ele]], boxs1,(timeout/numRemaining),True,itemIds, miniCostList, miniBinWeightCapacitys, boxWeights)
                end=time.time()
                timeout-=(end-start)
                if arrangmentPossible:
                    score=sum([box.volume for box in apiFormat[0].boxes])
                    if ((score>=bestScore) or (score==bestScore and costList[ele]<minCost)):
                        bestScore=score
                        anyArrangmentPossible=True
                        # no error, update to better solution
                        if not(timedOut) and arrangmentPossible:
                            minArrangment=apiFormat
                            minCost=costList[ele]
                            indexUsed=ele
                    
        # ran out of time
        except TimeoutError:
            pass
        # no solution, look for next bin
        except NotImplementedError:
            pass
    # we have to jankily reformat the API to add a bunch of empty containers
    containersUsed=[]
    if indexUsed==None:
        # no arrangment, timedout, unable to decide if arrangment is possible
        return None, True, anyArrangmentPossible
    else:
        for ele in range(0, len(bins1)):
            if ele==indexUsed:
                assert(len(minArrangment)==1)
                # update the arrangment id so that it is placed in the right place
                minArrangment[0].id=ele
                containersUsed.append(minArrangment[0])
            else:
                x,y,z=float(bins1[ele].split('x')[0]),float(bins1[ele].split('x')[1]),float(bins1[ele].split('x')[2])
                containersUsed.append(BinAPI(ele,x,y,z,costList[ele],0,False))
    return containersUsed,False,True

# wrapper for the ItemPY3DBP class
def string_wrapper_for_item_class(itemString):
    l,w,h=float(itemString.split('x')[0]),float(itemString.split('x')[1]),float(itemString.split('x')[2])
    return ItemPY3DBP('',l,w,h)
def string_wrapper_for_container_class(itemString):
    l,w,h=float(itemString.split('x')[0]),float(itemString.split('x')[1]),float(itemString.split('x')[2])
    return ContainerPY3DBP('',l,w,h)
# bin weights must be in same order, same for box weights
def master_calculate_optimal_solution(bins1, boxs1,timeout=60,multibinpack=True,itemsIds=[],costList=None,binWeightCapacitys=None, boxWeights=None):
    # metaparameter, expose to API at some point
    if len(boxs1)==0:
        raise Exception("cant try with no items")
    if not multibinpack:
        return fit_all(bins1, boxs1, timeout,itemsIds, costList, binWeightCapacitys, boxWeights)


    
    
    import math
    import time
    
    partitionListSize=calculate_partion_list_size(len(bins1), len(boxs1))
    # half a billion
    maxMemorySize=500000000
    if(partitionListSize > maxMemorySize):
        return None, False, None
    
    # if we reach this time trigger a timeout error
    
    # string intiliaztion
    boxs1=[string_wrapper_for_item_class(box) for box in boxs1]
    # initialize the itemIds
    for idIndex in range(0, len(itemsIds)):
        boxs1[idIndex].name=itemsIds[idIndex]
    bins1=[string_wrapper_for_container_class(bin) for bin in bins1] 
    
    assert((binWeightCapacitys==None and boxWeights==None) or (binWeightCapacitys!=None and binWeightCapacitys!=None))

    
    # minimize volume if there is no cost list, otherwise use dollar
    if(costList==None):
        costList=[bin.volume for bin in bins1]
    
 
    # this cant timeout because its contribution to time should be minimal
    generator=box_stuff1.OptimizeBoxesGenerator(bins1,boxs1,costList)


    
    ## find the index arrangment of the cheapest combination (actual computation)
    if len(bins1)>1:
        minArrangment, minCost,timedOut,renderingList=bruteforce_multibinpack(generator,bins1, boxs1,time.time()+timeout,costList,binWeightCapacitys,boxWeights)
    else:
        minArrangment, minCost,timedOut,renderingList=bruteforce_singlepack(generator,bins1, boxs1,time.time()+timeout,costList,binWeightCapacitys,boxWeights)

    if(minCost==float('inf')):
        return None, timedOut, max(costList)>generator.cheapestPossible

    
    
    ### min arrangment is merely indexes, still need the actual packages in there
    
    ### these should be equal in length

    # this is duplicate work; actually could be computationally intensive too
    # OLD OLD OLD OLD 
    #arrangments=get_xyz_of_optimal_solution(minArrangment, bins1, boxs1,endTimeRendering)
    
    #return binList,packageList
    
    # new stuff, last two things are only for debugging if necessary
    apiFormat=convert_to_api_form(renderingList,costList, binWeightCapacitys, timedOut)

    # sort by maxTuple 
    for container in apiFormat:
        container.boxes=sorted(container.boxes, key= lambda box:(box.x+(box.xDim/2),box.y+(box.yDim/2),box.z+(box.zDim/2)))
    return apiFormat,False, True


class BinAPI():
    def to_string(self):
        binAttributes="("+str(self.id)+","+str(self.xDim)+","+str(self.yDim)+","+str(self.zDim)+","+str(self.volume)+","+str(self.cost)+","+str(self.weightCapacity)+","+str(self.timedOut)
        boxAttributes=""
        for box in self.boxes:
            boxAttributes+=box.to_string()
        # end of the string
        boxAttributes+=")"
        return binAttributes+boxAttributes
    
    def to_dictionary(self):
        aDictionary={}
        aDictionary['id']=self.id
        aDictionary['xDim']=self.xDim
        aDictionary['yDim']=self.yDim
        aDictionary['zDim']=self.zDim
        aDictionary['volume']=self.volume
        aDictionary['cost']=self.cost
        aDictionary['weightCapacity']=self.weightCapacity
        # this is basically just a fancy for loop
        aDictionary['timedOut']=self.timedOut
        aDictionary['itemList']=[box.to_dictionary() for box in self.boxes]
        return aDictionary
    def __init__(self,id,xDim,yDim, zDim,cost, weightCapacity,timedOut):
        self.id=id
        
        self.xDim=float(xDim)
        self.yDim=float(yDim)     
        self.zDim=float(zDim)
        self.volume=float(xDim*yDim*zDim)
        
        
        self.cost=float(cost)
        self.weightCapacity=float(weightCapacity) if (weightCapacity is not None) else weightCapacity
        self.timedOut=timedOut
        self.boxes=[]
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
            xDim, yDim, zDim,weight=package.xDim, package.yDim, package.zDim,package.weight
            if package.weight==None:
                weight=0
            for boxIndex in range(0, len(self.boxes)):
                # boxes have the same coordinates
                
                # we have to do this because internally the HxLxD might get swapped around by the algorithm
                if (sorted([self.boxes[boxIndex].xDim,self.boxes[boxIndex].yDim,self.boxes[boxIndex].zDim])==sorted([xDim,yDim,zDim])):
                    self.boxes[boxIndex].set_center(key)
                    self.boxes[boxIndex].xDim=xDim
                    self.boxes[boxIndex].yDim=yDim
                    self.boxes[boxIndex].zDim=zDim
                    self.boxes[boxIndex].weight=weight
                    slotted.append(self.boxes.pop(boxIndex))
                    break
                
        self.boxes=slotted


class BoxAPI():
    def __init__(self,id, xDim, yDim, zDim,volume,weight):
        self.id=id
        self.xDim=float(xDim)
        self.yDim=float(yDim)

        self.zDim=float(zDim)
        self.volume=float(volume)
        self.weight=float(weight) if weight is not None else weight
        
        self.x=None
        self.y=None
        self.z=None


    def to_dictionary(self):
        aDictionary={}
        aDictionary['xDim']=self.xDim
        aDictionary['yDim']=self.yDim

        aDictionary['zDun']=self.zDun
        aDictionary['volume']=self.volume
        aDictionary['weight']=self.weight
        aDictionary['xCenter']=self.x
        aDictionary['yCenter']=self.y
        aDictionary['zCenter']=self.z
        return aDictionary
    
    def set_center(self, center):
        self.x, self.y, self.z=float(center[0]), float(center[1]), float(center[2])
    def to_string(self):
        return "<"+str(self.xDim)+","+str(self.yDim)+","+str(self.zDim)+","+str(self.volume)+","+str(self.weight)+","+str(self.x)+","+str(self.y)+","+str(self.z)+">"
# this is mostly due to not recognizing design failure earlier. binList and packageList don't allow ordering so we have this big mess of a method to make
# things more clear

# NOTE TO SELF: this makes the implicity assumption that the binList and packageList returned have the same order as minArrangment (although often smaller in size); think this is true but
# good place to start if some bugs show up
def convert_to_api_form(arrangments,costList, binWeightCapacitys,timedOut):
    
        # dummy initilizations for bin params
    if costList==None:
        costList=[None for ele in range(0, len(arrangments))]
    if binWeightCapacitys==None:
        binWeightCapacitys=[None for ele in range(0, len(arrangments))]
    
    containerObjects=[]


    for containerIndex in range(0, len(arrangments)):
        newContainer=BinAPI(containerIndex,arrangments[containerIndex].container.xDim,arrangments[containerIndex].container.yDim, arrangments[containerIndex].container.zDim,0,0,timedOut)
        containerObjects.append(newContainer)

    for containerIndex in range(0, len(arrangments)):
        for item in arrangments[containerIndex].bestItems:
            x,y,z=item.position[0]+(item.get_dimension()[0]/2), item.position[1]+(item.get_dimension()[1]/2), item.position[2]+(item.get_dimension()[2]/2)
            # weight unitilized here
            newBox=BoxAPI(item.name, item.xDim,item.yDim,item.zDim, item.volume,0)
            newBox.set_center((x,y,z))
            (containerObjects[containerIndex]).add_box(newBox)



    '''
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
                # put the coordinates into their corresponding location with the box  
                
                binObjects[currentBin].format_coordinates(packageList.pop(0))
        currentBin+=1
                
    '''
    
    return containerObjects

        






