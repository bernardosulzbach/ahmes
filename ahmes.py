#!/usr/bin/python


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
            assert len(byte_list) == len(self.get_bytes()), 'byte_list should have the same size as the current list'
            assert all(map(lambda e: isinstance(e, int), byte_list)), 'byte_list should be a list of bytes'
            self.bytes = byte_list

    def __str__(self):
        if not self.initialized:
            return "Failed to initialize the program."
        length_of_largest_index = len(str(len(self.bytes)))
        lines = []
        for i, e in enumerate(self.get_bytes()):
            lines.append(str(i).rjust(length_of_largest_index) + ": " + str(e))
        return '\n'.join(lines)


if __name__ == '__main__':
    program = AhmesProgram('ones.mem')
    program.set_bytes(program.get_bytes())
    print(str(program))
