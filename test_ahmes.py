import unittest
import ahmes
import ahmes_math


class TestAhmesProgram(unittest.TestCase):
    def test_set_bytes_should_assert_the_list_is_of_the_correct_size(self):
        program = ahmes.AhmesProgram.from_binary_file('ones.mem')
        byte_list = program.get_bytes()
        self.assertRaises(AssertionError, program.set_bytes, byte_list[1:])
        self.assertRaises(AssertionError, program.set_bytes, byte_list[:-1])

    def test_set_bytes_should_assert_the_list_elements_are_all_of_the_correct_type(self):
        program = ahmes.AhmesProgram.from_binary_file('ones.mem')
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

    def test_load_byte_should_increment_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        old_memory_accesses = computer.memory_accesses
        computer.load_byte(1)
        self.assertEqual(old_memory_accesses + 1, computer.memory_accesses)

    def test_store_byte_should_increment_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        old_memory_accesses = computer.memory_accesses
        computer.store_byte(1, 1)
        self.assertEqual(old_memory_accesses + 1, computer.memory_accesses)

    def test_increment_pc_should_mutate_pc(self):
        computer = ahmes.AhmesComputer()
        for i in range(1024):
            old_pc = computer.pc
            computer.increment_pc()
            self.assertNotEqual(old_pc, computer.pc)

    def test_store_function_changes_only_one_byte(self):
        chosen_value = 127
        chosen_address = 7
        computer = ahmes.AhmesComputer()
        copy_of_computer_bytes = list(computer.bytes)
        computer.ac = chosen_value
        ahmes.store_function(computer, chosen_address)
        for i, byte in enumerate(computer.bytes):
            if i == chosen_address:
                self.assertEqual(chosen_value, byte)
            else:
                self.assertEqual(copy_of_computer_bytes[i], byte)  # All other bytes should have been left unchanged

    def test_store_function_increments_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        memory_accesses_before_store = computer.memory_accesses
        ahmes.store_function(computer, 128)
        memory_accesses_after_store = computer.memory_accesses
        self.assertEqual(memory_accesses_before_store + 1, memory_accesses_after_store)

    def test_load_function_does_not_change_any_byte(self):
        chosen_address = 7
        computer = ahmes.AhmesComputer()
        copy_of_computer_bytes = list(computer.bytes)
        ahmes.load_function(computer, chosen_address)
        for i, byte in enumerate(computer.bytes):
            self.assertEqual(copy_of_computer_bytes[i], byte)

    def test_load_function_increments_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        memory_accesses_before_load = computer.memory_accesses
        ahmes.load_function(computer, 128)
        memory_accesses_after_load = computer.memory_accesses
        ahmes.load_function(computer, 128)
        self.assertEqual(memory_accesses_before_load + 1, memory_accesses_after_load)

    def test_shift_right_does_not_increment_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        memory_accesses_before_shift = computer.memory_accesses
        ahmes.shift_right_function(computer)
        memory_accesses_after_shift = computer.memory_accesses
        self.assertEqual(memory_accesses_before_shift, memory_accesses_after_shift)

    def test_shift_left_does_not_increment_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        memory_accesses_before_shift = computer.memory_accesses
        ahmes.shift_left_function(computer)
        memory_accesses_after_shift = computer.memory_accesses
        self.assertEqual(memory_accesses_before_shift, memory_accesses_after_shift)

    def test_rotate_right_does_not_increment_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        memory_accesses_before_rotation = computer.memory_accesses
        ahmes.rotate_right_function(computer)
        memory_accesses_after_rotation = computer.memory_accesses
        self.assertEqual(memory_accesses_before_rotation, memory_accesses_after_rotation)

    def test_rotate_left_does_not_increment_memory_accesses(self):
        computer = ahmes.AhmesComputer()
        memory_accesses_before_rotation = computer.memory_accesses
        ahmes.rotate_left_function(computer)
        memory_accesses_after_rotation = computer.memory_accesses
        self.assertEqual(memory_accesses_before_rotation, memory_accesses_after_rotation)
