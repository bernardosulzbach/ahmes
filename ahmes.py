#!/usr/bin/python

import ahmes_math


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


class AhmesIndicators(object):
    def __init__(self, ahmes_computer):
        self.ahmes_computer = ahmes_computer
        self.update()

    def update(self):
        self.n = ahmes_math.to_signed_byte(self.ahmes_computer.ac) < 0
        self.z = self.ahmes_computer.ac == 0
        self.v = False
        self.c = False
        self.b = False


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
        self.indicators = AhmesIndicators(self)
        self.instructions = 0
        self.memory_accesses = 0

    def set_ac(self, ac):
        ahmes_math.assert_is_a_valid_byte_value(ac)
        self.ac = ac

    def set_pc(self, pc):
        ahmes_math.assert_is_a_valid_byte_value(pc)
        self.pc = pc

    def increment_pc(self):
        self.pc = (self.pc + 1) % 256

    def load_program(self, program):
        assert isinstance(program, AhmesProgram), 'program should be an AhmesProgram'
        self.bytes = list(program.bytes)  # Copy the bytes, not just the reference

    def advance(self):
        pass

    def load_byte(self, address):
        """
        Loads the byte at the specified address, incrementing the number of memory accesses.
        :param address: a valid byte value
        :return: the byte at the specified address
        """
        ahmes_math.assert_is_a_valid_byte_value(address)
        self.memory_accesses += 1
        return self.bytes[address]

    def store_byte(self, address, value):
        """
        Stores the specified byte value in the specified address, incrementing the number of memory accesses.
        :param address: a valid byte value
        :param value: a valid byte value
        """
        ahmes_math.assert_is_a_valid_byte_value(address)
        ahmes_math.assert_is_a_valid_byte_value(value)
        self.bytes[address] = value
        self.memory_accesses += 1

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


class AhmesInstruction(object):
    def __init__(self, function, mnemonic, code):
        """
        Constructs a new AhmesInstruction with a function, a mnemonic, and a code value.
        :param function: a function that takes an AhmesComputer as an argument
        :param mnemonic: an uppercase string that represents the instruction
        :param code: a valid byte code for the instruction
        :return: an AhmesInstruction
        """
        assert isinstance(mnemonic, str), 'mnemonic should be a str'
        assert mnemonic.isupper(), 'mnemonic should be uppercase'
        assert len(mnemonic) > 0, 'mnemonic should not be empty'
        ahmes_math.assert_is_a_valid_byte_value(code)
        self.function = function
        self.mnemonic = mnemonic
        self.code = code


class SingleByteAhmesInstruction(AhmesInstruction):
    def __init__(self, function, mnemonic, code):
        """
        Constructs a new SingleByteAhmesInstruction with a function of one parameter, a mnemonic, and a code value.
        :param function: a function that takes an AhmesComputer as an argument
        :param mnemonic: an uppercase string that represents the instruction
        :param code: a valid byte code for the instruction
        :return: a SingleByteAhmesInstruction
        """

        def wrapped_function(ahmes_computer):
            ahmes_computer.increment_pc()
            function(ahmes_computer)

        super().__init__(wrapped_function, mnemonic, code)


class TwoByteAhmesInstruction(AhmesInstruction):
    def __init__(self, function, mnemonic, code):
        """
        Constructs a new TwoByteAhmesInstruction with a function of two parameters, a mnemonic, and a code value.
        :param function: a function with two parameters: an AhmesComputer and a byte
        :param mnemonic: an uppercase string that represents the instruction
        :param code: a valid byte code for the instruction
        :return: a TwoByteAhmesInstruction
        """

        def wrapped_function(ahmes_computer):
            ahmes_computer.increment_pc()
            operand = ahmes_computer.retrieve_current_byte()
            ahmes_computer.increment_pc()
            function(ahmes_computer, operand)

        super().__init__(wrapped_function, mnemonic, code)


class AhmesJumpInstruction(TwoByteAhmesInstruction):
    def __init__(self, predicate, mnemonic, code):
        """
        Constructs a new AhmesJumpInstruction with a predicate function, a mnemonic, and a code value.
        :param predicate : a function that takes an AhmesComputer as an argument and returns a logic value
        :param mnemonic: an uppercase string that represents the instruction
        :param code: a valid byte code for the instruction
        :return: an AhmesJumpInstruction
        """

        def wrapped_function(ahmes_computer, operand):
            if predicate(ahmes_computer):
                ahmes_computer.set_pc(operand)

        super().__init__(wrapped_function, mnemonic, code)


def no_op_function(ahmes_computer):
    """
    The no-op function.
    :param ahmes_computer: an AhmesComputer
    :return: None
    """
    pass


def make_ahmes_instruction_index(pedantic):
    instruction_list = [SingleByteAhmesInstruction(no_op_function, 'NOP', 0),
                        TwoByteAhmesInstruction(no_op_function, 'STA', 16),
                        TwoByteAhmesInstruction(no_op_function, 'LDA', 32),
                        TwoByteAhmesInstruction(no_op_function, 'ADD', 48),
                        TwoByteAhmesInstruction(no_op_function, 'OR', 64),
                        TwoByteAhmesInstruction(no_op_function, 'AND', 80),
                        SingleByteAhmesInstruction(no_op_function, 'NOT', 96),
                        TwoByteAhmesInstruction(no_op_function, 'SUB', 112),
                        AhmesJumpInstruction(no_op_function, 'JMP', 128),
                        AhmesJumpInstruction(no_op_function, 'JN', 144),
                        AhmesJumpInstruction(no_op_function, 'JP', 148),
                        AhmesJumpInstruction(no_op_function, 'JV', 152),
                        AhmesJumpInstruction(no_op_function, 'JNV', 156),
                        AhmesJumpInstruction(no_op_function, 'JZ', 160),
                        AhmesJumpInstruction(no_op_function, 'JNZ', 164),
                        AhmesJumpInstruction(no_op_function, 'JC', 176),
                        AhmesJumpInstruction(no_op_function, 'JNC', 180),
                        AhmesJumpInstruction(no_op_function, 'JB', 184),
                        AhmesJumpInstruction(no_op_function, 'JNB', 188),
                        SingleByteAhmesInstruction(no_op_function, 'SHR', 224),
                        SingleByteAhmesInstruction(no_op_function, 'SHL', 225),
                        SingleByteAhmesInstruction(no_op_function, 'ROR', 226),
                        SingleByteAhmesInstruction(no_op_function, 'ROL', 227),
                        SingleByteAhmesInstruction(no_op_function, 'HLT', 240)]
    instruction_index = [None] * 256
    for instruction in instruction_list:
        instruction_index[instruction.code] = instruction
    if pedantic:
        no_op_instruction = instruction_index[0]
        for i, e in enumerate(instruction_index):
            if e is None:
                instruction_index[i] = no_op_instruction
    else:
        last_valid_instruction = instruction_index[0]
        for i, e in enumerate(instruction_index):
            if e is None:
                instruction_index[i] = last_valid_instruction
            else:
                last_valid_instruction = e
    return instruction_index


ahmes_instructions = make_ahmes_instruction_index(True)


def resolve_ahmes_instruction(value):
    """
    Resolves a byte code into an AhmesInstruction.
    :param value: a valid byte value
    :return: an AhmesInstruction
    """
    return ahmes_instructions[value]


if __name__ == '__main__':
    computer = AhmesComputer(16, 32)
    print(str(computer))
    ahmes_program = AhmesProgram('ones.mem')
    ahmes_program.set_bytes(ahmes_program.get_bytes())
    print(str(ahmes_program))
