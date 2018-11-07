#seqeuntial xor byte comparisons. input vs key.
import sys
debug=1

if len(sys.argv) < 2:
  print("You must supply at least one hex input")
  sys.exit()

if len(sys.argv) > 2:
  key = sys.argv[2]
else:
  key = 'ICE'

#hex to binary byte
def hexToBin(data):
  return bin(int(data,16))[2:].zfill(8)
#ascii to binary byte
def asciiToBin(data):
  return bin(int.from_bytes(data.encode(),'big'))[2:]
#Reverse, reverse!
def binToHex(data):
  return hex(int(data,2))[2:]
#2 hops this time
def binToAscii(data):
  data=int(data,2)
  return data.to_bytes((data.bit_length()+7)//8,'big').decode()

#for looping back to start of key at end of sequence LOL HAHA %
def radix(currentIteration,keyLength):
  if currentIteration < keyLength:
    return currentIteration
  else:
    divmod=currentIteration//keyLength
    number=currentIteration-divmod*keyLength
    return number

#sequentialXOR sys.argv[1] vs key
newkey=''
for i,x in enumerate(sys.argv[1]):
  newkey+=key[radix(i,len(key))]

databin=asciiToBin(sys.argv[1])
keybin=asciiToBin(newkey)

output=''
for i,x in enumerate(databin):
  if x != keybin[i]:
    output+='1'
  else:
    output+='0'

print("In : {} {} {}".format(databin, binToHex(databin), binToAscii(databin)))
print("Key: {} {} {}".format(keybin,binToHex(keybin), binToAscii(keybin)))
print("Out: {} {}".format(output,binToHex(output)))
