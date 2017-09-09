import codecs
import binascii

def xor(bytes, value):
    result = []
    for i in range(len(bytes)):
        result.append(bytes[i] ^ value)
    return bytearray(result)

# ascii a-z characters are 97-122, or 0x61-0x7a
# capitals, spaces
# if many characters outside that range, consider it garbage
def englishness(bytes):
    count = 0
    for i in bytes:
        if is_garbage(i):
            count+=1
    return len(bytes)-count

def is_garbage(byte):
    if byte == 32: return False #space
    if byte >= 65 and byte <= 90: return False #uppercase
    if byte >= 97 and byte <= 122: return False #lowercase
    return True



input = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
print(input)

bytes = codecs.decode(input, 'hex')

candidates = []
for i in range(255):
    decoded = xor(bytes, i)
    score = englishness(decoded)
    if score > 20:
        decoded_string = ''.join(chr(i) for i in decoded)
        candidates.append((score, decoded))

candidates.sort(key = lambda tup: tup[0])

for i in range(len(candidates)):
    print(candidates[i][1]) # last one printed is most likely

"""
bytes = xor(bytes, 3)
print(binascii.hexlify(bytearray(bytes)))
bytes = xor(bytes, 3)
print(binascii.hexlify(bytearray(bytes)))
"""

