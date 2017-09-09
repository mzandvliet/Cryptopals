import codecs
import binascii

input_a = "1c0111001f010100061a024b53535009181c"
input_b = "686974207468652062756c6c277320657965"
bytes_a = codecs.decode(input_a, 'hex')
bytes_b = codecs.decode(input_b, 'hex')

xored = []
for i in range(len(bytes_a)):
    # xored.append((bytes_a[i] ^ bytes_b[i]).to_bytes(1, byteorder='big')) # forces byte result instead of int
    xored.append(bytes_a[i] ^ bytes_b[i]) # results in int list

#xored_string = ''.join(chr(i) for i in xored) # This produces readable chars from an int list, we want to print bytes
#xored_bytes = b''.join(xored) # works for an actual byte list
xored_bytes = binascii.hexlify(bytearray(xored)) # turns out using binascii.hexlify is easiest
print(xored_bytes)


