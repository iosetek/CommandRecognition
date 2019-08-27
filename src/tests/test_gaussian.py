from src.gaussian import Gaussian
import unittest
import numpy as np

class TestEnlargeEachCell(unittest.TestCase):
    def test_probability_for_position(self):
        self.assertTrue(False, "TODO")


    def test_get_random_gaussian(self):
        self.assertTrue(False, "TODO")


    def test_create_one_dimensional_gaussian(self):
        mean = np.array([3])
        cov = np.array([[3]])
        Gaussian(mean, cov)


    def test_create_two_dimensional_gaussian(self):
        mean = np.array([3, 2])
        cov = np.array([[3, 0], [0, 3]])
        Gaussian(mean, cov)


    def test_create_three_dimensional_gaussian(self):
        mean = np.array([3, 2, 5])
        cov = np.array([[3, 0, 0], [0, 3, 0], [0, 0, 3]])
        Gaussian(mean, cov)


    def test_zero_dimension_mean(self):
        mean = np.array([])
        cov = np.array([3])
        with self.assertRaises(Gaussian.ZeroDimensionsException):
            Gaussian(mean, cov)


    def test_zero_dimension_covariance(self):
        mean = np.array([3])
        cov = np.array([])
        with self.assertRaises(Gaussian.ZeroDimensionsException):
            Gaussian(mean, cov)


    def test_empty_list_for_mean_and_covariance(self):
        mean = np.array([])
        cov = np.array([])
        with self.assertRaises(Gaussian.ZeroDimensionsException):
            Gaussian(mean, cov)


    def test_mean_not_numpy_array(self):
        mean = [1, 3]
        cov = np.array([[5, 0], [0, 5]])
        with self.assertRaises(Gaussian.MeanOrCovarianceIsNotNumpyArrayException):
            Gaussian(mean, cov)


    def test_covariance_not_numpy_array(self):
        mean = np.array([1, 3])
        cov = [[5, 0], [0, 5]]
        with self.assertRaises(Gaussian.MeanOrCovarianceIsNotNumpyArrayException):
            Gaussian(mean, cov)


    def test_not_numpy_array(self):
        mean = [1, 3]
        cov = [[5, 0], [0, 5]]
        with self.assertRaises(Gaussian.MeanOrCovarianceIsNotNumpyArrayException):
            Gaussian(mean, cov)


    def test_two_dimensional_mean_array(self):
        mean = np.array([[3, 2], [5, 1]])
        cov = np.array([[3, 5], [1, 2]])
        with self.assertRaises(Gaussian.MeanMatrixIsNotSingleDimensionedException):
            Gaussian(mean, cov)


    def test_not_squared_covariance_array(self):
        mean = np.array([3, 2])
        cov = np.array([[3, 5, 3], [1, 2, 2]])
        with self.assertRaises(Gaussian.CovarianceMatrixIsNotSquaredException):
            Gaussian(mean, cov)


    def test_not_two_dimensional_covariance_matrix(self):
        mean = np.array([3])
        cov = np.array([3])
        with self.assertRaises(Gaussian.CovarianceMatrixIsNotTwoDimensional):
            Gaussian(mean, cov)


    def test_different_dimensions_for_mean_and_covariance(self):
        mean = np.array([3])
        cov = np.array([[3, 5], [1, 2]])
        with self.assertRaises(Gaussian.MeanAndCovarianceHaveDifferentSizesException):
            Gaussian(mean, cov)


    def test_equal_one_dimensional_gaussians(self):
        meanA = np.array([3], dtype=float)
        covA = np.array([[3]], dtype=float)
        meanB = np.array([3], dtype=float)
        covB = np.array([[3.00001]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertTrue(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))


    def test_equal_two_dimensional_gaussians(self):
        meanA = np.array([3, 5], dtype=float)
        covA = np.array([[3, 5], [1, 2]], dtype=float)
        meanB = np.array([3, 5.000001], dtype=float)
        covB = np.array([[3.00001, 5], [1, 2]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertTrue(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))


    def test_equal_three_dimensional_gaussians(self):
        meanA = np.array([3, 5, 4], dtype=float)
        covA = np.array([[10, 5, 2], [1, 20, 1], [3, 3, 40]], dtype=float)
        meanB = np.array([3, 5.000001, 3.999999], dtype=float)
        covB = np.array([[10.00001, 5, 1.99999], [1, 20, 1.00001], [3, 2.99999, 40]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertTrue(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))


    def test_equal_one_dimensional_gaussians_with_too_small_tolerance(self):
        meanA = np.array([3], dtype=float)
        covA = np.array([[3]], dtype=float)
        meanB = np.array([3], dtype=float)
        covB = np.array([[3.001]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertFalse(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))


    def test_equal_two_dimensional_gaussians_with_too_small_tolerance(self):
        meanA = np.array([3, 5], dtype=float)
        covA = np.array([[3, 5], [1, 2]], dtype=float)
        meanB = np.array([3, 5.1], dtype=float)
        covB = np.array([[3.00001, 5], [1, 2]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertFalse(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))


    def test_equal_three_dimensional_gaussians_with_too_small_tolerance(self):
        meanA = np.array([3, 5, 4], dtype=float)
        covA = np.array([[10, 5, 2], [1, 20, 1], [3, 3, 40]], dtype=float)
        meanB = np.array([3, 5.000001, 3.999999], dtype=float)
        covB = np.array([[10.00001, 5, 1.999], [1, 20, 1.00001], [3, 2.99999, 40]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertFalse(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))


    def test_equal_of_two_gaussians_with_different_dimensions(self):
        meanA = np.array([3], dtype=float)
        covA = np.array([[10]], dtype=float)
        meanB = np.array([3, 5.000001, 3.999999], dtype=float)
        covB = np.array([[10.00001, 5, 1.999], [1, 20, 1.00001], [3, 2.99999, 40]], dtype=float)
        first_gaussian = Gaussian(meanA, covA)
        second_gaussian = Gaussian(meanB, covB)
        self.assertFalse(first_gaussian.is_equal_to(second_gaussian, tolerance=0.0001))