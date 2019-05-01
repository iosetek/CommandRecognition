import unittest
import numpy as np
from src.mfcc import MFCC

class TestConvertFrames(unittest.TestCase):
    def test_empty_data(self):
        actual = MFCC(np.array([], dtype=float))
        actual.convert_to_n_frames(3)
        expected = MFCC(np.array([], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_equal_number_of_frames(self):
        actual = MFCC(np.array([[0, 2], [3, 1], [2, 2]], dtype=float))
        actual.convert_to_n_frames(3)
        expected = MFCC(np.array([[0, 2], [3, 1], [2, 2]], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_simple_data_reduction(self):
        actual = MFCC(np.array([[0, 0], [2, 2], [4, 4], [6, 6]], dtype=float))
        actual.convert_to_n_frames(2)
        expected = MFCC(np.array([[1, 1], [5, 5]], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_not_simple_data_reduction(self):
        actual = MFCC(np.array([[0, 0], [2, 2], [4, 4], [6, 6], [8, 8]], dtype=float))
        actual.convert_to_n_frames(2)
        expected = MFCC(np.array([[1.6, 1.6], [6.4, 6.4]], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_simple_data_elongation(self):
        actual = MFCC(np.array([[2, 2], [4, 4]], dtype=float))
        actual.convert_to_n_frames(4)
        expected = MFCC(np.array([[2, 2], [2, 2], [4, 4], [4, 4]], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_not_simple_data_elongation(self):
        actual = MFCC(np.array([[2, 2], [4, 4]], dtype=float))
        actual.convert_to_n_frames(5)
        expected = MFCC(np.array([[2, 2], [2, 2], [3, 3], [4, 4], [4, 4]], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_another_not_simple_data_elongation(self):
        actual = MFCC(np.array([[2, 2], [3, 3], [4, 4], [5, 5]], dtype=float))
        actual.convert_to_n_frames(5)
        expected = MFCC(np.array([[2, 2], [2.75, 2.75], [3.5, 3.5], [4.25, 4.25], [5, 5]], dtype=float))

        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

if __name__ == '__main__':
    unittest.main()