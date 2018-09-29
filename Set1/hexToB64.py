import string


def hex_to_b64(string_hex: str):
    """Converts the string representation of a hex number to Base64; returns a string"""
    # convert hex string to a Python number
    num_hex = int(string_hex, 16)

    # Make dictionary of values for Base64 {0:'A', 1:'B', ... , 61:'9', 62:'+', 63:'/'}
    values = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    dict_b64 = dict(zip(range(64), values))

    # Initialize the result string
    str_b64 = ''

    # Loop condition explanation is below
    while num_hex != 0:

        # Every time we mod the number by 64 - we get the least significant digit in b64.
        cur_digit_b64 = num_hex % 64

        # We look up that digit's string value in the dictionary and append it to the result string.
        str_b64 = dict_b64[cur_digit_b64] + str_b64

        # After calculating the least significant digit - we 'chop' it off the end of our number
        # by div-ing it by 64 and taking that as the new hex value.
        num_hex = num_hex // 64

        # After we div for the last time - we'll get 0 as a result. This means that we calculated the most
        # significant digit of the b64 representation and conversion is almost complete (hence, the loop condition)

    return str_b64


if __name__ == '__main__':
    print(hex_to_b64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'))
