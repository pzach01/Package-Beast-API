

# returns True if a shape has a vertex within the other
def vertices_inside(item1, item2):
    ## all extreme points are within bounds
    min1, max1=item1[0],item1[7]
    for point in item2:
        if min1[0]<point[0]<max1[0]:
            if min1[1]<point[1]<max1[1]:
                if min1[2]<point[2]<max1[2]:
                    return True
    return False







# use PAT instead of being a retard and wasting 2 months of your life
def objects_intersect(item1, item2):
    # can't have points nested within each other
    if(vertices_inside(item1, item2) or vertices_inside(item2, item1)):
        return True
    # already sorted here
    min1, max1=item1[0],item1[7]
    min2, max2=item1[0],item2[7]
    # NEED TO CHECK item2's axises as well 


    # check if any of item1's axises split the shapes
    for dimension in range(0,3):
        #axises=[min1[dimension],max1[dimension],min2[dimension],max2[dimension]]
        # generate axises so it is unique
        axises=[min1[dimension]]
        if max1[dimension] not in axises:
            axises.append(max1[dimension])
        if min2[dimension] not in axises:
            axises.append(min2[dimension])
        if max2[dimension] not in axises:
            axises.append(max2[dimension])

        # check if its splits em
        for axis in axises:
            split=True
            seen=False
            # the index here doesn't matter at all, could both be random
            firstPointItem1=item1[0]
            firstPointItem2=item2[0]
            if (firstPointItem1[dimension]<=axis<=firstPointItem2[dimension]):
                seen=True
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

            if split and seen:
                return False

        for axis in axises:
            split=True
            seen=False
            if (firstPointItem2[dimension]<=axis<=firstPointItem1[dimension]):
                seen=True
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
            if split and seen:
                return False
    return True
    # if we can find an axis that splits the cubes  (view in 2d) then they don't intersect