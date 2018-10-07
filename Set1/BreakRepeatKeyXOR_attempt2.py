import binascii
from collections import namedtuple
import itertools
from Set1 import SingleByteXORCipher
import binascii


def hamming_dist(byteval1: bytearray, byteval2: bytearray):
    """Returns int with number of different bits in input bytearrays"""
    dist = 0
    # iterating over a bytearray returns int
    # if we convert it to bin as is - we get no padding bits on the left
    # ex.: bin(8) would produce '100', but for a proper representation of an ASCII character,
    # we need it to be 00000100 (8 bits). Thus, we use the zfill(8)
    byteval1_zfill = ''.join([bin(x)[2:].zfill(8) for x in byteval1])
    byteval2_zfill = ''.join([bin(x)[2:].zfill(8) for x in byteval2])

    # take pairs of bits picked from both values and increase
    # distance by 1 if the bits in pair are not equal
    for bit_pair in zip(byteval1_zfill, byteval2_zfill):
        if bit_pair[0] != bit_pair[1]:
            dist += 1
    return dist


def find_key_sizes(ciph: bytearray):
    """Returns a list of possible key lengths for the given cipher,
    sorted by the their corresponding Hamming distances (in ascending order)"""
    keys = []  # initialize the result list for appending
    for ksize in range(2, 40):  # check for all key sizes between 2 and 40
        # compare the first 4 slices of size ksize
        slice1 = ciph[:ksize]
        slice2 = ciph[ksize: ksize * 2]
        slice3 = ciph[ksize * 2: ksize * 3]
        slice4 = ciph[ksize * 3: ksize * 4]

        ham_dist = (hamming_dist(slice1, slice2) + hamming_dist(slice2, slice3) + hamming_dist(slice3, slice4)) / 3
        # normalize the hamming distance by dividing it by ksize
        # to negate the effect that large keys will naturally have larger edit distances
        normalized_ham_dist = ham_dist / ksize

        keys.append((ksize, normalized_ham_dist))  # add the result to the list as a tuple pair

    # return list of keysizes sorted by their corresponding Hamming distances (in ascending order)
    return [x[0] for x in sorted(keys, key=lambda x: x[1])]


def split_blocks(ciph: bytearray, block_size: int):
    """Returns a list of bytearray blocks of the given size taken from the input bytearray"""
    n = max(1, block_size)
    return [ciph[i:i+n] for i in range(0, len(ciph), n)]


def transpose_blocks(block_list: list):
    """Returns a transposed version of the input block list"""
    result = []
    for n in range(0, len(block_list[0])):
        result.append([])
        for block in block_list:
            try:
                result[n].append(block[n])
            except IndexError:
                pass
        result[n] = bytearray(result[n])
    return result


def get_key(transposed_blocks: list):
    finalkey = ""
    for transposed_block in transposed_blocks:
        finalkey = finalkey + SingleByteXORCipher.get_plaintexts_bytes(transposed_block)[0][0]
    return finalkey


def decode_cipher(ciph: bytearray, k: bytearray):
    result = ""
    it = itertools.cycle(k)
    for symb in ciph:
        result = result + chr(symb ^ next(it))
    return result


byted_b64 = binascii.a2b_base64((open('./assets/6.txt', mode='r').read()))
cipherbytes = bytearray(byted_b64)
for best_ksize in find_key_sizes(cipherbytes):
    # best_ksize = find_key_sizes(cipherbytes)[0]
    spl = split_blocks(cipherbytes, block_size=best_ksize)
    transposed = transpose_blocks(spl)
    k = bytearray(get_key(transposed), encoding='utf-8')
    print("Key size:", best_ksize, decode_cipher(cipherbytes, k))
    print("Key :", k.decode())
    print("====================================")


#  print(hamming_dist(b'this is a test', b'wokka wokka!!!'))
