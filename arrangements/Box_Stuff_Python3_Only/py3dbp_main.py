from . import py3dbp_constants
from .py3dbp_constants import RotationType,Axis
from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import intersect_lucas,outside_container
import copy
import time

START_POSITION = (0, 0, 0)



class ItemPY3DBP:
    def __init__(self, name, xDim, yDim, zDim):

        self.name = name
        self.xDim = xDim
        self.yDim = yDim
        self.zDim = zDim
        self.rotation_type = [1,1,1]
        self.position = START_POSITION
        self.volume = self.get_volume()
        self.firstValue=1
        self.secondValue=1
        self.thirdValue=1
        self.dimension=None
        self.edgePoints=[]
        self.minTuple=None
        self.maxTuple=None
        # updates dimension
        self.set_rotation_type_and_dimension(self.rotation_type)
        self.depth=None
        self.pivotSets=None
        self.nextSmallestItemDepth=None
    def initialize_pivot_sets(self,numberOfSets):
        self.pivotSets=[set() for count in range(0, numberOfSets)]
    def set_depth(self, depth):
        self.depth=depth
    def set_rotation_type_and_dimension(self, rotation_type):
        self.rotation_type=rotation_type

        self.firstValue,self.secondValue,self.thirdValue=rotation_type[0],rotation_type[1],rotation_type[2]


        self.dimension=[
            self.firstValue*self.xDim,
            self.secondValue*self.yDim,
            self.thirdValue*self.zDim
        ]

        # we do this using the less verbose form for a computational speedup because this code gets hit so heavily
        position1PlusDimension1=self.position[0]+self.get_dimension()[0]
        position2PlusDimension2=self.position[1]+self.get_dimension()[1]
        position3PlusDimension3=self.position[2]+self.get_dimension()[2]
        self.edgePoints=([
            [self.position[0],self.position[1],self.position[2]],
            [position1PlusDimension1,self.position[1],self.position[2]],
            [self.position[0],position2PlusDimension2,self.position[2]],
            [position1PlusDimension1,position2PlusDimension2,self.position[2]],
            [self.position[0],self.position[1],position3PlusDimension3],
            [position1PlusDimension1,self.position[1],position3PlusDimension3],
            [self.position[0],position2PlusDimension2,position3PlusDimension3],
            [position1PlusDimension1,position2PlusDimension2,position3PlusDimension3],


        ])
        self.minTuple=min([self.position[0],self.position[1],self.position[2]],[position1PlusDimension1,position2PlusDimension2,position3PlusDimension3])
        self.maxTuple=max([self.position[0],self.position[1],self.position[2]],[position1PlusDimension1,position2PlusDimension2,position3PlusDimension3])
        
    def string(self):
        return "%s(%fx%fx%f, weight: %s) pos(%f, %f, %f) rt(%s) vol(%s)" % (
            self.name, self.xDim, self.yDim, self.zDim, self.weight,
            self.position[0], self.position[1], self.position[2], self.rotation_type, self.volume
        )

    def get_volume(self):
        return abs(self.xDim * self.yDim * self.zDim)

    def get_dimension(self):
        return self.dimension
        






class ContainerPY3DBP:
    def __init__(self, name, xDim, yDim, zDim):
        self.name = name
        self.xDim = xDim
        self.yDim = yDim
        self.zDim = zDim
        self.items = []
        self.unfitted_items = []
        self.volume = self.get_volume()

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.name, self.xDim, self.yDim, self.zDim,
            self.volume
        )

    def get_volume(self):
        return abs(self.xDim * self.yDim * self.zDim)





        
class Packer:
    # default initilization of rotation types to all rotations (-,-,-) to (+,+,+); all 8
    def __init__(self,rotationTypes):
        self.container = None
        self.items = []
        self.unfit_items = []
        self.total_items = 0
        self.cache=[]
        self.rotationTypes=rotationTypes
        # default 10 minute timeout

        self.timeout=time.time()+10


    def set_container(self, container):
        self.container=container

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)
    

    def pack(self,render=False, bigger_first=False, distribute_items=False):
        self.unfit_items=copy.deepcopy(self.items)
        self.items=[]
        # stuff that is useful in disqualifying bad pivots
        depthCount=0
        for item in self.unfit_items:
            item.set_depth(depthCount)
            item.initialize_pivot_sets(len(self.unfit_items))
            depthCount+=1
        for upperItemIndex in range(0, len(self.unfit_items)):
            upperItem=self.unfit_items[upperItemIndex]
            for lowerItemIndex in range(upperItemIndex+1,len(self.unfit_items)):
                lowerItem=self.unfit_items[lowerItemIndex]
                if upperItem.xDim>lowerItem.xDim:
                    upperItem.nextSmallestItemDepth=lowerItem.depth
                    break
                if upperItem.yDim>lowerItem.yDim:
                    upperItem.nextSmallestItemDepth=lowerItem.depth
                    break
                if upperItem.zDim>lowerItem.zDim:
                    upperItem.nextSmallestItemDepth=lowerItem.depth
                    break
        # recursive calls
        # add the origin as a valid first point to try to the first item
        if self.try_to_place_an_item():

            return True
        else:
            return False

                
    # returns True if item can be placed here, False otherwise
    def try_to_place_an_item(self):
        itemToTryToPlace=self.unfit_items[0]
        # remember this is the entry point

        if self.items==[]:
            # try to place it at the origin
                for dimensionalRotation in self.rotationTypes:
                    itemToTryToPlace.set_rotation_type_and_dimension(dimensionalRotation)
                    # true by default item.position=[0,0,0]
                    if self.can_place_at_position(itemToTryToPlace):
                        # then do it
                        oldItem=self.unfit_items.pop(0)
                        self.items.append(oldItem)
                        
                        if self.unfit_items==[]:
                            return True
                        # send the new pivots down the line
                        self.unfit_items[0].pivotSets[itemToTryToPlace.depth].add((0,0,0))

                        if self.try_to_place_an_item():
                            return True
                        # get rid of any sideeffects
                        self.unfit_items[0].pivotSets[itemToTryToPlace.depth]=set()
                        oldItem=self.items.pop(len(self.items)-1)
                        self.unfit_items.insert(0,oldItem)
                # couldn't find an arrangment; no need to remove sideffects
                return False


        # old way of getting pivots
        '''
        possiblePivots=set()
        for currentItem in self.items:
            # 8 pivot points
            for pivotPoint in Axis.ALL:

                # update the pivot; this should proably be hid behind a 'get_pivot' method
                firstValue,secondValue,thirdValue=pivotPoint[0],pivotPoint[1],pivotPoint[2]
                newPivot=(currentItem.position[0]+firstValue*currentItem.xDim,currentItem.position[1]+secondValue*currentItem.yDim,currentItem.position[2]+thirdValue*currentItem.zDim)
                possiblePivots.add(newPivot)
                
        '''



        # the new way of doing things
        newPivots=set()
        # TODO
        # get the new pivots (as the result of using the last item); a little odd to not update immediately
        for pivotPoint in Axis.ALL:
        
            # update the pivot; this should proably be hid behind a 'get_pivot' method
            firstValue,secondValue,thirdValue=pivotPoint[0],pivotPoint[1],pivotPoint[2]
            previousItem=self.items[len(self.items)-1]
            newPivot=(previousItem.position[0]+firstValue*previousItem.xDim,previousItem.position[1]+secondValue*previousItem.yDim,previousItem.position[2]+thirdValue*previousItem.zDim)
            newPivots.add(newPivot)
        
        for pivotSet in itemToTryToPlace.pivotSets:
            for point in pivotSet:
                newPivots.add(point)
        #assert(newPivots==possiblePivots)        
        #possiblePivots=sorted(list(possiblePivots))

        # this is essential to getting new pivots to work nicely
        possiblePivots=sorted(list(newPivots))
        for pivotIndex in range(0, len(possiblePivots)):
            itemToTryToPlace.position=possiblePivots[pivotIndex]
            for dimensionalRotation in self.rotationTypes:
                itemToTryToPlace.set_rotation_type_and_dimension(dimensionalRotation)

                if self.can_place_at_position(itemToTryToPlace):
                    # then do it
                    oldItem=self.unfit_items.pop(0)
                    self.items.append(oldItem)
                    self.cache=[]
                    if self.unfit_items==[]:
                        return True
                    # send the new pivots down the line
                    for p in range(pivotIndex, len(possiblePivots)):
                        self.unfit_items[0].pivotSets[itemToTryToPlace.depth].add(possiblePivots[p])
                    #self.unfit_items[0].pivotSets[itemToTryToPlace.depth]=copy.deepcopy(possiblePivots)
                    if self.try_to_place_an_item():
                        return True
                    # clear any sideeffects
                    for p in range(pivotIndex, len(possiblePivots)):
                        self.unfit_items[0].pivotSets[itemToTryToPlace.depth].remove(possiblePivots[p])
                    #self.unfit_items[0].pivotSets[itemToTryToPlace.depth]=set()

                    self.cache=[]
                    oldItem=self.items.pop(len(self.items)-1)
                    self.unfit_items.insert(0,oldItem)
            if time.time()>self.timeout:
                raise TimeoutError('couldnt pack item in time')
            # add the point to the next item so that it could possibly use it as a valid point
            if not itemToTryToPlace.nextSmallestItemDepth==None:
                #print(itemToTryToPlace.nextSmallestItemDepth)
                #print(self.items)
                #print(self.unfit_items)
                self.unfit_items[itemToTryToPlace.nextSmallestItemDepth-(len(self.items))].pivotSets[itemToTryToPlace.depth].add(possiblePivots[pivotIndex])
            #add the pivot to a lower location
        # reset sideffects caused by single point adding (not necessary yet) for all lower items and this item
        for lowerItem in self.unfit_items:
            lowerItem.pivotSets[itemToTryToPlace.depth]=set()
        return False
    # returns true if you can place at a position
    def can_place_at_position(self, item):
        render=False
        if render:
            from . import testing_underfitting
            from .testing_underfitting import render_something_that_failed
            coordinates={}
            innerItems=[]
            count=0
            doneBefore=False
            for itemInner in self.items+[item]:
                count+=1
                # this is because equality is custom defined
                if itemInner==item and (not doneBefore):
                    coordinates[(item.position[0],item.position[1],item.position[2],count)]=(itemInner.get_dimension()[0], itemInner.get_dimension()[1], itemInner.get_dimension()[2])
                    doneBefore=True
                else:
                    coordinates[(itemInner.position[0],itemInner.position[1],itemInner.position[2],count)]=(itemInner.get_dimension()[0], itemInner.get_dimension()[1], itemInner.get_dimension()[2])
                innerItems.append(itemInner)
            print(len(coordinates))

            render_something_that_failed(self.container, innerItems,coordinates,self.rotationTypes)


        if outside_container(item, self.container.xDim,self.container.yDim, self.container.zDim):
            return False


        if not (self.cache==[]):
            if intersect_lucas(self.cache[0], item,self.container.xDim, self.container.yDim, self.container.zDim):
                return False

        for current_item_in_bin in reversed(self.items):
            if current_item_in_bin is not item:
                if intersect_lucas(current_item_in_bin, item,self.container.xDim,self.container.yDim, self.container.zDim):
                    self.cache=[current_item_in_bin]
                    return False
        return True