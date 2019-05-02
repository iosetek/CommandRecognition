import unittest
import numpy as np
import os

from src.command.c_gaussian import GaussianCommand
from src.command.c_mfcc import MfccCommand
from src.gaussian import Gaussian
from src.mfcc import MFCC

class TestJsonConversion(unittest.TestCase):
    def test_gaussian_command_conversion(self):
        if not os.path.exists("src/tests/testdata"):
            os.makedirs("src/tests/testdata")
        try:
            os.remove("src/tests/testdata/test_gaussian_command.json")
        except FileNotFoundError:
            pass

        pis = [3.11, 5]
        means = [np.array([2.0, 1.6], dtype=float), np.array([1.0, 2.2222], dtype=float)]
        variances = [np.array([[2, 0], [0, 3]], dtype=float), np.array([[5, 0], [0, 1.1]], dtype=float)]

        input_command_name = "test_gaussian_command"
        input_gaussians = [Gaussian(pis[0], means[0], variances[0]), Gaussian(pis[1], means[1], variances[1])]

        input_command = GaussianCommand(input_command_name, input_gaussians)
        input_command.save_to_json_file("src/tests/testdata/test_gaussian_command.json")

        output_command = GaussianCommand.from_json_file("src/tests/testdata/test_gaussian_command.json")

        self.assertEqual(input_command.get_name(), output_command.get_name())
        self.assertTrue(input_command.get_gaussians()[0].is_equal_with_gaussian(output_command.get_gaussians()[0]))
        self.assertTrue(input_command.get_gaussians()[1].is_equal_with_gaussian(output_command.get_gaussians()[1]))

    def test_mfcc_command_conversion(self):
        if not os.path.exists("src/tests/testdata"):
            os.makedirs("src/tests/testdata")
        try:
            os.remove("src/tests/testdata/test_mfcc_command.json")
        except FileNotFoundError:
            pass

        input_mfcc = np.array([
                [2, 1.72, 50, 3.111, 2.453],
                [1.444, 1.0, 11, 123, 0.001],
                [1, 2, 3, 2, 1],
                [0, 13, 1.4, 1.14, 0.0],
                [0, 0, 0, 0, 0]], np.float)

        input_command_name = "test_mfcc_command"

        input_command = MfccCommand(input_command_name, MFCC(input_mfcc))
        input_command.save_to_json_file("src/tests/testdata/test_mfcc_command.json")

        output_command = MfccCommand.from_json_file("src/tests/testdata/test_mfcc_command.json")

        self.assertEqual(input_command.get_name(), output_command.get_name())
        self.assertTrue(input_command.get_data().is_equal_to(output_command.get_data()))


