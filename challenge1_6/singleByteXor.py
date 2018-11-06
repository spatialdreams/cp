#####################################################################################
#   Takes a hex string and XORs it against the ascii character range. Ranks the     #
# results depending on presence of characters and the absence of special characters.#
#####################################################################################
import sys
import string
import conversions as convert

arange=["{0:b}".format(i).zfill(8) for i in range(128)]

#additional output if true
debug=0

#XOR each input byte vs each comparitor byte
def compare(bytesarray,comparitors=arange):
  binoutputs=[]
  for x in comparitors:
    binoutput=[]
    for y in bytesarray:
      byteout=''
      for e,z in enumerate(y):
        if z != x[e%8]:
          byteout+='1'
        else:
          byteout+='0'
      if debug > 1:
        print('xor {} vs {} equals {}'.format(x,y,byteout))
      binoutput.append(byteout)
    binoutputs.append((x,binoutput))
  return binoutputs

#try to convert result to ascii. Abscond if not UTF.
def outputToAscii(bytearray):
  asciioutput=''
  for x in bytearray:
    try:
      asciioutput+=convert.b2a(str.encode(x))
    except:
      if debug > 1:
        print(x,'cannot be converted to UTF')
  if len(asciioutput)==len(bytearray):
    return (asciioutput)
  else:
    if debug:
      print("Decode error from",bytearray,"This isn't utf. Omitting from results.")

#score the results 
specialCharacters=['/','^','\\','@','+','~','%','{','}','[',']','|','`','<','>','=',]
def score(text):
  newScore=0
  for x in text:
    if x in string.ascii_letters[:26]:
      newScore+= 3
    if x in string.ascii_letters[26:52]:
      newScore+= 2
    elif x in specialCharacters:
      newScore+= -2
    elif x==' ':
      newScore+= 1
    else:
      newScore+= 0
  return newScore


def main(input,datatype,comparitors=arange):
  #if input is hex, convert it to binary bytes.
  if datatype=='hex':
    input=convert.h2b(input)
  bytes=[input[x*8:x*8+8] for x in range(int(len(input)/8))]
  if debug:
    print('Input as bytes:',bytes,'\nComparitors:',comparitors)

  #compare bytes
  binoutputs=compare(bytes,comparitors)
  
  #convert byte arrays to ascii and abandon nonvalid answers.
  asciioutputs=[]
  for item in binoutputs:
    asciioutputs.append([convert.b2a(item[0]),outputToAscii(item[1])])
  
  #score all results that produces valid ascii, if any. 
  if len(asciioutputs) > 0:
    for item in asciioutputs:
      item.append(score(item[1]))
      if debug:
        print('comparitor:',item[0],'resulting string:',item[1],' Score:',item[2])
  else:
    print('No valid utf-8 results from',input)

  #return the winner(s)
  winners=[]
  bigboi=0
  for x in asciioutputs:
    if x[2] > bigboi:
      bigboi=x[2]
  for x in asciioutputs:
    if x[2] == bigboi:
      if bigboi > 0:
        winners.append(x[:2])
  print('SBX Returned winner(s):{}'.format(list(x[0] for x in winners)),'from this input')
  return winners

#run this script with arg1 if called from terminal 
#but don't run if imported from another script
if len(sys.argv) > 1:
  main(sys.argv[1],'hex')
