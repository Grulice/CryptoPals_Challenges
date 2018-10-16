def rpad_my_shit(shit: bytearray, width: int, pad_byte: bytes=b'\x04'):
    pad_bytes = pad_byte * (width - len(shit))
    return shit + pad_bytes


if __name__ == '__main__':
    print(rpad_my_shit(bytearray(b'YELLOW SUBMARINE'), 20, pad_byte=b'\x04'))

