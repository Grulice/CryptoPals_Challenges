from Crypto.Cipher import AES
from Set2 import Oracles, PKCS7_Padding
import binascii
import random


UNKNOWN_BYTES = bytearray(binascii.a2b_base64("""Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""))
KEY = Oracles.rand_key()
# Generate random prefix of random length (1-64 bytes)
RAND_PREFIX = bytearray([random.randint(0, 255) for _ in range(0, random.randint(1, 64))])
padding = b'a'*32
repeat_lastindex = 0


def AES_128_ECB(myPT: bytearray = b''):
    """Encrypt given PT with unknown string appended and random prefix of random length prepended"""
    pt = RAND_PREFIX + myPT + UNKNOWN_BYTES  # append unknown text to my plaintext

    # Pad plaintext
    pt = PKCS7_Padding.getw_and_rpad(pt)

    # encrypt and return
    enc_suite = AES.new(mode=AES.MODE_ECB, key=KEY)
    return enc_suite.encrypt(pt)


def has_repeatblocks(ct: bytearray):
    """Find out if the input bytearray has (at least) 2 consecutive identical 16 byte blocks"""
    for i in range(0, len(ct) - 1, 16):
        chunk1 = ct[i   : i+16]
        chunk2 = ct[i+16: i+32]
        if chunk1 == chunk2:
            return i+32
    return 0


def find_padding(encryptor):
    global padding
    global repeat_lastindex
    for i in range(16):
        curr_ct = encryptor(padding)
        lastind = has_repeatblocks(curr_ct)
        if lastind:
            repeat_lastindex = lastind
            return
        padding += b'a'
    return None


def encrypt_wrapper(input = b''):
    ct = AES_128_ECB(padding + input)
    return ct[repeat_lastindex:]


def break_cipher(encryptor, blocksize: int):
    """Do byte-at-a-time decryption on the given encryptor function, using given blocksize"""
    # TODO: Write comments for this function

    deciphered_bytes = b''  # initialize the result variable to be able to use it when it's empty

    # Divide the cipher into 16 byte blocks and decrypt block-by-block
    for block_num in range(len(encryptor()) // 16):
        blockstart = block_num*16  # index of current block's start

        for pad_size in range(blocksize-1, -1, -1):
            pad_bytes = b'a' * pad_size

            cipher_dict = {encryptor(bytearray(pad_bytes + deciphered_bytes + bytes([enc_char])))[blockstart:blockstart+16]
                           : enc_char for enc_char in range(256)}

            cur_symb = cipher_dict[encryptor(pad_bytes)[blockstart:blockstart+16]]
            deciphered_bytes += bytes([cur_symb])
    return deciphered_bytes


if __name__ == '__main__':
    find_padding(AES_128_ECB)
    print(padding, len(padding), repeat_lastindex)

    broken = break_cipher(encrypt_wrapper, 16)
    print(broken.decode())
