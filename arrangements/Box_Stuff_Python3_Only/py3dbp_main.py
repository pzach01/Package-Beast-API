from . import py3dbp_constants
from .py3dbp_constants import RotationType,Axis
from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import intersect_lucas,outside_container
import copy

START_POSITION = [0, 0, 0]



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
        # updates dimension
        self.set_rotation_type_and_dimension(self.rotation_type)
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
        self.edgePoints=sorted([
            [self.position[0],self.position[1],self.position[2]],
            [position1PlusDimension1,self.position[1],self.position[2]],
            [self.position[0],position2PlusDimension2,self.position[2]],
            [position1PlusDimension1,position2PlusDimension2,self.position[2]],
            [self.position[0],self.position[1],position3PlusDimension3],
            [position1PlusDimension1,self.position[1],position3PlusDimension3],
            [self.position[0],position2PlusDimension2,position3PlusDimension3],
            [position1PlusDimension1,position2PlusDimension2,position3PlusDimension3],


        ])
        
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


    def set_container(self, container):
        self.container=container

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)
    

    def pack(self,render=False, bigger_first=False, distribute_items=False):
        self.unfit_items=copy.deepcopy(self.items)
        self.items=[]
        # recursive calls
        if self.try_to_place_an_item(self.unfit_items[0]):

            return True
        else:
            return False

                
    # returns True if item can be placed here, False otherwise
    def try_to_place_an_item(self,item):
    
        # remember this is the entry point

        if self.items==[]:
            # try to place it at the origin
                for dimensionalRotation in self.rotationTypes:
                    item.set_rotation_type_and_dimension(dimensionalRotation)
                    # true by default item.position=[0,0,0]
                    if self.can_place_at_position(item):
                        # then do it
                        self.items.append(item)
                        self.unfit_items.remove(item)
                        if self.unfit_items==[]:
                            return True
                        elif self.try_to_place_an_item(self.unfit_items[0]):
                            return True
                        else:
                            self.items.remove(item)
                            self.unfit_items.append(item)
                # couldn't find an arrangment
                return False
        possiblePivots=[]
        for currentItem in self.items:
            # 8 pivot points
            for pivotPoint in Axis.ALL:

                # update the pivot; this should proably be hid behind a 'get_pivot' method
                firstValue,secondValue,thirdValue=pivotPoint[0],pivotPoint[1],pivotPoint[2]
                newPivot=[currentItem.position[0]+firstValue*currentItem.xDim,currentItem.position[1]+secondValue*currentItem.yDim,currentItem.position[2]+thirdValue*currentItem.zDim]
                if newPivot not in possiblePivots:
                    possiblePivots.append(newPivot)
                


        
        possiblePivots=sorted(possiblePivots)

        for pivot in possiblePivots:
            item.position=pivot
            for dimensionalRotation in self.rotationTypes:
                item.set_rotation_type_and_dimension(dimensionalRotation)

                if self.can_place_at_position(item):
                    # then do it
                    self.items.append(item)
                    self.unfit_items.remove(item)
                    self.cache=[]
                    if self.unfit_items==[]:
                        return True
                    elif self.try_to_place_an_item(self.unfit_items[0]):
                        return True
                    else:
                        self.cache=[]
                        self.items.remove(item)
                        self.unfit_items.append(item)

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