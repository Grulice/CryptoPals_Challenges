import base64
from collections import namedtuple
from Set1 import SingleByteXORCipher


def hamming_dist(byteval1: bytearray, byteval2: bytearray):
    dist = 0
    byteval1_zfill = ''.join([bin(x)[2:].zfill(8) for x in byteval1])
    byteval2_zfill = ''.join([bin(x)[2:].zfill(8) for x in byteval2])

    for bit_pair in zip(byteval1_zfill, byteval2_zfill):
        if bit_pair[0] != bit_pair[1]:
            dist += 1
    return dist


def find_keySize(ciph: bytes):
    best_ham = [0, 1000]  # best_ham[0] is the current best key size, best_ham[1] is the cur best ham dist
    for key_size in range(2, 40):
        ham_dist_NORM = hamming_dist(ciph[:key_size], ciph[key_size: key_size*2]) / key_size
        if ham_dist_NORM < best_ham[1]:
            best_ham = [key_size, ham_dist_NORM]
    print(best_ham[0])
    return best_ham[0]


def group(input_list, chunk_size):
    result = []
    while len(input_list) > 0:
        result.append(input_list[:chunk_size])
        input_list = input_list[chunk_size:]
    return result


def transpose_blocks(ciph: bytes, block_size: int):
    grouped = group(ciph, block_size)
    return [bytes(''.join([chr(x[n]) for x in grouped]), encoding='utf-8') for n in range(len(grouped[0]))]


def findKey(ciph: bytes):
    for kSize in range(2, 42):
    # kSize = find_keySize(ciph)
        transposed = transpose_blocks(ciph, kSize)
        key = b''
        for block in transposed:
            key = key + bytes(SingleByteXORCipher.get_plaintexts_bytes(block)[0][0], encoding='utf-8')
        yield key


def get_repeat_key(k, textlen):
    return k * (textlen // len(k)) + k[:(textlen % len(k))]


base64_bytes = bytes(open('./assets/6.txt', mode='r').read(), encoding='utf-8')

for key in findKey(base64_bytes):
    repeat_key = get_repeat_key(key, len(base64_bytes))
    print(SingleByteXORCipher.sxor(str(base64_bytes), str(repeat_key)))




# print(hamming_dist(b'this is a test', b'wokka wokka!!!'))
