import unittest
import numpy as np
from src.mfcc import MFCCParser

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

class TestConvertFrames(unittest.TestCase):
    def test_empty_data(self):
        # TODO: check if convert can handle situation with empty data
        print("TODO")

    def test_equal_number_of_frames(self):
        # TODO: if data has equal number of frames as conversion parameter it should be the same after conversion
        not_converted = np.array([[0, 2], [3, 1], [2, 2]], np.float)
        converted = parser.convert_to_n_frames(not_converted, 3)
        expected = np.array([[0, 2], [3, 1], [2, 2]], np.float)

        self.assertEqual(True, (expected==converted).all())

    def test_simple_data_reduction(self):
        # TODO: case where data has more frames than covnersion parameter
        not_converted = np.array([[0, 0], [2, 2], [4, 4], [6, 6]], np.float)
        converted = parser.convert_to_n_frames(not_converted, 2)
        expected = np.array([[1, 1], [5, 5]], np.float)

        self.assertEqual(True, (expected==converted).all())

    def test_not_simple_data_reduction(self):
        # TODO: case where data has more frames than covnersion parameter
        not_converted = np.array([[0, 0], [2, 2], [4, 4], [6, 6], [8, 8]], np.float)
        converted = parser.convert_to_n_frames(not_converted, 2)
        expected = np.array([[1.6, 1.6], [6.4, 6.4]], np.float)

        self.assertEqual(True, (expected==converted).all())

    def test_simple_data_elongation(self):
        # TODO: case where data has less frames than conversion parameter
        not_converted = np.array([[2, 2], [4, 4]], np.float)
        converted = parser.convert_to_n_frames(not_converted, 4)
        expected = np.array([[2, 2], [2, 2], [4, 4], [4, 4]], np.float)

        self.assertEqual(True, (expected==converted).all())

    def test_not_simple_data_elongation(self):
        # TODO: case where data has less frames than conversion parameter
        not_converted = np.array([[2, 2], [4, 4]], np.float)
        converted = parser.convert_to_n_frames(not_converted, 5)
        expected = np.array([[2, 2], [2, 2], [3, 3], [4, 4], [4, 4]], np.float)

        self.assertEqual(True, (expected==converted).all())

    def test_another_not_simple_data_elongation(self):
        # TODO: case where data has less frames than conversion parameter
        not_converted = np.array([[2, 2], [3, 3], [4, 4], [5, 5]], np.float)
        converted = parser.convert_to_n_frames(not_converted, 5)
        expected = np.array([[2, 2], [2.75, 2.75], [3.5, 3.5], [4.25, 4.25], [5, 5]], np.float)

        self.assertEqual(True, (expected==converted).all())

if __name__ == '__main__':
    unittest.main()