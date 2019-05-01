import unittest
import numpy as np
from src.mfcc import MFCC

class TestNormalizeFrames(unittest.TestCase):
    def test_does_not_need_to_normalize(self):
        actual = MFCC(np.array([[1, 1], [2, 2]], np.float))
        actual.normalize_to(6)
        expected = MFCC(np.array([[1, 1], [2, 2]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))


    def test_simple_normalize_to_lower(self):
        actual = MFCC(np.array([[2, 2], [4, 4]], np.float))
        actual.normalize_to(6)
        expected = MFCC(np.array([[1, 1], [2, 2]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))


    def test_not_simple_normalize_to_lower(self):
        actual = MFCC(np.array([[2, 2], [6, 6]], np.float))
        actual.normalize_to(14)
        expected = MFCC(np.array([[1.75, 1.75], [5.25, 5.25]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))


    def test_simple_normalize_to_greater(self):
        actual = MFCC(np.array([[1, 1], [2, 2]], np.float))
        actual.normalize_to(12)
        expected = MFCC(np.array([[2, 2], [4, 4]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))


    def test_not_simple_normalize_to_greater(self):
        actual = MFCC(np.array([[1.75, 1.75], [5.25, 5.25]], np.float))
        actual.normalize_to(16)
        expected = MFCC(np.array([[2, 2], [6, 6]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))


if __name__ == '__main__':
    unittest.main()