####################################################################################
#  outputs the number of different positional bits between two binary input values #
####################################################################################
def getDistance(bitset1, bitset2):
  if len(bitset1) != len(bitset2):
    raise ValueError('Positional arguments must be of equal length')
  distance=0
  for e,i in enumerate(bitset1):
    if i != bitset2[e]:
      distance+=1
  distance=distance/len(bitset1)
  return distance
