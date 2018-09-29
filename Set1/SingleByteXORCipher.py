import string
import math
from collections import defaultdict


REFERENCE_FILE = "./assets/Gutenberg_Books.txt"
CIPHER_HEX = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def hex_to_str(string_hex: str):
    """Converts hex to string"""
    return bytearray.fromhex(string_hex).decode()


def get_char_freq_dict(inp_str: str):
    """Returns a dict of frequencies of each char from the input string"""
    freq_count = defaultdict(lambda: 0)
    inp_str_len = len(inp_str)
    for ch in inp_str:
        freq_count[ch] += 1

    freq_percent = defaultdict(lambda: 0.0)
    for key, value in freq_count.items():
        freq_percent[key] = freq_count[key] * 100 / inp_str_len
    return dict(freq_percent)


def get_score(freq_dict: dict, ref_dict: dict):
    """Returns a float score for how much freq_dict deviates from ref_dict.
    The less the score - the less the deviation"""
    score = 0.0
    for key in freq_dict:
        deviation = math.fabs(freq_dict[key] - ref_dict.get(key, 0))
        score += deviation
    return score


def sxor(s1, s2):
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


freq_reference = get_char_freq_dict(open(REFERENCE_FILE, mode='r', encoding='utf-8').read())
cipher_string = hex_to_str(CIPHER_HEX)

plaintexts = []

for ref_char in freq_reference:
    cur_plaintext = sxor(ref_char*len(cipher_string), cipher_string)
    cur_candidate_freq = get_char_freq_dict(cur_plaintext)
    plaintexts.append((ref_char, cur_plaintext, get_score(cur_candidate_freq, freq_reference)))

for plaintext in sorted(plaintexts, key=lambda x: x[2]):
    print(plaintext)
