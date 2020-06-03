from . import py3dbp_constants
from .py3dbp_constants import RotationType, Axis
from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import intersect_lucas

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


    def string(self):
        return "%s(%fx%fx%f, weight: %s) pos(%f, %f, %f) rt(%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position[0], self.position[1], self.position[2], self.rotation_type, self.volume
        )

    def get_volume(self):
        return self.width * self.height * self.depth

    def get_dimension(self):
        # is a number
        axisCopy=self.rotation_type
        firstBit=axisCopy//(3**2)
        axisCopy=axisCopy%(3**2)
        secondBit=axisCopy//(3**1)
        axisCopy=axisCopy%(3**1)
        thirdBit=axisCopy
        #firstValue=[0 if firstBit==0 else 1 if firstBit==1 else -1][0]
        #secondValue=[0 if secondBit==0 else 1 if secondBit==1 else -1][0]
        #thirdValue=[0 if thirdBit==0 else 1 if thirdBit==1 else -1][0]
        firstValue=1 if firstBit==0 else -1
        secondValue=1 if secondBit==0 else -1
        thirdValue=1 if thirdBit==0 else -1
        dimension=[
            firstValue*self.width,
            secondValue*self.height,
            thirdValue*self.depth
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
        return self.width * self.height * self.depth

    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return total_weight


    def put_item(self, item, pivot):
            if pivot[0]<0 or pivot[1]<0 or pivot[2]<0:
                return False
            fit = False
            valid_item_position = item.position
            item.position = pivot

            for i in range(0, len(RotationType.ALL)):
                if item not in self.items:

                    item.rotation_type = i
                    dimension = item.get_dimension()


                    if (
                        self.width < pivot[0] + dimension[0] or
                        self.height < pivot[1] + dimension[1] or
                        self.depth < pivot[2] + dimension[2]
                    ):
                        continue

                    fit = True

                    for current_item_in_bin in self.items:
                        if intersect_lucas(current_item_in_bin, item,self.width,self.height, self.depth):
                            fit = False
                            break

                    if fit:
                        if self.get_total_weight() + item.weight > self.max_weight:
                            fit = False
                            return fit

                        #print("item appended to bin:", item.string())
                        self.items.append(item)
                    
                    # experimental below: need something like this to prevent item from going outside bin
                    if (item.width+item.get_dimension()[0]<0):
                        fit=False
                    if (item.height+item.get_dimension()[1]<0):
                        fit=False
                    if (item.depth+item.get_dimension()[2]<0):
                        fit=False
    
                    if not fit:
                        item.position = valid_item_position

                    return fit

            if not fit:
                item.position = valid_item_position

            return fit


        
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
        #             print(i)

        #             for current_item_in_bin in self.items:
        #                 if intersect(current_item_in_bin, item):
        #                     fit = False
        #                     break

        #             if fit:
        #                 if self.get_total_weight() + item.weight > self.max_weight:
        #                     fit = False
        #                     return fit
        #                 print("p-0", pivot[0], "p-1", pivot[1], "p-2", pivot[2])
        #                 print("dim-0", dimension[0], "dim-1", dimension[1], "dim-2", dimension[2])
        #                 print("rotation", item.rotation_type)
        #                 print("sss", item.string())
        #                 self.items.append(item)   

        #             if not fit:
        #                 item.position = valid_item_position
        #             return fit

        #     if not fit:
        #         item.position = valid_item_position 
        #     return fit
        


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)

    def pack_to_bin(self, bin, item,render):
        fitted = False

        if not bin.items:
            response = bin.put_item(item, START_POSITION)

            if not response:
                bin.unfitted_items.append(item)

            return

        for axis in range(0, len(Axis.ALL)):
            for currentItem in bin.items:
                pivot = [0, 0, 0]

                # 3 'bit' string in base 3 yields 27 combinations
                # 1st 'bit'= +, -, or no addition
                # 2nd 'bit' =+, -, or no addition
                # 3rd 'bit' =+, -, or no addition 
                # not sure if this line is neccessary
                axisCopy=axis
                firstBit=axisCopy//(2**2)
                axisCopy=axisCopy%(2**2)
                secondBit=axisCopy//(2**1)
                axisCopy=axisCopy%(2**1)
                thirdBit=axisCopy
                #firstValue=[0 if firstBit==0 else 1 if firstBit==1 else -1][0]
                #secondValue=[0 if secondBit==0 else 1 if secondBit==1 else -1][0]
                #thirdValue=[0 if thirdBit==0 else 1 if thirdBit==1 else -1][0]
                firstValue=0 if firstBit==0 else 1
                secondValue=0 if secondBit==0 else 1
                thirdValue=0 if thirdBit==0 else 1
                pivot=[
                    currentItem.position[0]+firstValue*currentItem.width,
                    currentItem.position[1]+secondValue*currentItem.height,
                    currentItem.position[2]+thirdValue*currentItem.depth
                ]


                render=False
                if render:
                    from . import testing_underfitting
                    from .testing_underfitting import render_something_that_failed
                    coordinates={}
                    innerItems=[]
                    count=0
                    doneBefore=False
                    for itemInner in bin.items+[item]:
                        count+=1
                        # this is because equality is custom defined
                        if itemInner==item and (not doneBefore):
                            coordinates[(pivot[0],pivot[1],pivot[2],count)]=(itemInner.get_dimension()[0], itemInner.get_dimension()[1], itemInner.get_dimension()[2])
                            doneBefore=True
                        else:
                            coordinates[(itemInner.position[0],itemInner.position[1],itemInner.position[2],count)]=(itemInner.get_dimension()[0], itemInner.get_dimension()[1], itemInner.get_dimension()[2])
                        innerItems.append(itemInner)
                    render_something_that_failed(bin, innerItems,coordinates)
                res=bin.put_item(item,pivot)

                if res:
                    fitted = True
                    break



        if not fitted:
            bin.unfitted_items.append(item)

    def pack(self,render=False, bigger_first=False, distribute_items=False):
        self.bins.sort(key=lambda bin: bin.volume, reverse=bigger_first)
        # self.items.sort(key=lambda item: item.volume, reverse=bigger_first)

        for bin in self.bins:
            for item in self.items:
                self.pack_to_bin(bin, item,render)
            #print('\n')
            if distribute_items:
                for item in bin.items:
                    self.items.remove(item)