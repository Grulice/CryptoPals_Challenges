import binascii
from itertools import cycle


def xor_bytes(barray1: bytearray, barray2: bytearray):
    return bytearray((a ^ b) for a, b in zip(barray1, barray2))


plaintext = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

plaintext_bytearray = bytearray(plaintext.encode())
key = b"HELLOGUYSIMAKEY"
it = cycle(key)
repeatkey = bytearray(next(it) for x in plaintext_bytearray)

bytearr = xor_bytes(plaintext_bytearray, repeatkey)

print("Ciphertext: ", bytearr)

bytearr = xor_bytes(bytearr, repeatkey)

print("Decihpered plaintext: ", bytearr)
