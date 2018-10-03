import base64


def hamming_dist(byteval1: bytes, byteval2: bytes):
    dist = 0
    byteval1_zfill = ''.join([bin(x)[2:].zfill(8) for x in byteval1])
    byteval2_zfill = ''.join([bin(x)[2:].zfill(8) for x in byteval2])

    for bit_pair in zip(byteval1_zfill, byteval2_zfill):
        if bit_pair[0] != bit_pair[1]:
            dist += 1
    return dist


base64_str = bytes(open('./assets/6.txt', mode='r').read(), encoding='utf-8')

print(base64.decodebytes(base64_str))

print(hamming_dist(b'this is a test', b'wokka wokka!!!'))
