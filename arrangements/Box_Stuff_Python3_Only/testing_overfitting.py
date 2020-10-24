# tests related to the software's ability to 
# identify a case where it can't fit all the
# items into a container
from . import testing_imports
from .testing_imports import *
import math
from .box_stuff2 import master_calculate_optimal_solution
import time
def test_for_overfits_both_types_api():
    iterations=10000
    timeout=60
    for i in range(0, iterations):
        print(i)
        if i%2:
            container, items=generate_an_overfit_arrangment_type_a()
            containerList=[container.get_dimension_string()]
            itemList=[item.get_dimension_string() for item in items]
            assert(sum([item.volume for item in items])>container.volume)
            start=time.time()
            apiObjects,timedOut, arrangmentPossible=master_calculate_optimal_solution(containerList, itemList,timeout,False)
            end=time.time()
            # 1 second grace period for timeouts
            print(end-start)

            assert(end-start-1<timeout)
            assert(len(apiObjects[0].boxes)<len(itemList))

        else:
            container, items=generate_an_overfit_arrangment_type_b()
            containerList=[container.get_dimension_string()]
            itemList=[item.get_dimension_string() for item in items]
            start=time.time()
            apiObjects,timedOut,arrangmentPossible=master_calculate_optimal_solution(containerList, itemList,timeout,False)
            end=time.time()
            # 1 second grace period for timeouts
            print(end-start)

            assert(end-start-1<timeout)
            assert(len(apiObjects[0].boxes)<len(itemList))
def test_for_overfits_both_types():
    iterations=10000
    timeout=60
    for i in range(0, iterations):
        print(i)
        if i%2:
            container, items=generate_an_overfit_arrangment_type_a()
            assert(sum([item.volume for item in items])>container.volume)
            packer=single_pack.single_pack(container, items,False,False,timeout)
            assert(not packer.isOptimal)
        else:
            container, items=generate_an_overfit_arrangment_type_b()
            packer=single_pack.single_pack(container, items,False,False, timeout)
            assert(not packer.isOptimal)

# volume overfit
def test_for_overfits_type_a():
    iterations=10000
    timeout=60
    for i in range(0, iterations):
        print(i)
        container, items=generate_an_overfit_arrangment_type_a()
        assert(sum([item.volume for item in items])>container.volume)
        packer=single_pack.single_pack(container, items,False,False,timeout)
        assert(packer==None)
# length/width/height overfit
def test_for_overfits_type_b():
    iterations=10000
    timeout=60

    for i in range(0, iterations):
        print(i)
        container, items=generate_an_overfit_arrangment_type_b()
        packer=single_pack.single_pack(container, items,math.inf,False,False, timeout)
        assert(packer==None)




# volume safeguard must be off for this code to work; shows clear downside obviously
def generate_an_overfit_arrangment_type_a():
    maxItems=8
    container, items,coordinates=generate_bins_that_fit_2(maxItems-1)
    itemVolume=sum([item.volume for item in items])
    
    desiredObjectVolume=container.volume-itemVolume
    firstDim,secondDim=random.randint(1,10),random.randint(1,10)
    import math
    thirdDim=math.ceil(desiredObjectVolume/(firstDim*secondDim))+1
    dimensionalOrder=random.randint(0,5)
    if dimensionalOrder==0:
        items.append(ItemPY3DBP(str('itemCausingFailure'),firstDim,secondDim,thirdDim))
    if dimensionalOrder==1:
        items.append(ItemPY3DBP(str('itemCausingFailure'),firstDim, thirdDim,secondDim))
    if dimensionalOrder==2:
        items.append(ItemPY3DBP(str('itemCausingFailure'),secondDim,firstDim,thirdDim))
    if dimensionalOrder==3:
        items.append(ItemPY3DBP(str('itemCausingFailure'),secondDim,thirdDim,firstDim))
    if dimensionalOrder==4:
        items.append(ItemPY3DBP(str('itemCausingFailure'),thirdDim,secondDim,firstDim))
    if dimensionalOrder==5:
        items.append(ItemPY3DBP(str('itemCausingFailure'),thirdDim,firstDim,secondDim))
    return container, items

def generate_an_overfit_arrangment_type_b():
    maxItems=5
    container, items,coordinates=generate_bins_that_fit_2(maxItems-1)
    itemVolume=sum([item.volume for item in items])
    
    desiredObjectVolume=container.volume-itemVolume
    firstDim,secondDim=1,1
    import math
    thirdDim=max(max(container.xDim,container.yDim),container.zDim)+1
    dimensionalOrder=random.randint(0,5)
    if dimensionalOrder==0:
        items.append(ItemPY3DBP(str('itemCausingFailure'),firstDim,secondDim,thirdDim))
    if dimensionalOrder==1:
        items.append(ItemPY3DBP(str('itemCausingFailure'),firstDim, thirdDim,secondDim))
    if dimensionalOrder==2:
        items.append(ItemPY3DBP(str('itemCausingFailure'),secondDim,firstDim,thirdDim))
    if dimensionalOrder==3:
        items.append(ItemPY3DBP(str('itemCausingFailure'),secondDim,thirdDim,firstDim))
    if dimensionalOrder==4:
        items.append(ItemPY3DBP(str('itemCausingFailure'),thirdDim,secondDim,firstDim))
    if dimensionalOrder==5:
        items.append(ItemPY3DBP(str('itemCausingFailure'),thirdDim,firstDim,secondDim))
    return container, items


# confusingly, thees two methods don't correspond to type1 and type2, but are named differently 
# exact copy of other method, but copied to eliminate dependency
def generate_bins_that_fit_2(iterationLimit):
    # need not be so
    n=iterationLimit
    # each point is at least .1 away from o
    resolution=1
    containerX,containerY,containerZ=random.randint(1,25), random.randint(1,25),random.randint(1,25)
    
    interiorPoints=[]
    # can quickly exceed memory limit; increase resolution (size) if going over memory or approximate container to 
    # generate the interior points
    for xVal in range(0, int((containerX+1)/resolution)):
        for yVal in range(0, int((containerY+1)/resolution)):
            for zVal in range(0, int((containerZ+1)/resolution)):
                interiorPoints.append((xVal, yVal, zVal))
    # there are more points then the volume (consider the 1x1x1 example; has 8 points volume 1)
    assert(len(interiorPoints)==((containerX+1)*(containerY+1)*(containerZ+1)/(resolution**3)))
    # implicitly prioritzes x>y>z
    interiorPoints=sorted(interiorPoints)
    # a list of points, can easily be used to get the dimensions of a box but keep points to demonstrate test integrity
    items=[]
    coordinates={}
    for i in range(0, n):
        if(len(interiorPoints)==0):
            # full volume
            break
        # the list of positions occupied by one new item
        nextPositionToTryToAddTo=random.randint(0, len(interiorPoints)-1)

        point=interiorPoints[nextPositionToTryToAddTo]    
        interiorPoints.remove(point)

        currentItem=[point]
        repeatCount=0
        while(True):

            
            
            # can modify this to make problem less feasible
            directionToExpandIn=random.randint(0,2)
            up=random.randint(0,1)
            # if (not up) then look down, essentially subtract from the points the resolution instead of adding to it,
            #this should allow us to fill more space with fewer boxes, making the problem hard for a smaller n sooner (because of greater volume occupancy)
            resolution=resolution if up else -resolution
            
            
            interiorPoints, existingShape=try_to_expand_in_one_direction_2(currentItem, interiorPoints,directionToExpandIn, resolution)
            if sorted(existingShape)==sorted(currentItem):
                repeatCount+=1
            else:
                currentItem=existingShape                                
                repeatCount=0
            # this is super stupid and slow, replace with popping the dimensions that cant be changed logic
            if repeatCount==20:

                items.append(currentItem)

                break            

    container=ContainerPY3DBP('',containerX, containerY, containerZ)
    returnItems=[]
    count=0
    for item in items:
        count+=1

        item=sorted(item)
        minTuple=item[0]
        maxTuple=item[len(item)-1]
        # no points or lines allowed, only planes
        if(((not (minTuple[0] ==maxTuple[0])) and (not(minTuple[1]==maxTuple[1]))) and (not(minTuple[2]==maxTuple[2]))):
            # to see why this makes sense, consider that a 1x1x1 container has volume 1, but 8 points

            newItem=ItemPY3DBP(str(count), int(maxTuple[0]-minTuple[0]), int(maxTuple[1]-minTuple[1]), int(maxTuple[2]-minTuple[2]))
            coordinates[sorted(item)[0]]=(newItem.xDim, newItem.yDim, newItem.zDim)

            assert((newItem.zDim+1)*(newItem.yDim+1)*(newItem.xDim+1)==len(item))
            returnItems.append(newItem)
    return container, returnItems,coordinates
# key invariant, if we can't expand, just return the shapes with no modification
def try_to_expand_in_one_direction_2(existingShape, interiorPoints, directionToExpandIn, resolution):
    existingShape=sorted(existingShape)
    # this is a rectangle so this will always have the desired max value despite sorting maybe prioritizing other results
    maxValue=existingShape[len(existingShape)-1][directionToExpandIn]
    
    currentOutlier=[]
    for point in existingShape:
        if point[directionToExpandIn]==maxValue:
            currentOutlier.append(point)
            
    # this is just a zero tuple with resolution for use in the list comprehension 
    newPosition=[0,0,0]
    newPosition[directionToExpandIn]=resolution
    newPosition=tuple(newPosition)
    import operator
    
    pointsNeededToExpand=[(tuple(map(operator.add, point, newPosition))) for point in currentOutlier]
    clearedToExpand=True
    for newPointNeeded in pointsNeededToExpand:
        if newPointNeeded in interiorPoints:
            pass
        else:
            clearedToExpand=False
            break
    # return values unchanged
    if (not clearedToExpand):    
        return interiorPoints, existingShape
    # otherwise, change the lists by removing all points in pointsNeededToExpand from interiorPoints and placing them in existingShape
    for point in pointsNeededToExpand:
        interiorPoints.remove(point)
        existingShape.append(point)
    return interiorPoints, existingShape
test_for_overfits_both_types_api()
test_for_overfits_both_types()
