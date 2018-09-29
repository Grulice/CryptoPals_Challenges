from os import path as path
from collections import defaultdict

# constants
FILE_PATH = "./assets/Gutenberg_Books.txt"


def char_frequency(inp_string: str):
    """Returns a dict of frequencies of each char given a string"""
    freq = defaultdict(lambda: 0)
    for ch in inp_string:
        freq[ch] += 1
    return dict(freq)


source_file = open(FILE_PATH, mode='r', encoding='utf-8')
source_str = source_file.read()
source_file.close()

frequency = char_frequency(source_str)
total_chars = len(source_str)

ranked_file_name = "{0}/{1}_chFreqRANKED{2}".format(path.split(FILE_PATH)[0], path.basename(FILE_PATH).split('.')[0], '.txt')
ranked_file = open(ranked_file_name, mode='w', encoding='utf-8')
for key, value in sorted(frequency.items(), key=lambda val: val[1], reverse=True):
    cur_val_str = "{0}:{1}\n".format(key, value*100/total_chars)
    print(cur_val_str)
    ranked_file.write(cur_val_str)
ranked_file.close()
