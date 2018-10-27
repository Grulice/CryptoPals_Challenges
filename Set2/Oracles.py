from Crypto.Cipher import AES
from Set1 import AES_ECB
from Set2 import PKCS7_Padding
import random


def rand_key():
    """Return random 16 byte bytearray for a random AES Key.
    __NOT CRYPTO SECURE__"""
    return bytearray([random.randint(0, 255) for _ in range(0, 16)])


def CBC_ECB_roulette(plaintext: bytearray):
    """Encrypt plaintext in either AES ECB or CBC (coin flip to decide which to use)
    Return (ciphertext: bytearray, is_CBC: bool) tuple for result checking"""

    # Append and prepend between 5 and 10 bytes
    pt = b'0' * random.randint(5, 10) \
         + plaintext + \
         b'0' * random.randint(5, 10)
    # Pad plaintext to nearest multiple of 16 bytes
    l_pt = len(pt)
    padwidth = l_pt // 16 if l_pt % 16 == 0 else l_pt // 16 + 1
    pt = PKCS7_Padding.rpad_my_shit(pt, width=16 * padwidth)

    encrypt_ECB = random.choice((True, False))  # flip the coin
    if encrypt_ECB:
        # create cipher in ECB mode with random 16 byte key
        enc_suite = AES.new(mode=AES.MODE_ECB, key=rand_key())
    else:
        # create cipher in CBC mode with random 16 byte IV and key
        enc_suite = AES.new(mode=AES.MODE_CBC, iv=rand_key(), key=rand_key())

    return enc_suite.encrypt(pt), encrypt_ECB


def is_ECB(encryptor):
    """Detect if the encryptor function is encrypting in ECB mode. All Hail the Mighty Oracle function!"""
    ciphertext, is_CBC = encryptor(b'A' * 48)
    return True if AES_ECB.score_likeECB(ciphertext) else False, is_CBC


if __name__ == '__main__':
    test_num = 10000
    correct_ans = 0
    for _ in range(test_num):
        oracle, act = is_ECB(CBC_ECB_roulette)
        if oracle == act:
            correct_ans += 1
    print(f"""The Mighty Oracle made {test_num} prophecies and was correct {correct_ans} times!""")


