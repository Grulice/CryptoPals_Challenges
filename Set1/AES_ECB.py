from Crypto.Cipher import AES
import binascii

encrypted_lines = binascii.a2b_base64(open('./assets/7.txt', mode='r').read())

encryption_suite = AES.new('YELLOW SUBMARINE'.encode(encoding='utf-8'), AES.MODE_ECB)
decrypted_lines = encryption_suite.decrypt(encrypted_lines)

print(decrypted_lines.decode('ascii'))