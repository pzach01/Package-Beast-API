

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




def get_min_max_tuple(extremePoints):
    
    minX,minY,minZ=extremePoints[0][0],extremePoints[0][1],extremePoints[0][2]
    maxX,maxY,maxZ=extremePoints[0][0],extremePoints[0][1],extremePoints[0][2]
    for extremePoint in extremePoints:
        if(extremePoint[0]<minX):
            minX=extremePoint[0]
        if(extremePoint[0]>maxX):
            maxX=extremePoint[0]
        if(extremePoint[1]<minY):
            minY=extremePoint[1]
        if(extremePoint[1]>maxY):
            maxY=extremePoint[1]
        if(extremePoint[2]<minZ):
            minZ=extremePoint[2]
        if(extremePoint[2]>maxZ):
            maxZ=extremePoint[2]
        
    return (minX,minY,minZ), (maxX,maxY,maxZ)
    
# returns if newShape and oldShape are the same shape in the same position
def same_shape(newShape, oldShape):
    sameShape=True
    for element in oldShape:
        if element in newShape:
            pass
        else:
            sameShape=False
    return sameShape

# returns if oldShape has all extreme points outside new shape. Different then (not (strictly_within(...)) because no_corner_points_inside(...) is a less permissive policy. 
def no_corner_points_inside(newShape, oldShape):
    min, max=get_min_max_tuple(newShape)
    for point in oldShape:
        if(min[0] < point[0] < max[0]):
            if(min[1]< point[1] <max[1]):
                if(min[2]< point[2] < max[2]):
                    return False
    return True

# assumes shape is sorted, allows us to use a speedup so we dont have to find the adjacent points but can just use an indexing technique O(1) vs O(n^2) to find
# this looks very odd though, but remember, per generate_extreme_points()
'''
p1=(lowerHeight,lowerWidth, lowerLength)
p2=(lowerHeight,lowerWidth, upperLength)
p3=(lowerHeight, upperWidth, lowerLength)
p4=(lowerHeight, upperWidth, upperLength)
p5=(upperHeight,lowerWidth, lowerLength)
p6=(upperHeight,lowerWidth, upperLength)
p7=(upperHeight, upperWidth, lowerLength)
p8=(upperHeight, upperWidth, upperLength)    
'''
### returns if a shape is strictly within bounds
def strictly_within(bounds, newShape):
    ## all extreme points are within bounds
    min, max=get_min_max_tuple(bounds)
    for extremePoint in newShape:
        if(not (extremePoint[0]>=min[0] and extremePoint[0]<=max[0])):
            return False
        if(not (extremePoint[1]>=min[1] and extremePoint[1]<=max[1])):
            return False
        if(not (extremePoint[2]>=min[2] and extremePoint[2]<=max[2])):
            return False
    
    
    return True





def construct_planes(shape):
    # same value for:lowerLength, upperLength, lowerWidth, upperWidth,lowerHeight, upperHeight
    planes=[[shape[0],shape[2],shape[4],shape[6]]
            ,[shape[1],shape[3],shape[5],shape[7]]
            ,[shape[0],shape[1],shape[4],shape[5]]
            ,[shape[2],shape[3],shape[6],shape[7]]
            ,[shape[0],shape[1],shape[2],shape[3]],
            [shape[4],shape[5],shape[6],shape[7]]]
    return planes

# so basically for a given plane, there are two two points that have the same value as a point on the other plane
# for two dimensions, and values at these points that is greater then the intersection point for one point and lesss 
# then the intersection for the other, the planes intersect
def planes_intersect(plane1, plane2):
    min1,max1=get_min_max_tuple(plane1)
    min2,max2=get_min_max_tuple(plane2)
    # get the dimension that stays the same
    plane1DimensionFixed=0 if min1[0]==max1[0] else 1 if min1[1]==max1[1] else 2
    plane2DimensionFixed=0 if min2[0]==max2[0] else 1 if min2[1]==max2[1] else 2
    
    # this could be max too, because min and max are equal in fixed dimension
    valueOfFixedDimension1=min1[plane1DimensionFixed]
    valueOfFixedDimension2=min2[plane2DimensionFixed]
    # planes are parrallel
    if(plane1DimensionFixed==plane2DimensionFixed):
        return False
    
    
    # both planes must have an intersection in this dimension
    sharedDimension=None
    for ele in [0,1,2]:
        if (ele is not plane1DimensionFixed) and (ele is not plane2DimensionFixed):
            sharedDimension=ele  
    # the planes intersect in the shared dimension
    # two mins then two maxes if possibility of intersection
    if(min1[sharedDimension]>=max2[sharedDimension] or min2[sharedDimension]>=max1[sharedDimension]):
        return False
    
    
    # is 'the + shape made'?, if so return True:
    # again min2 could be max2 in the first clause because the values are fixed in this dimension, same situation for min1 in second clause

    if(
        (
            (min2[plane1DimensionFixed]<min1[plane1DimensionFixed]<max2[plane1DimensionFixed]) or  (min2[plane1DimensionFixed]<max1[plane1DimensionFixed]<max2[plane1DimensionFixed])
            )
        and (
            (min1[plane2DimensionFixed]<min2[plane2DimensionFixed]<max1[plane2DimensionFixed]) or (min1[plane2DimensionFixed]<max2[plane2DimensionFixed]<max1[plane2DimensionFixed]))
        ):
        return True
    return False

# returns the FIRST plane that has this fixed index
def get_fixed_plane_index(planes, fixedDimension):
    index=0
    for plane in planes:
        
        # transitive property
        if((((plane[0][fixedDimension]==plane[1][fixedDimension]) and (plane[1][fixedDimension]==plane[2][fixedDimension])) and (plane[2][fixedDimension]==plane[3][fixedDimension]))):
            return index
        index+=1
  
  
# returns if planeA and planeB are 'sliding past each other', but not 
def weakly_parralel(planeA, planeB,fixedDimension):
    # they dont hold the same value for this dimension
    if (not (planeA[0][fixedDimension] == planeB[0][fixedDimension])):
        return False
    
    min1,max1=get_min_max_tuple(planeA)
    min2,max2=get_min_max_tuple(planeB)
    nonFixedDimensions=[0,1,2]
    nonFixedDimensions.remove(fixedDimension)
    
    lineIntersectionCount=0
    for dim in nonFixedDimensions:
        if (max1[dim]>=max2[dim]):
            if(min1[dim]<max2[dim]):
                lineIntersectionCount+=1
        else:
            if(min2[dim]<max1[dim]):
                lineIntersectionCount+=1
            
    if lineIntersectionCount==2:
        return True
    



# use PAT instead of being a retard and wasting 2 months of your life
def new_is_valid_corner_point_v2(item1, item2):
    # can't have points nested within each other
    if(vertices_inside(item1, item2) or vertices_inside(item2, item1)):
        return False
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
                return True

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
                return True
    return False
    # if we can find an axis that splits the cubes  (view in 2d) then they don't intersect