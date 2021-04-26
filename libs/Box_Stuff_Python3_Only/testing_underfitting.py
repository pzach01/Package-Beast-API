
import copy
import math

def draw_bin(ax,bin_width, bin_height, bin_depth, bin_edge_color='black'):
    ax.plot3D([0,bin_width], [0,0], [0, 0], bin_edge_color)
    ax.plot3D([0, 0], [0,bin_height], [0, 0], bin_edge_color)
    ax.plot3D([0,0], [0,0], [0, bin_depth], bin_edge_color)

    ax.plot3D([0,bin_width], [bin_height,bin_height], [0, 0], bin_edge_color)
    ax.plot3D([0,bin_width], [0,0], [bin_depth, bin_depth], bin_edge_color)
    ax.plot3D([0,bin_width], [bin_height,bin_height], [bin_depth, bin_depth], bin_edge_color)

    ax.plot3D([bin_width, bin_width], [0,bin_height], [0, 0], bin_edge_color)
    ax.plot3D([0, 0], [0,bin_height], [bin_depth, bin_depth], bin_edge_color)
    ax.plot3D([bin_width, bin_width], [0,bin_height], [bin_depth, bin_depth], bin_edge_color)

    ax.plot3D([bin_width,bin_width], [0,0], [0, bin_depth], bin_edge_color)
    ax.plot3D([0,0], [bin_height,bin_height], [0, bin_depth], bin_edge_color)
    ax.plot3D([bin_width,bin_width], [bin_height,bin_height], [0, bin_depth], bin_edge_color)

    ax.set_xlim(0,max(bin_width, bin_height, bin_depth))
    ax.set_ylim(0,max(bin_width, bin_height, bin_depth))
    ax.set_zlim(0,max(bin_width, bin_height, bin_depth))

def draw_boxes(ax,x_vals, y_vals, z_vals, widths, heights, depths):

    colors = ['red', 'green', 'blue', 'yellow', 'purple']
    for i in range(len(x_vals)):
        ax.scatter(x_vals[i], y_vals[i], z_vals[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i], z_vals[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i], y_vals[i]+heights[i], z_vals[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i]+heights[i], z_vals[i], c=colors[i%len(colors)], marker='o')

        ax.scatter(x_vals[i], y_vals[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i], y_vals[i]+heights[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i]+heights[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')

        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i],y_vals[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i], x_vals[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]], [y_vals[i],y_vals[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])

        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i],y_vals[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])

        ax.plot3D([x_vals[i]+widths[i], x_vals[i]+widths[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i], x_vals[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i]+widths[i], x_vals[i]+widths[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])

        ax.plot3D([x_vals[i]+widths[i],x_vals[i]+widths[i]], [y_vals[i],y_vals[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i]+widths[i],x_vals[i]+widths[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])



# test for underfitting into a single container by
# generating difficult arrangments


# attempts to fill a container to max capacity with a random set of items, so that we have n items fitting into the container
# ideally this is decoupled from the box software
# obviously a ton of room to adjust the 'hardness' of the problem here by controlling n, range of boxes (nearly rectangular/square or both mixed together) 
# and distance from max volume


# generates arrangment that can be fit if algorithm is optimal. may be too hard or too easy

def generate_bins_that_fit(iterationLimit):
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
            
            
            interiorPoints, existingShape=try_to_expand_in_one_direction(currentItem, interiorPoints,directionToExpandIn, resolution)
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
    returnItemsRandomized=[]
    count=0
    while(len(returnItems)>0):
        itemToPop=random.randint(0,len(returnItems)-1)
        item=returnItems.pop(itemToPop)
        ordering=random.randint(0,5)
        #ordering=0
        newItem=None
        if ordering==0:
            newItem=ItemPY3DBP(item.name, item.xDim, item.yDim, item.zDim)
        if ordering==1:
            newItem=ItemPY3DBP(item.name, item.xDim, item.zDim, item.yDim)
        if ordering==2:
            newItem=ItemPY3DBP(item.name, item.yDim, item.xDim, item.zDim)
        if ordering==3:
            newItem=ItemPY3DBP(item.name, item.yDim, item.zDim, item.xDim)
        if ordering==4:
            newItem=ItemPY3DBP(item.name, item.zDim, item.xDim, item.yDim)
        if ordering==5:
            newItem=ItemPY3DBP(item.name, item.zDim, item.yDim, item.xDim)
        returnItemsRandomized.append(newItem)
    return container, returnItemsRandomized,coordinates
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


def test_one_underfit_api(ele):
    timeout=60
    batchTime=30
    numContainers=random.randint(1,10)
    container, items,coordinates=generate_bins_that_fit(numContainers)
    if len(items)==0:
        return 

    # one container as a list

    containers=[container.get_dimension_string()]
    items=[item.get_dimension_string() for item in items]
    ids=[ele for ele in range(0, len(items))]
    start=time.time()
    apiObjects, timedOut, arrangmentPossible=master_calculate_optimal_solution(containers,items,timeout,False,ids)
    end=time.time()
    if end-start<(timeout-5):
        print(end-start)
        assert(len(apiObjects[0].boxes)==len(items))
        assert(arrangmentPossible)
        assert(not timedOut)
        for objectIndex in range(0, len(apiObjects[0].boxes)):
            if not(objectIndex==0):
                lastObject=apiObjects[0].boxes[objectIndex-1]
                thisObject=apiObjects[0].boxes[objectIndex]
                if (lastObject.x+(lastObject.xDim/2))>(thisObject.x+(thisObject.xDim/2)):
                    if (lastObject.y+(lastObject.yDim/2))>(thisObject.y+(thisObject.yDim/2)):
                        if (lastObject.z+(lastObject.zDim/2))>(thisObject.z+(thisObject.zDim/2)):
                            raise Exception("unsorted objects for stepthrough function")
        test_for_double_fit_api_version(apiObjects,1000)
        test_for_outside_container_api(apiObjects)
    # cant assert optimality because generator could have run out
    elif (timeout-5)<(end-start)<(timeout):
        print("Lock recursion case"+str(end-start))

        assert(end-start>(timeout-5))
        test_for_double_fit_api_version(apiObjects,1000)
        test_for_outside_container_api(apiObjects)
    else:
        print("Strong case:"+str(end-start))

        assert(timedOut)

def test_one_underfit(ele):

    numContainers=random.randint(1,10)
    container, items,coordinates=generate_bins_that_fit(numContainers)


    container=ContainerPY3DBP('Container',container.xDim, container.yDim, container.zDim)
    packer=single_pack.single_pack(container, items,True, True,math.inf)
    assert(len(packer.items)==len(items))
    if not packer.isOptimal:
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
        return packer, container, items, coordinates
    else:
        test_for_double_fit(packer, 1000)
        for item in packer.items:
            if outside_container(item, container.xDim,container.yDim,container.zDim):
                raise Exception("rendered outside container")
        # what we did
        volumeOccupied=sum([item.volume for item in items])/container.volume
        # what py3dbp did
        volumeOccupied2=sum([item.volume for item in packer.items])/packer.container.volume
        assert(volumeOccupied==volumeOccupied2)
        assert(packer.unfit_items==[])
        #print("N: "+str(len(items)))
        #print("Occupacy percentage:"+str(volumeOccupied))
    return packer, container, items, coordinates
# note that we use this when we failure to render by PY3DBP, but have coordinates from test_one_underfit()
def render_something_that_failed(container, items,coordinates,rotationTypes):
    packer=Packer(rotationTypes)
    bin_width,bin_height,bin_depth=container.xDim,container.yDim,container.zDim
    newItems=[]
    import copy
    for key in coordinates.keys():


        newItem=ItemPY3DBP('',coordinates[key][0], coordinates[key][1], coordinates[key][2])
        # BUG: THIS MIGHT NOT BE UNIQUE
        # remember generate_bins_that_fit uses number of points in a cube, not the volume

        newItem.position=[key[0],key[1],key[2]]
        newItems.append(copy.deepcopy(newItem))
    packer.items=newItems


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_vals = []
    y_vals = []
    z_vals = []
    widths = []
    heights = []
    depths = []


    for item in packer.items:
        x_vals.append(float(item.position[0]))
        y_vals.append(float(item.position[1]))
        z_vals.append(float(item.position[2]))


        widths.append(float(item.get_dimension()[0]))
        heights.append(float(item.get_dimension()[1]))
        depths.append(float(item.get_dimension()[2]))





    draw_bin(ax,bin_width, bin_height, bin_depth)
    draw_boxes(ax,x_vals, y_vals, z_vals, widths, heights, depths)
    ax.set_xlabel('Width (x)')
    ax.set_ylabel('Height (y)')
    ax.set_zlabel('Depth (z)')

    plt.show() 
def test_underfits():
    specialContainer, specialItems=None,None
    failedAt1000Iterations=0
    for ele in range(0, 1000000):
        print(ele)

        packer=None
        packer, container, items, coordinates=test_one_underfit(ele)
        if ele==16841:
            print("Container: "+str(container.xDim)+'x'+str(container.yDim)+'x'+str(container.zDim))
            for item in items:
                print("Item: "+str(item.xDim)+'x'+str(item.yDim)+'x'+str(item.zDim))
#        try:
#            packer, container, items, coordinates=test_one_underfit(ele)
#        except Exception:
#            print('Failed')
#            break
#        render_something_that_failed(container, items, coordinates)
        if not packer.isOptimal:
            # can do this to recieve verification that you can fit it in 
            render_something_that_failed(container, items, coordinates)
            raise Exception

def test_underfits_api():
    for ele in range(0, 100000):
        print(ele)
        test_one_underfit_api(ele)




# try to fit items into a single (optimized) container when you are given multiple containers into 
def test_one_underfit_multipack(printStuff=True):
    import random

    timeout=30
    numItems=random.randint(1,15)

    container, items,coordinates=generate_bins_that_fit(numItems)


    numContainers=random.randint(1,15)
    containers=[container.get_dimension_string()]
    # only save container in this code
    for ele in range(0, numContainers):
        container, items,coordinates=generate_bins_that_fit(numItems)
        containers.append(container.get_dimension_string())

    random.shuffle(containers)
    if len(items)==0:
        return 

    # one container as a list

    items=[item.get_dimension_string() for item in items]
    ids=[ele for ele in range(0, len(items))]


    mostSpaceUsedWithSingleContainers=0
    import math
    leastContainerVolumeWithSingleContainers=math.inf
    for container in containers:
        apiObjects, timedOut, arrangmentPossible=master_calculate_optimal_solution([container],items,timeout,False,ids)
        # why is this here?
        if not arrangmentPossible:
            continue
        spaceUsed=sum([box.volume for box in apiObjects[0].boxes])
        containerVolume=apiObjects[0].volume
        # update best score
        if spaceUsed>mostSpaceUsedWithSingleContainers:
            mostSpaceUsedWithSingleContainers=spaceUsed
            leastContainerVolumeWithSingleContainers=containerVolume
        elif mostSpaceUsedWithSingleContainers==spaceUsed:
            if leastContainerVolumeWithSingleContainers>containerVolume:
                mostSpaceUsedWithSingleContainers=spaceUsed
                leastContainerVolumeWithSingleContainers=containerVolume

    mostSpaceUsedWithMultipleContainers=0
    leastContainerVolumeWithMultipleContainers=math.inf
    while(mostSpaceUsedWithSingleContainers>mostSpaceUsedWithMultipleContainers and leastContainerVolumeWithSingleContainers<leastContainerVolumeWithMultipleContainers):
        apiObjects, timedOut, arrangmentPossible=master_calculate_optimal_solution(containers,items,timeout,False,ids)
        if apiObjects==None:
            # too wierd to happen during regular behavior
            raise Exception('wierd stuff')
    
        nonEmptyContainers=[container for container in apiObjects if len(container.boxes)>0]
        assert(len(nonEmptyContainers)==1)
        mostSpaceUsedWithMultipleContainers=sum([box.volume for box in nonEmptyContainers[0].boxes])
        leastContainerVolumeWithMultipleContainers=nonEmptyContainers[0].volume
        timeout*=2
        # check that there isnt an unsorted stepthrough function
        for objectIndex in range(0, len(apiObjects[0].boxes)):
            if not(objectIndex==0):
                lastObject=apiObjects[0].boxes[objectIndex-1]
                thisObject=apiObjects[0].boxes[objectIndex]
                if (lastObject.x+(lastObject.xDim/2))>(thisObject.x+(thisObject.xDim/2)):
                    if (lastObject.y+(lastObject.yDim/2))>(thisObject.y+(thisObject.yDim/2)):
                        if (lastObject.z+(lastObject.zDim/2))>(thisObject.z+(thisObject.zDim/2)):
                            raise Exception("unsorted objects for stepthrough function")

    if printStuff:
        print('Method: single pack')
        print('   most space used: '+str(mostSpaceUsedWithSingleContainers))
        print('   least container volume:'+str(leastContainerVolumeWithSingleContainers))

        print('Method: multi pack')  
        print('   most space used: '+str(mostSpaceUsedWithMultipleContainers))
        print('   least container volume:'+str(leastContainerVolumeWithMultipleContainers)) 
    # we always double at the end (so this is the timeout that gave us the answer)
    print('Timeout :'+str(timeout/2))

def test_underfits_multipack():
    for ele in range(0, 100000):
        print(ele)
        test_one_underfit_multipack()

# test the sieve
def test_one_underfit_sieve(printStuff=True):
    import random

    timeout=30
    numItems=random.randint(1,15)

    container, items,coordinates=generate_bins_that_fit(numItems)


    numContainers=random.randint(1,15)
    containers=[container.get_dimension_string()]
    # only save container in this code
    for ele in range(0, numContainers):
        container, items,coordinates=generate_bins_that_fit(numItems)
        containers.append(container.get_dimension_string())

    random.shuffle(containers)
    if len(items)==0:
        return 

    # one container as a list

    items=[item.get_dimension_string() for item in items]
    ids=[ele for ele in range(0, len(items))]


    optimalLength=len(items)
    optimalContainers=[]
    for container in containers:
        apiObjects, timedOut, arrangmentPossible=master_calculate_optimal_solution([container],items,timeout,False,ids)
        # why is this here?
        if not arrangmentPossible:
            continue
        lengthFound=len(apiObjects[0].boxes)
        if lengthFound==optimalLength:
            optimalContainers.append(sorted([apiObjects[0].xDim,apiObjects[0].yDim,apiObjects[0].zDim]))
        


    keepGoing=True

    while(keepGoing):
        start=time.time()
        apiObjects, timedOut, arrangmentPossible=box_stuff2.sieve_containers(containers,items,timeout,False,ids)
        if apiObjects==None:
            # too wierd to happen during regular behavior
            raise Exception('wierd stuff')
        assert(arrangmentPossible)
        # check that containers are returned in same order as they were input (needed in shippments.serializer; but not strictly necessary everywhere else)
        for index in range(0,len(containers)):
            x,y,z=containers[index].split('x')[0],containers[index].split('x')[1],containers[index].split('x')[2]
            x,y,z=float(x),float(y),float(z)
            sortedInputList=sorted([x,y,z])
            sortedOutputList=sorted([apiObjects[index].xDim,apiObjects[index].yDim,apiObjects[index].zDim])
            assert(sortedInputList==sortedOutputList)


        # check for optimality
        tempContainers=[]
        for container in apiObjects:
            lengthFound=len(container.boxes)
            if lengthFound==optimalLength:
                tempContainers.append(sorted([container.xDim,container.yDim,container.zDim]))
        keepGoing=False
        for item in tempContainers:
            if item not in optimalContainers:
                keepGoing=True
        print(timeout)
        timeout*=2
        end=time.time()
        if timeout>2000:
            print("Failed test case")
            raise Exception('failed here')
        
    
    # we always double at the end (so this is the timeout that gave us the answer)
    for item in tempContainers:
        assert(item in optimalContainers)
    print('Successful timeout :'+str(end-start))


def test_underfits_sieve():
    for ele in range(0, 100000):
        print(ele)
        test_one_underfit_sieve()

'''
from . import testing_imports
from .testing_imports import *
#test_underfits_api()
#test_underfits()
#test_underfits_multipack()
#test_underfits_sieve()
'''