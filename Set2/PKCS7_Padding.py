def rpad_my_shit(shit: bytearray, width: int, pad_byte: bytes):
    pad_bytes = pad_byte * (width - len(shit))
    return shit + pad_bytes


print(rpad_my_shit(bytearray(b'YELLOW SUBMARINE'), 20, pad_byte=b'\x04'))