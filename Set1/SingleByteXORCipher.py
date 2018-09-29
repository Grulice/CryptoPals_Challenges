import string


def hex_to_str(string_hex: str):
    """Converts hex to string"""
    return bytearray.fromhex(string_hex).decode()


for c in hex_to_str("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"):
    print(c)