from . import py3dbp_constants
from .py3dbp_constants import RotationType, Axis, CouldntFit
from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import intersect_lucas,outside_container

START_POSITION = [0, 0, 0]



class ItemPY3DBP:
    def __init__(self, name, width, height, depth, weight):

        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.rotation_type = 0
        self.position = START_POSITION
        self.volume = self.get_volume()
        self.firstValue=1
        self.secondValue=1
        self.thirdValue=1
    def set_rotation_type(self, rotation_type):
        self.rotation_type=rotation_type

        permutation=self.rotation_type//(8**1)
        axisCopy=self.rotation_type%(8**1)
        
        firstBit=axisCopy//(2**2)
        axisCopy=axisCopy%(2**2)
        secondBit=axisCopy//(2**1)
        axisCopy=axisCopy%(2**1)
        thirdBit=axisCopy
        self.firstValue=1 if firstBit==0 else -1
        self.secondValue=1 if secondBit==0 else -1
        self.thirdValue=1 if thirdBit==0 else -1

        if permutation==0:
            self.width,self.height,self.depth=self.width,self.height,self.depth
        if permutation==1:
            self.width,self.height,self.depth=self.width, self.depth, self.height
        if permutation==2:
            self.width, self.height, self.depth=self.height, self.width, self.depth
        if permutation==3:
            self.width, self.height, self.depth==self.height, self.depth, self.width
        if permutation==4:
            self.width, self.height, self.depth=self.depth, self.width, self.height
        if permutation==5:
            self.width, self.height, self.depth=self.depth, self.height, self.width
        # also there is 
        # LxWxH
        # LxHxW
        # HxLxW
        # HxWxL
        # WxHxL
        # WxLxH

    def string(self):
        return "%s(%fx%fx%f, weight: %s) pos(%f, %f, %f) rt(%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position[0], self.position[1], self.position[2], self.rotation_type, self.volume
        )

    def get_volume(self):
        return abs(self.width * self.height * self.depth)

    def get_dimension(self):
        # is a number

        #firstValue=[0 if firstBit==0 else 1 if firstBit==1 else -1][0]
        #secondValue=[0 if secondBit==0 else 1 if secondBit==1 else -1][0]
        #thirdValue=[0 if thirdBit==0 else 1 if thirdBit==1 else -1][0]
        '''
        if self.rotation_type==0:
            return [self.width, self.height, self.depth]
        if self.rotation_type==1:
            return [self.width, self.depth, self.height]
        if self.rotation_type==2:
            return [self.height, self.width, self.depth]
        if self.rotation_type==3:
            return [self.height, self.depth, self.width]
        if self.rotation_type==4:
            return [self.depth, self.width, self.height]
        if self.rotation_type==5:
            return [self.depth, self.height, self.width]
        '''
        dimension=[
            self.firstValue*self.width,
            self.secondValue*self.height,
            self.thirdValue*self.depth
        ]
        




        return dimension


class ContainerPY3DBP:
    def __init__(self, name, width, height, depth, max_weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items = []
        self.unfitted_items = []
        self.volume = self.get_volume()

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight,
            self.volume
        )

    def get_volume(self):
        return abs(self.width * self.height * self.depth)

    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return total_weight



        
        # def put_item(self, item, pivot):
        #     fit = False
        #     valid_item_position = item.position
        #     item.position = pivot

            
        #     for i in range(0, len(RotationType.ALL)):
                
        #         if fit == False:

        #             dimension = item.get_dimension()
                    

        #             if (
        #                 self.width < pivot[0] + dimension[0] or
        #                 self.height < pivot[1] + dimension[1] or
        #                 self.depth < pivot[2] + dimension[2]
        #             ):  
        #                 continue

        #             fit = True
        #             item.rotation_type = i   

        #             for current_item_in_bin in self.items:
        #                 if intersect(current_item_in_bin, item):
        #                     fit = False
        #                     break

        #             if fit:
        #                 if self.get_total_weight() + item.weight > self.max_weight:
        #                     fit = False
        #                     return fit

        #                 self.items.append(item)   

        #             if not fit:
        #                 item.position = valid_item_position
        #             return fit

        #     if not fit:
        #         item.position = valid_item_position 
        #     return fit
        

# return None if you can't pack to bin otherwise the items with their positions
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
    
    def pack_to_bin(self, bin, item,render):
        fitted = False

        if len(bin.items)==0:
            bin.put_item(item, START_POSITION)

            if not response:
                bin.unfitted_items.append(item)

            return

        for axis in range(0, len(Axis.ALL)):
            for currentItem in bin.items:
                #print('Axis: '+str(axis))
                pivot = [0, 0, 0]

                # 1st 'bit'= +, -
                # 2nd 'bit' =+, -
                # 3rd 'bit' =+, - 
                # not sure if this line is neccessary




                res=bin.put_item(item,pivot)

                if res:
                    fitted = True
                    break



        if not fitted:
            bin.unfitted_items.append(item)

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
                    item.rotation_type=dimensionalRotation
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
                #firstValue=[0 if firstBit==0 else 1 if firstBit==1 else -1][0]
                #secondValue=[0 if secondBit==0 else 1 if secondBit==1 else -1][0]
                #thirdValue=[0 if thirdBit==0 else 1 if thirdBit==1 else -1][0]
        
                #firstValue=0 if firstBit==0 else 1
                #secondValue=0 if secondBit==0 else 1
                #thirdValue=0 if thirdBit==0 else 1
                '''
                item.position=[
                    currentItem.position[0]+firstValue*currentItem.width,
                    currentItem.position[1]+secondValue*currentItem.height,
                    currentItem.position[2]+thirdValue*currentItem.depth
                ]
                '''
                possiblePivots.append(
                    [currentItem.position[0]+firstValue*currentItem.width,
                    currentItem.position[1]+secondValue*currentItem.height,
                    currentItem.position[2]+thirdValue*currentItem.depth]
                )


        #print('unsorted:'+str(possiblePivots))
        
        possiblePivots=sorted(possiblePivots)
        #print('sorted:'+str(possiblePivots))

        for pivot in possiblePivots:
            item.position=pivot
            #print(pivot)
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


        # needed for special case where there are no other items in the container but still need to know if in bounds
        if outside_container(item, self.bins[0].width,self.bins[0].height, self.bins[0].depth):
            return False


        # reverse to (hopefully) get collisions faster
        if not (self.cache==[]):
            if intersect_lucas(self.cache[0], item,self.bins[0].width, self.bins[0].height, self.bins[0].depth):
                return False


        for current_item_in_bin in reversed(self.items):
            if current_item_in_bin is not item:
                if intersect_lucas(current_item_in_bin, item,self.bins[0].width,self.bins[0].height, self.bins[0].depth):
                    self.cache=[current_item_in_bin]
                    #print('Insersected')
                    return False
        #print('No intersection')
        return True