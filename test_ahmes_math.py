from unittest import TestCase

import ahmes_math


class TestByteMath(TestCase):
    def test_is_byte_should_raise_an_assertion_error_if_the_value_is_not_an_int(self):
        self.assertRaises(AssertionError, ahmes_math.is_byte, '')
        self.assertRaises(AssertionError, ahmes_math.is_byte, '0')
        self.assertRaises(AssertionError, ahmes_math.is_byte, '1')
        self.assertRaises(AssertionError, ahmes_math.is_byte, '127')
        self.assertRaises(AssertionError, ahmes_math.is_byte, '255')
        self.assertRaises(AssertionError, ahmes_math.is_byte, '256')

        self.assertRaises(AssertionError, ahmes_math.is_byte, [])
        self.assertRaises(AssertionError, ahmes_math.is_byte, [0])
        self.assertRaises(AssertionError, ahmes_math.is_byte, [1])
        self.assertRaises(AssertionError, ahmes_math.is_byte, [127])
        self.assertRaises(AssertionError, ahmes_math.is_byte, [255])
        self.assertRaises(AssertionError, ahmes_math.is_byte, [256])

        self.assertRaises(AssertionError, ahmes_math.is_byte, 'int')
        self.assertRaises(AssertionError, ahmes_math.is_byte, 'byte')
        self.assertRaises(AssertionError, ahmes_math.is_byte, 'float')
        self.assertRaises(AssertionError, ahmes_math.is_byte, 'number')

        self.assertRaises(AssertionError, ahmes_math.is_byte, 0.0)
        self.assertRaises(AssertionError, ahmes_math.is_byte, 1.0)

        self.assertRaises(AssertionError, ahmes_math.is_byte, 1j)
        self.assertRaises(AssertionError, ahmes_math.is_byte, 1j)
        self.assertRaises(AssertionError, ahmes_math.is_byte, 1 + 1j)
        self.assertRaises(AssertionError, ahmes_math.is_byte, 1 - 1j)

    def test_is_byte_should_return_true_for_all_valid_bytes(self):
        for i in range(256):
            self.assertTrue(ahmes_math.is_byte(i))

    def test_is_byte_should_return_false_for_negative_integers(self):
        for i in range(-1024, 0):
            self.assertFalse(ahmes_math.is_byte(i))

    def test_is_byte_should_return_false_for_integers_bigger_than_the_maximum_byte_value(self):
        for i in range(256):
            self.assertFalse(ahmes_math.is_byte(256 + i))

    def test_assert_is_a_valid_byte_value_should_raise_assertion_errors_for_invalid_bytes(self):
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, '')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, '0')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, '1')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, '127')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, '255')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, '256')

        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, [])
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, [0])
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, [1])
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, [127])
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, [255])
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, [256])

        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 'int')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 'byte')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 'float')
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 'number')

        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 0.0)
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 1.0)

        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 1j)
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 1j)
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 1 + 1j)
        self.assertRaises(AssertionError, ahmes_math.assert_is_a_valid_byte_value, 1 - 1j)

    def test_assert_is_a_valid_byte_value_should_not_raise_assertion_errors_for_valid_bytes(self):
        for i in range(256):
            ahmes_math.assert_is_a_valid_byte_value(i)

    def test_to_signed_byte_should_work_for_all_byte_values(self):
        for i in range(256):
            if i < 128:
                self.assertEqual(i, ahmes_math.to_signed_byte(i))
            else:
                self.assertEqual(256 - i, ahmes_math.to_signed_byte(i))

    def test_shift_left_should_always_return_a_valid_byte(self):
        for i in range(256):
            self.assertTrue(ahmes_math.is_byte(ahmes_math.shift_left(i)))

    def test_shift_left_should_double_nonnegative_values(self):
        for i in range(127):
            self.assertEqual(2 * i, ahmes_math.shift_left(i))

    def test_shift_right_should_always_return_a_valid_byte(self):
        for i in range(256):
            self.assertTrue(ahmes_math.is_byte(ahmes_math.shift_right(i)))

    def test_shift_right_should_halve_nonnegative_values(self):
        for i in range(127):
            self.assertEqual(i // 2, ahmes_math.shift_right(i))

    def test_rotate_left_should_always_return_a_valid_byte(self):
        for i in range(256):
            self.assertTrue(ahmes_math.is_byte(ahmes_math.rotate_left(i)))

    def test_rotate_left_should_equal_shift_left_for_bytes_with_the_most_significant_bit_unset(self):
        for i in range(127):
            self.assertEqual(ahmes_math.shift_left(i), ahmes_math.rotate_left(i))

    def test_rotate_right_should_always_return_a_valid_byte(self):
        for i in range(256):
            self.assertTrue(ahmes_math.is_byte(ahmes_math.rotate_right(i)))

    def test_rotate_right_should_equal_shift_right_for_bytes_with_the_least_significant_bit_unset(self):
        for i in range(0, 256, 2):
            self.assertEqual(ahmes_math.shift_right(i), ahmes_math.rotate_right(i))
