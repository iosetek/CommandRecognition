import unittest
import numpy as np
import math
from src.mfcc import MFCC

class TestEnlargeEachCell(unittest.TestCase):
    def test_decrease_values(self):
        actual = MFCC(np.array([[1, 1], [2, 2]], np.float))
        actual.enlarge_each_cell_to_be_positive()
        expected = MFCC(np.array([[0, 0], [1, 1]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_increase_values(self):
        actual = MFCC(np.array([[1, 2, 1], [-4, -3, 0]], np.float))
        actual.enlarge_each_cell_to_be_positive()
        expected = MFCC(np.array([[5, 6, 5], [0, 1, 4]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_keep_same_values(self):
        actual = MFCC(np.array([[1, 0, 1, 2], [3, 5, 0, 2], [2, 2, 2, 2]], np.float))
        actual.enlarge_each_cell_to_be_positive()
        expected = MFCC(np.array([[1, 0, 1, 2], [3, 5, 0, 2], [2, 2, 2, 2]], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))

    def test_empty_data(self):
        actual = MFCC(np.array([], np.float))
        actual.enlarge_each_cell_to_be_positive()
        expected = MFCC(np.array([], np.float))
        self.assertTrue(actual.is_equal_to(expected, float_abs_diff=0.0001))
