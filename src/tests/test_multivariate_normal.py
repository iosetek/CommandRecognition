from scipy.stats import multivariate_normal as mvn
from src.diagonal_multivariate import DiagonalMultivariateNormal
import unittest

class TestDiagonalMultivariateNormal(unittest.TestCase):
    def test_without_multiplying(self):
        self.__test(mean=[8], diag=[2], pos=[5])
        self.__test(mean=[1, 1], diag=[1, 1], pos=[1, 1])
        self.__test(mean=[1, 1], diag=[1, 1], pos=[2, 2])
        self.__test(mean=[1, 1], diag=[2, 1], pos=[1, 1])
        self.__test(mean=[1, 2, 3], diag=[1, 1, 1], pos=[3, 2, 1])
        self.__test(mean=[1, 2, 3], diag=[1, 3, 0.5], pos=[5, 5, 5])
        self.__test(mean=[1, 2, 3, 5, 8], diag=[2, 1, 20, 13, 99], pos=[5, 3, 3, 0.2, 18])


    def __test(self, mean, diag, pos, delta=1e-10):
        expected_pdf = mvn.pdf(pos, mean, diag)
        actual_pdf = DiagonalMultivariateNormal(mean, diag).pdf(pos,)
        self.assertAlmostEqual(expected_pdf, actual_pdf, delta=delta)


    def test_really_small_values(self):
        self.__test(mean=[1] * 400, diag=[1] * 400, pos=[2] * 400, delta=1e-240)

