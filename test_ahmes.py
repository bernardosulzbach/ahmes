#!/usr/bin/python

import unittest
import ahmes
import ahmes_math


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


class TestAhmesComputer(unittest.TestCase):
    def test_pc_should_start_as_a_valid_byte(self):
        computer = ahmes.AhmesComputer()
        self.assertTrue(ahmes_math.is_byte(computer.pc))

    def test_increment_pc_should_never_invalidate_pc(self):
        computer = ahmes.AhmesComputer()
        for i in range(1024):
            computer.increment_pc()
            self.assertTrue(ahmes_math.is_byte(computer.pc))

    def test_increment_pc_should_mutate_pc(self):
        computer = ahmes.AhmesComputer()
        for i in range(1024):
            old_pc = computer.pc
            computer.increment_pc()
            self.assertNotEqual(old_pc, computer.pc)

    def test_resolve_ahmes_instruction_should_resolve_all_valid_bytes(self):
        for i in range(256):
            self.assertIsInstance(ahmes.resolve_ahmes_instruction(i), ahmes.AhmesInstruction)
