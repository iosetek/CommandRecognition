from src.diagonal_multivariate import DiagonalMultivariateNormal
import random
import numpy as np

class Gaussian:
    """
    Gaussian object is simple representation of ND gauss distribution.
    """
    def __init__(self, mean, cov):
        self.__mean = mean
        self.__cov = cov
        self.__validate()
        self.__g = DiagonalMultivariateNormal(mean, cov)


    def __validate(self):
        if not isinstance(self.__mean, np.ndarray) or not isinstance(self.__cov, np.ndarray):
            raise Gaussian.MeanOrCovarianceIsNotNumpyArrayException
        if len(self.__mean) == 0 or len(self.__cov) == 0:
            raise Gaussian.ZeroDimensionsException
        if len(self.__mean.shape) != 1:
            raise Gaussian.MeanMatrixIsNotSingleDimensionedException
        if len(self.__cov.shape) != 1:
            raise Gaussian.CovarianceMatrixIsNotDimensionedException
        dimensions = len(self.__cov)
        if len(self.__mean) != dimensions:
            raise Gaussian.MeanAndCovarianceHaveDifferentSizesException


    @classmethod
    def generate_random_gaussian(cls, n_dimensions, one_vector):
        mean = np.array([0] * n_dimensions, dtype=float)
        sigma = np.array([0] * n_dimensions, dtype=float)

        for i in range(n_dimensions):
            # TODO: Multivariate normal should accept 0 values, not require just a small value.
            mean[i] = one_vector.component(i) + random.randint(-100, 100) / 50
            # sigma[i][i] = random.randint(100, 1000) / 0.5
            sigma[i] = 3e1

        return Gaussian(mean, sigma)


    # TODO Name it correctly
    def get_probability_for_position(self, pos, em_reserve=0):
        return self.__g.pdf(pos, reserve=em_reserve)


    def get_mean(self):
        return self.__mean


    # TODO Verify this name
    def get_covariance(self):
        return self.__cov


    def is_equal_to(self, gaussian, tolerance=0.0001):
        if len(self.__mean) != len(gaussian.get_mean()):
            return False
        if len(self.__cov) != len(gaussian.get_covariance()):
            return False
        if sum(abs(self.__mean - gaussian.get_mean())) > tolerance:
            return False
        if sum(abs(self.__cov - gaussian.get_covariance())) > tolerance:
            return False

        return True

    
    class ZeroDimensionsException(Exception):
        pass


    class CovarianceMatrixIsNotDimensionedException(Exception):
        pass


    class MeanMatrixIsNotSingleDimensionedException(Exception):
        pass


    class CovarianceMatrixIsNotSquaredException(Exception):
        pass


    class MeanAndCovarianceHaveDifferentSizesException(Exception):
        pass


    class MeanOrCovarianceIsNotNumpyArrayException(Exception):
        pass
