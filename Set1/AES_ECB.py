from Crypto.Cipher import AES
import binascii


def AES_ECB_decrypt(key: bytearray, ciphertext: bytearray):
    encryption_suite = AES.new(key, AES.MODE_ECB)
    return encryption_suite.decrypt(ciphertext)


# Yellow submarine key decryption
# encrypted_lines = binascii.a2b_base64(open('./assets/7.txt', mode='r').read())
# print(AES_ECB_decrypt(bytearray(b'YELLOW SUBMARINE'), encrypted_lines))

