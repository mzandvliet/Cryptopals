import codecs
import binascii
import base64
from functools import reduce

""" 
# plaintext has been put through:
1. repeat-key xor
2. base64

# we don't know key length. We also don't know char range.

# create a fun dist_hamming, which returns number of different bits between two (equal len) strings


Todo: It'll be interesting to convert this code to numpy and/or tensorflow later
"""

def strToByteArray(str):
    return bytearray(str.encode('utf-8'))

def byteArrayToStr(bytes):
    return ''.join(chr(i) for i in bytes)

def distHamming(lineA, lineB):
    """
    Hamming distance
    Input: two bytearrays of equal length
    Output: number of differing bits
    """
    if len(lineA) != len(lineB): raise ValueError("lineA and lineB need to be same length")

    diffBits = 0
    for i in range(len(lineA)):
        a = lineA[i]
        b = lineB[i]

        for i in range(8):
            shiftedA = a >> i
            shiftedB = b >> i
            maskedA = shiftedA & 0x1
            maskedB = shiftedB & 0x1
            if maskedA != maskedB: diffBits += 1

    return diffBits

def testHamming():
    lineA = "this is a test"
    lineB = "wokka wokka!!!"

    lineA = bytearray(lineA.encode('utf-8'))
    lineB = bytearray(lineB.encode('utf-8'))

    assert(distHamming(lineA, lineB) == 37)

def xor_single_char(bytes, char):
    result = []
    for i in range(len(bytes)):
        result.append(bytes[i] ^ char)
    return bytearray(result)

def rate_englishness(bytes):
    garbage_count = 0
    for i in bytes:
        if is_garbage(i):
            garbage_count+=1
    return len(bytes)-garbage_count

def is_garbage(byte):
    if byte == 32: return False #space
    if byte >= 65 and byte <= 90: return False #uppercase
    if byte >= 97 and byte <= 122: return False #lowercase
    return True

def most_likely_keychar(bytes):
    """
    returns (key, keyscore)
    """
    key = None
    key_score = 0
    for char in range(255):
        decoded = xor_single_char(bytes, char)
        score = rate_englishness(decoded)
        if score > key_score: # note: multiple keys with same good score possible
            key = char
            key_score = score

    return (key, key_score)

def rotXor(bytes, key):
    return [bytes[i] ^ key[i % len(key)] for i in range(len(bytes))]

if __name__ == '__main__':
    testHamming()

    file = open("data/6.txt", "r")
    # Decided to b64decode entire file into memory first
    text = base64.b64decode(file.read())
    file.close()

    # Try all key sizes, compute average hamming norms
    candidateKeySizes = []
    for keysize in range(27, 31):
        count = 0
        totalDist = 0
        
        for i in range(0, len(text), keysize):
            bytesA = text[i:i+keysize]
            bytesB = text[i+keysize:i+keysize*2]
            if (len(bytesA) != len(bytesB)):
                break
            count += 1

            totalDist += distHamming(bytesA, bytesB)

        avgNormDist = totalDist/(count * keysize)
        candidateKeySizes.append((keysize, avgNormDist))
        
        print("Key Size: %s, avg norm dist: %s"%(keysize, avgNormDist))
    
    candidateKeySizes.sort(key=lambda tup:tup[1])

    print("Most likely key sizes:")
    for i in candidateKeySizes[:2]:
        print(" - %s, score: %s"%(i[0], i[1]))

    candidateKeySizes = candidateKeySizes[:2]

    candidate_keys = []
    for candidate in candidateKeySizes:
        keysize = candidate[0]
        blocks = [[] for i in range(keysize)]
        for i in range(0, len(text)):
            blocks[i%keysize].append(text[i])

        keyChars = []
        for block in blocks:
            keyChars.append(most_likely_keychar(block))
        key = []
        keyScore = 0 # todo: as comprehension
        for i in keyChars:
            key.append(i[0])
            keyScore += i[1]

        candidate_keys.append((key, keyScore))

    candidate_keys.sort(key=lambda tup:tup[1], reverse=True)
    
    for key in candidate_keys:
        print("key: %s, score: %s"%(byteArrayToStr(key[0]), key[1]))

    key = candidate_keys[0][0]
    decryptedBytes = rotXor(text, key)
    decrypted_str = byteArrayToStr(decryptedBytes)

    print("Done! Message: \n")
    print(decrypted_str)

    
