import codecs
import binascii

def encrypt_rot_xor(bytes, key):
    key_len = len(key)
    result = []
    for i in range(len(bytes)):
        result.append(bytes[i] ^ key[i%key_len])
    return result

# Note: this list interpretation does exactly the same as above
def list_interp_xor(bytes, key):
    return [bytes[i] ^ key[i % len(key)] for i in range(len(bytes))]

if __name__ == '__main__':
    # Note: It is really, really easy to mess up the string literal
    mes = '''Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal'''
    key = 'ICE'

    mes_bytes = mes.encode('utf-8')
    key_bytes = key.encode('utf-8')

    # Note: instead of encoding generic strings you can create binstring literals with b"hello" notation

    encrypted = encrypt_rot_xor(mes_bytes, key_bytes)
    print(binascii.hexlify(bytearray(encrypted)))