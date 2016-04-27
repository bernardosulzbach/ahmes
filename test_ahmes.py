#!/usr/bin/python

import unittest
import ahmes


class TestAhmesProgram(unittest.TestCase):
    def test_set_bytes_should_assert_the_list_is_of_the_correct_size(self):
        program = ahmes.AhmesProgram('ones.mem')
        byte_list = program.get_bytes()
        self.assertRaises(AssertionError, program.set_bytes, byte_list[1:])
        self.assertRaises(AssertionError, program.set_bytes, byte_list[:-1])

    def test_set_bytes_should_assert_the_list_elements_are_all_of_the_correct_type(self):
        program = ahmes.AhmesProgram('ones.mem')
        byte_list_size = len(program.get_bytes())
        string_list_of_the_same_size = [str(i) for i in range(byte_list_size)]
        self.assertRaises(AssertionError, program.set_bytes, string_list_of_the_same_size)
        float_list_of_the_same_size = [float(i) for i in range(byte_list_size)]
        self.assertRaises(AssertionError, program.set_bytes, float_list_of_the_same_size)
        mixed_list_of_the_same_size = [i for i in range(byte_list_size)]
        mixed_list_of_the_same_size[-1] = '255'
        self.assertRaises(AssertionError, program.set_bytes, mixed_list_of_the_same_size)
