from __future__ import division
import time
import copy
import os




        
def pickle_file(fileName, pickledObject):
    from pickle import Pickler
    file = open(fileName, 'wb')
    p = Pickler(file)
    p.dump(pickledObject)
    file.close() 
def unpickel_file(fileName):
    from pickle import Unpickler    
    file = open(fileName, 'rb')
    up = Unpickler(file)
    returnObject= up.load()
    file.close()
    return returnObject





import random
import box_stuff2
r=unpickel_file('python2random')
def time_finding_optimal_solution(n,fits=False):
    for numBoxes in range(1, 11):
        for numBins in range(1, 11):
            start=time.time()
            errorCount=0
            couldntAddShapeCount=0
            for numTrials in range(0, n):
                if(fits):
                    bins, boxes=copy.deepcopy(generate_boxes_that_fit(numBins, numBoxes))
                else:
                    bins, boxes=copy.deepcopy(generate_random_bin_box_string(numBins, numBoxes))                
                try:
                    

                    box_stuff2.master_calculate_optimal_solution(bins, boxes)
                except NotImplementedError:
                    errorCount+=1
                except ValueError:
                    print(bins, boxes)
                    
                    couldntAddShapeCount+=1
            end=time.time()        
            average=(end-start)/n
            print("Bins: "+str(numBins))
            print("Boxes: "+str(numBoxes))
            print("Average time: "+str(average))
            print("Error Frequency:"+str(errorCount/n))
            ### occurs when there was an order for a particurlar frequency, but the box couldnt figure out how to add it (in my code)
            print("Serious Error Frequency:"+str(couldntAddShapeCount/n))
# produces .79 if python3 code behaves the same as python2 code
def same_as_python2_test():
    listy=[
    ['91x69x77'],
    ['91x26x64'],
    ['91x88x58'],
    ['17x42x100'],
    ['11x32x96'],
    ['45x21x32'],
    ['91x34x43'],
    ['63x81x50'],
    ['9x58x4'],
    ['10x20x70'],
    ['29x70x17'],
    ['12x3x71'],
    ['86x22x24'],
    ['2x65x31'],
    ['14x65x60'],
    ['45x16x64'],
    ['56x44x17'],
    ['93x87x69'],
    ['100x59x35'],
    ['12x61x52'],
    ['44x100x84'],
    ['12x89x1'],
    ['66x32x73'],
    ['96x54x77'],
    ['6x67x12'],
    ['46x34x8'],
    ['75x10x26'],
    ['9x67x31'],
    ['5x3x22'],
    ['51x2x3'],
    ['67x53x14'],
    ['32x13x28'],
    ['39x22x20'],
    ['23x31x56'],
    ['89x65x45'],
    ['1x19x64'],
    ['41x85x91'],
    ['30x37x30'],
    ['68x10x28'],
    ['88x38x97'],
    ['40x84x47'],
    ['10x58x22'],
    ['92x71x53'],
    ['93x55x97'],
    ['72x18x30'],
    ['85x10x99'],
    ['5x75x62'],
    ['41x61x59'],
    ['36x29x5'],
    ['66x89x38'],
    ['86x40x26'],
    ['81x93x10'],
    ['88x32x78'],
    ['30x100x34'],
    ['21x6x14'],
    ['10x83x3'],
    ['12x24x15'],
    ['78x1x69'],
    ['35x15x23'],
    ['53x25x40'],
    ['39x54x71'],
    ['30x61x72'],
    ['30x77x9'],
    ['50x36x13'],
    ['66x86x49'],
    ['36x91x100'],
    ['63x57x64'],
    ['71x69x54'],
    ['76x75x65'],
    ['53x38x22'],
    ['51x31x48'],
    ['18x91x13'],
    ['88x57x92'],
    ['89x18x28'],
    ['100x67x9'],
    ['27x10x31'],
    ['8x4x5'],
    ['48x72x51'],
    ['68x66x14'],
    ['71x51x42'],
    ['97x46x69'],
    ['78x49x16'],
    ['19x29x20'],
    ['41x7x77'],
    ['77x64x12'],
    ['22x90x88'],
    ['73x87x21'],
    ['29x44x48'],
    ['37x25x82'],
    ['19x58x82'],
    ['16x34x38'],
    ['29x92x88'],
    ['13x7x60'],
    ['51x4x87'],
    ['88x57x9'],
    ['20x84x69'],
    ['45x94x5'],
    ['69x84x83'],
    ['10x71x57'],
    ['63x16x97'],
    ['97x12x56'],
    ['54x45x34'],
    ['24x74x52'],
    ['46x51x29'],
    ['90x77x27'],
    ['31x54x64'],
    ['91x93x7'],
    ['87x2x58'],
    ['78x18x23'],
    ['8x45x84'],
    ['1x76x39'],
    ['94x57x47'],
    ['29x85x47'],
    ['70x67x82'],
    ['30x11x19'],
    ['63x12x4'],
    ['36x67x19'],
    ['30x13x98'],
    ['91x99x64'],
    ['38x28x35'],
    ['79x55x14'],
    ['89x86x2'],
    ['10x51x48'],
    ['83x22x99'],
    ['35x15x98'],
    ['77x80x18'],
    ['97x31x47'],
    ['88x12x3'],
    ['62x51x95'],
    ['98x37x75'],
    ['3x72x45'],
    ['32x29x48'],
    ['46x32x3'],
    ['4x3x85'],
    ['43x46x92'],
    ['9x82x89'],
    ['43x71x3'],
    ['40x2x74'],
    ['98x93x53'],
    ['82x68x1'],
    ['32x11x44'],
    ['34x3x2'],
    ['12x57x84'],
    ['64x88x23'],
    ['25x38x7'],
    ['53x12x7'],
    ['85x26x45'],
    ['47x5x4'],
    ['87x92x76'],
    ['47x19x16'],
    ['53x22x63'],
    ['100x95x25'],
    ['24x5x93'],
    ['97x84x73'],
    ['60x92x32'],
    ['50x92x61'],
    ['36x20x29'],
    ['87x60x72'],
    ['85x74x54'],
    ['6x79x24'],
    ['18x4x51'],
    ['63x11x11'],
    ['46x52x23'],
    ['91x44x25'],
    ['81x78x32'],
    ['35x43x7'],
    ['91x21x22'],
    ['73x47x66'],
    ['15x67x97'],
    ['98x3x15'],
    ['22x59x52'],
    ['49x26x11'],
    ['47x23x67'],
    ['98x14x90'],
    ['94x39x3'],
    ['35x26x73'],
    ['98x97x22'],
    ['23x42x26'],
    ['66x62x2'],
    ['24x45x43'],
    ['75x9x9'],
    ['40x18x13'],
    ['98x69x5'],
    ['75x12x95'],
    ['22x34x5'],
    ['23x14x72'],
    ['95x11x26'],
    ['84x57x84'],
    ['32x8x45'],
    ['42x13x64'],
    ['74x57x70'],
    ['74x88x71'],
    ['32x88x89'],
    ['86x93x1'],
    ['87x85x34'],
    ['17x79x87'],
    ['42x6x16'],
    ['31x67x79'],
    ['11x8x64'],
    ['46x51x92']]
    errorCount=0
    couldntAddShapeCount=0
    for ele in range(0,100):
        
        try:
            

            box_stuff2.master_calculate_optimal_solution(listy[ele*2], listy[ele*2+1])
        except NotImplementedError:
            errorCount+=1
        except ValueError:
            print(listy[ele*2])
            print(listy[ele*2+1])
            couldntAddShapeCount+=1   
    print("Error Frequency:"+str(errorCount/100))
    

def generate_random_bin_box_string(numBins, numBoxes):  
    binList=[]
    boxList=[]
    for num in range(0, numBins):
        height=r.randint(1,100)
        width=r.randint(1,100)
        length=r.randint(1,100)
        string='{height}x{width}x{length}'.format(height=height, width=width, length=length)
        binList.append(string)
    for num in range(0, numBoxes):
        height=r.randint(1,100)
        width=r.randint(1,100)
        length=r.randint(1,100)
        string='{height}x{width}x{length}'.format(height=height, width=width, length=length)
        boxList.append(string)
    return binList, boxList




def generate_box_percent_ranges(n):
    aList=[[element] for element in range(1, 101)]
    for element in range(1, n):
        newList=[]
        for element in range(0, len(aList)):
            temp=generate_ranges_helper(aList[element])
            for sublist in temp:
                newList.append(sublist) 
            print(element)
        aList=copy.deepcopy(newList)
    return aList

# generate boxes that must fit in at least one box (without any other boxes)
def generate_boxes_that_fit(numBins, numBoxes):
    binList=[]
    boxList=[]
    for num in range(0, numBins):
        height=r.randint(1,100)
        width=r.randint(1,100)
        length=r.randint(1,100)
        string='{height}x{width}x{length}'.format(height=height, width=width, length=length)
        binList.append(string)
    
    bounds=binList
    for num in range(0, numBoxes):
        boxSelected=bounds[r.randint(0,len(bounds)-1)]
        x,y,z=int(boxSelected.split('x')[0]),int(boxSelected.split('x')[1]),int(boxSelected.split('x')[2])
        height=r.randint(1,x)
        width=r.randint(1,y)
        length=r.randint(1,z)
        string='{height}x{width}x{length}'.format(height=height, width=width, length=length)
        boxList.append(string)
    return binList, boxList
        
        
        
        
def generate_ranges_helper(oldList):
    newList=[]
    for num in range(1, 101):
        temp=copy.deepcopy(oldList)
        temp.append(num)
        newList.append(temp)
    return newList


# test if adding the cost constraint behaves as 'sposed to
def cost_testing():


    bins=['10x10x10','8x8x8','8x8x8']
    boxes=['5x5x5','5x5x5']
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[100, 1,1])    
    assert(sum([bin.volume for bin in binList])==1024)
    
    
    

    bins=['10x10x10','8x8x8','8x8x8']
    boxes=['5x5x5','5x5x5']
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[1, 1,1])    
    assert(sum([bin.volume for bin in binList])==1000) 
    
    
    

    bins=['10x10x10','8x8x8','8x8x8','7x7x7']
    boxes=['5x5x5','5x5x5']
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[100, 1,1.50,1])    
    assert(sum([bin.volume for bin in binList])==855)    
    
    
    
    print("Passed Test")


def weight_testing():
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1']
    binWeights=[100,1]
    boxWeights=[20,20]
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(sum([bin.volume for bin in binList])==1000)   
    
    
    
    
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1']
    binWeights=[100,100]
    boxWeights=[20,20]
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(sum([bin.volume for bin in binList])==8**3)   
    
    
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1','1x1x1','1x1x1','1x1x1']
    binWeights=[120,100]
    boxWeights=[20,20,20,20,20]
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(sum([bin.volume for bin in binList])==10**3)      
        
    bins=['10x10x10','8x8x8']
    boxes=['1x1x1','1x1x1','1x1x1','1x1x1','1x1x1']
    binWeights=[151,100]
    boxWeights=[20,25,30,35,40]
    binList,packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=None, binWeightCapacitys=binWeights, boxWeights=boxWeights)   
    assert(sum([bin.volume for bin in binList])==10**3) 
    
    
     
same_as_python2_test()
