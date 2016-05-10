import ahmes
import ahmes_math


def parse_program(string):
    """
    Given a human-readable string of instructions and addresses, parses the text into an AhmesProgram.
    :param string: a string representing an AhmesProgram
    :return: an AhmesProgram
    """
    tokens = string.split()
    byte_list = []
    for token in tokens:
        # Handle numbers
        if token.isnumeric():
            integer_value = int(token)
            if ahmes_math.is_byte(integer_value):
                byte_list.append(integer_value)
            else:
                raise ValueError("got " + token + " when expecting a valid byte value in the range [0, 255]")
        # Handle instruction mnemonics
        else:
            instruction = ahmes.resolve_ahmes_instruction_from_mnemonic(token)
            if instruction is not None:
                byte_list.append(instruction.code)
            else:
                raise ValueError("got " + token + " when expecting a valid instruction mnemonic")
    return ahmes.AhmesProgram.from_byte_list(byte_list)
