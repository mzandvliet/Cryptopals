import codecs
import binascii
import base64

""" 
# plaintext has been put through:
1. repeat-key xor
2. base64

# we don't know key length. We also don't know char range.

# create a fun dist_hamming, which returns number of different bits between two (equal len) strings
"""

def strToByteArray(str):
    return bytearray(str.encode('utf-8'))

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

if __name__ == '__main__':
    testHamming()

    file = open("data/6.txt", "r")
    # Decided to b64decode entire file into memory first
    text = base64.b64decode(file.read())
    file.close()

    # Try all key sizes, compute average hamming norms
    candidate_sizes = []
    for keysize in range(2, 40):
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
        candidate_sizes.append((keysize, avgNormDist))
        
        print("Key Size: %s, avg norm dist: %s"%(keysize, avgNormDist))

    candidate_sizes.sort(key=lambda tup:tup[1])

    print("Most likely key sizes:")
    for i in candidate_sizes[:5]:
        print(" - %s, score: %s"%(i[0], i[1]))