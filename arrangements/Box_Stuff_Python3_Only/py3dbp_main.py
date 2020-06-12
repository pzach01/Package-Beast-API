from . import py3dbp_constants
from .py3dbp_constants import RotationType, Axis
from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import intersect_lucas,outside_container

START_POSITION = [0, 0, 0]



class ItemPY3DBP:
    def __init__(self, name, width, height, depth):

        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.rotation_type = 0
        self.position = START_POSITION
        self.volume = self.get_volume()
        self.firstValue=1
        self.secondValue=1
        self.thirdValue=1
    def set_rotation_type(self, rotation_type):
        self.rotation_type=rotation_type

        axisCopy=self.rotation_type%(8**1)
        
        firstBit=axisCopy//(2**2)
        axisCopy=axisCopy%(2**2)
        secondBit=axisCopy//(2**1)
        axisCopy=axisCopy%(2**1)
        thirdBit=axisCopy
        self.firstValue=1 if firstBit==0 else -1
        self.secondValue=1 if secondBit==0 else -1
        self.thirdValue=1 if thirdBit==0 else -1




    def string(self):
        return "%s(%fx%fx%f, weight: %s) pos(%f, %f, %f) rt(%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position[0], self.position[1], self.position[2], self.rotation_type, self.volume
        )

    def get_volume(self):
        return abs(self.width * self.height * self.depth)

    def get_dimension(self):
        dimension=[
            self.firstValue*self.width,
            self.secondValue*self.height,
            self.thirdValue*self.depth
        ]
        




        return dimension


class ContainerPY3DBP:
    def __init__(self, name, width, height, depth):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.items = []
        self.unfitted_items = []
        self.volume = self.get_volume()

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth,
            self.volume
        )

    def get_volume(self):
        return abs(self.width * self.height * self.depth)





        
class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0
        self.cache=[]


    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)
    

    def pack(self,render=False, bigger_first=False, distribute_items=False):
        import copy
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
                for dimensionalRotation in RotationType.ALL:
                    item.set_rotation_type(dimensionalRotation)
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
                pivotCopy=pivotPoint
                thirdValue=pivotCopy//(2**2)
                pivotCopy=pivotCopy%(2**2)
                secondValue=pivotCopy//(2**1)
                pivotCopy=pivotCopy%(2**1)
                firstValue=pivotCopy

                possiblePivots.append(
                    [currentItem.position[0]+firstValue*currentItem.width,
                    currentItem.position[1]+secondValue*currentItem.height,
                    currentItem.position[2]+thirdValue*currentItem.depth]
                )


        
        possiblePivots=sorted(possiblePivots)

        for pivot in possiblePivots:
            item.position=pivot
            for dimensionalRotation in RotationType.ALL:
                item.set_rotation_type(dimensionalRotation)

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

            render_something_that_failed(self.bins[0], innerItems,coordinates)


        if outside_container(item, self.bins[0].width,self.bins[0].height, self.bins[0].depth):
            return False


        if not (self.cache==[]):
            if intersect_lucas(self.cache[0], item,self.bins[0].width, self.bins[0].height, self.bins[0].depth):
                return False

        for current_item_in_bin in reversed(self.items):
            if current_item_in_bin is not item:
                if intersect_lucas(current_item_in_bin, item,self.bins[0].width,self.bins[0].height, self.bins[0].depth):
                    self.cache=[current_item_in_bin]
                    return False
        return True