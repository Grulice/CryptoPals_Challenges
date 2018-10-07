from Set1 import SingleByteXORCipher
import binascii

PLAINTEXT = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
KEY = "PICEO"

repeatkey = KEY * (len(PLAINTEXT) // len(KEY)) + KEY[:(len(PLAINTEXT) % len(KEY))]

result = SingleByteXORCipher.sxor(PLAINTEXT, repeatkey)

print(binascii.b2a_base64(result.encode()))
print(binascii.hexlify(result.encode()))
