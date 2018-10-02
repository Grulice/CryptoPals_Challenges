from Set1 import SingleByteXORCipher

with open('./assets/4.txt', mode='r') as f:

    ciphertexts = f.readlines()

plaintexts = []

for ciphertext in ciphertexts:
    cur_plaintext = SingleByteXORCipher.get_plaintexts(ciphertext)[0]
    plaintexts.append(cur_plaintext)

best_plaintext = min(plaintexts, key=lambda x: x[2])

print(best_plaintext)
