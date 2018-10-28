from Crypto.Cipher import AES
from Set2 import Oracles, PKCS7_Padding
import binascii


UNKNOWN_BYTES = bytearray(binascii.a2b_base64("""Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""))
KEY = Oracles.rand_key()


def AES_128_ECB(myPT: bytearray = b''):
    """Encrypt given PT with unknown string appended"""
    pt = myPT + UNKNOWN_BYTES  # append unknown text to my plaintext

    # Pad plaintext
    l_pt = len(pt)
    padwidth = l_pt // 16 if l_pt % 16 == 0 else l_pt // 16 + 1
    pt = PKCS7_Padding.rpad_my_shit(pt, width=16 * padwidth)

    # encrypt and return
    enc_suite = AES.new(mode=AES.MODE_ECB, key=KEY)
    return enc_suite.encrypt(pt)


def find_block_size(encryptor):
    """Detects the block size in bytes for the given encryptor function"""
    # TODO: Write comments for this function
    for lpad_size in range(512):
        ciphertext = encryptor(bytearray(b'a' * lpad_size))
        for block_size in range(1, lpad_size // 2):
            if ciphertext[:block_size] == ciphertext[block_size:block_size*2]:
                return block_size
    return None


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
    b_size = find_block_size(AES_128_ECB)
    broken = break_cipher(AES_128_ECB, b_size)
    print(broken.decode())
