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

# run a global check that is it at least maybe possible to fit a box into a container before we start packing
def get_possible_to_fit_one_box(bins1,boxs1):
    possibleToFitOneBox=False
    # run a global check that you can fit at least one box
    for box in boxs1:
        xBox,yBox,zBox=float(box.split('x')[0]),float(box.split('x')[1]),float(box.split('x')[2])
        boxList=sorted([xBox,yBox,zBox])
        for container in bins1:
            xContainer,yContainer,zContainer=float(container.split('x')[0]),float(container.split('x')[1]),float(container.split('x')[2])
            containerList=sorted([xContainer,yContainer,zContainer])
            couldFit=True
            for index in range(0, 3):
                if containerList[index]<boxList[index]:
                    couldFit=False
                    break

            if couldFit:
                possibleToFitOneBox=True
                break
    return possibleToFitOneBox


def lock_recursion_and_increase_timeout(container,packer,timeout, testMode):
    if timeout<5:
        raise Exception("unsupported behavior in timeout structure")
    from .py3dbp_main import Packer
    from .py3dbp_constants import Axis, RotationType
    from .single_pack import DimensionalMixupsGenerator,get_best_packer
    import time

    # how is this tested? very important question?
    # initial thoughts: turn all other pack methods timeout to 0 and ensure it stil gets what we think
    # cant have size 0 bestItems and optimal packer
    if (((not(packer.isOptimal)) and (not(len(packer.bestItems)==0)) or testMode) and (len(packer.items)+len(packer.unfit_items)>1)): 
        endTime=time.time()+timeout

        # get the packer that yields the best arrangment seen so far

        initialPacker=Packer(packer.rotationTypes,5)
        initialPacker.container=packer.container
        initialPacker.items=packer.bestItems

        allPivots=set()
        for item in initialPacker.items:
            for pivotPoint in Axis.ALL:
                firstValue,secondValue,thirdValue=pivotPoint[0],pivotPoint[1],pivotPoint[2]
                newPivot=(item.position[0]+firstValue*item.xDim,item.position[1]+secondValue*item.yDim,item.position[2]+thirdValue*item.zDim)
                allPivots.add(newPivot)
        trueUnfits=(packer.items+packer.unfit_items)[len(packer.bestItems):]
        generator=DimensionalMixupsGenerator(trueUnfits)
        while(True):
            try:
                if time.time()>endTime:
                    break
                if testMode:

                    #generator.count=random.ranndint(0, 6**len(trueUnfits)-1)
                    print("Generator: "+str(generator.count))

                newPacker=copy.deepcopy(initialPacker)


                newPacker.unfit_items=generator.next()
                # run the start of pack without self.try_to_place_item
                # actually just make this its own method and call it before calling pack (initialize item hierarchy)
                newPacker.initialize_object_hierarchy()
                # regular code will pass down the object hierarchy here
                newPacker.unfit_items[0].pivotSets[0]=allPivots
                # will have to make some the start of packer.pack() optional (and turn off here but true by default)
                newPacker.rotationTypes=RotationType.ALL
                newPacker.packFromBeginning=False
                newPacker.isOptimal=False
                newPacker.bestItems=[]
                newPacker.bestDepth=0
                newPacker.timeout=time.time()+1
                
                newPacker.pack()
                packer=get_best_packer(packer,newPacker)

                if newPacker.isOptimal:
                    break
                if testMode:    
                    break

            except StopIteration:
                break
            except TimeoutError:
                packer=get_best_packer(packer,newPacker)
                if testMode:
                    break
                pass



    container.boxes=[]
    for item in packer.bestItems:
        x,y,z=item.position[0]+(item.get_dimension()[0]/2), item.position[1]+(item.get_dimension()[1]/2), item.position[2]+(item.get_dimension()[2]/2)
        # weight unitilized here
        newBox=BoxAPI(item.name, item.xDim,item.yDim,item.zDim, item.volume,0)
        newBox.set_center((x,y,z))
        container.add_box(newBox)
    container.boxes=sorted(container.boxes, key= lambda box:(box.x+(box.xDim/2),box.y+(box.yDim/2),box.z+(box.zDim/2)))
    return container
    '''
    for containerIndex in range(0, len(arrangments)):
        for item in arrangments[containerIndex].bestItems:
            x,y,z=item.position[0]+(item.get_dimension()[0]/2), item.position[1]+(item.get_dimension()[1]/2), item.position[2]+(item.get_dimension()[2]/2)
            # weight unitilized here
            newBox=BoxAPI(item.name, item.xDim,item.yDim,item.zDim, item.volume,0)
            newBox.set_center((x,y,z))
            (containerObjects[containerIndex]).add_box(newBox)


    for container in apiFormat:
        container.boxes=sorted(container.boxes, key= lambda box:(box.x+(box.xDim/2),box.y+(box.yDim/2),box.z+(box.zDim/2)))

    return container
    ''' 
def truncate_to_nth_decimal_point(number, n):
    number=str(number)
    if '.' not in number:
        return float(number)
    beforeDecimal,afterDecimal=number.split('.')[0],number.split('.')[1]
    newNumber=beforeDecimal+'.'+afterDecimal[0:min(n,len(afterDecimal))]
    return float(newNumber)

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
    if endTime<time.time():
        raise Exception("unsupported value in timeout field")
    import math
    assert(len(binMasterList)==1)
    assert(len(costList)==1)
    bin=binMasterList[0]
    rendering=box_stuff1.binpack(boxMasterList,bin,endTime-time.time(),saveNonOptimal=True)
    return None, costList[0] if len(rendering.bestItems)>0 else math.inf,endTime-time.time()<0,[rendering]
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


def get_indices_remaining(startingIndex,bins,costList, minCost,bestScore,optimalScore,disqualifyTooLight,volumeList):
    # sometimes starting index is non-zero to reflect ignoring already searched bins
    indicesRemaining=[index for index in range(startingIndex, len(bins))]
    # get containers that could (be cheaper and yield same or better score) or (if not optimal yet yield a better score)
    indicesRemaining=[index for index in indicesRemaining if ((costList[index]<minCost and volumeList[index]>=bestScore) or  (not bestScore==optimalScore and volumeList[index]>bestScore))]

    # if on the last rotation only use containers that can produce optimal score
    if (disqualifyTooLight):
        indicesRemaining=[index for index in indicesRemaining if volumeList[index]>=optimalScore]
    return indicesRemaining
# return indices which could possibly fit everything
def get_possibly_optimal_indices_remaining(startingIndex,bins,items,optimalScore,volumeList):
    # sometimes starting index is non-zero to reflect ignoring already searched bins
    indicesRemaining=[index for index in range(startingIndex, len(bins))]

    indicesRemaining=[index for index in indicesRemaining if volumeList[index]>=optimalScore]
    
    indicesMinusBinsThatCantFitLargeItems=[]
    for index in indicesRemaining:
        container=bins[index]
        xContainer,yContainer,zContainer=float(container.split('x')[0]),float(container.split('x')[1]),float(container.split('x')[2])
        containerList=sorted([xContainer,yContainer,zContainer])

        couldFit=True
        for item in items:
            xItem,yItem,zItem=float(item.split('x')[0]),float(item.split('x')[1]),float(item.split('x')[2])
            itemList=sorted([xItem,yItem,zItem])
            for thing in range(0, 3):
                if containerList[thing]<itemList[thing]:
                    couldFit=False
                    break
        if couldFit:
            indicesMinusBinsThatCantFitLargeItems.append(index)
    return indicesMinusBinsThatCantFitLargeItems


def get_possible_to_fit_all_items(bins1, boxs1):
    anyFit=False
    epsilon=.01
    for container in bins1:
        xContainer,yContainer,zContainer=float(container.split('x')[0]),float(container.split('x')[1]),float(container.split('x')[2])
        containerList=sorted([xContainer,yContainer,zContainer])

        containerVolume=(xContainer*yContainer*zContainer)

        couldFit=True
        
        boxesVolume=0
        for box in boxs1:
            xBox,yBox,zBox=float(box.split('x')[0]),float(box.split('x')[1]),float(box.split('x')[2])
            boxesVolume+=(xBox*yBox*zBox)
            boxList=sorted([xBox,yBox,zBox])

            for index in range(0, 3):
                if containerList[index]<boxList[index]:
                    couldFit=False
                    break
        if (containerVolume+epsilon<boxesVolume):
            couldFit=False
        if couldFit:
            anyFit=True
            break
    return anyFit
# ripoff of fit_all but returns multiple containers

def fit_all_sieve(bins1, boxs1, timeout, itemIds=[], costList=None, binWeightCapacitys=None, boxWeights=None):
    possibleToFitAllItemsAPriori=get_possible_to_fit_all_items(bins1,boxs1)
    if not possibleToFitAllItemsAPriori:
        return None, False, False,False
                   
    import math



    assert((binWeightCapacitys==None and boxWeights==None) or (binWeightCapacitys!=None and binWeightCapacitys!=None))
    volumeList=[]
    for ele in bins1:
        x,y,z=float(ele.split('x')[0]),float(ele.split('x')[1]),float(ele.split('x')[2])
        volume=x*y*z
        volumeList.append(truncate_to_nth_decimal_point(volume,3))
    if(costList==None):
        costList=volumeList
        # use volume

    # end replication of bruteforce code
    indicesUsed={}
    anyTimeout=False

    optimalScore=0
    for ele in boxs1:
        x,y,z=float(ele.split('x')[0]),float(ele.split('x')[1]),float(ele.split('x')[2])
        volume=x*y*z
        optimalScore+=volume
    # so that it matches up at 3rd decimal point        
    optimalScore=truncate_to_nth_decimal_point(optimalScore,3)

    # possible bugs could result from differences in truncation for different fields in the code

    numRotations=3
    # timeout allocation fractions for each rotation:
    # f(1)=[1]
    # f(2)=[1/3, 1]; first gets 1/3 of time remaining, 2nd gets all of time remaining
    # f(3)=[1/7,1/3, 1]; first gets 1/7 of time remaining, 2nd gets 1/3 of time remaining, last gets all remaining time
    # ...

    # f(n)=[1] if x==1 else [1/((2**n)-1)]+f(n-1)
    timeProfilesLambda=lambda x: [1] if x==1 else [1/((2**x)-1)]+timeProfilesLambda(x-1)
    timeProfiles=timeProfilesLambda(numRotations)
    noMoreRotations=False



    for rotation in range(0, numRotations):

        numRemainingInitial=len(get_possibly_optimal_indices_remaining(0,bins1,boxs1,optimalScore,volumeList))
        # override using multiple rotations and try to pack everything in one container in first pass
        if numRemainingInitial==1:
            fractionToUseForThisRotation=1
            noMoreRotations=True
        else:
            fractionToUseForThisRotation=timeProfiles[rotation]
        timeForThisRotation=timeout*fractionToUseForThisRotation
        start=time.time()

        for ele in range(0, len(bins1)):
            indicesRemaining=get_possibly_optimal_indices_remaining(ele,bins1,boxs1,optimalScore,volumeList)


            numRemaining=len(indicesRemaining)
            # override case where there is exactly one item remaining

            # we use this non-verbose form to avoid repeating ourselves (chiefly the condition(s) above)
            if (ele in indicesRemaining) and (ele not in indicesUsed.keys()):
                # sanity check
                assert(indicesRemaining[0]==ele)
                # cant subscript none so must use lambda
                miniCostList=None if costList==None else [costList[ele]]
                miniBinWeightCapacitys=None if binWeightCapacitys==None else [binWeightCapacitys[ele]]

                innerStart=time.time()
                apiFormat,timedOut,arrangmentPossible,renderingList=master_calculate_optimal_solution([bins1[ele]], boxs1,(timeForThisRotation/numRemaining),True,itemIds, miniCostList, miniBinWeightCapacitys, boxWeights,True)
                innerEnd=time.time()
                timeForThisRotation-=(innerEnd-innerStart)
                anyTimeout=True if (timedOut or anyTimeout) else False

                if arrangmentPossible:
                    # 3rd decimal point
                    score=truncate_to_nth_decimal_point(sum([box.volume for box in apiFormat[0].boxes]),3)
                    if score==optimalScore:
                        # no error, update to better solution
                        indicesUsed[ele]=apiFormat

                        

        end=time.time()
        timeout-=(end-start)
        if noMoreRotations:
            break
    # we have to jankily reformat the API to add a bunch of empty containers
    containersUsed=[]
    if len(indicesUsed.keys())==0:
        # no arrangment, timedout, unable to decide if arrangment is possible

        return None, anyTimeout, True, False
    else:
        for ele in range(0, len(bins1)):
            if ele in indicesUsed.keys():
                minArrangment=indicesUsed[ele]
                assert(len(minArrangment)==1)
                # update the arrangment id so that it is placed in the right place
                container=minArrangment[0]
                container.id=ele
                containersUsed.append(container)
    return containersUsed,anyTimeout,True,True




# attempt to fill all boxes in one of the bins
# Note to self: the backend code actually uses the API here 
def fit_all(bins1, boxs1, timeout, itemIds=[], costList=None, binWeightCapacitys=None, boxWeights=None):
    possibleToFitOneBox=get_possible_to_fit_one_box(bins1,boxs1)
    if not possibleToFitOneBox:
        return None, False, False
                   
    import math
    minCost=math.inf
    minArrangment=None
    minPacker=None

    timeSpentAtEndPacking=5
    timeout-=timeSpentAtEndPacking

    assert((binWeightCapacitys==None and boxWeights==None) or (binWeightCapacitys!=None and binWeightCapacitys!=None))
    volumeList=[]
    for ele in bins1:
        x,y,z=float(ele.split('x')[0]),float(ele.split('x')[1]),float(ele.split('x')[2])
        volume=x*y*z
        volumeList.append(truncate_to_nth_decimal_point(volume,3))
    if(costList==None):
        costList=volumeList
        # use volume

    # end replication of bruteforce code
    indexUsed=None
    anyTimeout=False
    bestScore=0

    optimalScore=0
    for ele in boxs1:
        x,y,z=float(ele.split('x')[0]),float(ele.split('x')[1]),float(ele.split('x')[2])
        volume=x*y*z
        optimalScore+=volume
    # so that it matches up at 3rd decimal point        
    optimalScore=truncate_to_nth_decimal_point(optimalScore,3)

    # possible bugs could result from differences in truncation for different fields in the code

    numRotations=3
    # timeout allocation fractions for each rotation:
    # f(1)=[1]
    # f(2)=[1/3, 1]; first gets 1/3 of time remaining, 2nd gets all of time remaining
    # f(3)=[1/7,1/3, 1]; first gets 1/7 of time remaining, 2nd gets 1/3 of time remaining, last gets all remaining time
    # ...

    # f(n)=[1] if x==1 else [1/((2**n)-1)]+f(n-1)
    timeProfilesLambda=lambda x: [1] if x==1 else [1/((2**x)-1)]+timeProfilesLambda(x-1)
    timeProfiles=timeProfilesLambda(numRotations)
    noMoreRotations=False



    disqualifyTooLight=False
    for rotation in range(0, numRotations):
        # lot going on in this line
        if rotation==(numRotations-1):
            disqualifyTooLight=True
        indicesRemainingInitial=get_indices_remaining(0,bins1,costList, minCost,bestScore,optimalScore,disqualifyTooLight,volumeList)
        numRemainingInitial=len(indicesRemainingInitial)

        # redo if disqualifying containers that are too light leads to not searching for the full time
        if disqualifyTooLight and numRemainingInitial==0:
            disqualifyTooLight=False
            indicesRemainingInitial=get_indices_remaining(0,bins1,costList, minCost,bestScore,optimalScore,disqualifyTooLight,volumeList)
            numRemainingInitial=len(indicesRemainingInitial)
        # override using multiple rotations and try to pack everything in one container in first pass
        if numRemainingInitial==1:
            fractionToUseForThisRotation=1
            noMoreRotations=True
        else:
            fractionToUseForThisRotation=timeProfiles[rotation]
        timeForThisRotation=timeout*fractionToUseForThisRotation
        start=time.time()

        for ele in range(0, len(bins1)):
            try:
                indicesRemaining=get_indices_remaining(ele,bins1,costList, minCost,bestScore,optimalScore,disqualifyTooLight,volumeList)


                numRemaining=len(indicesRemaining)
                # override case where there is exactly one item remaining

                # we use this non-verbose form to avoid repeating ourselves (chiefly the condition(s) above)
                if ele in indicesRemaining:
                    # sanity check
                    assert(indicesRemaining[0]==ele)
                    # cant subscript none so must use lambda
                    miniCostList=None if costList==None else [costList[ele]]
                    miniBinWeightCapacitys=None if binWeightCapacitys==None else [binWeightCapacitys[ele]]

                    innerStart=time.time()
                    apiFormat,timedOut,arrangmentPossible,renderingList=master_calculate_optimal_solution([bins1[ele]], boxs1,(timeForThisRotation/numRemaining),True,itemIds, miniCostList, miniBinWeightCapacitys, boxWeights,True)
                    innerEnd=time.time()
                    timeForThisRotation-=(innerEnd-innerStart)
                    anyTimeout=True if (timedOut or anyTimeout) else False

                    if arrangmentPossible:
                        # 3rd decimal point
                        score=truncate_to_nth_decimal_point(sum([box.volume for box in apiFormat[0].boxes]),3)

                        # this line is still necessary because of the partial results return
                        if ((score>bestScore) or (score==bestScore and costList[ele]<minCost)):
                            bestScore=score
                            # no error, update to better solution
                            minArrangment=apiFormat
                            minPacker=renderingList[0]
                            minCost=costList[ele]
                            indexUsed=ele
                        
            # ran out of time
            except TimeoutError:
                pass
            # no solution, look for next bin
            except NotImplementedError:
                pass
        end=time.time()
        timeout-=(end-start)
        if noMoreRotations:
            break
    # we have to jankily reformat the API to add a bunch of empty containers
    containersUsed=[]
    if indexUsed==None:
        # no arrangment, timedout, unable to decide if arrangment is possible

        return None, anyTimeout, False
    else:
        for ele in range(0, len(bins1)):
            if ele==indexUsed:
                assert(len(minArrangment)==1)
                # update the arrangment id so that it is placed in the right place
                container=minArrangment[0]
                container.id=ele
                # change minArrangment[0] to have the boxes of the packer and then resort
                lockRecursion=True

                testMode=False
                if testMode:
                    minPacker.bestItems=minPacker.bestItems[:max(1,(len(minPacker.bestItems)-random.randint(1,5)))]
                tightenedContainer=lock_recursion_and_increase_timeout(container,minPacker,timeSpentAtEndPacking,testMode) if lockRecursion else container
                containersUsed.append(tightenedContainer)
            else:
                x,y,z=float(bins1[ele].split('x')[0]),float(bins1[ele].split('x')[1]),float(bins1[ele].split('x')[2])
                containersUsed.append(BinAPI(ele,x,y,z,costList[ele],0,False))
    return containersUsed,anyTimeout,True

# wrapper for the ItemPY3DBP class
def string_wrapper_for_item_class(itemString):
    l,w,h=float(itemString.split('x')[0]),float(itemString.split('x')[1]),float(itemString.split('x')[2])
    return ItemPY3DBP('',l,w,h)
def string_wrapper_for_container_class(itemString):
    l,w,h=float(itemString.split('x')[0]),float(itemString.split('x')[1]),float(itemString.split('x')[2])
    return ContainerPY3DBP('',l,w,h)

def sieve_containers(bins1, boxs1,timeout=60,multibinpack=True,itemsIds=[],costList=None,binWeightCapacitys=None, boxWeights=None,returnRenderingList=False):
    if len(boxs1)==0:
        raise Exception("cant try with no items")
    assert(not multibinpack)
    return fit_all_sieve(bins1, boxs1, timeout,itemsIds, costList, binWeightCapacitys, boxWeights)

# bin weights must be in same order, same for box weights
def master_calculate_optimal_solution(bins1, boxs1,timeout=60,multibinpack=True,itemsIds=[],costList=None,binWeightCapacitys=None, boxWeights=None,returnRenderingList=False):
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
        return None, False, False
    
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
        if returnRenderingList:
            return None, timedOut, False,[]
        else:
            return None, timedOut, False

    
    
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

    if returnRenderingList:
        return apiFormat,timedOut, True,renderingList
    else:
        return apiFormat,timedOut,True


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

        






