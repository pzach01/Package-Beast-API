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
    
# computationally intensive; could replace with probalistic algorithm but have no gurantee of squares actually fitting together
def edges_intersect(newShape, oldShape):

    
    
    # reversed is used so that planes that are close to each other are used
    planesA, planesB=construct_planes(newShape), construct_planes(oldShape)
    # 6 * 6 = 36; this is done for each shape currently loaded in (factorial combinations) so gets huge fast
    
    # clear optimization in practice
    planesA,planesB=[plane for plane in planesA if plane not in planesB], ([plane for plane in planesB if plane not in planesA])

    for plane1 in planesA:
        for plane2 in planesB:
            if(planes_intersect(plane1, plane2)):
                return True
    return False

def new_is_valid_corner_point(bounds, existingShapes,newShape):
    # new shape must be strictly within bounds
    if strictly_within(bounds, newShape):
        
        
        
        # old code
        for oldShape in existingShapes:
            ### keep checking the list if this newShape is strictly outside oldShape
            if(same_shape(newShape, oldShape)):
                return False
            if(not (no_corner_points_inside(newShape, oldShape) and no_corner_points_inside(oldShape, newShape))):
                return False
            if(edges_intersect(newShape, oldShape)):
                return False
            
            
            

            
        return True
    else:
        return False        


def new_code():
    sameShape=True
    for element in oldShape:
        if element in newShape:
            pass
        else:
            sameShape=False
    if(sameShape):
        return False  
    
    

newShape=[(0.0,0.0,4.0), (0.0,0.0,9.0),
          (0.0,6.0,4.0), (0.0,6.0,9.0),
          (9.0,0.0,4.0), (9.0,0.0,9.0),
          (9.0,6.0,4.0), (9.0,6.0,9.0)]

oldShape=[(0.0,0.0,0.0),(0.0,0.0,4.0),
          (0.0,6.0,0.0),(0.0,6.0,4.0),
          (10.0,0.0,0.0),(10.0,0.0,4.0),
          (10.0,6.0,0.0),(10.0,6.0,4.0)]
b1=edges_intersect(newShape,oldShape)
b2=edges_intersect(oldShape,newShape)


p1=[(9.0,0.0,0.0),(9.0,0.0,5.0),(9.0,6.0,0.0),(9.0,6.0,5.0)]
p2=[(0.0,0.0,4.0),(0.0,6.0,4.0),(10.0,0.0,4.0),(10.0,6.0,4.0)]
# true
planes_intersect(p1,p2)


# should return false
p3=[(9.0,0.0,4.0), (9.0,0.0,9.0), (9.0,6.0,4.0), (9.0,6.0,9.0)]
p4=[(0.0,0.0,0.0), (0.0,6.0,0.0), (10.0,0.0,0.0), (10.0,6.0,0.0)]
planes_intersect(p3,p4)