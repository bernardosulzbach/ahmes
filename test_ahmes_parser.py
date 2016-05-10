from unittest import TestCase

import ahmes_parser


class TestParser(TestCase):
    def test_empty_program_parsing(self):
        program = ahmes_parser.parse_program("")
        for i, byte in enumerate(program.bytes):
            self.assertEqual(0, byte)
