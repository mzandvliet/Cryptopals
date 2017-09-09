import codecs
import binascii

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

if __name__ == '__main__':
    lineA = "this is a test"
    lineB = "wokka wokka!!!"

    lineA = bytearray(lineA.encode('utf-8'))
    lineB = bytearray(lineB.encode('utf-8'))

    print(distHamming(lineA, lineB))

    file = open("data/6.txt", "r")
    for keysize in range(2, 40):
        print("\nKey Size: %s"%(keysize))
        file.seek(0,0)
        bytes = file.read(keysize * 2)
        while bytes != "":
            bytesA = strToByteArray(bytes[:keysize])
            bytesB = strToByteArray(bytes[keysize:])
            if (len(bytesA) != len(bytesB)):
                print("Early out, not enough text to feed hamming")
                break
            print(distHamming(bytesA, bytesB))
            bytes = file.read(keysize * 2)

    file.close()

    """
    # experiment with bitshift/bitmask for hamming functino
    charA = ord("a")
    charB = ord("b")

    diffBits = 0
    for i in range(8):
        shiftedA = charA >> i
        shiftedB = charB >> i
        maskedA = shiftedA & 0x1
        maskedB = shiftedB & 0x1
        if maskedA != maskedB: diffBits += 1
    print(diffBits)
    """

# ==========================================================================

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

    # we forgot to decode base64 first
    # should we perhaps first read in the entire file, base64 decode that, then loop?

    for keysize in range(2, 40):
        file.seek(0,0)
        bytes = file.read(keysize * 2)
        bytes = base64.b64decode(bytes) # Todo: hmmmmm
        count = 0
        totalDist = 0
        
        while bytes != "":
            bytesA = bytes[:keysize]
            bytesB = bytes[keysize:]
            if (len(bytesA) != len(bytesB)):
                break
            count += 1

            totalDist += distHamming(bytesA, bytesB)
            bytes = file.read(keysize * 2)

        print("\nKey Size: %s, avg norm dist: %s"%(keysize, totalDist/(count * keysize)))

    file.close()

# ==================================================================

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

    # we forgot to decode base64 first
    # should we perhaps first read in the entire file, base64 decode that, then loop?

    text = base64.b64decode(file.read())
    file.close()

    for keysize in range(2, 40):
        count = 0
        totalDist = 0
        
        for i in range(0, len(text), keysize*2):
            bytesA = text[i:i+keysize]
            bytesB = text[i+keysize:i+keysize*2]
            if (len(bytesA) != len(bytesB)):
                break
            count += 1

            totalDist += distHamming(bytesA, bytesB)

        print("\nKey Size: %s, avg norm dist: %s"%(keysize, totalDist/(count * keysize)))