#!/usr/bin/python


class AhmesProgram(object):
    def __init__(self, filename):
        self.initialized = False
        self.filename = filename
        self.bytes = []

    def __str__(self):
        self.initialize_bytes()
        if not self.initialized:
            return "Failed to initialize the program."
        length_of_largest_index = len(str(len(self.bytes)))
        lines = []
        for i, e in enumerate(self.get_bytes()):
            lines.append(str(i).rjust(length_of_largest_index) + ": " + str(e))
        return '\n'.join(lines)

    def initialize_bytes(self):
        if not self.initialized:
            try:
                with open(self.filename, 'rb') as open_file:
                    self.bytes = open_file.read()
                    self.initialized = True
            except FileNotFoundError:
                pass  # Acceptable, the class handles this exception

    def get_bytes(self):
        return self.bytes[4::2]

if __name__ == '__main__':
    program = AhmesProgram('ones.mem')
    print(str(program))
