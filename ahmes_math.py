def is_byte(value):
    """
    Returns whether or not an integer value could be stored in a byte of 8 bits.
    :param value: any int
    """
    assert isinstance(value, int), 'integer should be an int'
    return 0 <= value < 256


def assert_is_a_valid_byte_value(value):
    assert is_byte(value), 'the provided value is not a valid byte value'


def to_signed_byte(value):
    assert_is_a_valid_byte_value(value)
    if value < 128:
        return value
    else:
        return 256 - value


def shift_left(value):
    return (value << 1) & 0xFF


def shift_right(value):
    return value >> 1