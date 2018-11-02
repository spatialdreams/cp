#Tries to find the keysize of a string encrypted with a repeating key by 
#averaging the hamming distance between sequential segments of an input file. 
#Min/max values are the lowest/highest amount of bytes to iterate through. We 
#take the 5 lowest scoring keysizes and try to decrypt the file by XORing each 
#key segment against the 127 ascii character space. Finally we rank the 
#results based on character frequency and absence of special characters.
import os  
import sys 
import json 
import pprint
import hamming
import singleByteXor as sbx 
import conversions as convert 
from io import BytesIO,StringIO
termwidth=os.get_terminal_size()[0] 
pp=pprint.PrettyPrinter(width=termwidth)

debug=0

data=[] 
def getHDaverages(bits,minbytes=1,maxbytes=40,sequences=4):
  for seqnumber in range(sequences):
    data.append([])
    for bytelength in range(minbytes,maxbytes+1):
      bytelength=bytelength*8
      start=seqnumber*bytelength
      end=start+bytelength
      a=bits[start:end]
      b=bits[start+end:end*2]

      hdistance=hamming.getDistance(a,b)
      data[seqnumber].append([bytelength,round(hdistance,3)])
      if debug > 1:
        print(convert.b2h(a),'vs', convert.b2h(b),'\ndistance:',hdistance)
    if debug:
      print('Pass',seqnumber+1,'[keylengh, hamming distance]')
      pp.pprint(data[seqnumber])

  averages=[]
  for y in range(len(data[seqnumber])):
    average=0
    for x in range(sequences):
      average+=data[x][y][1]
    averages.append(round(average/sequences,3))
  averages={n+minbytes:x for n,x in enumerate(averages)}
  return averages

#takes a string and an array of keylengths.
def breakApart(bits,keylengths):
  sequences=[]
  for kl in keylengths:
    newBits=bits
    s=StringIO(newBits)
    bitseqs=[''*naught for naught in range(kl)]
    i=0
    while True:
      i=i%kl
      chunk=s.read(8)
      if len(chunk) > 0:
        bitseqs[i]+=(chunk)
        i+=1
      if len(chunk) < 8:
        break
    sequences.append([kl,bitseqs])
  return sequences

def main(file,minbytes,maxbytes,sequences):
  with open(file,'r') as infile:
    filedata=infile.read().replace('\n','')

  #convert file to binary
  bits=convert.b64tobin(str.encode(filedata))
  #get the average hamming distances between variable length sequences
  print('Getting average byte distance between sequences from',pinput[0])
  averages=getHDaverages(bits,minbytes,maxbytes,sequences)
  #get 5 byte lengths with the lowest average hamming distance between them
  keylengths5=[x[0] for x in (sorted(averages.items(), key=lambda kv: kv[1])[:5])]
  print('The keylengths with the 5 lowest distances are:', keylengths5)
  #transpose into array of sequential bytes one keylength away from the previous byte.
  sequences=breakApart(bits,keylengths5)
  #Run sequences through our Single Byte Xor scoring sytem. Adds results to the list of possibilities.
  possibilities={}
  for data in sequences:
    for e,bytearray in enumerate(data[1]): 
      print('keylength:',data[0],'sequence:',e,'start of seq:',bytearray[:20]+'...')
      if data[0] in possibilities:
        possibilities[data[0]].append(sbx.main(bytearray,'bits'))
      else:
        possibilities[data[0]]=[]
        possibilities[data[0]].append(sbx.main(bytearray,'bits'))

  #write possibilities to file so we can look at it manually.
  with open('outfile.txt','w') as outfile: 
   outfile.write(json.dumps(possibilities))
   print('wrote output to outfile.txt')

  #reconstruct sequences
  for key in possibilities:
    passphrase=''
    outputarray=[]
    outputstring=''
    for sequence in possibilities[key]:
      passphrase+=sequence[0][0]
      outputarray.append(sequence[0][1])
    osrs=[y for x in zip(*outputarray) for y in x]
    for character in osrs:
      outputstring+=character
    print('Keylength:',key,'Passphrase: "'+passphrase+'" Resulting string:\n'+outputstring)
    swc=input('\nDoes this seem correct?')

#run script with arguments if called from terminal but not if imported from 
#another script.
if sys.argv[0]==os.path.basename(__file__):
  pinput=['6_b64.txt',3,40,4]
  for x in range(1,len(sys.argv)):
    pinput[x-1]=sys.argv[x]
  main(pinput[0],pinput[1],pinput[2],pinput[3]) 
