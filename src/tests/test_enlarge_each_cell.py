import unittest
import numpy as np
import math
from src.mfcc import MFCCParser

class TestEnlargeEachCell(unittest.TestCase):
    def test_decrease_values(self):
        not_changed = np.array([[1, 1], [2, 2]], np.float)
        changed = MFCCParser.enlarge_each_cell_to_be_positive(not_changed)
        expected = np.array([[0, 0], [1, 1]], np.float)
        self.assertEqual(True, (expected==changed).all())

    def test_increase_values(self):
        not_changed = np.array([[1, 2, 1], [-4, -3, 0]], np.float)
        changed = MFCCParser.enlarge_each_cell_to_be_positive(not_changed)
        expected = np.array([[5, 6, 5], [0, 1, 4]], np.float)
        self.assertEqual(True, (expected==changed).all())

    def test_keep_same_values(self):
        not_changed = np.array([[1, 0, 1, 2], [3, 5, 0, 2], [2, 2, 2, 2]], np.float)
        changed = MFCCParser.enlarge_each_cell_to_be_positive(not_changed)
        expected = np.array([[1, 0, 1, 2], [3, 5, 0, 2], [2, 2, 2, 2]], np.float)
        self.assertEqual(True, (expected==changed).all())

    # def test_empty_data(self):
    #     not_changed = np.array([[]], np.float)
    #     changed = MFCCParser.enlarge_each_cell_to_be_positive(not_changed)
    #     expected = np.array([[]], np.float)
    #     self.assertEqual(True, (expected==changed).all())
