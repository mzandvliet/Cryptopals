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

def xorSingleChar(bytes, char):
    """
    XORs all input bytes with a single key char
    Input: bytearray text
    Output: XORed bytearray text
    """
    result = []
    for i in range(len(bytes)):
        result.append(bytes[i] ^ char)
    return bytearray(result)

def rateEnglish(bytes):
    """
    Gives a score indicating how much the input bytearray chars resemble english
    Higher is more likely to be written text, lower is more likely to be garbage
    Input: bytearray text
    Output: int score
    """
    garbage_count = 0
    for i in bytes:
        if isGarbageChar(i):
            garbage_count+=1
    return len(bytes)-garbage_count

def isGarbageChar(byte):
    """
    Indicates whether this char is likely to be garbage or english
    """
    if byte == 32: return False #space
    if byte >= 65 and byte <= 90: return False #uppercase
    if byte >= 97 and byte <= 122: return False #lowercase
    return True

def MostLikelyKeySingleChar(bytes):
    """
    Finds most likely key character, assuming that input is XOR encrypted with a single key char
    returns (key, keyscore)
    """
    key = None
    key_score = 0
    for char in range(255):
        decoded = xorSingleChar(bytes, char)
        score = rateEnglish(decoded)
        if score > key_score: # note: multiple keys with same good score possible
            key = char
            key_score = score

    return (key, key_score)

def encodeRepeatXor(bytes, key):
    """
    Encodes input bytearray with given key of arbitrary size
    returns bytearray of encoded characters
    """
    return [bytes[i] ^ key[i % len(key)] for i in range(len(bytes))]

if __name__ == '__main__':
    testHamming()

    # b64decode entire message into memory first
    message = ''
    with open("data/6.txt", "r") as file:
        message = base64.b64decode(file.read())

    # Try many key sizes, compute average Hamming norms by comparing distance
    # between every two keysize char blocks of the message
    # Likely key sizes should show lower average Hamming norm

    print("\nComputing Hamming norms for range of potential key sizes...\n")

    candidateKeySizes = []
    for keySize in range(2, 40):
        pairCount = 0
        hammingSum = 0
        
        for i in range(0, len(message), keySize):
            partA = message[i:i+keySize]
            partB = message[i+keySize:i+keySize*2]
            if (len(partA) != len(partB)):
                break
            pairCount += 1

            hammingSum += distHamming(partA, partB)

        avgHamming = hammingSum/(pairCount * keySize)
        candidateKeySizes.append((keySize, avgHamming))
        
        print("Key Size: %s, Average normal distance: %s"%(keySize, avgHamming))
    
    # Sort most likely key sizes, take top N

    candidateKeySizes.sort(key=lambda tup:tup[1])
    candidateKeySizes = candidateKeySizes[:4]

    print("\nMost likely key sizes found:\n")
    for i in candidateKeySizes:
        print(" - %s, score: %s"%(i[0], i[1]))

    # For each likely key size, split message into lists per key-char

    print("\nSearching for keys...\n")

    candidate_keys = []
    for candidate in candidateKeySizes:
        keySize = candidate[0]
        blocks = [[] for i in range(keySize)]
        for i in range(0, len(message)):
            blocks[i%keySize].append(message[i])

        # Find the most likely single char for each part of the key

        keyChars = []
        for block in blocks:
            keyChars.append(MostLikelyKeySingleChar(block))

        # Combine results to create whole key, and aggregate single-char scores into an average
        # score for that whole key

        key = []
        keyScore = 0 # todo: as comprehension
        for i in keyChars:
            key.append(i[0])
            keyScore += i[1]

        candidate_keys.append((key, keyScore))

    # sort potential keys by score

    candidate_keys.sort(key=lambda tup:tup[1], reverse=True)

    print("\nMost likely keys found:\n")
    for key in candidate_keys:
        print("key: %s, score: %s"%(byteArrayToStr(key[0]), key[1]))

    # take the most likely key and decrypt the message

    key = candidate_keys[0][0]
    decryptedBytes = encodeRepeatXor(message, key)
    decrypted_str = byteArrayToStr(decryptedBytes)

    print("\nDone! Message: \n")
    print(decrypted_str)

    
