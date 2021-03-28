

# returns True if a shape has a vertex within the other
def vertices_inside(minItem1,maxItem1, item2):
    ## all extreme points are within bounds
    for point in item2:
        if minItem1[0]<point[0]<maxItem1[0]:
            if minItem1[1]<point[1]<maxItem1[1]:
                if minItem1[2]<point[2]<maxItem1[2]:
                    return True
    return False


def objects_intersect_fast(item1Min, item1Max, item2Min, item2Max):
    for dimension in range(0,3):
        #axises=[min1[dimension],max1[dimension],min2[dimension],max2[dimension]]
        # generate axises so it is unique
        axises=[item1Min[dimension]]
        if item1Max[dimension] not in axises:
            axises.append(item1Max[dimension])
        if item2Min[dimension] not in axises:
            axises.append(item2Min[dimension])
        if item2Max[dimension] not in axises:
            axises.append(item2Max[dimension])

        # check if its splits em
        for axis in axises:
            if (item1Max[dimension]<=axis<=item2Min[dimension]):
                return False
            if (item2Max[dimension]<=axis<=item1Min[dimension]):
                return False
    return True




# use PAT instead of being a retard and wasting 2 months of your life
def objects_intersect(item1, item2):
    # can't have points nested within each other

    # already sorted here
    minItem1, maxItem1=item1[0],item1[7]
    minItem2, maxItem2=item1[0],item2[7]
    # NEED TO CHECK item2's axises as well 


    # check if any of item1's axises split the shapes
    for dimension in range(0,3):
        #axises=[min1[dimension],max1[dimension],min2[dimension],max2[dimension]]
        # generate axises so it is unique
        axises=[minItem1[dimension]]
        if maxItem1[dimension] not in axises:
            axises.append(maxItem1[dimension])
        if minItem2[dimension] not in axises:
            axises.append(minItem2[dimension])
        if maxItem2[dimension] not in axises:
            axises.append(maxItem2[dimension])

        # check if its splits em
        for axis in axises:
            split=True
            # the index here doesn't matter at all, could both be random
            firstPointItem1=item1[0]
            firstPointItem2=item2[0]
            if (firstPointItem1[dimension]<=axis<=firstPointItem2[dimension]):
                for point in item1:
                    if axis<point[dimension]:
                        split=False
                        break
                if not split:
                    continue
                for point in item2:
                    if axis>point[dimension]:
                        split=False
                        break

                if split:
                    return False

        for axis in axises:
            split=True
            if (firstPointItem2[dimension]<=axis<=firstPointItem1[dimension]):
                for point in item1:
                    if axis>point[dimension]:
                        split=False
                        break
                if not split:
                    continue
                for point in item2:
                    if axis<point[dimension]:
                        split=False
                        break
                if split:
                    return False
    return True
    # if we can find an axis that splits the cubes  (view in 2d) then they don't intersect