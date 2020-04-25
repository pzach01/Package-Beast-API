import itertools
import package
from package import Package
import box_stuff1
from box_stuff1 import slot_bin_with_coordinates
p1=Package('3x2x3')
listy=[p1 for ele in range(0,6)]

bin=Package('12x3x3')
allArrangments=(itertools.permutations(listy,len(listy)))
boxArrangment=allArrangments.next()
coordinateDict=slot_bin_with_coordinates(boxArrangment,bin)