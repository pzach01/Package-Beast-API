'''

                pivot = [0, 0, 0]
                # 3 'bit' string in base 3 yields 27 combinations
                # 1st 'bit'= +, -, or no addition
                # 2nd 'bit' =+, -, or no addition
                # 3rd 'bit' =+, -, or no addition 
                # not sure if this line is neccessary
                axisCopy=axis
                firstBit=axisCopy//(3**2)
                axisCopy=axisCopy%(3**2)
                secondBit=axisCopy//(3**1)
                axisCopy=axisCopy%(3**1)
                thirdBit=axisCopy
                firstValue=[0 if firstBit==0 else 1 if firstBit==1 else -1][0]
                secondValue=[0 if secondBit==0 else 1 if secondBit==1 else -1][0]
                thirdValue=[0 if thirdBit==0 else 1 if thirdBit==1 else -1][0]
                pivot=[
                    currentItem.position[0]+firstValue*currentItem.width,
                    currentItem.position[1]+secondValue*currentItem.height,
                    currentItem.position[2]+secondValue*currentItem.depth
                ]
'''


'''

axis=21
axisCopy=axis
firstBit=axisCopy//(3**2)
axisCopy=axisCopy%(3**2)
secondBit=axisCopy//(3**1)
axisCopy=axisCopy%(3**1)
thirdBit=axisCopy
print(firstBit)
print(secondBit)
print(thirdBit)
firstBit=1
firstValue=[0 if firstBit==0 else 1 if firstBit==1 else -1][0]
print(firstValue)
'''




#import Box_Stuff_Python3_Only.testing_multipack
#print("Passed regular tests")

#import Box_Stuff_Python3_Only.testing_single_pack as spt
#print("Passed single pack tests")

import Box_Stuff_Python3_Only.testing_rendering as rt

#import Box_Stuff_Python3_Only.testing_underfitting as ut

# testing