bins=['100x100x100']
boxes=['20x12x8', '18x12x10', '30x30x30', '40x40x40']

import Box_Stuff_Python3_Only.box_stuff2 as bp
timeout=3
apiObjects=bp.master_calculate_optimal_solution(bins,boxes,timeout)
'''
for apiObject in apiObjects:
    print(apiObject.to_string())
''' 
    
allTheDictionarys=[]
for apiObject in apiObjects:
    allTheDictionarys.append(apiObject.to_dictionary())
print(allTheDictionarys)
# convert one bin to json
import json
jsonExample=json.dumps(allTheDictionarys[0])

# I think it is good to seperate backend and frontend things so there are two seperate method calls so we only have to change one down the road 
# there will be several null attributes in the default call. Wanted this here even though its unused so don't have to redo string formatting



