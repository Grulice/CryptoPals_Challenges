from Crypto.Cipher import AES
from Set1 import AES_ECB
import binascii


def xor(barr1: bytearray, barr2: bytearray):
    return bytearray([b1 ^ b2 for b1, b2 in zip(barr1, barr2)])


def AES_CBC_decrypt(ciph: bytearray, iv: bytearray, k: bytearray):
    chunked_ciph = [ciph[n:n + 16] for n in range(0, len(ciph), 16)]
    decrypted = bytearray()
    prev_ciph = iv
    for chunk in chunked_ciph:
        chunk_decrypted = AES_ECB.AES_ECB_decrypt(key=k, ciphertext=chunk)
        decrypted.extend(xor(chunk_decrypted, prev_ciph))
        prev_ciph = chunk
    return decrypted





if __name__ == '__main__':
    with open('./assets/10.txt', mode='r') as f:
        cipher_bytes = binascii.a2b_base64(f.read())
    key = bytearray(b'YELLOW SUBMARINE')
    print(AES_CBC_decrypt(bytearray(cipher_bytes), bytearray(b'\x00\x00\x00'), key).decode())
