from unittest import TestCase

import ahmes_parser


def integer_list_to_string(integer_list):
    return " ".join([str(integer) for integer in integer_list])


class TestParser(TestCase):
    def test_parse_program_should_work_for_an_empty_program(self):
        program = ahmes_parser.parse_program("")
        for i, byte in enumerate(program.bytes):
            self.assertEqual(0, byte)

    def test_parse_program_should_work_for_a_simple_correct_program(self):
        byte_list = [16, 4, 32, 6, 16, 0]
        program = ahmes_parser.parse_program(integer_list_to_string(byte_list))
        for i, byte in enumerate(program.bytes):
            self.assertEqual(byte_list[i], byte)

    def test_parse_program_should_fail_on_negative_numbers(self):
        byte_list = [16, 4, 32, 6, 16, -1]
        self.assertRaises(ValueError, ahmes_parser.parse_program, integer_list_to_string(byte_list))

    def test_parse_program_should_fail_on_numbers_above_the_maximum_byte_value(self):
        byte_list = [16, 4, 32, 6, 16, 256]
        self.assertRaises(ValueError, ahmes_parser.parse_program, integer_list_to_string(byte_list))
