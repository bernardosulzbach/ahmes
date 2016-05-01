#!/usr/bin/python


def find_maximum_string_width(objects):
    maximum_so_far = 0
    for i, e in enumerate(objects):
        maximum_so_far = max(maximum_so_far, len(str(e)))
    return maximum_so_far


def make_list_of_key_value_lines(keys, values):
    assert len(keys) == len(values), 'keys and values should have the same length'
    lines = []
    maximum_key_width = find_maximum_string_width(keys)
    maximum_value_width = find_maximum_string_width(values)
    # Doubling the '{' and the '}' prevents the formatter from parsing them.
    format_string = '{{0:{0}}}: {{1:{1}}}'.format(maximum_key_width, maximum_value_width)
    for i, e in enumerate(keys):
        lines.append(format_string.format(e, values[i]))
    return lines


def make_string_of_key_value_lines(keys, values):
    return '\n'.join(make_list_of_key_value_lines(keys, values))


def is_byte(integer):
    """
    Returns whether or not an integer value could be stored in a byte of 8 bits.
    :param integer: any int
    """
    assert isinstance(integer, int), 'integer should be an int'
    return 0 <= integer <= 255


class AhmesComputer(object):
    """
    A pure Python implementation of the Ahmes computer.
    """

    def __init__(self, ac=0, pc=0):
        self.ac = 0  # It is a good practice to define all attributes inside the __init__ method
        self.pc = 0
        self.set_ac(ac)  # Should reuse the AC setter so that the validation step is not duplicated
        self.set_pc(pc)  # Same for PC
        self.bytes = [0] * 256

    def set_ac(self, ac):
        assert is_byte(ac), 'ac should be a valid byte value'
        self.ac = ac

    def set_pc(self, pc):
        assert is_byte(pc), 'pc should be a valid byte value'
        self.pc = pc

    def load_program(self, program):
        assert isinstance(program, AhmesProgram), 'program should be an AhmesProgram'
        self.bytes = list(program.bytes)  # Copy the bytes, not just the reference

    def advance(self):
        pass

    def __str__(self):
        keys = ['AC', 'PC']
        keys.extend([i for i in range(256)])
        values = [self.ac, self.pc]
        values.extend(self.bytes)
        return make_string_of_key_value_lines(keys, values)


class AhmesProgram(object):
    """
    A pure Python representation of an Ahmes program.
    """

    def __init__(self, filename):
        self.initialized = False
        self.filename = filename
        self.bytes = []
        self.initialize_bytes()

    def initialize_bytes(self):
        if not self.initialized:
            try:
                with open(self.filename, 'rb') as open_file:
                    read_bytes = open_file.read()
                    # The first 4 bytes are not part of the program.
                    # The remaining of the file seems to be made up of pairs of bytes of which only the first is used.
                    self.bytes = read_bytes[4::2]
                    self.initialized = True
            except FileNotFoundError:
                pass  # Acceptable, the class handles this exception

    def get_bytes(self):
        return self.bytes

    def set_bytes(self, byte_list):
        """
        Sets the bytes of this AhmesProgram to the provided list of bytes.
        If the program could not be initialized, this is a no-op.
        :param byte_list: a list of bytes
        """
        if self.initialized:
            assert len(byte_list) == len(
                    self.get_bytes()), 'byte_list should have the same size as the current list'
            assert all(map(lambda e: isinstance(e, int), byte_list)), 'byte_list should be a list of bytes'
            self.bytes = byte_list

    def __str__(self):
        if not self.initialized:
            return 'Failed to initialize the program.'
        keys = [i for i in range(256)]
        values = self.bytes
        return make_string_of_key_value_lines(keys, values)


if __name__ == '__main__':
    computer = AhmesComputer(16, 32)
    print(str(computer))
    ahmes_program = AhmesProgram('ones.mem')
    ahmes_program.set_bytes(ahmes_program.get_bytes())
    print(str(ahmes_program))
