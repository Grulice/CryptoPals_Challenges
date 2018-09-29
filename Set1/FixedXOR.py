def xor(val1: str, val2: str):
    val1num = int(val1, 16)
    val2num = int(val2, 16)

    return hex(val1num ^ val2num)[2:]


if __name__ == '__main__':
    print(xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965"))


