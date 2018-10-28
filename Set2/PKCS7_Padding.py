def rpad_my_shit(shit: bytearray, width: int, pad_byte: bytes=b'\x04'):
    pad_bytes = pad_byte * (width - len(shit))
    return shit + pad_bytes


def getw_and_rpad(shit, pad_byte: bytes= b'\x04'):
    l_pt = len(shit)
    padwidth = l_pt // 16 if l_pt % 16 == 0 else l_pt // 16 + 1
    return rpad_my_shit(shit, width=16 * padwidth)

if __name__ == '__main__':
    print(rpad_my_shit(bytearray(b'YELLOW SUBMARINE'), 20, pad_byte=b'\x04'))

