# test for underfitting into a single container by
# generating difficult arrangments


# attempts to fill a container to max capacity with a random set of items, so that we have n items fitting into the container
# ideally this is decoupled from the box software
# obviously a ton of room to adjust the 'hardness' of the problem here by controlling n, range of boxes (nearly rectangular/square or both mixed together) 
# and distance from max volume

import random
# makes test deterministic (reproducable)
random.seed(0)

import py3dbp_main
from py3dbp_main import Bin,Item
import single_pack
import single_pack_testing

# generates arrangment that can be fit if algorithm is optimal. may be too hard or too easy

def generate_bins_that_fit(iterationLimit):
    # need not be so
    n=iterationLimit
    # each point is at least .1 away from o
    resolution=1
    containerX,containerY,containerZ=20,20,20
    
    interiorPoints=[]
    # can quickly exceed memory limit; increase resolution (size) if going over memory or approximate container to 
    # generate the interior points
    for xVal in range(0, int(containerX/resolution)):
        for yVal in range(0, int(containerY/resolution)):
            for zVal in range(0, int(containerZ/resolution)):
                interiorPoints.append((xVal, yVal, zVal))
                
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
            
            
            interiorPoints, existingShape=try_to_expand_in_one_direction(currentItem, interiorPoints,directionToExpandIn, resolution)
            
            if sorted(existingShape)==sorted(currentItem):
                repeatCount+=1
            else:
                currentItem=existingShape                                
                repeatCount=0
            # this is super stupid and slow, replace with popping the dimensions that cant be changed logic
            if repeatCount==20:
                coordinates[point]=len(existingShape)
                break            
        items.append(currentItem)
    container=Bin('',containerX, containerY, containerZ,1000)
    returnItems=[]
    for item in items:
        item=sorted(item)
        minTuple=item[0]
        maxTuple=item[len(item)-1]
        # no points or lines allowed, only planes
        if(((not (minTuple[0] ==maxTuple[0])) and (not(minTuple[1]==maxTuple[1]))) and (not(minTuple[2]==maxTuple[2]))):
            
            newItem=Item('', int(maxTuple[0]-minTuple[0]+1), int(maxTuple[1]-minTuple[1]+1), int(maxTuple[2]-minTuple[2]+1), 1)
            assert(newItem.depth*newItem.height*newItem.width==len(item))
            returnItems.append(newItem)
    return container, returnItems,coordinates
# key invariant, if we can't expand, just return the shapes with no modification
def try_to_expand_in_one_direction(existingShape, interiorPoints, directionToExpandIn, resolution):
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



specialContainer, specialItems=None,None
failedAt1000Iterations=0
import copy
for ele in range(0, 1000):
    
    print(ele)
    container, items,coordinates=generate_bins_that_fit(10)
    print([item.string() for item in items])
    print(container.string())
    container=Bin('',container.width, container.height, container.depth,100)
    itemList=[Item('',item.width, item.height, item.depth, 1) for item in items]
    packer=single_pack.single_pack(container, itemList,1000)
    
    if packer==None:
        
        #packer=single_pack.single_pack(container, itemList,1000)        
        #specialContainer,specialItems=container,items
        #print("failed")
        # pseudopacker

        

            
        '''
            pointWidth=random.random()*container.width
            pointDepth=random.random()*container.height
            pointHeight=random.random()*container.depth    
        '''
        # failed
        break
    else:
        single_pack_testing.test_for_double_fit(packer, 10000)
        # what we did
        volumeOccupied=sum([item.volume for item in items])/container.volume
        # what py3dbp did
        volumeOccupied2=sum([item.volume for item in packer.items])/packer.bins[0].volume
        assert(volumeOccupied==volumeOccupied2)
        assert(packer.unfit_items==[])
        #print("N: "+str(len(items)))
        #print("Occupacy percentage:"+str(volumeOccupied))
        
        
print(failedAt1000Iterations/100)
#13
#3
#1


#2
#1
#1


#1
#11
#7