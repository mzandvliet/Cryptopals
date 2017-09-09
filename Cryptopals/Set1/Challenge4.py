import codecs
import binascii

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

def most_likely_candidate(bytes):
    result = None
    result_score = 0
    for char in range(255):
        decoded = xor_single_char(bytes, char)
        score = rate_englishness(decoded)
        if score > result_score:
            result = decoded
            result_score = score

    return (result_score, result)

def hex_bytes_to_str(bytes):
    return ''.join(chr(i) for i in bytes)

with open("data/4.txt", "r") as text:
    candidates = []
    for line in text:
        bytes = codecs.decode(line.strip(), 'hex')
        candidate = most_likely_candidate(bytes)
        candidates.append(candidate)
        print("%s, %s"%(candidate[0], hex_bytes_to_str(candidate[1])))
    candidates.sort(key=lambda tup: tup[0])
    print(candidates[len(candidates)-1])