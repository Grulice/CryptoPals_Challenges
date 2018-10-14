from Crypto.Cipher import AES
import binascii


def AES_ECB_decrypt(key: bytearray, ciphertext: bytearray):
    encryption_suite = AES.new(key, AES.MODE_ECB)
    return encryption_suite.decrypt(ciphertext)


def score_likeECB(ciph: bytearray):
    chunked_ciph = [ciph[n:n+16] for n in range(0, len(ciph), 16)]
    return len(chunked_ciph) - len(set(chunked_ciph))


# Yellow submarine key decryption
# encrypted_lines = binascii.a2b_base64(open('./assets/7.txt', mode='r').read())
# print(AES_ECB_decrypt(bytearray(b'YELLOW SUBMARINE'), encrypted_lines))


# Detect AES ECB
with open('./assets/8.txt', mode='r') as f:
    hex_lines = f.readlines()
byte_lines = [binascii.a2b_hex(x.strip()) for x in hex_lines]
byte_lines.sort(key=score_likeECB, reverse=True)

for byte_line in byte_lines:
    print(f"ECB likeness score: {score_likeECB(byte_line)}\nbytes:\n {byte_line}\nhex:\n {binascii.b2a_hex(byte_line)}\n=====================")
