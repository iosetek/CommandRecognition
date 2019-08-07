import unittest
import numpy as np
import math
from src.super_vector import SuperVector

class TestEnlargeEachCell(unittest.TestCase):
    def test_equal_vectors(self):
        vectorA = SuperVector([1, 2, 3])
        vectorB = SuperVector([1, 2, 3])
        self.assertTrue(vectorA.is_equal_to(vectorB))

    def test_initialization_from_2d_array(self):
        vectorA = SuperVector.init_from_mfcc([[1, 2], [3, 4]])
        vectorB = SuperVector([1, 2, 3, 4])
        self.assertTrue(vectorA.is_equal_to(vectorB))

    def test_not_equal_vectors_with_same_length(self):
        vectorA = SuperVector([1, 2, 3])
        vectorB = SuperVector([1, 2, 4])
        self.assertFalse(vectorA.is_equal_to(vectorB))

    def test_tolerance(self):
        vectorA = SuperVector([1, 2, 3])
        vectorB = SuperVector([1, 2, 4])
        self.assertTrue(vectorA.is_equal_to(vectorB, tolerance=1))

    def test_equality_of_vectors_with_different_length(self):
        vectorA = SuperVector([1, 2, 3])
        vectorB = SuperVector([1, 2, 3, 4])
        self.assertFalse(vectorA.is_equal_to(vectorB))

    def test_equality_of_empty_vectors(self):
        vectorA = SuperVector([])
        vectorB = SuperVector([])
        self.assertTrue(vectorA.is_equal_to(vectorB))
