import unittest
import numpy as np
from mfcc import MFCCParser

parser = MFCCParser(
    window_function=np.hamming,
    window_length=0.03,
    distance_to_next_window=0.01,
    cepstral_amount=2,
    filters_amount=30,
    fft_size=2048,
    append_energy=True,
    low_freq=0,
    max_freq=None,
    preemph_filter=0.97,
    cep_lifter=22)

class TestNormalizeFrames(unittest.TestCase):
    def test_does_not_need_to_normalize(self):
        not_normalized = np.array([[1, 1], [2, 2]], np.float)
        normalized = parser.normalize_to(not_normalized, 6)
        expected = np.array([[1, 1], [2, 2]], np.float)
        self.assertEqual(True, (expected==normalized).all())

    def test_simple_normalize_to_lower(self):
        not_normalized = np.array([[2, 2], [4, 4]], np.float)
        normalized = parser.normalize_to(not_normalized, 6)
        expected = np.array([[1, 1], [2, 2]], np.float)
        self.assertEqual(True, (expected==normalized).all())

    def test_not_simple_normalize_to_lower(self):
        not_normalized = np.array([[2, 2], [6, 6]], np.float)
        normalized = parser.normalize_to(not_normalized, 14)
        expected = np.array([[1.75, 1.75], [5.25, 5.25]], np.float)
        self.assertEqual(True, (expected==normalized).all())

    def test_simple_normalize_to_greater(self):
        not_normalized = np.array([[1, 1], [2, 2]], np.float)
        normalized = parser.normalize_to(not_normalized, 12)
        expected = np.array([[2, 2], [4, 4]], np.float)
        self.assertEqual(True, (expected==normalized).all())

    def test_not_simple_normalize_to_greater(self):
        not_normalized = np.array([[1.75, 1.75], [5.25, 5.25]], np.float)
        normalized = parser.normalize_to(not_normalized, 16)
        expected = np.array([[2, 2], [6, 6]], np.float)
        self.assertEqual(True, (expected==normalized).all())

if __name__ == '__main__':
    unittest.main()