import base64

#ascii to bin and back, with short links.
def asciiToBin(text, encoding='utf-8', errors='surrogatepass'):
  bits = bin(int.from_bytes(text.encode(encoding,errors),'big'))[2:]
  return bits.zfill(8 * ((len(bits) + 7) //8))
def a2b(text, encoding='utf-8', errors='surrogatepass'):
  return asciiToBin(text, encoding, errors)

def binToAscii(bits, encoding='utf-8', errors='surrogatepass'):
  n = int(bits,2)
  return  n.to_bytes((n.bit_length()+7) // 8, 'big').decode(encoding,errors) or '\0'
def b2a(bits, encoding='utf-8', errors='surrogatepass'):
  return binToAscii(bits, encoding, errors)

#hex to bin and back, with short links.
def hexToBin(data):
  bindata=''
  for x in data:
    bindata+=bin(int(x,16))[2:].zfill(4)
  return bindata
def h2b(data):
  return hexToBin(data)

def binToHex(bits):
  return hex(int(bits,2))[2:]
def b2h(bits):
  return binToHex(bits)

#b64 to bin and back
def b64tobin(data):
  decoded=base64.decodebytes(data)
  return "".join(["{:08b}".format(x) for x in decoded])

#add 'bin to b64' when we need it
