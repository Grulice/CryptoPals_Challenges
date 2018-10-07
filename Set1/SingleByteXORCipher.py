import string
import math
from collections import defaultdict


# REFERENCE_FILE = "Set1/assets/Gutenberg_Books.txt"
CIPHER_HEX = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def hex_to_str(string_hex: str, encoding='utf-8'):
    """Converts hex to string"""
    return bytearray.fromhex(string_hex).decode(encoding)


def get_char_freq_dict(inp_str: str):
    """Returns a dict of frequencies of each char from the input string"""
    freq_count = defaultdict(lambda: 0)
    for ch in inp_str:
        freq_count[ch] += 1
    return freq_count


def percent_char_freq_dict(freq_count: dict):
    freq_percent = defaultdict(lambda: 0.0)
    for key, value in freq_count.items():
        freq_percent[key] = freq_count[key] * 100 / sum(freq_count.values())
    return freq_percent


def get_score(freq_dict: dict, ref_dict: dict):
    """Returns a float score for how much freq_dict deviates from ref_dict.
    The less the score - the less the deviation"""
    score = 0.0
    for key in freq_dict:
        deviation = math.fabs(freq_dict[key] - ref_dict.get(key, 0))
        score += deviation
    return score


def sxor(s1, s2):
    """XOR two strings; returns a string"""
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def get_plaintexts(ciph_str_hex: str):
    try:
        cipher_string = hex_to_str(ciph_str_hex)
    except UnicodeDecodeError:
        cipher_string = hex_to_str(ciph_str_hex, encoding='latin-1')

    plaintexts = []
    for ref_char in freq_reference_percent:
        cur_key = ref_char * len(cipher_string)
        cur_plaintext = sxor(cipher_string, cur_key)
        cur_plaintext_freq = percent_char_freq_dict(get_char_freq_dict(cur_plaintext))
        plaintexts.append((ref_char, cur_plaintext, get_score(cur_plaintext_freq, freq_reference_percent)))
    return sorted(plaintexts, key=lambda x: x[2])


def get_plaintexts_bytes(ciph: bytearray):
    cipher_string = ciph.decode(encoding='ascii')

    plaintexts = []
    for ref_char in freq_reference_percent:
        cur_key = ref_char * len(cipher_string)
        cur_plaintext = sxor(cipher_string, cur_key)
        cur_plaintext_freq = percent_char_freq_dict(get_char_freq_dict(cur_plaintext))
        plaintexts.append((ref_char, cur_plaintext, get_score(cur_plaintext_freq, freq_reference_percent)))
    return sorted(plaintexts, key=lambda x: x[2])


# freq_reference = get_char_freq_dict(open(REFERENCE_FILE, mode='r', encoding='utf-8').read())
freq_reference_count = dict([(' ', 1157526), ('e', 630735), ('t', 436515), ('a', 381392), ('o', 374391), ('n', 337936), ('s', 320543), ('i', 318236), ('h', 314735), ('r', 298063), ('d', 218502), ('l', 205060), ('u', 147567), ('\n', 130242), ('m', 124836), ('c', 119322), ('f', 111468), ('w', 110995), ('g', 101391), ('y', 97801), (',', 96577), ('p', 81190), ('b', 71680), ('.', 52588), ('v', 47862), ('k', 37264), ('I', 28339), ('T', 17572), ('-', 14888), (';', 13904), ('A', 13045), ("'", 11737), ('H', 10337), ('"', 10331), ('S', 9396), ('x', 7879), ('W', 7509), ('M', 7235), ('B', 6465), ('j', 5996), ('E', 5948), ('!', 5918), ('’', 5687), ('q', 5426), ('“', 5086), ('C', 5017), ('O', 4976), ('P', 4899), (':', 4630), ('”', 4608), ('N', 4552), ('L', 4522), ('G', 4519), ('D', 4110), ('_', 4098), ('F', 4076), ('?', 3915), ('z', 3643), ('R', 3271), ('—', 2498), ('Y', 2424), ('1', 2151), ('J', 1967), (')', 1861), ('(', 1856), ('U', 1487), ('‘', 1351), ('V', 1330), ('2', 1290), ('*', 1265), ('0', 1194), ('5', 1077), ('3', 905), ('K', 829), ('4', 768), ('8', 688), ('6', 646), ('7', 625), ('Q', 577), ('9', 560), ('[', 551), (']', 546), ('}', 532), ('{', 517), ('~', 414), ('X', 334), ('/', 288), ('æ', 172), ('Ć', 126), ('é', 87), ('è', 78), ('=', 76), ('&', 70), ('ð', 57), ('Z', 51), ('á', 50), ('í', 30), ('þ', 24), ('$', 22), ('ó', 20), ('@', 18), ('£', 17), ('Þ', 16), ('ú', 16), ('Æ', 13), ('ý', 13), ('ö', 11), ('#', 10), ('%', 10), ('>', 9), ('ü', 8), ('|', 6), ('ê', 6), ('â', 5), ('ô', 4), ('œ', 4), ('…', 4), ('à', 3), ('ë', 3), ('ï', 2), ('ä', 1), ('Á', 1), ('§', 1), ('Ú', 1), ('°', 1), ('ח', 1), ('ו', 1), ('ϰ', 1), ('η', 1), ('τ', 1), ('ο', 1), ('ς', 1), ('Œ', 1), ('ç', 1)])
freq_reference_percent = percent_char_freq_dict(freq_reference_count)

if __name__ == "__main__":
    cipher_string = hex_to_str(CIPHER_HEX)
    print(get_plaintexts(CIPHER_HEX))

