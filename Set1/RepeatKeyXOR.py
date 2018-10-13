import itertools
from Set1 import SingleByteXORCipher
import binascii


def hamming_dist_OLD(byteval1: bytearray, byteval2: bytearray):
    """Return number of different bits in input bytearrays"""
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


def hamming_dist(byteval1: bytearray, byteval2: bytearray):
    return sum(['{:8b}'.format(left ^ right).count('1')
                for left, right in zip(byteval1, byteval2)
                ]
               )


def find_key_sizes(ciph: bytearray):
    """Return a list of possible key lengths for the given cipher,
    sorted by the their corresponding Hamming distances (ascending order)"""
    keys = []  # initialize the result list for appending
    for ksize in range(2, 40):  # check for all key sizes between 2 and 40
        # take first 4 slices of size ksize
        slice1 = ciph[:ksize]
        slice2 = ciph[ksize: ksize * 2]
        slice3 = ciph[ksize * 2: ksize * 3]
        slice4 = ciph[ksize * 3: ksize * 4]
        # find avg ham distance between first 4 slices
        ham_dist = (hamming_dist(slice1, slice2)
                    + hamming_dist(slice2, slice3)
                    + hamming_dist(slice3, slice4)) / 3

        # normalize the hamming distance by dividing it by ksize
        # to negate the effect that large keys will naturally have larger edit distances
        normalized_ham_dist = ham_dist / ksize

        keys.append((ksize, normalized_ham_dist))  # add the result to the list as a tuple pair

    # return list of keysizes sorted by their corresponding Hamming distances (in ascending order)
    return [x[0] for x in sorted(keys, key=lambda x: x[1])]


def split_blocks(ciph: bytearray, block_size: int):
    """Return a list of bytearray split chunks of the given size taken from the input bytearray"""
    n = max(1, block_size)
    return [ciph[i:i+n] for i in range(0, len(ciph), n)]


def transpose_blocks(block_list: list):
    """Return a transposed version of the input block list"""
    result = []
    # Transposing a 2d list means flipping around its rows and columns.
    # Here's how to construct this:
    #  - Create a new 2d list as follows:
    #    take first elements from all rows of the target list and add them
    #    to the first row of our list; take second elements from rows of target list,
    #    add them to second row of our list. Rinse and repeat.

    # This loop constructs resulting 2d list row by row. Result will have the same number of rows
    # as the initial list has columns. block_list[0] is the first row of initial list. Its len()
    # is the number of columns the initial list has.
    for n in range(0, len(block_list[0])):
        result.append([])  # create an empty list element so that we can access it below
        for block in block_list:
            #  this is in try block because the last block of the list might be smaller than the rest
            #  ex.: divide (0, 1, 2, 3, 4, 5, 6, 7) into groups of 3: (0,1,2)(3,4,5)(6,7)
            try:
                result[n].append(block[n])
            except IndexError:
                pass
        result[n] = bytearray(result[n])  # add the transposed row
    return result


def get_key(transposed_blocks: list):
    """Concat and return keys resulting from single-byte XOR decipher of each transposed block"""
    finalkey = ""
    for transposed_block in transposed_blocks:
        finalkey = finalkey + SingleByteXORCipher.get_plaintexts_bytes(transposed_block)[0][0]
    return finalkey


def decode_cipher(ciph: bytearray, k: bytearray):
    """Get plaintext from cipher text and key. Key is repeated automatically if necessary"""
    it = itertools.cycle(k)
    return bytearray([symb ^ next(it) for symb in ciph])


def get_plaintexts(cipherbytes: bytearray):
    """Generate (key, plaintext) tuples for the repeat-key encrypted
    cipher text in order from most likely to least"""
    for best_ksize in find_key_sizes(cipherbytes):
        spl = split_blocks(cipherbytes, block_size=best_ksize)
        transposed = transpose_blocks(spl)
        k = bytearray(get_key(transposed), encoding='utf-8')
        yield (k, decode_cipher(cipherbytes, k))


if __name__ == "__main__":
    byted_b64 = binascii.a2b_base64((open('./assets/6.txt', mode='r').read()))  # convert b64 str to bytes
    cipher = bytearray(byted_b64)  # convert bytes to bytearray
    # Not really necessary in this case, but we standardize around bytearray, so deal with it

    for plaintext in get_plaintexts(cipher):
        curr_key, curr_pt = plaintext
        print(f"Key size: {len(curr_key)} | Key: {curr_key}\n")
        # ignore decoding errors because wrong keys will produce pt's with a lot of random undecodeable bytes
        print(curr_pt.decode(errors='ignore'))
        print("====================================")
