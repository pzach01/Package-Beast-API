bins=['50x50x50']
'''
boxes=['10x6x4', 
'9x6x5', '15x15x15', 
'20x20x20']
'''
boxes=['10x10x10' for ele in range(0,80)]
import time
start=time.time()

import Box_Stuff_Python3_Only.box_stuff2 as bp
timeout=0
apiObjects=bp.master_calculate_optimal_solution(bins,boxes,timeout)
'''
for apiObject in apiObjects:
    print(apiObject.to_string())
''' 
end=time.time()

print(end-start)

allTheDictionarys=[]
for apiObject in apiObjects:
    allTheDictionarys.append(apiObject.to_dictionary())

# convert one bin to json
import json
jsonExample=json.dumps(allTheDictionarys[0])
# I think it is good to seperate backend and frontend things so there are two seperate method calls so we only have to change one down the road 
# there will be several null attributes in the default call. Wanted this here even though its unused so don't have to redo string formatting




# for a given plane, if there are two points
# that have the same value as a point on the other plane for two dimensions,
# and values at these points is greater then the
# intersection point for one point point and less then the intersection for the other,
# the plane intersect