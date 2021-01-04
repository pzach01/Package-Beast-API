from . import testing_imports
from .testing_imports import *
from .single_pack import DimensionalMixupBigSetsGenerator,DimensionalMixupBigSetsGeneratorWithExhaustiveEnds,DimensionalMixupsGenerator

# doesnt test that partitions are optimal, merely that they enumerate all combinations
def test_2_partition():

    n=random.randint(1,20)
    count=0
    item_permutation=[]
    for ele in range(0,n):
        item=ItemPY3DBP(count,count+1,count+2,count+3)
        count+=4
        item_permutation.append(item)
    
    itemFlips=[random.randint(0,5),random.randint(0,5)]

    first=random.randint(0,n)
    partition=(first, n-first)

    permutationToObserve=convert_to_item_permutation(item_permutation, itemFlips,partition)

    mixer=DimensionalMixupBigSetsGenerator(item_permutation)
    permutationObserved=False
    while(True):
        try:
            res=mixer.next()
            if res is None:
                foundIt=False
            else:
                assert(len(res)==len(item_permutation))

                foundIt=True
                # check if all the items are equal
                for index in range(0, len(res)):
                    if not permutationToObserve[index].name==res[index].name:
                        foundIt=False
                    if not permutationToObserve[index].xDim==res[index].xDim:
                        foundIt=False
                    if not permutationToObserve[index].yDim==res[index].yDim:
                        foundIt=False
                    if not permutationToObserve[index].zDim==res[index].zDim:
                        foundIt=False
            if foundIt:
                permutationObserved=True
                break
        except StopIteration:
            break
    assert(permutationObserved)
def test_3_partition():
    n=random.randint(1,20)
    count=0
    item_permutation=[]
    for ele in range(0,n):
        item=ItemPY3DBP(count,count+1,count+2,count+3)
        count+=4
        item_permutation.append(item)
    
    itemFlips=[random.randint(0,5),random.randint(0,5),random.randint(0,5)]

    first=random.randint(0,n)
    second=random.randint(0,n-first)
    third=n-(first+second)
    assert((first+second+third)==n)
    # get nonbiased distribution over sample
    mix=random.randint(0,5)
    if mix==0:
        partition=(first, second,third)
    elif mix==1:
        partition=(first, third, second)
    elif mix==2:
        partition=(second, first, third)
    elif mix==3:
        partition=(second, third, first)
    elif mix==4:
        partition=(third, first, second)
    elif mix==5:
        partition=(third, second, first)

    permutationToObserve=convert_to_item_permutation(item_permutation, itemFlips,partition)

    mixer=DimensionalMixupBigSetsGenerator(item_permutation)
    permutationObserved=False
    while(True):
        try:
            res=mixer.next()
            if res is None:
                foundIt=False
            else:
                assert(len(res)==len(item_permutation))
                foundIt=True
                # check if all the items are equal
                for index in range(0, len(res)):
                    if not permutationToObserve[index].name==res[index].name:
                        foundIt=False
                    if not permutationToObserve[index].xDim==res[index].xDim:
                        foundIt=False
                    if not permutationToObserve[index].yDim==res[index].yDim:
                        foundIt=False
                    if not permutationToObserve[index].zDim==res[index].zDim:
                        foundIt=False

            if foundIt:
                permutationObserved=True
                break
        except StopIteration:
            break
    assert(permutationObserved)



def convert_to_item_permutation(item_permutation,itemFlips, partition):
    new_item_permutation=[]
    count=0
    globalCount=0
    for ele in partition:
        for thing in range(0, ele):
            if itemFlips[count]==0:
                new_item_permutation.append(ItemPY3DBP(item_permutation[globalCount].name,item_permutation[globalCount].xDim, item_permutation[globalCount].yDim,item_permutation[globalCount].zDim))
            elif itemFlips[count]==1:
                new_item_permutation.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].xDim, item_permutation[globalCount].zDim, item_permutation[globalCount].yDim))
            elif itemFlips[count]==2:
                new_item_permutation.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].yDim, item_permutation[globalCount].xDim, item_permutation[globalCount].zDim))
            elif itemFlips[count]==3:
                new_item_permutation.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].yDim, item_permutation[globalCount].zDim, item_permutation[globalCount].xDim))
            elif itemFlips[count]==4:
                new_item_permutation.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].zDim, item_permutation[globalCount].xDim, item_permutation[globalCount].yDim))
            elif itemFlips[count]==5:
                new_item_permutation.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].zDim, item_permutation[globalCount].yDim, item_permutation[globalCount].xDim))
            else:
                print(itemFlips[count])
                raise Exception("bug in BigSets testing")
            globalCount+=1
        count+=1
    return new_item_permutation


def test_3_partition_with_exhaustive_ending():

    n=random.randint(1,20)
    # crazy ending length cant be more then n; enforced in generator as well
    exhaustiveEndingLength=min(n,3)

    count=0
    item_permutation=[]
    for ele in range(0,n):
        item=ItemPY3DBP(count,count+1,count+2,count+3)
        count+=4
        item_permutation.append(item)
    
    itemFlips=[random.randint(0,5),random.randint(0,5),random.randint(0,5)]

    numItemsInPartition=n-exhaustiveEndingLength
    first=random.randint(0,numItemsInPartition)
    second=random.randint(0,numItemsInPartition-first)
    third=numItemsInPartition-(first+second)
    assert((first+second+third)==numItemsInPartition)
    # get nonbiased distribution over sample
    mix=random.randint(0,5)
    if mix==0:
        partition=(first, second,third)
    elif mix==1:
        partition=(first, third, second)
    elif mix==2:
        partition=(second, first, third)
    elif mix==3:
        partition=(second, third, first)
    elif mix==4:
        partition=(third, first, second)
    elif mix==5:
        partition=(third, second, first)

    permutationToObserveBigSets=convert_to_item_permutation(item_permutation[0:(numItemsInPartition)], itemFlips,partition)
    permutationToObserveNotBigSets=[]
    for ele in range(0, exhaustiveEndingLength):
        globalCount=(numItemsInPartition)+ele
        thisFlip=random.randint(0,5)
        if thisFlip==0:
            permutationToObserveNotBigSets.append(ItemPY3DBP(item_permutation[globalCount].name,item_permutation[globalCount].xDim, item_permutation[globalCount].yDim,item_permutation[globalCount].zDim))
        elif thisFlip==1:
            permutationToObserveNotBigSets.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].xDim, item_permutation[globalCount].zDim, item_permutation[globalCount].yDim))
        elif thisFlip==2:
            permutationToObserveNotBigSets.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].yDim, item_permutation[globalCount].xDim, item_permutation[globalCount].zDim))
        elif thisFlip==3:
            permutationToObserveNotBigSets.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].yDim, item_permutation[globalCount].zDim, item_permutation[globalCount].xDim))
        elif thisFlip==4:
            permutationToObserveNotBigSets.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].zDim, item_permutation[globalCount].xDim, item_permutation[globalCount].yDim))
        elif thisFlip==5:
            permutationToObserveNotBigSets.append(ItemPY3DBP(item_permutation[globalCount].name, item_permutation[globalCount].zDim, item_permutation[globalCount].yDim, item_permutation[globalCount].xDim))
        else:
            raise Exception("bug in BigSets testing")

    # concatenation
    permutationToObserve=permutationToObserveBigSets+permutationToObserveNotBigSets
    assert(len(permutationToObserve)==len(item_permutation))

    mixer=DimensionalMixupBigSetsGeneratorWithExhaustiveEnds(item_permutation,exhaustiveEndingLength)
    mixer.expectedList=permutationToObserveBigSets
    permutationObserved=False
    while(True):
        try:
            res=mixer.next()
            assert(len(res)==len(item_permutation))
            foundIt=True
            # check if all the items are equal
            for index in range(0, len(res)):
                if not permutationToObserve[index].name==res[index].name:
                    foundIt=False
                if not permutationToObserve[index].xDim==res[index].xDim:
                    foundIt=False
                if not permutationToObserve[index].yDim==res[index].yDim:
                    foundIt=False
                if not permutationToObserve[index].zDim==res[index].zDim:
                    foundIt=False
            if foundIt:
                permutationObserved=True
                break
        except StopIteration:
            break
    assert(permutationObserved)


def test_base_6_switches():
    import random
    numItems=random.randint(1,7)
    items=[ItemPY3DBP('unit',1,1,1) for ele in range(0, numItems)]
    d=DimensionalMixupsGenerator(items)
    switchesToFind=[random.randint(0,5) for ele in range(0, numItems)]
    while(True):

        try:
            d.next()
            switchesFound=d.base_6_as_switches(d.count, len(items))
            found=True
            for index in range(0, len(switchesFound)):
                if switchesFound[index]==switchesToFind[index]:
                    pass
                else:
                    found=False
                    break
            if found:
                break
        except StopIteration:
            raise Exception('unfound base 6 switch')

          
for ele in range(0, 100000):
    test_3_partition()
    test_2_partition()
    test_base_6_switches()


    #test_3_partition_with_exhaustive_ending()
    print(ele)
